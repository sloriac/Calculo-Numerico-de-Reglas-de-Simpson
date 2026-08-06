"""Pydantic schemas for the Simpson 3/8 Composite API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class IntegrationRequest(BaseModel):
    lower_bound: float = Field(alias="a")
    upper_bound: float = Field(alias="b")
    subintervals: int = Field(alias="n")
    expression: str = Field(alias="function")

    model_config = {"populate_by_name": True}


class QuadratureNodeResponse(BaseModel):
    x: float
    y: float
    weight: int


class PanelResponse(BaseModel):
    x: list[float]
    y: list[float]


class IntegrationResponse(BaseModel):
    nodes: list[QuadratureNodeResponse]
    step_size: float
    subintervals: int
    approximation: float
    exact_value: float
    absolute_error: float
    relative_error: float
    execution_time_seconds: float
    evaluation_count: int
    curve_x: list[float]
    curve_y: list[float]
    panels: list[PanelResponse]


class SweepRow(BaseModel):
    label: float
    step_size_h: float | None = None
    approximation: float
    exact_value: float
    absolute_error: float
    relative_error: float
    execution_time_seconds: float | None = None


class ExperimentsResponse(BaseModel):
    partition_sweep: list[SweepRow]
    degree_sweep: list[SweepRow]
