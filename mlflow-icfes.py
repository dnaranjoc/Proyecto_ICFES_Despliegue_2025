# Para la importación de los datos desde Socrata
from sodapy     import Socrata

import csv
from datetime   import datetime
import pandas   as pd
import numpy    as np
import warnings
import scipy.stats as stats
import math

#Para gráficos y mapas de calor
import seaborn            as sb
import matplotlib.pyplot  as plt
import plotly.graph_objs  as go

#Para la imputación de los datos
from sklearn.impute     import SimpleImputer
from sklearn.compose    import ColumnTransformer
import missingno        as msno

#Para el pre-procesamiento de los datos
from sklearn.preprocessing      import LabelEncoder, OrdinalEncoder, OneHotEncoder
from sklearn.feature_selection  import SelectKBest, chi2


#Para generar los modelos
from sklearn.model_selection    import train_test_split
from sklearn.linear_model       import LinearRegression, LogisticRegression
from sklearn.neighbors          import KNeighborsClassifier
from sklearn.metrics            import mean_squared_error, r2_score, classification_report, confusion_matrix
import statsmodels.api          as sm
import statsmodels.formula.api  as smf

# Para herramienta de interactividad
import ipywidgets     as widgets
from ipywidgets       import interact, interactive, fixed, interact_manual
from ipywidgets       import HBox, VBox
import panel          as pn
from IPython.display  import display, clear_output

# Suprimir los warnings específicos
warnings.filterwarnings("ignore")

#Códigos de Socrata para acceder a los datos de cada periodo
codes = {"2020-1":"a8xr-en99" , "2020-2":"rnvb-vnyh"} #"2019-2":"ynam-yc42" ,
client = Socrata("www.datos.gov.co", None)
limit = 80000  #Límite de filas que se importará

datos = {}

for periodo, codigo in codes.items():
  datos[periodo] = pd.DataFrame.from_records(client.get(codigo, limit = limit))

#Para agregar todo en un dataframe primero se valida qué columnas son comunes

columnas_comunes = set(datos['2020-1'].columns)
for key, df in datos.items():
    columnas_comunes.intersection_update(df.columns)

columnas_comunes = list(columnas_comunes)
print("Las columnas comunes entre los distintos periodos son: "+ str(columnas_comunes))

# Filtramos cada DataFrame para conservar solo las columnas comunes y agregamos la columna "periodo"
dataframes_filtrados = []

for key, df in datos.items():
    df_filtrado = df[columnas_comunes].copy()
    df_filtrado['periodo'] = key
    dataframes_filtrados.append(df_filtrado)

# Concatenamos los DataFrames filtrados en un único DataFrame
df_unico = pd.concat(dataframes_filtrados, ignore_index=True)

# Convertir la columna 'estu_fechanacimiento' a tipo datetime
df_unico['estu_fechanacimiento'] = pd.to_datetime(df_unico['estu_fechanacimiento'], format='%Y-%m-%dT%H:%M:%S.%f', errors='coerce')

# Clasificar las columnas en numéricas y categóricas
numericas = df_unico.select_dtypes(include=[np.number]).columns.tolist()
categoricas = df_unico.select_dtypes(include=[object]).columns.tolist()

# Identificar las columnas que contienen "_cod_" o "_codigo_"
cod_columns = [col for col in numericas if '_cod_' in col or '_codigo_' in col]

# Mover estas columnas de la lista de columnas numéricas a la lista de columnas categóricas
for col in cod_columns:
    numericas.remove(col)
    categoricas.append(col)

# Seleccionar las columnas de "cole" que no son códigos, exceptuando 'cole_cod_dane_sede'
cole_columns = [col for col in clasificacion_variables['cole'] if 'cod' not in col.lower() and 'codigo' not in col.lower() or col == 'cole_cod_dane_sede']

# Seleccionar las columnas específicas de "fami" y "estu"
fami_columns = ['fami_situacioneconomica', 'fami_estratovivienda', 'fami_trabajolabormadre', 'fami_trabajolaborpadre']
estu_columns = ['estu_fechanacimiento','estu_genero']

# Combinar todas las columnas seleccionadas en una lista
columnas_a_conservar = clasificacion_variables['punt'] + cole_columns + fami_columns + estu_columns

# Filtrar el DataFrame original para conservar solo las columnas especificadas
df_filtrado = df_unico[columnas_a_conservar]

# Transformar la columna de fecha de nacimiento a Edad, y sacar la de Nacimiento del listado
# Calcular la edad en años
fecha_examen = pd.to_datetime("01/07/2020")
df_filtrado['estu_edad_anios'] = (fecha_examen - df_filtrado['estu_fechanacimiento']).dt.days // 365.25

# Eliminar la columna 'estu_fechanacimiento'
df_filtrado = df_filtrado.drop(columns=['estu_fechanacimiento'])



#Importe MLFlow para registrar los experimentos, el regresor de bosques aleatorios y la métrica de error cuadrático medio
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# defina el servidor para llevar el registro de modelos y artefactos
mlflow.set_tracking_uri('http://localhost:5000')
# registre el experimento
experiment = mlflow.set_experiment("randomforest-icfes")

# Aquí se ejecuta MLflow sin especificar un nombre o id del experimento. MLflow los crea un experimento para este cuaderno por defecto y guarda las características del experimento y las métricas definidas. 
# Para ver el resultado de las corridas haga click en Experimentos en el menú izquierdo. 
with mlflow.start_run(experiment_id=experiment.experiment_id):
    # defina los parámetros del modelo
    n_estimators = 200 
    max_depth = 6
    max_features = 4
    # Cree el modelo con los parámetros definidos y entrénelo
    rf = RandomForestRegressor(n_estimators = n_estimators, max_depth = max_depth, max_features = max_features)
    rf.fit(X_train, y_train)
    # Realice predicciones de prueba
    predictions = rf.predict(X_test)
  
    # Registre los parámetros
    mlflow.log_param("num_trees", n_estimators)
    mlflow.log_param("maxdepth", max_depth)
    mlflow.log_param("max_feat", max_features)
  
    # Registre el modelo
    mlflow.sklearn.log_model(rf, "random-forest-model")
  
    # Cree y registre la métrica de interés
    mse = mean_squared_error(y_test, predictions)
    mlflow.log_metric("mse", mse)
    print(mse)