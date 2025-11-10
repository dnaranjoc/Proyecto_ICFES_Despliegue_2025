# ===============================================================
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import os

# ===============================================================
# 1️⃣ Cargar datos
# ===============================================================
dataset_path = "data/saber11_encoded1.parquet"
df = pd.read_parquet(dataset_path)

# Nombre del dataset (por ejemplo, para trackear en MLflow)
dataset_name = os.path.basename(dataset_path).replace(".parquet", "")

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
# 4️⃣ Estandarizar (solo fit con train)
# ===============================================================
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(
    scaler.fit_transform(X_train),
    columns=X_train.columns,
    index=X_train.index
)

X_val_scaled = pd.DataFrame(
    scaler.transform(X_val),
    columns=X_val.columns,
    index=X_val.index
)

X_test_scaled = pd.DataFrame(
    scaler.transform(X_test),
    columns=X_test.columns,
    index=X_test.index
)

# ===============================================================
# 5️⃣ Reducción opcional del tamaño de entrenamiento
# ===============================================================
reduce_train = True         # 👈 Cambia a False si quieres usar todos los datos
n_rows_train = 1000000    # límite máximo de filas

if reduce_train and len(X_train_scaled) > n_rows_train:
    X_train_small = X_train_scaled.sample(n=n_rows_train, random_state=42)
    y_train_small = y_train.loc[X_train_small.index]
    print(f"📉 Se redujo el tamaño de entrenamiento a {n_rows_train:,} filas.")
else:
    X_train_small = X_train_scaled.copy()
    y_train_small = y_train.copy()
    print(f"📈 Usando todas las {len(X_train_small):,} filas para entrenamiento.")

# ===============================================================
# 6️⃣ Configuración de MLflow
# ===============================================================
experiment = mlflow.set_experiment("SaberInsight_Modelos")

# ===============================================================
# 7️⃣ Entrenar y registrar resultados
# ===============================================================
metricas_val = {}

for col in y_train.columns:
    print(f"\n🔹 Entrenando modelo para: {col}")

    with mlflow.start_run(experiment_id=experiment.experiment_id, run_name=f"{col}"):

        modelo = LinearRegression()
        modelo.fit(X_train_small, y_train_small[col])

        y_pred_val = modelo.predict(X_val_scaled)

        mae_val = mean_absolute_error(y_val[col], y_pred_val)
        mse_val = mean_squared_error(y_val[col], y_pred_val)
        r2_val = r2_score(y_val[col], y_pred_val)
        metricas_val[col] = [mae_val, mse_val, r2_val]

        # Registro en MLflow
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_param("target", col)
        mlflow.log_param("training_rows", len(X_train_small))
        mlflow.log_param("dataset_name", dataset_name)
        mlflow.log_param("reduce_train", reduce_train)
        mlflow.log_param("n_rows_train", n_rows_train)

        mlflow.log_metric("MAE_val", mae_val)
        mlflow.log_metric("MSE_val", mse_val)
        mlflow.log_metric("R2_val", r2_val)

        signature = infer_signature(X_val_scaled, y_pred_val)
        mlflow.sklearn.log_model(
            modelo,
            name=f"{col}_LinearRegression",
            signature=signature,
            input_example=X_val_scaled.head(3)
        )

print("\n✅ Entrenamiento completado (validation)")