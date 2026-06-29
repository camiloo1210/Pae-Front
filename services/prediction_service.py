"""
Prediction Service — encapsula el modelo ML.

Single Responsibility: la UI solo llama a predict() con un dict.
Cualquier cambio en el modelo (nuevo preprocesador, versioning,
A/B testing) ocurre aquí sin tocar las páginas.
"""

from __future__ import annotations

import pandas as pd
import joblib
import streamlit as st
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
_MODEL_DIR = Path(__file__).parent.parent
@dataclass(frozen=True)
class PredictionInput:
    """Value Object — garantiza que los datos de entrada estén completos."""
    especie:       str
    raza:          str
    edad_meses:    int
    peso_kg:       float
    tamano:        str
    estado_salud:  str
    sociabilidad:  str
    esterilizado:  str
    publicaciones: int
    interacciones: int
    visitas:       int
    costos:        float

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([{
            "Especie":           self.especie,
            "Raza":              self.raza,
            "Edad_Meses":        self.edad_meses,
            "Peso_Kg":           self.peso_kg,
            "Tamano":            self.tamano,
            "Estado_Salud":      self.estado_salud,
            "Nivel_Sociabilidad":self.sociabilidad,
            "Esterilizado":      self.esterilizado,
            "Publicaciones":     self.publicaciones,
            "Interacciones_RRSS":self.interacciones,
            "Visitas_Recibidas": self.visitas,
            "Costos_Mantenimiento": self.costos,
        }])


@dataclass(frozen=True)
class PredictionResult:
    """Value Object — resultado tipado, nunca un float suelto."""
    days:     int
    category: str   # "fast" | "normal" | "critical"
    label:    str
    action:   str

    @property
    def is_critical(self) -> bool:
        return self.category == "critical"

    @property
    def is_fast(self) -> bool:
        return self.category == "fast"


def _classify(days: int) -> tuple[str, str, str]:
    if days > 45:
        return ("critical",
                "Larga estadía",
                "Activar protocolo foster y campaña de marketing intensiva de inmediato.")
    elif days < 15:
        return ("fast",
                "Tránsito rápido",
                "Alta probabilidad de adopción temprana. Preparar documentación de salida.")
    else:
        return ("normal",
                "Estadía regular",
                "Planificar mantenimiento estándar y reforzar visibilidad en redes sociales.")


@st.cache_resource
def _load_model() -> tuple:
    """
    Carga el preprocesador y el modelo una sola vez en la sesión.
    Falla explícitamente con mensaje claro si los archivos no existen.
    """
    ct_path    = _MODEL_DIR / "preprocesador_pae.pkl"
    model_path = _MODEL_DIR / "modelo_pae.pkl"

    missing = [p for p in (ct_path, model_path) if not p.exists()]
    if missing:
        raise FileNotFoundError(
            f"Archivos de modelo no encontrados: {[str(m) for m in missing]}. "
            "Asegúrate de que preprocesador_pae.pkl y modelo_pae.pkl estén "
            "en la raíz del proyecto (mismo nivel que pages/)."
        )

    return joblib.load(ct_path), joblib.load(model_path)


def predict(input_data: PredictionInput) -> PredictionResult:
    """
    Punto de entrada único para predicciones.
    Lanza excepciones tipadas — la UI decide cómo mostrarlas.
    """
    ct, modelo = _load_model()
    df_input   = input_data.to_dataframe()
    processed  = ct.transform(df_input)
    raw_days   = modelo.predict(processed)[0]
    days       = max(1, int(round(raw_days)))   # garantizar entero positivo
    category, label, action = _classify(days)

    return PredictionResult(
        days=days,
        category=category,
        label=label,
        action=action,
    )
