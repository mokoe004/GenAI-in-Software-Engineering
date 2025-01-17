import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

# Create Dash app
app = dash.Dash(__name__)
app.title = "GitHub Copilot Implementation Simulator"

# Example Data for Milestones
roadmap_data = pd.DataFrame({
    "Iteration": ["Planning & Training", "Pilot Implementation", "Refinement", "Full Integration"],
    "Start": ["2025-01-01", "2025-01-22", "2025-03-01", "2025-05-01"],
    "End": ["2025-01-21", "2025-02-28", "2025-04-30", "2025-06-30"],
    "Milestones": [
        "Stakeholder training completed",
        "Pilot success feedback gathered",
        "90% issues resolved",
        "Full integration achieved"
    ]
})
roadmap_data["Start"] = pd.to_datetime(roadmap_data["Start"])
roadmap_data["End"] = pd.to_datetime(roadmap_data["End"])

# Example KPIs
kpi_data = {
"Productivity Increase":100,
    "Error Reduction": 100,
    "Adoption Rate" : 100,
}

# Wert wird durch KPIs und Länge der Iterationen bestimmt. Zusammenhang zu Iterationen herstellen?
csf_data = {
    "Metric": ["Technical Infrastructure", "Employee Acceptance", "ROI", "Code Quality", "Data Privacy"],
    "Current": [60, 20, 60, 40, 50],
    "Target": [100, 100, 100, 100,100]
}

# Layout
app.layout = html.Div([
    html.H1("GitHub Copilot Implementation Simulator"),
    html.Div([
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
    html.Div([
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
    html.Button("Update Timeline", id="update-timeline-btn", n_clicks=0),
    html.Button("Reset Timeline", id="reset-timeline-btn", n_clicks=0, style={"marginLeft": "10px"}),
    html.Div([
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
    html.Div([
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
    html.Div([
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

# Callbacks für Funktionalität

# Dynamisch Start und End datum
@app.callback(
    [Output("start-date-picker", "date"),
     Output("end-date-picker", "date")],
    Input("iteration-dropdown", "value")
)
def update_date_pickers(selected_iteration):
    # Get the row for the selected iteration
    selected_row = roadmap_data[roadmap_data["Iteration"] == selected_iteration]
    start_date = selected_row["Start"].iloc[0].date()
    end_date = selected_row["End"].iloc[0].date()
    return str(start_date), str(end_date)

# Roadmap aktualisieren
@app.callback(
    Output("roadmap-timeline", "figure"),
    [
        Input("update-timeline-btn", "n_clicks"),
        Input("reset-timeline-btn", "n_clicks"),
        Input("milestones-checklist", "value")
    ],
    [
        State("iteration-dropdown", "value"),
        State("start-date-picker", "date"),
        State("end-date-picker", "date")
    ]
)
def update_timeline(update_clicks, reset_clicks, achieved_milestones, iteration, start_date, end_date):
    ctx = dash.callback_context

    if not ctx.triggered:
        fig = px.timeline(
            roadmap_data, x_start="Start", x_end="End", y="Iteration", color="Iteration",
            title="Interactive Roadmap Timeline", text="Milestones"
        ).update_layout(xaxis_title="Timeline", yaxis_title="Implementation Phase", showlegend=False)
        fig.for_each_trace(lambda trace: trace.update(opacity=0.5 if trace.name in achieved_milestones else 1))
        return fig

    if ctx.triggered[0]["prop_id"] == "reset-timeline-btn.n_clicks":
        # Reset to original data
        roadmap_data["Start"] = pd.to_datetime(["2025-01-01", "2025-01-22", "2025-03-01", "2025-05-01"])
        roadmap_data["End"] = pd.to_datetime(["2025-01-21", "2025-02-28", "2025-04-30", "2025-06-30"])
    elif ctx.triggered[0]["prop_id"] == "update-timeline-btn.n_clicks":
        # Update the start and end dates for the selected iteration
        idx = roadmap_data[roadmap_data["Iteration"] == iteration].index[0]
        roadmap_data.at[idx, "Start"] = pd.to_datetime(start_date)
        roadmap_data.at[idx, "End"] = pd.to_datetime(end_date)

    # Recreate the timeline figure
    fig = px.timeline(
        roadmap_data, x_start="Start", x_end="End", y="Iteration", color="Iteration",
        title="Interactive Roadmap Timeline", text="Milestones"
    )
    fig.update_layout(xaxis_title="Timeline", yaxis_title="Implementation Phase", showlegend=False)
    fig.for_each_trace(lambda trace: trace.update(opacity=0.5 if trace.name in achieved_milestones else 1))
    return fig

# Simulation
@app.callback(
    Output("simulation-output", "children"),
    [
        *[
            Input(f"{key.replace(' ', '-').lower()}-slider", "value")
            for key in kpi_data.keys()
        ]
    ]
)
def update_simulation(*args):
    goals = [
        "Increase productivity, quality, and sustainability of the team's software development processes.",
        "Seamlessly integrate CoPilot into the team’s workflows.",
        "Ensure team members' acceptance and engagement with CoPilot."
    ]
    # Calculate probabilities based on the KPI sliders
    probabilities = [f"{value}%" for value in args]
    # Prepare the goals output
    goals_output = html.Ul([
        html.Li(f"{goal} - {prob}")
        for goal, prob in zip(goals, probabilities)
    ])
    # Determine overall status
    overall_success = sum(args) / len(args)
    status = "On Track" if overall_success >= 75 else "Needs Improvement"

    return html.Div([
        html.H3(f"Overall Success Rate: {overall_success:.2f}%"),
        html.P(f"Status: {status}"),
        html.H4("Goals and Achievement Probabilities:"),
        goals_output
    ])


if __name__ == "__main__":
    app.run_server(debug=True)
