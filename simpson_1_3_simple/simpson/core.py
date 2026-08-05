"""Simpson's One-Third Simple Rule: closed-form quadratic (Lagrange P2) quadrature.

Fixed by definition to two subintervals (three nodes). No integration/derivation
library primitives are used — every step of the algorithm is implemented explicitly.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

FunctionOfX = Callable[[float], float]

_NODE_WEIGHTS: tuple[int, int, int] = (1, 4, 1)


@dataclass(frozen=True, slots=True)
class QuadratureNode:
    x: float
    y: float
    weight: int


@dataclass(frozen=True, slots=True)
class SimpsonSimpleResult:
    lower_bound: float
    upper_bound: float
    step_size: float
    nodes: tuple[QuadratureNode, QuadratureNode, QuadratureNode]
    approximation: float

    @property
    def evaluation_count(self) -> int:
        return len(self.nodes)


def _compute_step_size(lower_bound: float, upper_bound: float) -> float:
    return (upper_bound - lower_bound) / 2.0


def _generate_nodes(
    lower_bound: float, step_size: float, function: FunctionOfX
) -> tuple[QuadratureNode, QuadratureNode, QuadratureNode]:
    return tuple(
        QuadratureNode(
            x=lower_bound + index * step_size,
            y=function(lower_bound + index * step_size),
            weight=weight,
        )
        for index, weight in enumerate(_NODE_WEIGHTS)
    )  # type: ignore[return-value]


def _weighted_sum(nodes: tuple[QuadratureNode, ...], step_size: float) -> float:
    return (step_size / 3.0) * sum(node.weight * node.y for node in nodes)


def integrate(function: FunctionOfX, lower_bound: float, upper_bound: float) -> SimpsonSimpleResult:
    """Approximate the definite integral of `function` over [lower_bound, upper_bound]."""
    if upper_bound <= lower_bound:
        raise ValueError("upper_bound must be strictly greater than lower_bound")

    step_size = _compute_step_size(lower_bound, upper_bound)
    nodes = _generate_nodes(lower_bound, step_size, function)
    approximation = _weighted_sum(nodes, step_size)

    return SimpsonSimpleResult(
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        step_size=step_size,
        nodes=nodes,
        approximation=approximation,
    )
