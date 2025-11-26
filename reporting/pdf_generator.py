# reporting/pdf_generator.py

import re
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors


class PDFGenerator:
    """Genera el PDF completo del reporte."""

    # ============================================================
    # LIMPIEZA Y FORMATEO DEL TEXTO DEL AGENTE IA
    # ============================================================
    def _clean_text(self, text: str) -> str:
        """
        Limpia texto para evitar errores en ReportLab:
        - Escapa caracteres XML (<, >, &)
        - Elimina bloques de ```
        - Normaliza saltos de línea
        - Preserva viñetas (*, -, números)
        """
        if not text:
            return "Texto no disponible."

        # Escapar caracteres XML
        text = (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )

        # Eliminar bloques ``` de Markdown
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

        # Mantener viñetas
        text = re.sub(r"^\s*[\*\-]\s+", "• ", text, flags=re.MULTILINE)

        # Normalizar saltos múltiples
        text = re.sub(r"\n\s*\n+", "\n", text)

        return text.strip()

    # ============================================================
    def generate_pdf(self, output_path, content: dict, template=None):

        pdf = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )

        styles = getSampleStyleSheet()

        # Estilo para listado simple
        bullet_style = ParagraphStyle(
            "Bullets",
            parent=styles["BodyText"],
            leftIndent=12,
            spaceAfter=4
        )

        story = []

        # ============================================================
        # 1. TÍTULO
        # ============================================================
        story.append(Paragraph(
            f"<b>{content.get('title', 'Reporte Analítico')}</b>",
            styles["Title"]
        ))
        story.append(Spacer(1, 0.5 * cm))

        # ============================================================
        # 2. INTERPRETACIÓN DE IA
        # ============================================================
        story.append(Paragraph("<b>Interpretación del Modelo:</b>", styles["Heading2"]))
        story.append(Spacer(1, 0.2 * cm))

        raw_text = content.get("interpretation", "Interpretación no disponible.")
        clean_text = self._clean_text(raw_text)

        paragraphs = clean_text.split("\n")

        for p in paragraphs:
            txt = p.strip()
            if not txt:
                continue

            # Detectar viñetas y aplicar estilo especial
            if txt.startswith("• "):
                story.append(Paragraph(txt, bullet_style))
            else:
                story.append(Paragraph(txt, styles["BodyText"]))

            story.append(Spacer(1, 0.12 * cm))

        story.append(Spacer(1, 0.5 * cm))

        # ============================================================
        # 3. ANÁLISIS ESTADÍSTICO
        # ============================================================
        story.append(Paragraph("<b>Análisis del Dataset:</b>", styles["Heading2"]))
        story.append(Spacer(1, 0.2 * cm))

        analysis_dict = content.get("analysis", {})

        for key, value in analysis_dict.items():

            if isinstance(value, dict):
                story.append(Paragraph(f"<b>{key}:</b>", styles["BodyText"]))

                data = [[str(k), str(v)] for k, v in value.items()]
                table = Table(data, colWidths=[6 * cm, 8 * cm])

                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ]))

                story.append(table)
                story.append(Spacer(1, 0.3 * cm))

            else:
                story.append(Paragraph(f"<b>{key}:</b> {value}", styles["BodyText"]))
                story.append(Spacer(1, 0.15 * cm))

        story.append(Spacer(1, 0.5 * cm))

        # ============================================================
        # 4. GRÁFICOS
        # ============================================================
        story.append(Paragraph("<b>Visualizaciones:</b>", styles["Heading2"]))
        story.append(Spacer(1, 0.3 * cm))

        for chart_path in content.get("charts", []):
            try:
                story.append(Image(chart_path, width=14 * cm, height=10 * cm))
                story.append(Spacer(1, 0.8 * cm))
            except Exception:
                story.append(Paragraph(
                    f"No se pudo cargar la imagen: {chart_path}",
                    styles["BodyText"]
                ))
                story.append(Spacer(1, 0.3 * cm))

        # ============================================================
        # GENERAR PDF
        # ============================================================
        pdf.build(story)
