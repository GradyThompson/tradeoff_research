import task_generation
import task
import schedulers as s
import controller
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import ast
import math

test_name = "final_zoomed"
delta = 1

tests_location = "./tests/"
results_location = "./results/"

def optimal_cost(tasks, queue_time, delta):
    num_containers = math.ceil(sum([task.get_execution_time() for task in tasks])/(queue_time + max([task.get_receival_time() for task in tasks]) + max([task.get_execution_time() for task in tasks])))
    cost = num_containers*delta + sum([task.get_execution_time() for task in tasks])
    return cost

latest_receival_time = 0
max_stretch = 0

#Generates the tasks for the task arguments
task_arguments = [
    {"id":"task1", "number":500, "stretch":10.0, "start_receiving_time":0.0, "stop_receiving_time":10.0, "time_unit":0.01, "average_time":1, "time_variance":1.0, "offset": 0.0},
    {"id":"task2", "number":500, "stretch":10.0, "start_receiving_time":5.0, "stop_receiving_time":15.0, "time_unit":0.01, "average_time":1, "time_variance":1.0, "offset": 0.0}
]

tasks = []
for arguments in task_arguments:
    id = arguments.get("id")
    number = arguments.get("number")
    stretch = arguments.get("stretch")
    start_receiving_time = arguments.get("start_receiving_time")
    stop_receiving_time = arguments.get("stop_receiving_time")
    time_unit = arguments.get("time_unit")
    average_time = arguments.get("average_time")
    time_variance = arguments.get("time_variance")
    offset = arguments.get("offset")

    task_set = task_generation.generate_tasks(id_prefix=id,
                                       number=number, 
                                       stretch=stretch, 
                                       start_receiving_time=start_receiving_time,
                                       stop_receiving_time=stop_receiving_time, 
                                       time_unit=time_unit, 
                                       average_time=average_time, 
                                       time_variance=time_variance)

    #Adds offset in the case of multiple task sets
    for task in task_set:
        task.receival_time += offset

    tasks.extend(task_set)

    if stop_receiving_time > latest_receival_time:
        latest_receival_time = stop_receiving_time

    if stretch > max_stretch:
        max_stretch = stretch

longest_task = max([task.get_execution_time() for task in tasks])
total_execution_time = sum([task.get_execution_time() for task in tasks])

expected_number_containers = total_execution_time//latest_receival_time

#Map of scheduler name to controllers
schedulers = {}

# Generate fixed containers up to 20
num_containers = 3
while num_containers <= 200:
    int_num_containers = int(num_containers)
    schedulers["EDF-%sC" % (int_num_containers)] = controller.Controller(tasks=tasks, scheduler=s.EDF_scheduler, delta=delta, num_containers=int_num_containers)
    num_containers += 1

#Add deterministic and bounded for epsilon of increments 0.05
change = 0.0005
epsilon = change
while epsilon < 1:
    schedulers["double-e-%s" % (epsilon)] = controller.Controller(tasks=tasks, scheduler=s.bounded_double_scheduler, epsilon=epsilon, delta=delta)
    schedulers["deterministic-e-%s" % (epsilon)] = controller.Controller(tasks=tasks, scheduler=s.deterministic_scheduler, epsilon=epsilon, delta=delta)
    schedulers["bounded-e-%s" % (epsilon)] = controller.Controller(tasks=tasks, scheduler=s.bounded_scheduler, epsilon=epsilon, delta=delta)
    epsilon *= 1.5
    epsilon = round(epsilon, 5)

#Stores the results of the simulations, key is the algorithm, value is [<queue times>, <cost>]
results = {"algorithm":[], "queue_times":[], "cost":[], "cost_ratio":[]}

for algorithm in schedulers.keys():
    print(algorithm)
    cost = schedulers.get(algorithm).run()
    queue_times = schedulers.get(algorithm).get_queue_times()
    results["algorithm"].append(algorithm)
    results["queue_times"].append(list(queue_times))
    results["cost"].append(cost)
    results["cost_ratio"].append(cost/optimal_cost(tasks=tasks, queue_time=max(queue_times), delta=delta))

#Adds optimal points
for queue_time in range(delta, (delta + math.ceil(sum([task.get_execution_time() for task in tasks])))//2, 20):
    results["algorithm"].append("optimal-%s" % (queue_time))
    results["queue_times"].append([queue_time])
    results["cost"].append(optimal_cost(tasks=tasks, queue_time=queue_time, delta=delta))
    results["cost_ratio"].append(1)

df = pd.DataFrame(results)
df.to_csv(results_location + test_name + ".csv", index=False)