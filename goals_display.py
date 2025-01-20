from random import random

from dash import Dash, html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc

import calculate
import data
from data import config

is_shown = False

def get_goals_card_body():
    # Tabellarische Daten
    data = calculate.calculate_goals_probabilities()
    calculate.calculate_overall_success()

    # Layout
    return dbc.Card([dbc.CardBody(
                    [
                        html.H4(f"Overall Success Rate: {config.get_success_rate()}%", className="card-title"),
                        dbc.Progress(value=config.get_success_rate()),
                        html.P(f"Status: {"On Track" if config.get_success_rate() >= 75 else "Needs Improvement"}", className="card-text"),
                        html.Hr(),
                        # Ausklapp-Button
                        dbc.Button(
                            "Show/Hide goals and Probabilities",
                            id="toggle-collapse-goals",
                            className="mb-2",
                            color="info",
                            n_clicks=0,
                        ),
                        # Ausklappbarer Bereich
                        dbc.Collapse(
                            dbc.Table.from_dataframe(data, striped=True, bordered=True, hover=True),
                            id="collapse-goals",
                            is_open=is_shown,  # Standardmäßig eingeklappt
                        ),
                    ]
                )],
                 id="goals-card",
                 style={
                    "position": "fixed",
                    "top": "10px",
                    "right": "10px",
                    "width": "400px",
                    "padding": "10px",
                    "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                    "zIndex": 1000,
                }
                 )

def register_goals_display_callbacks(app):
    # Callback zum Ein-/Ausklappen
    @app.callback(
        Output("collapse-goals", "is_open"),
        Input("toggle-collapse-goals", "n_clicks"),
        [State("collapse-goals", "is_open")],
    )
    def toggle_collapse(n_clicks, is_open):
        global is_shown
        if n_clicks:
            is_shown=not is_open
            return not is_open
        is_shown = is_open
        return is_open

    # Simulation Callback für Meilensteine
    @app.callback(
        [Output("goals-card", "children", allow_duplicate=True)],
        [
            Input(f"milestones-checklist-{index}", "value")
            for index in range(len(config.iteration_milestone))
        ]+
        [
            Input(f"{key.replace(' ', '-').lower()}-slider", "value")
            for key in config.kpi_data.keys()
        ],
        prevent_initial_call=True
    )
    def update_simulation(*inputs):
        # Meilensteine und Slider-Werte aus den Inputs extrahieren
        num_iterations = len(config.iteration_milestone)
        milestones_achieved = inputs[:num_iterations]  # Erste Inputs sind Meilenstein-Werte
        slider_values = inputs[num_iterations:]  # Danach kommen die Slider-Werte

        # Aktualisiere die Meilenstein-Konfiguration
        calculate.calculate_milestones_achieved(milestones_achieved)

        # Aktualisiere Slider-Werte in config.kpi_data
        slider_keys = list(config.kpi_data.keys())
        for key, value in zip(slider_keys, slider_values):
            config.kpi_data[key] = value

        # Rückgabe des aktualisierten Goals-Card-Inhalts
        return [get_goals_card_body()]
