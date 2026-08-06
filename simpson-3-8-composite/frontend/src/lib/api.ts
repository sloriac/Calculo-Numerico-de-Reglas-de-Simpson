export interface QuadratureNode {
  x: number;
  y: number;
  weight: number;
}

export interface Panel {
  x: number[];
  y: number[];
}

export interface IntegrationResult {
  nodes: QuadratureNode[];
  step_size: number;
  subintervals: number;
  approximation: number;
  exact_value: number;
  absolute_error: number;
  relative_error: number;
  execution_time_seconds: number;
  evaluation_count: number;
  curve_x: number[];
  curve_y: number[];
  panels: Panel[];
}

export interface SweepRow {
  label: number;
  step_size_h: number | null;
  approximation: number;
  exact_value: number;
  absolute_error: number;
  relative_error: number;
  execution_time_seconds: number | null;
}

export interface ExperimentsResult {
  partition_sweep: SweepRow[];
  degree_sweep: SweepRow[];
}

export class ApiError extends Error {}

async function parseErrorDetail(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: string };
    return body.detail ?? response.statusText;
  } catch {
    return response.statusText;
  }
}

export async function computeIntegration(
  a: number,
  b: number,
  n: number,
  expression: string
): Promise<IntegrationResult> {
  const response = await fetch("/api/integrate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ a, b, n, function: expression }),
  });

  if (!response.ok) {
    throw new ApiError(await parseErrorDetail(response));
  }

  return response.json();
}

export async function fetchExperiments(): Promise<ExperimentsResult> {
  const response = await fetch("/api/experiments");

  if (!response.ok) {
    throw new ApiError(await parseErrorDetail(response));
  }

  return response.json();
}
