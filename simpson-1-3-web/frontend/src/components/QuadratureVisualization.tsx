import Plot from "react-plotly.js";
import type { Data, Layout } from "plotly.js";
import type { IntegrationResult } from "../lib/api";

interface QuadratureVisualizationProps {
  result: IntegrationResult;
}

export function QuadratureVisualization({ result }: QuadratureVisualizationProps) {
  const depth = (Math.max(...result.curve_x) - Math.min(...result.curve_x)) * 0.08;

  const data: Data[] = [
    {
      type: "surface",
      x: [result.curve_x, result.curve_x],
      y: [result.curve_x.map(() => 0), result.curve_x.map(() => depth)],
      z: [result.curve_y, result.curve_y],
      colorscale: "Tealgrn",
      showscale: false,
      opacity: 0.92,
      name: "f(x) area",
    },
    {
      type: "scatter3d",
      mode: "lines",
      x: result.curve_x,
      y: result.curve_x.map(() => 0),
      z: result.parabola_y,
      line: { color: "#ff8a3d", width: 7 },
      name: "Parábola interpolante P2(x)",
    },
    {
      type: "scatter3d",
      mode: "text+markers",
      x: result.nodes.map((node) => node.x),
      y: result.nodes.map(() => 0),
      z: result.nodes.map((node) => node.y),
      marker: { size: 6, color: "#ffd60a", symbol: "diamond" },
      text: result.nodes.map((node, index) => `x${index} · w=${node.weight}`),
      textposition: "top center",
      textfont: { color: "#e6ebf2" },
      name: "Nodos",
    },
  ];

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
    showlegend: true,
    legend: { bgcolor: "rgba(0,0,0,0)", font: { color: "#e6ebf2", size: 11 } },
    font: { color: "#e6ebf2" },
    autosize: true,
  };

  return (
    <Plot
      data={data}
      layout={layout}
      config={{ displaylogo: false, responsive: true }}
      style={{ width: "100%", height: "420px" }}
      useResizeHandler
    />
  );
}
