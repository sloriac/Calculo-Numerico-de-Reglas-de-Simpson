"""Command-line demonstration for the Simpson 3/8 Simple quadrature suite."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from rich.console import Console
from rich.table import Table

from simpson.core import SimpsonThreeEighthsResult, integrate
from simpson.experiments import run_interval_width_sweep, run_polynomial_degree_sweep
from simpson.expression import compile_function
from simpson.metrics import ErrorMetrics, compute_error
from simpson.reference import romberg_integrate

console = Console()
OUTPUT_DIR = Path("output")

DEFAULT_LOWER_BOUND = 0.0
DEFAULT_UPPER_BOUND = 2.0
DEFAULT_FUNCTION_EXPRESSION = "x**2 + 2*x + 4"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simpson 3/8 Simple quadrature demo")
    parser.add_argument("--a", type=float, default=None)
    parser.add_argument("--b", type=float, default=None)
    parser.add_argument("--function", type=str, default=None)
    parser.add_argument("--non-interactive", action="store_true")
    return parser.parse_args()


def resolve_inputs(args: argparse.Namespace) -> tuple[float, float, str]:
    if args.non_interactive:
        return (
            args.a if args.a is not None else DEFAULT_LOWER_BOUND,
            args.b if args.b is not None else DEFAULT_UPPER_BOUND,
            args.function if args.function is not None else DEFAULT_FUNCTION_EXPRESSION,
        )

    lower_bound = args.a if args.a is not None else float(console.input("Límite inferior a: ") or DEFAULT_LOWER_BOUND)
    upper_bound = args.b if args.b is not None else float(console.input("Límite superior b: ") or DEFAULT_UPPER_BOUND)
    expression = args.function if args.function is not None else (
        console.input(f"f(x) [{DEFAULT_FUNCTION_EXPRESSION}]: ") or DEFAULT_FUNCTION_EXPRESSION
    )
    return lower_bound, upper_bound, expression


def render_single_run(result: SimpsonThreeEighthsResult, error: ErrorMetrics) -> None:
    table = Table(title="Simpson 3/8 Simple — Quadrature Nodes", show_lines=True)
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


def error_study_function(x: float) -> float:
    return math.sin(x) * math.exp(0.3 * x)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    args = parse_args()
    lower_bound, upper_bound, expression = resolve_inputs(args)
    demo_function = compile_function(expression)

    result = integrate(demo_function, lower_bound, upper_bound)
    exact_value = romberg_integrate(demo_function, lower_bound, upper_bound)
    error = compute_error(result, exact_value)
    render_single_run(result, error)

    widths = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0]
    width_sweep_df = run_interval_width_sweep(error_study_function, lower_bound=0.0, widths=widths)
    width_sweep_df.to_csv(OUTPUT_DIR / "interval_width_sweep.csv", index=False)

    degree_sweep_df = run_polynomial_degree_sweep(0.0, 2.0, degrees=[1, 2, 3, 4, 5, 6])
    degree_sweep_df.to_csv(OUTPUT_DIR / "polynomial_degree_sweep.csv", index=False)

    console.print("\n[bold green]Interval width sweep (h = (b - a) / 3)[/]")
    console.print(width_sweep_df.to_string(index=False))

    console.print("\n[bold green]Polynomial degree sweep — exactness holds up to degree 3[/]")
    console.print(degree_sweep_df.to_string(index=False))


if __name__ == "__main__":
    main()
