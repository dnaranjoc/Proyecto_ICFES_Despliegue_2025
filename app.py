from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "SaberInsight"

app.layout = html.Div([
    dbc.NavbarSimple(
        brand="SaberInsight",
        color="#1E3A8A",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink("Inicio", href="/")),
            dbc.NavItem(dbc.NavLink("Predicción", href="/prediccion")),
            dbc.NavItem(dbc.NavLink("Resultados", href="/resultados")),
        ],
        class_name="mb-4"
    ),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)

