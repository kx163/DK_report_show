from scipy.stats import norm
from collections import Counter
import numpy as np


# The Gaussian model class
class GaussianModel(object):
    def __init__(self):
        self.mean = 0.0
        self.std = 0.0

    def fit(self, data):
        self.mean, self.std = norm.fit(data)


# The Poisson model class
class PoissonModel(object):
    def __init__(self):
        self.k = 0.0

    def fit(self, data):
        self.k = float(sum([k * v for k, v in Counter(data).items()])) / len(data)


# The plain class to store the probabilistic model of the tasks
class TaskModel(object):
    def __init__(self):
        self.t_go_to_start_bay = GaussianModel()
        self.t_couple_trolley = GaussianModel()
        self.t_undock_trolley = GaussianModel()
        self.t_exit_start_bay = GaussianModel()
        self.t_go_to_end_bay = GaussianModel()
        self.t_visual_align = GaussianModel()
        self.t_drop_trolley = GaussianModel()
        self.t_undock_robot = GaussianModel()

        self.d_navigation = GaussianModel()

        self.n_estop = PoissonModel()
        self.n_joy_twist = PoissonModel()
        self.n_joystick = PoissonModel()

        self.n_navigation_failure = PoissonModel()
        self.t_navigation_failures = GaussianModel()
        self.navigation_failure_per_meter = PoissonModel()

        self.navigation_speed = GaussianModel()
        self.obstacle_per_meter = PoissonModel()

        self.total_go_to_start_bay = GaussianModel()
        self.total_couple_trolley_and_exit_bay = GaussianModel()
        self.total_go_to_end_bay = GaussianModel()
        self.total_drop_trolley_in_bay = GaussianModel()
        self.total_spent = GaussianModel()

        self.meters_per_navigation_failure = 0.0
        self.meters_per_obstacle = 0.0

    def to_list(self):
        return [
            self.t_go_to_start_bay.mean,
            self.t_go_to_start_bay.std,
            self.t_couple_trolley.mean,
            self.t_couple_trolley.std,
            self.t_undock_trolley.mean,
            self.t_undock_trolley.std,
            self.t_exit_start_bay.mean,
            self.t_exit_start_bay.std,
            self.t_go_to_end_bay.mean,
            self.t_go_to_end_bay.std,
            self.t_visual_align.mean,
            self.t_visual_align.std,
            self.t_drop_trolley.mean,
            self.t_drop_trolley.std,
            self.t_undock_robot.mean,
            self.t_undock_robot.std,

            self.d_navigation.mean,
            self.d_navigation.std,

            self.n_estop.k,
            self.n_joy_twist.k,
            self.n_joystick.k,

            self.n_navigation_failure.k,
            self.t_navigation_failures.mean if not np.isnan(self.t_navigation_failures.mean) else 0.,
            self.t_navigation_failures.std if not np.isnan(self.t_navigation_failures.std) else 0.,
            self.navigation_failure_per_meter.k,

            self.navigation_speed.mean,
            self.navigation_speed.std,
            self.obstacle_per_meter.k,

            self.total_go_to_start_bay.mean,
            self.total_go_to_start_bay.std,
            self.total_couple_trolley_and_exit_bay.mean,
            self.total_couple_trolley_and_exit_bay.std,
            self.total_go_to_end_bay.mean,
            self.total_go_to_end_bay.std,
            self.total_drop_trolley_in_bay.mean,
            self.total_drop_trolley_in_bay.std,
            self.total_spent.mean,
            self.total_spent.std,

            self.meters_per_navigation_failure,
            self.meters_per_obstacle
        ]

    def from_list(self, row):
        self.t_go_to_start_bay.mean = float(row[0])
        self.t_go_to_start_bay.std = float(row[1])
        self.t_couple_trolley.mean = float(row[2])
        self.t_couple_trolley.std = float(row[3])
        self.t_undock_trolley.mean = float(row[4])
        self.t_undock_trolley.std = float(row[5])
        self.t_exit_start_bay.mean = float(row[6])
        self.t_exit_start_bay.std = float(row[7])
        self.t_go_to_end_bay.mean = float(row[8])
        self.t_go_to_end_bay.std = float(row[9])
        self.t_visual_align.mean = float(row[10])
        self.t_visual_align.std = float(row[11])
        self.t_drop_trolley.mean = float(row[12])
        self.t_drop_trolley.std = float(row[13])
        self.t_undock_robot.mean = float(row[14])
        self.t_undock_robot.std = float(row[15])

        self.d_navigation.mean = float(row[16])
        self.d_navigation.std = float(row[17])

        self.n_estop.k = float(row[18])
        self.n_joy_twist.k = float(row[19])
        self.n_joystick.k = float(row[20])

        self.n_navigation_failure.k = float(row[21])
        self.t_navigation_failures.mean = float(row[22])
        self.t_navigation_failures.std = float(row[23])
        self.navigation_failure_per_meter.k = float(row[24])

        self.navigation_speed.mean = float(row[25])
        self.navigation_speed.std = float(row[26])
        self.obstacle_per_meter.k = float(row[27])

        self.total_go_to_start_bay.mean = float(row[28])
        self.total_go_to_start_bay.std = float(row[29])
        self.total_couple_trolley_and_exit_bay.mean = float(row[30])
        self.total_couple_trolley_and_exit_bay.std = float(row[31])
        self.total_go_to_end_bay.mean = float(row[32])
        self.total_go_to_end_bay.std = float(row[33])
        self.total_drop_trolley_in_bay.mean = float(row[34])
        self.total_drop_trolley_in_bay.std = float(row[35])
        self.total_spent.mean = float(row[36])
        self.total_spent.std = float(row[37])

        self.meters_per_navigation_failure = float(row[38])
        self.meters_per_obstacle = float(row[39])
        return self

    @staticmethod
    def to_title_list():
        return [
            "t_go_to_start_bay.mean",
            "t_go_to_start_bay.std",
            "t_couple_trolley.mean",
            "t_couple_trolley.std",
            "t_undock_trolley.mean",
            "t_undock_trolley.std",
            "t_exit_start_bay.mean",
            "t_exit_start_bay.std",
            "t_go_to_end_bay.mean",
            "t_go_to_end_bay.std",
            "t_visual_align.mean",
            "t_visual_align.std",
            "t_drop_trolley.mean",
            "t_drop_trolley.std",
            "t_undock_robot.mean",
            "t_undock_robot.std",

            "d_navigation.mean",
            "d_navigation.std",

            "n_estop.k",
            "n_joy_twist.k",
            "n_joystick.k",

            "n_navigation_failure.k",
            "t_navigation_failures.mean",
            "t_navigation_failures.std",
            "navigation_failure_per_meter.k",

            "navigation_speed.mean",
            "navigation_speed.std",
            "obstacle_per_meter.k",

            "total_go_to_start_bay.mean",
            "total_go_to_start_bay.std",
            "total_couple_trolley_and_exit_bay.mean",
            "total_couple_trolley_and_exit_bay.std",
            "total_go_to_end_bay.mean",
            "total_go_to_end_bay.std",
            "total_drop_trolley_in_bay.mean",
            "total_drop_trolley_in_bay.std",
            "total_spent.mean",
            "total_spent.std",

            "meters_per_navigation_failure",
            "meters_per_obstacle"
        ]
