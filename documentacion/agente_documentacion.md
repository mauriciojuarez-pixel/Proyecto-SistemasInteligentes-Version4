# Documentación del Proyecto: Agente Autónomo con Gemma 2B IT

## 1. Resumen del Proyecto
Este proyecto implementa un **agente autónomo** capaz de analizar DataFrames, generar resúmenes interpretativos, sugerir visualizaciones y optimizar su propio comportamiento utilizando **Gemma 2B IT** (modelo GGUF) y **llama.cpp**.  
Incluye un **sistema de memoria por sesión**, gestión de prompts y logging detallado de todas las operaciones.

---

## 2. Estructura de Carpetas

agente/
├─ init.py
├─ config.py
├─ utils.py
├─ column_inspector.py
├─ agent_controller.py
├─ prompt_builder.py
├─ autonomous/
│ ├─ autonomous_agent.py
│ ├─ chain_manager.py
│ └─ memory_manager.py

                      ┌──────────────────────┐
                      │      config.py       │
                      └──────────┬───────────┘
                                 │
                     (rutas y directorios)
                                 │
       ┌───────────────┬─────────┼───────┐
       │               │                 │         
┌───────▼───────┐ ┌───▼─────────┐ ┌──────▼──────────┐
│ utils.py      │ │memory_manager │  prompt_builder │
└───────┬───────┘ └──────┬──────┘ └───────┬─────────┘
│ │ │
(funciones gen.) (persistencia) (generación prompts)
│ │ │
│ ┌────────▼────────┐   ┌───────▼──────────┐
│ │ autonomous/     │   │ autonomous_agent │
│ │ chain_manager   │   └────────┬─────────┘
│ └────────┬────────┘            │
│ (ejecución LLM, memoria)       │
│          │
└───────────────┬───────────────┬────────────┘
                │               │
┌─────────▼───────┐        ┌────▼────────────┐
│ agent_controller│        │ column_inspector│
└─────────────────┘        └─────────────────┘
           │                              │
(gestiona agentes por sesión) (roles de columnas)


---

## 3. Análisis de Módulos

### 3.1 `utils.py`
- Funciones auxiliares generales:
  - `make_json_serializable(obj)`: convierte objetos complejos (Timestamp, NaN, ndarray) a formatos JSON-friendly.
  - `save_dict_as_json(data, out_file)`: guarda diccionario como archivo JSON.
  - `load_json(file_path)`: carga JSON y devuelve diccionario.
  - `timestamp_now(fmt)`: devuelve timestamp actual como string.
  - `ensure_dir(path)`: crea carpeta si no existe.

---

### 3.2 `config.py`
- Define **rutas y parámetros globales**:
  - Directorios para modelos (`MODELS_DIR`), memoria (`MEMORY_DIR`), logs (`LOGS_DIR`) y reportes (`REPORTS_DIR`).
  - Variables de sesión por defecto (`DEFAULT_SESSION_ID`) y nombre de log (`DEFAULT_LOG_NAME`).
- Crea automáticamente los directorios si no existen.

---

### 3.3 `column_inspector.py`
- Función principal: `infer_column_roles(df, use_model=False, sample_size=5)`
  - Infiera el **rol de cada columna** automáticamente.
  - Si `use_model=True`, utiliza Gemma para inferir roles basándose en ejemplos.
  - Si falla, aplica heurísticas simples según nombres de columna y tipo de datos.
- Retorna un diccionario `{columna: rol_descriptivo}`.

---

### 3.4 `prompt_builder.py` - `BuilderPrompt`
- Clase que **construye prompts y ejecuta el modelo GGUF**:
  - `generate(prompt, max_tokens)`: ejecuta el modelo y devuelve texto.
  - `build_report_prompt(df, metadata, instruction)`: genera prompt para resumen ejecutivo.
  - `build_column_prompt(df, sample_size)`: genera prompt para inferir roles de columnas.
  - `_format_statistics(df)`, `_format_correlations(df)`, `_format_column_roles(df)`: formatean datos para prompts.
  - `execute_model(prompt, max_length)`: ejecuta el prompt directamente en Gemma.
- Logging detallado de construcción y ejecución de prompts.

---

### 3.5 `agent_controller.py` - `AgentController`
- Controlador central para **gestión de agentes por sesión**.
- Funciones principales:
  - `get_agent(session_id, model_path)`: obtiene o crea un agente.
  - `plan_goal(session_id, goal)`: genera un plan de acción.
  - `analyze_dataframe(session_id, df)`: envía DataFrame al agente y almacena resultados.
  - `generate_summary(session_id)`: genera resumen interpretativo.
  - `optimize_agent(session_id)`: ejecuta optimización interna.
  - `reset_agent(session_id)`: reinicia estado y memoria del agente.
- Integra logging de cada acción y manejo de errores.

---

### 3.6 `autonomous/autonomous_agent.py` - `AutonomousAgent`
- Representa un **agente autónomo individual**.
- Funciones principales:
  - `plan_actions(goal)`: genera un plan de pasos.
  - `analyze_data(df)`: analiza un DataFrame y almacena resultados.
  - `generate_summary()`: produce un resumen interpretativo.
  - `self_optimize()`: placeholder para optimización interna.
  - `reset()`: limpia memoria y estado.
- Integra:
  - `ChainManager`: para ejecución de prompts y LLM.
  - `MemoryManager`: para guardar y recuperar contexto entre sesiones.
- Logging: registra cada acción relevante y errores.

---

### 3.7 `autonomous/chain_manager.py` - `ChainManager`
- Administra prompts y ejecución del modelo GGUF.
- Funciones principales:
  - `build_prompt(df, metadata, instruction, use_column_inspector)`: genera prompt profesional.
  - `execute_prompt(prompt_text, max_tokens)`: ejecuta prompt con Gemma.
  - `execute_chain(df, metadata, instruction, use_column_inspector, max_tokens)`: genera y ejecuta cadena completa.
  - `inject_context(context)`: añade contexto adicional a la memoria.
  - `trace_chain()`: devuelve historial de ejecución.
- Logging de tiempos y errores de ejecución.

---

### 3.8 `autonomous/memory_manager.py` - `MemoryManager`
- Maneja **memoria persistente por sesión**.
- Funciones principales:
  - `store_context(session_id, context)`: almacena datos en memoria.
  - `recall_context(session_id)`: recupera contexto.
  - `clear_memory(session_id)`: limpia memoria de sesión.
  - `update_context(session_id, key, value)`: actualiza un valor específico.
  - `get_context_value(session_id, key)`: obtiene valor de contexto.
- Logging de cada operación sobre la memoria.

---

### 3.9 `__init__.py`
- Importa módulos centrales:
  - `config`, `utils`, `column_inspector`, `agent_controller`, `autonomous_agent`, `chain_manager`, `memory_manager`.
- Facilita el acceso global a todas las funcionalidades del paquete `agente`.

---
