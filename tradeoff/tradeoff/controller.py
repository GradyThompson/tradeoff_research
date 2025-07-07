from simulated_system import SimulatedSystem
from job import Job
from model import Model
import job_manager
from action import Action
import result_manager
import typing

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
        self.results_file_name:str = results_file_name
        self.time:int = 0
        self.wait_time:int = -1

        self.jobs:list[Job] = sorted(job_manager.jobs_from_file(input_jobs_file_name))
        self.job_ind:int = 0
        self.queued_jobs: list[Job] = []

    """
    Moves the controller to the next step, continues until the earlier of the wait time and the next job release time
    
    Returns:
        The simulated system and queued jobs
    """
    def next_step(self)->typing.Tuple[SimulatedSystem, list[Job]]:
        if self.wait_time == -1:
            next_time = self.jobs[self.job_ind].get_receival_time()
        elif self.job_ind == len(self.jobs):
            next_time = self.wait_time
        else:
            next_time = min(self.jobs[self.job_ind].get_receival_time(), self.wait_time)
        self.wait_time = -1
        while self.job_ind < len(self.jobs) and self.jobs[self.job_ind].get_receival_time() <= next_time:
            self.queued_jobs.append(self.jobs[self.job_ind])
            self.job_ind += 1
        self.system.run(next_time)

        # Get and handle actions
        actions: list[Action] = self.model.determine_actions(system=self.system, unassigned_jobs=self.queued_jobs)
        for action in actions:
            if action.get_action_type() == Action.WAIT:
                self.wait_time = action.get_time()
        self.system.perform_actions(actions=actions)
        self.time = next_time

        # Remove assigned jobs from queued
        jobs_to_remove: list[Job] = []
        assigned_jobs: set[Job] = self.system.get_assigned_jobs()
        for job in self.queued_jobs:
            if job in assigned_jobs:
                jobs_to_remove.append(job)
        for job in jobs_to_remove:
            self.queued_jobs.remove(job)
        return self.system, self.queued_jobs

    """
    Resets the system
    
    Returns:
        The simulated system and queued jobs after reset
    """
    def reset(self)->typing.Tuple[SimulatedSystem, list[Job]]:
        self.system.reset()
        self.queued_jobs = []
        self.job_ind = 0
        self.time:int = 0
        self.wait_time:int = -1
        return self.system, self.queued_jobs

    """
    Runs the system until completion
        
    Returns:
        The name of the file with the results
    """
    def control_loop(self)->str:
        while self.job_ind < len(self.jobs) or self.wait_time != -1:
            self.next_step()
        time_until_done:int = self.system.get_time_until_done()
        self.system.run(self.time + time_until_done)
        result_manager.save_system_performance(self.system, self.jobs, self.results_file_name)
        return self.results_file_name