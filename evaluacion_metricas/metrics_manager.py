# evaluacion_metricas/metrics_manager.py
from pathlib import Path
import json
import time
from datetime import datetime
import pandas as pd
class MetricsManager:
    """
    Gestor central de métricas para pipeline completo:
    - Calidad de datos
    - Desempeño del agente IA
    - Desempeño de reportes PDF
    - Integración total
    """

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metrics = {
            "pipeline_start": None,
            "pipeline_end": None,
            "duration_sec": None,
            "datasets": {},
            "agent": {},
            "report": {},
        }

    # ----------------------------------
    # Tiempo total del pipeline
    # ----------------------------------
    def mark_start(self):
        self.metrics["pipeline_start"] = datetime.now().isoformat()
        self._start_time = time.time()

    def mark_end(self):
        self.metrics["pipeline_end"] = datetime.now().isoformat()
        self.metrics["duration_sec"] = round(time.time() - self._start_time, 2)

    # ----------------------------------
    # Métricas de datasets procesados
    # ----------------------------------
    # En evaluacion_metricas/metrics_manager.py
    def add_dataset_metrics(self, dataset_name: str, df_raw: pd.DataFrame, df_processed: pd.DataFrame, quality_score: float):
        self.metrics["datasets"][dataset_name] = {
            "num_rows_raw": len(df_raw),
            "num_rows_processed": len(df_processed),
            "columns": df_processed.columns.tolist(),
            "quality_score": quality_score
        }

    # ----------------------------------
    # Métricas del agente IA
    # ----------------------------------
    def add_agent_metrics(self, session_id: str, plan: str, analysis: dict, summary: str, optimization: dict):
        self.metrics["agent"][session_id] = {
            "plan_length": len(plan) if plan else 0,
            "analysis_keys": list(analysis.keys()) if analysis else [],
            "summary_length": len(summary) if summary else 0,
            "optimization_keys": list(optimization.keys()) if optimization else [],
        }

    # ----------------------------------
    # Métricas del reporte PDF
    # ----------------------------------
    def add_report_metrics(self, pdf_path: str, df: "pd.DataFrame", summary: str, num_charts: int = 0):
        self.metrics["report"] = {
            "pdf_path": str(pdf_path),
            "num_rows": int(df.shape[0]),
            "num_columns": int(df.shape[1]),
            "summary_length": len(summary),
            "num_charts": num_charts,
        }

    # ----------------------------------
    # Guardado final de métricas
    # ----------------------------------
    def save_metrics(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self.output_dir / f"metrics_{timestamp}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.metrics, f, ensure_ascii=False, indent=4)
        return file_path
    
    def start_timer(self):
        self.mark_start()

    def end_timer(self):
        self.mark_end()
