"""Safe evaluation of user-supplied f(x) expressions, restricted to the math module."""

from __future__ import annotations

import math

from .core import FunctionOfX

_ALLOWED_NAMES = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}


def compile_function(expression: str) -> FunctionOfX:
    """Turn a string like 'x**2 + 2*x + 4' or 'sin(x) * exp(0.3*x)' into a callable."""
    code = compile(expression, "<f(x)>", "eval")

    def function(x: float) -> float:
        return eval(code, {"__builtins__": {}}, {**_ALLOWED_NAMES, "x": x})

    return function
