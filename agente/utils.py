# agente/utils.py

import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

def make_json_serializable(obj):
    """Convierte tipos no serializables a formatos JSON-friendly."""
    import pandas as pd

    if isinstance(obj, pd.Timestamp):
        if pd.isna(obj):
            return None
        return obj.isoformat()
    if isinstance(obj, pd.Timedelta):
        return str(obj)
    if obj is pd.NaT:
        return None

    from datetime import datetime, date
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    if isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if pd.isna(obj):
        return None
    if isinstance(obj, set):
        return list(obj)

    return str(obj)


def save_dict_as_json(data: dict, out_file: Path):
    """Guarda un diccionario en un archivo JSON de forma segura."""
    out_file = Path(out_file)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    serializable = {k: make_json_serializable(v) for k, v in data.items()}
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)


def load_json(file_path: Path) -> dict:
    """Carga un archivo JSON y devuelve un diccionario."""
    file_path = Path(file_path)
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def timestamp_now(fmt="%Y%m%d_%H%M%S") -> str:
    """Devuelve timestamp actual como string."""
    return datetime.now().strftime(fmt)


def ensure_dir(path: Path):
    """Crea la carpeta si no existe."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
