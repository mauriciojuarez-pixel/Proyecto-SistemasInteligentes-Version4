# agente/config.py

from pathlib import Path

# --- Directorio base del proyecto ---
BASE_DIR = Path(__file__).resolve().parents[2]  # Retrocede hasta la raíz del proyecto

# --- Rutas importantes ---
MODELS_DIR = BASE_DIR / "data" / "models"
GEMMA_2B_IT_PATH = MODELS_DIR / "gemma_2b_it_base" / "models--google--gemma-2b-it" / "snapshots" / "96988410cbdaeb8d5093d1ebdc5a8fb563e02bad" / "gemma-2b-it.gguf"

MEMORY_DIR = BASE_DIR / "data" / "outputs" / "memory"
LOGS_DIR = BASE_DIR / "data" / "outputs" / "logs"
REPORTS_DIR = BASE_DIR / "data" / "outputs" / "reports"

# --- Parámetros del agente ---
DEFAULT_SESSION_ID = "default_session"
DEFAULT_LOG_NAME = "agente"

# --- Crear carpetas si no existen ---
for path in [MEMORY_DIR, LOGS_DIR, REPORTS_DIR]:
    path.mkdir(parents=True, exist_ok=True)
