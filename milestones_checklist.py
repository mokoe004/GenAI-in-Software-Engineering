from modal import get_modal_button
from data import config
from goals_display import get_goals_card_body

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

import pandas as pd


def get_milestones_checklist():
    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    get_single_milestone(iteration, iteration_index),
                    width=3,  # Breite jeder Karte (kann angepasst werden, z. B. 4 für breitere Karten)
                )
                for iteration_index, iteration in enumerate(config.iteration_milestone)
            ],
            justify="start",  # Andere Optionen: "center", "end", "between", "around"
        ),
        fluid=True,
    )

def get_single_milestone(iteration, iteration_index):
    return dbc.Card(
        dbc.CardHeader(
            [html.H4(iteration["iteration"]),
             dbc.CardBody(
                 [
                     dbc.Checklist(
                         id=f"milestones-checklist-{iteration_index}",
                         options=[{"label": milestone, "value": milestone}
                                  for milestone in iteration["milestones"]],
                         value=[],
                         inline=True
                     )
                 ]
             )]
        ))
