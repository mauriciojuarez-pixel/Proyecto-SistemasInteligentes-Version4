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

## 3.1 agente/agent_controller.py

Controlador central para gestionar agentes autónomos.  
Permite crear agentes por sesión, analizar datos, generar planes y resúmenes.

### Clase / Métodos

| Método | Descripción |
|--------|-------------|
| `AgentController()` | Inicializa el controlador, mantiene agentes por `session_id` y registro del último output. |
| `get_agent(session_id: str = "default_session", model_path: str = None) -> AutonomousAgent` | Obtiene un agente existente o crea uno nuevo si no existe para la sesión indicada. |
| `plan_goal(session_id: str, goal: str) -> str` | Solicita al agente generar un plan de acción para un objetivo. Guarda el resultado en `last_output`. |
| `analyze_dataframe(session_id: str, df: pd.DataFrame, instruction: str) -> str` | Envía un DataFrame al agente para análisis y almacenamiento. Guarda el análisis en `last_output`. |
| `generate_summary(session_id: str, instruction: str) -> str` | Solicita al agente generar un resumen interpretativo basado en el último análisis. Guarda el resultado en `last_output`. |
| `optimize_agent(session_id: str) -> str` | Ejecuta la optimización interna del agente. Guarda el resultado en `last_output`. |
| `reset_agent(session_id: str)` | Resetea el estado y memoria del agente para la sesión indicada. |

## 3.2 agente/column_inspector.py

Proporciona funciones para inferir automáticamente el rol de cada columna en un DataFrame.  
Puede usar heurísticas simples o invocar el modelo Gemma 2B IT para inferencia avanzada.

### Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `infer_column_roles(df: pd.DataFrame, use_model: bool = False, sample_size: int = 5) -> dict` | Infiera el rol de cada columna del DataFrame. Si `use_model=True`, consulta Gemma 2B IT con ejemplos; si falla, usa heurísticas basadas en nombres y tipos. Retorna un diccionario `{columna: rol_descriptivo}`. |

---
## 3.3 agente/config.py

Contiene configuraciones globales y rutas críticas para el agente autónomo.  
Define directorios de modelos, memoria, logs y reportes, así como parámetros por defecto.

### Variables / Constantes

| Variable | Descripción |
|----------|-------------|
| `BASE_DIR` | Directorio raíz del proyecto. |
| `MODELS_DIR` | Carpeta donde se almacenan los modelos del agente. |
| `GEMMA_2B_IT_PATH` | Ruta completa al modelo Gemma 2B IT preentrenado. |
| `MEMORY_DIR` | Carpeta para almacenar la memoria de los agentes. |
| `LOGS_DIR` | Carpeta para almacenar logs generados por los agentes. |
| `REPORTS_DIR` | Carpeta para guardar reportes generados. |
| `DEFAULT_SESSION_ID` | ID de sesión por defecto para agentes. |
| `DEFAULT_LOG_NAME` | Nombre de logger por defecto para el agente. |

> Al inicializar, se crean automáticamente los directorios `MEMORY_DIR`, `LOGS_DIR` y `REPORTS_DIR` si no existen.

## 3.4 agente/prompt_builder.py

Módulo responsable de generar prompts estructurados para el modelo Gemma 2B IT (GGUF) y ejecutar las inferencias con `llama.cpp`.  
Incluye funciones de análisis de columnas, estadísticas y correlaciones, así como formateo de metadata para prompts.

### Clase `BuilderPrompt`

#### Atributos principales

| Atributo | Descripción |
|----------|-------------|
| `model_path` | Ruta al modelo GGUF de Gemma 2B IT. |
| `model` | Instancia de `Llama` para ejecutar inferencias. |

#### Métodos principales

| Método | Función |
|--------|---------|
| `generate(prompt, max_tokens)` | Genera texto con Gemma usando un prompt dado. |
| `build_report_prompt(df, metadata, instruction, use_column_inspector)` | Construye prompt completo para análisis y resumen de un DataFrame, incluyendo estadísticas, roles de columnas y correlaciones. |
| `build_column_prompt(df, sample_size)` | Construye prompt para que Gemma infiera los roles de las columnas de un DataFrame. |
| `execute_model(prompt, max_length)` | Ejecuta el modelo con el prompt y devuelve la respuesta. |

#### Métodos internos de formateo

- `_format_metadata(metadata)` → Convierte metadata en texto legible.  
- `_format_column_roles(df, use_model, sample_size)` → Obtiene roles de columnas, usando heurísticas o Gemma.  
- `_format_statistics(df)` → Resume estadísticamente cada columna.  
- `_format_correlations(df)` → Lista correlaciones altas entre columnas numéricas.  
- `_generate_hash(text)` → Genera hash SHA1 para un texto (uso interno).  

> Los prompts generados incluyen una sección de información interna (`metadata`, `column_roles`, `statistics`, `correlations`) que no debe mostrarse en el resumen final según las instrucciones a Gemma.


## 3.5 agente/utils.py

Contiene funciones auxiliares para manejo de datos, serialización JSON, timestamps y creación de directorios. Estas utilidades facilitan la interacción del agente con datos y archivos de manera consistente.

### Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `make_json_serializable(obj)` | Convierte objetos no serializables (pandas Timestamp, Timedelta, numpy types, sets, arrays, NaT, etc.) a tipos compatibles con JSON. |
| `save_dict_as_json(data: dict, out_file: Path)` | Guarda un diccionario en un archivo JSON, asegurando que todos los valores sean serializables mediante `make_json_serializable`. |
| `load_json(file_path: Path) -> dict` | Carga un archivo JSON y devuelve un diccionario. Si el archivo no existe, retorna `{}`. |
| `timestamp_now(fmt: str = "%Y%m%d_%H%M%S") -> str` | Devuelve un string con el timestamp actual formateado según `fmt`. |
| `ensure_dir(path: Path)` | Crea la carpeta indicada si no existe, incluyendo todos sus directorios padres. |
 

 ## 3.6 agente/autonomous/autonomous_agent.py

Define la clase `AutonomousAgent`, un agente autónomo para análisis de datos, generación de resúmenes interpretativos y sugerencias de visualización. Utiliza `ChainManager` para ejecutar cadenas de análisis y `MemoryManager` para persistir contexto por sesión.

### Clase: `AutonomousAgent`

| Método | Descripción |
|--------|-------------|
| `__init__(session_id="default_session", model_path=None)` | Inicializa el agente, carga memoria y ChainManager, y prepara el contexto de la sesión. |
| `plan_actions(goal: str)` | Genera un plan de acción básico para un objetivo dado y lo almacena en memoria. |
| `analyze_data(df: pd.DataFrame, instruction="Analiza y resume los datos.")` | Analiza un DataFrame, genera estadísticas, sugerencias de visualización y un análisis interpretativo mediante ChainManager. Almacena resultados en memoria. |
| `_generate_visualization_suggestions(df: pd.DataFrame)` | Genera recomendaciones de visualización basadas en tipos de columnas y correlaciones. |
| `generate_summary(instruction="Genera un resumen interpretativo de los datos.")` | Genera un resumen interpretativo de los datos cargados usando ChainManager y lo almacena en memoria. |
| `execute(prompt: str)` | Ejecuta un prompt sobre los datos actuales. Funciona como alias universal para interacciones con el agente. |
| `get_visualization_suggestions()` | Retorna la lista de sugerencias de visualización generadas en el último análisis. |
| `decide_next_step()` | Determina el siguiente paso a seguir según el estado actual del análisis. |
| `self_optimize()` | Ejecuta la optimización interna del agente (simulada) y retorna resultado. |
| `reset()` | Limpia la memoria y reinicia todos los estados internos del agente. |

## 3.7 agente/autonomous/chain_manager.py

Administra la construcción de prompts y la ejecución del modelo GGUF (Gemma 2B IT) usando `BuilderPrompt` y `llama_cpp`. Mantiene un registro de tiempos, memoria de conversación y errores.

### Clase: `ChainManager`

| Método | Descripción |
|--------|-------------|
| `__init__(model_path=None)` | Inicializa el ChainManager, carga el modelo GGUF y prepara la memoria de conversación. |
| `build_prompt(df=None, metadata=None, instruction="Analiza y resume los datos.", use_column_inspector=True)` | Construye un prompt profesional usando `BuilderPrompt` y retorna un `PromptTemplate`. Registra tiempos de construcción. |
| `execute_prompt(prompt_text: str, max_tokens: int = 1024)` | Ejecuta directamente un prompt sobre el modelo GGUF. Guarda mensajes de usuario y respuesta en memoria de conversación. |
| `execute_chain(df=None, metadata=None, instruction="Analiza y resume los datos.", use_column_inspector=True, max_tokens=1024)` | Combina construcción y ejecución del prompt. Retorna el texto generado o un mensaje de error. |
| `inject_context(context: dict)` | Inyecta contexto adicional en la memoria de conversación, agregando cada par clave-valor como mensaje de usuario. |
| `trace_chain()` | Devuelve el registro de eventos (`trace`) de la cadena de prompts y ejecuciones. |


## 3.8 agente/autonomous/memory_manager.py

Gestor de memoria para agentes autónomos. Permite almacenar, recuperar, actualizar y limpiar contexto por sesión.

### Clase: `MemoryManager`

| Método | Descripción |
|--------|-------------|
| `__init__()` | Inicializa la memoria interna `_memory_store` como diccionario vacío. |
| `store_context(session_id: str, context: dict)` | Almacena o combina el contexto dado para una sesión específica. Los valores se copian profundamente. |
| `recall_context(session_id: str) -> dict` | Recupera todo el contexto de una sesión. Retorna un diccionario vacío si la sesión no existe. |
| `clear_memory(session_id: str)` | Limpia todo el contexto asociado a una sesión. |
| `update_context(session_id: str, key: str, value)` | Actualiza o agrega un valor específico en el contexto de una sesión. |
| `get_context_value(session_id: str, key: str)` | Devuelve un valor específico del contexto de una sesión. Retorna `None` si la clave no existe. |
