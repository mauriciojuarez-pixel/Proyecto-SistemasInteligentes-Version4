# scripts/update_model.py

import sys
import subprocess
from pathlib import Path
from datetime import datetime
import shutil
from dotenv import load_dotenv
import os

# --- Cargar variables de entorno ---
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
if not HUGGINGFACE_TOKEN:
    print("[ERROR] No se encontró HUGGINGFACE_TOKEN en .env")
    sys.exit(1)

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "data" / "models"
BASE_MODEL_DIR = MODELS_DIR / "gemma_2b_it_base"
FINETUNED_DIR = MODELS_DIR / "gemma_2b_it_finetuned"
CHECKPOINTS_DIR = MODELS_DIR / "checkpoints"
LOG_FILE = BASE_DIR / "data" / "outputs" / "logs" / "update_model.log"

# URL del modelo (usando token para autenticación)
BASE_MODEL_REPO = f"https://{HUGGINGFACE_TOKEN}:@huggingface.co/google/gemma-2b-it"

# --- Funciones ---
def log(message: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def ensure_directories():
    for folder in [MODELS_DIR, FINETUNED_DIR, CHECKPOINTS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)
    log("[INFO] Directorios de modelos verificados/creados.")

# scripts/update_model.py

from huggingface_hub import snapshot_download

def clone_or_update_model():
    try:
        log("[INFO] Descargando modelo base desde Hugging Face usando snapshot_download...")
        snapshot_download(
            repo_id="google/gemma-2b-it",
            cache_dir=str(BASE_MODEL_DIR),
            use_auth_token=HUGGINGFACE_TOKEN
        )
        log("[INFO] Modelo base descargado correctamente.")
    except Exception as e:
        log(f"[ERROR] Error descargando modelo base: {e}")
        sys.exit(1)

def prepare_finetune_folder():
    FINETUNED_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    log("[INFO] Carpetas para fine-tuning y checkpoints listas.")

def update_model():
    log("=== Iniciando actualización del modelo ===")
    ensure_directories()
    clone_or_update_model()
    prepare_finetune_folder()
    log("=== Actualización del modelo finalizada ===")

# --- Ejecución ---
if __name__ == "__main__":
    update_model()

