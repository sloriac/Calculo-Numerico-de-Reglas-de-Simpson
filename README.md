# Cálculo Numérico — Reglas de Simpson (Suite completa)

Cuatro consolas independientes (una por variante del método), unidas por una
página de inicio en 3D (`simpson-hub`) donde cada método es un planeta.

```
simpson_project_completo/
├── simpson-1-3-web/              Tu 1/3 Simple (ya en producción)
├── simpson-1-3-composite/        1/3 Compuesta
├── simpson-3-8-simple/           3/8 Simple
├── simpson-3-8-composite/        3/8 Compuesta (envuelve Simpson38.py sin tocarlo)
└── simpson-hub/                  Página de inicio — sistema solar en Three.js
```

Cada uno de los 4 métodos es un proyecto **independiente y autosuficiente**
(su propio backend + frontend ya compilado) — no comparten proceso ni
dependen unos de otros para funcionar. El hub solo los enlaza visualmente.

## Asignación de puertos (importante)

El hub asume estos puertos por defecto. Si corres cada uno en un puerto
distinto, ajusta `simpson-hub/frontend/src/config/methods.ts` (campo `url`
de cada método) antes de compilar el hub.

| Método | Carpeta | Puerto |
|---|---|---|
| 1/3 Simple | `simpson-1-3-web/backend` | `8000` |
| 1/3 Compuesta | `simpson-1-3-composite` | `8001` |
| 3/8 Simple | `simpson-3-8-simple` | `8002` |
| 3/8 Compuesta | `simpson-3-8-composite` | `8003` |

## Cómo correr todo (5 terminales)

**Terminal 1 — 1/3 Simple:**
```powershell
cd simpson-1-3-web\backend
pip install -r requirements.txt
uvicorn app:app --port 8000
```

**Terminal 2 — 1/3 Compuesta:**
```powershell
cd simpson-1-3-composite
pip install -r requirements.txt
uvicorn app:app --port 8001
```

**Terminal 3 — 3/8 Simple:**
```powershell
cd simpson-3-8-simple
pip install -r requirements.txt
uvicorn app:app --port 8002
```

**Terminal 4 — 3/8 Compuesta:**
```powershell
cd simpson-3-8-composite
pip install -r requirements.txt
uvicorn app:app --port 8003
```

**Terminal 5 — El Hub (página de inicio):**
```powershell
cd simpson-hub
python -m http.server 8080 --directory static
```

Abre **http://localhost:8080** — ahí está el sistema solar. Arrastra para
rotar la cámara, usa scroll para acercar/alejar, pasa el mouse sobre un
planeta para ver su información, y haz clic para entrar a esa consola.

## Si quieres modificar el diseño del hub

```powershell
cd simpson-hub/frontend
npm install
npm run dev
```

Esto abre con recarga en vivo en `http://localhost:5173`. Cuando termines:

```powershell
npm run build
```

Esto compila directo hacia `simpson-hub/static/`.

## Notas de diseño

- Cada planeta representa un método: color, tamaño y velocidad orbital son
  distintos para cada uno (ver `simpson-hub/frontend/src/config/methods.ts`).
- El brillo del Sol y los planetas usa post-procesamiento (Bloom) via
  `@react-three/postprocessing` — efecto puramente visual, no afecta el
  cálculo de ningún método.
- La paleta de colores (teal, naranja, dorado, violeta) es consistente con
  las 4 consolas individuales, para que se sienta como un solo producto.
