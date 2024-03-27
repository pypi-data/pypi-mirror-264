from functools import partial
from loguru import logger
from typing import Callable, Iterator, List, Optional, Tuple
import copy
import torch
from torch import Tensor
from torch.nn import Module
import torch.distributed as dist
from torch.distributed import Work
from torch.nn.parameter import Parameter
from decent_dp.topo import TopologyReg, Topology
from torch.utils.hooks import RemovableHandle
from torch.optim import Optimizer
from torch.optim.lr_scheduler import LRScheduler

class DecentralizedDataParallel(Module):
    def __init__(self,
                 model: Module,
                 topology: str = 'ring',
                 fused_optim: bool = False,
                 optim_fn: Optional[Callable] = None,
                 lr_schd_fn: Optional[Callable[[Optimizer], LRScheduler]] = None,
                 param_as_bucket_view: bool = True,
                 bucket_size_in_mb: int = 10):
        super(DecentralizedDataParallel, self).__init__()
        self._model = model
        self._fused_optim = fused_optim
        self._optim_fn = optim_fn
        self._lr_schd_fn = lr_schd_fn
        self._bucket_size = bucket_size_in_mb * 1024 * 1024
        self._param_as_bucket_view = param_as_bucket_view

        self._rank: int = -1
        self._world_size: int = -1
        self._initialize_ddp()

        if torch.cuda.is_available():
            self._model.cuda()
        
        if self._fused_optim and (self._optim_fn is None):
            logger.error('fused optimizer is enabled, but no optimizer is provided')
            raise ValueError()
        if self._fused_optim and (self._lr_schd_fn is None):
            if self._rank == 0:
                logger.warning('fused optimizer is enabled, but no learning rate scheduler is provided')

        
        self._topo: Optional[Topology] = None
        self._params: List[Tensor] = list([x for x in self._model.parameters() if x.requires_grad])
        self._used_param_ids: List[int] = []
        self._used_params: List[Tensor] = []
        self._step: int = -1
        self._comm_op: Optional[Work] = None
        self._is_initialized: bool = False
        self._last_param_cnt: List[int] = []
        self._last_param_cnt_b: List[int] = []
        self._is_gpu_available = torch.cuda.is_available()
        self._optim_hook: Optional[Callable] = None
        self._first_run_hooks: List[RemovableHandle] = []
        self._ddp_hooks: List[RemovableHandle] = []
        self._buckets: List[List[Tensor]] = []
        self._comm_buffers: List[List[Tensor]] = []
        self._comm_blocks: List[Tensor] = []
        self._param_blocks: List[Tensor] = []
        self._grad_blocks: List[Tensor] = []
        self._optims: List[Optimizer] = []
        self._lr_schds: List[LRScheduler] = []
        self._ext_optim: Optional[Optimizer] = None

        
        self._initialize_topo(topology)
        self._create_hooks()
        self._sync_at_start()
    
    def _initialize_ddp(self):
        if not (dist.is_available() and dist.is_initialized()):
            logger.error('PyTorch distributed is not initialized')
            raise RuntimeError()
        self._rank = dist.get_rank()
        self._world_size = dist.get_world_size()
        if self._rank == 0:
            logger.info(f"Using Decentralized Data Parallel [# workers: {self._world_size}]")
            logger.info(f"Add method 'pre_average_hook' to the optimizer to register a hook that is called before averaging")
    
    def _initialize_topo(self, topology: str):
        self._topo = TopologyReg.registry[topology]()
        self._topo.create_edges()
    
    @torch.no_grad()
    def _sync_at_start(self):
        for param in self._params:
            dist.broadcast(param, 0)
    
    @torch.no_grad()
    def global_avg(self):
        torch._foreach_div_([x.data for x in self._params], self._world_size)
        dist.all_reduce_coalesced([x.data for x in self._params], op=dist.ReduceOp.SUM)
    
    def _create_hooks(self):
        for pid, param in enumerate(self._params):
            self._first_run_hooks.append(
                param.register_post_accumulate_grad_hook(
                    partial(
                        lambda data, pid: self._first_run_fn(data, pid),
                        pid=pid
                    )
                )
            )
    
    @torch.no_grad()
    def _first_run_fn(self, _: Tensor, pid: int):
        self._used_param_ids.append(pid)

    @torch.no_grad()
    def _ddp_fn(self, _: Tensor, bucket_id: int):
        self._last_param_cnt[bucket_id] -= 1
        if self._last_param_cnt[bucket_id] == 0:
            self._last_param_cnt[bucket_id] = self._last_param_cnt_b[bucket_id]
            if self._comm_op[bucket_id] is not None:
                self._comm_op[bucket_id].wait()
                self._comm_op[bucket_id] = None
                edge = self._topo.get_current_edge(self._step)
                weight = edge['weights'][edge['ranks'].index(self._rank)]

                if (not self._fused_optim) and (self._ext_optim is not None) \
                    and (hasattr(self._ext_optim, 'pre_average_hook')) and (bucket_id == len(self._buckets) - 1):
                    self._ext_optim.pre_average_hook(edge, weight)
                
                if self._fused_optim and (hasattr(self._optims[bucket_id], 'pre_average_hook')):
                    self._optims[bucket_id].pre_average_hook(edge, weight)

                if not self._param_as_bucket_view:
                    torch._foreach_mul_(self._buckets[bucket_id], weight - (1 - weight) / (len(edge['ranks']) - 1))
                    torch._foreach_add_(self._buckets[bucket_id], self._comm_buffers[bucket_id])
                else:
                    self._param_blocks[bucket_id].mul_(weight - (1 - weight) / (len(edge['ranks']) - 1))
                    self._param_blocks[bucket_id].add_(self._comm_blocks[bucket_id])

            if self._fused_optim:
                # logger.debug("fused here")
                self._optims[bucket_id].step()
                self._optims[bucket_id].zero_grad()
                if self._lr_schds[bucket_id] is not None:
                    self._lr_schds[bucket_id].step()
                
                # launch the next communication if fused optimizer is used
                if not self._param_as_bucket_view:
                    torch._foreach_copy_(self._comm_buffers[bucket_id], self._buckets[bucket_id])
                else:
                    self._comm_blocks[bucket_id].copy_(self._param_blocks[bucket_id])
                edge = self._topo.get_current_edge(self._step + 1)
                weight = edge['weights'][edge['ranks'].index(self._rank)]
                self._comm_blocks[bucket_id].mul_((1 - weight) / (len(edge['ranks']) - 1))

                self._comm_op[bucket_id] = dist.all_reduce(
                    self._comm_blocks[bucket_id],
                    op=dist.ReduceOp.SUM,
                    group=edge['group'],
                    async_op=True
                )
    
    def _initialize_params(self):
        verify = [[[i, self._params[i].numel()] for i in self._used_param_ids]]
        result = [None] if self._rank != 0 else verify
        dist.broadcast_object_list(result, src=0)

        if not all([x == y for x, y in zip(verify[0], result[0])]):
            logger.error('Number/Order of elements in used parameters is different on different nodes')
            raise RuntimeError()

        for hook in self._first_run_hooks:
            hook.remove()
        del self._first_run_hooks

        
        # keep the last occurance of each parameter
        used_param_ids_unique = []
        for id in reversed(self._used_param_ids):
            if id not in used_param_ids_unique:
                used_param_ids_unique.append(id)
        used_param_ids_unique = list(reversed(used_param_ids_unique))

        # total number of parameters
        total_size = sum([self._params[i].numel() for i in used_param_ids_unique])
        
        # split the parameters into roughly equal buckets, and register hooks on the last parameter of each bucket
        start = 0
        size = 0
        for i in range(len(used_param_ids_unique)):
            size += self._params[used_param_ids_unique[i]].numel() * self._params[used_param_ids_unique[i]].element_size()
            if (size >= self._bucket_size) or (i == len(used_param_ids_unique) - 1):
                self._ddp_hooks.append(
                    self._params[used_param_ids_unique[i]].register_post_accumulate_grad_hook(
                        partial(
                            lambda data, bucket_id: self._ddp_fn(data, bucket_id),
                            bucket_id=len(self._ddp_hooks)
                        )
                    )
                )
                self._last_param_cnt.append(self._used_param_ids.count(used_param_ids_unique[i]))
                self._buckets.append([self._params[j] for j in used_param_ids_unique[start:i+1]])
                if self._fused_optim:
                    self._optims.append(self._optim_fn(self._buckets[-1]))
                    self._lr_schds.append(self._lr_schd_fn(self._optims[-1]) if self._lr_schd_fn is not None else None)
                size = 0
                start = i + 1
        
        self._last_param_cnt_b = copy.deepcopy(self._last_param_cnt)
        size_dict = {}

        for i in range(len(self._buckets)):
            total_size = sum([p.numel() for p in self._buckets[i]])

            # make sure the total size is unique
            while total_size in size_dict:
                total_size += 1
            size_dict[total_size] = True

            comm_buffer = torch.empty(total_size, device=self._buckets[i][0].device, requires_grad=False, dtype=self._buckets[i][0].dtype)
            if self._param_as_bucket_view:
                self._param_blocks.append(torch.empty(total_size, device=self._buckets[i][0].device, requires_grad=True, dtype=self._buckets[i][0].dtype))
                self._grad_blocks.append(torch.empty(total_size, device=self._buckets[i][0].device, requires_grad=False, dtype=self._buckets[i][0].dtype))
                self._param_blocks[-1].grad = self._grad_blocks[-1]
                start = 0
                for j in range(len(self._buckets[i])):
                    size = self._buckets[i][j].numel()
                    self._param_blocks[-1].narrow(0, start, size).copy_(self._buckets[i][j].view(-1))
                    self._grad_blocks[-1].narrow(0, start, size).copy_(self._buckets[i][j].grad.view(-1))
                    self._buckets[i][j].data = self._param_blocks[-1].narrow(0, start, size).view_as(self._buckets[i][j])
                    self._buckets[i][j].grad = self._grad_blocks[-1].narrow(0, start, size).view_as(self._buckets[i][j])
                    start += size

            self._comm_buffers.append([])
            self._comm_blocks.append(comm_buffer)
            start = 0
            for j in range(len(self._buckets[i])):
                size = self._buckets[i][j].numel()
                self._comm_buffers[-1].append(comm_buffer.narrow(0, start, size).view_as(self._buckets[i][j]))
                # self._buckets[i][j].__setattr__('comm_buffer', self._comm_buffers[-1][-1])
                start += size
        
        self._comm_op = [None] * len(self._buckets)


    @torch.no_grad()
    def sync(self):
        self._step += 1
        if not self._is_initialized:
            self._initialize_params()
            self._is_initialized = True

            # manually trigger the first communication
            if self._fused_optim:
                for i in range(len(self._buckets)):
                    self._optims[i].step()
                    self._optims[i].zero_grad()
                    if self._lr_schds[i] is not None:
                        self._lr_schds[i].step()
                    if not self._param_as_bucket_view:
                        torch._foreach_copy_(self._comm_buffers[i], self._buckets[i])
                    else:
                        self._comm_blocks[i].copy_(self._param_blocks[i])
                    edge = self._topo.get_current_edge(self._step)
                    weight = edge['weights'][edge['ranks'].index(self._rank)]
                    self._comm_blocks[i].mul_((1 - weight) / (len(edge['ranks']) - 1))
                    self._comm_op[i] = dist.all_reduce(
                        self._comm_blocks[i],
                        op=dist.ReduceOp.SUM,
                        group=edge['group'],
                        async_op=True
                    )
        
        if not self._fused_optim:
            for i in range(len(self._buckets)):
                if not self._param_as_bucket_view:
                    torch._foreach_copy_(self._comm_buffers[i], self._buckets[i])
                else:
                    self._comm_blocks[i].copy_(self._param_blocks[i])
            edge = self._topo.get_current_edge(self._step)
            weight = edge['weights'][edge['ranks'].index(self._rank)]
            for i in range(len(self._buckets)):
                self._comm_blocks[i].mul_((1 - weight) / (len(edge['ranks']) - 1))
            for i in range(len(self._buckets)):
                self._comm_op[i] = dist.all_reduce(
                    self._comm_blocks[i],
                    op=dist.ReduceOp.SUM,
                    group=edge['group'],
                    async_op=True
                )
    
    def register_pre_average_hook(self, optim: Optimizer):
        self._ext_optim = optim

    def train(self, mode: bool = True):
        self._model.train(mode)
    
    def eval(self):
        self._model.eval()

    def forward(self, *args, **kwargs):
        return self._model(*args, **kwargs)

    def parameters(self, recurse: bool = True) -> Iterator[Parameter]:
        yield from self._model.parameters(recurse)
    
    def named_parameters(self, prefix: str = '', recurse: bool = True, remove_duplicate: bool = True) -> Iterator[Tuple[str, Parameter]]:
        return super().named_parameters(prefix, recurse, remove_duplicate)
