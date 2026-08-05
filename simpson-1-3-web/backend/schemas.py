"""Pydantic schemas shared by the API layer."""

from __future__ import annotations

from pydantic import BaseModel, Field


class IntegrationRequest(BaseModel):
    lower_bound: float = Field(alias="a")
    upper_bound: float = Field(alias="b")
    expression: str = Field(alias="function")

    model_config = {"populate_by_name": True}


class QuadratureNodeResponse(BaseModel):
    x: float
    y: float
    weight: int


class IntegrationResponse(BaseModel):
    nodes: list[QuadratureNodeResponse]
    step_size: float
    approximation: float
    exact_value: float
    absolute_error: float
    relative_error: float
    execution_time_seconds: float
    evaluation_count: int
    curve_x: list[float]
    curve_y: list[float]
    parabola_y: list[float]


class SweepRow(BaseModel):
    label: float
    step_size_h: float | None = None
    approximation: float
    exact_value: float
    absolute_error: float
    relative_error: float
    execution_time_seconds: float | None = None


class ExperimentsResponse(BaseModel):
    width_sweep: list[SweepRow]
    degree_sweep: list[SweepRow]
