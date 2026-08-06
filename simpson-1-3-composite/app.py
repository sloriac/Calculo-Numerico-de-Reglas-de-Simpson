"""FastAPI application: thin API layer over the simpson (composite) package."""

from __future__ import annotations

import math
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from schemas import ExperimentsResponse, IntegrationRequest, IntegrationResponse, PanelResponse, QuadratureNodeResponse, SweepRow
from simpson.core import integrate
from simpson.experiments import run_partition_sweep, run_polynomial_degree_sweep
from simpson.expression import compile_function
from simpson.metrics import benchmark, compute_error
from simpson.reference import romberg_integrate
from simpson.visualization import sample_curve, sample_panels

FRONTEND_DIST = Path(__file__).parent / "static"

app = FastAPI(title="Simpson 1/3 Composite API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _error_study_function(x: float) -> float:
    return math.sin(x) * math.exp(0.3 * x)


@app.post("/api/integrate", response_model=IntegrationResponse)
def integrate_endpoint(request: IntegrationRequest) -> IntegrationResponse:
    try:
        function = compile_function(request.expression)
        result = integrate(function, request.lower_bound, request.upper_bound, request.subintervals)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except (SyntaxError, NameError, ZeroDivisionError) as error:
        raise HTTPException(status_code=422, detail=f"Invalid expression: {error}") from error

    exact_value = romberg_integrate(function, request.lower_bound, request.upper_bound)
    error_metrics = compute_error(result, exact_value)
    bench = benchmark(function, request.lower_bound, request.upper_bound, request.subintervals)
    curve_x, curve_y = sample_curve(function, result)
    panels = sample_panels(result)

    return IntegrationResponse(
        nodes=[QuadratureNodeResponse(x=node.x, y=node.y, weight=node.weight) for node in result.nodes],
        step_size=result.step_size,
        subintervals=result.subintervals,
        approximation=result.approximation,
        exact_value=exact_value,
        absolute_error=error_metrics.absolute_error,
        relative_error=error_metrics.relative_error,
        execution_time_seconds=bench.execution_time_seconds,
        evaluation_count=bench.evaluation_count,
        curve_x=curve_x,
        curve_y=curve_y,
        panels=[PanelResponse(x=panel["x"], y=panel["y"]) for panel in panels],
    )


@app.get("/api/experiments", response_model=ExperimentsResponse)
def experiments_endpoint() -> ExperimentsResponse:
    partition_sweep_df = run_partition_sweep(_error_study_function, 0.0, 4.0, [2, 4, 6, 10, 20, 50, 100])
    degree_sweep_df = run_polynomial_degree_sweep(0.0, 2.0, subintervals=8, degrees=[1, 2, 3, 4, 5, 6])

    partition_rows = [
        SweepRow(
            label=row.subintervals_n,
            step_size_h=row.step_size_h,
            approximation=row.approximation,
            exact_value=row.exact_value,
            absolute_error=row.absolute_error,
            relative_error=row.relative_error,
            execution_time_seconds=row.execution_time_seconds,
        )
        for row in partition_sweep_df.itertuples()
    ]
    degree_rows = [
        SweepRow(
            label=row.polynomial_degree,
            approximation=row.approximation,
            exact_value=row.exact_value,
            absolute_error=row.absolute_error,
            relative_error=row.relative_error,
        )
        for row in degree_sweep_df.itertuples()
    ]

    return ExperimentsResponse(partition_sweep=partition_rows, degree_sweep=degree_rows)


if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
