from dash import callback, Input, Output, State
import requests
import dash

from config import settings
# Usamos la URL desde la configuración
API_URL = settings.ICFES_API_URL

# 2. Diccionarios de mapeo valores UI → modelo
map_si_no = {"Sí": "S", "No": "N"}
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
map_genero_estudiante = {"Femenino": "1", "Masculino": "0"}
map_jornada = {
    "Unica": "Unica",
    "Parcial diurna": "Parcial_Diurna",
    "Parcial flexible": "Parcial_Flexible"
}
map_personas_hogar = {
    "1 a 2": "1",
    "3 a 4": "2",
    "5 a 6": "3",
    "7 a 8": "4",
    "9 o más": "5"
}

map_estrato = {
    "Sin estrato": "0",
    "Estrato 1": "1",
    "Estrato 2": "2",
    "Estrato 3": "3",
    "Estrato 4": "4",
    "Estrato 5": "5",
    "Estrato 6": "6"
}

map_cuartos = {
    "Uno": "1",
    "Dos": "2",
    "Tres": "3",
    "Cuatro": "4",
    "Cinco": "5",
    "Seis o más": "6"
}

map_educacicon = {
    "Ninguna": "0",
    "Primaria incompleta": "1",
    "Primaria completa": "2",
    "Bachillera incompleto": "3",
    "Bachillera completo": "4",
    "Técnica incompleta": "5",
    "Técnica completa": "6",
    "Educación profesional incompleta": "7",
    "Educación profesional completa": "8",
    "Postgrado": "9"
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
    State("input_naturaleza", "value"),
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
        "cole_naturaleza": map_colegio_naturaleza[naturaleza],
        "cole_sede_principal": map_si_no[sede_principal],
        "estu_genero_M": map_genero_estudiante[genero],
        "fami_estratovivienda": map_estrato[estrato],
        "fami_personashogar": map_personas_hogar[personas],
        "fami_tieneautomovil": map_binario[auto],
        "fami_tienecomputador": map_binario[compu],
        "fami_tieneinternet": map_binario[internet],
        "fami_tienelavadora": map_binario[lavadora],
        "estu_edad_anios": edad,
        "mismo_municipio_prueba": map_binario[mun_prueba],
        "mismo_municipio_colegio": map_binario[mun_colegio],
        "cole_jornada_cat": map_jornada[jornada],
        "fami_cuartoshogar_num": map_cuartos[cuartos],
        "fami_educacionmadre_num": map_educacicon[educ_madre],
        "fami_educacionpadre_num": map_educacicon[educ_padre],
    }

    # 5. Enviar al API
    try:
        response = requests.post(API_URL, json=datos_modelo)
        response.raise_for_status()
        prediccion = response.json()

        if isinstance(prediccion, dict) and "punt_lectura_critica" in prediccion:
            lectura = prediccion["punt_lectura_critica"]
            mate = prediccion["punt_matematicas"]
            sociales = prediccion["punt_sociales_ciudadanas"]
            c_nat = prediccion["punt_c_naturales"]
            ingles = prediccion["punt_ingles"]

            # Fórmula del puntaje global:
            # ((lectura*3 + mate*3 + sociales*3 + c_nat*3 + ingles) / 13) * 5
            punt_global = ((lectura * 3
                            + mate * 3
                            + sociales * 3
                            + c_nat * 3
                            + ingles) / 13) * 5

            # Lo agregamos al diccionario de predicción
            prediccion["punt_global"] = punt_global

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