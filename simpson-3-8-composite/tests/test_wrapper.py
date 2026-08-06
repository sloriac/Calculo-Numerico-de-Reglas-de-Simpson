import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from wrapper import compute_error, integrate


def test_matches_the_mathematically_correct_value(capsys):
    result = integrate(lambda x: x**2 + 2 * x + 4, 0.0, 2.0, subintervals=6)
    # Simpson's rule (any variant/order) is exact for polynomials up to degree 3,
    # so this must equal exactly 44/3, independent of n.
    assert result.approximation == pytest.approx(44 / 3, rel=1e-9)


@pytest.mark.parametrize("degree", [0, 1, 2, 3])
def test_exact_for_polynomials_up_to_degree_three(degree, capsys):
    result = integrate(lambda x, d=degree: x**d, 0.0, 2.0, subintervals=6)
    exact = 2 ** (degree + 1) / (degree + 1)
    assert result.approximation == pytest.approx(exact, rel=1e-9)


def test_node_weight_pattern_matches_teammates_loop(capsys):
    result = integrate(lambda x: x, 0.0, 3.0, subintervals=3)
    weights = [node["weight"] for node in result.nodes]
    assert weights == [1, 3, 3, 1]


def test_rejects_non_multiple_of_three(capsys):
    with pytest.raises(ValueError):
        integrate(math.sin, 0.0, 2.0, subintervals=4)


def test_rejects_invalid_bounds(capsys):
    with pytest.raises(ValueError):
        integrate(math.sin, 2.0, 0.0, subintervals=3)


def test_compute_error_converts_percentage_to_fraction():
    error = compute_error(approximation=9.9, exact_value=10.0)
    assert error.relative_error == pytest.approx(0.01, rel=1e-6)
    assert error.absolute_error == pytest.approx(0.1, rel=1e-6)
