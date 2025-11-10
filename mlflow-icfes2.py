# ===============================================================
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

# ===============================================================
# 1️⃣ Cargar datos
# ===============================================================
df = pd.read_parquet("data/saber11_encoded.parquet")

# ===============================================================
# 2️⃣ Definir variables predictoras y de salida
# ===============================================================
Y_cols = [
    'punt_lectura_critica',
    'punt_matematicas',
    'punt_sociales_ciudadanas',
    'punt_c_naturales',
    'punt_ingles'
]

Y = df[Y_cols]
X = df.drop(columns=Y_cols + ['punt_global'])

# ===============================================================
# 3️⃣ Partición train/val/test
# ===============================================================
X_temp, X_test, y_temp, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.2, random_state=42
)

# ===============================================================
# 4️⃣ Reducir tamaño de entrenamiento (sample)
# ===============================================================
# Ajusta n_rows_train según memoria disponible
n_rows_train = 1000000  # ejemplo: 30k filas
if len(X_train) > n_rows_train:
    X_train_small = X_train.sample(n=n_rows_train, random_state=42)
    y_train_small = y_train.loc[X_train_small.index]
else:
    X_train_small = X_train.copy()
    y_train_small = y_train.copy()

# ===============================================================
# 5️⃣ Configuración de MLflow
# ===============================================================
experiment = mlflow.set_experiment("Saber11_Modelos")

# ===============================================================
# 6️⃣ Entrenar LinearRegression y registrar resultados (solo validation)
# ===============================================================
metricas_val = {}

for col in y_train.columns:
    print(f"\n🔹 Entrenando modelo para: {col}")

    with mlflow.start_run(experiment_id=experiment.experiment_id, run_name=f"{col}"):
        # Modelo
        modelo = LinearRegression()
        modelo.fit(X_train_small, y_train_small[col])

        # Predicción sobre validation
        y_pred_val = modelo.predict(X_val)

        # Métricas solo sobre validation
        mae_val = mean_absolute_error(y_val[col], y_pred_val)
        mse_val = mean_squared_error(y_val[col], y_pred_val)
        r2_val = r2_score(y_val[col], y_pred_val)

        metricas_val[col] = [mae_val, mse_val, r2_val]

        # Registro en MLflow
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_param("target", col)
        mlflow.log_param("training_rows", len(X_train_small))

        mlflow.log_metric("MAE_val", mae_val)
        mlflow.log_metric("MSE_val", mse_val)
        mlflow.log_metric("R2_val", r2_val)

        # Guardar modelo con 'name' y firma
        signature = infer_signature(X_val, y_pred_val)
        mlflow.sklearn.log_model(
            modelo,
            name=f"{col}_LinearRegression",
            signature=signature,
            input_example=X_val.head(3)
        )

print("\n✅ Entrenamiento completado (validation)")
