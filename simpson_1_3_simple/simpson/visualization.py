"""Interactive Plotly visualizations of the Simpson 1/3 Simple quadrature."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .core import FunctionOfX, QuadratureNode, SimpsonSimpleResult

_BACKGROUND = "#0b0f19"
_FONT_COLOR = "#e8ecf1"
_CURVE_COLOR = "#ff6d00"
_NODE_COLOR = "#ffd600"
_SURFACE_SCALE = "Tealgrn"


def _lagrange_parabola(nodes: tuple[QuadratureNode, ...], x: np.ndarray) -> np.ndarray:
    x0, x1, x2 = (node.x for node in nodes)
    y0, y1, y2 = (node.y for node in nodes)
    l0 = (x - x1) * (x - x2) / ((x0 - x1) * (x0 - x2))
    l1 = (x - x0) * (x - x2) / ((x1 - x0) * (x1 - x2))
    l2 = (x - x0) * (x - x1) / ((x2 - x0) * (x2 - x1))
    return y0 * l0 + y1 * l1 + y2 * l2


def build_3d_area_view(function: FunctionOfX, result: SimpsonSimpleResult, resolution: int = 150) -> go.Figure:
    x = np.linspace(result.lower_bound, result.upper_bound, resolution)
    y_curve = np.array([function(value) for value in x])
    y_parabola = _lagrange_parabola(result.nodes, x)

    ribbon_depth = np.array([0.0, (result.upper_bound - result.lower_bound) * 0.08])
    z_surface = np.tile(y_curve, (2, 1))
    x_surface = np.tile(x, (2, 1))
    y_surface = np.tile(ribbon_depth.reshape(-1, 1), (1, resolution))

    figure = go.Figure()

    figure.add_trace(
        go.Surface(
            x=x_surface,
            y=y_surface,
            z=z_surface,
            colorscale=_SURFACE_SCALE,
            showscale=False,
            opacity=0.92,
            name="f(x) area",
        )
    )

    figure.add_trace(
        go.Scatter3d(
            x=x,
            y=np.zeros_like(x),
            z=y_parabola,
            mode="lines",
            line={"color": _CURVE_COLOR, "width": 7},
            name="Interpolating parabola P2(x)",
        )
    )

    figure.add_trace(
        go.Scatter3d(
            x=[node.x for node in result.nodes],
            y=[0] * len(result.nodes),
            z=[node.y for node in result.nodes],
            mode="markers+text",
            marker={"size": 7, "color": _NODE_COLOR, "symbol": "diamond"},
            text=[f"x{i} · w={node.weight}" for i, node in enumerate(result.nodes)],
            textposition="top center",
            textfont={"color": _FONT_COLOR},
            name="Quadrature nodes",
        )
    )

    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor=_BACKGROUND,
        plot_bgcolor=_BACKGROUND,
        scene={
            "xaxis_title": "x",
            "yaxis": {"showticklabels": False, "title": ""},
            "zaxis_title": "f(x)",
            "camera": {"eye": {"x": 1.6, "y": -1.6, "z": 0.9}},
        },
        title=f"Simpson 1/3 Simple — I ≈ {result.approximation:.6f} on [{result.lower_bound:g}, {result.upper_bound:g}]",
        font={"color": _FONT_COLOR},
        margin={"l": 0, "r": 0, "t": 60, "b": 0},
        legend={"bgcolor": "rgba(0,0,0,0)"},
    )

    return figure


def build_convergence_dashboard(width_sweep_df: pd.DataFrame, degree_sweep_df: pd.DataFrame) -> go.Figure:
    figure = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=(
            "Absolute error vs. step size h",
            "Execution time vs. interval width",
            "Error vs. polynomial degree",
        ),
    )

    figure.add_trace(
        go.Scatter(
            x=width_sweep_df["step_size_h"],
            y=width_sweep_df["absolute_error"],
            mode="markers+lines",
            marker={"color": "#00e5ff"},
            name="Absolute error",
        ),
        row=1,
        col=1,
    )
    figure.update_xaxes(type="log", title_text="h (log scale)", row=1, col=1)
    figure.update_yaxes(type="log", title_text="Absolute error (log scale)", row=1, col=1)

    figure.add_trace(
        go.Scatter(
            x=width_sweep_df["interval_width"],
            y=width_sweep_df["execution_time_seconds"],
            mode="markers+lines",
            marker={"color": "#ff6d00"},
            name="Execution time",
        ),
        row=1,
        col=2,
    )
    figure.update_xaxes(title_text="Interval width (b - a)", row=1, col=2)
    figure.update_yaxes(title_text="Seconds per call", row=1, col=2)

    figure.add_trace(
        go.Bar(
            x=degree_sweep_df["polynomial_degree"],
            y=degree_sweep_df["absolute_error"].clip(lower=1e-16),
            marker={"color": "#ffd600"},
            name="Absolute error",
        ),
        row=1,
        col=3,
    )
    figure.update_xaxes(title_text="Polynomial degree", row=1, col=3)
    figure.update_yaxes(type="log", title_text="Absolute error (log scale)", row=1, col=3)

    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor=_BACKGROUND,
        title="Simpson 1/3 Simple — Empirical Convergence Study",
        showlegend=False,
        font={"color": _FONT_COLOR},
    )

    return figure
