"""
PAE — Punto de entrada de la aplicación.
"""

import streamlit as st
from PIL import Image
from ui.styles import inject_global_styles

logo_img = Image.open("public/image 8.png")
st.set_page_config(
    page_title="PAE · Sistema de Adopciones",
    page_icon=logo_img,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.logo("public/image 8.png", icon_image="public/image 8.png")

inject_global_styles()

# ── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("NAVEGACIÓN", unsafe_allow_html=False)
    st.page_link("Inicio.py",              label="Inicio",        icon=":material/home:")
    st.page_link("pages/1_Dashboard.py",   label="Dashboard",     icon=":material/analytics:")
    st.page_link("pages/2_Predictor.py",   label="Predictor",  icon=":material/online_prediction:")
    st.page_link("pages/3_Evaluacion.py",  label="Evaluación",    icon=":material/query_stats:")
    st.page_link("pages/4_Registro.py",    label="Registro",      icon=":material/app_registration:")
    st.page_link("pages/5_Gestion.py",     label="Gestión",       icon=":material/manage_accounts:")

    st.divider()
    st.caption("Versión 2.0 · PAE Ecuador")

# ── Hero Section ─────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

col_hero, col_empty, col_img = st.columns([1.2, 0.1, 1])

with col_hero:
    st.html("""
        <div class="hero-title">
            Revolucionando el cuidado animal con <span>Análisis de Datos.</span>
        </div>
        <div class="hero-subtitle">
            Nuestro modelo centraliza la operación del refugio en tiempo real. 
            Esta herramienta predice la estadía de cada animal, identifica casos críticos 
            antes de que se agraven y optimiza las adopciones para salvar más vidas.
        </div>
    """)

    c1, c2 = st.columns(2)
    with c1:
        st.page_link(
            "pages/1_Dashboard.py",
            label="Ver Panel Operacional",
            icon=":material/dashboard_customize:",
        )
    with c2:
        st.page_link(
            "pages/2_Predictor.py",
            label="Probar Predictor",
            icon=":material/magic_button:",
        )

with col_img:
    st.html('<div class="rounded-img">')
    st.image("public/hero_dog.png", use_container_width=True)
    st.html('</div>')


