from dash import html, dcc, register_page

# Registramos la página
register_page(__name__, path="/resultados", name="Resultados")

# Creamos una función para deplegar los puntajes de cada materia
def _card_puntaje(nombre, icono, puntaje):
    return html.Div(
        style={
            "backgroundColor": "white",
            "borderRadius": "14px",
            "padding": "14px 16px",
            "minWidth": "180px",
            "boxShadow": "0 2px 6px rgba(0,0,0,0.03)"
        },
        children=[
            html.Div([
                html.Span(icono, style={"marginRight": "6px"}),
                html.Span(nombre, style={"fontWeight": "600", "fontSize": "14px"})
            ]),
            html.Div(
                [
                    html.Span(f"{puntaje}", style={"fontSize": "26px", "fontWeight": "700", "color": "#111827"}),
                    html.Span("/100", style={"color": "#9CA3AF", "marginLeft": "4px"})
                ],
                style={"marginTop": "8px"}
            )
        ]
    )


# Definimos el layout principal de la página
layout = html.Div(
    style={
        "backgroundColor": "#F5F5F5",
        "minHeight": "100vh",
        "padding": "20px 40px",
        "fontFamily": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    },
    children=[
        html.H2(
            "Resultados estimados",
            style={"color": "#1E3A8A", "marginBottom": "20px"}
        ),

        # Diseñamos la sección superior que contiene el puntaje global y el percentil
        html.Div(
            style={"display": "flex", "gap": "20px", "flexWrap": "wrap"},
            children=[
                html.Div(
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "12px",
                        "padding": "16px 20px",
                        "flex": "0 0 280px",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"
                    },
                    children=[
                        html.Div("Puntaje global", style={"color": "#4B5563", "fontSize": "14px"}),
                        html.Div([
                            html.Span("352", style={"fontSize": "40px", "fontWeight": "700", "color": "#111827"}),
                            html.Span("/500", style={"color": "#F97316", "fontWeight": "600", "marginLeft": "4px"})
                        ], style={"margin": "8px 0 16px 0"}),

                    ]
                ),

                html.Div(
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "12px",
                        "padding": "16px 20px",
                        "flex": "1",
                        "minWidth": "300px",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"
                    },
                    children=[
                        html.Div("¿En qué percentiles estás?", style={"color": "#4B5563", "fontSize": "14px"}),
                        html.Div(
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "space-between",
                                "marginTop": "16px",
                                "gap": "20px"
                            },
                            children=[
                                html.Div(
                                    style={"flex": 1},
                                    children=[
                                        html.Div("Estudiantes a nivel nacional", style={"fontSize": "13px"}),
                                        html.Div(
                                            style={
                                                "height": "10px",
                                                "backgroundColor": "#E5E7EB",
                                                "borderRadius": "9999px",
                                                "marginTop": "10px",
                                                "overflow": "hidden"
                                            },
                                            children=html.Div(
                                                style={
                                                    "width": "70%",
                                                    "height": "100%",
                                                    "background": "linear-gradient(90deg, #0EA5E9, #1D4ED8)",
                                                }
                                            )
                                        )
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Div("70", style={"fontSize": "32px", "fontWeight": "700", "color": "#0F172A"}),
                                        html.Div(
                                            "Tu puntaje superó al 70% de los estudiantes a nivel nacional.",
                                            style={"fontSize": "12px", "color": "#4B5563", "maxWidth": "180px"}
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),

        # Diseñamos la sección en donde desplegaremos el puntaje de cada materia
        html.H3("Puntaje por pruebas", style={"marginTop": "28px", "marginBottom": "14px", "color": "#1F2937"}),

        html.Div(
            style={"display": "flex", "gap": "16px", "flexWrap": "wrap"},
            children=[
                _card_puntaje("Lectura Crítica", "📚", 90),
                _card_puntaje("Matemáticas", "🧮", 78),
                _card_puntaje("Sociales y Ciudadanas", "🤝", 55),
                _card_puntaje("Ciencias Naturales", "🌿", 73),
                _card_puntaje("Inglés", "Hi", 62),
            ]
        ),

        # En esta sección incluimos las recomendaciones para mejorar
        html.Div(
            style={
                "backgroundColor": "white",
                "borderRadius": "12px",
                "padding": "20px",
                "marginTop": "28px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.04)"
            },
            children=[
                html.P(
                    '"Vas por muy buen camino. Para lograr un mejor desempeño, refuerza tus conocimientos en "Sociales y ciudadanas e Inglés."',
                    style={"fontSize": "16px", "lineHeight": "1.6"}
                )
            ]
        )
    ]
)