import dash_core_components as dcc
import dash_html_components as html
import csv
from Task import Task
from collections import OrderedDict


# #########
# Loading necessary data for statistics board
# #########

# store all level of task titles in an ordered dict for later usage in layout
samples_by_granularity = OrderedDict([
    ("Finest decomposition of task", ["t_go_to_start_bay",
                                      "t_couple_trolley",
                                      "t_undock_trolley",
                                      "t_exit_start_bay",
                                      "t_go_to_end_bay",
                                      "sum_navigation_failures",
                                      "t_visual_align",
                                      "t_drop_trolley",
                                      "t_undock_robot"]),
    ("Coarse decomposition of task", ["total_go_to_start_bay",
                                      "total_couple_trolley_and_exit_bay",
                                      "total_go_to_end_bay",
                                      "total_drop_trolley_in_bay"]),
    ("No decomposition of task", ["total_spent"])
])

# dict for translating the task titles to more readable phrases
title_translation = {
    "t_go_to_start_bay": "Go to the start station",
    "t_couple_trolley": "Couple with the trolley",
    "t_undock_trolley": "Undock the coupled trolley",
    "t_exit_start_bay": "Exit the start station",
    "t_go_to_end_bay": "Go to the destination station",
    "sum_navigation_failures": "Total navigation failure",
    "t_visual_align": "Visual alignment",
    "t_drop_trolley": "Drop the trolley",
    "t_undock_robot": "Undock the robot",
    "total_go_to_start_bay": "Go to the start station",
    "total_couple_trolley_and_exit_bay": "Couple with the trolley and exit the start station",
    "total_go_to_end_bay": "Go to the destination station",
    "total_drop_trolley_in_bay": "Drop the trolley in the destination station",
    "total_spent": "Total time spent for the whole task"
}


# load the task samples from csv path
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

# actually load the task samples
sample_csv_path = "./data/12_samples.csv"
loaded_title, loaded_sample_names, loaded_samples = load_samples(sample_csv_path)


# load all the tasks in short and long run trials from csv path
def load_tasks(task_csv):
    with open(task_csv, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        return [Task().from_list(row) for row in reader]

# actually load all the tasks in short and long run trials
short_run_csv_path = "./data/2018-03-22-15-19-10-extract.bag.csv"
long_run_csv_path = "./data/2018-03-22-17-27-17-extract.bag.csv"
short_run_tasks = load_tasks(short_run_csv_path)
long_run_tasks = load_tasks(long_run_csv_path)
l_short = len(short_run_tasks)
l_long = len(long_run_tasks)


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
