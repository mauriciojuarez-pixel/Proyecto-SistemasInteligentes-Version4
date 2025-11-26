# limpieza_data/anomaly_detection.py

import pandas as pd
import numpy as np
from scipy.stats import zscore
from limpieza_data.logger import init_logger, log_info, log_error
from limpieza_data.config import LOG_NAME

logger = init_logger(LOG_NAME)


def detect_outliers(df: pd.DataFrame, method: str = "zscore", threshold: float = 3.0) -> pd.DataFrame:
    try:
        dfc = df.copy()
        numeric_cols = dfc.select_dtypes(include="number").columns
        if len(numeric_cols) == 0:
            dfc["is_outlier"] = False
            return dfc

        if method == "zscore":
            zs = np.abs(dfc[numeric_cols].apply(zscore))
            dfc["is_outlier"] = (zs > threshold).any(axis=1)
        elif method == "iqr":
            dfc["is_outlier"] = False
            for col in numeric_cols:
                q1 = dfc[col].quantile(0.25)
                q3 = dfc[col].quantile(0.75)
                iqr = q3 - q1
                mask = (dfc[col] < (q1 - 1.5 * iqr)) | (dfc[col] > (q3 + 1.5 * iqr))
                dfc.loc[mask, "is_outlier"] = True
        else:
            log_error(logger, f"Método desconocido detect_outliers: {method}")
            raise ValueError("Método no soportado")

        log_info(logger, f"Outliers detectados con método {method}.")
        return dfc
    except Exception as e:
        log_error(logger, f"Error detectando outliers: {e}")
        raise


def remove_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    try:
        if "is_outlier" not in df.columns:
            log_info(logger, "Columna 'is_outlier' no encontrada; no se eliminará nada.")
            return df
        before = len(df)
        clean = df[df["is_outlier"] == False].drop(columns=["is_outlier"])
        log_info(logger, f"Anomalías eliminadas: {before - len(clean)}")
        return clean
    except Exception as e:
        log_error(logger, f"Error eliminando anomalías: {e}")
        raise


def flag_noisy_data(df: pd.DataFrame, noise_thresh: float = 2.5) -> pd.DataFrame:
    try:
        dfc = df.copy()
        numeric_cols = dfc.select_dtypes(include="number").columns
        if len(numeric_cols) == 0:
            dfc["noisy_score"] = 0.0
            dfc["is_noisy"] = False
            return dfc

        dfc["noisy_score"] = dfc[numeric_cols].apply(lambda x: np.abs(x - x.mean()) / (x.std() + 1e-8)).mean(axis=1)
        dfc["is_noisy"] = dfc["noisy_score"] > noise_thresh
        log_info(logger, "Datos ruidosos etiquetados.")
        return dfc
    except Exception as e:
        log_error(logger, f"Error marcando datos ruidosos: {e}")
        raise


def score_data_quality(df: pd.DataFrame) -> float:
    try:
        total = len(df)
        if total == 0:
            return 0.0
        null_ratio = df.isnull().sum().sum() / (total * len(df.columns))
        outlier_ratio = df.get("is_outlier", pd.Series([False] * total)).mean()
        score = max(0, 1 - (null_ratio + outlier_ratio))
        log_info(logger, f"Score de calidad calculado: {score:.3f}")
        return round(score, 3)
    except Exception as e:
        log_error(logger, f"Error calculando score de calidad: {e}")
        raise
