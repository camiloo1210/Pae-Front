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
    "Nombre", "Especie", "Raza", "Edad_Meses", "Peso_Kg", "Tamano",
    "Estado_Salud", "Nivel_Sociabilidad", "Esterilizado",
    "Publicaciones", "Interacciones_RRSS", "Visitas_Recibidas",
    "Costos_Mantenimiento",
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

    razas_perros = ["Mestizo", "Labrador", "Poodle", "Bulldog", "Pastor Alemán"]
    razas_gatos = ["Mestizo", "Siamés", "Persa", "Angora"]
    razas = [
        rng.choice(razas_perros, p=[0.6, 0.1, 0.1, 0.1, 0.1]) if e == "Perro" else rng.choice(razas_gatos, p=[0.7, 0.1, 0.1, 0.1])
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

    visitas_recibidas = rng.integers(0, 15, size=n)

    base_dias = 20
    dias = (
        base_dias
        + np.where(especies == "Perro", 5, -5)
        + np.where(np.array(razas) == "Mestizo", 10, -5) # Mestizos tardan más
        + np.where(tamanos == "Grande", 15, np.where(tamanos == "Mediano", 5, -5))
        + np.where(salud == "En Tratamiento", 20, np.where(salud == "Regular", 8, 0))
        + np.where(sociabilidad == "Bajo", 12, np.where(sociabilidad == "Medio", 4, 0))
        + np.where(esterilizado == "Si", -5, 5)
        - visitas_recibidas * 2 # Más visitas reducen los días
        + rng.normal(0, 8, size=n)
    ).clip(3, 90).astype(int)

    costos_mantenimiento = (dias * rng.uniform(2.5, 5.0, size=n)).round(2)

    hoy = date.today()
    fechas_ingreso = [hoy - timedelta(days=int(d) + int(rng.integers(0,30))) for d in dias]

    return pd.DataFrame({
        "Nombre":             nombres,
        "Especie":            especies,
        "Raza":               razas,
        "Edad_Meses":         rng.integers(2, 96, size=n),
        "Peso_Kg":            rng.uniform(1.5, 35, size=n).round(1),
        "Tamano":             tamanos,
        "Estado_Salud":       salud,
        "Nivel_Sociabilidad": sociabilidad,
        "Esterilizado":       esterilizado,
        "Publicaciones":      rng.integers(1, 12, size=n),
        "Interacciones_RRSS": rng.integers(50, 800, size=n),
        "Visitas_Recibidas":  visitas_recibidas,
        "Costos_Mantenimiento": costos_mantenimiento,
        "Fecha_Ingreso":      fechas_ingreso,
        "Dias_Estadia":       dias,
        "Adoptado":           rng.choice([True, False], size=n, p=[0.72, 0.28]),
    })


@st.cache_data(ttl=300)
def load_historical_data() -> pd.DataFrame:
    """
    Carga y valida los datos históricos.
    (Cache invalidada para recargar los nombres actualizados)
    """
    if not _DATA_PATH.exists():
        st.toast("⚠️ CSV no encontrado — usando datos de demostración", icon="⚠️")
        return _generate_synthetic_data()

    df = pd.read_csv(_DATA_PATH, parse_dates=["Fecha_Ingreso"])

    # Validación de esquema
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"El CSV está incompleto. Columnas faltantes: {missing}. "
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
        "estadia_promedio":   round(activos["Dias_Estadia"].mean(), 1) if not activos.empty else 0,
        "larga_estadia":      len(larga_estadia),
        "costo_activos":      round(activos["Costos_Mantenimiento"].sum(), 2) if "Costos_Mantenimiento" in activos.columns else 0,
        "tasa_adopcion":      round(df["Adoptado"].mean() * 100, 1) if not df.empty else 0,
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


def add_new_animal(record_data: dict) -> str:
    """
    Agrega un nuevo animal al archivo CSV histórico.
    Asigna un ID automático, establece los valores base de un ingreso nuevo,
    y vacía la caché de Streamlit para que el Dashboard lo refleje al instante.
    Retorna el ID_Ingreso generado.
    """
    if not _DATA_PATH.exists():
        df = pd.DataFrame([record_data])
        df.to_csv(_DATA_PATH, index=False)
        return record_data.get("ID_Ingreso", "PAE-00001")

    # Leer archivo completo
    df = pd.read_csv(_DATA_PATH)
    
    # Autogenerar ID_Ingreso secuencial
    if not df.empty and 'ID_Ingreso' in df.columns:
        last_id = df['ID_Ingreso'].str.extract(r'PAE-(\d+)')[0].dropna()
        if not last_id.empty:
            next_num = last_id.astype(int).max() + 1
        else:
            next_num = 1
    else:
        next_num = 1
        
    generated_id = f"PAE-{next_num:05d}"
    record_data['ID_Ingreso'] = generated_id
    
    # Completar campos predeterminados para un nuevo ingreso
    record_data['Adoptado'] = False
    record_data['Dias_Estadia'] = 0
    record_data['Fecha_Ingreso'] = date.today().strftime("%Y-%m-%d")
    record_data.setdefault('Publicaciones', 1)
    record_data.setdefault('Interacciones_RRSS', 0)
    record_data.setdefault('Visitas_Recibidas', 0)
    record_data.setdefault('Costos_Mantenimiento', 0.0)

    # Crear nuevo DF de 1 fila
    new_row = pd.DataFrame([record_data])
    
    # Asegurarse que las columnas coincidan en orden
    for col in df.columns:
        if col not in new_row.columns:
            new_row[col] = np.nan
    new_row = new_row[df.columns]
    
    # Concatenar y guardar
    df_updated = pd.concat([df, new_row], ignore_index=True)
    df_updated.to_csv(_DATA_PATH, index=False)
    
    # Limpiar caché de lectura para que el dashboard lo vea inmediatamente
    load_historical_data.clear()
    
    return generated_id


def update_animal(id_ingreso: str, updated_data: dict) -> bool:
    """
    Actualiza los datos de un animal existente en el CSV histórico.
    """
    if not _DATA_PATH.exists():
        return False
        
    df = pd.read_csv(_DATA_PATH)
    
    if 'ID_Ingreso' not in df.columns:
        return False
        
    mask = df['ID_Ingreso'] == id_ingreso
    if not mask.any():
        return False
        
    # Actualizar solo las columnas que se pasan en el diccionario
    for key, value in updated_data.items():
        if key in df.columns:
            df.loc[mask, key] = value
            
    df.to_csv(_DATA_PATH, index=False)
    
    # Vaciar caché para que Streamlit refleje los cambios en todas las vistas
    load_historical_data.clear()
    
    return True
