import os
import math
from loguru import logger
import torch.distributed as dist
from typing import Any, Callable, Dict, List


class Topology:
    def __init__(self):
        self._world_size = dist.get_world_size()
        self._local_world_size = int(os.environ["LOCAL_WORLD_SIZE"])
        self._n_nodes = self._world_size // self._local_world_size
        self._rank = -1
        self.registry = {}

    def create_edges(self):
        if not dist.is_initialized():
            logger.error("Distributed environment is not initialized")
            raise RuntimeError()
        self._rank = dist.get_rank()        
        self._all_edges = self.get_edges()
        self._validate_edges(self._all_edges)

        # Create default group
        all_ranks = [i for i in range(self._world_size)]
        self.registry['all'] = dist.new_group(all_ranks)

        for idx in range(len(self._all_edges)):
            for edge in self._all_edges[idx]:
                identifier = str(edge['ranks'])
                if not (identifier in self.registry):
                    self.registry[identifier] = dist.new_group(edge['ranks'])
                edge['group'] = self.registry[identifier]
        
        self._edges = []
        for idx in range(len(self._all_edges)):
            for edge in self._all_edges[idx]:
                if self._rank in edge['ranks']:
                    self._edges.append(edge)
                    break

    def _validate_edges(self, edges: List[List[Dict[str, Any]]]):
        for idx in range(len(edges)):
            used = [False] * self._world_size
            for edge in edges[idx]:
                for rank in edge['ranks']:
                    if used[rank]:
                        logger.error(f"Topology is not valid, node {rank} is used more than once in one iteration")
                        raise ValueError()
                    used[rank] = True
                # validate that ranks are sorted
                if not all([x < y for x, y in zip(edge['ranks'][:-1], edge['ranks'][1:])]):
                    logger.error(f"Topology is not valid, ranks are not sorted")
                    raise ValueError()
            if not all(used):
                logger.error(f"Topology is not valid, some nodes are not used in one iteration")
                raise ValueError()

    def get_current_edge(self, step: int) -> Dict[str, Any]:
        return self._edges[step % len(self._edges)]

    def get_edges(self) -> List[List[Dict[str, Any]]]: ...

class TopologyReg:
    registry: Dict[str, Topology] = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        def _register(topology: Topology) -> Topology:
            if name in cls.registry:
                raise ValueError(f"Topology {name} is already registered")
            if not issubclass(topology, Topology):
                raise ValueError(f"Topology {name} must extend class Topology")
            cls.registry[name] = topology
            return topology
        return _register

@TopologyReg.register('ring')
class RingTopology(Topology):
    def get_edges(self) -> List[List[Dict[str, Any]]]:
        if self._world_size % 2 != 0:
            logger.error('Ring topology is not supported for odd world size')
            raise ValueError()

        edges = [[], []]
        # Odd iterations
        for i in range(0, self._world_size, 2):
            edges[0].append({
                'ranks': sorted([i, (i + 1) % self._world_size]),
                'weights': [0.5, 0.5]
            })
        # Even iterations
        for i in range(0, self._world_size, 2):
            edges[1].append({
                'ranks': sorted([i, (i - 1 + self._world_size) % self._world_size]),
                'weights': [0.5, 0.5]
            })
        return edges

@TopologyReg.register('one-peer-exp')
class OnePeerExpTopology(Topology):
    def get_edges(self) -> List[List[Dict[str, Any]]]:
        rounds = round(math.log2(self._world_size))
        if self._world_size != 2 ** rounds:
            logger.error('Exponential topology is only supported for 2^x world size')
            raise ValueError()

        edges = []
        for i in range(rounds):
            edges.append([])
            used = [False] * self._world_size
            for j in range(self._world_size):
                if not used[j]:
                    used[j] = True
                    used[(j + 2 ** i) % self._world_size] = True
                    edges[i].append({
                        'ranks': sorted([j, (j + 2 ** i) % self._world_size]),
                        'weights': [0.5, 0.5]
                    })
        return edges

@TopologyReg.register('exp-ring')
class ExpRingTopology(Topology):
    def get_edges(self) -> List[List[Dict[str, Any]]]:
        if self._local_world_size < 4:
            logger.error('Exponential ring topology is not supported for local world size < 4')
            raise ValueError()

        rounds = round(math.log2(self._n_nodes))
        if (self._n_nodes != 2 ** rounds) or (rounds < 1):
            logger.error('Exponential ring topology is only supported for 2^x local world size and x > 1')
            raise ValueError()

        factor = 0.2
        edges = []
        cnt = 0
        for i in range(rounds):
            edges.append([])
            edges.append([])
            used = [False] * self._n_nodes
            for j in range(self._n_nodes):
                if not used[j]:
                    used[j] = True
                    t = (j + 2 ** i) % self._n_nodes
                    used[t] = True
                    if cnt % 2 == 0:
                        edges[-1].append({
                            'ranks': [j * self._local_world_size, t * self._local_world_size],
                            'weights': [factor, factor]
                        })
                        edges[-1].append({
                            'ranks': [(j + 1) * self._local_world_size - 1, (t + 1) * self._local_world_size - 1],
                            'weights': [factor, factor]
                        })
                        edges[-1].append({
                            'ranks': list(range(j * self._local_world_size + 1, (j + 1) * self._local_world_size - 1)),
                            'weights': [1 / (self._local_world_size - 2)] * (self._local_world_size - 2)
                        })
                        edges[-1].append({
                            'ranks': list(range(t * self._local_world_size + 1, (t + 1) * self._local_world_size - 1)),
                            'weights': [1 / (self._local_world_size - 2)] * (self._local_world_size - 2)
                        })
                        edges[-2].append({
                            'ranks': list(range(j * self._local_world_size, (j + 1) * self._local_world_size)),
                            'weights': [1 / self._local_world_size] * self._local_world_size
                        })
                        edges[-2].append({
                            'ranks': list(range(t * self._local_world_size, (t + 1) * self._local_world_size)),
                            'weights': [1 / self._local_world_size] * self._local_world_size
                        })
                    else:
                        edges[-1].append({
                            'ranks': list(range(j * self._local_world_size, (j + 1) * self._local_world_size)),
                            'weights': [1 / self._local_world_size] * self._local_world_size
                        })
                        edges[-1].append({
                            'ranks': list(range(t * self._local_world_size, (t + 1) * self._local_world_size)),
                            'weights': [1 / self._local_world_size] * self._local_world_size
                        })
                        edges[-2].append({
                            'ranks': [j * self._local_world_size, t * self._local_world_size],
                            'weights': [factor, factor]
                        })
                        edges[-2].append({
                            'ranks': [(j + 1) * self._local_world_size - 1, (t + 1) * self._local_world_size - 1],
                            'weights': [factor, factor]
                        })
                        edges[-2].append({
                            'ranks': list(range(j * self._local_world_size + 1, (j + 1) * self._local_world_size - 1)),
                            'weights': [1 / (self._local_world_size - 2)] * (self._local_world_size - 2)
                        })
                        edges[-2].append({
                            'ranks': list(range(t * self._local_world_size + 1, (t + 1) * self._local_world_size - 1)),
                            'weights': [1 / (self._local_world_size - 2)] * (self._local_world_size - 2)
                        })
                    cnt += 1
        return edges