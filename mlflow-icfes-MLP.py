# ===============================================================
# mlflow-icfes-MLP.py
# Entrena modelos MLPRegressor sobre datasets escalados
# ===============================================================

import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.neural_network import MLPRegressor
import os

# ===============================================================
# 1️⃣ Configurar dataset a usar
# ===============================================================
dataset_name = "saber11_encoded2"   # 👈 Cambia si usas otro dataset
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
reduce_train = False        # 👈 Cambia a True para reducir datos
n_rows_train = 1_000_000    # límite máximo de filas

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
mlflow.set_tracking_uri("http://54.209.209.170:8050")
experiment = mlflow.set_experiment("SaberInsight_Modelos")

# ===============================================================
# 5️⃣ Entrenamiento y registro con MLP
# ===============================================================
metricas_val = {}

# 🔧 Hiperparámetros recomendados para 2M x 32
mlp_params = {
    "hidden_layer_sizes": (128, 64, 32),  # Tres capas densas decrecientes
    "activation": "relu",
    "solver": "adam",
    "alpha": 0.0005,                      # Regularización L2
    "batch_size": 1024,                    # Tamaño de batch para estabilidad
    "learning_rate_init": 0.001,
    "max_iter": 200,
    "shuffle": True,
    "random_state": 42,
    "verbose": False,
    "early_stopping": False
}

for col in y_train.columns:
    print(f"\n🔹 Entrenando modelo MLPRegressor para: {col}")

    with mlflow.start_run(experiment_id=experiment.experiment_id, run_name=f"{dataset_name}_{col}_MLP"):

        # Modelo
        modelo = MLPRegressor(**mlp_params)
        modelo.fit(X_train_small, y_train_small[col])

        # Predicción sobre validación
        y_pred_val = modelo.predict(X_val_scaled)

        # Métricas
        mae_val = mean_absolute_error(y_val[col], y_pred_val)
        mse_val = mean_squared_error(y_val[col], y_pred_val)
        r2_val = r2_score(y_val[col], y_pred_val)
        metricas_val[col] = [mae_val, mse_val, r2_val]

        # Registro en MLflow
        mlflow.log_param("model_type", "MLPRegressor")
        for k, v in mlp_params.items():
            mlflow.log_param(k, v)

        mlflow.log_param("target", col)
        mlflow.log_param("training_rows", len(X_train_small))
        mlflow.log_param("dataset_name", dataset_name)
        mlflow.log_param("reduce_train", reduce_train)
        mlflow.log_param("n_rows_train", n_rows_train)

        mlflow.log_metric("MAE_val", mae_val)
        mlflow.log_metric("MSE_val", mse_val)
        mlflow.log_metric("R2_val", r2_val)

        # Guardar modelo con firma
        signature = infer_signature(X_val_scaled, y_pred_val)
        mlflow.sklearn.log_model(
            modelo,
            name=f"{col}_MLPRegressor",
            signature=signature,
            input_example=X_val_scaled.head(3)
        )

print("\n✅ Entrenamiento completado y registrado en MLflow (MLP)")
