import dash_core_components as dcc
import dash_html_components as html
from load_data import *


# #########
# The layout of the statistics board
# #########

statistics_div_id = "statistics"
statistics_layout = html.Div(
    id=statistics_div_id,
    children=[
        dcc.Tabs(
            id="task-granularity",
            tabs=[{"label": i, "value": i} for i in samples_by_granularity.keys()],
            value=samples_by_granularity.keys()[0]
        ),
        html.H4(
            "The above tab will affect fig.3 and fig.4",
            style=dict(textAlign="center")
        ),
        dcc.Graph(
            id='typical-samples',
        ),
        dcc.Graph(
            id='stats'
        ),
        html.Br(),
    ]
)
