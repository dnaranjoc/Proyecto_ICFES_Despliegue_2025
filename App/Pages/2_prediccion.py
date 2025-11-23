from dash import html, dcc, register_page

# Registramos la página
register_page(__name__, path="/prediccion", name="Predicción")

# Definimos el layout de la página que contiene los datos que vamos a recolectar
layout = html.Div([
    html.H2("Predicción", style={'textAlign': 'center', 'color': '#1E3A8A'}),

    html.Label("Edad", style={"fontSize": "17px", "fontWeight": "bold"}),
    html.Br(),
    dcc.Input(id="input_edad", type='number', placeholder="Ingresa tu edad"),
    html.Br(),

    html.Label("Género", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_genero",
        options=[
            {"label": "Femenino",   "value": "Femenino"},
            {"label": "Masculino",  "value": "Masculino"},
        ],
        value="Femenino",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("Estrato", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_estrato",
        options=[
            {"label": "Estrato 1", "value": "Estrato 1"},
            {"label": "Estrato 2", "value": "Estrato 2"},
            {"label": "Estrato 3", "value": "Estrato 3"},
            {"label": "Estrato 4", "value": "Estrato 4"},
            {"label": "Estrato 5", "value": "Estrato 5"},
            {"label": "Estrato 6", "value": "Estrato 6"},
            {"label": "Sin estrato", "value": "Sin estrato"},
        ],
        value="Estrato 3",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("Número de personas en el hogar", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_personashogar",
        options=[
            {"label": "1 a 2", "value": "1 a 2"},
            {"label": "3 a 4", "value": "3 a 4"},
            {"label": "5 a 6", "value": "5 a 6"},
            {"label": "7 a 8", "value": "7 a 8"},
            {"label": "9 o más", "value": "9 o más"},
        ],
        value="3 a 4",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("¿En tu casa hay automovil?", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_automovil",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
        ],
        value="Sí",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("¿En tu casa hay computador?", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_computador",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
        ],
        value="Sí",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("¿En tu casa hay servicio de internet?", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_internet",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
        ],
        value="Sí",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("¿En tu casa hay lavadora?", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_lavadora",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
        ],
        value="Sí",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("¿Cuántos cuartos hay en tu hogar?", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_cuartos",
        options=[
            {"label": "Uno", "value": "Uno"},
            {"label": "Dos", "value": "Dos"},
            {"label": "Tres", "value": "Tres"},
            {"label": "Cuatro", "value": "Cuatro"},
            {"label": "Cinco", "value": "Cinco"},
            {"label": "Seis o más", "value": "Seis o más"},
        ],
        value="Tres",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("Nivel de educación de la madre", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_educmadre",
        options=[
            {"label": "Ninguna", "value": "Ninguna"},
            {"label": "Primaria incompleta", "value": "Primaria incompleta"},
            {"label": "Primaria completa", "value": "Primaria completa"},
            {"label": "Bachillerato incompleto", "value": "Bachillerato incompleto"},
            {"label": "Bachillerato completo", "value": "Bachillerato completo"},
            {"label": "Técnica incompleta", "value":"Técnica incompleta"},
            {"label": "Técnica completa", "value": "Técnica completa"},
            {"label": "Educación profesional incompleta", "value": "Educación profesional incompleta"},
            {"label": "Educación profesional completa", "value": "Educación profesional completa"},
            {"label": "Postgrado", "value": "Postgrado"},
        ],
        value="Educación profesional completa",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("Nivel de educación del padre", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_educpadre",
        options=[
            {"label": "Ninguna", "value": "Ninguna"},
            {"label": "Primaria incompleta", "value": "Primaria incompleta"},
            {"label": "Primaria completa", "value": "Primaria completa"},
            {"label": "Bachillerato incompleto", "value": "Bachillerato incompleto"},
            {"label": "Bachillerato completo", "value": "Bachillerato completo"},
            {"label": "Técnica incompleta", "value": "Técnica incompleta"},
            {"label": "Técnica completa", "value": "Técnica completa"},
            {"label": "Educación profesional incompleta", "value": "Educación profesional incompleta"},
            {"label": "Educación profesional completa", "value": "Educación profesional completa"},
            {"label": "Postgrado", "value": "Postgrado"},
        ],
        value="Educación profesional completa",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("Jornada del colegio", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_jornada",
        options=[
            {"label": "Parcial diurna", "value": "Parcial diurna"},
            {"label": "Parcial flexible", "value": "Parcial flexible"},
            {"label": "Única", "value": "Única"},
        ],
        value="Única",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("Colegio calendario", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_calendario",
        options=[
            {"label": "A", "value": "A"},
            {"label": "B", "value": "B"},
            {"label": "Otro", "value": "Otro"},
        ],
        value="A",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("Colegio Bilingüe", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_bilingue",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
            {"label": "No Reporta", "value": "No Reporta"},
        ],
        value="No Reporta",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("Ubicación del Colegio", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_ubicacion",
        options=[
            {"label": "Rural", "value": "Rural"},
            {"label": "Urbano", "value": "Urbano"},
        ],
        value="Urbano",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("Caracter del Colegio", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_caracter",
        options=[
            {"label": "Académico", "value": "Académico"},
            {"label": "Técnico", "value": "Técnico"},
            {"label": "Técnico/Académico", "value": "Técnico/Académico"},
            {"label": "No aplica", "value": "No aplica"},
        ],
        value="Académico",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("Género del Colegio", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_generocolegio",
        options=[
            {"label": "Mixto", "value": "Mixto"},
            {"label": "Femenino", "value": "Femenino"},
            {"label": "Masculino", "value": "Masculino"},
        ],
        value="Mixto",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("Naturaleza del Colegio", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_naturaleza",
        options=[
            {"label": "Oficial", "value": "Oficial"},
            {"label": "No oficial", "value": "No oficial"},
        ],
        value="Oficial",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("¿Estudias en la sede principal del Colegio?", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_sedeprincipal",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
        ],
        value="Sí",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("¿Vives en el mismo municipio donde estudias?", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_mun_colegio",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
        ],
        value="Sí",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    html.Label("¿Vives en el mismo municipio donde vas a presentar la prueba?", style={"fontSize": "17px", "fontWeight": "bold"}),
    dcc.RadioItems(
        id="input_mun_prueba",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
        ],
        value="Sí",
        labelStyle={"display": "inline-block", "padding": "6px 10px"},
        inputStyle={"margin-right": "6px"},
    ),
    html.Br(),

    # BOTÓN QUE EJECUTA PREDICCIÓN
    html.Button(
        "Predecir mi Resultado",
        id="btn-predict",
        n_clicks=0,
        style={
            'display': 'block', 'margin': '2rem auto',
            'padding': '1rem 2rem', 'backgroundColor': '#F59E0B',
            'color': 'black', 'borderRadius': '10px',
            'width': 'fit-content'
        }
    ),

    html.Br(),

    #Guardamos y redirigimos
    dcc.Store(id="data-prediccion"),
    dcc.Location(id="redirect-resultados", refresh=True)

])