# scripts/verify_requirements.py

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parent
REQUIREMENTS_FILE = BASE_DIR.parent / "requirements.txt"
LOG_FILE = BASE_DIR.parent / "data" / "outputs" / "logs" / "verify_requirements.log"


# ------------------------------------------------------------
# UTILIDAD: Cargar requirements con limpieza de BOM y NULL
# ------------------------------------------------------------
def read_requirements(file_path: Path):
    """
    Lee requirements.txt eliminando BOM, caracteres nulos, UTF-16 y líneas corruptas.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo requirements.txt no encontrado en {file_path}")

    raw = file_path.read_bytes()

    # 1. Limpiar caracteres nulos (UTF-16 típico)
    cleaned = raw.replace(b"\x00", b"")

    # 2. Eliminar BOM (ÿþ o feff)
    if cleaned.startswith(b"\xef\xbb\xbf"):  # UTF-8 BOM
        cleaned = cleaned[3:]
    if cleaned.startswith(b"\xff\xfe") or cleaned.startswith(b"\xfe\xff"):  # UTF-16 BOM
        cleaned = cleaned[2:]

    # 3. Intentar decodificar correctamente
    try:
        text = cleaned.decode("utf-8")
    except:
        try:
            text = cleaned.decode("latin1")
        except:
            text = cleaned.decode("utf-16", errors="ignore")

    # 4. Limpiar líneas vacías o corruptas
    packages = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if " " in line:
            continue  # evita líneas rotas
        if "==" in line:
            packages.append(line)
        else:
            # si no tiene versión, igual lo agregamos como paquete simple
            packages.append(line)

    return packages


# ------------------------------------------------------------
# Verificar si el paquete está instalado
# ------------------------------------------------------------
def check_package(pkg: str):
    """
    Verifica si un paquete está instalado.
    Usa importación segura (paquetes como 'scikit-learn' se vuelven 'sklearn').
    """
    simple_name = pkg.split("==")[0]

    # Manejar nombre con guiones
    import_name = simple_name.replace("-", "_")

    try:
        __import__(import_name)
        return True
    except ImportError:
        return False


# ------------------------------------------------------------
# Instalar paquete
# ------------------------------------------------------------
def install_package(pkg: str):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])


# ------------------------------------------------------------
# Log
# ------------------------------------------------------------
def log(message: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)


# ------------------------------------------------------------
# Verificación principal
# ------------------------------------------------------------
def verify_requirements(auto_install=False):
    packages = read_requirements(REQUIREMENTS_FILE)
    missing = []

    for pkg in packages:
        pkg_name = pkg.split("==")[0]
        if not check_package(pkg_name):
            missing.append(pkg)
            log(f"[WARNING] Paquete faltante: {pkg}")
            if auto_install:
                try:
                    log(f"[INFO] Instalando {pkg}...")
                    install_package(pkg)
                    log(f"[INFO] Paquete instalado: {pkg}")
                except Exception as e:
                    log(f"[ERROR] Error instalando {pkg}: {e}")

    if not missing:
        log("[INFO] Todas las librerías están instaladas correctamente.")
    else:
        log(f"[INFO] Paquetes faltantes: {missing}")


# ------------------------------------------------------------
# Ejecución
# ------------------------------------------------------------
if __name__ == "__main__":
    verify_requirements(auto_install=True)
