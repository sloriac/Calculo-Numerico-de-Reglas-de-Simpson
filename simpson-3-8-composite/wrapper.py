"""Thin orchestration layer around the teammate's original Simpson38.py.

Simpson38.py is NOT modified anywhere in this project. This module only
imports its public functions and adds what the team's shared conventions
need around it:

  - external validation of n (his file only validates inside the terminal
    menu, not inside the math function itself, so a direct API call needs
    its own guard)
  - automatic reference-value computation (Romberg), replacing the manual
    "type in the antiderivative" step from his terminal version, for a
    smoother web experience
  - a display-only node/weight reconstruction (mirroring his internal loop
    exactly) so the frontend can render a node table, since his function
    only returns the final number
  - unit conversion of his percentage-based relative error to a fraction,
    to match the convention used by the other three team modules
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reference import FunctionOfX
from Simpson38 import calcular_error as _calcular_error_original
from Simpson38 import simpson_3_8 as _simpson_3_8_original


class DisplayNode(TypedDict):
    x: float
    y: float
    weight: int


@dataclass(frozen=True, slots=True)
class SimpsonThreeEighthsCompositeResult:
    lower_bound: float
    upper_bound: float
    step_size: float
    subintervals: int
    nodes: tuple[DisplayNode, ...]
    approximation: float

    @property
    def evaluation_count(self) -> int:
        return len(self.nodes)


@dataclass(frozen=True, slots=True)
class ErrorMetrics:
    exact_value: float
    absolute_error: float
    relative_error: float


def _validate_subintervals(subintervals: int) -> None:
    if subintervals <= 0:
        raise ValueError("subintervals (n) must be a positive integer")
    if subintervals % 3 != 0:
        raise ValueError("subintervals (n) must be a multiple of 3 for Simpson 3/8 Composite")


def _node_weight(index: int, subintervals: int) -> int:
    """Mirrors Simpson38.py's own coefficient loop, for display purposes only."""
    if index == 0 or index == subintervals:
        return 1
    return 2 if index % 3 == 0 else 3


def _build_display_nodes(
    function: FunctionOfX, lower_bound: float, step_size: float, subintervals: int
) -> tuple[DisplayNode, ...]:
    return tuple(
        DisplayNode(
            x=(x := lower_bound + index * step_size),
            y=function(x),
            weight=_node_weight(index, subintervals),
        )
        for index in range(subintervals + 1)
    )


def integrate(
    function: FunctionOfX, lower_bound: float, upper_bound: float, subintervals: int
) -> SimpsonThreeEighthsCompositeResult:
    if upper_bound <= lower_bound:
        raise ValueError("upper_bound must be strictly greater than lower_bound")
    _validate_subintervals(subintervals)

    # The actual computation below calls the teammate's original function untouched.
    approximation = _simpson_3_8_original(function, lower_bound, upper_bound, subintervals)

    step_size = (upper_bound - lower_bound) / subintervals
    nodes = _build_display_nodes(function, lower_bound, step_size, subintervals)

    return SimpsonThreeEighthsCompositeResult(
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        step_size=step_size,
        subintervals=subintervals,
        nodes=nodes,
        approximation=approximation,
    )


def compute_error(approximation: float, exact_value: float) -> ErrorMetrics:
    # Delegates to the teammate's own error function untouched; only converts
    # his percentage-based relative error to a fraction for team-wide consistency.
    absolute_error, relative_error_percent = _calcular_error_original(approximation, exact_value)
    return ErrorMetrics(
        exact_value=exact_value,
        absolute_error=absolute_error,
        relative_error=relative_error_percent / 100.0,
    )
