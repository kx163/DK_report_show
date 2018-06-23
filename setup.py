import dash
import os


# App setup section
app = dash.Dash()
app.config.suppress_callback_exceptions = True
app.title = "DK Trial Analysis In Graphs"
board_tab_id = "boards"
root_path = os.path.dirname(__file__)