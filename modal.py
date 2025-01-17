from dash import Dash, html, Input, Output, State, ctx, dcc
import dash_bootstrap_components as dbc

from data import roadmap_data, kpi_data, csf_data, team_members, goals

# Layout of the app
def get_modale_button():
    return html.Div([
        # Button to open the modal
        dbc.Button("Configure Team Members", id="open-modal", n_clicks=0, className="mb-3"),

        # The modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Configure Team Member Parameters")),
            dbc.ModalBody([
                html.Div([
                    dbc.Label("Team Member:"),
                    dcc.Dropdown(
                        id="role-dropdown",
                        options=[{"label": member["name"], "value": member["name"]} for member in team_members],
                        placeholder="Select a role"
                    )
                ], className="mb-3"),

                html.Div([
                    dbc.Label("Experience Level (Years):"),
                    html.P(id="experience-display", className="form-control-static")
                ], className="mb-3"),

                html.Div([
                    dbc.Label("Age:"),
                    html.P(id="age-display", className="form-control-static")
                ], className="mb-3"),

                html.Div([
                    dbc.Label("Level of Commitment (1-5):"),
                    dcc.Slider(id="commitment-slider", min=1, max=5, step=1, value=3,
                               marks={i: str(i) for i in range(1, 6)})
                ], className="mb-3"),

                html.Div([
                    dbc.Label("Resistance (1-5):"),
                    dcc.Slider(id="resistance-slider", min=1, max=5, step=1, value=3,
                               marks={i: str(i) for i in range(1, 6)})
                ], className="mb-3"),

                html.Div([
                    dbc.Label("Impact on Team (1-5):"),
                    dcc.Slider(id="impact-slider", min=1, max=5, step=1, value=3,
                               marks={i: str(i) for i in range(1, 6)})
                ], className="mb-3")
            ]),
            dbc.ModalFooter([
                dbc.Button("Save Changes", id="save-button", className="me-2", n_clicks=0),
                dbc.Button("Close", id="close-modal", n_clicks=0)
            ])
        ], id="modal", is_open=False),

        # Div to display the saved parameters
        html.Div(id="output-div", className="mt-3")
    ])

def register_modale_callbacks(app):
    # Callbacks
    @app.callback(
        [Output("modal", "is_open"),
         Output("experience-display", "children"),
         Output("age-display", "children")],
        [Input("open-modal", "n_clicks"),
         Input("close-modal", "n_clicks"),
         Input("role-dropdown", "value")],
        [State("modal", "is_open")]
    )
    def toggle_modal(open_clicks, close_clicks, selected_member, is_open):
        """Toggle the modal open or close and display static data."""
        if ctx.triggered_id == "open-modal":
            return True, "", ""
        if ctx.triggered_id == "close-modal":
            return False, "", ""

        # Update static displays based on selected member
        if selected_member:
            member = next((m for m in team_members if m["name"] == selected_member), None)
            if member:
                experience = f"{member['experience_years']} years"
                age = f"{member['age']} years"
                return is_open, experience, age

        return is_open, "", ""

    @app.callback(
        Output("output-div", "children"),
        Input("save-button", "n_clicks"),
        [State("role-dropdown", "value"),
         State("commitment-slider", "value"),
         State("resistance-slider", "value"),
         State("impact-slider", "value")]
    )
    def save_changes(save_clicks, role, commitment, resistance, impact):
        """Save the entered parameters and display them."""
        if save_clicks > 0:
            return html.Div([
                html.P(f"Role: {role}"),
                html.P(f"Level of Commitment: {commitment}"),
                html.P(f"Resistance: {resistance}"),
                html.P(f"Impact on Team: {impact}")
            ])
        return ""

