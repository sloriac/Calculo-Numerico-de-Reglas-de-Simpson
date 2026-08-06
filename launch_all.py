"""Launches all 4 Simpson quadrature consoles + the hub with a single command.

Run from the repository root (the folder containing simpson-1-3-web,
simpson-1-3-composite, simpson-3-8-simple, simpson-3-8-composite, and
simpson-hub as siblings):

    python launch_all.py

Requires that each project's dependencies were already installed at least
once (pip install -r requirements.txt inside each folder). This script does
not install anything — it only starts the 5 already-configured servers and
stops them all together on Ctrl+C.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SERVICES = [
    {
        "name": "1/3 Simple",
        "cwd": ROOT / "simpson-1-3-web" / "backend",
        "cmd": [sys.executable, "-m", "uvicorn", "app:app", "--port", "8000"],
        "url": "http://localhost:8000",
    },
    {
        "name": "1/3 Compuesta",
        "cwd": ROOT / "simpson-1-3-composite",
        "cmd": [sys.executable, "-m", "uvicorn", "app:app", "--port", "8001"],
        "url": "http://localhost:8001",
    },
    {
        "name": "3/8 Simple",
        "cwd": ROOT / "simpson-3-8-simple",
        "cmd": [sys.executable, "-m", "uvicorn", "app:app", "--port", "8002"],
        "url": "http://localhost:8002",
    },
    {
        "name": "3/8 Compuesta",
        "cwd": ROOT / "simpson-3-8-composite",
        "cmd": [sys.executable, "-m", "uvicorn", "app:app", "--port", "8003"],
        "url": "http://localhost:8003",
    },
    {
        "name": "Hub (inicio)",
        "cwd": ROOT / "simpson-hub",
        "cmd": [sys.executable, "-m", "http.server", "8080", "--directory", "static"],
        "url": "http://localhost:8080",
    },
]


def main() -> None:
    missing = [service for service in SERVICES if not service["cwd"].exists()]
    if missing:
        print("No se encontraron estas carpetas — confirma que corres esto desde la raíz del repo:")
        for service in missing:
            print(f"  ✗ {service['cwd']}")
        sys.exit(1)

    print("Iniciando las 4 consolas + el hub...\n")
    processes = []
    for service in SERVICES:
        print(f"  → {service['name']:<16} {service['url']}")
        proc = subprocess.Popen(service["cmd"], cwd=service["cwd"])
        processes.append(proc)
        time.sleep(0.4)

    print("\nTodo listo. Abre http://localhost:8080")
    print("Presiona Ctrl+C para detener todo.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo todos los servicios...")
        for proc in processes:
            proc.terminate()
        for proc in processes:
            proc.wait()
        print("Listo.")


if __name__ == "__main__":
    main()
