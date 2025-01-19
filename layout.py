from modal import get_modal_button
from data import config
from goals_display import get_goals_card_body

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

import pandas as pd


# Layout
def create_layout():
    """
    Create the layout of the app

    Returns:
    --------
    dbc.Container: The layout of the app
    """
    return dbc.Container(className="p-3", children=[
        html.H1("GitHub Copilot Implementation Simulator"),
        get_modal_button(),
        html.Div([], id="out-div"),
        dbc.Container([
            html.H2("Roadmap Timeline"),
            dcc.Graph(
                id="roadmap-timeline",
                figure=px.timeline(
                    config.roadmap_data, x_start="Start", x_end="End", y="Iteration", color="Iteration",
                    title="Implementation Timeline - hover over the bars for more details, click to expand",
                    labels={"Iteration": "Phase"},
                    text="Milestones"
                ).update_traces(
                    textposition="outside",
                    textfont=dict(size=10)
                ).update_layout(
                    xaxis_title="Timeline",
                    yaxis_title="Implementation Phase",
                    showlegend=False
                )
            ),
            dbc.Offcanvas(
                html.P(
                    "This is the content of the Offcanvas. "
                    "Close it by clicking on the close button, or "
                    "the backdrop."
                ),
                id="offcanvas",
                title="Iteration specific",
                is_open=False,
            ),
        ]),
        dbc.Container([
                html.H3("Adjust Iterations"),
                dbc.Container([
                    html.Label("Select Iteration:"),
                    dcc.Dropdown(
                        id="iteration-dropdown",
                        options=[{"label": name, "value": name} for name in config.roadmap_data["Iteration"]],
                        value="Planning & Training"
                    ),
                    dbc.Container([
                        dbc.Label("Start Date:", className="mx-3"),
                        dcc.DatePickerSingle(id="start-date-picker", date=str(config.roadmap_data.iloc[0]["Start"].date())),
                        dbc.Label("End Date:", className="mx-3"),
                        dcc.DatePickerSingle(id="end-date-picker", date=str(config.roadmap_data.iloc[0]["End"].date()))
                    ], className="p-3"),

                ], className="mt-30")
            ]),
        dbc.Button("Update Timeline", id="update-timeline-btn", n_clicks=0, className="m-3"),
        dbc.Button("Reset Timeline", id="reset-timeline-btn", n_clicks=0, className="m-3"),
        dbc.Container([
            html.H4("Mark Milestones as Achieved"),
            html.Div([

                dbc.Checklist(
                    id="milestones-checklist",
                    options=[
                        {"label": milestone, "value": iteration}
                        for iteration, milestone in zip(config.roadmap_data["Iteration"], config.roadmap_data["Milestones"])
                    ],
                    value=[],
                    inline=True
                )
            ], className="mt-3 ml-3")
        ]),
        dbc.Container([
            html.H2("Critical Succes Factors (CSF)"),
            dcc.Graph(
                id="csf-bar-chart",
                figure=px.bar(
                    pd.DataFrame(config.csf_data),
                    x="Metric", y="Current",
                    title="Current vs. Target CSF",
                    color_discrete_sequence=["#636EFA"]
                ).add_bar(
                    x=config.csf_data["Metric"],
                    y=config.csf_data["Target"],
                    name="Target",
                    marker_color="#EF553B"
                ).update_layout(
                    barmode="group",
                    yaxis_title="Percentage",
                    xaxis_title="CSF"
                )
            )
        ]),
        dbc.Container([
            html.H2("Adjust Parameters KPIs"),
            *[
                html.Div([
                    html.Label(f"{key} (%):"),
                    dcc.Slider(
                        id=f"{key.replace(' ', '-').lower()}-slider",
                        min=0,
                        max=100,
                        step=5,
                        value=value
                    )
                ]) for key, value in config.kpi_data.items()
            ]
        ], style={"marginTop": "20px"}),
        get_goals_card_body(),
        html.Div(id="simulation-output", style={"marginTop": "20px"})
    ])