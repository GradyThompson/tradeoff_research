from system.simulated_system import SimulatedSystem
from system.job import Job
import typing
import matplotlib.pyplot as plt

"""
Saves the system performance results, including cost and queue time information

Args:
    system: The system with containers
    jobs: The list of jobs
    data_file_name: The name of the file to store the information into
    
File:
    Cost <total system cost>
    <Job_1 id>,<Job_1 Queue Time>
    <Job_2 id>,<Job_2 Queue Time>
    ...
    <Job_n id>,<Job_n Queue Time>
"""
def save_system_performance(system:SimulatedSystem, jobs:list[Job], data_file_name:str):
    cost:int = system.get_cost()
    with open(data_file_name, "w") as data_file:
        data_file.write("cost: " + str(cost))
        for job in jobs:
            data_file.write("\n" + job.get_id() + "," + str(job.get_queue_time()))


"""
Loads results from a file using the same formating as is outputed by save_system_performance

Args:
    file_name: name of file with the results
    
Returns:
    The cost
    The list of job queue times
"""
def load_file_results(file_name:str)->typing.Tuple[int, list[int]]:
    job_queue_times: list[int] = []
    cost = 0
    with open(file_name, "r") as data_file:
        data = data_file.readlines()
        cost = int(data[0].split(":")[1].strip())
        job_queue_times = [int(line.split(",")[1]) for line in data[1:]]
    return cost, job_queue_times

"""
Plots the graph of maximum queue delay vs cost for multiple schedulers

Args:
    scheduler_result_data: mapping of the name of schedulers to the name of the file containing their results
    
Scheduler name:
    <scheduler class>,<scheduler name>
"""
def plot_max_queue_v_cost(scheduler_result_data: typing.Dict[str, str]):
    labelled_data:typing.Dict[str, list[list[int]]] = {}
    for scheduler in scheduler_result_data.keys():
        scheduler_class = scheduler.split("_")[0]
        result_file_name = scheduler_result_data.get(scheduler)
        cost, queue_times = load_file_results(result_file_name)
        if scheduler_class in labelled_data.keys():
            labelled_data[scheduler_class][0].append(cost)
            labelled_data[scheduler_class][1].append(max(queue_times))
        else:
            labelled_data[scheduler_class] = [[cost], [max(queue_times)]]
    for label in labelled_data.keys():
        costs = labelled_data.get(label)[0]
        max_queue_times = labelled_data.get(label)[1]
        plt.scatter(x=costs, y=max_queue_times, label=label)
    plt.xlabel("Cost")
    plt.ylabel("Maximum Queue Time")
    plt.title('Cost vs Maximum Queue Time')
    plt.legend()
    plt.grid(True)
    plt.show()