"""Parameter sweeps for Simpson 3/8 Composite, built entirely on wrapper.py
(which itself never modifies Simpson38.py)."""

from __future__ import annotations

import pandas as pd

from metrics import benchmark
from reference import FunctionOfX, romberg_integrate
from wrapper import compute_error, integrate


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
        error = compute_error(bench.result.approximation, exact_value)

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
    records = []
    for degree in degrees:
        function = _make_power_function(degree)
        exact_value = (upper_bound ** (degree + 1) - lower_bound ** (degree + 1)) / (degree + 1)
        result = integrate(function, lower_bound, upper_bound, subintervals)
        error = compute_error(result.approximation, exact_value)

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
