import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# =========================================================
# 1. Cargar datos codificados desde el parquet local
# =========================================================
print("📦 Cargando saber11_encoded2.parquet ...")
df = pd.read_parquet("saber11_encoded2.parquet")
print(f"✅ Data cargada con forma: {df.shape}")

# =========================================================
# 2. Definir columnas objetivo (targets)
#    (usando los nombres reales de tu archivo)
# =========================================================
targets = [
    "punt_lectura_critica",
    "punt_matematicas",
    "punt_ingles",
    "punt_sociales_ciudadanas",
    "punt_c_naturales",   # 👈 este es el nombre correcto en tu df
]

print("\n🎯 Columnas objetivo usadas como y:")
for t in targets:
    print(f"   • {t}")

y = df[targets].copy()
X = df.drop(columns=targets).copy()

print(f"\n📊 X shape: {X.shape}")
print(f"📊 y shape: {y.shape}")

# =========================================================
# 3. Train / Validation split
# =========================================================
print("\n✂️ Haciendo train/validation split (80% / 20%) ...")
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"   X_train (full): {X_train.shape}")
print(f"   X_val   (full): {X_val.shape}")
print(f"   y_train (full): {y_train.shape}")
print(f"   y_val   (full): {y_val.shape}")

# =========================================================
# 4. Reducir tamaño para no reventar la RAM
# =========================================================
MAX_ROWS_TRAIN = 800_000   # puedes subir/bajar estos límites si la máquina aguanta
MAX_ROWS_VAL   = 200_000

if len(X_train) > MAX_ROWS_TRAIN:
    print(f"\n📉 Reduciendo X_train a {MAX_ROWS_TRAIN:,} filas para evitar OOM...")
    X_train = X_train.sample(n=MAX_ROWS_TRAIN, random_state=42)
    y_train = y_train.loc[X_train.index]

if len(X_val) > MAX_ROWS_VAL:
    print(f"📉 Reduciendo X_val a {MAX_ROWS_VAL:,} filas para evitar OOM...")
    X_val = X_val.sample(n=MAX_ROWS_VAL, random_state=42)
    y_val = y_val.loc[X_val.index]

print(f"\n✅ Tamaños FINALES usados para escalar:")
print(f"   X_train: {X_train.shape}")
print(f"   X_val:   {X_val.shape}")
print(f"   y_train: {y_train.shape}")
print(f"   y_val:   {y_val.shape}")

# =========================================================
# 5. Escalar X con StandardScaler
# =========================================================
print("\n📏 Escalando features con StandardScaler ...")
scaler = StandardScaler()

X_train_scaled_arr = scaler.fit_transform(X_train)
X_val_scaled_arr   = scaler.transform(X_val)

# Convertimos a float32 para ahorrar memoria
X_train_scaled = pd.DataFrame(
    X_train_scaled_arr,
    index=X_train.index,
    columns=X_train.columns,
).astype("float32")

X_val_scaled = pd.DataFrame(
    X_val_scaled_arr,
    index=X_val.index,
    columns=X_val.columns,
).astype("float32")

print("✅ Escalado completado.")
print(f"   X_train_scaled: {X_train_scaled.shape}, dtype={X_train_scaled.dtypes.iloc[0]}")
print(f"   X_val_scaled:   {X_val_scaled.shape}, dtype={X_val_scaled.dtypes.iloc[0]}")

# =========================================================
# 6. Guardar los 4 archivos en data/scaled/
# =========================================================
os.makedirs("data/scaled", exist_ok=True)
base = "data/scaled/saber11_encoded2"

print("\n💾 Guardando archivos parquet en data/scaled/ ...")
X_train_scaled.to_parquet(f"{base}_X_train_scaled.parquet")
X_val_scaled.to_parquet(f"{base}_X_val_scaled.parquet")
y_train.to_parquet(f"{base}_y_train.parquet")
y_val.to_parquet(f"{base}_y_val.parquet")

print("\n✅ Listo! Se generaron estos archivos:")
print(f"   {base}_X_train_scaled.parquet")
print(f"   {base}_X_val_scaled.parquet")
print(f"   {base}_y_train.parquet")
print(f"   {base}_y_val.parquet")
