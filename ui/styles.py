"""
PAE Design System — CSS tokens y estilos globales.
Inyectado una sola vez desde cada página con inject_global_styles().
"""

# Paleta de colores Premium Tier S+
COLORS = {
    "primary":        "#0F766E",   # Teal 700 — Premium dark teal
    "primary_light":  "#F0FDFA",   # Teal 50
    "primary_dark":   "#115E59",   # Teal 800
    "amber":          "#D97706",   # Amber 600
    "amber_light":    "#FEF3C7",   # Amber 50
    "red":            "#DC2626",   # Red 600
    "red_light":      "#FEF2F2",   # Red 50
    "blue":           "#2563EB",   # Blue 600
    "blue_light":     "#EFF6FF",   # Blue 50
    "text_dark":      "#0F172A",   # Slate 900
    "text_muted":     "#64748B",   # Slate 500
    "border":         "rgba(15, 23, 42, 0.08)",
    "surface":        "#F8FAFC",   # Slate 50
    "surface_card":   "#FFFFFF",
}

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');

/* ── Reset de elementos nativos de Streamlit ─────────────────────── */
#MainMenu, footer { visibility: hidden; }
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1100px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #F8FAFC;
}

/* ── Tipografía base ─────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0F172A;
}

/* ── Sidebar premium ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0F172A !important; /* Slate 900 */
    border-right: 1px solid #1E293B !important;
}

[data-testid="stSidebar"] .stMarkdown, 
[data-testid="stSidebar"] .stText,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stIconMaterial"] {
    color: #F8FAFC !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] p {
    color: #94A3B8 !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}
[data-testid="stSidebar"] hr {
    border-color: #1E293B !important;
}

/* Fix sidebar input backgrounds */
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] > div {
    background-color: #1E293B !important;
    border-color: #334155 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #F8FAFC !important;
}
[data-testid="stSidebar"] [data-baseweb="input"] input {
    background-color: transparent !important;
    color: #F8FAFC !important;
}
[data-testid="stSidebar"] [data-baseweb="input"] input::placeholder {
    color: #64748B !important;
}

/* Style the multi-select tags */
[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background-color: #0F766E !important;
    border: 1px solid #115E59 !important;
    color: #F0FDFA !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] span[data-baseweb="tag"] span {
    color: #F0FDFA !important;
}
[data-testid="stSidebar"] span[data-baseweb="tag"] svg {
    fill: #F0FDFA !important;
}
/* Logo en sidebar */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0 24px;
    border-bottom: 1px solid #1E293B;
    margin-bottom: 24px;
}
.sidebar-logo-dot {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, #0D9488, #0F766E);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    box-shadow: 0 4px 6px -1px rgba(15, 118, 110, 0.3);
}
.sidebar-logo-text {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
    letter-spacing: -0.02em !important;
    text-transform: none !important;
}
.sidebar-logo-sub {
    font-size: 11px !important;
    color: #94A3B8 !important;
    font-weight: 500;
}

/* ── KPI Cards ───────────────────────────────────────────────────── */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid rgba(15,23,42,0.06);
    border-radius: 16px;
    padding: 24px;
    position: relative;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: var(--accent, #0F766E);
    border-radius: 16px 16px 0 0;
}
.kpi-eyebrow {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748B;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Fira Code', monospace;
    font-size: 36px;
    font-weight: 600;
    color: #0F172A;
    line-height: 1;
    margin-bottom: 8px;
    letter-spacing: -0.03em;
}
.kpi-delta {
    font-size: 13px;
    color: #64748B;
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 500;
}
.delta-pos { color: #0F766E; font-weight: 600; background: #F0FDFA; padding: 2px 8px; border-radius: 12px; }
.delta-neg { color: #DC2626; font-weight: 600; background: #FEF2F2; padding: 2px 8px; border-radius: 12px; }

/* ── Section headers ─────────────────────────────────────────────── */
.section-eyebrow {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #0F766E;
    margin-bottom: 6px;
}
.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 4px;
    letter-spacing: -0.02em;
}
.section-sub {
    font-size: 14px;
    color: #64748B;
    margin-bottom: 24px;
    line-height: 1.5;
}

/* ── Alert badges ────────────────────────────────────────────────── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.badge-red    { background: #FEF2F2; color: #991B1B; border: 1px solid #FECACA; }
.badge-amber  { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
.badge-green  { background: #F0FDFA; color: #115E59; border: 1px solid #A7F3D0; }
.badge-blue   { background: #EFF6FF; color: #1E40AF; border: 1px solid #BFDBFE; }

/* ── Alert cards en dashboard ────────────────────────────────────── */
.alert-row {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    border-radius: 12px;
    border: 1px solid rgba(15,23,42,0.06);
    margin-bottom: 10px;
    background: #FFFFFF;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: border-color 0.2s ease;
}
.alert-row:hover {
    border-color: rgba(15,23,42,0.15);
}
.alert-name { font-size: 15px; font-weight: 600; color: #0F172A; }
.alert-meta { font-size: 13px; color: #64748B; margin-top: 4px; }
.alert-days { font-family: 'Fira Code', monospace; font-size: 24px; font-weight: 700; min-width: 60px; text-align: right; letter-spacing: -0.05em; }
.alert-days-red   { color: #DC2626; }
.alert-days-amber { color: #D97706; }
.alert-days-green { color: #0F766E; }

/* ── Resultado del predictor ─────────────────────────────────────── */
.predictor-result {
    background: #0F172A;
    border-radius: 20px;
    padding: 32px;
    color: #F8FAFC;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
}
.predictor-label {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #94A3B8;
    margin-bottom: 12px;
}
.predictor-number {
    font-family: 'Fira Code', monospace;
    font-size: 84px;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1;
    letter-spacing: -0.04em;
}
.predictor-unit {
    font-size: 16px;
    font-weight: 500;
    color: #94A3B8;
    margin-top: 8px;
    margin-bottom: 24px;
}
.predictor-status {
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 14px;
    line-height: 1.6;
    font-weight: 500;
}
.status-critical { background: rgba(220, 38, 38, 0.15); color: #FCA5A5; border: 1px solid rgba(220, 38, 38, 0.3); }
.status-warning  { background: rgba(217, 119, 6, 0.15); color: #FCD34D; border: 1px solid rgba(217, 119, 6, 0.3); }
.status-ok       { background: rgba(15, 118, 110, 0.15); color: #5EEAD4; border: 1px solid rgba(15, 118, 110, 0.3); }

/* ── Formulario del predictor ────────────────────────────────────── */
[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 20px;
    padding: 32px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
.stSelectbox label, .stNumberInput label {
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #475569 !important;
}
[data-testid="stFormSubmitButton"] button {
    background: #0F766E !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 14px 28px !important;
    width: 100%;
    transition: all 0.2s ease;
    box-shadow: 0 4px 6px -1px rgba(15, 118, 110, 0.3);
}
[data-testid="stFormSubmitButton"] button:hover {
    background: #115E59 !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 8px -1px rgba(15, 118, 110, 0.4);
}

/* ── Tabs de navegación interna ──────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #F1F5F9;
    padding: 6px;
    border-radius: 12px;
    border: none;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    color: #64748B;
    background: transparent;
    padding: 8px 20px;
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #0F172A;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #0F766E !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"]    { display: none; }

/* ── Divider personalizado ───────────────────────────────────────── */
.pae-divider {
    height: 1px;
    background: rgba(15,23,42,0.08);
    margin: 32px 0;
}

/* ── Dataframe / tabla ───────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(15,23,42,0.08) !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}
/* ── Landing Page (Inicio.py) ──────────────────────────────────────── */
.hero-title {
    font-size: 56px;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.1;
    letter-spacing: -0.04em;
    margin-bottom: 24px;
}
.hero-title span {
    color: #0F766E;
}
.hero-subtitle {
    font-size: 18px;
    color: #475569;
    line-height: 1.6;
    margin-bottom: 40px;
    max-width: 90%;
}
.rounded-img img {
    border-radius: 24px;
    box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.25);
    object-fit: cover;
}
.feature-card {
    background: #FFFFFF;
    border: 1px solid rgba(15,23,42,0.06);
    border-radius: 16px;
    padding: 32px;
    height: 100%;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
}
.feature-icon {
    font-size: 32px;
    color: #0F766E;
    margin-bottom: 20px;
    display: inline-block;
    padding: 12px;
    background: #F0FDFA;
    border-radius: 12px;
}
.feature-title {
    font-size: 18px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 12px;
}
.feature-text {
    font-size: 14px;
    color: #64748B;
    line-height: 1.6;
}
.stat-bar {
    display: flex;
    align-items: center;
    justify-content: space-around;
    background: #0F172A;
    border-radius: 24px;
    padding: 40px;
    margin: 64px 0;
    box-shadow: 0 20px 25px -5px rgba(15, 118, 110, 0.15);
}
.stat-item {
    text-align: center;
}
.stat-value {
    font-family: 'Fira Code', monospace;
    font-size: 48px;
    font-weight: 700;
    color: #5EEAD4;
    line-height: 1;
    margin-bottom: 8px;
}
.stat-label {
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #94A3B8;
}

</style>
"""


def inject_global_styles() -> None:
    """Inyecta el sistema de diseño PAE en la página actual."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def kpi_card(eyebrow: str, value: str, delta: str = "", delta_positive: bool = True,
             accent: str = "#0F766E") -> str:
    """Retorna HTML de una KPI card lista para st.markdown()."""
    delta_class = "delta-pos" if delta_positive else "delta-neg"
    # Usamos caracteres simples en vez de emojis. Podríamos inyectar SVG, pero un span limpio es muy profesional.
    delta_icon  = "↑" if delta_positive else "↓"
    delta_html  = f'<div class="kpi-delta"><span class="{delta_class}">{delta_icon} {delta}</span></div>' if delta else ""
    return f"""
    <div class="kpi-card" style="--accent:{accent}">
        <div class="kpi-eyebrow">{eyebrow}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>"""


def section_header(eyebrow: str, title: str, subtitle: str = "") -> str:
    sub = f'<div class="section-sub">{subtitle}</div>' if subtitle else ""
    return f"""
    <div class="section-eyebrow">{eyebrow}</div>
    <div class="section-title">{title}</div>
    {sub}"""


def badge(text: str, variant: str = "green") -> str:
    """variant: green | amber | red | blue"""
    return f'<span class="badge badge-{variant}">{text}</span>'


def predictor_result(days: int) -> str:
    if days > 45:
        status_class = "status-critical"
        status_text  = "Caso de larga estadía. Activar protocolo de marketing intensivo e evaluar hogar foster de inmediato."
    elif days < 15:
        status_class = "status-ok"
        status_text  = "Alta probabilidad de adopción temprana. Preparar documentación de salida."
    else:
        status_class = "status-warning"
        status_text  = "Estadía regular. Planificar mantenimiento estándar y reforzar visibilidad en redes."

    return f"""
    <div class="predictor-result">
        <div class="predictor-label">Predicción del modelo IA</div>
        <div class="predictor-number">{int(days)}</div>
        <div class="predictor-unit">días estimados en refugio</div>
        <div class="predictor-status {status_class}">
            <strong>Acción recomendada</strong><br>{status_text}
        </div>
    </div>"""
