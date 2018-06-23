import os
import csv
from Task import Task
from TaskModel import TaskModel
from collections import OrderedDict
from setup import root_path


data_path = os.path.join(root_path, 'data')
print data_path


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
model_csv_path = os.path.join(data_path, "2_models.csv")
short_run_model, long_run_model = load_models(model_csv_path)
# store the models in an ordered dict for later usage in layout
model_choices = OrderedDict([("busy", short_run_model), ("quiet", long_run_model)])

# store the robot specs in an ordered dict for later usage in layout
robot_choices = OrderedDict([("current", current_robot), ("next-gen", next_robot)])


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
sample_csv_path = os.path.join(data_path, "12_samples.csv")
loaded_title, loaded_sample_names, loaded_samples = load_samples(sample_csv_path)


# load all the tasks in short and long run trials from csv path
def load_tasks(task_csv):
    with open(task_csv, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        return [Task().from_list(row) for row in reader]

# actually load all the tasks in short and long run trials
short_run_csv_path = os.path.join(data_path, "2018-03-22-15-19-10-extract.bag.csv")
long_run_csv_path = os.path.join(data_path, "2018-03-22-17-27-17-extract.bag.csv")
short_run_tasks = load_tasks(short_run_csv_path)
long_run_tasks = load_tasks(long_run_csv_path)
l_short = len(short_run_tasks)
l_long = len(long_run_tasks)
