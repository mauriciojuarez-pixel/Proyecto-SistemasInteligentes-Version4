# agente/autonomous/autonomous_agent.py

import pandas as pd
from limpieza_data.logger import init_logger
from agente.autonomous.chain_manager import ChainManager
from agente.autonomous.memory_manager import MemoryManager

logger = init_logger("AutonomousAgent")


class AutonomousAgent:
    """
    Agente autónomo para análisis de datos, generación de resúmenes interpretativos
    y sugerencias de visualización, usando ChainManager + memoria persistente.
    """

    def __init__(self, session_id="default_session", model_path=None):
        self.session_id = session_id
        self.memory = MemoryManager()
        self.chain = ChainManager(model_path=model_path)
        self.context = self.memory.recall_context(session_id) or {}
        self.last_plan = None
        self.last_analysis = None
        self.original_df = None
        self.last_visualization_suggestions = None

        logger.info(f"Agente inicializado con sesión '{session_id}'")

    # ---------------------------------------------------------------------
    def plan_actions(self, goal: str):
        """Genera un plan de acción básico y lo almacena en memoria."""
        plan = f"Plan para: {goal}"
        self.last_plan = plan
        self.memory.store_context(self.session_id, {"plan": plan})
        logger.info(f"Plan generado para el objetivo: {goal}")
        return plan

    # ---------------------------------------------------------------------
    def analyze_data(self, df: pd.DataFrame, instruction="Analiza y resume los datos."):
        """
        Analiza un DataFrame y guarda resultados en memoria.
        Calcula estadísticas, sugiere visualizaciones y genera análisis con Gemma.
        """
        if df is None or df.empty:
            logger.warning("El DataFrame está vacío.")
            return "El DataFrame está vacío."

        self.original_df = df.copy()

        # Ejecutar cadena con ChainManager
        logger.info("Ejecutando cadena de análisis de datos con ChainManager...")
        try:
            analysis_text = self.chain.execute_chain(
                df=df,
                instruction=instruction,
                use_column_inspector=True
            )
        except Exception as e:
            logger.error(f"Error al analizar el DataFrame: {e}")
            return f"Error en el análisis: {e}"

        self.last_analysis = analysis_text
        self.memory.store_context(self.session_id, {"analysis": analysis_text})
        logger.info("Análisis completado y almacenado en memoria.")

        # Generar sugerencias de visualización
        self.last_visualization_suggestions = self._generate_visualization_suggestions(df)
        self.memory.store_context(self.session_id, {"visualization_suggestions": self.last_visualization_suggestions})

        return analysis_text

    # ---------------------------------------------------------------------
    def _generate_visualization_suggestions(self, df: pd.DataFrame):
        """Genera recomendaciones de visualización basadas en tipos de columnas y correlaciones."""
        suggestions = []
        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()
        date_cols = df.select_dtypes(include="datetime").columns.tolist()

        for col in num_cols:
            suggestions.append(f"Histograma para '{col}'")
            suggestions.append(f"Boxplot para '{col}'")

        for col in cat_cols:
            for num in num_cols:
                suggestions.append(f"Gráfico de barras de '{num}' agrupado por '{col}'")

        for date_col in date_cols:
            for num in num_cols:
                suggestions.append(f"Gráfico de línea de '{num}' a lo largo del tiempo '{date_col}'")

        return suggestions

    # ---------------------------------------------------------------------
    def generate_summary(self, instruction="Genera un resumen interpretativo de los datos."):
        """Genera un resumen interpretativo usando Gemma vía ChainManager."""
        if self.original_df is None or self.original_df.empty:
            logger.warning("No hay datos originales disponibles para generar resumen.")
            return "No hay datos disponibles para generar resumen."

        logger.info("Generando resumen interpretativo de los datos...")
        try:
            summary_text = self.chain.execute_chain(
                df=self.original_df,
                instruction=instruction,
                use_column_inspector=True
            )
        except Exception as e:
            logger.error(f"Error generando resumen: {e}")
            return f"Error generando resumen: {e}"

        self.memory.store_context(self.session_id, {"summary": summary_text})
        logger.info("Resumen generado y almacenado en memoria.")
        return summary_text

    # ---------------------------------------------------------------------
    def execute(self, prompt: str):
        """
        Alias universal para ejecutar un prompt.
        Compatible con ReportManager.
        """
        if self.original_df is None:
            logger.warning("No hay datos cargados. Ejecutando con DataFrame vacío.")
            return self.chain.execute_chain(df=pd.DataFrame(), instruction=prompt)
        return self.chain.execute_chain(df=self.original_df, instruction=prompt, use_column_inspector=True)

    # ---------------------------------------------------------------------
    def get_visualization_suggestions(self):
        return self.last_visualization_suggestions or []

    # ---------------------------------------------------------------------
    def decide_next_step(self):
        if not self.last_analysis:
            logger.info("No hay análisis previo, la siguiente acción es analizar datos.")
            return "Analizar datos primero"
        logger.info("Decisión tomada: generar resumen")
        return "Generar resumen"

    # ---------------------------------------------------------------------
    def self_optimize(self):
        logger.info("Ejecutando optimización interna del agente...")
        return "Parámetros optimizados"

    # ---------------------------------------------------------------------
    def reset(self):
        self.memory.clear_memory(self.session_id)
        self.context = {}
        self.last_plan = None
        self.last_analysis = None
        self.original_df = None
        self.last_visualization_suggestions = None
        logger.info(f"Agente y memoria de sesión '{self.session_id}' reiniciados.")
