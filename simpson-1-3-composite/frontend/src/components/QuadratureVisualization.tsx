import Plot from "react-plotly.js";
import type { Data, Layout } from "plotly.js";
import type { IntegrationResult } from "../lib/api";

interface QuadratureVisualizationProps {
  result: IntegrationResult;
}

const PANEL_COLORS = ["#ff8a3d", "#ff5da2", "#a78bfa", "#facc15", "#4ade80", "#38bdf8"];

export function QuadratureVisualization({ result }: QuadratureVisualizationProps) {
  const depth = (Math.max(...result.curve_x) - Math.min(...result.curve_x)) * 0.08;

  const surfaceTrace: Data = {
    type: "surface",
    x: [result.curve_x, result.curve_x],
    y: [result.curve_x.map(() => 0), result.curve_x.map(() => depth)],
    z: [result.curve_y, result.curve_y],
    colorscale: "Tealgrn",
    showscale: false,
    opacity: 0.85,
    name: "f(x) area",
  };

  const panelTraces: Data[] = result.panels.map((panel, index) => ({
    type: "scatter3d",
    mode: "lines",
    x: panel.x,
    y: panel.x.map(() => 0),
    z: panel.y,
    line: { color: PANEL_COLORS[index % PANEL_COLORS.length], width: 6 },
    name: `Panel ${index + 1}`,
    showlegend: false,
  }));

  const nodeTrace: Data = {
    type: "scatter3d",
    mode: "text+markers",
    x: result.nodes.map((node) => node.x),
    y: result.nodes.map(() => 0),
    z: result.nodes.map((node) => node.y),
    marker: { size: 5, color: "#ffd60a", symbol: "diamond" },
    text: result.nodes.map((node, index) => `x${index}·w${node.weight}`),
    textposition: "top center",
    textfont: { color: "#e6ebf2", size: 9 },
    name: "Nodos",
  };

  const data: Data[] = [surfaceTrace, ...panelTraces, nodeTrace];

  const layout: Partial<Layout> = {
    template: "plotly_dark" as unknown as Layout["template"],
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    scene: {
      xaxis: { title: { text: "x" }, color: "#7c8797" },
      yaxis: { showticklabels: false, title: { text: "" } },
      zaxis: { title: { text: "f(x)" }, color: "#7c8797" },
      camera: { eye: { x: 1.6, y: -1.6, z: 0.9 } },
    },
    margin: { l: 0, r: 0, t: 10, b: 0 },
    showlegend: false,
    font: { color: "#e6ebf2" },
    autosize: true,
  };

  return (
    <Plot
      data={data}
      layout={layout}
      config={{ displaylogo: false, responsive: true, displayModeBar: "hover" }}
      style={{ width: "100%", height: "420px" }}
      useResizeHandler
    />
  );
}
