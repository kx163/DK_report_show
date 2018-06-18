import csv
from Task import Task
from TaskModel import TaskModel
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from collections import OrderedDict
from itertools import chain
import plotly.colors


# Data Section 1: Prepare the data of the first illustration: the typical samples
samples_by_granularity = OrderedDict([
    ("low level task", ["t_go_to_start_bay",
                        "t_couple_trolley",
                        "t_undock_trolley",
                        "t_exit_start_bay",
                        "t_go_to_end_bay",
                        "sum_navigation_failures",
                        "t_visual_align",
                        "t_drop_trolley",
                        "t_undock_robot"]),
    ("medium level task", ["total_go_to_start_bay",
                           "total_couple_trolley_and_exit_bay",
                           "total_go_to_end_bay",
                           "total_drop_trolley_in_bay"]),
    ("total spent", ["total_spent"])
])


def load_samples(sample_csv):
    with open(sample_csv, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        title = next(reader, None)
        samples = []
        sample_names = []
        for row in reader:
            task = Task()
            sample_names.append(row[0])
            task.from_list(row[1:])
            samples.append(task)
        return title, sample_names, samples


sample_csv_path = "./data/12_samples.csv"
loaded_title, loaded_sample_names, loaded_samples = load_samples(sample_csv_path)
# Data Section 1 End


# Data Section 2: Prepare the data of the second illustration: the statistics
def load_tasks(task_csv):
    with open(task_csv, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        return [Task().from_list(row) for row in reader]


short_run_csv_path = "./data/2018-03-22-15-19-10-extract.bag.csv"
long_run_csv_path = "./data/2018-03-22-17-27-17-extract.bag.csv"
short_run_tasks = load_tasks(short_run_csv_path)
long_run_tasks = load_tasks(long_run_csv_path)
l_short = len(short_run_tasks)
l_long = len(long_run_tasks)
# Data Section 2 End


# Data Section 3: Prepare the data of the third illustration: the prediction
def load_models(model_csv):
    with open(model_csv, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        _short_model = TaskModel().from_list(next(reader, None)[1:])
        _long_model = TaskModel().from_list(next(reader, None)[1:])
        return _short_model, _long_model


model_csv_path = "./data/2_models.csv"
short_run_model, long_run_model = load_models(model_csv_path)
model_choices = OrderedDict([("busy", short_run_model), ("quiet", long_run_model)])

current_robot = dict(v_navigation=0.6, v_docking=0.25, v_manual=0.45, actuator=3.)
next_robot = dict(v_navigation=1.5, v_docking=0.25, v_manual=0.45, actuator=1.)
robot_choices = OrderedDict([("current", current_robot), ("next-gen", next_robot)])


def calculate_saved_distance(distance, model, model_robot, predictive_robot, hours=8.):
    t_go_to_start_bay = model.t_go_to_start_bay.mean / 1000.
    t_couple_trolley = model.t_couple_trolley.mean / 1000.
    t_undock_trolley = model.t_undock_trolley.mean / 1000.
    t_exit_start_bay = model.t_exit_start_bay.mean / 1000.
    t_visual_align = model.t_visual_align.mean / 1000.
    t_drop_trolley = model.t_drop_trolley.mean / 1000.
    t_undock_robot = model.t_undock_robot.mean / 1000.
    t_sum_navigation_failure = distance * model.navigation_failure_per_meter.k * (model.t_navigation_failures.mean
                                                                                  / 1000.)
    speed_ratio = model.navigation_speed.mean / model_robot["v_navigation"]

    total_go_to_start_bay = t_go_to_start_bay
    total_couple_trolley_and_exit_bay = (t_couple_trolley + t_undock_trolley + t_exit_start_bay
                                         - model_robot["actuator"]) * model_robot["v_docking"] \
                                        / predictive_robot["v_docking"] + predictive_robot["actuator"]
    total_go_to_end_bay = distance / (speed_ratio * predictive_robot["v_navigation"]) + t_sum_navigation_failure
    total_drop_trolley_in_bay = (t_visual_align + t_drop_trolley + t_undock_robot - model_robot["actuator"]) \
                                * model_robot["v_docking"] / predictive_robot["v_docking"] \
                                + predictive_robot["actuator"]

    total_predictive_spent = total_go_to_start_bay + total_couple_trolley_and_exit_bay \
                             + total_go_to_end_bay + total_drop_trolley_in_bay
    return distance * hours * 3600. / total_predictive_spent


def calculate_limit_and_typical_values(model, model_robot, predictive_robot, hours=8.):
    t_go_to_start_bay = model.t_go_to_start_bay.mean / 1000.
    t_couple_trolley = model.t_couple_trolley.mean / 1000.
    t_undock_trolley = model.t_undock_trolley.mean / 1000.
    t_exit_start_bay = model.t_exit_start_bay.mean / 1000.
    t_visual_align = model.t_visual_align.mean / 1000.
    t_drop_trolley = model.t_drop_trolley.mean / 1000.
    t_undock_robot = model.t_undock_robot.mean / 1000.
    t_single_navigation_failure = model.navigation_failure_per_meter.k * model.t_navigation_failures.mean / 1000.
    speed_ratio = model.navigation_speed.mean / model_robot["v_navigation"]

    total_go_to_start_bay = t_go_to_start_bay
    total_couple_trolley_and_exit_bay = (t_couple_trolley + t_undock_trolley + t_exit_start_bay
                                         - model_robot["actuator"]) * model_robot["v_docking"] \
                                        / predictive_robot["v_docking"] + predictive_robot["actuator"]
    total_drop_trolley_in_bay = (t_visual_align + t_drop_trolley + t_undock_robot - model_robot["actuator"]) \
                                * model_robot["v_docking"] / predictive_robot["v_docking"] \
                                + predictive_robot["actuator"]

    factor_go_to_end_bay = 1. / speed_ratio / predictive_robot["v_navigation"] + t_single_navigation_failure
    saved_distance_limit = hours * 3600. / factor_go_to_end_bay
    t_fixed = total_go_to_start_bay + total_couple_trolley_and_exit_bay + total_drop_trolley_in_bay
    typical_station_distance = saved_distance_limit * t_fixed / hours / 3600.
    typical_station_distance = 3 * typical_station_distance
    typical_saved_distance = hours * 3600. / (factor_go_to_end_bay + t_fixed / typical_station_distance)
    return saved_distance_limit, typical_station_distance, typical_saved_distance
# Data Section 3 End


# Data Section 4: Prepare the data of the fourth illustration: the impact of docking time
def calculate_saved_distance_by_docking_time(distance, model, model_robot, predictive_robot, saved_ratio, hours=8.):
    time_ratio = 1 - saved_ratio
    t_go_to_start_bay = model.t_go_to_start_bay.mean / 1000.
    t_couple_trolley = model.t_couple_trolley.mean / 1000.
    t_undock_trolley = model.t_undock_trolley.mean / 1000.
    t_exit_start_bay = model.t_exit_start_bay.mean / 1000.
    t_visual_align = model.t_visual_align.mean / 1000.
    t_drop_trolley = model.t_drop_trolley.mean / 1000.
    t_undock_robot = model.t_undock_robot.mean / 1000.
    t_sum_navigation_failure = distance * model.navigation_failure_per_meter.k * (model.t_navigation_failures.mean
                                                                                  / 1000.)
    speed_ratio = model.navigation_speed.mean / model_robot["v_navigation"]

    total_go_to_start_bay = t_go_to_start_bay
    total_couple_trolley_and_exit_bay = ((t_couple_trolley + t_undock_trolley + t_exit_start_bay
                                          - model_robot["actuator"]) * model_robot["v_docking"]
                                         / predictive_robot["v_docking"] + predictive_robot["actuator"]) * time_ratio
    total_go_to_end_bay = distance / (speed_ratio * predictive_robot["v_navigation"]) + t_sum_navigation_failure
    total_drop_trolley_in_bay = ((t_visual_align + t_drop_trolley + t_undock_robot - model_robot["actuator"])
                                 * model_robot["v_docking"] / predictive_robot["v_docking"]
                                 + predictive_robot["actuator"]) * time_ratio
    total_predictive_spent = (total_go_to_start_bay + total_couple_trolley_and_exit_bay
                              + total_go_to_end_bay + total_drop_trolley_in_bay)
    return distance * hours * 3600. / total_predictive_spent
# Data Section 4 End


# App setup section
app = dash.Dash()
server = app.server


app.layout = html.Div([
    html.H1("DK Trial Analysis In Graphs", style=dict(textAlign="center")),
    html.Hr(),
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
    html.Br(),
    html.H4(
        "The traffic and robot model radio buttons will affect fig 1. and fig 2.",
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
                        options=[{"label": i, "value": i} for i in model_choices.keys()],
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
                        options=[{"label": i, "value": i} for i in robot_choices.keys()],
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
    html.Br(),
    dcc.Graph(
        id="saved-distances"
    ),
    html.Br(),
    dcc.Graph(
        id="saved-distances-by-docking-time"
    ),
    html.Br(),
    html.Hr(),
    dcc.Tabs(
        id="task-granularity",
        tabs=[{"label": i, "value": i} for i in samples_by_granularity.keys()],
        value=samples_by_granularity.keys()[0]
    ),
    html.H4(
        "The above tab will affect fig.3 and fig.4",
        style=dict(textAlign="center")
    ),
    html.Br(),
    dcc.Graph(
        id='typical-samples',
    ),
    html.Br(),
    dcc.Graph(
        id='stats'
    ),
    html.Br(),
])

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
# App setup section ends


# App callback section
@app.callback(
    dash.dependencies.Output('typical-samples', 'figure'),
    [dash.dependencies.Input('task-granularity', 'value')]
)
def generate_typical_samples_figure(granularity):
    y_title = loaded_title[0]
    x_legends = samples_by_granularity[granularity]
    x_values = [[getattr(s, t) / 1000. for s in loaded_samples] for t in x_legends]
    traces = []
    for i in range(len(x_legends)):
        trace = go.Bar(
            y=loaded_sample_names,
            x=x_values[i],
            name=x_legends[i],
            orientation='h'
        )
        traces.append(trace)
    layout = go.Layout(
        barmode='stack',
        title='fig.3 - Typical samples from DK trial',
        xaxis=dict(title='time in seconds', domain=[0, 140]),
        yaxis=dict(title=y_title),
        margin={'l': 180, 'r': 60, 't': 30, 'b': 30}
    )
    return go.Figure(data=traces, layout=layout)


@app.callback(
    dash.dependencies.Output('stats', 'figure'),
    [dash.dependencies.Input('task-granularity', 'value')]
)
def generate_stats_figure(granularity):
    task_titles = samples_by_granularity[granularity]
    y_short = list(chain(*[(t,) * l_short for t in task_titles]))
    y_long = list(chain(*[(t,) * l_long for t in task_titles]))
    x_short = [getattr(task, title) / 1000. for title in task_titles for task in short_run_tasks]
    x_long = [getattr(task, title) / 1000. for title in task_titles for task in long_run_tasks]
    trace_short = go.Box(
        x=x_short,
        y=y_short,
        name='Short Run Trial',
        marker=dict(
            color='#3D9970'
        ),
        boxmean='sd',
        boxpoints=False,
        orientation='h'
    )
    trace_long = go.Box(
        x=x_long,
        y=y_long,
        name='Long Run Trial',
        marker=dict(
            color='#FF4136'
        ),
        boxmean='sd',
        boxpoints=False,
        orientation='h'
    )
    data = [trace_short, trace_long]
    layout = go.Layout(
        boxmode='group',
        title='fig.4 - Statistics from DK Trial',
        xaxis=dict(title='time in seconds', domain=[0, 140]),
        yaxis=dict(title='task name'),
        margin={'l': 180, 'r': 60, 't': 30, 'b': 30}
    )
    return go.Figure(data=data, layout=layout)


@app.callback(
    dash.dependencies.Output('saved-distances', 'figure'),
    [dash.dependencies.Input('shift-hours', 'value')]
)
def generate_saved_distances(shift_hours):
    _hours = float(shift_hours)
    left_bound = 0
    right_bound = 300
    distance_range = range(left_bound, right_bound + 1, 5)
    colors = plotly.colors.DEFAULT_PLOTLY_COLORS
    # plot for current prototype in busy period
    trace_current_busy = go.Scatter(
        x=distance_range,
        y=map(lambda d: calculate_saved_distance(d, short_run_model, current_robot, current_robot, _hours),
              distance_range),
        name="Current Prototype in busy period",
        mode="lines",
        line=dict(color=colors[0])
    )
    res = calculate_limit_and_typical_values(short_run_model, current_robot, current_robot, _hours)
    line_current_busy_limit = go.Scatter(
        x=[left_bound, right_bound],
        y=[res[0], res[0]],
        name="Limit of saved distance for current prototype in busy period",
        mode="lines",
        line=dict(color=colors[0], dash="dash")
    )
    marker_current_busy_typical = go.Scatter(
        x=[res[1]],
        y=[res[2]],
        name="Typical station distance and saved station for current prototype in busy period",
        mode="markers",
        marker=dict(color=colors[0], size=10)
    )
    # plot for current prototype in quiet period
    trace_current_quiet = go.Scatter(
        x=distance_range,
        y=map(lambda d: calculate_saved_distance(d, long_run_model, current_robot, current_robot, _hours),
              distance_range),
        name="Current Prototype in quiet period",
        mode="lines",
        line=dict(color=colors[1])
    )
    res = calculate_limit_and_typical_values(long_run_model, current_robot, current_robot, _hours)
    line_current_quiet_limit = go.Scatter(
        x=[left_bound, right_bound],
        y=[res[0], res[0]],
        name="Limit of saved distance for current prototype in quiet period",
        mode="lines",
        line=dict(color=colors[1], dash="dash")
    )
    marker_current_quiet_typical = go.Scatter(
        x=[res[1]],
        y=[res[2]],
        name="Typical station distance and saved station for current prototype in quiet period",
        mode="markers",
        marker=dict(color=colors[1], size=10)
    )
    # plot for next-gen prototype in busy period
    trace_next_gen_busy = go.Scatter(
        x=distance_range,
        y=map(lambda d: calculate_saved_distance(d, short_run_model, current_robot, next_robot, _hours),
              distance_range),
        name="Next-gen Prototype in busy period",
        mode="lines",
        line=dict(color=colors[2])
    )
    res = calculate_limit_and_typical_values(short_run_model, current_robot, next_robot, _hours)
    line_next_gen_busy_limit = go.Scatter(
        x=[left_bound, right_bound],
        y=[res[0], res[0]],
        name="Limit of saved distance for next-gen prototype in busy period",
        mode="lines",
        line=dict(color=colors[2], dash="dash")
    )
    marker_next_gen_busy_typical = go.Scatter(
        x=[res[1]],
        y=[res[2]],
        name="Typical station distance and saved station for next-gen prototype in busy period",
        mode="markers",
        marker=dict(color=colors[2], size=10)
    )
    # plot for next-gen prototype in quiet period
    trace_next_gen_quiet = go.Scatter(
        x=distance_range,
        y=map(lambda d: calculate_saved_distance(d, long_run_model, current_robot, next_robot, _hours),
              distance_range),
        name="Next-gen Prototype in quiet period",
        mode="lines",
        line=dict(color=colors[3])
    )
    res = calculate_limit_and_typical_values(long_run_model, current_robot, next_robot, _hours)
    line_next_gen_quiet_limit = go.Scatter(
        x=[left_bound, right_bound],
        y=[res[0], res[0]],
        name="Limit of saved distance for next-gen prototype in quiet period",
        mode="lines",
        line=dict(color=colors[3], dash="dash")
    )
    marker_next_gen_quiet_typical = go.Scatter(
        x=[res[1]],
        y=[res[2]],
        name="Typical station distance and saved station for next-gen prototype in quiet period",
        mode="markers",
        marker=dict(color=colors[3], size=10)
    )
    data = [trace_next_gen_quiet, line_next_gen_quiet_limit, marker_next_gen_quiet_typical,
            trace_next_gen_busy, line_next_gen_busy_limit, marker_next_gen_busy_typical,
            trace_current_quiet, line_current_quiet_limit, marker_current_quiet_typical,
            trace_current_busy, line_current_busy_limit, marker_current_busy_typical]
    layout = go.Layout(
        title='fig.1 - Prediction on how many meters can be saved for one robot in one shift',
        xaxis=dict(title='distance between picking and packing stations'),
        yaxis=dict(title='saved meters'),
        margin={'l': 180, 'r': 60, 't': 30, 'b': 30}
    )
    return go.Figure(data=data, layout=layout)


@app.callback(
    dash.dependencies.Output('prediction', 'children'),
    [dash.dependencies.Input('traffic-choice', 'value'),
     dash.dependencies.Input('robot-choice', 'value'),
     dash.dependencies.Input('shift-hours', 'value'),
     dash.dependencies.Input('station-distance', 'value')]
)
def generate_saved_distance(traffic_choice, robot_choice, shift_hours, station_distance):
    _distance = float(station_distance)
    _hours = float(shift_hours)
    _model = model_choices[traffic_choice]
    _predictive_robot = robot_choices[robot_choice]
    saving = calculate_saved_distance(_distance, _model, current_robot, _predictive_robot, _hours)
    return "One robot could predictively save %d meters walking distance per shift!" % int(saving)


@app.callback(
    dash.dependencies.Output('saved-distances-by-docking-time', 'figure'),
    [dash.dependencies.Input('shift-hours', 'value'),
     dash.dependencies.Input('station-distance', 'value')]
)
def generate_saved_distance_by_docking_time(shift_hours, station_distance):
    _distance = float(station_distance)
    _hours = float(shift_hours)
    left_bound = 0
    right_bound = 50
    saved_percentage_range = range(left_bound, right_bound + 1, 1)
    saved_ratio_range = [x / 100. for x in saved_percentage_range]
    colors = plotly.colors.DEFAULT_PLOTLY_COLORS
    # plot for current prototype in busy period
    trace_current_busy = go.Scatter(
        x=saved_ratio_range,
        y=map(lambda t: calculate_saved_distance_by_docking_time(_distance, short_run_model, current_robot,
                                                                 current_robot, t, _hours), saved_ratio_range),
        name="Current Prototype in busy period",
        mode="lines",
        line=dict(color=colors[0])
    )
    # plot for current prototype in quiet period
    trace_current_quiet = go.Scatter(
        x=saved_ratio_range,
        y=map(lambda t: calculate_saved_distance_by_docking_time(_distance, long_run_model, current_robot,
                                                                 current_robot, t, _hours), saved_ratio_range),
        name="Current Prototype in quiet period",
        mode="lines",
        line=dict(color=colors[1])
    )
    # plot for next-gen prototype in busy period
    trace_next_gen_busy = go.Scatter(
        x=saved_ratio_range,
        y=map(lambda t: calculate_saved_distance_by_docking_time(_distance, short_run_model, current_robot,
                                                                 next_robot, t, _hours), saved_ratio_range),
        name="Next-gen Prototype in busy period",
        mode="lines",
        line=dict(color=colors[2])
    )
    # plot for next-gen prototype in quiet period
    trace_next_gen_quiet = go.Scatter(
        x=saved_ratio_range,
        y=map(lambda t: calculate_saved_distance_by_docking_time(_distance, long_run_model, current_robot,
                                                                 next_robot, t, _hours), saved_ratio_range),
        name="Next-gen Prototype in quiet period",
        mode="lines",
        line=dict(color=colors[3])
    )
    data = [trace_next_gen_quiet, trace_next_gen_busy, trace_current_quiet, trace_current_busy]
    layout = go.Layout(
        title='fig.2 - Impact of the docking time on the saved distance for one robot in one shift',
        xaxis=dict(title='saved time on docking by percentage', tickformat=",.0%"),
        yaxis=dict(title='saved meters'),
        margin={'l': 180, 'r': 60, 't': 30, 'b': 30}
    )
    return go.Figure(data=data, layout=layout)
# App callback section ends


if __name__ == '__main__':
    app.run_server(debug=True)
