from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router

app = FastAPI(
    title="SaberInsight ICFES API",
    version="0.0.1",
    description="API para servir el modelo de predicción de resultados ICFES",
)

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas API
app.include_router(api_router)

# Healthcheck


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "ICFES API running"}

# Ejecución local

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )