import { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Stars } from "@react-three/drei";
import { EffectComposer, Bloom } from "@react-three/postprocessing";
import { Sun } from "./Sun";
import { Planet } from "./Planet";
import { OrbitRing } from "./OrbitRing";
import { METHODS, type MethodConfig } from "../config/methods";

interface SolarSystemProps {
  onSelect: (method: MethodConfig) => void;
  onHover: (method: MethodConfig | null) => void;
  hoveredId: string | null;
}

export function SolarSystem({ onSelect, onHover, hoveredId }: SolarSystemProps) {
  return (
    <Canvas camera={{ position: [0, 9, 16], fov: 50 }} dpr={[1, 2]}>
      <color attach="background" args={["#05070d"]} />
      <ambientLight intensity={0.15} />

      <Suspense fallback={null}>
        <Stars radius={80} depth={50} count={4000} factor={3} saturation={0} fade speed={0.5} />

        <Sun />

        {METHODS.map((method) => (
          <OrbitRing key={`ring-${method.id}`} radius={method.orbitRadius} color={method.color} />
        ))}

        {METHODS.map((method) => (
          <Planet
            key={method.id}
            method={method}
            onSelect={onSelect}
            onHover={onHover}
            isHovered={hoveredId === method.id}
          />
        ))}

        <EffectComposer>
          <Bloom intensity={0.6} luminanceThreshold={0.25} luminanceSmoothing={0.9} mipmapBlur />
        </EffectComposer>
      </Suspense>

      <OrbitControls
        enablePan={false}
        minDistance={8}
        maxDistance={28}
        maxPolarAngle={Math.PI / 2.1}
        autoRotate
        autoRotateSpeed={0.15}
      />
    </Canvas>
  );
}
