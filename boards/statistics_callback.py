import dash
import plotly.graph_objs as go
from itertools import chain
from setup import app
from statistics_layout import *


@app.callback(
    dash.dependencies.Output('typical-samples', 'figure'),
    [dash.dependencies.Input('task-granularity', 'value')]
)
def generate_typical_samples_figure(granularity):
    x_legends = samples_by_granularity[granularity]
    x_values = [[getattr(s, t) / 1000. for s in loaded_samples] for t in x_legends]
    traces = []
    for i in range(len(x_legends)):
        trace = go.Bar(
            y=loaded_sample_names,
            x=x_values[i],
            name=title_translation[x_legends[i]],
            orientation='h'
        )
        traces.append(trace)
    layout = go.Layout(
        barmode='stack',
        title='fig.3 - Typical samples from DK trial',
        xaxis=dict(title='time in seconds', domain=[0, 140]),
        yaxis=dict(title='typical samples'),
        margin={'l': 180, 'r': 60, 't': 30, 'b': 130},
        annotations=[
            dict(
                x=0.5,
                y=-0.3,
                showarrow=False,
                xref='paper',
                yref='paper',
                text="model sample means the statistic model of the trial, "
                     "100% means the longest distance sample in the trial, "
                     "0% means the shortest distance sample in the trial, "
                     "while other percentages mean similarly."
            )
        ]
    )
    return go.Figure(data=traces, layout=layout)


@app.callback(
    dash.dependencies.Output('stats', 'figure'),
    [dash.dependencies.Input('task-granularity', 'value')]
)
def generate_stats_figure(granularity):
    task_titles = samples_by_granularity[granularity]
    y_short = list(chain(*[(title_translation[t],) * l_short for t in task_titles]))
    y_long = list(chain(*[(title_translation[t],) * l_long for t in task_titles]))
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
        yaxis=dict(title='sub-task name'),
        margin={'l': 180, 'r': 60, 't': 30, 'b': 30}
    )
    return go.Figure(data=data, layout=layout)
