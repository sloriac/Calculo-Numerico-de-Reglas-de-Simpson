import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import type { Mesh } from "three";
import { createMottledTexture } from "../lib/planetTextures";

export function Sun() {
  const meshRef = useRef<Mesh>(null);
  const texture = useMemo(() => createMottledTexture("#ffb347", 3), []);

  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.03;
    }
  });

  return (
    <group>
      <pointLight color="#fff4e0" intensity={45} distance={40} decay={2} />

      <mesh ref={meshRef}>
        <sphereGeometry args={[1.15, 48, 48]} />
        <meshStandardMaterial
          map={texture}
          emissive="#ffb347"
          emissiveIntensity={1.8}
          emissiveMap={texture}
          toneMapped={false}
        />
      </mesh>

      <mesh scale={1.18}>
        <sphereGeometry args={[1.15, 32, 32]} />
        <meshBasicMaterial color="#ffcc66" transparent opacity={0.18} side={THREE.BackSide} />
      </mesh>
      <mesh scale={1.35}>
        <sphereGeometry args={[1.15, 32, 32]} />
        <meshBasicMaterial color="#ff9d42" transparent opacity={0.08} side={THREE.BackSide} />
      </mesh>
    </group>
  );
}
