# agente/autonomous/memory_manager.py

import copy
import logging
from limpieza_data.logger import init_logger

logger = init_logger("MemoryManager")


class MemoryManager:
    """
    Gestor de memoria para agentes autónomos.
    Permite almacenar y recuperar contexto por sesión.
    """

    def __init__(self):
        # Memoria en formato {session_id: {key: value}}
        self._memory_store = {}
        logger.info("MemoryManager inicializado.")

    # ---------------------------------------------------------------------
    def store_context(self, session_id: str, context: dict):
        """
        Almacena contexto en memoria para una sesión específica.
        Los valores se combinan con el contexto existente.
        """
        if session_id not in self._memory_store:
            self._memory_store[session_id] = {}

        for k, v in context.items():
            self._memory_store[session_id][k] = copy.deepcopy(v)

        logger.info(f"Contexto almacenado en sesión '{session_id}': {list(context.keys())}")

    # ---------------------------------------------------------------------
    def recall_context(self, session_id: str) -> dict:
        """
        Recupera el contexto completo de una sesión.
        Retorna {} si la sesión no existe.
        """
        context = copy.deepcopy(self._memory_store.get(session_id, {}))
        logger.info(f"Contexto recuperado de sesión '{session_id}': {list(context.keys())}")
        return context

    # ---------------------------------------------------------------------
    def clear_memory(self, session_id: str):
        """
        Limpia todo el contexto de una sesión específica.
        """
        if session_id in self._memory_store:
            del self._memory_store[session_id]
            logger.info(f"Memoria de sesión '{session_id}' limpiada.")
        else:
            logger.warning(f"No se encontró memoria para limpiar en sesión '{session_id}'.")

    # ---------------------------------------------------------------------
    def update_context(self, session_id: str, key: str, value):
        """
        Actualiza o agrega un valor específico en el contexto de una sesión.
        """
        if session_id not in self._memory_store:
            self._memory_store[session_id] = {}

        self._memory_store[session_id][key] = copy.deepcopy(value)
        logger.info(f"Contexto actualizado en sesión '{session_id}': {key}")

    # ---------------------------------------------------------------------
    def get_context_value(self, session_id: str, key: str):
        """
        Devuelve un valor específico del contexto de una sesión.
        Retorna None si la clave no existe.
        """
        value = copy.deepcopy(self._memory_store.get(session_id, {}).get(key))
        logger.info(f"Valor recuperado para '{key}' en sesión '{session_id}': {type(value).__name__}")
        return value
