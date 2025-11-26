# evaluacion_metricas/report_metrics.py
import time
from typing import List

class ReportMetrics:
    """Clase para calcular métricas de desempeño de reportes PDF."""

    @staticmethod
    def coverage_analysis(columns_analyzed: List[str], total_columns: List[str]) -> float:
        """Calcula el % de columnas efectivamente analizadas."""
        if not total_columns:
            return 0.0
        return round(len(columns_analyzed) / len(total_columns) * 100, 2)

    @staticmethod
    def charts_completeness(generated_charts: List[str], expected_charts: List[str]) -> float:
        """Calcula el % de gráficos generados respecto a los esperados."""
        if not expected_charts:
            return 0.0
        return round(len(generated_charts) / len(expected_charts) * 100, 2)

    @staticmethod
    def report_generation_time(start_time: float, end_time: float) -> float:
        """Tiempo total en segundos para generar un reporte."""
        if start_time > end_time:
            raise ValueError("start_time debe ser menor o igual a end_time")
        return round(end_time - start_time, 4)

    @staticmethod
    def completeness_score(coverage: float, chart_score: float) -> float:
        """Score agregado de completitud del reporte."""
        return round((coverage + chart_score) / 2, 2)
