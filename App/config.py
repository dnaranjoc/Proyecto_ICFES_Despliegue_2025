import os
from dataclasses import dataclass

@dataclass
class Settings:
    """
    Configuración simple para SaberInsight.
    Lee la URL de la API desde la variable de entorno ICFES_API_URL,
    y si no existe usa un valor por defecto (local).
    """
    PROJECT_NAME: str = "SaberInsight"
    DEBUG: bool = True
    ICFES_API_URL: str = os.getenv(
        "ICFES_API_URL",
        "backend-production-aafd.up.railway.app/docs/predict",  # valor por defecto
    )

settings = Settings()
