## 1. scripts/verify_requirements.py

Script para verificar que todos los paquetes listados en `requirements.txt` estén instalados.  
Puede limpiar el archivo de requirements de BOM, caracteres nulos y líneas corruptas, y opcionalmente instalar paquetes faltantes.

### Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `read_requirements(file_path: Path)` | Lee un archivo `requirements.txt` limpiando BOM, UTF-16, caracteres nulos y líneas corruptas. Retorna una lista de paquetes listos para instalar (`["pandas==1.5.3", "numpy==1.26.0", ...]`). |
| `check_package(pkg: str) -> bool` | Verifica si un paquete está instalado. Convierte nombres con guiones a guion bajo para importación segura. Retorna `True` si está instalado, `False` si falta. |
| `install_package(pkg: str)` | Instala un paquete usando `pip` desde el entorno de Python actual. |
| `log(message: str)` | Escribe un mensaje en el log (`data/outputs/logs/verify_requirements.log`) y lo imprime en consola. |
| `verify_requirements(auto_install=False)` | Verifica todos los paquetes del `requirements.txt`. Si `auto_install=True`, intenta instalar los que faltan automáticamente y registra los resultados en log. |

### Uso
python scripts/verify_requirements.py


## 2. scripts/update_model.py

Script para descargar o actualizar el modelo base **Gemma 2B IT** desde Hugging Face,  
y preparar las carpetas para fine-tuning y checkpoints.  

Se asegura que existan las rutas necesarias y usa el token de Hugging Face definido en `.env`.

### Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `log(message: str)` | Registra mensajes en consola y en el log `data/outputs/logs/update_model.log` con timestamp. |
| `ensure_directories()` | Crea/verifica los directorios `MODELS_DIR`, `FINETUNED_DIR` y `CHECKPOINTS_DIR`. |
| `clone_or_update_model()` | Descarga el modelo base `google/gemma-2b-it` desde Hugging Face usando `snapshot_download` y el token. |
| `prepare_finetune_folder()` | Crea/verifica las carpetas para fine-tuning (`FINETUNED_DIR`) y checkpoints (`CHECKPOINTS_DIR`). |
| `update_model()` | Función principal que llama a todas las anteriores para realizar la actualización completa del modelo. |

### Variables importantes

| Variable | Descripción |
|----------|-------------|
| `HUGGINGFACE_TOKEN` | Token de Hugging Face cargado desde `.env`. Obligatorio para descargar el modelo. |
| `BASE_MODEL_DIR` | Carpeta donde se almacena el modelo base. |
| `FINETUNED_DIR` | Carpeta destinada a guardar el modelo fine-tuneado. |
| `CHECKPOINTS_DIR` | Carpeta para guardar checkpoints intermedios. |
| `LOG_FILE` | Ruta del log de actualización: `data/outputs/logs/update_model.log`. |

### Uso
python scripts/update_model.py


## 3. scripts/setup_env.py

Script para inicializar el entorno de trabajo del proyecto.  
Crea la estructura de carpetas necesaria y el archivo de control de versiones para el modelo fine-tuneado.

### Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `create_folder(path: Path)` | Crea una carpeta si no existe, mostrando un mensaje informativo. |
| `initialize_directories()` | Inicializa todas las carpetas del proyecto según el diccionario `FOLDERS`. |
| `initialize_version_file()` | Crea un archivo JSON de control de versiones (`version.json`) para el modelo fine-tuneado si no existe. |
| `initialize_environment()` | Función principal que llama a la inicialización de carpetas y del archivo de versiones. |

### Variables importantes

| Variable | Descripción |
|----------|-------------|
| `BASE_DIR` | Carpeta raíz del proyecto. |
| `DATA_DIR` | Carpeta `data` dentro del proyecto. |
| `DATASETS_DIR` | Carpeta donde se almacenan los datasets. |
| `MODELS_DIR` | Carpeta donde se almacenan los modelos. |
| `OUTPUTS_DIR` | Carpeta para resultados y reportes. |
| `FOLDERS` | Diccionario con las rutas específicas a crear: datasets, modelos, checkpoints, reportes, logs, métricas. |
| `VERSION_FILE` | Archivo `version.json` para controlar la versión actual y el historial de modelos fine-tuneados. |

### Uso
python scripts/setup_env.py

## 4. scripts/report_pipeline.py

Pipeline de generación de reportes PDF usando el sistema de reportes del proyecto.  
Integra `ReportManager`, `PDFGenerator`, `ChartExporter` y plantillas para generar un PDF final con todos los datasets procesados.

### Flujo principal

1. Carga todos los CSV procesados desde `data/datasets/processed`.  
2. Crea la carpeta de salida `data/outputs/final_reports`.  
3. Ejecuta `ReportManager` para generar el reporte PDF consolidado.  
4. Guarda el PDF final como `reporte_final.pdf`.

### Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `timestamp_now()` | Devuelve la fecha y hora actual en formato `YYYY-MM-DD HH:MM:SS`. Función auxiliar local. |
| `main()` | Función principal que ejecuta todo el pipeline: carga CSV, consolida datos, llama a ReportManager y genera el PDF. |

### Variables importantes

| Variable | Descripción |
|----------|-------------|
| `BASE_DIR` | Directorio raíz del proyecto. |
| `processed_dir` | Carpeta donde se encuentran los datasets procesados (`/data/datasets/processed`). |
| `files` | Lista de archivos CSV encontrados en `processed_dir`. |
| `df_list` | Lista de DataFrames cargados desde los CSV. |
| `df` | DataFrame consolidado de todos los CSV procesados. |
| `output_dir` | Carpeta de salida para reportes finales (`/data/outputs/final_reports`). |
| `pdf_path` | Ruta completa del PDF final (`reporte_final.pdf`). |
| `manager` | Instancia de `ReportManager` utilizada para generar el PDF. |

### Uso
python scripts/report_pipeline.py


## 5. scripts/limpieza_data_pipeline.py

Pipeline completo de limpieza y análisis de datos.  
Integra los módulos de `limpieza_data` para transformar datasets RAW en datasets procesados, generar estadísticas y reportes.

### Flujo principal

1. Carga todos los CSV desde `data/datasets/raw/` usando `load_all_raw_csv()`.  
2. Normaliza los nombres de columnas (`normalize_columns`).  
3. Elimina duplicados (`remove_duplicates`).  
4. Rellena valores nulos (`fill_nulls`).  
5. Detecta columnas de fecha y las estandariza (`standardize_dates`).  
6. Convierte tipos de columnas específicas (`convert_types`).  
7. Detecta y elimina outliers (`detect_outliers`, `remove_anomalies`).  
8. Calcula un score de calidad de los datos (`score_data_quality`).  
9. Guarda los datasets procesados en `data/datasets/processed/` (`save_processed`).  
10. Ejecuta análisis completo con estadísticas, correlaciones e histogramas (`full_analysis_pipeline`) y guarda los reportes en `data/outputs/reports/`.

### Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `detectar_columnas_fecha(df: pd.DataFrame) -> list` | Detecta columnas que parecen fechas usando formatos comunes y un muestreo de filas. Retorna lista de nombres de columnas de fecha. |
| `ejecutar_pipeline()` | Función principal del pipeline que ejecuta todas las etapas de limpieza, análisis y guardado de datasets. |

### Variables importantes

| Variable | Descripción |
|----------|-------------|
| `BASE_DIR` | Directorio raíz del proyecto. |
| `datasets` | Diccionario `{filename: DataFrame}` cargado desde RAW. |
| `df` | DataFrame actual que se procesa por archivo. |
| `cols_fecha` | Columnas detectadas como fechas en el DataFrame. |
| `out_path` | Ruta donde se guarda el CSV procesado. |
| `report_dir` | Carpeta donde se generan los reportes estadísticos y gráficos. |

### Uso
python scripts/limpieza_data_pipeline.py

## 6. scripts/agente_pipeline.py

Pipeline de ejecución de agentes autónomos para análisis de datos y generación de resúmenes.  
Integra `AgentController` para administrar agentes individuales, generar planes, análisis y resúmenes ejecutivos.

### Flujo principal

1. Crear un **controlador central** (`AgentController`).  
2. Leer todos los CSV procesados desde `data/datasets/processed/` y concatenarlos en un `DataFrame`.  
3. Crear o recuperar un agente con una sesión específica (`session_id`).  
4. Generar un **plan de acción** para un objetivo concreto (`plan_goal`).  
5. Analizar el `DataFrame` mediante el agente (`analyze_dataframe`).  
6. Generar un **resumen ejecutivo** de los datos (`generate_summary`).  
7. Optimizar los parámetros internos del agente (`optimize_agent`).  
8. Resetear la memoria y contexto del agente (`reset_agent`).  

### Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `main()` | Función principal que ejecuta todo el pipeline: carga datos, crea agente, genera plan, análisis, resumen, optimización y reset. |

### Variables importantes

| Variable | Descripción |
|----------|-------------|
| `controller` | Instancia de `AgentController` que gestiona los agentes y sus sesiones. |
| `all_files` | Lista de rutas de archivos CSV procesados. |
| `df` | `DataFrame` concatenado de todos los CSV procesados. |
| `session_id` | Identificador único de la sesión del agente. |
| `agent` | Instancia del agente autónomo correspondiente a la sesión. |
| `goal` | Objetivo que se le asigna al agente para generar el plan de acción. |
| `plan` | Plan de acción generado por el agente para el objetivo definido. |
| `analysis` | Resultado del análisis de los datos por el agente. |
| `summary` | Resumen ejecutivo generado por el agente. |
| `optimization` | Resultado de la optimización de parámetros internos del agente. |

### Uso

python scripts/agente_pipeline.py


## 7. scripts/full_system_pipeline.py

Pipeline completo de integración del sistema, combinando:

1. Limpieza y análisis de datos (`RAW` → `PROCESSED`)  
2. Ejecución de agente autónomo (plan, análisis, resumen, optimización)  
3. Generación de reportes PDF con `ReportManager`  

Se requieren las siguientes carpetas y módulos:
- `limpieza_data/`
- `agente/`
- `reporting/`

### Flujo principal

1. **Pipeline de limpieza y análisis**  
   - Carga todos los CSV de `data/datasets/raw/`.  
   - Normaliza columnas, elimina duplicados y rellena nulos.  
   - Detecta columnas de fechas y las estandariza.  
   - Convierte columnas ID a tipo entero (`Int64`).  
   - Detecta y elimina outliers/anomalías.  
   - Calcula score de calidad del dataset.  
   - Guarda datasets procesados en `data/datasets/processed/`.  
   - Ejecuta análisis estadístico y genera reportes intermedios en `data/outputs/reports/`.

2. **Pipeline del agente autónomo IA**  
   - Instancia `AgentController` y crea sesión `main_session`.  
   - Genera **plan de acción** para el análisis del dataset.  
   - Analiza los datos y genera un **resumen interpretativo**.  
   - Ejecuta **optimización** de parámetros internos del agente.

3. **Pipeline de reporte PDF**  
   - Crea carpeta de salida `data/outputs/final_reports`.  
   - Instancia `ReportManager` y genera PDF completo usando el resumen generado por el agente.  

4. **Finalización**  
   - Reset de la sesión del agente (`reset_agent`).  
   - Logging completo de eventos y errores.

### Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `detectar_columnas_fecha(df: pd.DataFrame) -> list` | Detecta columnas que parecen contener fechas usando formatos comunes y fallback seguro con `pd.to_datetime`. |
| `pipeline_limpieza()` | Ejecuta todo el pipeline de limpieza, análisis y guardado de datasets procesados. |
| `pipeline_agente(df: pd.DataFrame)` | Ejecuta el agente autónomo: plan, análisis, resumen y optimización. Retorna el controlador, sesión y resultados. |
| `pipeline_report(df: pd.DataFrame, controller, session_id, resumen_interpretativo)` | Genera un PDF final con `ReportManager` usando los datos procesados y el resumen del agente. |
| `main()` | Función principal que une todos los pipelines: limpieza, agente y reporte, y resetea la sesión al finalizar. |

### Variables importantes

| Variable | Descripción |
|----------|-------------|
| `BASE_DIR` | Directorio raíz del proyecto. |
| `logger` | Logger principal para tracking de eventos y errores. |
| `processed_dir` | Carpeta donde se guardan los CSV procesados. |
| `df` | `DataFrame` concatenado con todos los CSV procesados. |
| `controller` | Instancia de `AgentController`. |
| `session_id` | Identificador de sesión del agente. |
| `plan` | Plan de acción generado por el agente. |
| `analysis` | Resultado del análisis de los datos por el agente. |
| `summary` | Resumen interpretativo generado por el agente. |
| `optimization` | Resultado de la optimización interna del agente. |

### Uso
python scripts/full_system_pipeline.py


