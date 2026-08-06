import { useMemo, useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import { Html } from "@react-three/drei";
import * as THREE from "three";
import type { Group, Mesh } from "three";
import type { MethodConfig } from "../config/methods";
import { createBandedTexture, createMottledTexture } from "../lib/planetTextures";

interface PlanetProps {
  method: MethodConfig;
  onSelect: (method: MethodConfig) => void;
  onHover: (method: MethodConfig | null) => void;
  isHovered: boolean;
}

export function Planet({ method, onSelect, onHover, isHovered }: PlanetProps) {
  const orbitRef = useRef<Group>(null);
  const meshRef = useRef<Mesh>(null);
  const [angle] = useState(() => Math.random() * Math.PI * 2);

  const texture = useMemo(
    () =>
      method.textureStyle === "banded"
        ? createBandedTexture(method.color, method.textureSeed)
        : createMottledTexture(method.color, method.textureSeed),
    [method.color, method.textureStyle, method.textureSeed]
  );

  useFrame((state, delta) => {
    if (orbitRef.current) {
      const t = angle + state.clock.elapsedTime * method.orbitSpeed;
      orbitRef.current.position.x = Math.cos(t) * method.orbitRadius;
      orbitRef.current.position.z = Math.sin(t) * method.orbitRadius;
    }
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.6;
    }
  });

  const scale = isHovered ? 1.25 : 1;

  return (
    <group ref={orbitRef}>
      <group scale={scale}>
        <mesh
          ref={meshRef}
          onClick={(event) => {
            event.stopPropagation();
            onSelect(method);
          }}
          onPointerOver={(event) => {
            event.stopPropagation();
            onHover(method);
            document.body.style.cursor = "pointer";
          }}
          onPointerOut={() => {
            onHover(null);
            document.body.style.cursor = "auto";
          }}
        >
          <sphereGeometry args={[method.planetSize, 48, 48]} />
          <meshStandardMaterial
            map={texture}
            emissive={method.color}
            emissiveIntensity={isHovered ? 0.35 : 0.08}
            roughness={0.75}
            metalness={0.05}
          />
        </mesh>

        {/* Atmosphere glow shell */}
        <mesh scale={1.12}>
          <sphereGeometry args={[method.planetSize, 32, 32]} />
          <meshBasicMaterial
            color={method.color}
            transparent
            opacity={isHovered ? 0.22 : 0.12}
            side={THREE.BackSide}
          />
        </mesh>

        {method.hasRing && (
          <mesh rotation={[Math.PI / 2.4, 0, 0]}>
            <ringGeometry args={[method.planetSize * 1.5, method.planetSize * 2.3, 64]} />
            <meshBasicMaterial
              color={method.color}
              transparent
              opacity={0.55}
              side={THREE.DoubleSide}
            />
          </mesh>
        )}
      </group>

      <Html
        position={[0, method.planetSize + 0.55, 0]}
        center
        distanceFactor={8}
        style={{ pointerEvents: "none", whiteSpace: "nowrap" }}
      >
        <div
          className="font-mono text-xs tracking-wide transition-opacity"
          style={{ color: method.color, opacity: isHovered ? 1 : 0.55 }}
        >
          {method.shortLabel}
        </div>
      </Html>
    </group>
  );
}
