"""Simpson's One-Third Composite Rule: repeated parabolic (Lagrange P2) quadrature.

Unlike the Simple variant, `n` is a free parameter here — it must be a positive
even integer, since the algorithm groups subintervals into consecutive pairs
and fits a parabola across each pair. No integration/derivation library
primitives are used; every step is implemented explicitly.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

FunctionOfX = Callable[[float], float]


@dataclass(frozen=True, slots=True)
class QuadratureNode:
    x: float
    y: float
    weight: int


@dataclass(frozen=True, slots=True)
class SimpsonCompositeResult:
    lower_bound: float
    upper_bound: float
    step_size: float
    subintervals: int
    nodes: tuple[QuadratureNode, ...]
    approximation: float

    @property
    def evaluation_count(self) -> int:
        return len(self.nodes)


def _validate_inputs(lower_bound: float, upper_bound: float, subintervals: int) -> None:
    if upper_bound <= lower_bound:
        raise ValueError("upper_bound must be strictly greater than lower_bound")
    if subintervals <= 0:
        raise ValueError("subintervals (n) must be a positive integer")
    if subintervals % 2 != 0:
        raise ValueError("subintervals (n) must be even for Simpson 1/3 Composite")


def _compute_step_size(lower_bound: float, upper_bound: float, subintervals: int) -> float:
    return (upper_bound - lower_bound) / subintervals


def _node_weight(index: int, subintervals: int) -> int:
    if index == 0 or index == subintervals:
        return 1
    return 4 if index % 2 == 1 else 2


def _generate_nodes(
    lower_bound: float, step_size: float, subintervals: int, function: FunctionOfX
) -> tuple[QuadratureNode, ...]:
    nodes = []
    for index in range(subintervals + 1):
        x = lower_bound + index * step_size
        nodes.append(QuadratureNode(x=x, y=function(x), weight=_node_weight(index, subintervals)))
    return tuple(nodes)


def _weighted_sum(nodes: tuple[QuadratureNode, ...], step_size: float) -> float:
    return (step_size / 3.0) * sum(node.weight * node.y for node in nodes)


def integrate(
    function: FunctionOfX, lower_bound: float, upper_bound: float, subintervals: int
) -> SimpsonCompositeResult:
    """Approximate the definite integral of `function` over [lower_bound, upper_bound]
    using `subintervals` (must be even) panels of Simpson 1/3 Simple, chained together.
    """
    _validate_inputs(lower_bound, upper_bound, subintervals)

    step_size = _compute_step_size(lower_bound, upper_bound, subintervals)
    nodes = _generate_nodes(lower_bound, step_size, subintervals, function)
    approximation = _weighted_sum(nodes, step_size)

    return SimpsonCompositeResult(
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        step_size=step_size,
        subintervals=subintervals,
        nodes=nodes,
        approximation=approximation,
    )
