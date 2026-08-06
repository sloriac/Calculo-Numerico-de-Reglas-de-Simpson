import pytest

from simpson.core import integrate
from simpson.metrics import benchmark, compute_error
from simpson.reference import romberg_integrate


def test_compute_error_against_known_exact_value():
    result = integrate(lambda x: x**2 + 2 * x + 4, 0.0, 2.0, subintervals=6)
    error = compute_error(result, exact_value=44 / 3)
    assert error.absolute_error == pytest.approx(0.0, abs=1e-9)


def test_benchmark_reports_n_plus_one_evaluations_and_positive_time():
    bench = benchmark(lambda x: x**2, 0.0, 2.0, subintervals=8, repetitions=20)
    assert bench.evaluation_count == 9
    assert bench.execution_time_seconds > 0


def test_romberg_reference_matches_analytical_integral():
    exact_value = romberg_integrate(lambda x: x**2 + 2 * x + 4, 0.0, 2.0)
    assert exact_value == pytest.approx(44 / 3, rel=1e-9)
