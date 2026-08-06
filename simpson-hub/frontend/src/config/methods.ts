export interface MethodConfig {
  id: string;
  name: string;
  shortLabel: string;
  description: string;
  color: string;
  url: string;
  orbitRadius: number;
  orbitSpeed: number;
  planetSize: number;
  author: string;
  textureStyle: "banded" | "mottled";
  textureSeed: number;
  hasRing: boolean;
}

export const METHODS: MethodConfig[] = [
  {
    id: "1-3-simple",
    name: "Simpson 1/3 Simple",
    shortLabel: "1/3 Simple",
    description: "Interpolación cuadrática · 3 nodos fijos",
    color: "#00e5c7",
    url: "http://localhost:8000",
    orbitRadius: 4.2,
    orbitSpeed: 0.22,
    planetSize: 0.62,
    author: "Jose Mario Arias",
    textureStyle: "mottled",
    textureSeed: 11,
    hasRing: false,
  },
  {
    id: "1-3-composite",
    name: "Simpson 1/3 Compuesta",
    shortLabel: "1/3 Compuesta",
    description: "n paneles cuadráticos encadenados",
    color: "#ff8a3d",
    url: "http://localhost:8001",
    orbitRadius: 6.2,
    orbitSpeed: 0.15,
    planetSize: 0.78,
    author: "Jose Mario Arias",
    textureStyle: "banded",
    textureSeed: 42,
    hasRing: false,
  },
  {
    id: "3-8-simple",
    name: "Simpson 3/8 Simple",
    shortLabel: "3/8 Simple",
    description: "Interpolación cúbica · 4 nodos fijos",
    color: "#ffd60a",
    url: "http://localhost:8002",
    orbitRadius: 8.2,
    orbitSpeed: 0.10,
    planetSize: 0.70,
    author: "Jose Mario Arias",
    textureStyle: "banded",
    textureSeed: 7,
    hasRing: false,
  },
  {
    id: "3-8-composite",
    name: "Simpson 3/8 Compuesta",
    shortLabel: "3/8 Compuesta",
    description: "n paneles cúbicos encadenados",
    color: "#a78bfa",
    url: "http://localhost:8003",
    orbitRadius: 10.2,
    orbitSpeed: 0.07,
    planetSize: 0.86,
    author: "Compañero de equipo",
    textureStyle: "banded",
    textureSeed: 99,
    hasRing: true,
  },
];
