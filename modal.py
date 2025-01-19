from dash import Dash, html, Input, Output, State, ctx, dcc
import dash_bootstrap_components as dbc

from data import config

# Layout of the modal
def get_modal_button():
    """
    Create a button to open a modal for configuring team members.

    Returns:
        dbc.Button: The button to open the modal.
    """
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
                        id="member-dropdown",
                        options=[{"label": member["name"], "value": member["name"]} for member in config.team_members],
                        placeholder="Select a role"
                    )
                ], className="mb-3"),

                dbc.Collapse(id="collapse", is_open=False,children=[
                    html.Div([
                        dbc.Label("Experience Level (Years):"),
                        html.P(id="experience-display", className="form-control-static"),
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
            ]),
            dbc.ModalFooter([
                dbc.Button("Save Changes", id="save-button", className="me-2", n_clicks=0),
                dbc.Button("Close", id="close-modal", n_clicks=0)
            ]),
            html.Div(id="output-div", className="mt-3")
        ], id="modal", is_open=False),
    ])

def register_modal_callbacks(app):
    """
    Register the modal callbacks for the app.

    Args:
        app (Dash): The Dash app where the callbacks will be registered.

    Returns:
        None
    """
    @app.callback(
        [Output("modal", "is_open"),
         Output("experience-display", "children"),
         Output("age-display", "children")],
        [Input("open-modal", "n_clicks"),
         Input("close-modal", "n_clicks"),
         Input("member-dropdown", "value")],
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
            member = next((m for m in config.team_members if m["name"] == selected_member), None)
            if member:
                experience = f"{member['experience_years']} years"
                age = f"{member['age']} years"
                return is_open, experience, age

        return is_open, "", ""

    @app.callback(
        Output("output-div", "children"),
        Input("save-button", "n_clicks"),
        [State("member-dropdown", "value"),
         State("commitment-slider", "value"),
         State("resistance-slider", "value"),
         State("impact-slider", "value")]
    )
    def save_changes(save_clicks, name,  commitment, resistance, impact):
        """Save the entered parameters and display them."""
        if save_clicks > 0:
            for member in config.team_members:
                if member["name"] == name:
                    member["params"]["Level of Commitment"] = commitment
                    member["params"]["Resistance"] = resistance
                    member["params"]["Impact on team"] = impact
                    return dbc.Toast(
            f"Changes saved for {name}!",
            id="positioned-toast",
            header="Positioned toast",
            dismissable=True,
            icon="success",
            duration=4000,
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
        )
        return dbc.Toast(
            "Please select a team member before saving!",
            id="positioned-toast",
            header="Positioned toast",
            dismissable=True,
            icon="danger",
            duration=4000,
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
        )

    @app.callback(
        Output("collapse", "is_open"),
        Input("member-dropdown", "value"),
        prevent_initial_call=True
    )
    def toggle_collapse(value):
        """Toggle the collapse if a member is selected."""
        return value is not None
