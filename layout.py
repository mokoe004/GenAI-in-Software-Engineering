from modal import get_modale_button
from data import roadmap_data, kpi_data, csf_data, team_members, goals

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

import pandas as pd


# Layout
def create_layout():
    return dbc.Container(className="p-3", children=[
        html.H1("GitHub Copilot Implementation Simulator"),
        get_modale_button(),
        dbc.Container([
            html.H2("Roadmap Timeline"),
            dcc.Graph(
                id="roadmap-timeline",
                figure=px.timeline(
                    roadmap_data, x_start="Start", x_end="End", y="Iteration", color="Iteration",
                    title="Implementation Timeline",
                    labels={"Iteration": "Phase"},
                    text="Milestones"
                ).update_layout(
                    xaxis_title="Timeline",
                    yaxis_title="Implementation Phase",
                    showlegend=False
                )
            )
        ]),
        dbc.Container([
                html.H3("Adjust Iterations"),
                html.Div([
                    html.Label("Select Iteration:"),
                    dcc.Dropdown(
                        id="iteration-dropdown",
                        options=[{"label": name, "value": name} for name in roadmap_data["Iteration"]],
                        value="Planning & Training"
                    ),
                    html.Label("Start Date:"),
                    dcc.DatePickerSingle(id="start-date-picker", date=str(roadmap_data.iloc[0]["Start"].date())),
                    html.Label("End Date:"),
                    dcc.DatePickerSingle(id="end-date-picker", date=str(roadmap_data.iloc[0]["End"].date()))
                ], style={"marginTop": "20px"})
            ]),
        dbc.Button("Update Timeline", id="update-timeline-btn", n_clicks=0, className="m-3"),
        dbc.Button("Reset Timeline", id="reset-timeline-btn", n_clicks=0, className="m-3"),
        dbc.Container([
            html.H4("Mark Milestones as Achieved"),
            html.Div([
                dcc.Checklist(
                    id="milestones-checklist",
                    options=[
                        {"label": milestone, "value": iteration}
                        for iteration, milestone in zip(roadmap_data["Iteration"], roadmap_data["Milestones"])
                    ],
                    value=[],
                    inline=True
                )
            ], style={"marginTop": "20px"})
        ]),
        dbc.Container([
            html.H2("Critical Succes Factors (CSF)"),
            dcc.Graph(
                id="csf-bar-chart",
                figure=px.bar(
                    pd.DataFrame(csf_data),
                    x="Metric", y="Current",
                    title="Current vs. Target CSF",
                    color_discrete_sequence=["#636EFA"]
                ).add_bar(
                    x=csf_data["Metric"],
                    y=csf_data["Target"],
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
                ]) for key, value in kpi_data.items()
            ]
        ], style={"marginTop": "20px"}),
        html.Div(id="simulation-output", style={"marginTop": "20px"})
    ])