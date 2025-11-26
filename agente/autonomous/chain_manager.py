# agente/autonomous/chain_manager.py

import pandas as pd
from pathlib import Path
from time import time
from langchain_classic.prompts import PromptTemplate
from langchain_classic.memory import ConversationBufferMemory
from llama_cpp import Llama

from limpieza_data.logger import init_logger, log_info, log_error
from agente.prompt_builder import BuilderPrompt
from agente.utils import timestamp_now

logger = init_logger("ChainManager")


class ChainManager:
    """
    Administra la construcción de prompts y la ejecución del modelo GGUF (Gemma 2B IT)
    usando BuilderPrompt y llama_cpp, con logging de tiempos y errores.
    """

    def __init__(self, model_path=None):
        try:
            self.model_path = model_path or (
                "data/models/gemma_2b_it_base/"
                "models--google--gemma-2b-it/"
                "snapshots/96988410cbdaeb8d5093d1ebdc5a8fb563e02bad/"
                "gemma-2b-it.gguf"
            )
            if not Path(self.model_path).exists():
                raise FileNotFoundError(f"Modelo GGUF no encontrado en:\n{self.model_path}")

            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=4096,
                n_threads=6,
                n_gpu_layers=20,
                verbose=False
            )

            self.memory = ConversationBufferMemory(memory_key="chat_history")
            self.trace = []

            log_info(logger, f"[{timestamp_now()}] ChainManager inicializado. Modelo: {self.model_path}")

        except Exception as e:
            log_error(logger, f"[{timestamp_now()}] Error inicializando ChainManager: {e}")
            raise

    # ---------------------------------------------------------------------
    def build_prompt(self, df=None, metadata=None, instruction="Analiza y resume los datos.", use_column_inspector=True):
        """
        Construye un prompt profesional usando BuilderPrompt.
        """
        start_time = time()
        try:
            builder = BuilderPrompt()
            df_for_prompt = df if isinstance(df, pd.DataFrame) else pd.DataFrame()

            prompt_text = builder.build_report_prompt(
                df=df_for_prompt,
                metadata=metadata,
                instruction=instruction,
                use_column_inspector=use_column_inspector
            )
            prompt = PromptTemplate(input_variables=["context"], template=prompt_text)

            elapsed = time() - start_time
            self.trace.append(f"Prompt construido correctamente en {elapsed:.2f}s.")
            log_info(logger, f"[{timestamp_now()}] Prompt generado en {elapsed:.2f}s.")
            return prompt
        except Exception as e:
            log_error(logger, f"[{timestamp_now()}] Error al construir prompt: {e}")
            return None

    # ---------------------------------------------------------------------
    def execute_prompt(self, prompt_text: str, max_tokens: int = 1024):
        """
        Ejecuta un prompt directamente usando el modelo GGUF.
        """
        start_time = time()
        try:
            response_raw = self.llm(prompt_text, max_tokens=max_tokens)
            response_text = response_raw["choices"][0]["text"].strip()

            # Guardar en memoria
            self.memory.chat_memory.add_user_message(prompt_text)
            self.memory.chat_memory.add_ai_message(response_text)

            elapsed = time() - start_time
            self.trace.append(f"Prompt ejecutado en {elapsed:.2f}s.")
            log_info(logger, f"[{timestamp_now()}] Modelo ejecutado correctamente en {elapsed:.2f}s.")
            return response_text
        except Exception as e:
            log_error(logger, f"[{timestamp_now()}] Error ejecutando prompt: {e}")
            return f"Error ejecutando prompt: {e}"

    # ---------------------------------------------------------------------
    def execute_chain(self, df=None, metadata=None, instruction="Analiza y resume los datos.", use_column_inspector=True, max_tokens=1024):
        """
        Genera prompt y lo ejecuta automáticamente.
        """
        try:
            prompt = self.build_prompt(df=df, metadata=metadata, instruction=instruction, use_column_inspector=use_column_inspector)
            if prompt is None:
                return "Error: no se pudo generar prompt."
            prompt_text = prompt.format(context=getattr(self.memory, "buffer", ""))
            return self.execute_prompt(prompt_text, max_tokens=max_tokens)
        except Exception as e:
            log_error(logger, f"[{timestamp_now()}] Error ejecutando cadena: {e}")
            return f"Error ejecutando cadena: {e}"

    # ---------------------------------------------------------------------
    def inject_context(self, context: dict):
        """
        Inyecta contexto adicional en la memoria.
        """
        start_time = time()
        try:
            for k, v in context.items():
                self.memory.chat_memory.add_user_message(f"{k}: {v}")
            elapsed = time() - start_time
            self.trace.append(f"Contexto inyectado en {elapsed:.2f}s.")
            log_info(logger, f"[{timestamp_now()}] Contexto inyectado correctamente en {elapsed:.2f}s.")
        except Exception as e:
            log_error(logger, f"[{timestamp_now()}] Error al inyectar contexto: {e}")

    # ---------------------------------------------------------------------
    def trace_chain(self):
        """
        Devuelve el registro de eventos (trace).
        """
        return self.trace
