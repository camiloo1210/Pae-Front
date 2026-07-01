"""
🔮 Predictor — Estimación de tiempo de estadía.

UI desacoplada: solo conoce PredictionInput y PredictionResult.
No sabe nada de joblib, pandas ni el modelo internamente.
"""

import streamlit as st
import sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent.parent))

from ui.styles import inject_global_styles, section_header, predictor_result, badge, COLORS
from services.prediction_service import PredictionInput, predict

# ── Config ────────────────────────────────────────────────────────────
logo_img = Image.open("public/image 8.png")
st.set_page_config(
    page_title="PAE · Predictor",
    page_icon=logo_img,
    layout="wide",
    initial_sidebar_state="expanded",
)
st.logo("public/image 8.png", icon_image="public/image 8.png")
inject_global_styles()

# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("NAVEGACIÓN", unsafe_allow_html=False)
    st.page_link("Inicio.py",              label="Inicio",        icon=":material/home:")
    st.page_link("pages/1_Dashboard.py",   label="Dashboard",     icon=":material/analytics:")
    st.page_link("pages/2_Predictor.py",   label="Predictor",  icon=":material/online_prediction:")
    st.page_link("pages/3_Evaluacion.py",  label="Evaluación",    icon=":material/query_stats:")
    st.page_link("pages/4_Registro.py",    label="Registro",      icon=":material/app_registration:")
    st.page_link("pages/5_Gestion.py",     label="Gestión",       icon=":material/manage_accounts:")
    st.divider()
    st.caption(
        "El modelo fue entrenado con datos históricos del refugio. "
        "La predicción es una estimación estadística, no una garantía."
    )

# ── Header ────────────────────────────────────────────────────────────
st.markdown(section_header(
    eyebrow="Motor de inteligencia artificial",
    title="Predictor de estadía",
    subtitle=(
        "Completa las características del animal recién ingresado. "
        "El modelo estima cuántos días permanecerá en el refugio "
        "y recomienda la acción operacional más adecuada."
    ),
), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Layout: formulario | resultado ───────────────────────────────────
col_form, col_result = st.columns([1.1, 0.9], gap="large")

with col_form:
    libre = st.toggle("Desactivar validaciones de límites", value=False, help="Permite ingresar valores extremos para probar la extrapolación del modelo.")
    with st.form("predictor_form", border=False):
        st.markdown("**Datos generales**")

        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            especie = st.selectbox("Especie", ["Perro", "Gato"])
        with r1c2:
            raza = st.selectbox("Raza", ["Mestizo", "Labrador", "Poodle", "Bulldog", "Pastor Alemán", "Siamés", "Persa", "Angora"])
        with r1c3:
            tamano = st.selectbox("Tamaño", ["Pequeño", "Mediano", "Grande"])

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            edad = st.number_input("Edad (meses)", min_value=None if libre else 1, max_value=None if libre else 240, value=12)
        with r2c2:
            peso = st.number_input("Peso (kg)", min_value=None if libre else 0.5, max_value=None if libre else 80.0, value=10.0, step=0.5)

        st.markdown("<div class='pae-divider'></div>", unsafe_allow_html=True)
        st.markdown("**Estado y comportamiento**")

        r3c1, r3c2 = st.columns(2)
        with r3c1:
            salud = st.selectbox(
                "Estado de salud",
                ["Excelente", "Bueno", "Regular", "En Tratamiento"]
            )
        with r3c2:
            sociabilidad = st.selectbox(
                "Nivel de sociabilidad",
                ["Alto", "Medio", "Bajo"]
            )

        esterilizado = st.selectbox("¿Esterilizado?", ["Si", "No"])

        st.markdown("<div class='pae-divider'></div>", unsafe_allow_html=True)
        st.markdown("**Visibilidad y Recursos**")

        r4c1, r4c2 = st.columns(2)
        with r4c1:
            publicaciones = st.number_input(
                "Campañas / publicaciones", min_value=None if libre else 0, max_value=None if libre else 50, value=3
            )
        with r4c2:
            interacciones = st.number_input(
                "Interacciones esperadas", min_value=None if libre else 0, max_value=None if libre else 5000, value=200
            )
            
        r5c1, r5c2 = st.columns(2)
        with r5c1:
            visitas = st.number_input(
                "Visitas presenciales", min_value=None if libre else 0, max_value=None if libre else 100, value=5
            )
        with r5c2:
            costos = st.number_input(
                "Costo mantenimiento ($)", min_value=None if libre else 0.0, max_value=None if libre else 1000.0, value=50.0, step=5.0
            )

        submitted = st.form_submit_button(
            "Calcular estadía estimada",
            use_container_width=True,
        )

# ── Resultado ─────────────────────────────────────────────────────────
with col_result:
    if submitted:
        try:
            input_data = PredictionInput(
                especie=especie,
                raza=raza,
                edad_meses=int(edad),
                peso_kg=float(peso),
                tamano=tamano,
                estado_salud=salud,
                sociabilidad=sociabilidad,
                esterilizado=esterilizado,
                publicaciones=int(publicaciones),
                interacciones=int(interacciones),
                visitas=int(visitas),
                costos=float(costos),
            )
            result = predict(input_data)

            # ── Resultado principal ──────────────────────────────────
            st.markdown(predictor_result(result.days), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Métricas secundarias ─────────────────────────────────
            st.markdown("**Factores de riesgo detectados**")
            mc1, mc2 = st.columns(2)

            with mc1:
                riesgo_salud = salud in ["Regular", "En Tratamiento"]
                st.metric(
                    "Estado de salud",
                    salud,
                    delta="Factor de riesgo" if riesgo_salud else "Sin riesgo",
                    delta_color="inverse" if riesgo_salud else "normal",
                )
            with mc2:
                riesgo_social = sociabilidad == "Bajo"
                st.metric(
                    "Sociabilidad",
                    sociabilidad,
                    delta="Factor de riesgo" if riesgo_social else "Sin riesgo",
                    delta_color="inverse" if riesgo_social else "normal",
                )

            mc3, mc4 = st.columns(2)
            with mc3:
                riesgo_tamano = tamano == "Grande" and especie == "Perro"
                st.metric(
                    "Tamaño",
                    f"{especie} {tamano}",
                    delta="Mayor dificultad" if riesgo_tamano else "Sin riesgo",
                    delta_color="inverse" if riesgo_tamano else "normal",
                )
            with mc4:
                st.metric(
                    "Visibilidad",
                    f"{publicaciones} campañas",
                    delta=f"{interacciones:,} interacciones",
                    delta_color="normal",
                )

            # ── Guardar en session_state para persistencia ────────────
            st.session_state["ultima_prediccion"] = {
                "dias":     result.days,
                "label":    result.label,
                "especie":  especie,
                "tamano":   tamano,
            }

        except FileNotFoundError as e:
            st.error(
                "**Modelo no encontrado.** "
                "Verifica que `preprocesador_pae.pkl` y `modelo_pae.pkl` "
                "estén en la raíz del proyecto.\n\n"
                f"Detalle técnico: `{e}`"
            )
        except Exception as e:
            st.error(f"Error inesperado en la predicción: `{e}`")

    else:
        # Estado vacío — guía al usuario
        st.markdown("""
        <div style="
            background: #F9FAFB;
            border: 1.5px dashed rgba(0,0,0,0.1);
            border-radius: 16px;
            padding: 48px 32px;
            text-align: center;
            color: #6B7280;
        ">
            <div style="font-size: 40px; margin-bottom: 16px;">
                <span class="material-symbols-outlined" style="font-size: 48px; color: #3B82F6;">online_prediction</span>
            </div>
            <div style="font-size: 15px; font-weight: 500; color: #374151; margin-bottom: 8px;">
                Completa el formulario para predecir
            </div>
            <div style="font-size: 13px; line-height: 1.6;">
                El modelo analizará las características del animal<br>
                y estimará su tiempo de estadía en el refugio.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Si hay predicción previa en sesión, mostrarla como contexto
        if "ultima_prediccion" in st.session_state:
            prev = st.session_state["ultima_prediccion"]
            st.markdown("<br>", unsafe_allow_html=True)
            st.caption(
                f"Última predicción: **{prev['especie']} {prev['tamano']}** → "
                f"**{prev['dias']} días** ({prev['label']})"
            )
