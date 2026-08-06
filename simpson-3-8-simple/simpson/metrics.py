"""Error quantification and performance instrumentation for Simpson 3/8 Simple."""

from __future__ import annotations

import time
from dataclasses import dataclass

from .core import FunctionOfX, SimpsonThreeEighthsResult, integrate


@dataclass(frozen=True, slots=True)
class ErrorMetrics:
    exact_value: float
    absolute_error: float
    relative_error: float


def compute_error(result: SimpsonThreeEighthsResult, exact_value: float) -> ErrorMetrics:
    absolute_error = abs(exact_value - result.approximation)
    relative_error = absolute_error / abs(exact_value) if exact_value != 0 else float("nan")
    return ErrorMetrics(exact_value=exact_value, absolute_error=absolute_error, relative_error=relative_error)


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    result: SimpsonThreeEighthsResult
    execution_time_seconds: float
    evaluation_count: int


def benchmark(function: FunctionOfX, lower_bound: float, upper_bound: float, repetitions: int = 2000) -> BenchmarkResult:
    """Average `integrate` over many repetitions to obtain a stable timing signal."""
    start = time.perf_counter()
    result = integrate(function, lower_bound, upper_bound)
    for _ in range(repetitions - 1):
        result = integrate(function, lower_bound, upper_bound)
    elapsed_per_call = (time.perf_counter() - start) / repetitions

    return BenchmarkResult(result=result, execution_time_seconds=elapsed_per_call, evaluation_count=result.evaluation_count)
