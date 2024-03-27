"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import warnings
from functools import partial
from itertools import chain
from typing import Any, Callable, Dict, List, Mapping

import networkx as nx
from tabulate import tabulate

from .graph import OnnxGraph
from .passes import L1, L2, L3, PASSES


class PassManager:
    """Ordered optimization pass list.

    Args:
        include (List[str], Optional): a list of pattern to select passes.
            Defaults to select all passes.
        exclude (List[str], Optional): a list of pattern to deselect passes.
            Defaults to None.
    """

    def __init__(
        self,
        include: List[str] = None,
        exclude: List[str] = None,
        configs: Dict[str, Any] = None,
    ) -> None:
        self.activated: List[Callable[[OnnxGraph], OnnxGraph]] = []
        if not include:
            passes = [PASSES.get(i) for i in chain(L1, L2, L3)]
        else:
            passes = [PASSES.get(i) for i in include]
        if exclude:
            passes = list(filter(lambda i: i not in exclude, passes))
        self.activated = list(filter(lambda p: p is not None, passes))
        if configs:
            self._assign_config_to_pass(configs)

    def _assign_config_to_pass(self, configs: Dict[str, Any]):
        for key, config in configs.items():
            index = -1
            if ":" in key:
                key, index = key.split(":", 2)
                index = int(index)
            if not isinstance(config, Mapping):
                warnings.warn(
                    f"config {key}:{index} must be a dict, but got {type(config)}"
                )
                continue
            candidates = [i for i in self.activated if i.__name__ == key]
            if index >= 0 and index >= len(candidates):
                warnings.warn(
                    f"config {key}:{index} exceeds the boundary. "
                    f"Number of {key} is {len(candidates)}"
                )
                continue
            if index >= 0:
                candidates = [candidates[index]]
            for func in candidates:
                pos = self.activated.index(func)
                self.activated[pos] = partial(func, **config)
                self.activated[pos].__name__ = key
                self.activated[pos].__deps__ = func.__deps__

    def _expand_deps(self, deps):
        root = nx.DiGraph()
        root.add_nodes_from(deps)
        leaves: list = deps.copy()
        while leaves:
            leaf = leaves.pop(0)
            children = PASSES.get(leaf).__deps__
            leaves.extend(children)
            root.add_edges_from([(leaf, child) for child in children])
            try:
                cycles = nx.find_cycle(root, leaf)
            except nx.NetworkXNoCycle:
                continue
            else:
                print(f"[E] Cyclic dependencies found!: {cycles}")
                break
        yield from reversed(list(nx.topological_sort(root)))

    def optimize(self, graph: OnnxGraph, strict: bool = False) -> OnnxGraph:
        """Invoke passes on the input graph.

        Args:
            graph (OnnxGraph): See :class:`OnnxGraph`.
            strict (bool): Break if any pass fails.
        """
        for opt in self.activated:
            try:
                for deps in self._expand_deps(opt.__deps__):
                    graph = PASSES.get(deps)(graph)
                graph = opt(graph)
            except Exception as ex:  # pylint: disable=broad-exception-caught
                print(f"[E] {opt.__name__} failed: {ex}")
                if strict:
                    raise
        return graph

    @classmethod
    def print_all(cls):
        """Print the name of all passes."""
        print(PASSES, flush=True)

    @classmethod
    def print_l1(cls):
        """Print the name of all L1 passes."""
        print(L1, flush=True)

    @classmethod
    def print_l2(cls):
        """Print the name of all L2 passes."""
        print(L2, flush=True)

    def __repr__(self) -> str:
        return tabulate(
            [[i.__name__, i] for i in self.activated], ["PASS", "Func"], "grid"
        )
