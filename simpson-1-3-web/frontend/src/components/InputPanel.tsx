import { type FormEvent, useState } from "react";

interface Preset {
  label: string;
  a: number;
  b: number;
  expression: string;
}

const PRESETS: Preset[] = [
  { label: "x² + 2x + 4  (informe)", a: 0, b: 2, expression: "x**2 + 2*x + 4" },
  { label: "sin(x)·e^0.3x", a: 0, b: 4, expression: "sin(x) * exp(0.3*x)" },
  { label: "1 / (1 + x²)", a: -1, b: 1, expression: "1 / (1 + x**2)" },
];

interface InputPanelProps {
  onSubmit: (a: number, b: number, expression: string) => void;
  isLoading: boolean;
}

export function InputPanel({ onSubmit, isLoading }: InputPanelProps) {
  const [a, setA] = useState("0");
  const [b, setB] = useState("2");
  const [expression, setExpression] = useState("x**2 + 2*x + 4");

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    onSubmit(Number(a), Number(b), expression);
  }

  function applyPreset(preset: Preset) {
    setA(String(preset.a));
    setB(String(preset.b));
    setExpression(preset.expression);
    onSubmit(preset.a, preset.b, preset.expression);
  }

  return (
    <div className="rounded-lg border border-[var(--color-panel-border)] bg-[var(--color-panel)] p-5">
      <h2 className="font-mono text-xs uppercase tracking-[0.2em] text-[var(--color-text-dim)]">Parámetros</h2>

      <form onSubmit={handleSubmit} className="mt-4 flex flex-col gap-4">
        <label className="flex flex-col gap-1.5">
          <span className="text-sm text-[var(--color-text-dim)]">Límite inferior · a</span>
          <input
            value={a}
            onChange={(event) => setA(event.target.value)}
            type="number"
            step="any"
            className="rounded-md border border-[var(--color-panel-border)] bg-[var(--color-void)] px-3 py-2 font-mono text-[var(--color-signal)] outline-none focus:border-[var(--color-signal)]"
          />
        </label>

        <label className="flex flex-col gap-1.5">
          <span className="text-sm text-[var(--color-text-dim)]">Límite superior · b</span>
          <input
            value={b}
            onChange={(event) => setB(event.target.value)}
            type="number"
            step="any"
            className="rounded-md border border-[var(--color-panel-border)] bg-[var(--color-void)] px-3 py-2 font-mono text-[var(--color-signal)] outline-none focus:border-[var(--color-signal)]"
          />
        </label>

        <label className="flex flex-col gap-1.5">
          <span className="text-sm text-[var(--color-text-dim)]">f(x)</span>
          <input
            value={expression}
            onChange={(event) => setExpression(event.target.value)}
            type="text"
            spellCheck={false}
            className="rounded-md border border-[var(--color-panel-border)] bg-[var(--color-void)] px-3 py-2 font-mono text-[var(--color-warn)] outline-none focus:border-[var(--color-signal)]"
          />
        </label>

        <button
          type="submit"
          disabled={isLoading}
          className="mt-1 rounded-md bg-[var(--color-signal)] px-4 py-2.5 font-mono text-sm font-semibold uppercase tracking-wider text-[var(--color-void)] transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isLoading ? "Calculando…" : "Calcular ▶"}
        </button>
      </form>

      <div className="mt-6 border-t border-[var(--color-panel-border)] pt-4">
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-[var(--color-text-dim)]">Presets</p>
        <div className="mt-2 flex flex-col gap-2">
          {PRESETS.map((preset) => (
            <button
              key={preset.label}
              type="button"
              onClick={() => applyPreset(preset)}
              className="rounded-md border border-[var(--color-panel-border)] px-3 py-2 text-left text-sm text-[var(--color-text-dim)] transition hover:border-[var(--color-signal)] hover:text-[var(--color-text)]"
            >
              {preset.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
