# scripts/setup_env.py

import os
import json
from pathlib import Path
from datetime import datetime

# --- Configuración de rutas base ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATASETS_DIR = DATA_DIR / "datasets"
MODELS_DIR = DATA_DIR / "models"
OUTPUTS_DIR = DATA_DIR / "outputs"

FOLDERS = {
    "datasets_raw": DATASETS_DIR / "raw",
    "datasets_processed": DATASETS_DIR / "processed",
    "datasets_samples": DATASETS_DIR / "samples",
    "models_base": MODELS_DIR / "gemma_2b_it_base",
    "models_finetuned": MODELS_DIR / "gemma_2b_it_finetuned",
    "checkpoints": MODELS_DIR / "checkpoints",
    "reports": OUTPUTS_DIR / "reports",
    "logs": OUTPUTS_DIR / "logs",
    "metrics": OUTPUTS_DIR / "metrics"
}

VERSION_FILE = MODELS_DIR / "gemma_2b_it_finetuned" / "version.json"

# --- Funciones de utilidad ---
def create_folder(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"[INFO] Carpeta creada: {path}")
    else:
        print(f"[INFO] Carpeta ya existe: {path}")

def initialize_directories():
    print("[INFO] Inicializando estructura de carpetas...")
    for key, path in FOLDERS.items():
        create_folder(path)
    print("[INFO] Estructura de carpetas lista.")

def initialize_version_file():
    if not VERSION_FILE.exists():
        VERSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        version_data = {"current_version": "v0", "history": []}
        with open(VERSION_FILE, "w") as f:
            json.dump(version_data, f, indent=4)
        print(f"[INFO] Archivo de versiones creado: {VERSION_FILE}")
    else:
        print(f"[INFO] Archivo de versiones ya existe: {VERSION_FILE}")

def initialize_environment():
    initialize_directories()
    initialize_version_file()
    print("[INFO] Entorno inicializado correctamente.")

# --- Ejecución ---
if __name__ == "__main__":
    initialize_environment()
