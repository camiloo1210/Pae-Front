import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Configuración de la página (El "shadcn" de Streamlit)
st.set_page_config(page_title="PAE - IA Adopciones", page_icon="🐾", layout="centered")

# 2. Cargar los modelos entrenados
@st.cache_resource
def load_models():
    ct = joblib.load('preprocesador_pae.pkl')
    modelo = joblib.load('modelo_pae.pkl')
    return ct, modelo

ct, modelo = load_models()

# 3. Interfaz de Usuario (UI)
st.title("🐾 Simulador de Adopciones PAE")
st.markdown("Ingresa las características del animal rescatado para predecir su tiempo estimado de estadía en el refugio mediante **Inteligencia Artificial**.")

with st.form("formulario_mascota"):
    col1, col2 = st.columns(2)
    
    with col1:
        especie = st.selectbox("Especie", ["Perro", "Gato"])
        tamano = st.selectbox("Tamaño", ["Pequeño", "Mediano", "Grande"])
        sociabilidad = st.selectbox("Nivel de Sociabilidad", ["Alto", "Medio", "Bajo"])
        peso = st.number_input("Peso (Kg)", min_value=0.5, value=10.0, step=0.5)
        
    with col2:
        salud = st.selectbox("Estado de Salud", ["Excelente", "Bueno", "Regular", "En Tratamiento"])
        esterilizado = st.selectbox("¿Esterilizado?", ["Si", "No"])
        edad = st.number_input("Edad (Meses)", min_value=1, value=12)
        publicaciones = st.number_input("Campañas/Publicaciones", min_value=0, value=3)
        interacciones = st.number_input("Interacciones Esperadas", min_value=10, value=200)

    # Botón de envío
    submit = st.form_submit_button("🔮 Calcular Tiempo de Estadía", type="primary")

# 4. Lógica de Predicción
if submit:
    # Crear un DataFrame con los datos que ingresó el usuario
    datos_usuario = pd.DataFrame({
        'Especie': [especie],
        'Edad_Meses': [edad],
        'Peso_Kg': [peso],
        'Tamano': [tamano],
        'Estado_Salud': [salud],
        'Nivel_Sociabilidad': [sociabilidad],
        'Esterilizado': [esterilizado],
        'Publicaciones': [publicaciones],
        'Interacciones_RRSS': [interacciones]
    })
    
    # Preprocesar (One-Hot Encoding) y Predecir
    datos_procesados = ct.transform(datos_usuario)
    prediccion = modelo.predict(datos_procesados)[0]
    
    # Mostrar el resultado con alertas operacionales
    st.divider()
    st.subheader("Resultados de la Predicción")
    st.metric(label="Tiempo Estimado de Refugio", value=f"{int(prediccion)} días")
    
    if prediccion > 45:
        st.error("⚠️ **Alerta Operacional:** Este animal es un caso de larga estadía. Se recomienda activar protocolo de marketing intensivo o buscar hogar temporal (foster) desde hoy.")
    elif prediccion < 15:
        st.success("✅ **Tránsito Rápido:** Alta probabilidad de adopción temprana. Preparar documentación de salida.")
    else:
        st.warning("⏳ **Estadía Regular:** Planificar logística normal de mantenimiento.")