# ===============================================================
# mlflow-icfes-CatBoost-final.py
# Entrena modelos CatBoostRegressor sobre datasets escalados,
# usando hiperparámetros ya calibrados (FineTuning previo).
# ===============================================================

import os
import numpy as np
import pandas as pd

import mlflow
import mlflow.catboost
from mlflow.models.signature import infer_signature

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from catboost import CatBoostRegressor

# ===============================================================
# 1️⃣ Configuración general
# ===============================================================

# Nombre del dataset escalado (ya preparado con DVC)
dataset_name = "saber11_encoded2"
scaled_path = f"data/scaled/{dataset_name}"

# ¿Reducir tamaño de entrenamiento?
reduce_train = False          # 👈 Para entrenamiento final déjalo en False
n_rows_train = 1_000_000      # Límite si reduce_train = True

# Ruta de tracking para MLflow
# 👉 Opción local (recomendado mientras el servidor remoto no responda)
mlflow.set_tracking_uri("file:./mlruns")

# Si más adelante tienes el servidor remoto activo, puedes usar:
# mlflow.set_tracking_uri("http://54.209.209.170:8050")

experiment = mlflow.set_experiment("SaberInsight_CatBoost_Final")

print("✅ Configuración inicial lista.")
print(f"   Dataset: {dataset_name}")
print(f"   Tracking URI: {mlflow.get_tracking_uri()}")
print(f"   Experimento MLflow: {experiment.name}")

# ===============================================================
# 2️⃣ Cargar datasets escalados
# ===============================================================

print(f"\n📦 Cargando datasets escalados desde: {scaled_path}")

X_train_scaled = pd.read_parquet(f"{scaled_path}_X_train_scaled.parquet")
X_val_scaled   = pd.read_parquet(f"{scaled_path}_X_val_scaled.parquet")

y_train = pd.read_parquet(f"{scaled_path}_y_train.parquet")
y_val   = pd.read_parquet(f"{scaled_path}_y_val.parquet")

print("✅ Datasets cargados correctamente:")
print(f"   • X_train_scaled: {X_train_scaled.shape}")
print(f"   • X_val_scaled:   {X_val_scaled.shape}")
print(f"   • y_train:        {y_train.shape}")
print(f"   • y_val:          {y_val.shape}")

# ===============================================================
# 3️⃣ Reducción opcional del tamaño de entrenamiento
# ===============================================================

if reduce_train and len(X_train_scaled) > n_rows_train:
    X_train_small = X_train_scaled.sample(n=n_rows_train, random_state=42)
    y_train_small = y_train.loc[X_train_small.index]
    print(f"\n📉 Se redujo el tamaño de entrenamiento a {n_rows_train:,} filas.")
else:
    X_train_small = X_train_scaled.copy()
    y_train_small = y_train.copy()
    print(f"\n📈 Usando todas las {len(X_train_small):,} filas para entrenamiento.")

# ===============================================================
# 4️⃣ Hiperparámetros base y calibrados por target
# ===============================================================

# Hiperparámetros base (por defecto) para CatBoost
base_params = {
    "loss_function": "RMSE",
    "eval_metric": "RMSE",
    "verbose": 200,
    "thread_count": -1,
    "random_seed": 42,
    # Valores por defecto razonables
    "iterations": 1000,
    "learning_rate": 0.05,
    "depth": 8,
    "l2_leaf_reg": 3,
    "bagging_temperature": 0.8,
    "random_strength": 1.0,
    "rsm": 0.8,
}

# Hiperparámetros calibrados (FineTuning) por variable objetivo
# ✅ Estos son los que ya obtuviste para punt_lectura_critica
best_params_por_target = {
    "punt_lectura_critica": {
        "iterations": 1200,
        "learning_rate": 0.05,
        "depth": 7,
        "l2_leaf_reg": 9,
        "bagging_temperature": 0.8,
        "random_strength": 1.2,
        "rsm": 0.9,
    },

    # 👉 Cuando tengas los resultados del FineTuning para los demás,
    #    los agregas aquí, por ejemplo:
    #
    # "punt_matematicas": {
    #     "iterations": ...,
    #     "learning_rate": ...,
    #     "depth": ...,
    #     "l2_leaf_reg": ...,
    #     "bagging_temperature": ...,
    #     "random_strength": ...,
    #     "rsm": ...,
    # },
    #
    # "punt_ingles": { ... },
    # "punt_sociales_ciudadanas": { ... },
    # "punt_ciencias_naturales": { ... },
}

print("\n🧩 Hiperparámetros calibrados cargados para los siguientes targets:")
for t in best_params_por_target.keys():
    print(f"   • {t}")

# ===============================================================
# 5️⃣ Entrenamiento por target y registro en MLflow
# ===============================================================

metricas_val = {}

print("\n🚀 Iniciando entrenamiento final de modelos CatBoost por target...")

for col in y_train.columns:
    print(f"\n🔹 Entrenando modelo CatBoostRegressor para target: {col}")

    # Construir hiperparámetros finales: base + específicos del target (si hay)
    params = base_params.copy()
    if col in best_params_por_target:
        params.update(best_params_por_target[col])
        print("   📌 Usando hiperparámetros calibrados para este target.")
    else:
        print("   ⚠️ No hay hiperparámetros calibrados específicos para este target.")
        print("      → Usando solo los hiperparámetros base.")

    for k, v in params.items():
        print(f"      {k}: {v}")

    # Ejecutar run en MLflow
    with mlflow.start_run(
        experiment_id=experiment.experiment_id,
        run_name=f"{dataset_name}_{col}_CatBoost_Final"
    ):
        # Log de parámetros
        mlflow.log_param("model_type", "CatBoostRegressor")
        mlflow.log_param("target", col)
        mlflow.log_param("dataset_name", dataset_name)
        mlflow.log_param("reduce_train", reduce_train)
        mlflow.log_param("n_rows_train", n_rows_train)
        mlflow.log_params(params)

        # Crear y entrenar modelo
        modelo = CatBoostRegressor(**params)
        modelo.fit(
            X_train_small,
            y_train_small[col],
            eval_set=(X_val_scaled, y_val[col]),
            use_best_model=False,
        )

        # Predicción sobre validación
        y_pred_val = modelo.predict(X_val_scaled)

        # Métricas
        mae_val = mean_absolute_error(y_val[col], y_pred_val)
        mse_val = mean_squared_error(y_val[col], y_pred_val)
        r2_val  = r2_score(y_val[col], y_pred_val)
        rmse_val = np.sqrt(mse_val)

        metricas_val[col] = {
            "MAE_val": mae_val,
            "MSE_val": mse_val,
            "RMSE_val": rmse_val,
            "R2_val": r2_val,
        }

        print("\n   📈 MÉTRICAS EN VALIDACIÓN")
        print(f"      MAE  = {mae_val:.4f}")
        print(f"      MSE  = {mse_val:.4f}")
        print(f"      RMSE = {rmse_val:.4f}")
        print(f"      R2   = {r2_val:.4f}")

        # Log de métricas en MLflow
        mlflow.log_metric("MAE_val", mae_val)
        mlflow.log_metric("MSE_val", mse_val)
        mlflow.log_metric("RMSE_val", rmse_val)
        mlflow.log_metric("R2_val", r2_val)

        # Guardar modelo en MLflow con firma
        signature = infer_signature(X_val_scaled, y_pred_val)
        mlflow.catboost.log_model(
            cb_model=modelo,
            artifact_path=f"{col}_CatBoost_Final",
            signature=signature,
            input_example=X_val_scaled.head(3),
        )

print("\n✅ Entrenamiento completado y modelos registrados en MLflow.")

print("\n==================== RESUMEN FINAL DE MÉTRICAS ====================")
for col, mets in metricas_val.items():
    print(f"\n🔹 TARGET: {col}")
    for k, v in mets.items():
        print(f"   {k}: {v:.4f}")
