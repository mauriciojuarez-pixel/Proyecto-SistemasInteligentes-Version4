"""
FULL SYSTEM PIPELINE
Integra 3 grandes fases:

1) Limpieza y análisis de datos (RAW → PROCESSED)
2) Pipeline del agente IA (análisis, plan, resumen)
3) Pipeline de reporte PDF usando ReportManager

Requisitos estructurales:
- limpieza_data/
- agente/
- reporting/
"""

import sys
from pathlib import Path
import pandas as pd
import glob

# ---------------------------------------------------------
# Agregar raíz del proyecto al PYTHONPATH
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

# ---------------------------------------------------------
# IMPORTS DEL SISTEMA
# ---------------------------------------------------------
# Limpieza
from limpieza_data.file_loader import load_all_raw_csv, save_processed
from limpieza_data.data_cleaner import (
    normalize_columns, remove_duplicates, fill_nulls,
    convert_types, standardize_dates
)
from limpieza_data.anomaly_detection import (
    detect_outliers, remove_anomalies, score_data_quality
)
from limpieza_data.analysis_tools import full_analysis_pipeline
from limpieza_data.logger import init_logger, log_info, log_error

# Agente IA
from agente.agent_controller import AgentController
from agente.utils import timestamp_now

# Report Manager
from reporting.report_manager import ReportManager


logger = init_logger("FullSystemPipeline")


import warnings

def detectar_columnas_fecha(df: pd.DataFrame) -> list:
    """
    Detecta columnas que parecen contener fechas.
    Se prueban formatos comunes antes de usar pd.to_datetime sin formato.
    """
    posibles = []
    COMMON_DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y"]

    for col in df.columns:
        try:
            sample = df[col].dropna().astype(str).iloc[:50]
            converted = False

            # Probar formatos comunes
            for fmt in COMMON_DATE_FORMATS:
                conv = pd.to_datetime(sample, format=fmt, errors="coerce")
                if conv.notna().mean() > 0.6:
                    posibles.append(col)
                    converted = True
                    break

            # Fallback usando pd.to_datetime pero **silenciando warnings**
            if not converted:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    conv = pd.to_datetime(sample, errors="coerce")
                if conv.notna().mean() > 0.6:
                    posibles.append(col)

        except Exception:
            continue

    return posibles





# ---------------------------------------------------------
# 1) PIPELINE DE LIMPIEZA Y ANÁLISIS (Actualizado)
# ---------------------------------------------------------
def pipeline_limpieza():
    log_info(logger, "=== INICIANDO PIPELINE DE LIMPIEZA ===")

    datasets = load_all_raw_csv()

    if not datasets:
        raise RuntimeError("No hay archivos CSV dentro de RAW/")

    for filename, df in datasets.items():
        log_info(logger, f"Procesando dataset: {filename}")

        # Normalización básica
        df = normalize_columns(df)
        df = remove_duplicates(df)
        df = fill_nulls(df, strategy="mean")

        # Detectar columnas que podrían ser fechas
        cols_fecha = detectar_columnas_fecha(df)
        if cols_fecha:
            # Estandarizar fechas con detección de múltiples formatos y sin warnings
            df = standardize_dates(df, cols_fecha)

        # Asegurar que el ID sea entero
        if "id" in df.columns:
            df = convert_types(df, {"id": "Int64"})

        # Detección y eliminación de outliers/anomalías
        df = detect_outliers(df, method="zscore", threshold=3.0)
        df = remove_anomalies(df)

        # Score de calidad del dataset
        calidad = score_data_quality(df)
        log_info(logger, f"Score de calidad: {calidad}")

        # Guardar dataset procesado
        processed_path = save_processed(df, filename)
        log_info(logger, f"Guardado en: {processed_path}")

        # Directorio para reportes/análisis
        output_dir = BASE_DIR / "data" / "outputs" / "reports" / filename.replace(".csv", "")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Pipeline completo de análisis adicional
        full_analysis_pipeline(df, str(output_dir))

    log_info(logger, "=== PIPELINE DE LIMPIEZA COMPLETADO ===")



# ---------------------------------------------------------
# 2) PIPELINE DEL AGENTE IA
# ---------------------------------------------------------
def pipeline_agente(df: pd.DataFrame):
    log_info(logger, "=== INICIANDO PIPELINE DEL AGENTE ===")

    controller = AgentController()
    session_id = "main_session"

    # Plan
    plan = controller.plan_goal(session_id, "Analizar dataset y generar resumen ejecutivo")
    print("\nPLAN:\n", plan)

    # Análisis
    analysis = controller.analyze_dataframe(session_id, df)
    print("\nANÁLISIS IA:\n", analysis)

    # Resumen interpretativo
    summary = controller.generate_summary(session_id)
    print("\nRESUMEN EJECUTIVO:\n", summary)

    # Optimización
    optimization = controller.optimize_agent(session_id)
    print("\nOPTIMIZACIÓN:\n", optimization)

    log_info(logger, "=== PIPELINE DEL AGENTE COMPLETADO ===")

    return controller, session_id, plan, analysis, summary, optimization


# ---------------------------------------------------------
# 3) PIPELINE DEL REPORTE PDF
# ---------------------------------------------------------
def pipeline_report(df: pd.DataFrame, controller: AgentController, session_id: str, resumen_interpretativo: str):
    log_info(logger, f"[{timestamp_now()}] Iniciando ReportPipeline...")

    output_dir = BASE_DIR / "data" / "outputs" / "final_reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    manager = ReportManager()

    # IMPORTANTE: enviamos el resumen ya generado
    final_pdf = manager.build_full_report(
        df,
        controller=controller,
        session_id=session_id,
        resumen_interpretativo=resumen_interpretativo
    )

    log_info(logger, f"PDF generado en: {final_pdf}")
    print(f"PDF generado en: {final_pdf}")


# ---------------------------------------------------------
# PIPELINE PRINCIPAL (UNE TODO)
# ---------------------------------------------------------
def main():
    try:
        print("\n========== FULL SYSTEM PIPELINE ==========\n")

        # 1. Limpieza
        pipeline_limpieza()

        # 2. Cargar datasets procesados
        processed_dir = BASE_DIR / "data" / "datasets" / "processed"
        files = glob.glob(str(processed_dir / "*.csv"))

        if not files:
            raise RuntimeError("No hay archivos procesados en /processed")

        df_list = [pd.read_csv(f) for f in files]
        df = pd.concat(df_list, ignore_index=True)

        # 3. Agente IA (YA NO se ejecuta de nuevo en el reporte)
        controller, session_id, plan, analysis, summary, optimization = pipeline_agente(df)

        # 4. Generar Reporte PDF usando el MISMO resumen
        pipeline_report(df, controller, session_id, resumen_interpretativo=summary)

        # 5. Reset agente al final
        controller.reset_agent(session_id)
        log_info(logger, f"Agente y memoria de sesión '{session_id}' reseteados correctamente.")

        log_info(logger, "=== FULL SYSTEM PIPELINE COMPLETADO ===")

    except Exception as e:
        log_error(logger, f"Error crítico: {e}")
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
