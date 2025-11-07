from dash import html, dcc, register_page
import plotly.express as px
import pandas as pd

register_page(__name__, path="/resultados", name="Resultados")

df = pd.DataFrame({
    "Módulo": ["Lectura Crítica", "Inglés", "Matemáticas", "C. Sociales", "C. Naturales"],
    "Puntaje": [100, 230, 150, 180, 160]
})

fig = px.bar(df, x="Módulo", y="Puntaje", range_y=[0, 300],
             color_discrete_sequence=["#6D28D9"])

layout = html.Div([
    html.H2("Puntaje Estimado", style={'textAlign': 'center', 'color': '#1E3A8A'}),
    dcc.Graph(figure=fig),
    html.Div([
        html.H4("Recomendaciones", style={'color': 'white'}),
        html.P("Vas por muy buen camino. Para lograr un mejor desempeño, "
               "refuerza tus conocimientos en Lectura Crítica y Matemáticas.",
               style={'color': 'white'})
    ], style={'backgroundColor': '#1E3A8A', 'borderRadius': '15px', 'padding': '1rem'})
])
