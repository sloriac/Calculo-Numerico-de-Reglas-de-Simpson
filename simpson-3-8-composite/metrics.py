"""Performance instrumentation for the wrapped Simpson 3/8 Composite.

Simpson38.py prints its step-by-step derivation on every call (by design —
that satisfies the assignment's "show the algorithm step by step" rubric
item for normal single runs). For repeated-timing benchmarks that call it
hundreds of times, this module temporarily silences stdout during the
repetition loop only, so sweeps don't flood the console. The teammate's
code itself is never touched.
"""

from __future__ import annotations

import contextlib
import io
import time
from dataclasses import dataclass

from reference import FunctionOfX
from wrapper import SimpsonThreeEighthsCompositeResult, integrate


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    result: SimpsonThreeEighthsCompositeResult
    execution_time_seconds: float
    evaluation_count: int


def benchmark(
    function: FunctionOfX, lower_bound: float, upper_bound: float, subintervals: int, repetitions: int = 50
) -> BenchmarkResult:
    result = integrate(function, lower_bound, upper_bound, subintervals)

    start = time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):
        for _ in range(repetitions):
            integrate(function, lower_bound, upper_bound, subintervals)
    elapsed_per_call = (time.perf_counter() - start) / repetitions

    return BenchmarkResult(result=result, execution_time_seconds=elapsed_per_call, evaluation_count=result.evaluation_count)
