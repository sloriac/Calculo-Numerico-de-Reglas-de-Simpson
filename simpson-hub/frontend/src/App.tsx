import { useState } from "react";
import { SolarSystem } from "./components/SolarSystem";
import { InfoPanel } from "./components/InfoPanel";
import type { MethodConfig } from "./config/methods";

export default function App() {
  const [hovered, setHovered] = useState<MethodConfig | null>(null);

  function handleSelect(method: MethodConfig) {
    window.location.href = method.url;
  }

  return (
    <div className="relative h-screen w-screen">
      <SolarSystem
        onSelect={handleSelect}
        onHover={setHovered}
        hoveredId={hovered?.id ?? null}
      />

      <div className="pointer-events-none absolute left-0 top-0 w-full p-6">
        <h1 className="font-mono text-xl font-bold tracking-tight text-[var(--color-text)]">
          CÁLCULO <span className="text-[var(--color-signal)]">NUMÉRICO</span>
        </h1>
        <p className="mt-1 font-mono text-xs uppercase tracking-[0.2em] text-[var(--color-text-dim)]">
          Reglas de Simpson · Universidad CENFOTEC
        </p>
      </div>

      <div className="pointer-events-none absolute right-0 top-0 p-6 text-right">
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-[var(--color-text-dim)]">
          Selecciona un método
        </p>
        <p className="mt-1 font-mono text-[10px] text-[var(--color-text-dim)]">
          arrastra para rotar · scroll para acercar
        </p>
      </div>

      <InfoPanel method={hovered} />
    </div>
  );
}
