import dash
import dash_core_components as dcc
import dash_html_components as html
from collections import OrderedDict
from setup import app, board_tab_id
from statistics_layout import statistics_layout, statistics_div_id
from prediction_layout import prediction_layout, prediction_div_id


boards = OrderedDict([
    (statistics_div_id, statistics_layout),
    (prediction_div_id, prediction_layout)
])

layout_list = [
    html.H1(app.title, style=dict(textAlign="center")),
    dcc.Tabs(
        id=board_tab_id,
        tabs=[{"label": i, "value": i} for i in boards.keys()],
        value=boards.keys()[0]
    ),
    html.Div(
        id="page-content"
    )
]


@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input(board_tab_id, 'value')]
)
def switch_board(board):
    return boards[board]


app.layout = html.Div(layout_list)
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
server = app.server


import statistics_callback
import prediction_callback


if __name__ == '__main__':
    app.run_server(debug=True)
