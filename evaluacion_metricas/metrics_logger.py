# evaluacion_metricas/metrics_logger.py
import json
import os
from datetime import datetime
from .utils import Utils

class MetricsLogger:
    """Clase para registrar métricas en JSON o CSV con timestamp."""

    def __init__(self, log_dir: str = "data/outputs/metrics/"):
        self.log_dir = log_dir
        Utils.ensure_dir(self.log_dir)

    def log_metrics(self, metrics: dict, filename: str = None, as_csv: bool = False):
        """Guarda las métricas en JSON o CSV."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not filename:
            filename = f"metrics_{timestamp}.json"
        path = os.path.join(self.log_dir, filename)
        if as_csv:
            if not filename.endswith(".csv"):
                path = path.replace(".json", ".csv")
            Utils.dict_to_csv(metrics, path)
        else:
            Utils.dict_to_json(metrics, path)
        return path

    def append_metrics(self, metrics: dict, filename: str):
        """Agrega métricas a un archivo JSON existente."""
        path = os.path.join(self.log_dir, filename)
        existing = {}
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        # Generar key única por timestamp
        key = datetime.now().strftime("%Y%m%d_%H%M%S")
        existing[key] = metrics
        Utils.dict_to_json(existing, path)
        return path
