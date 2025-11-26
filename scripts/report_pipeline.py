"""
Pipeline de generación de reportes PDF usando:
- ReportManager
- PDFGenerator
- ChartExporter
- Templates (versión con clase)
"""
# scripts/report_pipeline.py
import pandas as pd
from pathlib import Path
import glob
import sys

# ==========================================
# Agregar raíz del proyecto al PYTHONPATH
# ==========================================
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

# ==========================================
# Importar módulos del sistema de reportes
# ==========================================
from reporting.report_manager import ReportManager
from limpieza_data.logger import init_logger, log_info, log_error


# ==========================================
# Setup de logger
# ==========================================
logger = init_logger("ReportPipeline")


def timestamp_now():
    """Pequeña función local porque limpieza_data no incluye utils."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    try:
        log_info(logger, f"[{timestamp_now()}] Iniciando Report Pipeline...")

        # =======================================================
        # 1. Cargar todos los CSV procesados desde /processed
        # =======================================================
        processed_dir = BASE_DIR / "data" / "datasets" / "processed"
        files = glob.glob(str(processed_dir / "*.csv"))

        if not files:
            raise FileNotFoundError(f"No existen archivos .csv en {processed_dir}")

        df_list = [pd.read_csv(file) for file in files]
        df = pd.concat(df_list, ignore_index=True)

        log_info(logger, f"[{timestamp_now()}] {len(files)} archivos cargados.")

        # =======================================================
        # 2. Crear carpeta de salida para el PDF final
        # =======================================================
        output_dir = BASE_DIR / "data" / "outputs" / "final_reports"
        output_dir.mkdir(parents=True, exist_ok=True)

        pdf_path = output_dir / "reporte_final.pdf"

        # =======================================================
        # 3. Ejecutar ReportManager
        # =======================================================
        manager = ReportManager()

        log_info(logger, f"[{timestamp_now()}] Generando el reporte PDF...")

        manager.generate_full_report(
            df=df,
            output_path=str(pdf_path)
        )

        # =======================================================
        # 4. Finalizar
        # =======================================================
        log_info(logger, f"[{timestamp_now()}] Reporte generado en: {pdf_path}")
        print(f"Reporte generado en: {pdf_path}")

    except Exception as e:
        log_error(logger, f"Error ejecutando Report Pipeline: {e}")
        print(f"Error ejecutando Report Pipeline: {e}")


if __name__ == "__main__":
    main()
