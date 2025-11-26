# Objetivos y Caso de Estudio

## Tema del Proyecto
Sistema que automatiza el trabajo de análisis y generación de reportes.  
El presente proyecto propone el desarrollo de un sistema que emplea agentes inteligentes para automatizar el análisis de archivos de datos en formato CSV o Excel y generar reportes completos en formato PDF. El sistema integra el modelo Gemma 2B IT, el cual interpreta los resultados del análisis y redacta conclusiones detalladas, complementadas con gráficos y métricas personalizadas.

## Caso de Estudio
Automatización inteligente del proceso de análisis y reporte de datos mediante agentes en Python.  
El proyecto se basa en la construcción de un agente autónomo utilizando el framework LangChain, capaz de planificar y ejecutar de manera independiente las tareas necesarias para cumplir un objetivo específico. El usuario únicamente debe proporcionar su archivo de datos (CSV o Excel), y el agente se encarga de todo el proceso:

- Limpieza y validación del dataset, eliminando ruido, duplicados y valores nulos.
- Análisis automatizado de la información.
- Generación de visualizaciones y métricas relevantes.
- Elaboración de un reporte en formato PDF con conclusiones interpretativas redactadas por el modelo Gemma 2B IT.

Además, el sistema permite que el desarrollador realice de forma manual un proceso de fine-tuning del modelo, suministrando nuevos datasets que serán utilizados para mejorar el desempeño del agente. De esta manera, el sistema no solo analiza, sino que aprende y mejora continuamente con nuevos datos.

## Objetivo Principal
Construir agentes mediante el framework LangChain – Caso de estudio: automatizar tareas en Python.  

Desarrollar un agente inteligente capaz de automatizar el análisis de datos y la generación de reportes, integrando el modelo Gemma 2B IT para producir resultados interpretativos.

## Objetivos Secundarios
- Aplicar técnicas de limpieza y validación de datos para garantizar la calidad de los análisis y del entrenamiento.  
- Definir y aplicar métricas ad hoc que evalúen el desempeño del modelo y la calidad de los reportes generados.  
- Mantener una arquitectura modular y escalable inspirada en el patrón MVC, que permita separar la capa visual, la lógica del agente y el procesamiento de datos.
