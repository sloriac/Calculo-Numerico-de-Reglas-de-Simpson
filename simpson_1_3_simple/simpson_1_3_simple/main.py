"""Command-line demonstration for the Simpson 1/3 Simple quadrature suite.

Swap `demo_function`, `LOWER_BOUND`, and `UPPER_BOUND` to analyze a different case.
"""

from __future__ import annotations

import math
from pathlib import Path

from rich.console import Console
from rich.table import Table

from simpson.core import integrate
from simpson.experiments import run_interval_width_sweep, run_polynomial_degree_sweep
from simpson.metrics import compute_error
from simpson.reference import romberg_integrate
from simpson.visualization import build_3d_area_view, build_convergence_dashboard

console = Console()
OUTPUT_DIR = Path("output")

LOWER_BOUND = 0.0
UPPER_BOUND = 2.0


def demo_function(x: float) -> float:
    return x**2 + 2 * x + 4


def error_study_function(x: float) -> float:
    """Non-polynomial probe: degree-2/3 exactness would hide truncation error."""
    return math.sin(x) * math.exp(0.3 * x)


def render_single_run(result, error) -> None:
    table = Table(title="Simpson 1/3 Simple — Quadrature Nodes", show_lines=True)
    table.add_column("Node")
    table.add_column("x", justify="right")
    table.add_column("f(x)", justify="right")
    table.add_column("Weight", justify="right")

    for index, node in enumerate(result.nodes):
        table.add_row(f"x{index}", f"{node.x:.6f}", f"{node.y:.6f}", str(node.weight))

    console.print(table)
    console.print(f"[bold cyan]Approximation:[/]        {result.approximation:.8f}")
    console.print(f"[bold yellow]Reference (Romberg):[/]  {error.exact_value:.8f}")
    console.print(f"[bold red]Absolute error:[/]        {error.absolute_error:.3e}")
    console.print(f"[bold red]Relative error:[/]        {error.relative_error:.3e}")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    result = integrate(demo_function, LOWER_BOUND, UPPER_BOUND)
    exact_value = romberg_integrate(demo_function, LOWER_BOUND, UPPER_BOUND)
    error = compute_error(result, exact_value)
    render_single_run(result, error)

    widths = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0]
    width_sweep_df = run_interval_width_sweep(error_study_function, lower_bound=LOWER_BOUND, widths=widths)
    width_sweep_df.to_csv(OUTPUT_DIR / "interval_width_sweep.csv", index=False)

    degree_sweep_df = run_polynomial_degree_sweep(LOWER_BOUND, UPPER_BOUND, degrees=[1, 2, 3, 4, 5, 6])
    degree_sweep_df.to_csv(OUTPUT_DIR / "polynomial_degree_sweep.csv", index=False)

    console.print("\n[bold green]Interval width sweep (h = (b - a) / 2)[/]")
    console.print(width_sweep_df.to_string(index=False))

    console.print("\n[bold green]Polynomial degree sweep — exactness holds up to degree 3[/]")
    console.print(degree_sweep_df.to_string(index=False))

    build_3d_area_view(demo_function, result).write_html(
        OUTPUT_DIR / "simpson_3d_view.html", include_plotlyjs="cdn"
    )
    build_convergence_dashboard(width_sweep_df, degree_sweep_df).write_html(
        OUTPUT_DIR / "convergence_dashboard.html", include_plotlyjs="cdn"
    )

    console.print(f"\n[bold magenta]Visualizations written to:[/] {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
