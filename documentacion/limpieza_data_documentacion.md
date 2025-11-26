Practicamente la creacion de framework


# Documentación del Módulo `limpieza_data/`

Este documento describe la arquitectura y las funciones principales de cada archivo `.py` dentro del módulo **`limpieza_data/`**, siguiendo un estilo claro y profesional.

---

# 1. config.py

Define la configuración central del módulo, incluyendo rutas principales del proyecto, constantes globales y creación automática de directorios para el pipeline de limpieza y análisis de datos.

## Funciones / Atributos

| Nombre | Descripción |
|--------|-------------|
| `BASE_DIR` | Directorio raíz del proyecto, calculado automáticamente usando `Path`. |
| `RAW_PATH` | Carpeta donde se almacenan los datasets **RAW** sin procesar. |
| `PROCESSED_PATH` | Carpeta donde se guardan los datasets **procesados** después de la limpieza. |
| `LOG_NAME` | Nombre del logger global utilizado por todos los módulos. |
| `RAW_PATH.mkdir()` | Garantiza que la carpeta RAW exista (la crea si no existe). |
| `PROCESSED_PATH.mkdir()` | Garantiza que la carpeta PROCESSED exista (la crea si no existe). |

# 2. logger.py

Gestiona la creación y configuración del logging del módulo `limpieza_data`.  
Permite registrar mensajes en consola y archivos, con timestamp y nivel de severidad.

## Funciones / Atributos

| Nombre / Función | Descripción |
|-----------------|-------------|
| `LOGS_DIR` | Carpeta donde se guardan los logs generados. Se crea automáticamente si no existe. |
| `DEFAULT_LOG_FILE` | Nombre y ruta por defecto del archivo de log, incluye la fecha actual. |
| `init_logger(name: str = LOG_NAME, log_file: Path = DEFAULT_LOG_FILE, level=logging.INFO)` | Inicializa un logger con consola y archivo, con formato estándar `[timestamp] [LEVEL] message`. |
| `logger` | Logger global inicializado con `init_logger()`. |
| `log_info(logger_obj, msg: str)` | Registra un mensaje de nivel INFO. |
| `log_warning(logger_obj, msg: str)` | Registra un mensaje de nivel WARNING. |
| `log_error(logger_obj, msg: str)` | Registra un mensaje de nivel ERROR. |
| `log_debug(logger_obj, msg: str)` | Registra un mensaje de nivel DEBUG. |


# 3. file_loader.py

Se encarga de la carga y guardado de datasets en CSV o Excel.  
Proporciona funciones para leer archivos RAW y guardar datasets procesados, con logging de eventos y errores.

## Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `load_csv(path: Path, encodings=("utf-8", "latin-1", "ISO-8859-1")) -> pd.DataFrame` | Carga un archivo CSV intentando múltiples encodings. Registra error si el archivo no existe o no puede leerse. |
| `load_excel(path: Path, sheet_name=0) -> pd.DataFrame` | Carga un archivo Excel, especificando la hoja (sheet_name). Registra error si el archivo no existe o falla la lectura. |
| `save_processed(df: pd.DataFrame, filename: str) -> Path` | Guarda un DataFrame procesado en la carpeta `PROCESSED_PATH`, como CSV o Excel según la extensión. |
| `load_all_raw_csv() -> Dict[str, pd.DataFrame]` | Carga todos los archivos CSV presentes en la carpeta RAW y devuelve un diccionario {nombre_archivo: DataFrame}. |


# 4. data_cleaner.py

Proporciona funciones para limpiar y transformar datasets.  
Incluye normalización de columnas, manejo de valores nulos, eliminación de duplicados, conversión de tipos y estandarización de fechas.

## Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `normalize_columns(df: pd.DataFrame) -> pd.DataFrame` | Normaliza los nombres de columnas a minúsculas, sin espacios y con guiones bajos. |
| `remove_duplicates(df: pd.DataFrame) -> pd.DataFrame` | Elimina filas duplicadas y registra la cantidad eliminada. |
| `fill_nulls(df: pd.DataFrame, strategy: str = "mean", fill_value=None) -> pd.DataFrame` | Rellena valores nulos usando estrategias: mean, median o constant. |
| `convert_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame` | Convierte tipos de columnas según un diccionario {columna: tipo}. |
| `standardize_dates(df: pd.DataFrame, date_cols: list, fmt=None) -> pd.DataFrame` | Convierte columnas de fecha a `datetime` y opcionalmente formatea a string con `fmt`. |


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

Proporciona herramientas de análisis de datos para el pipeline de limpieza.  
Incluye correlaciones, multicolinealidad, estadísticas descriptivas, histogramas y exportación a JSON.

## Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `compute_correlations(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame` | Calcula la matriz de correlación para columnas numéricas. |
| `detect_multicollinearity(df: pd.DataFrame, threshold: float = 0.9) -> list` | Detecta pares de columnas con alta correlación (> threshold). |
| `visualize_correlation_matrix(corr_matrix: pd.DataFrame, out_file: str)` | Genera y guarda un heatmap de la matriz de correlación. |
| `compute_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame` | Calcula estadísticas descriptivas (media, mediana, std, min, max, etc.). |
| `generate_histograms(df: pd.DataFrame, out_dir: str)` | Crea histogramas de todas las columnas numéricas y los guarda como PNG. |
| `_make_json_serializable(obj)` | Convierte objetos no serializables (datetime, Timestamp, numpy, sets, NA) a formatos compatibles con JSON. |
| `summary_to_json(summary_df: pd.DataFrame, out_file: str)` | Exporta un DataFrame a JSON, convirtiendo tipos no serializables automáticamente. |
| `full_analysis_pipeline(df: pd.DataFrame, report_dir: str) -> dict` | Ejecuta pipeline completo de análisis: correlaciones, multicolinealidad, estadísticas, histogramas y exportación JSON; retorna un diccionario con resultados. |


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
