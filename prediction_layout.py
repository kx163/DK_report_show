import dash_core_components as dcc
import dash_html_components as html
import csv
from TaskModel import TaskModel
from collections import OrderedDict


# #########
# Loading necessary data for prediction board
# #########

# Specs of the current and next generation prototypes
current_robot = dict(v_navigation=0.6, v_docking=0.25, v_manual=0.45, actuator=3.)
next_robot = dict(v_navigation=1.5, v_docking=0.25, v_manual=0.45, actuator=1.)


# load the trial statistic models by csv path
def load_models(model_csv):
    with open(model_csv, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        _short_model = TaskModel().from_list(next(reader, None)[1:])
        _long_model = TaskModel().from_list(next(reader, None)[1:])
        return _short_model, _long_model


# actually load the trial statistic models
model_csv_path = "./data/2_models.csv"
short_run_model, long_run_model = load_models(model_csv_path)
# store the models in an ordered dict for later usage in layout
model_choices = OrderedDict([("busy", short_run_model), ("quiet", long_run_model)])

# store the robot specs in an ordered dict for later usage in layout
robot_choices = OrderedDict([("current", current_robot), ("next-gen", next_robot)])


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
