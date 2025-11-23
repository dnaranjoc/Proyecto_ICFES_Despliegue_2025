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
    #cole_bilingue: str
    cole_calendario: str
    cole_caracter: str
    cole_genero: str
    cole_naturaleza: str

    # Codificadas como texto (aunque representen números)
    estu_genero_M: str
    fami_estratovivienda: str
    fami_personashogar: str

    # Binarias 0/1
    fami_tieneautomovil: int
    fami_tienecomputador: int
    fami_tieneinternet: int
    fami_tienelavadora: int
    cole_bilingue: int
    cole_sede_principal: int

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

scaler = joblib.load(MODELS_DIR / "saber11_encoded2_scaler.pkl")
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

    # --------------------------------------------
    # 1. Convertir la entrada a DataFrame
    # --------------------------------------------
    try:
        input_df = pd.DataFrame([jsonable_encoder(input_data)])
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al construir DataFrame a partir de la entrada: {e}"
        )

    # --------------------------------------------
    # 2. Codificar variables categóricas
    # --------------------------------------------
    cat_cols = [
        'cole_area_ubicacion', 'cole_calendario', 'cole_caracter',
        'cole_naturaleza', 'cole_jornada_cat'
    ]

    try:
        df = pd.get_dummies(input_df, columns=cat_cols, drop_first=True, dtype=float)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al codificar variables categóricas: {e}"
        )

    # --------------------------------------------
    # 2.1 Alinear columnas con las usadas por el modelo
    #    (IMPORTANTE para que scaler y modelos no fallen)
    # --------------------------------------------
    try:
        expected_cols = scaler.feature_names_in_  # columnas usadas al entrenar el scaler
        # Añadir columnas faltantes con 0
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0.0
        # Remover columnas extra
        df = df[expected_cols]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al alinear columnas con las del modelo: {e}"
        )

    # --------------------------------------------
    # 3. Escalado
    # --------------------------------------------
    try:
        input_scaled = pd.DataFrame(
            scaler.transform(df),
            columns=df.columns,
            index=df.index
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al escalar variables: {e}"
        )

    # --------------------------------------------
    # 4. Predicciones
    # --------------------------------------------
    try:
        punt_lectura = float(modelo_lectura.predict(input_scaled)[0])
        punt_mate = float(modelo_mate.predict(input_scaled)[0])
        punt_sociales = float(modelo_sociales.predict(input_scaled)[0])
        punt_c_nat = float(modelo_c_naturales.predict(input_scaled)[0])
        punt_ingles = float(modelo_ingles.predict(input_scaled)[0])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al predecir con los modelos: {e}"
        )

    # --------------------------------------------
    # 5. Respuesta final
    # --------------------------------------------
    return PredictionResponse(
        punt_lectura_critica=punt_lectura,
        punt_matematicas=punt_mate,
        punt_sociales_ciudadanas=punt_sociales,
        punt_c_naturales=punt_c_nat,
        punt_ingles=punt_ingles,
        model_version="0.0.1",
        errors=None,
    )