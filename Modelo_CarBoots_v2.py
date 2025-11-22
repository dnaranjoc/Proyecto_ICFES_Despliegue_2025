# ===============================================================
# 0️⃣ IMPORTS Y CONFIGURACIÓN
# ===============================================================
import numpy as np
import pandas as pd

from catboost import CatBoostRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("✅ Librerías importadas correctamente.")

# ===============================================================
# 1️⃣ OPCIONAL: REDUCIR TAMAÑO DEL DATASET
# ===============================================================
reduce_train = False        # 👈 pon True si quieres muestrear
n_rows_train = 300_000      # límite de filas para tuning

if reduce_train and len(X_train_scaled) > n_rows_train:
    X_train_tune = X_train_scaled.sample(n=n_rows_train, random_state=42)
    y_train_tune = y_train.loc[X_train_tune.index]
    print(f"📉 Usaremos solo {n_rows_train:,} filas para el FineTuning.")
else:
    X_train_tune = X_train_scaled
    y_train_tune = y_train
    print(f"📈 Usaremos todas las {len(X_train_tune):,} filas para el FineTuning.")
# ===============================================================
# 2️⃣ MODELO BASE CATBOOST
# ===============================================================
def crear_modelo_base():
    params_base = {
        "loss_function": "RMSE",
        "eval_metric": "RMSE",
        "bootstrap_type": "Bayesian",   # ⭐ tu cambio
        "random_seed": 42,
        "thread_count": -1,
        "verbose": 100
    }
    print("⚙️ Creando modelo base CatBoostRegressor...")
    for k, v in params_base.items():
        print(f"   {k}: {v}")
    return CatBoostRegressor(**params_base)
# ===============================================================
# 3️⃣ ESPACIO DE HIPERPARÁMETROS PARA TUNING
# ===============================================================
param_dist = {
    "iterations": [400, 600, 800, 1000, 1200],
    "learning_rate": [0.03, 0.04, 0.05, 0.07],
    "depth": [6, 7, 8, 9],
    "l2_leaf_reg": [2, 3, 5, 7, 9],
    "bagging_temperature": [0.5, 0.8, 1.0, 1.2],
    "random_strength": [0.8, 1.0, 1.2],
    "rsm": [0.6, 0.75, 0.9]
}

print("🎯 Espacio de hiperparámetros definido para FineTuning.")
for k, v in param_dist.items():
    print(f"   {k}: {v}")
# ===============================================================
# 4️⃣ FUNCIÓN DE FINETUNING PARA UN TARGET
# ===============================================================
def finetune_catboost_target(X_train, y_train_col, X_val, y_val_col, target_name,
                             n_iter=15, cv=3):
    """
    FineTuning de CatBoostRegressor para una variable objetivo.
    - X_train, y_train_col: datos de entrenamiento
    - X_val, y_val_col: datos de validación
    - target_name: nombre de la columna objetivo (string)
    """

    print("\n===============================================================")
    print(f"🎯 FineTuning CatBoost para TARGET: {target_name}")
    print("===============================================================")

    modelo_base = crear_modelo_base()

    # Wrapper para sklearn
    search = RandomizedSearchCV(
        estimator=modelo_base,
        param_distributions=param_dist,
        n_iter=n_iter,
        scoring="neg_root_mean_squared_error",
        cv=cv,
        verbose=2,
        random_state=42,
        n_jobs=-1   # cuidado si la máquina es muy limitada
    )

    print("🚀 Iniciando búsqueda aleatoria de hiperparámetros...")
    search.fit(X_train, y_train_col)

    print("\n✅ FineTuning completado.")
    print(f"🔎 Mejor puntuación (CV RMSE negativo): {search.best_score_:.4f}")
    print("📌 Mejores hiperparámetros encontrados:")
    for k, v in search.best_params_.items():
        print(f"   {k}: {v}")

    # Mejor modelo ya reentrenado por RandomizedSearchCV
    best_model = search.best_estimator_

    print("\n📊 Evaluando mejor modelo en conjunto de validación...")
    y_pred_val = best_model.predict(X_val)

    mae = mean_absolute_error(y_val_col, y_pred_val)
    mse = mean_squared_error(y_val_col, y_pred_val)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_val_col, y_pred_val)

    print("\n📈 MÉTRICAS EN VALIDACIÓN")
    print(f"   MAE  = {mae:.4f}")
    print(f"   MSE  = {mse:.4f}")
    print(f"   RMSE = {rmse:.4f}")
    print(f"   R2   = {r2:.4f}")

    resultados = {
        "best_params": search.best_params_,
        "cv_best_score": search.best_score_,
        "MAE_val": mae,
        "MSE_val": mse,
        "RMSE_val": rmse,
        "R2_val": r2
    }

    return best_model, resultados
# ===============================================================
# 5️⃣ APLICAR FINETUNING A TODAS LAS VARIABLES OBJETIVO
# ===============================================================
resultados_globales = {}

for col in y_train_tune.columns:
    best_model, res = finetune_catboost_target(
        X_train=X_train_tune,
        y_train_col=y_train_tune[col],
        X_val=X_val_scaled,
        y_val_col=y_val[col],
        target_name=col,
        n_iter=12,   # puedes subir a 20 si tienes tiempo
        cv=3
    )
    
    resultados_globales[col] = res

print("\n==================== RESUMEN FINAL DE MÉTRICAS ====================")
for col, res in resultados_globales.items():
    print(f"\n🔹 TARGET: {col}")
    for k, v in res.items():
        if isinstance(v, float):
            print(f"   {k}: {v:.4f}")
        else:
            print(f"   {k}: {v}")
