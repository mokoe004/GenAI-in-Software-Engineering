import dash
import json
from layout import create_layout
from callbacks import register_callbacks
from modal import register_modal_callbacks
import pandas as pd

import dash_bootstrap_components as dbc

from data import roadmap_data, kpi_data, csf_data, team_members, goals

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
app.title = "GitHub Copilot Implementation Simulator"
app.layout = create_layout()

# Register callbacks
register_callbacks(app)
register_modal_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
