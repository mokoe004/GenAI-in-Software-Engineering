import dash

from layout import create_layout
from callbacks import register_callbacks
from modal import register_modal_callbacks
from goals_display import register_goals_display_callbacks
from csf_inputs import register_csf_inputs_callbacks

import dash_bootstrap_components as dbc

# Create Dash app
# Can be changed to another theme, just replace CERULEAN with the desired theme
# Example: BOOTSRAP, FLATLY, LUX, MATERIA, PULSE, SANDSTONE, SLATE, SOLAR, SPACELAB, SUPERHERO, UNITED, YETI
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
app.title = "GitHub Copilot Implementation Simulator"
app.layout = create_layout()

# Register callbacks
register_callbacks(app)
register_modal_callbacks(app)
register_goals_display_callbacks(app)
register_csf_inputs_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
