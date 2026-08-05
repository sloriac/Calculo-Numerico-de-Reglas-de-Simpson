import pytest

from simpson.expression import compile_function


def test_evaluates_polynomial_expression():
    f = compile_function("x**2 + 2*x + 4")
    assert f(2) == pytest.approx(12.0)


def test_evaluates_math_module_functions():
    f = compile_function("sin(x) * exp(0.3*x)")
    assert f(0) == pytest.approx(0.0)


def test_blocks_builtin_access():
    f = compile_function("__import__('os').system('echo unsafe')")
    with pytest.raises(NameError):
        f(0)
