"""
Módulo: templates
Responsable de gestionar plantillas base utilizadas por el Report Manager.
Define estructuras reutilizables para títulos, secciones y formatos
de reportes en texto, HTML o markdown.
"""

from datetime import datetime


class ReportTemplate:
    """
    Contenedor de plantillas y funciones de construcción.
    Permite a ReportManager usar instancias de esta clase sin cambiar código.
    """

    # ===========================
    #  Plantillas base (MD)
    # ===========================
    BASIC_HEADER_MD = """# {title}
Generado: {timestamp}
Autor: {author}

---
"""

    BASIC_SECTION_MD = """
## {section_title}

{content}
"""

    BASIC_FOOTER_MD = """
---

Reporte generado automáticamente por el sistema.
"""

    BASIC_TABLE_MD = """
### {title}

| Campo | Valor |
|-------|--------|
{rows}
"""

    # ===========================
    #  Plantillas HTML
    # ===========================
    HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
<h1>{title}</h1>
<p><strong>Generado:</strong> {timestamp}</p>
<p><strong>Autor:</strong> {author}</p>
<hr>
{content}
</body>
</html>
"""

    # ===========================================================
    #  MÉTODOS (usados por el ReportManager o PDF generator)
    # ===========================================================

    def render_header(self, title: str, author: str = "Sistema") -> str:
        return self.BASIC_HEADER_MD.format(
            title=title,
            author=author,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    def render_section(self, title: str, content: str) -> str:
        return self.BASIC_SECTION_MD.format(
            section_title=title,
            content=content
        )

    def render_footer(self) -> str:
        return self.BASIC_FOOTER_MD

    def render_table(self, title: str, data: dict) -> str:
        rows = ""
        for key, value in data.items():
            rows += f"| {key} | {value} |\n"
        return self.BASIC_TABLE_MD.format(title=title, rows=rows)

    def render_html(self, title: str, content: str, author: str = "Sistema") -> str:
        return self.HTML_TEMPLATE.format(
            title=title,
            content=content,
            author=author,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    # ===========================
    #  Plantilla completa MD
    # ===========================
    def build_markdown_report(self, title: str, sections: list, author: str = "Sistema") -> str:
        md = self.render_header(title, author)
        for sec_title, sec_content in sections:
            md += self.render_section(sec_title, sec_content)
        md += self.render_footer()
        return md
