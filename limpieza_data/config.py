# limpieza_data/config.py

from pathlib import Path

# --- Directorio base del proyecto ---
BASE_DIR = Path(__file__).resolve().parents[1]

# --- Rutas del dataset ---
RAW_PATH = BASE_DIR / "data" / "datasets" / "raw"
PROCESSED_PATH = BASE_DIR / "data" / "datasets" / "processed"

# Crear carpetas si no existen
RAW_PATH.mkdir(parents=True, exist_ok=True)
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

# --- Nombre del logger global ---
LOG_NAME = "limpieza_data"
