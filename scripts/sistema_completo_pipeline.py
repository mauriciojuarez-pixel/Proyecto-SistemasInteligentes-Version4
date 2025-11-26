"""
SISTEMA COMPLETO PIPELINE
Integra limpieza, agente IA y generación de reportes PDF.
Registra métricas de desempeño robustas y muestra todo en terminal.
"""

import sys
from pathlib import Path
import pandas as pd
import glob
import warnings

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
from limpieza_data.anomaly_detection import detect_outliers, remove_anomalies, score_data_quality
from limpieza_data.analysis_tools import full_analysis_pipeline
from limpieza_data.logger import init_logger, log_info, log_error

# Agente IA
from agente.agent_controller import AgentController
from agente.utils import timestamp_now

# Report Manager
from reporting.report_manager import ReportManager

# Métricas
from evaluacion_metricas.metrics_manager import MetricsManager

logger = init_logger("SistemaCompletoPipeline")
metrics_manager = MetricsManager(BASE_DIR / "data" / "outputs" / "metrics")

# ---------------------------------------------------------
# Función para detectar columnas de fecha
# ---------------------------------------------------------
def detectar_columnas_fecha(df: pd.DataFrame) -> list:
    posibles = []
    COMMON_DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y"]

    for col in df.columns:
        try:
            sample = df[col].dropna().astype(str).iloc[:50]
            converted = False
            for fmt in COMMON_DATE_FORMATS:
                conv = pd.to_datetime(sample, format=fmt, errors="coerce")
                if conv.notna().mean() > 0.6:
                    posibles.append(col)
                    converted = True
                    break
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
# PIPELINE DE LIMPIEZA
# ---------------------------------------------------------
def pipeline_limpieza():
    log_info(logger, "=== INICIANDO PIPELINE DE LIMPIEZA ===")
    metrics_manager.start_timer()

    datasets = load_all_raw_csv()
    if not datasets:
        raise RuntimeError("No hay archivos CSV dentro de RAW/")

    for filename, df in datasets.items():
        log_info(logger, f"Procesando dataset: {filename}")
        df_orig = df.copy()

        df = normalize_columns(df)
        df = remove_duplicates(df)
        df = fill_nulls(df, strategy="mean")

        cols_fecha = detectar_columnas_fecha(df)
        if cols_fecha:
            df = standardize_dates(df, cols_fecha)

        if "id" in df.columns:
            df = convert_types(df, {"id": "Int64"})

        df = detect_outliers(df, method="zscore", threshold=3.0)
        df = remove_anomalies(df)

        calidad = score_data_quality(df)
        log_info(logger, f"Score de calidad: {calidad}")

        processed_path = save_processed(df, filename)
        log_info(logger, f"Guardado en: {processed_path}")

        output_dir = BASE_DIR / "data" / "outputs" / "reports" / filename.replace(".csv", "")
        output_dir.mkdir(parents=True, exist_ok=True)
        full_analysis_pipeline(df, str(output_dir))

        # Guardar métricas de dataset
        metrics_manager.add_dataset_metrics(
            dataset_name=filename,
            df_raw=df_orig,
            df_processed=df,
            quality_score=calidad
        )

    log_info(logger, "=== PIPELINE DE LIMPIEZA COMPLETADO ===")

# ---------------------------------------------------------
# PIPELINE DEL AGENTE
# ---------------------------------------------------------
def pipeline_agente(df: pd.DataFrame):
    log_info(logger, "=== INICIANDO PIPELINE DEL AGENTE ===")
    controller = AgentController()
    session_id = "main_session"

    # PLAN
    plan_text = controller.plan_goal(session_id, "Analizar dataset y generar resumen ejecutivo")
    print("\n[AGENTE] PLAN:\n", plan_text)

    # ANALISIS
    analysis_text = controller.analyze_dataframe(session_id, df)
    print("\n[AGENTE] ANÁLISIS:\n", analysis_text)

    # RESUMEN EJECUTIVO
    summary_text = controller.generate_summary(session_id)
    print("\n[AGENTE] RESUMEN EJECUTIVO:\n", summary_text)

    # OPTIMIZACIÓN
    optimization_text = controller.optimize_agent(session_id)
    print("\n[AGENTE] OPTIMIZACIÓN:\n", optimization_text)

    # Guardar métricas del agente
    metrics_manager.add_agent_metrics(
        session_id=session_id,
        plan={"text": plan_text},
        analysis={"text": analysis_text},
        summary={"text": summary_text},
        optimization={"text": optimization_text}
    )

    log_info(logger, "=== PIPELINE DEL AGENTE COMPLETADO ===")
    return controller, session_id, {"text": summary_text}

# ---------------------------------------------------------
# PIPELINE DEL REPORTE PDF
# ---------------------------------------------------------
def pipeline_report(df: pd.DataFrame, controller: AgentController, session_id: str, resumen_interpretativo: dict):
    log_info(logger, f"[{timestamp_now()}] Iniciando ReportPipeline...")
    output_dir = BASE_DIR / "data" / "outputs" / "final_reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    manager = ReportManager()
    final_pdf = manager.build_full_report(
        df,
        controller=controller,
        session_id=session_id,
        resumen_interpretativo=resumen_interpretativo.get("text", "")
    )
    log_info(logger, f"PDF generado en: {final_pdf}")

    metrics_manager.add_report_metrics(
        pdf_path=final_pdf,
        df=df,
        summary=resumen_interpretativo,
        num_charts=len(df.columns)
    )

# ---------------------------------------------------------
# PIPELINE PRINCIPAL
# ---------------------------------------------------------
def main():
    try:
        print("\n========== SISTEMA COMPLETO PIPELINE ==========\n")
        metrics_manager.start_timer()

        # 1. Limpieza
        pipeline_limpieza()

        # 2. Cargar datasets procesados
        processed_dir = BASE_DIR / "data" / "datasets" / "processed"
        files = glob.glob(str(processed_dir / "*.csv"))
        if not files:
            raise RuntimeError("No hay archivos procesados en /processed")
        df_list = [pd.read_csv(f) for f in files]
        df = pd.concat(df_list, ignore_index=True)

        # 3. Pipeline agente
        controller, session_id, summary = pipeline_agente(df)

        # 4. Generar reporte PDF
        pipeline_report(df, controller, session_id, resumen_interpretativo=summary)

        # 5. Guardar métricas finales
        metrics_manager.end_timer()
        metrics_file = metrics_manager.save_metrics()
        log_info(logger, f"Métricas guardadas en: {metrics_file}")
        print(f"\n[MÉTRICAS] Guardadas en: {metrics_file}\n")

        # 6. Reset agente
        controller.reset_agent(session_id)
        log_info(logger, f"Agente y memoria de sesión '{session_id}' reseteados correctamente.")

        log_info(logger, "=== SISTEMA COMPLETO PIPELINE FINALIZADO ===")
        print("\n========== PIPELINE FINALIZADO ==========\n")

    except Exception as e:
        log_error(logger, f"Error crítico: {e}")
        print(f"ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    main()
