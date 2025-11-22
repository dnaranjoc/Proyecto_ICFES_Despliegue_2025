from typing import Optional

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

router = APIRouter()

# Esquemas


class IcfesFeatures(BaseModel):
    """
    Este esquema refleja las mismas variables que se envian desde
    App/callbacks.py en el diccionario `datos_modelo`.
    """

    cole_area_ubicacion: float
    cole_bilingue: float
    cole_calendario: float
    cole_caracter: float
    cole_genero: float
    cole_naturaleza: float
    cole_sede_principal: float

    estu_genero_M: float
    fami_estratovivienda: float
    fami_personashogar: float
    fami_tieneautomovil: float
    fami_tienecomputador: float
    fami_tieneinternet: float
    fami_tienelavadora: float
    estu_edad_anios: float

    mismo_municipio_prueba: float
    mismo_municipio_colegio: float
    cole_jornada_cat: float
    fami_cuartoshogar_num: float
    fami_educacionmadre_num: float
    fami_educacionpadre_num: float


class PredictionResponse(BaseModel):
    """
    Respuesta de la API.
    """
    prediction: float
    model_version: str = "0.0.1"
    errors: Optional[str] = None



# Carga del modelo (TODO)


# Cuando el modelo esté entrenado, acá irá algo como:
# import joblib
# model = joblib.load("artefactos/icfes_model.pkl")

model = None  # placeholder por ahora

# /predict


@router.post("/predict", response_model=PredictionResponse)
def predict(input_data: IcfesFeatures) -> PredictionResponse:
    """
    Endpoint de predicción para el modelo ICFES.
    """

    try:
        # Convertir el input a DataFrame con una sola fila
        input_df = pd.DataFrame([jsonable_encoder(input_data)])
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al construir DataFrame a partir de la entrada: {e}",
        )

    # TODO: cuando el modelo exista, reemplazar esto por algo como:
    # if model is None:
    #     raise HTTPException(status_code=500, detail="Modelo no cargado")
    # y luego:
    # preds = model.predict(input_df)
    # pred_value = float(preds[0])

    # Dummy: devolver siempre 250 como "puntaje"
    pred_value = float(np.array([250.0])[0])

    return PredictionResponse(
        prediction=pred_value,
        model_version="0.0.1",
        errors=None,
    )