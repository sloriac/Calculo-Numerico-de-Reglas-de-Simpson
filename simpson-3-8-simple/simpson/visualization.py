"""Sampling helpers for visualizing Simpson 3/8 Simple: the true curve plus
the single interpolating cubic across the four nodes.
"""

from __future__ import annotations

import numpy as np

from .core import FunctionOfX, QuadratureNode, SimpsonThreeEighthsResult


def _lagrange_cubic(
    nodes: tuple[QuadratureNode, QuadratureNode, QuadratureNode, QuadratureNode], x: np.ndarray
) -> np.ndarray:
    x0, x1, x2, x3 = (node.x for node in nodes)
    y0, y1, y2, y3 = (node.y for node in nodes)
    l0 = (x - x1) * (x - x2) * (x - x3) / ((x0 - x1) * (x0 - x2) * (x0 - x3))
    l1 = (x - x0) * (x - x2) * (x - x3) / ((x1 - x0) * (x1 - x2) * (x1 - x3))
    l2 = (x - x0) * (x - x1) * (x - x3) / ((x2 - x0) * (x2 - x1) * (x2 - x3))
    l3 = (x - x0) * (x - x1) * (x - x2) / ((x3 - x0) * (x3 - x1) * (x3 - x2))
    return y0 * l0 + y1 * l1 + y2 * l2 + y3 * l3


def sample_curve_and_parabola(
    function: FunctionOfX, result: SimpsonThreeEighthsResult, resolution: int = 150
) -> tuple[list[float], list[float], list[float]]:
    x = np.linspace(result.lower_bound, result.upper_bound, resolution)
    y_curve = np.array([function(value) for value in x])
    y_parabola = _lagrange_cubic(result.nodes, x)
    return x.tolist(), y_curve.tolist(), y_parabola.tolist()
