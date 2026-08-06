import type { MethodConfig } from "../config/methods";

interface InfoPanelProps {
  method: MethodConfig | null;
}

export function InfoPanel({ method }: InfoPanelProps) {
  return (
    <div className="pointer-events-none absolute bottom-8 left-1/2 w-full max-w-md -translate-x-1/2 px-6">
      <div
        className="rounded-lg border bg-[var(--color-panel)]/90 p-4 backdrop-blur transition-all duration-300"
        style={{
          borderColor: method ? method.color : "var(--color-panel-border)",
          opacity: method ? 1 : 0,
          transform: method ? "translateY(0)" : "translateY(8px)",
        }}
      >
        {method && (
          <>
            <p className="font-mono text-xs uppercase tracking-[0.2em]" style={{ color: method.color }}>
              {method.shortLabel}
            </p>
            <p className="mt-1 font-mono text-lg font-semibold text-[var(--color-text)]">{method.name}</p>
            <p className="mt-1 text-sm text-[var(--color-text-dim)]">{method.description}</p>
            <p className="mt-2 font-mono text-xs text-[var(--color-text-dim)]">Click para entrar →</p>
          </>
        )}
      </div>
    </div>
  );
}
