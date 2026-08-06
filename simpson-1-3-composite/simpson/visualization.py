"""Sampling helpers for visualizing Simpson 1/3 Composite: the true curve plus
each panel's individual interpolating parabola, stitched across the domain.
"""

from __future__ import annotations

import numpy as np

from .core import FunctionOfX, QuadratureNode, SimpsonCompositeResult


def _lagrange_quadratic(nodes: tuple[QuadratureNode, QuadratureNode, QuadratureNode], x: np.ndarray) -> np.ndarray:
    x0, x1, x2 = (node.x for node in nodes)
    y0, y1, y2 = (node.y for node in nodes)
    l0 = (x - x1) * (x - x2) / ((x0 - x1) * (x0 - x2))
    l1 = (x - x0) * (x - x2) / ((x1 - x0) * (x1 - x2))
    l2 = (x - x0) * (x - x1) / ((x2 - x0) * (x2 - x1))
    return y0 * l0 + y1 * l1 + y2 * l2


def sample_curve(function: FunctionOfX, result: SimpsonCompositeResult, resolution: int = 300) -> tuple[list[float], list[float]]:
    x = np.linspace(result.lower_bound, result.upper_bound, resolution)
    y = np.array([function(value) for value in x])
    return x.tolist(), y.tolist()


def sample_panels(result: SimpsonCompositeResult, points_per_panel: int = 20) -> list[dict[str, list[float]]]:
    panels = []
    for start in range(0, result.subintervals, 2):
        triple = result.nodes[start : start + 3]
        x = np.linspace(triple[0].x, triple[2].x, points_per_panel)
        y = _lagrange_quadratic(triple, x)
        panels.append({"x": x.tolist(), "y": y.tolist()})
    return panels
