"""
📝 Registro — Ingreso de nuevos animales al refugio.

Permite agregar un nuevo animal al sistema. Al guardarlo, se evalúa
automáticamente con el modelo de predicción para lanzar alertas preventivas.
"""

import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from PIL import Image
import sys
from pathlib import Path

# Configuración de paths relativos
sys.path.insert(0, str(Path(__file__).parent.parent))

from ui.styles import inject_global_styles, section_header, COLORS
from services.data_service import add_new_animal, load_historical_data

# ── Configuración de Página ───────────────────────────────────────────
logo_img = Image.open("public/image 8.png")
st.set_page_config(
    page_title="PAE · Registro",
    page_icon=logo_img,
    layout="centered",
    initial_sidebar_state="expanded",
)
st.logo("public/image 8.png", icon_image="public/image 8.png")
inject_global_styles()

# ── Sidebar Navegación ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("NAVEGACIÓN", unsafe_allow_html=False)
    st.page_link("Inicio.py",              label="Inicio",        icon=":material/home:")
    st.page_link("pages/1_Dashboard.py",   label="Dashboard",     icon=":material/analytics:")
    st.page_link("pages/2_Predictor.py",   label="Predictor",     icon=":material/online_prediction:")
    st.page_link("pages/3_Evaluacion.py",  label="Evaluación",    icon=":material/query_stats:")
    st.page_link("pages/4_Registro.py",    label="Registro",      icon=":material/app_registration:")
    st.page_link("pages/5_Gestion.py",     label="Gestión",       icon=":material/manage_accounts:")

# ── Header ────────────────────────────────────────────────────────────
st.markdown(section_header(
    eyebrow="Ingresos",
    title="Registro de Nuevo Animal",
    subtitle="Registra un nuevo ingreso. El sistema evaluará el caso automáticamente para alertar sobre posibles largas estadías.",
), unsafe_allow_html=True)

# ── Carga de Modelos y Datos Históricos ───────────────────────────────
@st.cache_resource
def load_ml_components():
    try:
        ct = joblib.load('preprocesador_pae.pkl')
        model = joblib.load('modelo_pae.pkl')
        return ct, model
    except Exception as e:
        return None, None

ct, model = load_ml_components()
df_hist = load_historical_data()

# ── Diálogo de Resultados S+ ──────────────────────────────────────────
@st.dialog("Evaluación de Ingreso", width="large")
def show_prediction_dialog(nombre, new_id, prediccion_dias, costo_estimado, especie, estado_salud, nivel_sociabilidad, df_plot):
    if prediccion_dias > 45:
        bg_color = "rgba(239, 68, 68, 0.08)"
        border_color = "rgba(239, 68, 68, 0.3)"
        icon = "🚨"
        title = "ALERTA CRÍTICA"
        color = "#EF4444"
        desc = "Activar protocolo Foster de inmediato o plan de visibilidad prioritario."
    elif prediccion_dias > 25:
        bg_color = "rgba(245, 158, 11, 0.08)"
        border_color = "rgba(245, 158, 11, 0.3)"
        icon = "⚠️"
        title = "Aviso Preventivo"
        color = "#F59E0B"
        desc = "Se estima una estadía moderada. Recomendamos seguimiento continuo."
    else:
        bg_color = "rgba(16, 185, 129, 0.08)"
        border_color = "rgba(16, 185, 129, 0.3)"
        icon = "✨"
        title = "Proyección Favorable"
        color = "#10B981"
        desc = "Se estima una adopción rápida. Excelente perfil."
        
    tab1, tab2 = st.tabs(["Resumen de Registro", "Inteligencia y Costos (KNN)"])
    
    with tab1:
        html_content = f"""
        <div style="background-color: {bg_color}; border: 1px solid {border_color}; border-radius: 12px; padding: 24px; text-align: center; font-family: 'Inter', sans-serif;">
            <div style="font-size: 3.5rem; margin-bottom: 12px; line-height: 1;">{icon}</div>
            <h3 style="color: {color}; margin: 0; font-weight: 700; font-size: 1.5rem;">{title}</h3>
            <p style="color: #475569; font-size: 1.05rem; margin-top: 12px; margin-bottom: 24px;">
                El modelo predictivo estima que <b>{nombre}</b> pasará <br>
                aproximadamente <b style="color: #0F172A; font-size: 1.3rem;">{prediccion_dias} días</b> en el refugio.
            </p>
            <div style="background-color: white; border-radius: 8px; padding: 16px; text-align: left; box-shadow: 0 1px 3px rgba(0,0,0,0.1); font-size: 0.95rem;">
                <div style="margin-bottom: 8px; color: #334155;"><strong>ID Asignado:</strong> <span style="float: right; color: #0F172A; font-weight: 600;">{new_id}</span></div>
                <div style="margin-bottom: 8px; color: #334155;"><strong>Costo Estimado:</strong> <span style="float: right; color: #0F172A; font-weight: 600;">${costo_estimado}</span></div>
                <div style="margin-bottom: 8px; color: #334155;"><strong>Salud / Sociabilidad:</strong> <span style="float: right; color: #0F172A;">{estado_salud} / {nivel_sociabilidad}</span></div>
                <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid #E2E8F0;">
                    <strong style="color: {color};">Acción recomendada:</strong><br>
                    <span style="color: #475569;">{desc}</span>
                </div>
            </div>
            <div style="margin-top: 20px; font-size: 0.8rem; color: #94A3B8;">
                El registro fue guardado exitosamente. El panel de Dashboard se ha actualizado en tiempo real.
            </div>
        </div>
        <br>
        """
        st.markdown(html_content, unsafe_allow_html=True)
        if st.button("Aceptar y Continuar", type="primary", use_container_width=True, key="btn_accept1"):
            st.rerun()
            
    with tab2:
        st.markdown(
            f"#### Grafo de Similitud de K-Nearest Neighbors (KNN)\n"
            f"El sistema filtró estrictamente por **Especie ({especie})** y **Estado de Salud ({estado_salud})**. "
            f"Dentro de ese sub-grupo, calculó matemáticamente a los **{df_plot[df_plot['Tipo'] == 'Top Similares'].shape[0]} animales históricamente más idénticos** "
            f"al que acabas de registrar basándose en la similitud de su Peso y Edad.\n\n"
            f"*(Nota visual: Si ves menos puntos azules, es porque algunos animales históricos tienen exactamente el mismo peso y edad, superponiéndose perfectamente en el gráfico).* "
        )
        
        # Graficar KNN
        fig = px.scatter(
            df_plot,
            x='Peso_Kg',
            y='Edad_Meses',
            color='Tipo',
            color_discrete_map={
                'Histórico': '#CBD5E1', 
                'Top Similares': '#3B82F6', 
                'Nuevo Ingreso (Centroide)': '#EF4444'
            },
            symbol='Tipo',
            symbol_map={
                'Histórico': 'circle', 
                'Top Similares': 'circle', 
                'Nuevo Ingreso (Centroide)': 'star'
            },
            hover_data=['Costos_Mantenimiento'] if 'Costos_Mantenimiento' in df_plot.columns else None
        )
        
        fig.update_traces(marker=dict(size=12, opacity=0.85, line=dict(width=1, color='DarkSlateGrey')))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
            margin=dict(l=0, r=0, t=10, b=0),
            height=300,
            xaxis=dict(title="Peso (Kg)"),
            yaxis=dict(title="Edad (Meses)")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"El costo final de **${costo_estimado}** se obtuvo promediando los costos reales de los {df_plot[df_plot['Tipo'] == 'Top Similares'].shape[0]} vecinos más cercanos marcados en azul.")
        
        if st.button("Cerrar", use_container_width=True, key="btn_close2"):
            st.rerun()

# ── Formulario de Registro ────────────────────────────────────────────
with st.container():
    st.markdown("<h4 style='color:#0F172A; font-weight:600;'>1. Datos Generales</h4>", unsafe_allow_html=True)
    nombre = st.text_input("Nombre del Animal", placeholder="Ej: Max, Luna...")
    
    col1, col2 = st.columns(2)
    with col1:
        especie = st.selectbox("Especie", ["Perro", "Gato"])
        edad_meses = st.number_input("Edad (Meses)", min_value=1, max_value=240, value=12)
        peso_kg = st.number_input("Peso (Kg)", min_value=0.5, max_value=80.0, value=10.0, step=0.5)
    with col2:
        if especie == "Perro":
            raza = st.selectbox("Raza", ["Mestizo", "Labrador", "Poodle", "Bulldog", "Pastor Alemán"])
        else:
            raza = st.selectbox("Raza", ["Mestizo", "Siamés", "Persa", "Angora"])
            
        tamano = st.selectbox("Tamaño", ["Pequeño", "Mediano", "Grande"])

    st.markdown("<div class='pae-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0F172A; font-weight:600;'>2. Estado Actual</h4>", unsafe_allow_html=True)
    
    col3, col4, col5 = st.columns(3)
    with col3:
        estado_salud = st.selectbox("Estado de Salud", ["Excelente", "Bueno", "Regular", "En Tratamiento"])
    with col4:
        nivel_sociabilidad = st.selectbox("Nivel de Sociabilidad", ["Alto", "Medio", "Bajo"])
    with col5:
        esterilizado = st.selectbox("¿Esterilizado?", ["Si", "No"])
        
    st.markdown("<div class='pae-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0F172A; font-weight:600;'>3. Recursos de Marketing Estimados</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; color:#64748B;'>Define la inversión inicial en visibilidad para este animal.</p>", unsafe_allow_html=True)
    
    col6, col7 = st.columns(2)
    with col6:
        publicaciones = st.slider("Publicaciones programadas", min_value=1, max_value=15, value=2)
        visitas_esperadas = st.number_input("Visitas iniciales programadas", min_value=0, max_value=20, value=0)
    with col7:
        interacciones = st.number_input("Objetivo de Interacciones en RRSS", min_value=0, max_value=1000, value=150)
        
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.button("Registrar y Evaluar Ingreso", type="primary", use_container_width=True)

# ── Lógica de Procesamiento ───────────────────────────────────────────
if submitted:
    if not nombre.strip():
        st.error("El nombre del animal es obligatorio.")
    elif not ct or not model:
        st.error("Error: No se pudieron cargar los modelos de Machine Learning. Asegúrate de ejecutar `entrenar.py`.")
    else:
        # Calcular Costo Promedio Inteligente (Similitud K-Nearest Neighbors Manual)
        try:
            # 1. Filtrar por características categóricas críticas
            mask_estricta = (df_hist['Especie'] == especie) & (df_hist['Estado_Salud'] == estado_salud) & (df_hist['Tamano'] == tamano)
            if mask_estricta.any():
                subset = df_hist[mask_estricta]
            else:
                # Fallback 1: Especie + Salud
                mask_media = (df_hist['Especie'] == especie) & (df_hist['Estado_Salud'] == estado_salud)
                if mask_media.any():
                    subset = df_hist[mask_media]
                else:
                    # Fallback 2: Solo Especie
                    subset = df_hist[df_hist['Especie'] == especie]
            
            if subset.empty:
                subset = df_hist
                
            # 2. Calcular similitud (distancia Euclidiana) basada en variables numéricas (Peso y Edad)
            # Evitar divisiones por cero sumando un epsilon
            std_peso = subset['Peso_Kg'].std() if subset['Peso_Kg'].std() > 0 else 1.0
            std_edad = subset['Edad_Meses'].std() if subset['Edad_Meses'].std() > 0 else 1.0
            
            distancias = (
                ((subset['Peso_Kg'] - peso_kg) / std_peso) ** 2 + 
                ((subset['Edad_Meses'] - edad_meses) / std_edad) ** 2
            ) ** 0.5
            
            # 3. Tomar el promedio de los 5 animales históricamente más similares
            top_5_similares = distancias.nsmallest(5).index
            costo_estimado = subset.loc[top_5_similares, 'Costos_Mantenimiento'].mean()
            
        except Exception as e:
            costo_estimado = 50.0 # Fallback seguro absoluto
            
        costo_estimado = round(costo_estimado, 2)
        
        # 1. Preparar datos para evaluación ML
        input_data = pd.DataFrame([{
            'Especie': especie,
            'Raza': raza,
            'Edad_Meses': edad_meses,
            'Peso_Kg': peso_kg,
            'Tamano': tamano,
            'Estado_Salud': estado_salud,
            'Nivel_Sociabilidad': nivel_sociabilidad,
            'Esterilizado': esterilizado,
            'Publicaciones': publicaciones,
            'Interacciones_RRSS': interacciones,
            'Visitas_Recibidas': visitas_esperadas,
            'Costos_Mantenimiento': costo_estimado
        }])
        
        # 2. Hacer predicción
        try:
            X_procesado = ct.transform(input_data)
            prediccion_dias = model.predict(X_procesado)[0]
            prediccion_dias = max(3, int(round(prediccion_dias))) # Minimo lógico de 3 días
            
            # 3. Guardar en el CSV
            record_dict = {
                'Nombre': nombre.strip(),
                'Especie': especie,
                'Raza': raza,
                'Edad_Meses': edad_meses,
                'Peso_Kg': peso_kg,
                'Tamano': tamano,
                'Estado_Salud': estado_salud,
                'Nivel_Sociabilidad': nivel_sociabilidad,
                'Esterilizado': esterilizado,
                'Publicaciones': publicaciones,
                'Interacciones_RRSS': interacciones,
                'Visitas_Recibidas': visitas_esperadas,
                'Costos_Mantenimiento': costo_estimado
            }
            new_id = add_new_animal(record_dict)
            
            # Preparar datos para el gráfico del modal
            df_plot = subset.copy()
            df_plot['Tipo'] = 'Histórico'
            
            # Marcar el top 5 si existían vecinos
            if 'top_5_similares' in locals():
                df_plot.loc[top_5_similares, 'Tipo'] = 'Top Similares'
                
            # Agregar el animal actual como centroide
            nuevo = pd.DataFrame([{
                'Peso_Kg': peso_kg, 
                'Edad_Meses': edad_meses, 
                'Tipo': 'Nuevo Ingreso (Centroide)'
            }])
            df_plot = pd.concat([df_plot, nuevo], ignore_index=True)
            
            # 4. Mostrar resultados en pop-up S+ Tier con tabs
            show_prediction_dialog(
                nombre=nombre.strip(), 
                new_id=new_id, 
                prediccion_dias=prediccion_dias, 
                costo_estimado=costo_estimado, 
                especie=especie, 
                estado_salud=estado_salud, 
                nivel_sociabilidad=nivel_sociabilidad,
                df_plot=df_plot
            )
            
        except Exception as e:
            st.error(f"Ocurrió un error al procesar el registro: {str(e)}")
