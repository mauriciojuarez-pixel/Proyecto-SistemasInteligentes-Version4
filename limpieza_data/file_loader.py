# limpieza_data/file_loader.py

from pathlib import Path
import pandas as pd
from typing import Dict
from limpieza_data.config import RAW_PATH, PROCESSED_PATH, LOG_NAME
from limpieza_data.logger import init_logger, log_info, log_error

logger = init_logger(LOG_NAME)


def load_csv(path: Path, encodings=("utf-8", "latin-1", "ISO-8859-1")) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        log_error(logger, f"CSV no encontrado: {path}")
        raise FileNotFoundError(path)

    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc)
            log_info(logger, f"Cargado CSV: {path.name} (encoding={enc})")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            log_error(logger, f"Error leyendo CSV {path.name}: {e}")
            raise
    raise UnicodeDecodeError(f"No se pudo leer {path} con encodings {encodings}")


def load_excel(path: Path, sheet_name=0) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        log_error(logger, f"Excel no encontrado: {path}")
        raise FileNotFoundError(path)
    try:
        df = pd.read_excel(path, sheet_name=sheet_name)
        log_info(logger, f"Cargado Excel: {path.name} (sheet={sheet_name})")
        return df
    except Exception as e:
        log_error(logger, f"Error leyendo Excel {path.name}: {e}")
        raise


def save_processed(df: pd.DataFrame, filename: str) -> Path:
    out = PROCESSED_PATH / filename
    try:
        PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
        if out.suffix.lower() == ".csv" or out.suffix == "_Limpio":
            out = out.with_suffix(".csv")
            df.to_csv(out, index=False)
        else:
            df.to_excel(out, index=False)
        log_info(logger, f"Guardado procesado: {out}")
        return out
    except Exception as e:
        log_error(logger, f"Error guardando {out}: {e}")
        raise


def load_all_raw_csv() -> Dict[str, pd.DataFrame]:
    datasets = {}
    try:
        for f in RAW_PATH.glob("*.csv"):
            datasets[f.name] = load_csv(f)
        log_info(logger, f"{len(datasets)} archivos CSV cargados desde RAW.")
        return datasets
    except Exception as e:
        log_error(logger, f"Error cargando archivos RAW: {e}")
        raise
