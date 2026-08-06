interface ErrorMeterProps {
  relativeError: number;
}

const MIN_EXPONENT = -12;
const MAX_EXPONENT = 0;

function toPercent(relativeError: number): number {
  const safeError = Math.max(relativeError, 1e-15);
  const exponent = Math.log10(safeError);
  const clamped = Math.min(Math.max(exponent, MIN_EXPONENT), MAX_EXPONENT);
  return ((clamped - MIN_EXPONENT) / (MAX_EXPONENT - MIN_EXPONENT)) * 100;
}

export function ErrorMeter({ relativeError }: ErrorMeterProps) {
  const percent = toPercent(relativeError);
  const hue = 152 - (percent / 100) * 152;

  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex justify-between font-mono text-[10px] uppercase tracking-widest text-[var(--color-text-dim)]">
        <span>exacto</span>
        <span>10⁻¹²</span>
        <span>10⁰</span>
      </div>
      <div className="relative h-2 w-full overflow-hidden rounded-full bg-[var(--color-void)]">
        <div
          className="absolute inset-y-0 left-0 rounded-full transition-all duration-500 ease-out"
          style={{ width: `${Math.max(percent, 2)}%`, backgroundColor: `hsl(${hue}, 85%, 55%)` }}
        />
      </div>
    </div>
  );
}
