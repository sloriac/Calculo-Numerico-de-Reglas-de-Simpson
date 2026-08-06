"""Command-line demonstration for the Simpson 3/8 Composite quadrature suite.

This calls the teammate's original Simpson38.py untouched (see wrapper.py),
adding only the automatic reference value and a consistent CLI shape shared
with the team's other three modules.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from rich.console import Console
from rich.table import Table

from metrics import benchmark
from reference import romberg_integrate
from wrapper import (
    ErrorMetrics,
    SimpsonThreeEighthsCompositeResult,
    compute_error,
    integrate,
)

console = Console()
OUTPUT_DIR = Path("output")

DEFAULT_LOWER_BOUND = 0.0
DEFAULT_UPPER_BOUND = 2.0
DEFAULT_SUBINTERVALS = 6
DEFAULT_FUNCTION_EXPRESSION = "x**2 + 2*x + 4"

_ALLOWED_NAMES = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}


def compile_function(expression: str):
    code = compile(expression, "<f(x)>", "eval")

    def function(x: float) -> float:
        return eval(code, {"__builtins__": {}}, {**_ALLOWED_NAMES, "x": x})

    return function


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simpson 3/8 Composite quadrature demo")
    parser.add_argument("--a", type=float, default=None)
    parser.add_argument("--b", type=float, default=None)
    parser.add_argument("--n", type=int, default=None, help="Number of subintervals (must be a multiple of 3)")
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
        console.input(f"Número de subintervalos n (múltiplo de 3) [{DEFAULT_SUBINTERVALS}]: ") or DEFAULT_SUBINTERVALS
    )
    expression = args.function if args.function is not None else (
        console.input(f"f(x) [{DEFAULT_FUNCTION_EXPRESSION}]: ") or DEFAULT_FUNCTION_EXPRESSION
    )
    return lower_bound, upper_bound, subintervals, expression


def render_single_run(result: SimpsonThreeEighthsCompositeResult, error: ErrorMetrics) -> None:
    table = Table(title="Simpson 3/8 Composite — Quadrature Nodes", show_lines=True)
    table.add_column("Node")
    table.add_column("x", justify="right")
    table.add_column("f(x)", justify="right")
    table.add_column("Weight", justify="right")

    for index, node in enumerate(result.nodes):
        table.add_row(f"x{index}", f"{node['x']:.6f}", f"{node['y']:.6f}", str(node["weight"]))

    console.print(table)
    console.print(f"[bold cyan]Approximation:[/]        {result.approximation:.8f}")
    console.print(f"[bold yellow]Reference (Romberg):[/]  {error.exact_value:.8f}")
    console.print(f"[bold red]Absolute error:[/]        {error.absolute_error:.3e}")
    console.print(f"[bold red]Relative error:[/]        {error.relative_error:.3e}")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    args = parse_args()
    lower_bound, upper_bound, subintervals, expression = resolve_inputs(args)
    demo_function = compile_function(expression)

    result = integrate(demo_function, lower_bound, upper_bound, subintervals)
    exact_value = romberg_integrate(demo_function, lower_bound, upper_bound)
    error = compute_error(result.approximation, exact_value)
    render_single_run(result, error)

    bench = benchmark(demo_function, lower_bound, upper_bound, subintervals)
    console.print(f"\n[bold magenta]Execution time:[/] {bench.execution_time_seconds * 1e6:.2f} µs per call")


if __name__ == "__main__":
    main()
