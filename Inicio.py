"""
🏠 PAE — Punto de entrada de la aplicación.

Muestra una pantalla de bienvenida y configura el sidebar
que es común a todas las páginas multipage de Streamlit.
"""

import streamlit as st
from ui.styles import inject_global_styles, section_header, COLORS

st.set_page_config(
    page_title="PAE · Sistema de Adopciones",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()

# ── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-dot">🐾</div>
        <div>
            <div class="sidebar-logo-text">PAE</div>
            <div class="sidebar-logo-sub">Sistema de Adopciones</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("NAVEGACIÓN", unsafe_allow_html=False)
    st.page_link("Inicio.py",              label="Inicio",        icon="🏠")
    st.page_link("pages/1_Dashboard.py",   label="Dashboard",     icon="📊")
    st.page_link("pages/2_Predictor.py",   label="Predictor IA",  icon="🔮")

    st.divider()
    st.caption("Versión 1.0 · PAE Ecuador")

# ── Hero ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

col_hero, col_img = st.columns([3, 1])

with col_hero:
    st.markdown(section_header(
        eyebrow="Bienvenido al sistema",
        title="Inteligencia artificial para el bienestar animal",
        subtitle=(
            "Predice el tiempo de estadía de cada animal en el refugio, "
            "detecta casos críticos antes de que se vuelvan urgentes, "
            "y toma decisiones operacionales con datos reales."
        ),
    ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.page_link(
            "pages/1_Dashboard.py",
            label="Ver panel general →",
            icon="📊",
            use_container_width=True,
        )
    with c2:
        st.page_link(
            "pages/2_Predictor.py",
            label="Predecir estadía →",
            icon="🔮",
            use_container_width=True,
        )

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

# ── Tres pilares informativos ─────────────────────────────────────────
p1, p2, p3 = st.columns(3)

with p1:
    st.markdown("### 📊 Dashboard operacional")
    st.markdown(
        "KPIs en tiempo real, alertas de casos prioritarios, "
        "y tendencias históricas de adopciones. "
        "Todo lo que el equipo necesita en una pantalla."
    )

with p2:
    st.markdown("### 🔮 Predictor IA")
    st.markdown(
        "Ingresa las características de un animal recién ingresado "
        "y el modelo predice cuántos días permanecerá en el refugio, "
        "junto con la acción operacional recomendada."
    )

with p3:
    st.markdown("### ⚡ Acción temprana")
    st.markdown(
        "Los casos de larga estadía se detectan antes de que ocurran. "
        "El sistema genera alertas para activar protocolos foster "
        "o campañas de visibilidad a tiempo."
    )
