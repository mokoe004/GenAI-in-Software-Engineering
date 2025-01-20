import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import json

from dash.html import Figure

from data import config
from iterations_md import iterations_md as iteration_markdown

def register_callbacks(app):
    """
    Register all the callbacks for the app

    Args:
    app: Dash app object

    Returns:
    None
    """
    # For offcanvas (additional information for roadmap)
    @app.callback(
        [Output("offcanvas", "is_open"),
         Output("offcanvas", "children")],
        Input("roadmap-timeline", "clickData"),
        [State("offcanvas", "is_open")],
    )
    def toggle_offcanvas(clickData, is_open):
        if clickData:
            # Get the iteration and milestone
            point = clickData["points"][0]
            iteration = point["y"]  # `y` returns the iteration
            details = dcc.Markdown(iteration_markdown[iteration]) # Get the markdown content for the iteration
            return (not is_open), details
        return is_open, "Click on a bar to see more details"


    # Update roadmap dates acording to picker
    @app.callback(
        [Output("start-date-picker", "date"),
         Output("end-date-picker", "date")],
        Input("iteration-dropdown", "value")
    )
    def update_date_pickers(selected_iteration):
        # Get the row for the selected iteration
        selected_row = config.roadmap_data[config.roadmap_data["Iteration"] == selected_iteration]
        start_date = selected_row["Start"].iloc[0].date()
        end_date = selected_row["End"].iloc[0].date()
        return str(start_date), str(end_date)

    # Update roadmap timeline
    @app.callback(
        Output("roadmap-timeline", "figure"),
        [
            Input("update-timeline-btn", "n_clicks"),
            Input("reset-timeline-btn", "n_clicks"),
            Input("milestones-checklist-0", "value")
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
                config.roadmap_data, x_start="Start", x_end="End", y="Iteration", color="Iteration",
                title="Interactive Roadmap Timeline - Hover over Iteration to get hint, click on Iteration for more information", text="First_Milestone"
            ).update_layout(xaxis_title="Timeline", yaxis_title="Implementation Phase", showlegend=False)
            fig.for_each_trace(lambda trace: trace.update(opacity=0.5 if trace.name in achieved_milestones else 1))
            return fig

        if ctx.triggered[0]["prop_id"] == "reset-timeline-btn.n_clicks":
            # Reset to original data
            config.roadmap_data["Start"] = pd.to_datetime(["2025-01-01", "2025-01-22", "2025-03-01", "2025-05-01"])
            config.roadmap_data["End"] = pd.to_datetime(["2025-01-21", "2025-02-28", "2025-04-30", "2025-06-30"])
        elif ctx.triggered[0]["prop_id"] == "update-timeline-btn.n_clicks":
            # Update the start and end dates for the selected iteration
            idx = config.roadmap_data[config.roadmap_data["Iteration"] == iteration].index[0]
            config.roadmap_data.at[idx, "Start"] = pd.to_datetime(start_date)
            config.roadmap_data.at[idx, "End"] = pd.to_datetime(end_date)

        # Recreate the timeline figure
        fig = px.timeline(
            config.roadmap_data, x_start="Start", x_end="End", y="Iteration", color="Iteration",
            title="Interactive Roadmap Timeline", text="First_Milestone"
        )
        fig.update_layout(xaxis_title="Timeline", yaxis_title="Implementation Phase", showlegend=False)
        fig.for_each_trace(lambda trace: trace.update(opacity=0.5 if trace.name in achieved_milestones else 1))
        return fig
