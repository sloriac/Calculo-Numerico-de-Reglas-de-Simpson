"""Parameter sweeps that generate the empirical dataset required by the project rubric.

Simpson 1/3 Simple has no configurable partition count (n is fixed at 2), so the
step size h is instead varied through the interval width (b - a) = 2h, which is
the quantity that actually drives the truncation error, per:

    E_t = -((b - a) ** 5) / 2880 * f''''(xi)
"""

from __future__ import annotations

import pandas as pd

from .core import FunctionOfX, integrate
from .metrics import benchmark, compute_error
from .reference import romberg_integrate


def _make_power_function(degree: int) -> FunctionOfX:
    def power_function(x: float) -> float:
        return x**degree

    return power_function


def run_interval_width_sweep(function: FunctionOfX, lower_bound: float, widths: list[float]) -> pd.DataFrame:
    records = []
    for width in widths:
        upper_bound = lower_bound + width
        exact_value = romberg_integrate(function, lower_bound, upper_bound)
        bench = benchmark(function, lower_bound, upper_bound)
        error = compute_error(bench.result, exact_value)

        records.append(
            {
                "interval_width": width,
                "step_size_h": bench.result.step_size,
                "approximation": bench.result.approximation,
                "exact_value": exact_value,
                "absolute_error": error.absolute_error,
                "relative_error": error.relative_error,
                "execution_time_seconds": bench.execution_time_seconds,
                "evaluation_count": bench.evaluation_count,
            }
        )

    return pd.DataFrame.from_records(records)


def run_polynomial_degree_sweep(lower_bound: float, upper_bound: float, degrees: list[int]) -> pd.DataFrame:
    """Empirically confirms third-order exactness: near-zero error for degree <= 3."""
    records = []
    for degree in degrees:
        function = _make_power_function(degree)
        exact_value = (upper_bound ** (degree + 1) - lower_bound ** (degree + 1)) / (degree + 1)
        result = integrate(function, lower_bound, upper_bound)
        error = compute_error(result, exact_value)

        records.append(
            {
                "polynomial_degree": degree,
                "approximation": result.approximation,
                "exact_value": exact_value,
                "absolute_error": error.absolute_error,
                "relative_error": error.relative_error,
            }
        )

    return pd.DataFrame.from_records(records)
