from dash import html, dcc, register_page

# Registramos la página
register_page(__name__, path="/prediccion", name="Predicción")

# Definimos el layout de la página que contiene los datos que vamos a recolectar
layout = html.Div([
    html.H2("Predicción", style={'textAlign': 'center', 'color': '#1E3A8A'}),

    html.Label("Edad"),
    html.Br(),
    dcc.Input(id="input_edad", type='number', placeholder="Ingresa tu edad"),
    html.Br(),

    html.Label("Género"),
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

    html.Label("Estrato"),
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

    html.Label("Número de personas en el hogar"),
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

    html.Label("Número de personas en el hogar"),
    dcc.Slider(
        id="input_slider_personas",
        min=1,
        max=5,
        step=1,
        value=2,
        marks={
            1: "1 a 2",
            2: "3 a 4",
            3: "5 a 6",
            4: "7 a 8",
            5: "9 o más"
        }
    ),
    html.Br(),

    html.Label("¿En tu casa hay automovil?"),
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

    html.Label("¿En tu casa hay computador?"),
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

    html.Label("¿En tu casa hay servicio de internet?"),
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

    html.Label("¿En tu casa hay lavadora?"),
    dcc.RadioItems(
        id="input_lavadora",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
        ],
        value="Sí",
    ),
    html.Br(),

    html.Label("¿Cuántos cuartos hay en tu hogar?"),
    dcc.Slider(
        id="input_cuartos",
        min=1, max=4, step=1, value=3,
        marks={i: str(i) for i in range(1, 7)}
    ),
    html.Br(),

    html.Label("¿Tu mamá tiene educación profesional?"),
    dcc.RadioItems(
        id="input_educmadre",
        options=[{"label": "Sí", "value": "Sí"}, {"label": "No", "value": "No"}],
        value="Sí",
    ),
    html.Br(),

    html.Label("¿Tu papá tiene educación profesional?"),
    dcc.RadioItems(
        id="input_educpadre",
        options=[{"label": "Sí", "value": "Sí"}, {"label": "No", "value": "No"}],
        value="Sí",
    ),
    html.Br(),

    html.Label("Jornada del colegio"),
    dcc.RadioItems(
        id="input_jornada",
        options=[
            {"label": "Parcial diurna", "value": "Parcial diurna"},
            {"label": "Parcial flexible", "value": "Parcial flexible"},
            {"label": "Única", "value": "Única"},
        ],
        value="Única",
    ),
    html.Br(),

    html.Label("Colegio calendario"),
    dcc.RadioItems(
        id="input_calendario",
        options=[
            {"label": "A", "value": "A"},
            {"label": "B", "value": "B"},
            {"label": "Otro", "value": "Otro"},
        ],
        value="A",
    ),
    html.Br(),

    html.Label("Colegio Bilingüe"),
    dcc.RadioItems(
        id="input_bilingue",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
            {"label": "No Reporta", "value": "No Reporta"},
        ],
        value="No Reporta",
    ),
    html.Br(),

    html.Label("Ubicación del Colegio"),
    dcc.RadioItems(
        id="input_ubicacion",
        options=[
            {"label": "Rural", "value": "Rural"},
            {"label": "Urbano", "value": "Urbano"},
        ],
        value="Urbano",
    ),
    html.Br(),

    html.Label("Caracter del Colegio"),
    dcc.RadioItems(
        id="input_caracter",
        options=[
            {"label": "Académico", "value": "Académico"},
            {"label": "Técnico", "value": "Técnico"},
            {"label": "Técnico/Académico", "value": "Técnico/Académico"},
            {"label": "No aplica", "value": "No aplica"},
        ],
        value="Académico",
    ),
    html.Br(),

    html.Label("Género del Colegio"),
    dcc.RadioItems(
        id="input_generocolegio",
        options=[
            {"label": "Mixto", "value": "Mixto"},
            {"label": "Femenino", "value": "Femenino"},
            {"label": "Masculino", "value": "Masculino"},
        ],
        value="Mixto",
    ),
    html.Br(),

    html.Label("Naturaleza del Colegio"),
    dcc.RadioItems(
        id="input_naturaleza",
        options=[
            {"label": "Oficial", "value": "Oficial"},
            {"label": "No oficial", "value": "No oficial"},
        ],
        value="Oficial",
    ),
    html.Br(),

    html.Label("¿Estudias en la sede principal del Colegio?"),
    dcc.RadioItems(
        id="input_sedeprincipal",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
        ],
        value="Sí",
    ),
    html.Br(),

    html.Label("¿Vives en el mismo municipio donde estudias?"),
    dcc.RadioItems(
        id="input_mun_colegio",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
        ],
        value="Sí",
    ),
    html.Br(),

    html.Label("¿Vives en el mismo municipio donde vas a presentar la prueba?"),
    dcc.RadioItems(
        id="input_mun_prueba",
        options=[
            {"label": "Sí", "value": "Sí"},
            {"label": "No", "value": "No"},
        ],
        value="Sí",
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

