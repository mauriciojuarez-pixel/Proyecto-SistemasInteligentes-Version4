# limpieza_data/analysis_tools.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import date, datetime
from pathlib import Path
from limpieza_data.logger import init_logger, log_info, log_error
from limpieza_data.config import LOG_NAME

logger = init_logger(LOG_NAME)


def compute_correlations(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    try:
        corr = df.corr(method=method, numeric_only=True)
        log_info(logger, f"Matriz de correlación ({method}) calculada.")
        return corr
    except Exception as e:
        log_error(logger, f"Error al calcular correlaciones: {e}")
        raise


def detect_multicollinearity(df: pd.DataFrame, threshold: float = 0.9) -> list:
    try:
        corr = df.corr(numeric_only=True).abs()
        upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        high = [
            (col, row, corr_val)
            for col in upper.columns
            for row, corr_val in upper[col].items()
            if corr_val > threshold
        ]
        log_info(logger, f"{len(high)} pares con alta correlación (> {threshold}).")
        return high
    except Exception as e:
        log_error(logger, f"Error detectando multicolinealidad: {e}")
        raise


def visualize_correlation_matrix(corr_matrix: pd.DataFrame, out_file: str):
    """
    Dibuja y guarda un heatmap de la matriz de correlación.
    Protege contra matrices vacías o con dimensiones inválidas.
    """
    try:
        if corr_matrix is None:
            raise ValueError("corr_matrix es None")

        # Asegurarse que sea DataFrame y tenga tamaño
        if not isinstance(corr_matrix, (pd.DataFrame,)):
            corr_matrix = pd.DataFrame(corr_matrix)

        if corr_matrix.size == 0:
            # Nothing to plot
            return None

        # Evitar heatmap si hay <2 columnas numéricas útiles
        if corr_matrix.shape[0] < 2 or corr_matrix.shape[1] < 2:
            # Guardar una figura simple o saltar
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.text(0.5, 0.5, "No hay suficientes columnas numéricas\npara calcular un heatmap",
                    ha="center", va="center")
            ax.axis("off")
            fig.savefig(out_file, bbox_inches="tight")
            plt.close(fig)
            return out_file

        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=False, cmap="viridis")
        plt.title("Matriz de Correlación")
        plt.tight_layout()
        plt.savefig(out_file)
        plt.close()
        return out_file

    except Exception as e:
        # Log desde el módulo que llame a esta función
        raise


def generate_histograms(df: pd.DataFrame, out_dir: str):
    try:
        out_path = Path(out_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        numeric = df.select_dtypes(include="number").columns
        for col in numeric:
            plt.figure()
            df[col].hist(bins=20)
            plt.title(f"Histograma - {col}")
            plt.xlabel(col)
            plt.ylabel("Frecuencia")
            plt.savefig(out_path / f"{col}_hist.png")
            plt.close()
        log_info(logger, f"Histogramas guardados en: {out_path}")
    except Exception as e:
        log_error(logger, f"Error generando histogramas: {e}")
        raise


def _make_json_serializable(obj):
    """Convierte tipos no serializables a formatos JSON-friendly."""
    # pandas Timestamp / datetime
    try:
        import pandas as _pd
        if isinstance(obj, _pd.Timestamp):
            if pd.isna(obj):
                return None
            return obj.isoformat()
        if isinstance(obj, _pd.Timedelta):
            return str(obj)
        if obj is _pd.NaT:
            return None
    except Exception:
        pass

    # datetime / date
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    # numpy scalars
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    if isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    if isinstance(obj, (np.bool_ , bool)):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()

    # pandas/numpy NA or nan
    try:
        if pd.isna(obj):
            return None
    except Exception:
        pass

    # sets -> list
    if isinstance(obj, set):
        return list(obj)

    # fallback: str()
    return str(obj)


def summary_to_json(summary_df: pd.DataFrame, out_file: str):
    """
    Exporta el DataFrame `summary_df` a JSON en out_file convirtiendo
    cualquier tipo no serializable a una representación JSON-friendly.
    """
    try:
        out_path = Path(out_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # Convertir DataFrame a diccionario (orient=index) para mantener filas
        raw = summary_df.to_dict(orient="index")

        # Recorrer y convertir valores no serializables
        def convert_value(v):
            # si es dict recursivo
            if isinstance(v, dict):
                return {k: convert_value(val) for k, val in v.items()}
            # listas/tuplas
            if isinstance(v, (list, tuple)):
                return [convert_value(x) for x in v]
            return _make_json_serializable(v)

        serializable = {str(k): convert_value(v) for k, v in raw.items()}

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)

        log_info(logger, f"Resumen exportado a JSON: {out_path}")

    except Exception as e:
        log_error(logger, f"Error exportando resumen a JSON: {e}")
        raise

def compute_descriptive_stats(df: pd.DataFrame) -> dict:
    """
    Retorna estadísticas descriptivas (mean, std, min, max) de las columnas numéricas.
    """
    numeric_df = df.select_dtypes(include="number")
    return numeric_df.describe().to_dict()



# limpieza_data/analysis_tools.py
def full_analysis_pipeline(df: pd.DataFrame, report_dir: str) -> dict:
    results = {}
    # 1. Correlaciones
    numeric_df = df.select_dtypes(include="number")
    results["correlation"] = numeric_df.corr().to_dict()

    # 2. Estadísticas descriptivas
    results["stats"] = numeric_df.describe().to_dict()

    # 3. Multicolinealidad (opcional)
    results["high_corr_pairs"] = detect_multicollinearity(numeric_df, threshold=0.9)

    # Guardar resumen JSON
    try:
        summary_path = Path(report_dir) / "summary.json"
        import json
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
    except Exception as e:
        log_error(logger, f"Error exportando resumen a JSON: {e}")

    return results


def describe_dataset(df):
    stats = compute_descriptive_stats(df)
    corrs = compute_correlations(df)
    multi = detect_multicollinearity(df)
    return {
        "stats": stats.to_dict(),
        "correlations": corrs.to_dict(),
        "multicollinearity": multi,
    }
