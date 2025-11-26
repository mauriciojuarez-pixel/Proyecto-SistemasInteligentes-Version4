evaluacion_metricas/
│
├── __init__.py
├─ agent_metrics.py        # Métricas de desempeño del agente IA
├─ metrics_logger.py       # Clase para registrar métricas en JSON/CSV
├─ metrics_manager.py      # Gestor central de métricas de todo el pipeline
├─ report_metrics.py       # Métricas de desempeño de reportes PDF
└─ utils.py                # Funciones auxiliares (directorios, conversión JSON/CSV, porcentajes)


## 4.1 evaluacion_metricas/agent_metrics.py

Proporciona herramientas para evaluar resúmenes generados por agentes autónomos en términos de cobertura, relevancia y tiempo de generación.

### Clase `AgentMetrics`

| Método | Descripción |
|--------|-------------|
| `coverage_insights(columns_mentioned: List[str], total_columns: List[str]) -> float` | Calcula el porcentaje de columnas del DataFrame mencionadas en el resumen. Retorna un float redondeado al 2do decimal. |
| `summary_length_ok(summary: str, min_words: int = 50, max_words: int = 500) -> bool` | Verifica si el resumen cumple con un rango de palabras definido. Retorna True si está dentro del rango. |
| `generation_time(start_time: float, end_time: float) -> float` | Calcula el tiempo total de generación del resumen en segundos. Lanza error si `start_time > end_time`. |
| `relevance_score(key_insights: List[str], expected_insights: List[str]) -> float` | Calcula el porcentaje de insights clave presentes en el resumen comparado con los esperados. Retorna un float redondeado al 2do decimal. |

## 4.2 evaluacion_metricas/metrics_logger.py

Proporciona herramientas para registrar métricas de desempeño en archivos JSON o CSV, con soporte para agregar entradas nuevas sin sobrescribir las existentes.

### Clase `MetricsLogger`

| Método | Descripción |
|--------|-------------|
| `__init__(self, log_dir: str = "data/outputs/metrics/")` | Inicializa el logger de métricas. Crea el directorio de logs si no existe. |
| `log_metrics(self, metrics: dict, filename: str = None, as_csv: bool = False)` | Guarda las métricas proporcionadas en un archivo JSON o CSV. Si no se proporciona `filename`, se genera uno con timestamp. Retorna la ruta del archivo guardado. |
| `append_metrics(self, metrics: dict, filename: str)` | Agrega métricas a un archivo JSON existente sin sobrescribir datos previos. Cada entrada se almacena con una key única basada en timestamp. Retorna la ruta del archivo actualizado. |


## 4.3 evaluacion_metricas/metrics_manager.py

Gestor central de métricas para todo el pipeline, incluyendo datasets, agente IA y reportes PDF. Permite medir duración, calidad y desempeño integral del sistema.

### Clase `MetricsManager`

| Método | Descripción |
|--------|-------------|
| `__init__(self, output_dir: Path)` | Inicializa el gestor de métricas y crea el directorio de salida si no existe. Prepara la estructura interna para datasets, agente y reportes. |
| `mark_start(self)` | Marca el inicio del pipeline registrando timestamp y tiempo inicial para cálculo de duración. |
| `mark_end(self)` | Marca el final del pipeline registrando timestamp y duración total en segundos. |
| `add_dataset_metrics(self, dataset_name: str, df_raw: pd.DataFrame, df_processed: pd.DataFrame, quality_score: float)` | Agrega métricas de un dataset procesado, incluyendo número de filas, columnas y score de calidad. |
| `add_agent_metrics(self, session_id: str, plan: str, analysis: dict, summary: str, optimization: dict)` | Registra métricas del agente IA: longitud del plan, llaves del análisis, longitud del resumen y llaves de optimización. |
| `add_report_metrics(self, pdf_path: str, df: pd.DataFrame, summary: str, num_charts: int = 0)` | Guarda métricas del reporte PDF: ruta, número de filas/columnas, longitud del resumen y cantidad de gráficos generados. |
| `save_metrics(self)` | Guarda todas las métricas acumuladas en un archivo JSON con timestamp. Retorna la ruta del archivo guardado. |
| `start_timer(self)` | Alias de `mark_start()`. |
| `end_timer(self)` | Alias de `mark_end()`. |


## 4.4 evaluacion_metricas/report_metrics.py

Proporciona herramientas para evaluar métricas de desempeño de los reportes PDF generados, incluyendo cobertura de análisis, gráficos y tiempo de generación.

### Clase `ReportMetrics`

| Método | Descripción |
|--------|-------------|
| `coverage_analysis(columns_analyzed: List[str], total_columns: List[str]) -> float` | Calcula el porcentaje de columnas del dataset efectivamente analizadas en el reporte. Retorna un float redondeado al 2do decimal. |
| `charts_completeness(generated_charts: List[str], expected_charts: List[str]) -> float` | Calcula el porcentaje de gráficos generados respecto a los esperados. Retorna un float redondeado al 2do decimal. |
| `report_generation_time(start_time: float, end_time: float) -> float` | Calcula el tiempo total de generación del reporte en segundos. Lanza error si `start_time > end_time`. |
| `completeness_score(coverage: float, chart_score: float) -> float` | Calcula un score agregado de completitud del reporte combinando cobertura y gráficos. Retorna un float redondeado al 2do decimal. |


## 4.5 evaluacion_metricas/utils.py

Proporciona funciones auxiliares para la gestión de métricas, incluyendo creación de directorios, guardado seguro y manejo de porcentajes.

### Clase `Utils`

| Método | Descripción |
|--------|-------------|
| `ensure_dir(path: str)` | Crea la carpeta especificada si no existe. |
| `safe_percentage(value: float) -> float` | Asegura que un valor de porcentaje esté entre 0 y 100, redondeado a 2 decimales. |
| `dict_to_json(data: Dict[str, Any], path: str)` | Guarda un diccionario como archivo JSON en la ruta indicada, creando directorios si es necesario. |
| `dict_to_csv(data: Dict[str, Any], path: str)` | Guarda un diccionario como archivo CSV en la ruta indicada, creando directorios si es necesario. |
