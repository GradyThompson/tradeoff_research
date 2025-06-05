from simulated_system import SimulatedSystem
from job import Job

"""
Saves the system performance results, including cost and queue time information

Args:
    system: The system with containers
    jobs: The list of jobs
    data_file_name: The name of the file to store the information into
    
File:
    Cost <total system cost>
    <Job_1 Queue Time>
    <Job_2 Queue Time>
    ...
    <Job_n Queue Time>
"""
def save_system_performance(system:SimulatedSystem, jobs:list[Job], data_file_name:str):
    cost:int = system.get_cost()
    with open(data_file_name, "w") as data_file:
        data_file.write("Cost str(cost)")
        for job in jobs:
            data_file.write("\n" + str(job.get_queue_time()))