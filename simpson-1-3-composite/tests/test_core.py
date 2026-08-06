import math

import pytest

from simpson.core import integrate


def test_matches_hand_worked_example_from_the_report():
    result = integrate(lambda x: x**2 + 2 * x + 4, 0.0, 2.0, subintervals=6)
    assert result.approximation == pytest.approx(44 / 3, rel=1e-12)


@pytest.mark.parametrize("degree", [0, 1, 2, 3])
@pytest.mark.parametrize("n", [2, 4, 6, 10])
def test_exact_for_polynomials_up_to_degree_three_any_valid_n(degree, n):
    result = integrate(lambda x, d=degree: x**d, 0.0, 2.0, subintervals=n)
    exact = 2 ** (degree + 1) / (degree + 1)
    assert result.approximation == pytest.approx(exact, rel=1e-9)


def test_not_exact_for_degree_four_polynomial():
    result = integrate(lambda x: x**4, 0.0, 2.0, subintervals=4)
    exact = 2**5 / 5
    assert result.approximation != pytest.approx(exact, rel=1e-9)


def test_step_size_divides_interval_by_n():
    result = integrate(math.sin, 0.0, 4.0, subintervals=8)
    assert result.step_size == pytest.approx(0.5)


def test_uses_n_plus_one_nodes():
    result = integrate(math.cos, -1.0, 1.0, subintervals=10)
    assert result.evaluation_count == 11


def test_node_weight_pattern_extremes_one_odd_four_even_two():
    result = integrate(math.exp, 0.0, 1.0, subintervals=4)
    weights = [node.weight for node in result.nodes]
    assert weights == [1, 4, 2, 4, 1]


def test_rejects_invalid_bounds():
    with pytest.raises(ValueError):
        integrate(math.sin, 2.0, 0.0, subintervals=4)


def test_rejects_odd_n():
    with pytest.raises(ValueError):
        integrate(math.sin, 0.0, 2.0, subintervals=5)


def test_rejects_zero_or_negative_n():
    with pytest.raises(ValueError):
        integrate(math.sin, 0.0, 2.0, subintervals=0)
