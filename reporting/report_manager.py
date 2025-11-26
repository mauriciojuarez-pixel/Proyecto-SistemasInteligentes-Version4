# reporting/report_manager.py

from pathlib import Path
import os
from datetime import datetime
import pandas as pd

# Reporting modules
from reporting.pdf_generator import PDFGenerator
from reporting.charts_export import ChartExporter
from reporting.templates import ReportTemplate

# IA
from agente.prompt_builder import BuilderPrompt
from agente.agent_controller import AgentController
from limpieza_data.logger import init_logger, log_error, log_info

# Limpieza y análisis
from limpieza_data.data_cleaner import (
    normalize_columns,
    remove_duplicates,
    fill_nulls
)

from limpieza_data.analysis_tools import (
    full_analysis_pipeline
)

logger = init_logger("ReportManager")


class ReportManager:
    """
    Orquesta la generación del reporte:
    - Limpieza
    - Análisis
    - Gráficos
    - Interpretación IA (YA GENERADA — se pasa como parámetro)
    - PDF final
    """

    def __init__(self, reports_dir: str = "generado/reports/", controller=None):

        self.reports_dir = Path(reports_dir)
        os.makedirs(self.reports_dir, exist_ok=True)

        # Componentes del sistema
        self.pdf_generator = PDFGenerator()
        self.chart_exporter = ChartExporter()
        self.template = ReportTemplate()

        # IA controller externo si viene del pipeline principal
        self.agent_controller = controller if controller else AgentController()

        # Constructor del prompt (aunque ya no se usa aquí)
        self.prompt_builder = BuilderPrompt()


    # ============================================================
    def generate_full_report(self, df: pd.DataFrame, output_path: str = None, session_id="default"):
        return self.build_full_report(df=df, session_id=session_id)


    # ============================================================
    def build_full_report(
        self,
        df: pd.DataFrame,
        session_id="default",
        controller=None,
        resumen_interpretativo: str = None
    ):
        """
        Construye un reporte completo sin ejecutar IA aquí.
        Se usa el `resumen_interpretativo` ya generado por el pipeline del agente.
        """

        # Selección del controller
        agent_controller = controller if controller else self.agent_controller

        # ============================================================
        # VALIDAR RESUMEN INTERPRETATIVO
        # ============================================================
        if not resumen_interpretativo or resumen_interpretativo.strip() == "":
            log_error(logger, "No se recibió resumen_interpretativo. Usando last_output del agente.")
            resumen_interpretativo = getattr(agent_controller, "last_output", "Interpretación IA no disponible.")

        agent_controller.last_output = resumen_interpretativo

        # ============================================================
        # 1) LIMPIEZA DE DATOS
        # ============================================================
        df = normalize_columns(df)
        df = remove_duplicates(df)
        df = fill_nulls(df)

        # ============================================================
        # 2) ANÁLISIS ESTADÍSTICO
        # ============================================================
        try:
            analysis_results = full_analysis_pipeline(
                df,
                report_dir=str(self.reports_dir)
            )
        except Exception as e:
            log_error(logger, f"Error en análisis estadístico: {e}")
            analysis_results = {}

        # ============================================================
        # 3) GRÁFICOS
        # ============================================================
        try:
            chart_paths = self.chart_exporter.export_all(
                df=df,
                output_dir=str(self.reports_dir)
            )
        except Exception as e:
            log_error(logger, f"Error exportando gráficos: {e}")
            chart_paths = []

        # ============================================================
        # 4) CONSTRUCCIÓN DEL CONTENIDO DEL PDF
        # ============================================================
        report_content = {
            "title": "Reporte Analítico Automático",
            "interpretation": resumen_interpretativo,  # <<--- SE USA DIRECTO
            "analysis": analysis_results,
            "charts": chart_paths,
            "metadata": {
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rows": len(df),
                "columns": len(df.columns),
            }
        }

        # ============================================================
        # 5) GENERAR PDF FINAL
        # ============================================================
        try:
            filename = self.auto_name_report()
            output_path = self.reports_dir / filename

            self.pdf_generator.generate_pdf(
                output_path=output_path,
                content=report_content,
                template=self.template
            )
        except Exception as e:
            log_error(logger, f"Error generando PDF: {e}")
            return None

        log_info(logger, f"PDF generado en: {output_path}")
        return str(output_path)


    # ============================================================
    def auto_name_report(self):
        """Genera nombre automático: report_20250101_145500.pdf"""
        return datetime.now().strftime("report_%Y%m%d_%H%M%S.pdf")
