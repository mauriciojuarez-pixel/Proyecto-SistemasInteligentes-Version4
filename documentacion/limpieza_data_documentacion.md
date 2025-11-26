Practicamente la creacion de framework


# Documentación del Módulo `limpieza_data/`

Este documento describe la arquitectura y las funciones principales de cada archivo `.py` dentro del módulo **`limpieza_data/`**, siguiendo un estilo claro y profesional.

---

# 1. config.py

Proporciona la configuración principal del proyecto `limpieza_data`.  
Define rutas de datasets y el nombre del logger global.

## Variables / Configuración

| Variable | Descripción |
|----------|-------------|
| `BASE_DIR` | Directorio base del proyecto, calculado automáticamente a partir de la ubicación del archivo. |
| `RAW_PATH` | Ruta donde se almacenan los datasets sin procesar (`data/datasets/raw`). Se crea si no existe. |
| `PROCESSED_PATH` | Ruta donde se guardan los datasets procesados (`data/datasets/processed`). Se crea si no existe. |
| `LOG_NAME` | Nombre del logger global utilizado en los módulos de `limpieza_data`. |


# 2. logger.py

Proporciona funciones para inicializar y usar logging en el proyecto `limpieza_data`.  
Incluye configuración de archivos de log diarios y helpers para distintos niveles de registro.

## Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `init_logger(name: str = LOG_NAME, log_file: Path = DEFAULT_LOG_FILE, level=logging.INFO)` | Inicializa un logger con nombre y archivo específicos. Configura salida a consola y a archivo. Retorna objeto logger. |
| `log_info(logger_obj, msg: str)` | Registra un mensaje de nivel INFO usando el logger dado. |
| `log_warning(logger_obj, msg: str)` | Registra un mensaje de nivel WARNING usando el logger dado. |
| `log_error(logger_obj, msg: str)` | Registra un mensaje de nivel ERROR usando el logger dado. |
| `log_debug(logger_obj, msg: str)` | Registra un mensaje de nivel DEBUG usando el logger dado. |



# 3. file_loader.py

Proporciona funciones para carga y guardado de datasets.  
Incluye lectura de CSV y Excel, guardado de archivos procesados y carga masiva de CSV desde la carpeta RAW.

## Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `load_csv(path: Path, encodings=("utf-8", "latin-1", "ISO-8859-1")) -> pd.DataFrame` | Carga un archivo CSV probando varios encodings. Registra la operación en el logger y lanza errores si no se puede leer. |
| `load_excel(path: Path, sheet_name=0) -> pd.DataFrame` | Carga un archivo Excel de la hoja indicada. Registra errores si el archivo no existe o falla la lectura. |
| `save_processed(df: pd.DataFrame, filename: str) -> Path` | Guarda un DataFrame procesado en la carpeta PROCESSED_PATH, automáticamente como CSV o Excel según extensión. |
| `load_all_raw_csv() -> Dict[str, pd.DataFrame]` | Carga todos los archivos CSV desde la carpeta RAW_PATH y retorna un diccionario `{nombre_archivo: DataFrame}`. |



# 4. data_cleaner.py

Proporciona funciones para limpieza y normalización de datasets.  
Incluye normalización de nombres de columnas, eliminación de duplicados, llenado de valores nulos, conversión de tipos y estandarización de fechas.

## Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `normalize_columns(df: pd.DataFrame) -> pd.DataFrame` | Normaliza nombres de columnas a minúsculas, sin espacios y reemplazando caracteres especiales. |
| `remove_duplicates(df: pd.DataFrame) -> pd.DataFrame` | Elimina filas duplicadas y retorna un DataFrame limpio. |
| `fill_nulls(df: pd.DataFrame, strategy: str = "mean", fill_value=None) -> pd.DataFrame` | Rellena valores nulos usando la estrategia indicada (`mean`, `median`, `constant`) o un valor fijo. |
| `convert_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame` | Convierte columnas a tipos específicos según un diccionario `{columna: tipo}`. |
| `standardize_dates(df: pd.DataFrame, date_cols: list, fmt: str = None) -> pd.DataFrame` | Convierte y estandariza columnas de fecha, probando varios formatos comunes; opcionalmente aplica formato `fmt`. |
| `clean_data(df)` | Pipeline de limpieza que aplica: normalización de columnas, eliminación de duplicados, llenado de nulos y estandarización de fechas (columna `fecha`). |



# 5. anomaly_detection.py

Proporciona funciones para detección y manejo de anomalías en datasets.  
Incluye detección de outliers, eliminación de anomalías, etiquetado de datos ruidosos y cálculo de calidad de datos.

## Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `detect_outliers(df: pd.DataFrame, method: str = "zscore", threshold: float = 3.0) -> pd.DataFrame` | Detecta outliers en columnas numéricas usando z-score o IQR y agrega columna `is_outlier`. |
| `remove_anomalies(df: pd.DataFrame) -> pd.DataFrame` | Elimina filas marcadas como outliers (`is_outlier=True`) y retorna dataframe limpio. |
| `flag_noisy_data(df: pd.DataFrame, noise_thresh: float = 2.5) -> pd.DataFrame` | Calcula un `noisy_score` promedio y marca filas ruidosas (`is_noisy=True`). |
| `score_data_quality(df: pd.DataFrame) -> float` | Calcula un score de calidad considerando proporción de nulos y outliers; retorna valor entre 0 y 1. |



# 6. analysis_tools.py

Proporciona funciones para análisis estadístico y de correlaciones en datasets.  
Incluye cálculo de correlaciones, detección de multicolinealidad, generación de histogramas, exportación de resúmenes a JSON y pipeline de análisis completo.

## Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `compute_correlations(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame` | Calcula la matriz de correlación de un DataFrame usando el método indicado (`pearson`, `kendall`, `spearman`) y registra la operación en el logger. |
| `detect_multicollinearity(df: pd.DataFrame, threshold: float = 0.9) -> list` | Identifica pares de columnas numéricas con alta correlación (> threshold) y retorna una lista de tuplas `(col1, col2, valor_correlacion)`. |
| `visualize_correlation_matrix(corr_matrix: pd.DataFrame, out_file: str)` | Genera un heatmap de la matriz de correlación y lo guarda como imagen. Maneja matrices vacías o con pocas columnas numéricas. |
| `generate_histograms(df: pd.DataFrame, out_dir: str)` | Genera histogramas para todas las columnas numéricas del DataFrame y los guarda en la carpeta indicada. |
| `_make_json_serializable(obj)` | Convierte tipos no serializables (Timestamp, datetime, NaN, ndarray, sets, etc.) a formatos compatibles con JSON. |
| `summary_to_json(summary_df: pd.DataFrame, out_file: str)` | Exporta un DataFrame como JSON, convirtiendo cualquier tipo no serializable a una representación JSON-friendly. |
| `compute_descriptive_stats(df: pd.DataFrame) -> dict` | Retorna estadísticas descriptivas (`mean`, `std`, `min`, `max`) de las columnas numéricas del DataFrame. |
| `full_analysis_pipeline(df: pd.DataFrame, report_dir: str) -> dict` | Ejecuta un análisis completo del DataFrame, incluyendo correlaciones, estadísticas descriptivas y multicolinealidad, y guarda un resumen JSON en el directorio indicado. |
| `describe_dataset(df: pd.DataFrame)` | Genera un resumen rápido con estadísticas descriptivas, correlaciones y multicolinealidad del DataFrame. |



# Estructura Completa del Módulo

limpieza_data/
│
├── config.py
├── logger.py
├── file_loader.py
├── data_cleaner.py
├── anomaly_detection.py
├── analysis_tools.py
└── __init__.py


                ┌──────────────────────┐
                │      config.py       │
                └──────────┬───────────┘
                           │
                 (rutas globales)
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌─────────────┐   ┌────────────────┐  ┌──────────────────┐
│ logger.py   │   │ file_loader.py │  │ data_cleaner.py  │
└──────┬──────┘   └───────┬────────┘  └──────────┬────────┘
       │                  │                      │
       │ (logs)           │ (IO archivos)        │ (limpieza)
       │                  │                      │
       │         ┌────────▼────────┐     ┌───────▼─────────┐
       │         │ anomaly_detection│     │ analysis_tools  │
       │         └────────┬─────────┘     └────────┬────────┘
       │                  │                       │
       │          (detección outliers)  (correlación, stats, JSON)
       │                  │                       │
       └──────────────────┴───────────────────────┘
                      (pipeline integrado)
