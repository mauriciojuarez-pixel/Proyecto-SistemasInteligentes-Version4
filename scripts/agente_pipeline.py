# scripts/agente_pipeline.py
import pandas as pd
import sys
from pathlib import Path
import glob

# Añade la carpeta raíz del proyecto al path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from agente.agent_controller import AgentController
from limpieza_data.logger import init_logger, log_info, log_error
from agente.utils import timestamp_now

logger = init_logger("AgentePipeline")


def main():
    try:
        # -------------------------------
        # Crear controlador central
        # -------------------------------
        controller = AgentController()
        log_info(logger, f"[{timestamp_now()}] Controlador central creado correctamente.")

        # -------------------------------
        # Leer archivos procesados
        # -------------------------------
        dataset_folder = Path("data/datasets/processed")
        all_files = glob.glob(str(dataset_folder / "*.csv"))

        if not all_files:
            raise FileNotFoundError(f"No se encontraron archivos CSV en {dataset_folder}")

        # Concatenar todos los CSV en un DataFrame
        df_list = [pd.read_csv(file) for file in all_files]
        df = pd.concat(df_list, ignore_index=True)
        log_info(logger, f"[{timestamp_now()}] DataFrame cargado desde {len(all_files)} archivos.")

        # -------------------------------
        # Crear o obtener agente
        # -------------------------------
        session_id = "test_session"
        agent = controller.get_agent(session_id=session_id)
        log_info(logger, f"[{timestamp_now()}] Agente obtenido/creado con sesión '{session_id}'.")

        # -------------------------------
        # Generar plan de acción
        # -------------------------------
        goal = "Analizar ventas y generar resumen ejecutivo"
        plan = controller.plan_goal(session_id, goal)
        print(f"\nPLAN:\n{plan}\n")

        # -------------------------------
        # Analizar DataFrame
        # -------------------------------
        analysis = controller.analyze_dataframe(session_id, df)
        print(f"\nANÁLISIS:\n{analysis}\n")

        # -------------------------------
        # Generar resumen ejecutivo
        # -------------------------------
        summary = controller.generate_summary(session_id)
        print(f"\nRESUMEN:\n{summary}\n")

        # -------------------------------
        # Optimizar agente
        # -------------------------------
        optimization = controller.optimize_agent(session_id)
        print(f"\nOPTIMIZACIÓN:\n{optimization}\n")

        # -------------------------------
        # Resetear agente
        # -------------------------------
        controller.reset_agent(session_id)
        print(f"\nAgente '{session_id}' reseteado.\n")

        log_info(logger, f"[{timestamp_now()}] Pipeline completado exitosamente.")

    except Exception as e:
        log_error(logger, f"[{timestamp_now()}] Error en el pipeline: {e}")
        print(f"Error ejecutando pipeline: {e}")


if __name__ == "__main__":
    main()
