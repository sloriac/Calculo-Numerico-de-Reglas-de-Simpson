# Simpson 1/3 Simple — Web Console

Interfaz gráfica (React + FastAPI) para el motor de cuadratura Simpson 1/3
Simple. La lógica numérica es exactamente la misma que ya está probada con
`pytest` en `backend/simpson/` — esto es solo una capa de presentación.

```
simpson-1-3-web/
├── backend/
│   ├── app.py               FastAPI: expone /api/integrate y /api/experiments
│   ├── main.py                CLI interactiva (Leer a, Leer b, Leer f) — sin navegador
│   ├── schemas.py              Modelos de request/response
│   ├── simpson/                  El paquete ya probado (core, metrics, etc.)
│   ├── tests/                     Los mismos 17 tests de antes
│   ├── static/                     Frontend ya compilado (ver más abajo)
│   └── requirements.txt
└── frontend/
    ├── src/                        Componentes React + TypeScript
    └── package.json
```

Este proyecto reemplaza por completo la carpeta anterior (`simpson_1_3_simple`)
— no se perdió nada: `main.py` (la versión de terminal) sigue aquí, solo que
ahora vive junto con la interfaz web, compartiendo el mismo `simpson/` sin
duplicar código.

## Correr la versión de terminal (sin navegador)

```powershell
cd backend
python main.py
```

## Correr la interfaz web

El frontend **ya viene compilado** dentro de `backend/static/`. Solo necesitas
Python:

```powershell
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

Abre tu navegador en **http://localhost:8000** — ahí está todo: formulario,
tabla de nodos, visualización 3D y dashboard de convergencia, en un solo
servidor.

## Opción B — Modo desarrollo (si vas a modificar el frontend)

Necesitas Node.js instalado (https://nodejs.org, versión LTS). Corres dos
terminales en paralelo:

**Terminal 1 — backend:**
```powershell
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

**Terminal 2 — frontend con recarga en vivo:**
```powershell
cd frontend
npm install
npm run dev
```

Abre **http://localhost:5173** (este sí necesita el backend corriendo en el
puerto 8000 al mismo tiempo, ya que Vite reenvía las llamadas `/api/*`).

Cuando termines de editar y quieras volver a generar la versión de la
Opción A:

```powershell
cd frontend
npm run build
```

Esto compila directo hacia `backend/static/`, listo para que `uvicorn` lo
sirva sin depender de Node.js nunca más.

## Corriendo las pruebas automatizadas

```powershell
cd backend
pytest
```

Debe dar `17 passed` — es el mismo motor de `simpson_1_3_simple`, sin cambios
en la lógica.
