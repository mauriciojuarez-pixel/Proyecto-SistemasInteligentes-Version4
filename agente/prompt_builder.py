# agente/prompt_builder.py

import hashlib
import pandas as pd
import json
from typing import Dict, Optional
from llama_cpp import Llama

# Funciones de limpieza_data
from limpieza_data.analysis_tools import compute_correlations
from limpieza_data.logger import init_logger  # Importamos el logger

# Importamos column_inspector para roles de columnas
from agente.column_inspector import infer_column_roles

# Inicializar logger
logger = init_logger(name="BuilderPrompt")


class BuilderPrompt:
    """
    Generador de prompts y ejecución con Gemma (GGUF) usando llama.cpp.
    """

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or (
            "data/models/gemma_2b_it_base/"
            "models--google--gemma-2b-it/"
            "snapshots/96988410cbdaeb8d5093d1ebdc5a8fb563e02bad/"
            "gemma-2b-it.gguf"
        )
        logger.info(f"Cargando modelo GGUF desde {self.model_path}")

        try:
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=8192,
                n_gpu_layers=-1,
                n_threads=8,
                temperature=0.0,
                verbose=False
            )
            logger.info("Modelo cargado correctamente.")
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {e}")
            raise

    # =========================================================
    # MÉTODO PRINCIPAL DE GENERACIÓN DE TEXTO
    # =========================================================
    def generate(self, prompt: str, max_tokens=1024) -> str:
        logger.info("Generando texto con Gemma...")
        try:
            response = self.model(
                prompt,
                max_tokens=max_tokens,
                stop=["</s>", "###"]
            )
            text = response["choices"][0]["text"].strip()
            logger.info("Texto generado correctamente.")
            return text
        except Exception as e:
            logger.error(f"Error en la generación de texto: {e}")
            return ""

    # =========================================================
    # FORMATTERS INTERNOS
    # =========================================================
    @staticmethod
    def _generate_hash(text: str) -> str:
        h = hashlib.sha1()
        h.update(text.encode("utf-8"))
        return h.hexdigest()

    @staticmethod
    def _format_metadata(metadata: Dict) -> str:
        if not metadata:
            return "No hay metadata adicional"
        return "\n".join([f"{k}: {v}" for k, v in metadata.items()])

    @staticmethod
    def _format_column_roles(df: pd.DataFrame, use_model: bool = False, sample_size: int = 5) -> str:
        """
        Formatea los roles de columnas usando column_inspector.
        """
        if not isinstance(df, pd.DataFrame):
            return ""
        roles = infer_column_roles(df, use_model=use_model, sample_size=sample_size)
        return "\n".join([f"- {col}: {role}" for col, role in roles.items()])

    @staticmethod
    def _format_statistics(df: pd.DataFrame) -> str:
        stats_lines = []
        for col in df.columns:
            try:
                if pd.api.types.is_numeric_dtype(df[col]):
                    mean = df[col].mean()
                    std = df[col].std()
                    min_val = df[col].min()
                    max_val = df[col].max()
                    mode_val = df[col].mode().iloc[0] if not df[col].mode().empty else "N/A"
                    stats_lines.append(f"{col}: mean={mean}, std={std}, min={min_val}, max={max_val}, mode={mode_val}")
                else:
                    unique_count = df[col].nunique()
                    top_val = df[col].mode().iloc[0] if not df[col].mode().empty else "N/A"
                    stats_lines.append(f"{col}: unique={unique_count}, top={top_val}")
            except Exception as e:
                stats_lines.append(f"{col}: error procesando ({e})")
        return "\n".join(stats_lines)

    @staticmethod
    def _format_correlations(df: pd.DataFrame) -> str:
        numeric_df = df.select_dtypes(include='number')
        if numeric_df.empty:
            return "No hay columnas numéricas para calcular correlaciones."
        corr_matrix = compute_correlations(numeric_df)
        top_corrs = []
        for col in corr_matrix.columns:
            high_corr = corr_matrix[col][
                (corr_matrix[col].abs() > 0.8) & (corr_matrix[col].abs() < 1.0)
            ]
            for related_col, value in high_corr.items():
                top_corrs.append(f"{col} ↔ {related_col}: {value:.2f}")
        return "\n".join(top_corrs) if top_corrs else "No hay correlaciones altas."

    # =========================================================
    # PROMPTS PÚBLICOS
    # =========================================================
    def build_report_prompt(
        self, df: pd.DataFrame, metadata: Optional[Dict] = None, instruction: str = "Analiza y resume los datos.",
        use_column_inspector: bool = False
    ) -> str:

        logger.info("Construyendo prompt para resumen ejecutivo...")
        metadata_text = self._format_metadata(metadata or {})
        columns_text = self._format_column_roles(df, use_model=use_column_inspector)
        stats_text = self._format_statistics(df)
        correlations_text = self._format_correlations(df)

        prompt = (
            f"{instruction}\n\n"
            "INSTRUCCIONES:\n"
            "- No muestres datos internos.\n"
            "- No repitas estadísticas, columnas ni metadatos.\n"
            "- No vuelvas a analizar los datos.\n"
            "- Solo escribe el resumen final.\n\n"
            "[INFORMACIÓN INTERNA — NO MOSTRAR]\n"
            f"{metadata_text}\n"
            f"{columns_text}\n"
            f"{stats_text}\n"
            f"{correlations_text}\n"
        )

        logger.info("Prompt construido correctamente.")
        return prompt

    def build_column_prompt(self, df: pd.DataFrame, sample_size: int = 5) -> str:
        logger.info("Construyendo prompt para inferir roles de columnas...")
        column_info_list = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            sample_values = df[col].dropna().head(sample_size).tolist()
            sample_values = [str(v) for v in sample_values]
            column_info_list.append({
                "column_name": col,
                "dtype": dtype,
                "sample_values": sample_values
            })
        column_info_json = json.dumps(column_info_list, indent=2, ensure_ascii=False)

        prompt = (
            "Eres Gemma 2B IT, especialista en estructuras de datos.\n"
            "Tu tarea es INFERIR el rol de cada columna basado en tipo de dato y ejemplos.\n\n"
            "INSTRUCCIONES:\n"
            "DEBES responder únicamente con un JSON válido.\n"
            f"[COLUMN_DATA]\n{column_info_json}\n\n"
            "RESPUESTA OBLIGATORIA (solo JSON):\n"
            "{\n"
            '  "column_name_1": "rol",\n'
            '  "column_name_2": "rol"\n'
            "}"
        )
        logger.info("Prompt de columnas construido correctamente.")
        return prompt
    
    def execute_model(self, prompt: str, max_length: int = 1024) -> str:
            """
            Ejecuta el modelo GGUF usando el prompt dado y devuelve la respuesta como texto.
            """
            try:
                response = self.model(
                    prompt,
                    max_tokens=max_length,
                    stop=["</s>", "###"]
                )
                return response["choices"][0]["text"].strip()
            except Exception as e:
                logger.error(f"Error ejecutando modelo en BuilderPrompt: {e}")
                return ""