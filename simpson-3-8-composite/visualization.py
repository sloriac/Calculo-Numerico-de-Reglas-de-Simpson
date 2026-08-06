"""Sampling helpers for visualizing Simpson 3/8 Composite.

Purely additive over wrapper.py / Simpson38.py — neither file is modified.
This module only samples the true curve and reconstructs each panel's cubic
interpolant (4 nodes per panel) for display purposes.
"""

from __future__ import annotations

import numpy as np

from reference import FunctionOfX
from wrapper import DisplayNode, SimpsonThreeEighthsCompositeResult


def _lagrange_cubic(nodes: tuple[DisplayNode, DisplayNode, DisplayNode, DisplayNode], x: np.ndarray) -> np.ndarray:
    x0, x1, x2, x3 = (node["x"] for node in nodes)
    y0, y1, y2, y3 = (node["y"] for node in nodes)
    l0 = (x - x1) * (x - x2) * (x - x3) / ((x0 - x1) * (x0 - x2) * (x0 - x3))
    l1 = (x - x0) * (x - x2) * (x - x3) / ((x1 - x0) * (x1 - x2) * (x1 - x3))
    l2 = (x - x0) * (x - x1) * (x - x3) / ((x2 - x0) * (x2 - x1) * (x2 - x3))
    l3 = (x - x0) * (x - x1) * (x - x2) / ((x3 - x0) * (x3 - x1) * (x3 - x2))
    return y0 * l0 + y1 * l1 + y2 * l2 + y3 * l3


def sample_curve(
    function: FunctionOfX, result: SimpsonThreeEighthsCompositeResult, resolution: int = 300
) -> tuple[list[float], list[float]]:
    x = np.linspace(result.lower_bound, result.upper_bound, resolution)
    y = np.array([function(value) for value in x])
    return x.tolist(), y.tolist()


def sample_panels(result: SimpsonThreeEighthsCompositeResult, points_per_panel: int = 20) -> list[dict[str, list[float]]]:
    panels = []
    for start in range(0, result.subintervals, 3):
        quad = tuple(result.nodes[start : start + 4])
        x = np.linspace(quad[0]["x"], quad[3]["x"], points_per_panel)
        y = _lagrange_cubic(quad, x)  # type: ignore[arg-type]
        panels.append({"x": x.tolist(), "y": y.tolist()})
    return panels
