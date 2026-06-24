"""
PAE Design System — CSS tokens y estilos globales.
Inyectado una sola vez desde cada página con inject_global_styles().
"""

# Paleta de colores del sistema PAE
COLORS = {
    "primary":        "#1D9E75",   # Verde teal — acción principal
    "primary_light":  "#E1F5EE",   # Fondo sutil en badges de éxito
    "primary_dark":   "#0F6E56",   # Hover / énfasis
    "amber":          "#BA7517",   # Advertencia
    "amber_light":    "#FAEEDA",
    "red":            "#A32D2D",   # Alerta crítica
    "red_light":      "#FCEBEB",
    "blue":           "#185FA5",   # Informativo
    "blue_light":     "#E6F1FB",
    "text_muted":     "#6B7280",
    "border":         "rgba(0,0,0,0.08)",
    "surface":        "#F9FAFB",
    "surface_card":   "#FFFFFF",
}

GLOBAL_CSS = """
<style>
/* ── Reset de elementos nativos de Streamlit ─────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1100px !important;
}

/* ── Tipografía base ─────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── Sidebar premium ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0D1117 !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    color: #E6EDF3 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] p {
    color: #8B949E !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stSidebar"] hr {
    border-color: #21262D !important;
}
/* Logo en sidebar */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0 20px;
    border-bottom: 1px solid #21262D;
    margin-bottom: 20px;
}
.sidebar-logo-dot {
    width: 32px; height: 32px;
    border-radius: 8px;
    background: #1D9E75;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}
.sidebar-logo-text {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #E6EDF3 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}
.sidebar-logo-sub {
    font-size: 11px !important;
    color: #8B949E !important;
}

/* ── KPI Cards ───────────────────────────────────────────────────── */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 12px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, #1D9E75);
    border-radius: 12px 12px 0 0;
}
.kpi-eyebrow {
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #6B7280;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 32px;
    font-weight: 600;
    color: #0D1117;
    line-height: 1;
    margin-bottom: 6px;
}
.kpi-delta {
    font-size: 12px;
    color: #6B7280;
    display: flex;
    align-items: center;
    gap: 4px;
}
.delta-pos { color: #0F6E56; font-weight: 500; }
.delta-neg { color: #A32D2D; font-weight: 500; }

/* ── Section headers ─────────────────────────────────────────────── */
.section-eyebrow {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #1D9E75;
    margin-bottom: 4px;
}
.section-title {
    font-size: 20px;
    font-weight: 600;
    color: #0D1117;
    margin-bottom: 2px;
}
.section-sub {
    font-size: 13px;
    color: #6B7280;
    margin-bottom: 20px;
}

/* ── Alert badges ────────────────────────────────────────────────── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.badge-red    { background: #FCEBEB; color: #791F1F; }
.badge-amber  { background: #FAEEDA; color: #633806; }
.badge-green  { background: #E1F5EE; color: #085041; }
.badge-blue   { background: #E6F1FB; color: #0C447C; }

/* ── Alert cards en dashboard ────────────────────────────────────── */
.alert-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    border-radius: 10px;
    border: 1px solid rgba(0,0,0,0.06);
    margin-bottom: 8px;
    background: #FFFFFF;
}
.alert-row:last-child { margin-bottom: 0; }
.alert-name { font-size: 14px; font-weight: 500; color: #0D1117; }
.alert-meta { font-size: 12px; color: #6B7280; margin-top: 2px; }
.alert-days { font-size: 22px; font-weight: 700; min-width: 52px; text-align: right; }
.alert-days-red   { color: #A32D2D; }
.alert-days-amber { color: #BA7517; }
.alert-days-green { color: #0F6E56; }

/* ── Resultado del predictor ─────────────────────────────────────── */
.predictor-result {
    background: #0D1117;
    border-radius: 16px;
    padding: 28px 28px 24px;
    color: #E6EDF3;
}
.predictor-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8B949E;
    margin-bottom: 10px;
}
.predictor-number {
    font-size: 72px;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1;
    letter-spacing: -2px;
}
.predictor-unit {
    font-size: 15px;
    color: #8B949E;
    margin-top: 6px;
    margin-bottom: 20px;
}
.predictor-status {
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 13px;
    line-height: 1.6;
}
.status-critical { background: rgba(163,45,45,0.2); color: #F4A4A4; border: 1px solid rgba(163,45,45,0.3); }
.status-warning  { background: rgba(186,117,23,0.2); color: #F5C97A; border: 1px solid rgba(186,117,23,0.3); }
.status-ok       { background: rgba(29,158,117,0.2); color: #6DD9B8; border: 1px solid rgba(29,158,117,0.3); }

/* ── Formulario del predictor ────────────────────────────────────── */
[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 16px;
    padding: 24px !important;
}
.stSelectbox label, .stNumberInput label {
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #6B7280 !important;
}
[data-testid="stFormSubmitButton"] button {
    background: #1D9E75 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 12px 28px !important;
    width: 100%;
    transition: background 0.15s ease;
}
[data-testid="stFormSubmitButton"] button:hover {
    background: #0F6E56 !important;
}

/* ── Plotly charts ───────────────────────────────────────────────── */
.js-plotly-plot .plotly { border-radius: 12px; }

/* ── Tabs de navegación interna ──────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #F3F4F6;
    padding: 4px;
    border-radius: 10px;
    border: none;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    font-size: 13px;
    font-weight: 500;
    color: #6B7280;
    background: transparent;
    padding: 7px 18px;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #0D1117 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"]    { display: none; }

/* ── Divider personalizado ───────────────────────────────────────── */
.pae-divider {
    height: 1px;
    background: rgba(0,0,0,0.06);
    margin: 24px 0;
}

/* ── Dataframe / tabla ───────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(0,0,0,0.07) !important;
}
</style>
"""


def inject_global_styles() -> None:
    """Inyecta el sistema de diseño PAE en la página actual."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def kpi_card(eyebrow: str, value: str, delta: str = "", delta_positive: bool = True,
             accent: str = "#1D9E75") -> str:
    """Retorna HTML de una KPI card lista para st.markdown()."""
    delta_class = "delta-pos" if delta_positive else "delta-neg"
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
        status_icon  = "⚠"
        status_text  = ("Caso de larga estadía. Activar protocolo de marketing intensivo "
                        "y evaluar hogar foster de inmediato.")
    elif days < 15:
        status_class = "status-ok"
        status_icon  = "✓"
        status_text  = "Alta probabilidad de adopción temprana. Preparar documentación de salida."
    else:
        status_class = "status-warning"
        status_icon  = "◌"
        status_text  = "Estadía regular. Planificar mantenimiento estándar y reforzar visibilidad en redes."

    return f"""
    <div class="predictor-result">
        <div class="predictor-label">Predicción del modelo IA</div>
        <div class="predictor-number">{int(days)}</div>
        <div class="predictor-unit">días estimados en refugio</div>
        <div class="predictor-status {status_class}">
            <strong>{status_icon} Acción recomendada</strong><br>{status_text}
        </div>
    </div>"""
