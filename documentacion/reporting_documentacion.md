# 1. report_manager.py

Orquesta todo el proceso de generación de reportes.  
Coordina la limpieza del dataset, el análisis estadístico, la generación de gráficos, la interpretación generada por IA y finalmente la creación del PDF final.

## Funciones / Métodos

| Función | Descripción |
|--------|-------------|
| `build_full_report(df, session_id="default")` | Ejecuta todo el pipeline del reporte: limpieza, análisis, exportación de gráficos, interpretación con LLM y generación del PDF final. |
| `auto_name_report()` | Genera automáticamente el nombre del archivo PDF con timestamp. |
----
# 2. pdf_generator.py

Genera el archivo PDF final utilizando ReportLab.  
Ensambla títulos, secciones de texto, métricas analíticas y gráficos exportados como imágenes PNG.

## Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `generate_pdf(output_path, content: dict, template)` | Construye el PDF final usando la información generada por `report_manager`. Incluye título, interpretación del modelo, análisis estadístico y gráficos. |

## Detalles del Comportamiento

- Usa `SimpleDocTemplate` para crear el PDF con márgenes definidos.
- Inserta el título principal del reporte usando estilos por defecto o los definidos en `templates.py`.
- Renderiza:
  - Interpretación generada por el modelo LLM (Gemma).
  - Métricas del análisis estadístico (como texto).
  - Gráficos PNG exportados desde `charts_export.py`.
- Cada sección incluye espaciado consistente mediante `Spacer`.
-----

# 3. templates.py

Define los estilos, estructuras base y plantillas reutilizables para generar contenido de reportes.  
Proporciona funciones para construir encabezados, secciones, tablas y pies de página en formato Markdown o HTML.

## Funciones / Métodos

| Función | Descripción |
|---------|-------------|
| `render_header(title: str, author: str)` | Crea el encabezado del reporte con título y autor. |
| `render_section(title: str, content: str)` | Genera una sección con título y contenido formateado. |
| `render_table(title: str, data: dict)` | Construye una tabla Markdown a partir de un diccionario clave–valor. |
| `render_footer()` | Devuelve un pie de página estándar para el reporte. |
| `render_html(title: str, content: str, author: str)` | Genera estructura HTML básica para exportar contenido. |
| `build_markdown_report(title: str, sections: list, author: str)` | Ensambla un reporte Markdown completo combinando encabezado, secciones y pie. |



# 4. charts_export.py

Módulo encargado de generar y exportar todos los gráficos utilizados en el reporte final.  
Produce histogramas, mapas de calor y boxplots en formato PNG.

## Funciones / Métodos

| Función | Descripción |
|--------|-------------|
| `export_all(df: pd.DataFrame) -> list` | Ejecuta el pipeline completo de gráficos y retorna una lista con las rutas de las imágenes generadas. |
| `generate_histograms(df: pd.DataFrame) -> list` | Genera histogramas para todas las columnas numéricas y devuelve sus rutas PNG. |
| `generate_correlation_heatmap(df: pd.DataFrame) -> str` | Crea y guarda un mapa de calor de correlaciones, retornando la ruta del archivo PNG. |
| `generate_boxplots(df: pd.DataFrame) -> list` | Genera boxplots para todas las columnas numéricas y devuelve las rutas de los archivos PNG. |



# 5. __init__.py

Hace que el directorio sea un módulo importable.
Opcionalmente puede exponer funciones o clases principales.
