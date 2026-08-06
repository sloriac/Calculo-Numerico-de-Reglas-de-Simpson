import Plot from "react-plotly.js";
import type { Data, Layout } from "plotly.js";
import type { ExperimentsResult } from "../lib/api";

interface ConvergenceDashboardProps {
  experiments: ExperimentsResult;
}

export function ConvergenceDashboard({ experiments }: ConvergenceDashboardProps) {
  const errorVsN: Data = {
    type: "scatter",
    mode: "lines+markers",
    x: experiments.partition_sweep.map((row) => row.label),
    y: experiments.partition_sweep.map((row) => row.absolute_error),
    marker: { color: "#00e5c7" },
    xaxis: "x",
    yaxis: "y",
  };

  const timeVsN: Data = {
    type: "scatter",
    mode: "lines+markers",
    x: experiments.partition_sweep.map((row) => row.label),
    y: experiments.partition_sweep.map((row) => row.execution_time_seconds ?? 0),
    marker: { color: "#ff8a3d" },
    xaxis: "x2",
    yaxis: "y2",
  };

  const errorVsDegree: Data = {
    type: "bar",
    x: experiments.degree_sweep.map((row) => row.label),
    y: experiments.degree_sweep.map((row) => Math.max(row.absolute_error, 1e-16)),
    marker: { color: "#ffd60a" },
    xaxis: "x3",
    yaxis: "y3",
  };

  const layout: Partial<Layout> = {
    template: "plotly_dark" as unknown as Layout["template"],
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: "#e6ebf2", size: 11 },
    showlegend: false,
    margin: { l: 45, r: 15, t: 30, b: 35 },
    grid: { rows: 1, columns: 3, pattern: "independent" },
    xaxis: { type: "log", title: { text: "n (log)" } },
    yaxis: { type: "log", title: { text: "error abs." } },
    xaxis2: { type: "log", title: { text: "n (log)" } },
    yaxis2: { title: { text: "tiempo (s)" } },
    xaxis3: { title: { text: "grado polinomio" } },
    yaxis3: { type: "log", title: { text: "error abs." } },
    annotations: [
      { text: "Error vs. n", showarrow: false, x: 0.12, y: 1.12, xref: "paper", yref: "paper", font: { size: 12 } },
      { text: "Tiempo vs. n", showarrow: false, x: 0.5, y: 1.12, xref: "paper", yref: "paper", font: { size: 12 } },
      { text: "Error vs. grado", showarrow: false, x: 0.88, y: 1.12, xref: "paper", yref: "paper", font: { size: 12 } },
    ],
  };

  return (
    <Plot
      data={[errorVsN, timeVsN, errorVsDegree]}
      layout={layout}
      config={{ displaylogo: false, responsive: true, displayModeBar: "hover" }}
      style={{ width: "100%", height: "340px" }}
      useResizeHandler
    />
  );
}
