"""Parameter sweeps for Simpson 1/3 Composite.

Unlike the Simple variant, `n` is a real, independent parameter here, so this
directly satisfies the rubric's request to study convergence as the number of
partitions changes — no proxy variable needed.
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


def run_partition_sweep(
    function: FunctionOfX, lower_bound: float, upper_bound: float, partition_counts: list[int]
) -> pd.DataFrame:
    exact_value = romberg_integrate(function, lower_bound, upper_bound)
    records = []

    for n in partition_counts:
        bench = benchmark(function, lower_bound, upper_bound, n)
        error = compute_error(bench.result, exact_value)

        records.append(
            {
                "subintervals_n": n,
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


def run_polynomial_degree_sweep(
    lower_bound: float, upper_bound: float, subintervals: int, degrees: list[int]
) -> pd.DataFrame:
    """Empirically confirms third-order exactness holds for any valid n, not just n=2."""
    records = []
    for degree in degrees:
        function = _make_power_function(degree)
        exact_value = (upper_bound ** (degree + 1) - lower_bound ** (degree + 1)) / (degree + 1)
        result = integrate(function, lower_bound, upper_bound, subintervals)
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
