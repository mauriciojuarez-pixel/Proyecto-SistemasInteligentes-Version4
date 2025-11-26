# evaluacion_metricas/agent_metrics.py
from typing import List

class AgentMetrics:
    """Clase para calcular métricas de desempeño de resúmenes generados por agentes autónomos."""

    @staticmethod
    def coverage_insights(columns_mentioned: List[str], total_columns: List[str]) -> float:
        """Porcentaje de columnas mencionadas en el resumen."""
        if not total_columns:
            return 0.0
        return round(len(columns_mentioned) / len(total_columns) * 100, 2)

    @staticmethod
    def summary_length_ok(summary: str, min_words: int = 50, max_words: int = 500) -> bool:
        """Verifica si el resumen tiene longitud adecuada."""
        length = len(summary.split())
        return min_words <= length <= max_words

    @staticmethod
    def generation_time(start_time: float, end_time: float) -> float:
        """Tiempo total en segundos para generar el resumen del agente."""
        if start_time > end_time:
            raise ValueError("start_time debe ser menor o igual a end_time")
        return round(end_time - start_time, 4)

    @staticmethod
    def relevance_score(key_insights: List[str], expected_insights: List[str]) -> float:
        """Calcula un score de relevancia basado en insights clave presentes."""
        if not expected_insights:
            return 0.0
        matched = sum(1 for insight in key_insights if insight in expected_insights)
        return round(matched / len(expected_insights) * 100, 2)
