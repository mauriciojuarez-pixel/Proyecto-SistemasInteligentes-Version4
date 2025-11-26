# limpieza_data/data_cleaner.py

from pathlib import Path
import pandas as pd
from limpieza_data.logger import init_logger, log_info, log_error
from limpieza_data.config import LOG_NAME

logger = init_logger(LOG_NAME)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df = df.copy()
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        log_info(logger, "Columnas normalizadas.")
        return df
    except Exception as e:
        log_error(logger, f"Error normalizando columnas: {e}")
        raise


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    try:
        before = len(df)
        df2 = df.drop_duplicates()
        log_info(logger, f"Duplicados eliminados: {before - len(df2)}")
        return df2
    except Exception as e:
        log_error(logger, f"Error eliminando duplicados: {e}")
        raise


def fill_nulls(df: pd.DataFrame, strategy: str = "mean", fill_value=None) -> pd.DataFrame:
    try:
        df = df.copy()
        num_cols = df.select_dtypes(include="number").columns
        if strategy == "mean":
            for c in num_cols:
                df[c].fillna(df[c].mean(), inplace=True)
        elif strategy == "median":
            for c in num_cols:
                df[c].fillna(df[c].median(), inplace=True)
        elif strategy == "constant":
            df.fillna(fill_value, inplace=True)
        else:
            log_info(logger, f"Estrategia desconocida: {strategy}. No se llenaron nulos.")
        log_info(logger, "Valores nulos procesados.")
        return df
    except Exception as e:
        log_error(logger, f"Error rellenando nulos: {e}")
        raise


def convert_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:
    try:
        df = df.copy()
        for col, t in type_map.items():
            if col in df.columns:
                df[col] = df[col].astype(t, errors="ignore")
        log_info(logger, "Conversiones de tipo aplicadas.")
        return df
    except Exception as e:
        log_error(logger, f"Error conviertiendo tipos: {e}")
        raise


def standardize_dates(df: pd.DataFrame, date_cols: list, fmt=None) -> pd.DataFrame:
    try:
        df = df.copy()
        for c in date_cols:
            if c in df.columns:
                df[c] = pd.to_datetime(df[c], errors="coerce")
                if fmt:
                    df[c] = df[c].dt.strftime(fmt)
        log_info(logger, f"Fechas estandarizadas: {date_cols}")
        return df
    except Exception as e:
        log_error(logger, f"Error estandarizando fechas: {e}")
        raise
