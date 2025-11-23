from dash import html, dcc, register_page, callback, Input, Output
from callbacks import map_resultados

register_page(__name__, path="/resultados", name="Resultados")

# FUNCION PARA TARJETAS DE PUNTAJE
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


# LAYOUT PRINCIPAL (vacío, se rellenará con callback)
layout = html.Div(
    [
        #dcc.Store(id="data-prediccion"),
        html.Div(id="contenido-resultados")
    ]
)


# CALLBACK PARA ARMAR LOS RESULTADOS
@callback(
    Output("contenido-resultados", "children"),
    Input("data-prediccion", "data"),
    #prevent_initial_call=True
)
def actualizar_resultados(data):

    if data is None or "prediction" not in data:
        return html.H3("No se recibieron resultados.", style={"textAlign": "center"})

    resultados = data["prediction"]

    # Si vino un error desde el backend, lo mostramos
    if isinstance(resultados, dict) and "error" in resultados:
        return html.Div(
            [
                html.H3("Ocurrió un error al obtener la predicción.", style={"textAlign": "center"}),
                html.P(str(resultados["error"]), style={"textAlign": "center", "color": "red"})
            ]
        )

    # Extraemos puntaje global
    puntaje_global = resultados.get("punt_global", 0)

    # Cálculo simple de percentil (ajustable luego)
    percentil = min(max(int((puntaje_global / 500) * 100), 1), 99)

    # Filtramos SOLO las materias (las claves que tenemos en map_resultados)
    materias = {
        k: v for k, v in resultados.items()
        if k in map_resultados and k != "punt_global"
    }

    # Si por alguna razón no hay materias válidas, mostramos mensaje
    if not materias:
        return html.H3("No se pudieron calcular los puntajes por materia.", style={"textAlign": "center"})

    # Determinar materias más débiles (2 puntajes más bajos)
    materias_ordenadas = sorted(materias.items(), key=lambda x: x[1])
    peores = materias_ordenadas[:2]
    texto_mejora = f"Refuerza tus conocimientos en {map_resultados[peores[0][0]]} y {map_resultados[peores[1][0]]}."

    #  ARMAMOS EL CONTENIDO DINÁMICO
    return html.Div(
        style={
            "backgroundColor": "#F5F5F5",
            "minHeight": "100vh",
            "padding": "20px 40px"
        },
        children=[
            html.H2("Resultados estimados", style={"color": "#1E3A8A"}),

            # BLOQUE SUPERIOR
            html.Div(
                style={"display": "flex", "gap": "20px", "flexWrap": "wrap"},
                children=[
                    # Puntaje global
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
                                html.Span(str(puntaje_global), style={"fontSize": "40px", "fontWeight": "700"}),
                                html.Span("/500", style={"color": "#F97316", "fontWeight": "600", "marginLeft": "4px"})
                            ])
                        ]
                    ),

                    # Percentil
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
                            html.Div("¿En qué percentil estás?", style={"color": "#4B5563", "fontSize": "14px"}),
                            html.Div(
                                style={"marginTop": "16px"},
                                children=[
                                    html.Div(f"{percentil}",
                                             style={"fontSize": "32px", "fontWeight": "700", "color": "#0F172A"}),
                                    html.Div(
                                        f"Tu puntaje superó al {percentil}% de los estudiantes a nivel nacional.",
                                        style={"fontSize": "13px", "color": "#4B5563"}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),

            # BLOQUE PUNTAJES POR MATERIA
            html.H3("Puntaje por pruebas", style={"marginTop": "28px", "color": "#1F2937"}),

            html.Div(
                style={"display": "flex", "gap": "16px", "flexWrap": "wrap"},
                children=[
                    _card_puntaje(map_resultados[k], "📘", v)
                    for k, v in materias.items()  # 
                ]
            ),

            # BLOQUE DE RECOMENDACIÓN
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
                        texto_mejora,
                        style={"fontSize": "16px", "lineHeight": "1.6"}
                    )
                ]
            )
        ]
    )