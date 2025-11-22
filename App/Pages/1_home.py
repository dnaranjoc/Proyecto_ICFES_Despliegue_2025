from dash import html, register_page

#Resgitramos la página
register_page(__name__, path="/", name="Inicio")

#Definimos el layout de la página
layout = html.Div([
    html.H1("SaberInsight", style={'textAlign': 'center', 'color': '#1E3A8A'}),
    html.P("Predicción de resultados Saber Pro", style={'textAlign': 'center'}),
    html.Div(
        [
            html.P("Conoce tus resultados esperados e identifica las áreas que debes fortalecer para un mejor desempeño.",
                   style={'textAlign': 'center', 'color': '#E5E7EB'}),
            #Creamos el botón que nos dirige a la página en donde se recolectarán los datos
            html.A("Calcular mi resultado esperado",
                   href="/prediccion",
                   style={
                       'display': 'block',
                       'margin': '2rem auto',
                       'padding': '1rem 2rem',
                       'backgroundColor': '#F59E0B',
                       'color': 'black',
                       'borderRadius': '10px',
                       'textDecoration': 'none',
                       'textAlign': 'center',
                       'width': 'fit-content'
                   })
        ],
        style={'backgroundColor': '#1E3A8A', 'padding': '3rem', 'borderRadius': '20px'}
    )
])
