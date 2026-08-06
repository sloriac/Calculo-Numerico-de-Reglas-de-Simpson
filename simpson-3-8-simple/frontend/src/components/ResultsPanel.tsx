import type { IntegrationResult } from "../lib/api";
import { ErrorMeter } from "./ErrorMeter";

interface ReadoutCardProps {
  label: string;
  value: string;
  accent?: string;
}

function ReadoutCard({ label, value, accent }: ReadoutCardProps) {
  return (
    <div className="rounded-lg border border-[var(--color-panel-border)] bg-[var(--color-panel)] p-4">
      <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[var(--color-text-dim)]">{label}</p>
      <p className="mt-1.5 font-mono text-xl font-semibold" style={{ color: accent ?? "var(--color-text)" }}>
        {value}
      </p>
    </div>
  );
}

interface ResultsPanelProps {
  result: IntegrationResult;
}

export function ResultsPanel({ result }: ResultsPanelProps) {
  return (
    <div className="flex flex-col gap-4">
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <ReadoutCard label="Aproximación" value={result.approximation.toFixed(6)} accent="var(--color-signal)" />
        <ReadoutCard label="Referencia (Romberg)" value={result.exact_value.toFixed(6)} />
        <ReadoutCard label="Error absoluto" value={result.absolute_error.toExponential(3)} accent="var(--color-warn)" />
      </div>

      <div className="rounded-lg border border-[var(--color-panel-border)] bg-[var(--color-panel)] p-4">
        <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[var(--color-text-dim)]">
          Error relativo
        </p>
        <div className="mt-2">
          <ErrorMeter relativeError={result.relative_error} />
        </div>
      </div>

      <div className="rounded-lg border border-[var(--color-panel-border)] bg-[var(--color-panel)] p-4">
        <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[var(--color-text-dim)]">
          Nodos de cuadratura
        </p>
        <table className="mt-3 w-full font-mono text-sm">
          <thead>
            <tr className="text-left text-[var(--color-text-dim)]">
              <th className="pb-2 font-normal">Nodo</th>
              <th className="pb-2 font-normal">x</th>
              <th className="pb-2 font-normal">f(x)</th>
              <th className="pb-2 font-normal">Peso</th>
            </tr>
          </thead>
          <tbody>
            {result.nodes.map((node, index) => (
              <tr key={index} className="border-t border-[var(--color-panel-border)]">
                <td className="py-2 text-[var(--color-node)]">x{index}</td>
                <td className="py-2">{node.x.toFixed(6)}</td>
                <td className="py-2">{node.y.toFixed(6)}</td>
                <td className="py-2">{node.weight}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p className="mt-3 font-mono text-xs text-[var(--color-text-dim)]">
          h = {result.step_size.toFixed(6)} · {result.evaluation_count} evaluaciones ·{" "}
          {(result.execution_time_seconds * 1e6).toFixed(2)} µs
        </p>
      </div>
    </div>
  );
}
