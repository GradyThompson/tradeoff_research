import queue
from queue import PriorityQueue
from simulated_system import SimulatedSystem
from job import Job
from model import Model
import job_manager

"""
Controls a state-based simulated system of jobs and machines
"""
class Controller:
    """
    Initializes controller

    Args:
        config_file_name: name of file with config information

    Config file:
        <input_jobs_file_name>
        <results_file_name>
        <model_module_name>,<model_class_name>,<model params (comma separated)>
        <startup_time>
    """
    def __init__(self, config_file_name:str):
        with open(config_file_name) as config_file:
            file_lines:list[str] = [line.strip() for line in config_file.readlines()]
            input_jobs_file_name:str = file_lines[0]
            results_file_name:str = file_lines[1]
            model_info:list[str] = file_lines[2].split(",")
            startup_duration:int = int(file_lines[3])

            model_module_name:str = model_info[0]
            model_class_name:str = model_info[1]
            model_params:list[str] = model_info[2:]

        self.system:SimulatedSystem = SimulatedSystem(startup_duration=startup_duration, curr_time=0)
        self.model:Model = Model(module_name=model_module_name, class_name=model_class_name, params=model_params)
        self.results_file_name = results_file_name
        self.time:int = 0

        self.jobs: list[Job] = job_manager.jobs_from_file(input_jobs_file_name)
        self.queued_jobs: PriorityQueue[Job] = queue.PriorityQueue()
        for job in self.jobs:
            self.queued_jobs.put(job)

    """
    Gets the release time of the next job
    """
    def next_job_release_time(self):
        job = self.queued_jobs.get()
        self.queued_jobs.put(job)
        
        time = job.get_receival_time()
        
        return time

    """
    Runs the system until completion
    """
    def control_loop(self):
        while len(self.queued_jobs) > 0:
            next_time = self.next_job_release_time()
            new_jobs = []
            while len(self.queued_jobs) > 0:
                next_job = self.queued_jobs.get()
                if next_job.get_receival_time() != next_time:
                    self.queued_jobs.put(next_job)
                    break
                else:
                    new_jobs.append(next_job)
            self.system_simulator.run(next_time)
            actions = self.model.determine_actions(system=self.system_simulator, unassigned_jobs=new_jobs)
            self.system_simulator.perform_actions(actions=actions)
            self.time = next_time
        self.system_simulator.finish()
