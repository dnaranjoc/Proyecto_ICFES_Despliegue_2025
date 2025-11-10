# ===============================================================
# fit_scaler.py
# Genera el escalador y datasets escalados para entrenamiento
# ===============================================================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

# ===============================================================
# 1️⃣ Configurar dataset a usar (ajustar manualmente)
# ===============================================================
dataset_name = "saber11_encoded1"   # 👈 Cambia a "saber11_encoded2" cuando quieras usar el otro
dataset_path = f"data/{dataset_name}.parquet"

# ===============================================================
# 2️⃣ Cargar datos
# ===============================================================
df = pd.read_parquet(dataset_path)
print(f"📦 Dataset cargado: {dataset_name} ({len(df):,} filas)")

# ===============================================================
# 3️⃣ Definir variables predictoras y de salida
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
# 4️⃣ Partición train/val/test
# ===============================================================
X_temp, X_test, y_temp, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.2, random_state=42
)

print(f"📊 Particiones -> Train: {len(X_train):,}, Val: {len(X_val):,}, Test: {len(X_test):,}")

# ===============================================================
# 5️⃣ Crear y ajustar el escalador (solo con train)
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
# 6️⃣ Guardar escalador y datasets con nombre del dataset
# ===============================================================
os.makedirs("data/scaled", exist_ok=True)
prefix = f"data/scaled/{dataset_name}"

# Guardar escalador
scaler_path = f"{prefix}_scaler.pkl"
joblib.dump(scaler, scaler_path)
print(f"💾 Escalador guardado en: {scaler_path}")

# Guardar datasets escalados
X_train_scaled.to_parquet(f"{prefix}_X_train_scaled.parquet")
X_val_scaled.to_parquet(f"{prefix}_X_val_scaled.parquet")
X_test_scaled.to_parquet(f"{prefix}_X_test_scaled.parquet")

# Guardar salidas sin escalar
y_train.to_parquet(f"{prefix}_y_train.parquet")
y_val.to_parquet(f"{prefix}_y_val.parquet")
y_test.to_parquet(f"{prefix}_y_test.parquet")

print(f"✅ Datasets escalados guardados con prefijo '{dataset_name}' en data/scaled/")