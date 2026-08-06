"""Simpson's Three-Eighths Simple Rule: closed-form cubic (Lagrange P3) quadrature.

Fixed by definition to three subintervals (four nodes). No integration/derivation
library primitives are used — every step of the algorithm is implemented explicitly.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

FunctionOfX = Callable[[float], float]

_NODE_WEIGHTS: tuple[int, int, int, int] = (1, 3, 3, 1)


@dataclass(frozen=True, slots=True)
class QuadratureNode:
    x: float
    y: float
    weight: int


@dataclass(frozen=True, slots=True)
class SimpsonThreeEighthsResult:
    lower_bound: float
    upper_bound: float
    step_size: float
    nodes: tuple[QuadratureNode, QuadratureNode, QuadratureNode, QuadratureNode]
    approximation: float

    @property
    def evaluation_count(self) -> int:
        return len(self.nodes)


def _compute_step_size(lower_bound: float, upper_bound: float) -> float:
    return (upper_bound - lower_bound) / 3.0


def _generate_nodes(
    lower_bound: float, step_size: float, function: FunctionOfX
) -> tuple[QuadratureNode, QuadratureNode, QuadratureNode, QuadratureNode]:
    return tuple(
        QuadratureNode(
            x=lower_bound + index * step_size,
            y=function(lower_bound + index * step_size),
            weight=weight,
        )
        for index, weight in enumerate(_NODE_WEIGHTS)
    )  # type: ignore[return-value]


def _weighted_sum(nodes: tuple[QuadratureNode, ...], step_size: float) -> float:
    return (3.0 * step_size / 8.0) * sum(node.weight * node.y for node in nodes)


def integrate(function: FunctionOfX, lower_bound: float, upper_bound: float) -> SimpsonThreeEighthsResult:
    """Approximate the definite integral of `function` over [lower_bound, upper_bound]."""
    if upper_bound <= lower_bound:
        raise ValueError("upper_bound must be strictly greater than lower_bound")

    step_size = _compute_step_size(lower_bound, upper_bound)
    nodes = _generate_nodes(lower_bound, step_size, function)
    approximation = _weighted_sum(nodes, step_size)

    return SimpsonThreeEighthsResult(
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        step_size=step_size,
        nodes=nodes,
        approximation=approximation,
    )
