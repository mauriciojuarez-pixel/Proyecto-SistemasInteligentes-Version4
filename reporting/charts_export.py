# reporting/charts_export.py
from pathlib import Path
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

class ChartExporter:

    def __init__(self, out_dir="generado/charts_export/"):
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)

    # ---------------------------------------------------------
    # Exporta TODOS los gráficos del dataset
    # ---------------------------------------------------------
    def export_all(self, df: pd.DataFrame, output_dir: str = None):
        if output_dir:
            self.out_dir = Path(output_dir)
            self.out_dir.mkdir(parents=True, exist_ok=True)

        charts = []

        charts.extend(self.generate_histograms(df))
        charts.append(self.generate_correlation_heatmap(df))
        charts.extend(self.generate_boxplots(df))

        return charts

    # ---------------------------------------------------------
    # Histogramas
    # ---------------------------------------------------------
    def generate_histograms(self, df: pd.DataFrame) -> list:
        paths = []
        numeric_cols = df.select_dtypes(include="number").columns

        for col in numeric_cols:
            filepath = os.path.join(self.out_dir, f"hist_{col}.png")

            plt.figure(figsize=(6, 4))
            plt.hist(df[col].dropna(), bins=20)
            plt.title(f"Histograma: {col}")
            plt.xlabel(col)
            plt.ylabel("Frecuencia")
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()

            paths.append(filepath)

        return paths

    # ---------------------------------------------------------
    # Heatmap de correlación
    # ---------------------------------------------------------
    def generate_correlation_heatmap(self, df: pd.DataFrame) -> str:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import os

        numeric_df = df.select_dtypes(include="number")
        filepath = os.path.join(self.out_dir, "correlation_heatmap.png")

        # Protección contra matrices vacías o con <2 columnas numéricas
        if numeric_df.shape[1] < 2:
            # Crear imagen informativa
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.text(0.5, 0.5,
                    "No hay suficientes columnas numéricas\npara generar heatmap",
                    ha="center", va="center")
            ax.axis("off")
            fig.savefig(filepath, bbox_inches="tight")
            plt.close(fig)
            return filepath

        # Matriz de correlación válida
        corr = numeric_df.corr()

        try:
            plt.figure(figsize=(8, 6))
            sns.heatmap(corr, annot=False, cmap="viridis")
            plt.title("Matriz de Correlación")
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()
        except Exception as e:
            # Fallback: imagen informativa si algo falla
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.text(0.5, 0.5, f"Error generando heatmap:\n{e}", ha="center", va="center")
            ax.axis("off")
            fig.savefig(filepath, bbox_inches="tight")
            plt.close()

        return filepath


    # ---------------------------------------------------------
    # Boxplots por columna
    # ---------------------------------------------------------
    def generate_boxplots(self, df: pd.DataFrame) -> list:
        paths = []
        numeric_cols = df.select_dtypes(include="number").columns

        for col in numeric_cols:
            filepath = os.path.join(self.out_dir, f"box_{col}.png")

            plt.figure(figsize=(6, 4))
            plt.boxplot(df[col].dropna())
            plt.title(f"Boxplot: {col}")
            plt.xlabel(col)
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()

            paths.append(filepath)

        return paths
