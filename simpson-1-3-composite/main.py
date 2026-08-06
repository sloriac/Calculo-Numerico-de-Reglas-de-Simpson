"""Command-line demonstration for the Simpson 1/3 Composite quadrature suite."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from rich.console import Console
from rich.table import Table

from simpson.core import SimpsonCompositeResult, integrate
from simpson.experiments import run_partition_sweep, run_polynomial_degree_sweep
from simpson.expression import compile_function
from simpson.metrics import ErrorMetrics, compute_error
from simpson.reference import romberg_integrate

console = Console()
OUTPUT_DIR = Path("output")

DEFAULT_LOWER_BOUND = 0.0
DEFAULT_UPPER_BOUND = 2.0
DEFAULT_SUBINTERVALS = 6
DEFAULT_FUNCTION_EXPRESSION = "x**2 + 2*x + 4"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simpson 1/3 Composite quadrature demo")
    parser.add_argument("--a", type=float, default=None)
    parser.add_argument("--b", type=float, default=None)
    parser.add_argument("--n", type=int, default=None, help="Number of subintervals (must be even)")
    parser.add_argument("--function", type=str, default=None)
    parser.add_argument("--non-interactive", action="store_true")
    return parser.parse_args()


def resolve_inputs(args: argparse.Namespace) -> tuple[float, float, int, str]:
    if args.non_interactive:
        return (
            args.a if args.a is not None else DEFAULT_LOWER_BOUND,
            args.b if args.b is not None else DEFAULT_UPPER_BOUND,
            args.n if args.n is not None else DEFAULT_SUBINTERVALS,
            args.function if args.function is not None else DEFAULT_FUNCTION_EXPRESSION,
        )

    lower_bound = args.a if args.a is not None else float(console.input("Límite inferior a: ") or DEFAULT_LOWER_BOUND)
    upper_bound = args.b if args.b is not None else float(console.input("Límite superior b: ") or DEFAULT_UPPER_BOUND)
    subintervals = args.n if args.n is not None else int(
        console.input(f"Número de subintervalos n (par) [{DEFAULT_SUBINTERVALS}]: ") or DEFAULT_SUBINTERVALS
    )
    expression = args.function if args.function is not None else (
        console.input(f"f(x) [{DEFAULT_FUNCTION_EXPRESSION}]: ") or DEFAULT_FUNCTION_EXPRESSION
    )
    return lower_bound, upper_bound, subintervals, expression


def render_single_run(result: SimpsonCompositeResult, error: ErrorMetrics) -> None:
    table = Table(title="Simpson 1/3 Composite — Quadrature Nodes", show_lines=True)
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
    lower_bound, upper_bound, subintervals, expression = resolve_inputs(args)
    demo_function = compile_function(expression)

    result = integrate(demo_function, lower_bound, upper_bound, subintervals)
    exact_value = romberg_integrate(demo_function, lower_bound, upper_bound)
    error = compute_error(result, exact_value)
    render_single_run(result, error)

    partition_sweep_df = run_partition_sweep(error_study_function, 0.0, 4.0, [2, 4, 6, 10, 20, 50, 100])
    partition_sweep_df.to_csv(OUTPUT_DIR / "partition_sweep.csv", index=False)

    degree_sweep_df = run_polynomial_degree_sweep(0.0, 2.0, subintervals=8, degrees=[1, 2, 3, 4, 5, 6])
    degree_sweep_df.to_csv(OUTPUT_DIR / "polynomial_degree_sweep.csv", index=False)

    console.print("\n[bold green]Partition sweep (n = 2, 4, 6, 10, 20, 50, 100)[/]")
    console.print(partition_sweep_df.to_string(index=False))

    console.print("\n[bold green]Polynomial degree sweep — exactness holds up to degree 3[/]")
    console.print(degree_sweep_df.to_string(index=False))


if __name__ == "__main__":
    main()
