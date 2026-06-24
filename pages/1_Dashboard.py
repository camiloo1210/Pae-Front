"""
📊 Dashboard — Panel operacional del refugio PAE.

Muestra KPIs, alertas de casos prioritarios y gráficos
alimentados por datos históricos reales (o sintéticos en demo).
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from PIL import Image

# Importaciones relativas al proyecto
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ui.styles import inject_global_styles, kpi_card, section_header, COLORS
from services.data_service import (
    load_historical_data,
    get_kpi_summary,
    get_priority_alerts,
    get_stay_by_species_size,
    get_monthly_adoptions,
)

# ── Config ────────────────────────────────────────────────────────────
logo_img = Image.open("public/image 8.png")
st.set_page_config(
    page_title="PAE · Dashboard",
    page_icon=logo_img,
    layout="wide",
    initial_sidebar_state="expanded",
)
st.logo("public/image 8.png", icon_image="public/image 8.png")
inject_global_styles()

# ── Sidebar ───────────────────────────────────────────────────────────
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
    st.page_link("Inicio.py",             label="Inicio",       icon="🏠")
    st.page_link("pages/1_Dashboard.py",  label="Dashboard",    icon="📊")
    st.page_link("pages/2_Predictor.py",  label="Predictor IA", icon="🔮")
    st.divider()

    st.markdown("FILTROS", unsafe_allow_html=False)
    especie_filtro = st.multiselect(
        "Especie", ["Perro", "Gato"], default=["Perro", "Gato"]
    )
    estado_filtro = st.multiselect(
        "Estado de salud",
        ["Excelente", "Bueno", "Regular", "En Tratamiento"],
        default=["Excelente", "Bueno", "Regular", "En Tratamiento"],
    )

# ── Cargar y filtrar datos ────────────────────────────────────────────
try:
    df_raw = load_historical_data()
except ValueError as e:
    st.error(f"Error de esquema en el CSV: {e}")
    st.stop()

df = df_raw[
    df_raw["Especie"].isin(especie_filtro) &
    df_raw["Estado_Salud"].isin(estado_filtro)
].copy()

if df.empty:
    st.warning("No hay datos con los filtros seleccionados. Amplía los filtros en el panel lateral.")
    st.stop()

kpis   = get_kpi_summary(df)
alerts = get_priority_alerts(df)

# ── Header ────────────────────────────────────────────────────────────
st.markdown(section_header(
    eyebrow="Panel operacional",
    title="Estado actual del refugio",
    subtitle="Actualizado automáticamente · Los filtros del panel lateral aplican a todas las secciones.",
), unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

accents = [COLORS["primary"], COLORS["blue"], COLORS["amber"], COLORS["red"]]
kpi_data = [
    ("Animales activos",     str(kpis["total_activos"]),   "", True),
    ("Adopciones este mes",  str(kpis["adoptados_mes"]),   f"Tasa global: {kpis['tasa_adopcion']}%", True),
    ("Estadía promedio",     f"{kpis['estadia_promedio']}d", "días en refugio", True),
    ("Casos larga estadía",  str(kpis["larga_estadia"]),   "Requieren acción", False),
]

for col, (eyebrow, value, delta, pos), accent in zip([k1,k2,k3,k4], kpi_data, accents):
    with col:
        st.markdown(kpi_card(eyebrow, value, delta, pos, accent), unsafe_allow_html=True)

st.markdown("<div class='pae-divider'></div>", unsafe_allow_html=True)

# ── Tabs: Análisis / Alertas ──────────────────────────────────────────
tab_analisis, tab_alertas, tab_tabla = st.tabs(
    ["📈  Análisis", "⚠️  Alertas prioritarias", "🗂️  Datos completos"]
)

# ───────────────────────────────────────────────────────────────────────
# TAB 1: ANÁLISIS
# ───────────────────────────────────────────────────────────────────────
with tab_analisis:
    col_bar, col_donut = st.columns([1.7, 1])

    # Gráfico de barras — estadía por especie y tamaño
    with col_bar:
        st.markdown("**Estadía promedio por especie y tamaño**")
        df_bar = get_stay_by_species_size(df)

        color_map = {"Perro": COLORS["primary"], "Gato": COLORS["blue"]}

        fig_bar = px.bar(
            df_bar,
            x="Promedio_Dias",
            y=df_bar["Especie"] + " · " + df_bar["Tamano"],
            color="Especie",
            color_discrete_map=color_map,
            orientation="h",
            text="Promedio_Dias",
        )
        fig_bar.update_traces(
            texttemplate="%{text:.0f}d",
            textposition="outside",
            marker_line_width=0,
        )
        fig_bar.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
            xaxis=dict(showgrid=False, showticklabels=False, title=""),
            yaxis=dict(title="", tickfont=dict(size=12)),
            margin=dict(l=0, r=40, t=30, b=0),
            height=300,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Donut — composición del refugio
    with col_donut:
        st.markdown("**Composición del refugio**")
        activos = df[~df["Adoptado"]]
        comp    = activos["Especie"].value_counts().reset_index()
        comp.columns = ["Especie", "Cantidad"]

        fig_donut = go.Figure(go.Pie(
            labels=comp["Especie"],
            values=comp["Cantidad"],
            hole=0.6,
            marker=dict(colors=[COLORS["primary"], COLORS["blue"]]),
            textinfo="label+percent",
            textfont=dict(size=13),
        ))
        fig_donut.update_layout(
            paper_bgcolor="white",
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            height=280,
            annotations=[dict(
                text=f"<b>{activos.shape[0]}</b><br>activos",
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False,
            )],
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("<div class='pae-divider'></div>", unsafe_allow_html=True)

    # Gráfico de tendencia mensual
    st.markdown("**Adopciones mensuales — últimos 12 meses**")
    df_monthly = get_monthly_adoptions(df)

    if not df_monthly.empty:
        df_monthly["Mes_str"] = df_monthly["Mes"].astype(str)
        fig_line = px.area(
            df_monthly,
            x="Mes_str",
            y="Adopciones",
            line_shape="spline",
            color_discrete_sequence=[COLORS["primary"]],
        )
        fig_line.update_traces(
            fill="tozeroy",
            fillcolor="rgba(29,158,117,0.1)",
            line=dict(width=2.5),
        )
        fig_line.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(title="", showgrid=False),
            yaxis=dict(title="Adopciones", showgrid=True, gridcolor="#F3F4F6"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=260,
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No hay suficientes datos históricos para mostrar la tendencia mensual.")

# ───────────────────────────────────────────────────────────────────────
# TAB 2: ALERTAS
# ───────────────────────────────────────────────────────────────────────
with tab_alertas:
    st.markdown(section_header(
        eyebrow="Casos prioritarios",
        title="Animales que requieren acción",
        subtitle="Ordenados por urgencia — mayor estadía primero.",
    ), unsafe_allow_html=True)

    for _, row in alerts.iterrows():
        dias = int(row["Dias_Estadia"])

        if dias > 45:
            badge_class = "badge-red"
            days_class  = "alert-days-red"
            accion      = "Activar protocolo foster"
        elif dias > 25:
            badge_class = "badge-amber"
            days_class  = "alert-days-amber"
            accion      = "Revisar plan de visibilidad"
        else:
            badge_class = "badge-green"
            days_class  = "alert-days-green"
            accion      = "Seguimiento rutinario"

        st.markdown(f"""
        <div class="alert-row">
            <div class="alert-days {days_class}">{dias}d</div>
            <div style="flex:1">
                <div class="alert-name">{row['Nombre']} — {row['Especie']}, {row['Tamano']}</div>
                <div class="alert-meta">
                    Salud: {row['Estado_Salud']} &nbsp;·&nbsp;
                    Sociabilidad: {row['Nivel_Sociabilidad']} &nbsp;·&nbsp;
                    <span class="badge {badge_class}">{accion}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("pages/2_Predictor.py",
                 label="Ir al predictor para analizar un caso →", icon="🔮")

# ───────────────────────────────────────────────────────────────────────
# TAB 3: DATOS COMPLETOS
# ───────────────────────────────────────────────────────────────────────
with tab_tabla:
    st.markdown(f"Mostrando **{len(df):,}** registros con los filtros aplicados.")

    display_cols = [
        "Nombre", "Especie", "Tamano", "Edad_Meses",
        "Estado_Salud", "Nivel_Sociabilidad", "Dias_Estadia", "Adoptado"
    ]
    cols_disponibles = [c for c in display_cols if c in df.columns]

    st.dataframe(
        df[cols_disponibles].sort_values("Dias_Estadia", ascending=False),
        use_container_width=True,
        height=460,
        column_config={
            "Dias_Estadia": st.column_config.NumberColumn("Días en refugio", format="%d días"),
            "Adoptado":     st.column_config.CheckboxColumn("Adoptado"),
            "Edad_Meses":   st.column_config.NumberColumn("Edad (meses)"),
        },
        hide_index=True,
    )
