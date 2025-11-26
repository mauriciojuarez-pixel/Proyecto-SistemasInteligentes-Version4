# scripts/limpieza_data_pipeline.py
"""
Pipeline completo de limpieza y análisis de datos.

Ejecuta:
- Carga de CSV desde RAW
- Limpieza (columnas, duplicados, nulos, tipos, fechas)
- Detección y eliminación de outliers
- Análisis estadístico (correlaciones, histogramas y stats)
- Guardado de resultados en PROCESSED y outputs/reports
"""

import sys
from pathlib import Path
# Agregar raíz del proyecto al PYTHONPATH
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))


from pathlib import Path
import pandas as pd

# Importar módulos del paquete limpieza_data
from limpieza_data.file_loader import load_all_raw_csv, save_processed
from limpieza_data.data_cleaner import (
    normalize_columns, remove_duplicates, fill_nulls,
    convert_types, standardize_dates
)
from limpieza_data.anomaly_detection import (
    detect_outliers, remove_anomalies, score_data_quality
)
from limpieza_data.analysis_tools import full_analysis_pipeline

from limpieza_data.config import PROCESSED_PATH, BASE_DIR
from limpieza_data.logger import init_logger, log_info, log_error
import warnings


logger = init_logger()  # Logger global del paquete


def detectar_columnas_fecha(df: pd.DataFrame) -> list:
    """
    Busca columnas que parecen fechas según patrones típicos.
    Evita warnings de pandas y permite múltiples formatos.
    """
    posibles = []
    COMMON_DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y"]

    for col in df.columns:
        try:
            sample = df[col].dropna().astype(str).iloc[:20]
            converted = False

            # Probar formatos comunes
            for fmt in COMMON_DATE_FORMATS:
                parsed = pd.to_datetime(sample, format=fmt, errors="coerce")
                if parsed.notna().sum() / len(parsed) > 0.6:
                    posibles.append(col)
                    converted = True
                    break

            # Si no se pudo con formatos, fallback seguro
            if not converted:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    parsed = pd.to_datetime(sample, errors="coerce")
                    if parsed.notna().sum() / len(parsed) > 0.6:
                        posibles.append(col)

        except Exception:
            continue

    return posibles
    return posibles


def ejecutar_pipeline():
    log_info(logger, "===== INICIANDO PIPELINE DE LIMPIEZA =====")

    try:
        # 1. Cargar datasets desde RAW/
        datasets = load_all_raw_csv()

        for filename, df in datasets.items():
            log_info(logger, f"Procesando archivo: {filename}")

            # 2. Normalizar columnas
            df = normalize_columns(df)

            # 3. Eliminar duplicados
            df = remove_duplicates(df)

            # 4. Rellenar nulos
            df = fill_nulls(df, strategy="mean")

            # 5. Detectar columnas fecha → estandarizar
            cols_fecha = detectar_columnas_fecha(df)
            if cols_fecha:
                df = standardize_dates(df, cols_fecha)

            # 6. Convertir tipos si es necesario (ejemplo genérico)
            df = convert_types(df, {"id": "Int64"}) if "id" in df.columns else df

            # 7. Detección y eliminación de outliers
            df = detect_outliers(df, method="zscore", threshold=3.0)
            df = remove_anomalies(df)

            # 8. Calcular score de calidad
            calidad = score_data_quality(df)
            log_info(logger, f"Score calidad {filename}: {calidad}")

            # 9. Guardar archivo procesado
            out_path = save_processed(df, filename)
            log_info(logger, f"Archivo procesado guardado en: {out_path}")

            # 10. Ejecutar análisis completo (correlaciones, stats, histogramas)
            report_dir = BASE_DIR / "data" / "outputs" / "reports" / filename.replace(".csv", "")
            report_dir.mkdir(parents=True, exist_ok=True)

            full_analysis_pipeline(df, str(report_dir))

        log_info(logger, "===== PIPELINE COMPLETADO EXITOSAMENTE =====")

    except Exception as e:
        log_error(logger, f"ERROR CRÍTICO EN EL PIPELINE: {e}")
        raise


if __name__ == "__main__":
    ejecutar_pipeline()
