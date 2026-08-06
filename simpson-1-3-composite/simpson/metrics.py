"""Error quantification and performance instrumentation for Simpson 1/3 Composite."""

from __future__ import annotations

import time
from dataclasses import dataclass

from .core import FunctionOfX, SimpsonCompositeResult, integrate


@dataclass(frozen=True, slots=True)
class ErrorMetrics:
    exact_value: float
    absolute_error: float
    relative_error: float


def compute_error(result: SimpsonCompositeResult, exact_value: float) -> ErrorMetrics:
    absolute_error = abs(exact_value - result.approximation)
    relative_error = absolute_error / abs(exact_value) if exact_value != 0 else float("nan")
    return ErrorMetrics(exact_value=exact_value, absolute_error=absolute_error, relative_error=relative_error)


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    result: SimpsonCompositeResult
    execution_time_seconds: float
    evaluation_count: int


def benchmark(
    function: FunctionOfX, lower_bound: float, upper_bound: float, subintervals: int, repetitions: int = 200
) -> BenchmarkResult:
    """Average `integrate` over many repetitions to obtain a stable timing signal."""
    start = time.perf_counter()
    result = integrate(function, lower_bound, upper_bound, subintervals)
    for _ in range(repetitions - 1):
        result = integrate(function, lower_bound, upper_bound, subintervals)
    elapsed_per_call = (time.perf_counter() - start) / repetitions

    return BenchmarkResult(result=result, execution_time_seconds=elapsed_per_call, evaluation_count=result.evaluation_count)
