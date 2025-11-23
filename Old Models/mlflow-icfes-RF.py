# ===============================================================
# mlflow-icfes-RF.py
# Entrena modelos Random Forest sobre datasets escalados
# ===============================================================

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import os

# ===============================================================
# 1️⃣ Configurar dataset a usar (mismo nombre que en fit_scaler.py)
# ===============================================================
dataset_name = "saber11_encoded2"
scaled_path = f"data/scaled/{dataset_name}"

# ===============================================================
# 2️⃣ Cargar datasets escalados
# ===============================================================
print(f"📦 Cargando datasets escalados de: {scaled_path}")

X_train_scaled = pd.read_parquet(f"{scaled_path}_X_train_scaled.parquet")
X_val_scaled = pd.read_parquet(f"{scaled_path}_X_val_scaled.parquet")

y_train = pd.read_parquet(f"{scaled_path}_y_train.parquet")
y_val = pd.read_parquet(f"{scaled_path}_y_val.parquet")

print(f"✅ Datasets cargados: Train={len(X_train_scaled):,}, Val={len(X_val_scaled):,}")

# ===============================================================
# 3️⃣ Reducción opcional del tamaño de entrenamiento
# ===============================================================
reduce_train = False
n_rows_train = 1_000_000

if reduce_train and len(X_train_scaled) > n_rows_train:
    X_train_small = X_train_scaled.sample(n=n_rows_train, random_state=42)
    y_train_small = y_train.loc[X_train_small.index]
    print(f"📉 Se redujo el tamaño de entrenamiento a {n_rows_train:,} filas.")
else:
    X_train_small = X_train_scaled.copy()
    y_train_small = y_train.copy()
    print(f"📈 Usando todas las {len(X_train_small):,} filas para entrenamiento.")

# ===============================================================
# 4️⃣ Configuración de MLflow
# ===============================================================
mlflow.set_tracking_uri("http://54.209.209.170:8050/")
experiment = mlflow.set_experiment("SaberInsight_Modelos")

# ===============================================================
# 5️⃣ Entrenamiento y registro
# ===============================================================
metricas_val = {}

for col in y_train.columns:
    print(f"\n🌲 Entrenando Random Forest para: {col}")

    with mlflow.start_run(experiment_id=experiment.experiment_id, run_name=f"{dataset_name}_{col}_RF"):

        # Hiperparámetros recomendados para 2M x 32
        n_estimators = 150
        max_samples = 0.2             # usa 20% de filas por árbol (si sklearn lo soporta)
        max_depth = 25
        min_samples_split = 20
        min_samples_leaf = 50
        max_features = "sqrt"         # o int(6)
        bootstrap = True
        random_state = 42
        n_jobs = -1

        modelo = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            max_features=max_features,
            bootstrap=bootstrap,
            max_samples=max_samples,   # requiere sklearn >= 0.22
            random_state=random_state,
            n_jobs=n_jobs,
            verbose=1
        )

        modelo.fit(X_train_small, y_train_small[col])

        # Predicción sobre validación
        y_pred_val = modelo.predict(X_val_scaled)

        # Métricas
        mae_val = mean_absolute_error(y_val[col], y_pred_val)
        mse_val = mean_squared_error(y_val[col], y_pred_val)
        r2_val = r2_score(y_val[col], y_pred_val)
        metricas_val[col] = [mae_val, mse_val, r2_val]

        # MLflow logging (agrega todos los params)
        mlflow.log_param("model_type", "RandomForestRegressor")
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_samples", max_samples)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("min_samples_split", min_samples_split)
        mlflow.log_param("min_samples_leaf", min_samples_leaf)
        mlflow.log_param("max_features", str(max_features))
        mlflow.log_param("bootstrap", bootstrap)
        mlflow.log_param("n_jobs", n_jobs)
        mlflow.log_param("random_state", random_state)

        mlflow.log_metric("MAE_val", mae_val)
        mlflow.log_metric("MSE_val", mse_val)
        mlflow.log_metric("R2_val", r2_val)

        # Guardar modelo con firma
        signature = infer_signature(X_val_scaled, y_pred_val)
        mlflow.sklearn.log_model(
            modelo,
            name=f"{col}_RandomForest",
            signature=signature,
            input_example=X_val_scaled.head(3)
        )

print("\n✅ Entrenamiento completado y registrado en MLflow (Random Forest)")