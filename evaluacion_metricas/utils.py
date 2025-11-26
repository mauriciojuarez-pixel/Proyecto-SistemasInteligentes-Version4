# evaluacion_metricas/utils.py
import json
import os
from typing import Dict, Any
import pandas as pd

class Utils:
    """Funciones auxiliares para la evaluación de métricas."""

    @staticmethod
    def ensure_dir(path: str):
        """Crea la carpeta si no existe."""
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    @staticmethod
    def safe_percentage(value: float) -> float:
        """Asegura que un porcentaje esté entre 0 y 100."""
        return max(0.0, min(100.0, round(value, 2)))

    @staticmethod
    def dict_to_json(data: Dict[str, Any], path: str):
        """Guarda un diccionario como JSON en la ruta indicada."""
        Utils.ensure_dir(os.path.dirname(path))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def dict_to_csv(data: Dict[str, Any], path: str):
        """Guarda un diccionario como CSV en la ruta indicada."""
        Utils.ensure_dir(os.path.dirname(path))
        df = pd.DataFrame([data])
        df.to_csv(path, index=False)
