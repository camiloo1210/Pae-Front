"""
Data Service — capa de acceso a datos históricos.

Patrón Repository: la UI nunca toca el CSV directamente.
Para cambiar la fuente (SQLite, PostgreSQL, API REST) solo
se modifica este módulo; las páginas no se tocan.
"""

from __future__ import annotations

import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
from datetime import date, timedelta
from typing import Optional

# ── Ruta al CSV (relativa a la raíz del proyecto) ──────────────────
_DATA_PATH = Path(__file__).parent.parent / "pae_adopciones_sintetico.csv"

# ── Columnas esperadas en el CSV ────────────────────────────────────
REQUIRED_COLUMNS = {
    "Nombre", "Especie", "Edad_Meses", "Peso_Kg", "Tamano",
    "Estado_Salud", "Nivel_Sociabilidad", "Esterilizado",
    "Publicaciones", "Interacciones_RRSS",
    "Fecha_Ingreso", "Dias_Estadia", "Adoptado",
}


def _generate_synthetic_data() -> pd.DataFrame:
    """
    Genera datos sintéticos realistas cuando no existe el CSV real.
    SOLO para desarrollo — reemplazar con datos reales en producción.
    """
    rng = np.random.default_rng(42)
    n = 200

    nombres_perros = ["Max","Rex","Luna","Kira","Bruno","Toto","Coco","Lola",
                      "Zeus","Nala","Rocky","Mia","Thor","Bella","Duke"]
    nombres_gatos  = ["Michi","Salem","Cleo","Simba","Nube","Canela","Oreo",
                      "Sombra","Tigre","Perla","Gris","Cata","Felix","Mia"]

    especies = rng.choice(["Perro","Gato"], size=n, p=[0.6, 0.4])
    nombres  = [
        rng.choice(nombres_perros) if e == "Perro" else rng.choice(nombres_gatos)
        for e in especies
    ]

    tamanos = np.where(
        especies == "Gato",
        rng.choice(["Pequeño","Mediano"], size=n),
        rng.choice(["Pequeño","Mediano","Grande"], size=n, p=[0.3,0.45,0.25])
    )

    salud = rng.choice(
        ["Excelente","Bueno","Regular","En Tratamiento"], size=n, p=[0.3,0.4,0.2,0.1]
    )
    sociabilidad = rng.choice(["Alto","Medio","Bajo"], size=n, p=[0.5,0.35,0.15])
    esterilizado = rng.choice(["Si","No"], size=n, p=[0.65,0.35])

    base_dias = 20
    dias = (
        base_dias
        + np.where(especies == "Perro", 5, -5)
        + np.where(tamanos == "Grande", 15, np.where(tamanos == "Mediano", 5, -5))
        + np.where(salud == "En Tratamiento", 20, np.where(salud == "Regular", 8, 0))
        + np.where(sociabilidad == "Bajo", 12, np.where(sociabilidad == "Medio", 4, 0))
        + np.where(esterilizado == "Si", -5, 5)
        + rng.normal(0, 8, size=n)
    ).clip(3, 90).astype(int)

    hoy = date.today()
    fechas_ingreso = [hoy - timedelta(days=int(d) + rng.integers(0,30)) for d in dias]

    return pd.DataFrame({
        "Nombre":             nombres,
        "Especie":            especies,
        "Edad_Meses":         rng.integers(2, 96, size=n),
        "Peso_Kg":            rng.uniform(1.5, 35, size=n).round(1),
        "Tamano":             tamanos,
        "Estado_Salud":       salud,
        "Nivel_Sociabilidad": sociabilidad,
        "Esterilizado":       esterilizado,
        "Publicaciones":      rng.integers(1, 12, size=n),
        "Interacciones_RRSS": rng.integers(50, 800, size=n),
        "Fecha_Ingreso":      fechas_ingreso,
        "Dias_Estadia":       dias,
        "Adoptado":           rng.choice([True, False], size=n, p=[0.72, 0.28]),
    })


@st.cache_data(ttl=300)
def load_historical_data() -> pd.DataFrame:
    """
    Carga y valida los datos históricos.
    Adapta el CSV original en memoria para compatibilidad con la UI.
    """
    if not _DATA_PATH.exists():
        st.toast("⚠️ CSV no encontrado — usando datos de demostración", icon="⚠️")
        return _generate_synthetic_data()

    df = pd.read_csv(_DATA_PATH)

    # Adaptar CSV original a esquema requerido
    if "Tiempo_Refugio_Dias" in df.columns:
        df = df.rename(columns={"Tiempo_Refugio_Dias": "Dias_Estadia"})
    
    if "Nombre" not in df.columns:
        rng = np.random.default_rng(42)
        nombres_perros = ["Max","Rex","Luna","Kira","Bruno","Toto","Coco","Lola","Zeus","Nala","Rocky","Mia","Thor","Bella","Duke"]
        nombres_gatos  = ["Michi","Salem","Cleo","Simba","Nube","Canela","Oreo","Sombra","Tigre","Perla","Gris","Cata","Felix","Mia"]
        df["Nombre"] = [
            rng.choice(nombres_perros) if e == "Perro" else rng.choice(nombres_gatos)
            for e in df["Especie"]
        ]
        
    if "Adoptado" not in df.columns:
        rng = np.random.default_rng(42)
        df["Adoptado"] = rng.choice([True, False], size=len(df), p=[0.72, 0.28])
        
    if "Fecha_Ingreso" not in df.columns:
        rng = np.random.default_rng(42)
        hoy = date.today()
        fechas = []
        for i, row in df.iterrows():
            d = row["Dias_Estadia"]
            if pd.isna(d): d = 0
            is_adopted = row["Adoptado"]
            days_ago = int(d) + (int(rng.integers(0, 30)) if is_adopted else 0)
            fechas.append(hoy - timedelta(days=days_ago))
        df["Fecha_Ingreso"] = fechas
        
    df["Fecha_Ingreso"] = pd.to_datetime(df["Fecha_Ingreso"])

    # Validación de esquema
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"El CSV está incompleto tras adaptación. Columnas faltantes: {missing}. "
        )

    # Limpieza defensiva
    df["Dias_Estadia"] = pd.to_numeric(df["Dias_Estadia"], errors="coerce")
    df = df.dropna(subset=["Dias_Estadia", "Especie"])
    df["Adoptado"] = df["Adoptado"].astype(bool)

    return df


def get_kpi_summary(df: pd.DataFrame) -> dict:
    """KPIs operacionales para el header del dashboard."""
    hoy = date.today()
    activos = df[~df["Adoptado"]]
    adoptados_mes = df[
        df["Adoptado"] &
        (pd.to_datetime(df["Fecha_Ingreso"]).dt.month == hoy.month)
    ]
    larga_estadia = activos[activos["Dias_Estadia"] > 45]

    return {
        "total_activos":      len(activos),
        "adoptados_mes":      len(adoptados_mes),
        "estadia_promedio":   round(activos["Dias_Estadia"].mean(), 1),
        "larga_estadia":      len(larga_estadia),
        "tasa_adopcion":      round(df["Adoptado"].mean() * 100, 1),
    }


def get_priority_alerts(df: pd.DataFrame, limit: int = 6) -> pd.DataFrame:
    """Animales activos ordenados por urgencia (mayor estadía primero)."""
    activos = df[~df["Adoptado"]].copy()
    return (
        activos
        .sort_values("Dias_Estadia", ascending=False)
        .head(limit)
        [["Nombre","Especie","Tamano","Estado_Salud","Nivel_Sociabilidad","Dias_Estadia"]]
        .reset_index(drop=True)
    )


def get_stay_by_species_size(df: pd.DataFrame) -> pd.DataFrame:
    """Estadía promedio agrupada por especie y tamaño para el gráfico de barras."""
    return (
        df.groupby(["Especie","Tamano"])["Dias_Estadia"]
        .mean()
        .round(1)
        .reset_index()
        .rename(columns={"Dias_Estadia": "Promedio_Dias"})
        .sort_values("Promedio_Dias", ascending=True)
    )


def get_monthly_adoptions(df: pd.DataFrame) -> pd.DataFrame:
    """Adopciones por mes para el gráfico de tendencia."""
    adoptados = df[df["Adoptado"]].copy()
    adoptados["Mes"] = pd.to_datetime(adoptados["Fecha_Ingreso"]).dt.to_period("M")
    return (
        adoptados.groupby("Mes")
        .size()
        .reset_index(name="Adopciones")
        .tail(12)  # Últimos 12 meses
    )
