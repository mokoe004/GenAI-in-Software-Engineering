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

    # Layout
    return dbc.Card([dbc.CardBody(
                    [
                        html.H4(f"Overall Success Rate: {config.success_rate}%", className="card-title"),
                        dbc.Progress(value=config.success_rate),
                        html.P(f"Status: {"On Track" if config.success_rate >= 75 else "Needs Improvement"}", className="card-text"),
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

    # Simulation
    @app.callback(
        [Output("goals-card", "children")],
        [Input("milestones-checklist", "value")]+
        [
            Input(f"{key.replace(' ', '-').lower()}-slider", "value")
            for key in config.kpi_data.keys()
        ],
        prevent_initial_call=True
    )
    def update_simulation(milestones_achieved, *slider_values):
        # Update config values based on slider inputs
        slider_keys = list(config.kpi_data.keys())  # Get the keys for easier mapping

        # Map slider values to config.kpi_data
        for key, value in zip(slider_keys, slider_values):
            config.kpi_data[key] = value

        return [get_goals_card_body()]
