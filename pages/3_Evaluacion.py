"""
📊 Evaluación — Métricas del Modelo de Regresión.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import sys
from pathlib import Path
from PIL import Image
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).parent.parent))

from ui.styles import inject_global_styles, section_header, kpi_card, COLORS

# ── Config ────────────────────────────────────────────────────────────
logo_img = Image.open("public/image 8.png")
st.set_page_config(
    page_title="PAE · Evaluación",
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
    st.page_link("pages/2_Predictor.py",   label="Predictor",     icon=":material/online_prediction:")
    st.page_link("pages/3_Evaluacion.py",  label="Evaluación",    icon=":material/query_stats:")
    st.page_link("pages/4_Registro.py",    label="Registro",      icon=":material/app_registration:")
    st.page_link("pages/5_Gestion.py",     label="Gestión",       icon=":material/manage_accounts:")
    st.divider()
    st.caption("Métricas de rendimiento y análisis explicativo del modelo de inteligencia artificial.")

# ── Header ────────────────────────────────────────────────────────────
st.markdown(section_header(
    eyebrow="Análisis de Rendimiento",
    title="Evaluación del Modelo",
    subtitle=(
        "Métricas de regresión (R², MAE, RMSE), calificación de características (feature importance) "
        "y matriz de correlación para entender cómo el modelo toma decisiones."
    ),
), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Carga de Datos y Modelos ─────────────────────────────────────────
@st.cache_resource
def load_models():
    try:
        ct = joblib.load('preprocesador_pae.pkl')
        reg = joblib.load('modelo_pae.pkl')
        return ct, reg
    except Exception as e:
        st.error(f"Error al cargar los modelos: {e}")
        return None, None

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('pae_adopciones_sintetico.csv')
        df = df.drop_duplicates()
        return df
    except Exception as e:
        st.error(f"Error al cargar el CSV: {e}")
        return pd.DataFrame()

ct, regressor = load_models()
dataset = load_data()

if ct is not None and regressor is not None and not dataset.empty:
    # Preparar datos para métricas
    y = dataset['Dias_Estadia'].values
    X = dataset.drop(columns=['Dias_Estadia', 'ID_Ingreso', 'Nombre', 'Adoptado', 'Fecha_Ingreso'], errors='ignore')
    
    # Evaluar estrictamente en el test set para igualar las métricas reales
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    X_test_procesado = ct.transform(X_test)
    y_pred = regressor.predict(X_test_procesado)
    
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # ── KPIs de Métricas ─────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(kpi_card(
            eyebrow="R² (Coef. Determinación)",
            value=f"{r2:.3f}",
            delta="Ajuste del modelo",
            delta_positive=True,
            accent=COLORS["blue"]
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card(
            eyebrow="MAE (Error Absoluto Medio)",
            value=f"{mae:.2f} días",
            delta="Error promedio en predicción",
            delta_positive=False,
            accent=COLORS["amber"]
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card(
            eyebrow="RMSE (Raíz Error Cuadrático)",
            value=f"{rmse:.2f} días",
            delta="Penalización de errores grandes",
            delta_positive=False,
            accent=COLORS["red"]
        ), unsafe_allow_html=True)

    # ── Resumen de Métricas ──────────────────────────────────────────
    r2_pct = r2 * 100
    if r2 >= 0.90:
        r2_interpretacion = "excelente"
    elif r2 >= 0.75:
        r2_interpretacion = "bueno"
    elif r2 >= 0.50:
        r2_interpretacion = "moderado"
    else:
        r2_interpretacion = "bajo"

    with st.expander("Interpretación de las métricas"):
        st.markdown(f"""
        El modelo de **Regresión Lineal** fue entrenado con **{len(X_train):,}** registros
        y evaluado sobre **{len(X_test):,}** registros de prueba (partición 80/20).
        El coeficiente de determinación **R² = {r2:.3f}** indica un ajuste **{r2_interpretacion}**:
        el modelo explica el **{r2_pct:.1f}%** de la variabilidad en los días de estadía.
        En promedio, la predicción se desvía **{mae:.2f} días** del valor real (MAE),
        mientras que el RMSE de **{rmse:.2f} días** penaliza los errores grandes,
        lo que sugiere que el modelo mantiene una precisión consistente sin valores atípicos extremos.
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0F172A;font-weight:600;'>Ajustes de Visualización Globales</h4>", unsafe_allow_html=True)
    
    feature_names = ct.get_feature_names_out()
    # Clean feature names (remove 'encoder__' prefix if exists)
    clean_names = [f.replace('encoder__', '').replace('remainder__', '') for f in feature_names]
    
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        agrupar_razas = st.toggle("Agrupar razas en una sola variable", value=False, help="Consolida todas las razas individuales en un solo promedio para una visualización más limpia en ambos gráficos.")
        
    with col_ctrl2:
        mostrar_base = st.toggle("Mostrar categorías base", value=False, help="Muestra las categorías omitidas por One-Hot Encoding (que sirven como punto de referencia con impacto 0).")
        
    if agrupar_razas:
        num_razas = sum(1 for f in clean_names if f.startswith('Raza_'))
        total_features = len(clean_names) - num_razas + 1 if num_razas > 0 else len(clean_names)
    else:
        total_features = len(clean_names)
        
    top_n = st.slider(
        "Cantidad de características a mostrar (más relevantes)",
        min_value=3, max_value=total_features, value=total_features
    )
        
    st.markdown("<div class='pae-divider'></div>", unsafe_allow_html=True)
    
    # ── Calificación de Features (Feature Importance) ───────────────
    st.markdown("<h3 style='color:#0F172A;font-weight:700;'>Calificación de Features (Pesos del Modelo)</h3>", unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Muestra qué variables tienen el mayor impacto en aumentar o disminuir el tiempo de estadía estimado por el modelo.</p>', unsafe_allow_html=True)
    
    coefs = regressor.coef_
    
    importance_df = pd.DataFrame({
        'Característica': clean_names,
        'Impacto en Días': coefs,
        'Magnitud Absoluta': np.abs(coefs)
    })
    
    if agrupar_razas:
        mask_raza = importance_df['Característica'].str.startswith('Raza_')
        if mask_raza.any():
            raza_mean = importance_df.loc[mask_raza, 'Impacto en Días'].mean()
            importance_df = importance_df[~mask_raza]
            importance_df = pd.concat([importance_df, pd.DataFrame([{
                'Característica': 'Raza (Promedio)',
                'Impacto en Días': raza_mean,
                'Magnitud Absoluta': abs(raza_mean)
            }])], ignore_index=True)
    
    importance_df = importance_df.sort_values('Magnitud Absoluta', ascending=True)
    importance_df = importance_df.tail(top_n)
    
    # Inyectar las variables base (0.0) si el usuario lo solicita
    if mostrar_base:
        try:
            ohe = ct.transformers_[0][1]
            ohe_cols = ct.transformers_[0][2]
            baselines = []
            for col, cats in zip(ohe_cols, ohe.categories_):
                baselines.append({
                    'Característica': f"{col}_{cats[0]} (Base)",
                    'Impacto en Días': 0.0,
                    'Magnitud Absoluta': 0.0
                })
            importance_df = pd.concat([importance_df, pd.DataFrame(baselines)], ignore_index=True)
            # Reordenar para que las base queden juntas en el gráfico
            importance_df = importance_df.sort_values('Magnitud Absoluta', ascending=True)
            total_features += len(baselines) # Actualizar altura del gráfico
        except Exception:
            pass
    
    # Colores: Verde si reduce días (negativo), Rojo si aumenta (positivo), Gris si es Base (0)
    cond_color = [
        importance_df['Impacto en Días'] > 0,
        importance_df['Impacto en Días'] < 0
    ]
    choices_color = [COLORS["red"], COLORS["green"]]
    importance_df['Color'] = np.select(cond_color, choices_color, default="#94A3B8") # Gris para el 0.0
    
    fig_imp = px.bar(
        importance_df, 
        x='Impacto en Días', 
        y='Característica',
        orientation='h',
        color='Color',
        color_discrete_map="identity",
        text_auto='.2f'
    )
    fig_imp.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Fira Sans",
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Días Agregados / Reducidos",
        yaxis_title="",
        showlegend=False,
        height=max(400, total_features * 32)
    )
    st.plotly_chart(fig_imp, use_container_width=True)
    
    # ── Resumen de Feature Importance ────────────────────────────────
    top3_pos = importance_df[importance_df['Impacto en Días'] > 0].nlargest(3, 'Impacto en Días')
    top3_neg = importance_df[importance_df['Impacto en Días'] < 0].nsmallest(3, 'Impacto en Días')
    
    pos_items = ", ".join([f"**{row['Característica']}** (+{row['Impacto en Días']:.1f} días)" for _, row in top3_pos.iterrows()])
    neg_items = ", ".join([f"**{row['Característica']}** ({row['Impacto en Días']:.1f} días)" for _, row in top3_neg.iterrows()])
    
    with st.expander("Interpretación de la calificación de features"):
        st.markdown(f"""
        El modelo utiliza **{len(ct.get_feature_names_out())}** variables procesadas mediante codificación One-Hot
        (`drop='first'`, donde la primera categoría alfabética actúa como referencia/baseline).
        
        **Factores que más AUMENTAN la estadía:** {pos_items}.
        Esto significa que un animal con estas condiciones permanecerá significativamente más tiempo en el refugio.
        
        **Factores que más REDUCEN la estadía:** {neg_items}.
        Estos atributos están asociados con adopciones más rápidas según los datos históricos.
        """)
    
    st.markdown("<div class='pae-divider'></div>", unsafe_allow_html=True)
    
    # ── Matriz de Correlación ────────────────────────────────────────
    st.markdown("<h3 style='color:#0F172A;font-weight:700;'>Matriz de Correlación</h3>", unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Analiza cómo se relacionan linealmente TODAS las variables (incluyendo las categóricas procesadas) con los días de estadía.</p>', unsafe_allow_html=True)
    
    # Para igualar tu Colab, creamos el dataframe procesado completo
    X_procesado = ct.transform(X)
    df_procesado = pd.DataFrame(X_procesado, columns=feature_names)
    df_procesado['Dias_Estadia'] = y
    
    # Extraemos solo las correlaciones con Dias_Estadia
    corr_target = df_procesado.corr()[['Dias_Estadia']].copy()
    
    if agrupar_razas:
        mask_corr_raza = corr_target.index.str.contains('encoder__Raza_')
        if mask_corr_raza.any():
            raza_corr_mean = corr_target.loc[mask_corr_raza, 'Dias_Estadia'].mean()
            corr_target = corr_target[~mask_corr_raza]
            corr_target.loc['Raza (Promedio)'] = raza_corr_mean
    
    corr_target = corr_target.sort_values(by='Dias_Estadia', ascending=False)
    
    # Limpiar nombres largos de encoder__ y remainder__
    corr_target.index = corr_target.index.str.replace('encoder__', '').str.replace('remainder__', '')
    
    # Filtrar para mostrar solo las variables que entraron en el Top N del slider
    selected_features = importance_df['Característica'].tolist()
    
    # Inyectar las variables Base en la matriz de correlación con valor 0.0 si fueron habilitadas
    for feat in selected_features:
        if feat.endswith('(Base)') and feat not in corr_target.index:
            corr_target.loc[feat] = 0.0
            
    valid_features = [f for f in selected_features if f in corr_target.index]
    valid_features.append('Dias_Estadia') # Mantener siempre el target
    
    corr_target = corr_target.loc[valid_features]
    corr_target = corr_target.sort_values(by='Dias_Estadia', ascending=False)
    
    # Heatmap
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr_target.values,
        x=["Dias_Estadia"],
        y=corr_target.index,
        text=np.round(corr_target.values, 2),
        texttemplate="%{text}",
        colorscale="RdBu_r",
        zmin=-1, zmax=1
    ))
    
    fig_corr.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Fira Sans",
        margin=dict(l=20, r=20, t=20, b=20),
        height=max(500, len(corr_target) * 35),
        xaxis_title="",
        yaxis_title=""
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # ── Resumen de Correlación ───────────────────────────────────────
    corr_sin_target = corr_target.drop('Dias_Estadia', errors='ignore')
    top_pos_corr = corr_sin_target[corr_sin_target['Dias_Estadia'] > 0].nlargest(3, 'Dias_Estadia')
    top_neg_corr = corr_sin_target[corr_sin_target['Dias_Estadia'] < 0].nsmallest(3, 'Dias_Estadia')
    
    pos_corr_items = ", ".join([f"**{idx}** ({row['Dias_Estadia']:.2f})" for idx, row in top_pos_corr.iterrows()])
    neg_corr_items = ", ".join([f"**{idx}** ({row['Dias_Estadia']:.2f})" for idx, row in top_neg_corr.iterrows()])
    
    with st.expander("Interpretación de la matriz de correlación"):
        st.markdown(f"""
        La matriz muestra la correlación de Pearson de cada variable con **Dias_Estadia**.
        Valores cercanos a **+1** indican que al aumentar esa variable, los días de estadía también aumentan;
        valores cercanos a **-1** indican una relación inversa (al aumentar la variable, los días disminuyen).
        
        **Mayor correlación positiva (aumentan estadía):** {pos_corr_items}.
        
        **Mayor correlación negativa (reducen estadía):** {neg_corr_items}.
        
        *Nota: Correlación no implica causalidad. Estas relaciones reflejan patrones estadísticos
        observados en los datos históricos del refugio, no necesariamente una relación de causa-efecto directa.*
        """)

else:
    st.info("No se pudieron cargar los modelos o los datos. Asegúrate de ejecutar `entrenar.py` primero.")
