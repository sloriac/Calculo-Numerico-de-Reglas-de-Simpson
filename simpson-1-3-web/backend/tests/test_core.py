import math

import pytest

from simpson.core import integrate


def test_matches_hand_worked_example_from_the_report():
    result = integrate(lambda x: x**2 + 2 * x + 4, 0.0, 2.0)
    assert result.approximation == pytest.approx(44 / 3, rel=1e-12)


@pytest.mark.parametrize("degree", [0, 1, 2, 3])
def test_exact_for_polynomials_up_to_degree_three(degree):
    result = integrate(lambda x, d=degree: x**d, 0.0, 2.0)
    exact = 2 ** (degree + 1) / (degree + 1)
    assert result.approximation == pytest.approx(exact, rel=1e-12)


def test_not_exact_for_degree_four_polynomial():
    result = integrate(lambda x: x**4, 0.0, 2.0)
    exact = 2**5 / 5
    assert result.approximation != pytest.approx(exact, rel=1e-9)


def test_step_size_is_half_the_interval_width():
    result = integrate(math.sin, 0.0, 4.0)
    assert result.step_size == pytest.approx(2.0)


def test_uses_exactly_three_nodes():
    result = integrate(math.cos, -1.0, 1.0)
    assert result.evaluation_count == 3


def test_node_weights_follow_one_four_one_pattern():
    result = integrate(math.exp, 0.0, 1.0)
    assert [node.weight for node in result.nodes] == [1, 4, 1]


def test_rejects_invalid_bounds():
    with pytest.raises(ValueError):
        integrate(math.sin, 2.0, 0.0)
