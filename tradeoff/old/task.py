"""
Computational task

Inputs
task_id - unique identifier of the task
execution_time - the execution time of the task - [<execution_time>, <min_bound>, <max_bound>]
receival_time - time the task is received by the system
lower_bound - the lower bound on the execution time
upper_bound - the upper bound on the execution time
"""
class Task:
    def __init__(self, task_id, execution_time, receival_time, lower_bound, upper_bound):
        self.task_id = task_id
        self.execution_time = execution_time
        self.receival_time = receival_time
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get_id(self):
        return self.task_id

    def get_execution_time(self):
        return self.execution_time

    def get_receival_time(self):
        return self.receival_time
    
    def get_bounds(self):
        return [self.lower_bound, self.upper_bound]