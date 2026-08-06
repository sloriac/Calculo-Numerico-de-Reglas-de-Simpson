"""High-precision reference solver used exclusively to validate Simpson 3/8 Composite.

This is NOT the assigned quadrature method. It exists only to produce a trustworthy
'exact' value for error analysis when no closed-form antiderivative is supplied,
implemented from scratch (Romberg / Richardson extrapolation) rather than delegating
to a library integration routine.
"""

from __future__ import annotations

from collections.abc import Callable

FunctionOfX = Callable[[float], float]


def _trapezoidal_estimate(function: FunctionOfX, lower_bound: float, upper_bound: float, subdivisions: int) -> float:
    step = (upper_bound - lower_bound) / subdivisions
    total = 0.5 * (function(lower_bound) + function(upper_bound))
    total += sum(function(lower_bound + i * step) for i in range(1, subdivisions))
    return total * step


def romberg_integrate(
    function: FunctionOfX,
    lower_bound: float,
    upper_bound: float,
    max_levels: int = 14,
    tolerance: float = 1e-12,
) -> float:
    table = [[0.0] * max_levels for _ in range(max_levels)]
    table[0][0] = _trapezoidal_estimate(function, lower_bound, upper_bound, 1)

    for level in range(1, max_levels):
        table[level][0] = _trapezoidal_estimate(function, lower_bound, upper_bound, 2 ** level)
        for order in range(1, level + 1):
            factor = 4 ** order
            table[level][order] = (factor * table[level][order - 1] - table[level - 1][order - 1]) / (factor - 1)
        if abs(table[level][level] - table[level - 1][level - 1]) < tolerance:
            return table[level][level]

    return table[max_levels - 1][max_levels - 1]
