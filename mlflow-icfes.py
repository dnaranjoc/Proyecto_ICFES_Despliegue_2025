#!/usr/bin/env python
# coding: utf-8

# # Librerías

import pandas   as pd
import numpy    as np

#Para la imputación de los datos
from sklearn.impute     import SimpleImputer
from sklearn.compose    import ColumnTransformer

#Para el pre-procesamiento de los datos
from sklearn.preprocessing      import LabelEncoder, OrdinalEncoder, OneHotEncoder
from sklearn.feature_selection  import SelectKBest, chi2


#Para generar los modelos
from sklearn.model_selection    import train_test_split

saber11_df = pd.read_parquet("data/saber11_limpio.parquet")

#MODELO CATBOOST POR ÁREA + REGISTRO EN MLFLOW (COMPLETO)

import mlflow
import mlflow.catboost
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ===============================================================
# Variables predictoras y objetivos
# ===============================================================
X = saber11_df[[
    'cole_area_ubicacion',
    'cole_bilingue',
    'cole_calendario',
    'cole_caracter',
    'cole_depto_ubicacion',
    'cole_genero',
    'cole_naturaleza',
    'cole_sede_principal',
    'estu_depto_presentacion',
    'estu_depto_reside',
    'estu_genero',
    'fami_estratovivienda',
    'fami_personashogar',
    'fami_tieneautomovil',
    'fami_tienecomputador',
    'fami_tieneinternet',
    'fami_tienelavadora',
    'mismo_municipio_prueba',
    'mismo_municipio_colegio',
    'cole_jornada_cat',
    'fami_educacionmadre_num',
    'fami_educacionpadre_num',
    'fami_cuartoshogar_num',
    'estu_edad_anios'
]]

Y = saber11_df[[
    'punt_lectura_critica',
    'punt_matematicas',
    'punt_sociales_ciudadanas',
    'punt_c_naturales',
    'punt_ingles'
]]

# ===============================================================
#  División de datos: 70% train, 15% val, 15% test
# ===============================================================
X_train, X_temp, Y_train, Y_temp = train_test_split(X, Y, test_size=0.30, random_state=42)
X_val, X_test, Y_val, Y_test = train_test_split(X_temp, Y_temp, test_size=0.50, random_state=42)

print(f"Entrenamiento: {X_train.shape}")
print(f"Validación: {X_val.shape}")
print(f"Prueba: {X_test.shape}")

# ===============================================================
# Configuración inicial de MLflow
# ===============================================================
experiment = mlflow.set_experiment("Saber11_CatBoost_Areas")

# ===============================================================
# Identificar variables categóricas
# ===============================================================
cat_features = X_train.select_dtypes(include='object').columns.tolist()

for df_ in [X_train, X_val, X_test]:
    for col in cat_features:
        df_[col] = df_[col].astype(str)

# ===============================================================
# Entrenamiento y registro de modelos por área
# ===============================================================
metricas_val = {}
metricas_test = {}

for col in Y_train.columns:
    print(f"\n🔹 Entrenando modelo CatBoost para: {col}")

    with mlflow.start_run(run_name=f"CatBoost_{col}"):

        modelo = CatBoostRegressor(
            iterations=500,
            learning_rate=0.05,
            depth=8,
            loss_function='RMSE',
            cat_features=cat_features,
            random_seed=42,
            verbose=False,
            early_stopping_rounds=50,
            allow_writing_files=False
        )

        modelo.fit(
            X_train, Y_train[col],
            eval_set=(X_val, Y_val[col]),
            use_best_model=True
        )

        # -----------------------------
        # Validación
        # -----------------------------
        y_pred_val = modelo.predict(X_val)
        mae_val = mean_absolute_error(Y_val[col], y_pred_val)
        rmse_val = np.sqrt(mean_squared_error(Y_val[col], y_pred_val))
        r2_val = r2_score(Y_val[col], y_pred_val)
        metricas_val[col] = [mae_val, rmse_val, r2_val]

	# Registro en MLflow
        # -----------------------------
        mlflow.log_param("iterations", 500)
        mlflow.log_param("learning_rate", 0.05)
        mlflow.log_param("depth", 8)
        mlflow.log_param("loss_function", "RMSE")
        mlflow.log_param("early_stopping_rounds", 50)
        mlflow.log_param("cat_features_count", len(cat_features))

        mlflow.log_metric("MAE_val", mae_val)
        mlflow.log_metric("RMSE_val", rmse_val)
        mlflow.log_metric("R2_val", r2_val)

        # Guardar modelo
        mlflow.catboost.log_model(modelo, artifact_path=f"CatBoost_{col}")

        print(f"Modelo {col} registrado en MLflow con R²_test = {r2_test:.3f}")
