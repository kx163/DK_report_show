import dash
import plotly.graph_objs as go
import plotly.colors
from setup import app
from prediction_layout import *


# #########
# Prepare the data for the curves of travelled distance
# #########


# calculate the travelled distance given the station distance, the trial model,
# the trial robot spec, the spec of robot to predict and the hours in a shift
def calculate_travelled_distance(distance, model, model_robot, predictive_robot, hours=8.):
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
                                         / predictive_robot["v_docking"] + predictive_robot["actuator"])
    total_go_to_end_bay = distance / (speed_ratio * predictive_robot["v_navigation"]) + t_sum_navigation_failure
    total_drop_trolley_in_bay = ((t_visual_align + t_drop_trolley + t_undock_robot - model_robot["actuator"])
                                 * model_robot["v_docking"] / predictive_robot["v_docking"]
                                 + predictive_robot["actuator"])

    total_predictive_spent = (total_go_to_start_bay + total_couple_trolley_and_exit_bay
                              + total_go_to_end_bay + total_drop_trolley_in_bay)
    return distance * hours * 3600. / total_predictive_spent


# calculate the limit of travelled distance, an example of the economic station distance
# and the travelled distance in case of this station distance
def calculate_limit_and_economic_values(model, model_robot, predictive_robot, hours=8.):
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
    total_couple_trolley_and_exit_bay = ((t_couple_trolley + t_undock_trolley + t_exit_start_bay
                                          - model_robot["actuator"]) * model_robot["v_docking"]
                                         / predictive_robot["v_docking"] + predictive_robot["actuator"])
    total_drop_trolley_in_bay = ((t_visual_align + t_drop_trolley + t_undock_robot - model_robot["actuator"])
                                 * model_robot["v_docking"] / predictive_robot["v_docking"]
                                 + predictive_robot["actuator"])

    factor_go_to_end_bay = 1. / speed_ratio / predictive_robot["v_navigation"] + t_single_navigation_failure
    saved_distance_limit = hours * 3600. / factor_go_to_end_bay
    t_fixed = total_go_to_start_bay + total_couple_trolley_and_exit_bay + total_drop_trolley_in_bay
    typical_station_distance = saved_distance_limit * t_fixed / hours / 3600.
    typical_station_distance = 3 * typical_station_distance
    typical_saved_distance = hours * 3600. / (factor_go_to_end_bay + t_fixed / typical_station_distance)
    return saved_distance_limit, typical_station_distance, typical_saved_distance


# #########
# Prepare the data for the curves of the impact of docking time
# #########

# calculate the travelled distance when the docking time is saved by a given ratio
def calculate_travelled_distance_by_docking_time(distance, model, model_robot, predictive_robot, saved_ratio, hours=8.):
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


# @app.callback(
#     dash.dependencies.Output('prediction', 'hidden'),
#     [dash.dependencies.Input('sub-pages', 'value')]
# )
# def generate_prediction_board(page):
#     return not page == 'prediction'


# #########
# callbacks for the curves of travelled distance
# #########
@app.callback(
    dash.dependencies.Output('saved-distances', 'figure'),
    [dash.dependencies.Input('shift-hours', 'value')]
)
def generate_travelled_distances(shift_hours):
    _hours = float(shift_hours)
    left_bound = 0
    right_bound = 300
    distance_range = range(left_bound, right_bound + 1, 5)
    colors = plotly.colors.DEFAULT_PLOTLY_COLORS
    # plot for current prototype in busy period
    trace_current_busy = go.Scatter(
        x=distance_range,
        y=map(lambda d: calculate_travelled_distance(d, short_run_model, current_robot, current_robot, _hours),
              distance_range),
        name="Current Prototype in busy period",
        mode="lines",
        line=dict(color=colors[0])
    )
    res = calculate_limit_and_economic_values(short_run_model, current_robot, current_robot, _hours)
    line_current_busy_limit = go.Scatter(
        x=[left_bound, right_bound],
        y=[res[0], res[0]],
        name="Limit of travelled distance for current prototype in busy period",
        mode="lines",
        line=dict(color=colors[0], dash="dash")
    )
    marker_current_busy_typical = go.Scatter(
        x=[res[1]],
        y=[res[2]],
        name="Example of economic station distance for current prototype in busy period",
        mode="markers",
        marker=dict(color=colors[0], size=10)
    )
    marker_current_busy_real = go.Scatter(
        x=[short_run_model.d_navigation.mean],
        y=[short_run_model.d_navigation.mean * (_hours * 3600000. / short_run_model.total_spent.mean)],
        name="Real travelled distance if we extend the short run to %.0d hours" % _hours,
        mode="markers",
        marker=dict(color=colors[0], size=15)
    )
    # plot for current prototype in quiet period
    trace_current_quiet = go.Scatter(
        x=distance_range,
        y=map(lambda d: calculate_travelled_distance(d, long_run_model, current_robot, current_robot, _hours),
              distance_range),
        name="Current Prototype in quiet period",
        mode="lines",
        line=dict(color=colors[1])
    )
    res = calculate_limit_and_economic_values(long_run_model, current_robot, current_robot, _hours)
    line_current_quiet_limit = go.Scatter(
        x=[left_bound, right_bound],
        y=[res[0], res[0]],
        name="Limit of travelled distance for current prototype in quiet period",
        mode="lines",
        line=dict(color=colors[1], dash="dash")
    )
    marker_current_quiet_typical = go.Scatter(
        x=[res[1]],
        y=[res[2]],
        name="Example of economic station distance for current prototype in quiet period",
        mode="markers",
        marker=dict(color=colors[1], size=10)
    )
    marker_current_quiet_real = go.Scatter(
        x=[long_run_model.d_navigation.mean],
        y=[long_run_model.d_navigation.mean * (_hours * 3600000. / long_run_model.total_spent.mean)],
        name="Real travelled distance if we extend the long run to %.0d hours" % _hours,
        mode="markers",
        marker=dict(color=colors[1], size=15)
    )
    # plot for next-gen prototype in busy period
    trace_next_gen_busy = go.Scatter(
        x=distance_range,
        y=map(lambda d: calculate_travelled_distance(d, short_run_model, current_robot, next_robot, _hours),
              distance_range),
        name="Next-gen Prototype in busy period",
        mode="lines",
        line=dict(color=colors[2])
    )
    res = calculate_limit_and_economic_values(short_run_model, current_robot, next_robot, _hours)
    line_next_gen_busy_limit = go.Scatter(
        x=[left_bound, right_bound],
        y=[res[0], res[0]],
        name="Limit of travelled distance for next-gen prototype in busy period",
        mode="lines",
        line=dict(color=colors[2], dash="dash")
    )
    marker_next_gen_busy_typical = go.Scatter(
        x=[res[1]],
        y=[res[2]],
        name="Example of economic station distance for next-gen prototype in busy period",
        mode="markers",
        marker=dict(color=colors[2], size=10)
    )
    # plot for next-gen prototype in quiet period
    trace_next_gen_quiet = go.Scatter(
        x=distance_range,
        y=map(lambda d: calculate_travelled_distance(d, long_run_model, current_robot, next_robot, _hours),
              distance_range),
        name="Next-gen Prototype in quiet period",
        mode="lines",
        line=dict(color=colors[3])
    )
    res = calculate_limit_and_economic_values(long_run_model, current_robot, next_robot, _hours)
    line_next_gen_quiet_limit = go.Scatter(
        x=[left_bound, right_bound],
        y=[res[0], res[0]],
        name="Limit of travelled distance for next-gen prototype in quiet period",
        mode="lines",
        line=dict(color=colors[3], dash="dash")
    )
    marker_next_gen_quiet_typical = go.Scatter(
        x=[res[1]],
        y=[res[2]],
        name="Example of economic station distance for next-gen prototype in quiet period",
        mode="markers",
        marker=dict(color=colors[3], size=10)
    )
    data = [trace_next_gen_quiet, line_next_gen_quiet_limit, marker_next_gen_quiet_typical,
            trace_next_gen_busy, line_next_gen_busy_limit, marker_next_gen_busy_typical,
            trace_current_quiet, line_current_quiet_limit, marker_current_quiet_typical, marker_current_quiet_real,
            trace_current_busy, line_current_busy_limit, marker_current_busy_typical,  marker_current_busy_real]
    layout = go.Layout(
        title='fig.1 - Prediction on total travelled distance for one robot in one shift',
        xaxis=dict(title='distance between picking and packing stations'),
        yaxis=dict(title='total travelled meters'),
        margin={'l': 180, 'r': 60, 't': 30, 'b': 30}
    )
    return go.Figure(data=data, layout=layout)


# #########
# callbacks for the prediction sentence
# #########
@app.callback(
    dash.dependencies.Output('prediction', 'children'),
    [dash.dependencies.Input('traffic-choice', 'value'),
     dash.dependencies.Input('robot-choice', 'value'),
     dash.dependencies.Input('shift-hours', 'value'),
     dash.dependencies.Input('station-distance', 'value')]
)
def generate_travelled_distance(traffic_choice, robot_choice, shift_hours, station_distance):
    _distance = float(station_distance)
    _hours = float(shift_hours)
    _model = model_choices[traffic_choice]
    _predictive_robot = robot_choices[robot_choice]
    saving = calculate_travelled_distance(_distance, _model, current_robot, _predictive_robot, _hours)
    return "One robot could save %d meters walking distance per shift!" % int(saving)


# #########
# callbacks for the curves of the impact of docking time
# #########
@app.callback(
    dash.dependencies.Output('saved-distances-by-docking-time', 'figure'),
    [dash.dependencies.Input('shift-hours', 'value'),
     dash.dependencies.Input('station-distance', 'value')]
)
def generate_travelled_distance_by_docking_time(shift_hours, station_distance):
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
        y=map(lambda t: calculate_travelled_distance_by_docking_time(_distance, short_run_model, current_robot,
                                                                     current_robot, t, _hours), saved_ratio_range),
        name="Current Prototype in busy period",
        mode="lines",
        line=dict(color=colors[0])
    )
    # plot for current prototype in quiet period
    trace_current_quiet = go.Scatter(
        x=saved_ratio_range,
        y=map(lambda t: calculate_travelled_distance_by_docking_time(_distance, long_run_model, current_robot,
                                                                     current_robot, t, _hours), saved_ratio_range),
        name="Current Prototype in quiet period",
        mode="lines",
        line=dict(color=colors[1])
    )
    # plot for next-gen prototype in busy period
    trace_next_gen_busy = go.Scatter(
        x=saved_ratio_range,
        y=map(lambda t: calculate_travelled_distance_by_docking_time(_distance, short_run_model, current_robot,
                                                                     next_robot, t, _hours), saved_ratio_range),
        name="Next-gen Prototype in busy period",
        mode="lines",
        line=dict(color=colors[2])
    )
    # plot for next-gen prototype in quiet period
    trace_next_gen_quiet = go.Scatter(
        x=saved_ratio_range,
        y=map(lambda t: calculate_travelled_distance_by_docking_time(_distance, long_run_model, current_robot,
                                                                     next_robot, t, _hours), saved_ratio_range),
        name="Next-gen Prototype in quiet period",
        mode="lines",
        line=dict(color=colors[3])
    )
    data = [trace_next_gen_quiet, trace_next_gen_busy, trace_current_quiet, trace_current_busy]
    layout = go.Layout(
        title='fig.2 - Impact of the docking time on the total travelled distance for one robot in one shift',
        xaxis=dict(title='saved time on docking by percentage', tickformat=",.0%"),
        yaxis=dict(title='total travelled meters'),
        margin={'l': 180, 'r': 60, 't': 30, 'b': 30}
    )
    return go.Figure(data=data, layout=layout)
