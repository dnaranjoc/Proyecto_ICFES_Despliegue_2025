from dash import html, dcc, register_page

register_page(__name__, path="/prediccion", name="Predicción")

layout = html.Div([
    html.H2("Predicción", style={'textAlign': 'center', 'color': '#1E3A8A'}),
    html.Label("Edad"),
    dcc.Input(type='number', placeholder="Ingresa tu edad"),
    html.Br(),
    html.Label("Estrato"),
    dcc.Dropdown(options=[1, 2, 3, 4, 5, 6]),
    html.Br(),
    html.Label("Jornada del colegio"),
    dcc.Dropdown(options=["Noche", "Mañana", "Sabatina", "Completa", "Única", "Tarde"]),
    html.Br(),
    html.Label("Colegio calendario"),
    dcc.Dropdown(options=["A", "B", "Otro"]),
    html.Br(),
    html.Label("Colegio Bilingüe"),
    dcc.Dropdown(options=["Sí", "No"]),
    html.Br(),
    html.Label("¿Cuántas horas dedicas a estudiar semanalmente?"),
    dcc.Dropdown(options=["Más de 30 horas", "Entre 11 y 20 horas", "0 horas", "Entre 21 y 30 horas"]),
    html.Br(),
    html.Label("En promedio ¿cuántos libros te lees anualmente"),
    dcc.Dropdown(options=["Entre 0 y 10 libros", "Entre 11 y 25 libros", "Entre 26 y 100 libros", "Más de 100 libros"]),
    html.Br(),
    html.Label("Educación del padre"),
    dcc.Dropdown(options=["Ninguno", "Técnica", "Profesional", "Postgrado", "Escolar"]),
    html.Br(),
    html.Label("Educación de la madre"),
    dcc.Dropdown(options=["Ninguno", "Técnica", "Profesional", "Postgrado", "Escolar"]),
    html.Br(),
    html.Label("¿Tu familia tiene automovil?"),
    dcc.Dropdown(options=["Sí", "No"]),
    html.Br(),
    html.A("Predecir mi Resultado", href="/resultados",
           style={
               'display': 'block', 'margin': '2rem auto',
               'padding': '1rem 2rem', 'backgroundColor': '#F59E0B',
               'color': 'black', 'borderRadius': '10px', 'width': 'fit-content',
               'textDecoration': 'none'
           })
])
