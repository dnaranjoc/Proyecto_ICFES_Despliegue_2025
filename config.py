from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    """
    Configuración central del proyecto SaberInsight.
    Lee variables desde el entorno o desde un archivo .env si existe.
    """

    # Nombre del proyecto
    PROJECT_NAME: str = "SaberInsight"

    # Modo debug para la app de Dash
    DEBUG: bool = True

    # URL de la API que expone el modelo
    # Por defecto apunta a un servidor local
    ICFES_API_URL: AnyHttpUrl | str = "http://127.0.0.1:8000/predict"

    class Config:
        # Lee el archivo .env automáticamente
        env_file = ".env"
        env_file_encoding = "utf-8"


# instancia global
settings = Settings()