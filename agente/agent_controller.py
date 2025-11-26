# agente/agent_controller.py

import pandas as pd
from agente.autonomous.autonomous_agent import AutonomousAgent
from limpieza_data.logger import init_logger, log_info, log_error
from agente.utils import timestamp_now

logger = init_logger("AgentController")


class AgentController:
    """
    Controlador central para gestionar agentes autónomos.
    Permite crear agentes por sesión, analizar datos, generar planes y resúmenes.
    """

    def __init__(self):
        # Diccionario de agentes por session_id
        self.last_output = None
        self.agents: dict[str, AutonomousAgent] = {}
        log_info(logger, f"[{timestamp_now()}] AgentController inicializado.")

    # ---------------------------------------------------------------------
    def get_agent(self, session_id: str = "default_session", model_path: str = None) -> AutonomousAgent:
        """
        Obtiene un agente existente o crea uno nuevo si no existe.
        """
        if session_id not in self.agents:
            try:
                self.agents[session_id] = AutonomousAgent(session_id=session_id, model_path=model_path)
                log_info(logger, f"[{timestamp_now()}] Nuevo agente creado para sesión '{session_id}'.")
            except Exception as e:
                log_error(logger, f"[{timestamp_now()}] Error creando agente: {e}")
                raise
        return self.agents[session_id]

    # ---------------------------------------------------------------------
    def plan_goal(self, session_id: str, goal: str) -> str:
        """
        Solicita al agente generar un plan de acción para un objetivo.
        """
        agent = self.get_agent(session_id)
        try:
            plan = agent.plan_actions(goal)
            self.last_output = plan

            log_info(logger, f"[{timestamp_now()}] Plan generado para sesión '{session_id}': {plan}")
            return plan
        except Exception as e:
            log_error(logger, f"[{timestamp_now()}] Error generando plan para sesión '{session_id}': {e}")
            raise

    # ---------------------------------------------------------------------
    def analyze_dataframe(self, session_id: str, df: pd.DataFrame, instruction: str = "Analiza y resume los datos.") -> str:
        """
        Envía un DataFrame al agente para análisis y almacenamiento en memoria.
        """
        agent = self.get_agent(session_id)
        try:
            analysis = agent.analyze_data(df, instruction=instruction)
            self.last_output = analysis

            log_info(logger, f"[{timestamp_now()}] Análisis completado para sesión '{session_id}'.")
            return analysis
        except Exception as e:
            log_error(logger, f"[{timestamp_now()}] Error analizando DataFrame para sesión '{session_id}': {e}")
            raise

    # ---------------------------------------------------------------------
    def generate_summary(self, session_id: str, instruction: str = "Genera un resumen interpretativo de los datos.") -> str:
        """
        Solicita al agente generar un resumen a partir del último análisis.
        """
        agent = self.get_agent(session_id)
        try:
            summary = agent.generate_summary(instruction=instruction)
            self.last_output = summary

            log_info(logger, f"[{timestamp_now()}] Resumen generado para sesión '{session_id}'.")
            return summary
        except Exception as e:
            log_error(logger, f"[{timestamp_now()}] Error generando resumen para sesión '{session_id}': {e}")
            raise

    # ---------------------------------------------------------------------
    def optimize_agent(self, session_id: str) -> str:
        """
        Ejecuta la optimización interna del agente.
        """
        agent = self.get_agent(session_id)
        try:
            result = agent.self_optimize()
            self.last_output = result

            log_info(logger, f"[{timestamp_now()}] Agente '{session_id}' optimizado: {result}")
            return result
        except Exception as e:
            log_error(logger, f"[{timestamp_now()}] Error optimizando agente '{session_id}': {e}")
            raise

    # ---------------------------------------------------------------------
    def reset_agent(self, session_id: str):
        """
        Resetea el estado y memoria del agente.
        """
        agent = self.agents.get(session_id)
        if agent:
            try:
                agent.reset()
                log_info(logger, f"[{timestamp_now()}] Agente '{session_id}' reseteado correctamente.")
            except Exception as e:
                log_error(logger, f"[{timestamp_now()}] Error reseteando agente '{session_id}': {e}")
                raise
        else:
            log_info(logger, f"[{timestamp_now()}] No existe agente con sesión '{session_id}' para resetear.")
