import task as T
import random
import numpy as np

"""
Generate random tasks

Input
number - the number of tasks generated
stretch - the maximum stretch (factor between max time and min time) of the tasks
stop_receiving_time - the time that tasks are no longer received
time_unit - the smallest unit of time
average_time - the average lower bound on task execution time
time_variance - the variance of the lower bound on task execution time

Returns a list of tasks
"""
def generate_tasks(id_prefix: str, number: int, stretch: float, start_receiving_time: float, stop_receiving_time: float, time_unit: float, average_time: float, time_variance: float) -> list[T.Task]:
    tasks = []
    for task_number in range(number):
        task_id = id_prefix + str(task_number)

        #Recieve task uniformly between start and end of period, rounded to time_unit
        receival_time = random.uniform(start_receiving_time, stop_receiving_time)//time_unit*time_unit

        #Lower bound is normal distribution
        lower_bound = max(np.random.normal(loc=average_time, scale=time_variance),
                          time_unit)//time_unit*time_unit

        #Upper bound is the stretch times the lower bound rounded to time_unit
        upper_bound =  stretch*lower_bound//time_unit*time_unit

        #Execution time is a normal distribution centered in the middle of lower and upper time
        execution_time = max(min(np.random.normal(loc=(upper_bound + lower_bound)/2, scale=(upper_bound - lower_bound)/4), 
                                upper_bound),
                             lower_bound)//time_unit*time_unit

        tasks.append(T.Task(task_id, execution_time, receival_time, lower_bound, upper_bound))
    return tasks

"""
Gets the tasks in the file

Input
file_path - a string with the file path

The file has the format (one task per line)
<ID>, <execution_time>, <receival_time>, <lower bound>, <upper bound>

Returns a list of the tasks in the file
"""
def tasks_from_file(file_path) -> list[T.Task]:
    tasks = []

    file = open(file_path, "r")
    for line in file:
        formatted_line = line.split(",")
        task_id = formatted_line[0]
        execution_time = float(formatted_line[1])
        recieval_time = float(formatted_line[2])
        lower_bound = float(formatted_line[3])
        upper_bound = float(formatted_line[4])
        tasks.append(T.Task(task_id, execution_time, recieval_time, lower_bound, upper_bound))

    file.close()
    return tasks

"""
Saves a list of tasks to a file

Input
tasks - the tasks
file_path - a string with the file path

The file has the format
<ID>, <execution_time>, <receival_time>
"""
def tasks_to_file(tasks: list[T.Task], file_path):
    file = open(file_path, "w")
    for task in tasks:
        line = ",".join([task.get_id(), 
                         str(task.get_execution_time()), 
                         str(task.get_receival_time()), 
                         str(task.get_bounds()[0]), 
                         str(task.get_bounds()[1])])
        file.write(line)
        if task != tasks[-1]:
            file.write("\n")
    file.close()