import dash_core_components as dcc
import dash_html_components as html
from load_data import *


# #########
# The layout of the prediction board
# #########

prediction_div_id = "prediction"
prediction_layout = html.Div(
    id=prediction_div_id,
    children=[
        html.H4(
            "The hours and distance inputs below will affect the prediction and fig 1. and fig 2.",
            style=dict(textAlign="center")
        ),
        html.Div(
            children=[
                html.Label(
                    "Hours in a shift:",
                    htmlFor="shift-hours",
                    style=dict(textAlign="right", padding="8px 0"),
                    className="three columns"
                ),
                dcc.Input(
                    id="shift-hours",
                    value=8.0,
                    type="number",
                    className="three columns"
                ),
                html.Label(
                    "Meters between picking and packing stations:",
                    htmlFor="station-distance",
                    style=dict(textAlign="right", padding="8px 0"),
                    className="three columns"
                ),
                dcc.Input(
                    id="station-distance",
                    value=100.0,
                    type="number",
                    className="three columns"
                ),
            ],
            className="row"
        ),
        html.H4(
            "The traffic and robot model radio buttons will only affect the prediction",
            style=dict(textAlign="center")
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Label(
                            "Traffic status inplace",
                            htmlFor="traffic-choice",
                            style=dict(textAlign="center"),
                            className="row"
                        ),
                        dcc.RadioItems(
                            id="traffic-choice",
                            options=[{"label": "warehouse in %s period" % i, "value": i} for i in model_choices.keys()],
                            value=model_choices.keys()[0],
                            labelStyle=dict(textAlign="center"),
                            labelClassName="six columns",
                            className="row"
                        ),
                    ],
                    className="six columns"
                ),
                html.Div(
                    children=[
                        html.Label(
                            "Robot model to use",
                            htmlFor="robot-choice",
                            style=dict(textAlign="center"),
                            className="row"
                        ),
                        dcc.RadioItems(
                            id="robot-choice",
                            options=[{"label": "our %s prototype" % i, "value": i} for i in robot_choices.keys()],
                            value=robot_choices.keys()[1],
                            labelStyle=dict(textAlign="center"),
                            labelClassName="six columns",
                            className="row"
                        ),
                    ],
                    className="six columns"
                ),
            ],
            className="row"
        ),
        html.Hr(),
        html.H1(
            id="prediction",
            children="",
            style=dict(textAlign="center")
        ),
        dcc.Graph(
            id="saved-distances"
        ),
        html.Br(),
        dcc.Graph(
            id="saved-distances-by-docking-time"
        ),
    ]
)
