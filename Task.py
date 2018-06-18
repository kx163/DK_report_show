import ast


# The plain class to store the analytic data of one task
class Task(object):
    def __init__(self):
        self.id_start_bay = 0
        self.id_end_bay = 0
        self.t_go_to_start_bay = 0
        self.t_couple_trolley = 0
        self.t_undock_trolley = 0
        self.t_exit_start_bay = 0
        self.t_go_to_end_bay = 0
        self.t_navigation_failures = []
        self.n_navigation_failure = 0
        self.n_estop = 0
        self.n_joy_twist = 0
        self.n_joystick = 0
        self.d_navigation = 0.0
        self.t_visual_align = 0
        self.t_drop_trolley = 0
        self.t_undock_robot = 0
        self.sum_navigation_failures = 0
        self.total_go_to_start_bay = 0
        self.total_couple_trolley_and_exit_bay = 0
        self.total_go_to_end_bay = 0
        self.total_drop_trolley_in_bay = 0
        self.total_spent = 0

    def finalise(self):
        self.total_go_to_start_bay = self.t_go_to_start_bay
        self.total_couple_trolley_and_exit_bay = self.t_couple_trolley + self.t_undock_trolley + self.t_exit_start_bay
        self.sum_navigation_failures = sum(self.t_navigation_failures)
        self.total_go_to_end_bay = self.t_go_to_end_bay + self.sum_navigation_failures
        self.total_drop_trolley_in_bay = self.t_visual_align + self.t_drop_trolley + self.t_undock_robot
        self.total_spent = self.total_go_to_start_bay + self.total_couple_trolley_and_exit_bay + \
            self.total_go_to_end_bay + self.total_drop_trolley_in_bay

    def to_list(self):
        return [self.id_start_bay,
                self.id_end_bay,
                self.t_go_to_start_bay,
                self.t_couple_trolley,
                self.t_undock_trolley,
                self.t_exit_start_bay,
                self.t_go_to_end_bay,
                self.t_navigation_failures,
                self.n_navigation_failure,
                self.n_estop,
                self.n_joy_twist,
                self.n_joystick,
                self.d_navigation,
                self.t_visual_align,
                self.t_drop_trolley,
                self.t_undock_robot,
                self.sum_navigation_failures,
                self.total_go_to_start_bay,
                self.total_couple_trolley_and_exit_bay,
                self.total_go_to_end_bay,
                self.total_drop_trolley_in_bay,
                self.total_spent]

    def from_list(self, row):
        self.id_start_bay = int(ast.literal_eval(row[0]))
        self.id_end_bay = int(ast.literal_eval(row[1]))
        self.t_go_to_start_bay = int(ast.literal_eval(row[2]))
        self.t_couple_trolley = int(ast.literal_eval(row[3]))
        self.t_undock_trolley = int(ast.literal_eval(row[4]))
        self.t_exit_start_bay = int(ast.literal_eval(row[5]))
        self.t_go_to_end_bay = int(ast.literal_eval(row[6]))
        self.t_navigation_failures = ast.literal_eval(row[7]) if isinstance(row[7], str) else row[7]
        self.n_navigation_failure = int(ast.literal_eval(row[8]))
        self.n_estop = int(ast.literal_eval(row[9]))
        self.n_joy_twist = int(ast.literal_eval(row[10]))
        self.n_joystick = int(ast.literal_eval(row[11]))
        self.d_navigation = float(ast.literal_eval(row[12]))
        self.t_visual_align = int(ast.literal_eval(row[13]))
        self.t_drop_trolley = int(ast.literal_eval(row[14]))
        self.t_undock_robot = int(ast.literal_eval(row[15]))
        self.sum_navigation_failures = int(ast.literal_eval(row[16]))
        self.total_go_to_start_bay = int(ast.literal_eval(row[17]))
        self.total_couple_trolley_and_exit_bay = int(ast.literal_eval(row[18]))
        self.total_go_to_end_bay = int(ast.literal_eval(row[19]))
        self.total_drop_trolley_in_bay = int(ast.literal_eval(row[20]))
        self.total_spent = int(ast.literal_eval(row[21]))
        return self

    @staticmethod
    def to_title_list():
        return ["id_start_bay",
                "id_end_bay",
                "t_go_to_start_bay",
                "t_couple_trolley",
                "t_undock_trolley",
                "t_exit_start_bay",
                "t_go_to_end_bay",
                "t_navigation_failures",
                "n_navigation_failure",
                "n_estop",
                "n_joy_twist",
                "n_joystick",
                "d_navigation",
                "t_visual_align",
                "t_drop_trolley",
                "t_undock_robot",
                "sum_navigation_failures",
                "total_go_to_start_bay",
                "total_couple_trolley_and_exit_bay",
                "total_go_to_end_bay",
                "total_drop_trolley_in_bay",
                "total_spent"]
