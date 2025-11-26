# 1. report_manager.py

Proporciona la clase `ReportManager` para orquestar la generación completa de reportes analíticos.  
Incluye limpieza de datos, análisis estadístico, generación de gráficos, integración con interpretación de IA y exportación a PDF.

## Clases / Métodos

| Clase / Método | Descripción |
|----------------|-------------|
| `ReportManager(reports_dir: str = "generado/reports/", controller=None)` | Inicializa el manager de reportes. Crea carpetas necesarias y carga componentes: `PDFGenerator`, `ChartExporter`, `ReportTemplate`, `AgentController` y `BuilderPrompt`. |
| `generate_full_report(df: pd.DataFrame, output_path: str = None, session_id="default")` | Orquesta la creación de un reporte completo, llamando internamente a `build_full_report`. |
| `build_full_report(df: pd.DataFrame, session_id="default", controller=None, resumen_interpretativo: str = None)` | Construye un reporte completo usando un DataFrame y un resumen interpretativo ya generado por IA. Aplica limpieza, análisis estadístico, gráficos y genera el PDF final. Retorna la ruta del PDF generado. |
| `auto_name_report()` | Genera un nombre automático para el PDF en formato `report_YYYYMMDD_HHMMSS.pdf`. |

# 2. pdf_generator.py

Proporciona la clase `PDFGenerator` para generar reportes en PDF.  
Incluye limpieza y formateo de texto, tablas de análisis, interpretación del modelo y exportación de gráficos.

## Clases / Métodos

| Clase / Método | Descripción |
|----------------|-------------|
| `PDFGenerator` | Clase principal para generar un PDF completo a partir de contenido estructurado. |
| `_clean_text(self, text: str) -> str` | Limpia texto de entrada para evitar errores en ReportLab: escapa caracteres XML, elimina bloques de Markdown, normaliza saltos de línea y preserva viñetas. |
| `generate_pdf(self, output_path, content: dict, template=None)` | Genera un PDF completo con título, interpretación del modelo, análisis estadístico y gráficos. `content` debe ser un diccionario con claves como `title`, `interpretation`, `analysis` y `charts`. |

# 3. templates.py

Proporciona la clase `ReportTemplate` para gestionar plantillas base utilizadas por el `ReportManager`.  
Incluye estructuras reutilizables para títulos, secciones y formatos de reportes en Markdown y HTML.

## Clases / Métodos

| Clase / Método | Descripción |
|----------------|-------------|
| `ReportTemplate` | Contenedor de plantillas y funciones de construcción. Permite a `ReportManager` usar instancias de esta clase sin cambiar código. |
| `render_header(title: str, author: str = "Sistema") -> str` | Genera el encabezado de un reporte en Markdown con título, autor y timestamp. |
| `render_section(title: str, content: str) -> str` | Genera una sección de reporte en Markdown con título y contenido. |
| `render_footer() -> str` | Retorna el pie de página estándar del reporte en Markdown. |
| `render_table(title: str, data: dict) -> str` | Genera una tabla en Markdown a partir de un diccionario `data`. |
| `render_html(title: str, content: str, author: str = "Sistema") -> str` | Genera un reporte completo en HTML usando plantilla base. |
| `build_markdown_report(title: str, sections: list, author: str = "Sistema") -> str` | Construye un reporte Markdown completo combinando encabezado, secciones y pie de página. |



# 4. charts_export.py

Proporciona la clase `ChartExporter` para generar y exportar gráficos de un dataset.  
Incluye histogramas, heatmap de correlación y boxplots por columna.

## Clases / Métodos

| Clase / Método | Descripción |
|----------------|-------------|
| `ChartExporter(out_dir="generado/charts_export/")` | Inicializa el exportador de gráficos. Crea automáticamente la carpeta de salida si no existe. |
| `export_all(df: pd.DataFrame, output_dir: str = None)` | Genera todos los gráficos del DataFrame: histogramas, heatmap de correlación y boxplots. Retorna lista de rutas de los archivos generados. |
| `generate_histograms(df: pd.DataFrame) -> list` | Genera histogramas para todas las columnas numéricas del DataFrame. Retorna lista de rutas de los archivos. |
| `generate_correlation_heatmap(df: pd.DataFrame) -> str` | Genera un heatmap de correlación para columnas numéricas. Maneja casos con pocas columnas o errores. Retorna ruta del archivo generado. |
| `generate_boxplots(df: pd.DataFrame) -> list` | Genera boxplots para todas las columnas numéricas del DataFrame. Retorna lista de rutas de los archivos generados. |



# 5. __init__.py

Hace que el directorio sea un módulo importable.
Opcionalmente puede exponer funciones o clases principales.
