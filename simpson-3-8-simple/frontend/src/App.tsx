import { useEffect, useState } from "react";
import { ApiError, computeIntegration, fetchExperiments, type ExperimentsResult, type IntegrationResult } from "./lib/api";
import { InputPanel } from "./components/InputPanel";
import { ResultsPanel } from "./components/ResultsPanel";
import { QuadratureVisualization } from "./components/QuadratureVisualization";
import { ConvergenceDashboard } from "./components/ConvergenceDashboard";

const HUB_URL = "http://localhost:8080";

function SectionLabel({ children }: { children: string }) {
  return <p className="font-mono text-xs uppercase tracking-[0.2em] text-[var(--color-text-dim)]">// {children}</p>;
}

export default function App() {
  const [result, setResult] = useState<IntegrationResult | null>(null);
  const [experiments, setExperiments] = useState<ExperimentsResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function runIntegration(a: number, b: number, expression: string) {
    setIsLoading(true);
    setError(null);
    try {
      const data = await computeIntegration(a, b, expression);
      setResult(data);
    } catch (caught) {
      setError(caught instanceof ApiError ? caught.message : "Error inesperado al calcular.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    runIntegration(0, 2, "x**2 + 2*x + 4");
    fetchExperiments()
      .then(setExperiments)
      .catch(() => setExperiments(null));
  }, []);

  return (
    <div className="mx-auto min-h-screen max-w-6xl px-6 py-8">
      <header className="mb-8 flex items-start justify-between border-b border-[var(--color-panel-border)] pb-5">
        <div>
          <h1 className="font-mono text-2xl font-bold tracking-tight">
            SIMPSON <span className="text-[var(--color-signal)]">3/8</span> SIMPLE
          </h1>
          <p className="mt-1 text-sm text-[var(--color-text-dim)]">Consola de cuadratura numérica</p>
        </div>

        <a
          href={HUB_URL}
          className="font-mono text-xs uppercase tracking-wider text-[var(--color-text-dim)] transition hover:text-[var(--color-signal)]"
        >
          ← Volver al inicio
        </a>
      </header>

      {error && (
        <div className="mb-6 rounded-lg border border-[var(--color-error-high)] bg-[var(--color-panel)] px-4 py-3 text-sm text-[var(--color-error-high)]">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[280px_1fr]">
        <InputPanel onSubmit={runIntegration} isLoading={isLoading} />

        <div className="flex flex-col gap-6">
          {result && <ResultsPanel result={result} />}

          {result && (
            <div className="rounded-lg border border-[var(--color-panel-border)] bg-[var(--color-panel)] p-4">
              <SectionLabel>Vista 3D de cuadratura</SectionLabel>
              <div className="mt-2">
                <QuadratureVisualization result={result} />
              </div>
            </div>
          )}

          {experiments && (
            <div className="rounded-lg border border-[var(--color-panel-border)] bg-[var(--color-panel)] p-4">
              <SectionLabel>Estudio de convergencia empírico</SectionLabel>
              <div className="mt-2">
                <ConvergenceDashboard experiments={experiments} />
              </div>
            </div>
          )}
        </div>
      </div>

      <footer className="mt-10 border-t border-[var(--color-panel-border)] pt-4 text-center font-mono text-xs text-[var(--color-text-dim)]">
        Cálculo Diferencial e Integral · Universidad CENFOTEC
      </footer>
    </div>
  );
}
