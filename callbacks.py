from dash import callback, Input, Output, State
import requests
import dash

# 1. URL DEL MODELO (se debe ajustar)
API_URL = "https://TU_API_EN_RAILWAY/predict"
# Ejemplo futuro:
# API_URL = "https://icfes-model-app-production.up.railway.app/predict"

# 2. Diccionarios de mapeo valores UI → modelo
map_si_no = {"Sí": "Si", "No": "No"}
map_binario = {"Sí": 1, "No": 0}
map_ubicacion = {"Rural": "RURAL", "Urbano": "URBANO"}
map_bilingue = {
    "Sí": "S",
    "No": "N",
    "No Reporta": "No_reporta"
}
map_calendario = {"A": "A", "B": "B", "Otro": "OTRO"}
map_caracter = {
    "Académico": "ACADÉMICO",
    "Técnico": "TÉCNICO",
    "Técnico/Académico": "TÉCNICO/ACADÉMICO",
    "No aplica": "NO APLICA"
}
map_genero_colegio = {
    "Mixto": "MIXTO",
    "Femenino": "FEMENINO",
    "Masculino": "MASCULINO"
}
map_colegio_naturaleza = {
    "Oficial": "OFICIAL",
    "No oficial": "NO OFICIAL",
}
map_genero_estudiante = {"Femenino": "F", "Masculino": "M"}
map_jornada = {
    "Unica": "Unica",
    "Parcial diurna": "Parcial_Diurna",
    "Parcial flexible": "Parcial_Flexible"
}
map_personas_hogar = {
    "1 a 2": "1 a 2",
    "3 a 4": "3 a 4",
    "5 a 6": "5 a 6",
    "7 a 8": "7 a 8",
    "9 o más": "9 o más"
}

map_resultados = {
    "punt_ingles": "Inglés",
    "punt_matematicas": "Matemáticas",
    "punt_sociales_ciudadanas": "Sociales y Ciudadanas",
    "punt_c_naturales": "Ciencias Naturales",
    "punt_lectura_critica": "Lectura Crítica",
    "punt_global": "Puntaje Global"
}


# 3. Callback principal que construye el JSON y lo envía al API
@callback(
    Output("data-prediccion", "data"),
    Input("btn-predict", "n_clicks"),

    State("input_edad", "value"),
    State("input_genero", "value"),
    State("input_estrato", "value"),
    State("input_personashogar", "value"),
    State("input_automovil", "value"),
    State("input_computador", "value"),
    State("input_internet", "value"),
    State("input_lavadora", "value"),
    State("input_cuartos", "value"),
    State("input_educmadre", "value"),
    State("input_educpadre", "value"),
    State("input_jornada", "value"),
    State("input_calendario", "value"),
    State("input_bilingue", "value"),
    State("input_ubicacion", "value"),
    State("input_caracter", "value"),
    State("input_generocolegio", "value"),
    State("input_naturaleza", "value"),     # ← CORRECCIÓN 1: estaba faltando
    State("input_sedeprincipal", "value"),
    State("input_mun_colegio", "value"),
    State("input_mun_prueba", "value"),

    prevent_initial_call=True
)
def procesar_prediccion(
    n, edad, genero, estrato, personas, auto, compu, internet, lavadora,
    cuartos, educ_madre, educ_padre, jornada, calendario, bilingue,
    ubicacion, caracter, genero_colegio, naturaleza,
    sede_principal, mun_colegio, mun_prueba
):

    # 4. Convertir valores al formato del modelo

    datos_modelo = {
        "cole_area_ubicacion": map_ubicacion[ubicacion],
        "cole_bilingue": map_bilingue[bilingue],
        "cole_calendario": map_calendario[calendario],
        "cole_caracter": map_caracter[caracter],
        "cole_genero": map_genero_colegio[genero_colegio],

        "cole_naturaleza": map_colegio_naturaleza[naturaleza],   # ← CORRECCIÓN 2

        "cole_sede_principal": map_si_no[sede_principal],
        "estu_genero": map_genero_estudiante[genero],
        "fami_estratovivienda": estrato,
        "fami_personashogar": map_personas_hogar[personas],
        "fami_tieneautomovil": map_si_no[auto],
        "fami_tienecomputador": map_si_no[compu],
        "fami_tieneinternet": map_si_no[internet],
        "fami_tienelavadora": map_si_no[lavadora],
        "estu_edad_anios": edad,
        "mismo_municipio_prueba": map_binario[mun_prueba],
        "mismo_municipio_colegio": map_binario[mun_colegio],
        "cole_jornada_cat": map_jornada[jornada],
        "fami_cuartoshogar_num": cuartos,
        "fami_educacionmadre_num": map_binario[educ_madre],
        "fami_educacionpadre_num": map_binario[educ_padre],
    }

    # 5. Enviar al API
    try:
        response = requests.post(API_URL, json=datos_modelo)
        response.raise_for_status()
        prediccion = response.json()

    except Exception as e:
        prediccion = {"error": str(e)}

    # 6. Enviar resultados a la página RESULTADOS
    return {
        "inputs": datos_modelo,
        "prediction": prediccion
    }

# CALLBACK PARA REDIRIGIR AUTOMÁTICAMENTE A /resultados
@callback(
    Output("redirect-resultados", "href"),
    Input("data-prediccion", "data"),
    prevent_initial_call=True
)
def ir_a_resultados(data):
    if data is None:
        return dash.no_update
    return "/resultados"