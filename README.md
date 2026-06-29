# PAE · Predicción del Tiempo de Adopción mediante Regresión Lineal

Este proyecto tiene como objetivo desarrollar un modelo de regresión lineal que permita predecir el tiempo estimado de adopción de un animal en la fundación PAE (Protección Animal Ecuador). A través de esta herramienta, se busca optimizar la gestión de recursos, el espacio disponible y las estrategias de difusión de la fundación.

**Autores:** Camily Solorzano, Camilo Brazales

## Contexto y Problema

PAE es una fundación sin fines de lucro dedicada al rescate, rehabilitación y adopción de animales domésticos en situación de calle. Actualmente, la fundación maneja un flujo constante de ingreso y salida de animales, pero no cuenta con herramientas analíticas que le permitan anticipar el comportamiento del proceso de adopción. 

La ausencia de un sistema predictivo impide estimar el tiempo de adopción de cada animal, lo que dificulta la planificación de recursos, espacio y estrategias de difusión. El problema se ha intensificado desde la pandemia, generando la necesidad de priorizar a los ejemplares con mayor riesgo de permanencia prolongada.

## Variables del Proyecto

El modelo toma en cuenta las siguientes variables para determinar el tiempo estimado de permanencia en el refugio:

**Variables Cuantitativas:**
- Edad del animal
- Peso
- Tiempo en refugio (variable objetivo a predecir)
- Número de publicaciones realizadas
- Número de interacciones (likes, shares, etc.) en redes sociales
- Número de visitas recibidas
- Costos de mantenimiento

**Variables Cualitativas:**
- Especie (perro/gato)
- Raza
- Estado de salud
- Nivel de sociabilidad
- Esterilización (sí/no)
- Tamaño (pequeño/mediano/grande)

## ¿Por qué usamos un modelo de Regresión Lineal?

Se optó por desarrollar un modelo de Machine Learning supervisado basado en **Regresión Lineal** porque el objetivo principal del proyecto es predecir un valor numérico continuo: el **tiempo estimado (en días)** que un animal permanecerá en el refugio antes de ser adoptado. 

A diferencia de los modelos de clasificación (que agruparían a los animales en categorías amplias como probabilidad de adopción alta, media o baja), la regresión lineal nos proporciona una estimación de días más exacta. Esto nos permite entender de forma clara el peso e impacto que tiene cada variable independiente (edad, especie, nivel de sociabilidad, etc.) directamente sobre el tiempo de estadía, facilitando así una mejor toma de decisiones operativas y planificación precisa de recursos para casos críticos.

## ¿Cómo funciona el frontend y el modelo?

El proyecto incluye una aplicación interactiva construida en **Streamlit** (Python) que sirve como interfaz visual (frontend) para el modelo.

### Arquitectura Principal
- `Inicio.py`: Punto de entrada principal de la aplicación.
- `pages/1_Dashboard.py`: Panel visual para análisis de los datos históricos.
- `pages/2_Predictor.py`: Interfaz interactiva donde se ingresan las características de un animal para obtener su predicción de días de estadía mediante el modelo cargado.
- `entrenar.py`: Script utilizado para entrenar el modelo de Regresión Lineal con los datos históricos (`pae_adopciones_sintetico.csv`).
- `modelo_pae.pkl` y `preprocesador_pae.pkl`: Archivos que almacenan el modelo ya entrenado y los transformadores de datos. Al levantar la interfaz en Streamlit, el predictor carga estos archivos en memoria para realizar inferencias de forma inmediata sin tener que volver a entrenar.

### Cómo correr el proyecto

El proyecto está diseñado para ejecutarse localmente usando Python. 

1. Abre una terminal en la carpeta raíz del proyecto.
2. (Opcional) Si deseas reentrenar el modelo con los datos del CSV actual, ejecuta:
   ```powershell
   py entrenar.py
   ```
   *Esto generará y guardará nuevamente los archivos `.pkl`.*
3. Para ejecutar la interfaz (frontend), corre el siguiente comando:
   ```powershell
   py -m streamlit run Inicio.py
   ```
4. Se abrirá automáticamente una pestaña en tu navegador web con la aplicación en funcionamiento.
