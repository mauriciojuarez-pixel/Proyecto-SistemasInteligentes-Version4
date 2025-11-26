# 7. limpieza_data_pipeline.py

Es el archivo **principal del pipeline**.  
Coordina los demás módulos y ejecuta todo el flujo del proceso de limpieza y análisis.

## Funciones / Métodos

| Función | Descripción |
|--------|-------------|
| `ejecutar_pipeline()` | Ejecuta todo el flujo: cargar → limpiar → detectar anomalías → analizar → exportar → generar visuales. |
| `preparar_directorios()` | Crea las carpetas necesarias (processed, reports, etc.). |
| `guardar_version_limpia(df_clean, ruta)` | Guarda el dataset limpio. |
| `generar_reportes(df_clean, ruta_reportes)` | Ejecuta `analysis_tools` para generar PNG, JSON y análisis. |

---