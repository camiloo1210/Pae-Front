"""
⚙️ Gestión — Administración y actualización de casos activos.
"""

import streamlit as st
import pandas as pd
import joblib
from PIL import Image
import sys
from pathlib import Path
from datetime import date

# Configuración de paths relativos
sys.path.insert(0, str(Path(__file__).parent.parent))

from ui.styles import inject_global_styles, section_header, COLORS
from services.data_service import load_historical_data, update_animal

# ── Configuración de Página ───────────────────────────────────────────
logo_img = Image.open("public/image 8.png")
st.set_page_config(
    page_title="PAE · Gestión",
    page_icon=logo_img,
    layout="wide",
    initial_sidebar_state="expanded",
)
st.logo("public/image 8.png", icon_image="public/image 8.png")
inject_global_styles()

# ── Sidebar Navegación y Filtros ──────────────────────────────────────
with st.sidebar:
    st.markdown("NAVEGACIÓN", unsafe_allow_html=False)
    st.page_link("Inicio.py",              label="Inicio",        icon=":material/home:")
    st.page_link("pages/1_Dashboard.py",   label="Dashboard",     icon=":material/analytics:")
    st.page_link("pages/2_Predictor.py",   label="Predictor",     icon=":material/online_prediction:")
    st.page_link("pages/3_Evaluacion.py",  label="Evaluación",    icon=":material/query_stats:")
    st.page_link("pages/4_Registro.py",    label="Registro",      icon=":material/app_registration:")
    st.page_link("pages/5_Gestion.py",     label="Gestión",       icon=":material/manage_accounts:")
    
    st.divider()
    
    st.markdown("FILTROS", unsafe_allow_html=False)
    adoptado_filtro = st.radio("Estado de Adopción", ["Todos", "En Refugio (Activos)", "Ya Adoptados"], index=1)
    
    especie_filtro = st.multiselect(
        "Especie", ["Perro", "Gato"], default=["Perro", "Gato"]
    )
    estado_filtro = st.multiselect(
        "Estado de salud",
        ["Excelente", "Bueno", "Regular", "En Tratamiento"],
        default=["Excelente", "Bueno", "Regular", "En Tratamiento"],
    )
    st.markdown("<br>", unsafe_allow_html=True)
    busqueda_nombre = st.text_input(
        "Buscar por nombre o ID",
        placeholder="Ej: Max, PAE-00001...",
    )

# ── Header ────────────────────────────────────────────────────────────
st.markdown(section_header(
    eyebrow="Administración",
    title="Gestión de Expedientes",
    subtitle="Busca, filtra y actualiza los registros. Observa cómo cambia la predicción de inteligencia artificial al vuelo.",
), unsafe_allow_html=True)

# ── Carga de Modelos y Datos ──────────────────────────────────────────
@st.cache_resource
def load_ml_components():
    try:
        ct = joblib.load('preprocesador_pae.pkl')
        model = joblib.load('modelo_pae.pkl')
        return ct, model
    except Exception as e:
        return None, None

ct, model = load_ml_components()
df = load_historical_data()

# ── Diálogo de Recálculo S+ ───────────────────────────────────────────
@st.dialog("Recálculo del Modelo", width="large")
def show_update_dialog(nombre, new_id, prediccion_dias, costo_estimado, estado_salud, nivel_sociabilidad):
    if isinstance(prediccion_dias, str):
        prediccion_dias = 999
        
    if prediccion_dias > 45:
        bg_color = "rgba(239, 68, 68, 0.08)"
        border_color = "rgba(239, 68, 68, 0.3)"
        title = "ALERTA CRÍTICA"
        color = "#EF4444"
        desc = "La nueva proyección sigue siendo de alto riesgo."
    elif prediccion_dias > 25:
        bg_color = "rgba(245, 158, 11, 0.08)"
        border_color = "rgba(245, 158, 11, 0.3)"
        title = "Aviso Preventivo"
        color = "#F59E0B"
        desc = "La proyección indica una estadía moderada con estos nuevos datos."
    else:
        bg_color = "rgba(16, 185, 129, 0.08)"
        border_color = "rgba(16, 185, 129, 0.3)"
        title = "Proyección Favorable"
        color = "#10B981"
        desc = "Con esta actualización, se estima una adopción rápida. ¡Gran trabajo!"
        
    html_content = f"""
    <div style="background-color: {bg_color}; border: 1px solid {border_color}; border-radius: 12px; padding: 24px; text-align: center; font-family: 'Inter', sans-serif;">
        <h3 style="color: {color}; margin: 0; font-weight: 700; font-size: 1.5rem;">{title}</h3>
        <p style="color: #475569; font-size: 1.05rem; margin-top: 12px; margin-bottom: 24px;">
            El recálculo de Inteligencia Artificial para <b>{nombre}</b> estima ahora <br>
            aproximadamente <b style="color: #0F172A; font-size: 1.3rem;">{prediccion_dias} días</b> de estadía total.
        </p>
        <div style="background-color: white; border-radius: 8px; padding: 16px; text-align: left; box-shadow: 0 1px 3px rgba(0,0,0,0.1); font-size: 0.95rem;">
            <div style="margin-bottom: 8px; color: #334155;"><strong>ID Expediente:</strong> <span style="float: right; color: #0F172A; font-weight: 600;">{new_id}</span></div>
            <div style="margin-bottom: 8px; color: #334155;"><strong>Costo Mantenimiento (Actualizado):</strong> <span style="float: right; color: #0F172A; font-weight: 600;">${costo_estimado}</span></div>
            <div style="margin-bottom: 8px; color: #334155;"><strong>Salud / Sociabilidad:</strong> <span style="float: right; color: #0F172A;">{estado_salud} / {nivel_sociabilidad}</span></div>
            <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid #E2E8F0;">
                <strong style="color: {color};">Conclusión:</strong><br>
                <span style="color: #475569;">{desc}</span>
            </div>
        </div>
        <div style="margin-top: 20px; font-size: 0.8rem; color: #94A3B8;">
            Cambios guardados. El dashboard y la tabla se actualizarán al continuar.
        </div>
    </div>
    <br>
    """
    st.markdown(html_content, unsafe_allow_html=True)
    if st.button("Aceptar y Continuar", type="primary", use_container_width=True, key="btn_accept_update"):
        st.rerun()

# ── Aplicar Filtros ───────────────────────────────────────────────────
df_filtrado = df.copy()

if adoptado_filtro == "En Refugio (Activos)":
    df_filtrado = df_filtrado[df_filtrado['Adoptado'] == False]
elif adoptado_filtro == "Ya Adoptados":
    df_filtrado = df_filtrado[df_filtrado['Adoptado'] == True]
    
df_filtrado = df_filtrado[
    df_filtrado["Especie"].isin(especie_filtro) &
    df_filtrado["Estado_Salud"].isin(estado_filtro)
]

if busqueda_nombre:
    mask_busqueda = df_filtrado["Nombre"].str.contains(busqueda_nombre, case=False, na=False) | \
                    df_filtrado["ID_Ingreso"].str.contains(busqueda_nombre, case=False, na=False)
    df_filtrado = df_filtrado[mask_busqueda]

# Calcular predicción al vuelo si el modelo está disponible y hay datos
if ct and model and not df_filtrado.empty:
    try:
        # Preprocesar datos
        input_data = df_filtrado[[
            'Especie', 'Raza', 'Edad_Meses', 'Peso_Kg', 'Tamano',
            'Estado_Salud', 'Nivel_Sociabilidad', 'Esterilizado',
            'Publicaciones', 'Interacciones_RRSS', 'Visitas_Recibidas', 'Costos_Mantenimiento'
        ]]
        X_procesado = ct.transform(input_data)
        predicciones = model.predict(X_procesado)
        df_filtrado['Prediccion_Estadia_Dias'] = [max(3, int(round(p))) for p in predicciones]
    except Exception as e:
        df_filtrado['Prediccion_Estadia_Dias'] = "Error ML"

# ── 1. Visor de Casos Activos ─────────────────────────────────────────
st.markdown(f"### Listado de Residentes ({len(df_filtrado)} encontrados)")

if df_filtrado.empty:
    st.info("No se encontraron registros con los filtros actuales.")
else:
    # Seleccionar columnas relevantes para mostrar
    cols_to_show = ['ID_Ingreso', 'Nombre', 'Especie', 'Raza', 'Estado_Salud', 'Nivel_Sociabilidad', 'Adoptado', 'Prediccion_Estadia_Dias', 'Dias_Estadia']
    cols_to_show = [c for c in cols_to_show if c in df_filtrado.columns]
    
    st.dataframe(
        df_filtrado[cols_to_show],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Prediccion_Estadia_Dias": st.column_config.NumberColumn(
                "Días Estimados (ML)",
                help="Predicción en vivo basada en sus variables actuales.",
                format="%d días",
            ),
            "Dias_Estadia": st.column_config.NumberColumn(
                "Días Reales Llevados",
                help="Días reales en el refugio.",
                format="%d días"
            ),
            "ID_Ingreso": "ID",
            "Adoptado": "Adoptado"
        }
    )

# ── 2. Edición de Registros ───────────────────────────────────────────
st.markdown("<div class='pae-divider'></div>", unsafe_allow_html=True)
st.markdown("### Actualización de Expediente")
st.markdown("<p style='color:#64748B; font-size:0.9rem;'>Modifica las variables de un animal para actualizar el registro y observar cómo cambia la predicción del modelo ML.</p>", unsafe_allow_html=True)

if not df_filtrado.empty:
    # Selector de Animal
    opciones = df_filtrado['ID_Ingreso'] + " - " + df_filtrado['Nombre']
    seleccion = st.selectbox("Selecciona un animal de la tabla superior para actualizar:", opciones.tolist())
    
    id_seleccionado = seleccion.split(" - ")[0]
    animal = df_filtrado[df_filtrado['ID_Ingreso'] == id_seleccionado].iloc[0]
    
    with st.form("form_actualizacion"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Datos Generales")
            opciones_salud = ["Excelente", "Bueno", "Regular", "En Tratamiento"]
            idx_salud = opciones_salud.index(animal['Estado_Salud']) if animal['Estado_Salud'] in opciones_salud else 0
            nuevo_estado_salud = st.selectbox("Estado de Salud", opciones_salud, index=idx_salud)
            
            opciones_esterilizado = ["Si", "No"]
            idx_est = opciones_esterilizado.index(animal['Esterilizado']) if animal['Esterilizado'] in opciones_esterilizado else 0
            nuevo_esterilizado = st.selectbox("¿Esterilizado?", opciones_esterilizado, index=idx_est)
            
            nuevo_peso = st.number_input("Peso (Kg)", min_value=0.5, max_value=80.0, value=float(animal['Peso_Kg']), step=0.5)
            
            es_adoptado_actual = bool(animal['Adoptado'])
            nuevo_adoptado = st.checkbox("Animal fue Adoptado", value=es_adoptado_actual)

        with col2:
            st.markdown("#### Comportamiento")
            opciones_soc = ["Alto", "Medio", "Bajo"]
            idx_soc = opciones_soc.index(animal['Nivel_Sociabilidad']) if animal['Nivel_Sociabilidad'] in opciones_soc else 0
            nuevo_sociabilidad = st.selectbox("Nivel de Sociabilidad", opciones_soc, index=idx_soc)
            
            nueva_edad = st.number_input("Edad (Meses)", min_value=1, max_value=240, value=int(animal['Edad_Meses']))
            
            nuevos_dias = st.number_input("Días Llevados Reales", min_value=0, max_value=3000, value=int(animal['Dias_Estadia']))
            
        with col3:
            st.markdown("#### Impacto de Visibilidad")
            nuevo_pub = st.slider("Publicaciones", min_value=1, max_value=15, value=int(animal['Publicaciones']))
            nuevo_visitas = st.number_input("Visitas Recibidas", min_value=0, max_value=20, value=int(animal['Visitas_Recibidas']))
            nuevo_interacciones = st.number_input("Interacciones RRSS", min_value=0, max_value=1000, value=int(animal['Interacciones_RRSS']))
            nuevo_costo = st.number_input("Costo Mantenimiento ($)", min_value=0.0, value=float(animal['Costos_Mantenimiento']), step=1.0)
            
        st.markdown("<br>", unsafe_allow_html=True)
        submitted_update = st.form_submit_button("Guardar Cambios y Recalcular Predicción", type="primary", use_container_width=True)
        
        if submitted_update:
            updated_data = {
                'Estado_Salud': nuevo_estado_salud,
                'Esterilizado': nuevo_esterilizado,
                'Peso_Kg': nuevo_peso,
                'Nivel_Sociabilidad': nuevo_sociabilidad,
                'Edad_Meses': nueva_edad,
                'Publicaciones': nuevo_pub,
                'Visitas_Recibidas': nuevo_visitas,
                'Interacciones_RRSS': nuevo_interacciones,
                'Costos_Mantenimiento': nuevo_costo,
                'Dias_Estadia': nuevos_dias,
                'Adoptado': nuevo_adoptado
            }
            success = update_animal(id_seleccionado, updated_data)
            if success:
                # Recalcular la IA en vivo para mostrar en el popup
                nueva_prediccion = "Error"
                if ct and model:
                    try:
                        input_dict = {
                            'Especie': [animal['Especie']],
                            'Raza': [animal['Raza']],
                            'Edad_Meses': [nueva_edad],
                            'Peso_Kg': [nuevo_peso],
                            'Tamano': [animal['Tamano']],
                            'Estado_Salud': [nuevo_estado_salud],
                            'Nivel_Sociabilidad': [nuevo_sociabilidad],
                            'Esterilizado': [nuevo_esterilizado],
                            'Publicaciones': [nuevo_pub],
                            'Interacciones_RRSS': [nuevo_interacciones],
                            'Visitas_Recibidas': [nuevo_visitas],
                            'Costos_Mantenimiento': [nuevo_costo]
                        }
                        temp_df = pd.DataFrame(input_dict)
                        X_temp = ct.transform(temp_df)
                        p = model.predict(X_temp)[0]
                        nueva_prediccion = max(3, int(round(p)))
                    except:
                        pass
                
                show_update_dialog(animal['Nombre'], id_seleccionado, nueva_prediccion, nuevo_costo, nuevo_estado_salud, nuevo_sociabilidad)
            else:
                st.error("Hubo un error al intentar actualizar el registro.")
else:
    st.warning("No hay registros que coincidan con los filtros para poder editar.")
