from typing import Optional

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pathlib import Path
import joblib

router = APIRouter()

# Esquemas


class IcfesFeatures(BaseModel):
    """
    Este esquema refleja las mismas variables que se envian desde
    App/callbacks.py en el diccionario `datos_modelo`.
    """

    # Categóricas puras (strings)
    cole_area_ubicacion: str
    cole_bilingue: str
    cole_calendario: str
    cole_caracter: str
    cole_genero: str
    cole_naturaleza: str
    cole_sede_principal: str

    # Codificadas como texto (aunque representen números)
    estu_genero_M: str
    fami_estratovivienda: str
    fami_personashogar: str

    # Binarias 0/1
    fami_tieneautomovil: int
    fami_tienecomputador: int
    fami_tieneinternet: int
    fami_tienelavadora: int

    # Numérica real
    estu_edad_anios: float

    # Binarias 0/1
    mismo_municipio_prueba: int
    mismo_municipio_colegio: int

    # Categóricas
    cole_jornada_cat: str
    fami_cuartoshogar_num: str
    fami_educacionmadre_num: str
    fami_educacionpadre_num: str


class PredictionResponse(BaseModel):
    """
    Respuesta de la API.
    """
    punt_lectura_critica: float
    punt_matematicas: float
    punt_sociales_ciudadanas: float
    punt_c_naturales: float
    punt_ingles: float
    model_version: str = "0.0.1"
    errors: Optional[str] = None
    # prediction: float
    # model_version: str = "0.0.1"
    # errors: Optional[str] = None


# Carga del modelo (TODO)
# (En realidad aquí ya estamos cargando los modelos desde disco)


# Cuando el modelo esté entrenado, acá irá algo como:
# import joblib
# model = joblib.load("artefactos/icfes_model.pkl")

# model = None  # placeholder por ahora

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"

modelo_lectura = joblib.load(MODELS_DIR / "modelo_punt_lectura_critica.pkl")
modelo_mate = joblib.load(MODELS_DIR / "modelo_punt_matematicas.pkl")
modelo_sociales = joblib.load(MODELS_DIR / "modelo_punt_sociales_ciudadanas.pkl")
modelo_c_naturales = joblib.load(MODELS_DIR / "modelo_punt_c_naturales.pkl")
modelo_ingles = joblib.load(MODELS_DIR / "modelo_punt_ingles.pkl")

# /predict


@router.post("/predict", response_model=PredictionResponse)
def predict(input_data: IcfesFeatures) -> PredictionResponse:
    """
    Endpoint de predicción para el modelo ICFES.
    """

    # 1. Convertir la entrada a DataFrame
    try:
        input_df = pd.DataFrame([jsonable_encoder(input_data)])
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al construir DataFrame a partir de la entrada: {e}",
        )

    # 2. Obtener predicciones de cada modelo
    try:
        punt_lectura = float(modelo_lectura.predict(input_df)[0])
        punt_mate = float(modelo_mate.predict(input_df)[0])
        punt_sociales = float(modelo_sociales.predict(input_df)[0])
        punt_c_nat = float(modelo_c_naturales.predict(input_df)[0])
        punt_ingles = float(modelo_ingles.predict(input_df)[0])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al predecir con los modelos: {e}",
        )

    # 3. Devolver todos los puntajes
    return PredictionResponse(
        punt_lectura_critica=punt_lectura,
        punt_matematicas=punt_mate,
        punt_sociales_ciudadanas=punt_sociales,
        punt_c_naturales=punt_c_nat,
        punt_ingles=punt_ingles,
        model_version="0.0.1",
        errors=None,
    )