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
        system: the system being run upon
        model: the scheduling model being used
        jobs: the jobs to be run in the system
        results_file_name: name of the file the results will be stored in
    """
    def __init__(self, system:SimulatedSystem, model:Model, jobs:list[Job], results_file_name:str):
        self.system:SimulatedSystem = system
        self.model:Model = model
        self.results_file_name:str = results_file_name
        self.time:int = 0
        self.wait_time:int = -1

        self.jobs:list[Job] = jobs
        self.job_ind:int = 0
        self.queued_jobs: list[Job] = []

    """
    Returns the system
    
    Returns:
        The system
    """
    def get_system(self):
        return self.system

    """
    Returns the queued jobs

    Returns:
        The queued jobs
    """

    def get_queued_jobs(self):
        return self.queued_jobs

    """
    Moves the controller to the next step, continues until the earlier of the wait time and the next job release time
    
    Args:
        actions: list of actions to perform if not using the set model
    
    Returns:
        The simulated system and queued jobs
    """
    def next_step(self, actions:list[Action] = None)->typing.Tuple[SimulatedSystem, list[Job]]:
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
        if actions is None:
            actions = self.model.determine_actions(system=self.system, unassigned_jobs=self.queued_jobs)
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
    """
    def reset(self):
        self.system.reset()
        self.queued_jobs = []
        self.job_ind = 0
        self.time:int = 0
        self.wait_time:int = -1

    """
    Checks if the simulation is done
    
    Returns:
        True if the system is done and False otherwise
    """
    def is_done(self):
        return self.job_ind >= len(self.jobs) and self.wait_time == -1

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

    """
    Parses a config file

    Args:
        config_file_name: name of file with config information

    Config file:
        <input_jobs_file_name>
        <results_file_name>
        <model_module_name>,<model_class_name>,<model params (comma separated)>
        <startup_time>

    Returns:
        The system
        The scheduling model
        The list of jobs to be run on the system
        The name of the file the results should be stored in
    """
    @staticmethod
    def parse_config(config_file_name: str) -> typing.Tuple[SimulatedSystem, Model, list[Job], str]:
        with open(config_file_name) as config_file:
            file_lines: list[str] = [line.strip() for line in config_file.readlines()]
            input_jobs_file_name: str = file_lines[0]
            results_file_name: str = file_lines[1]
            model_info: list[str] = file_lines[2].split(",")
            startup_duration: int = int(file_lines[3])

            model_module_name: str = model_info[0]
            model_class_name: str = model_info[1]
            model_params: list[str] = model_info[2:]

        system: SimulatedSystem = SimulatedSystem(startup_duration=startup_duration, curr_time=0)
        model: Model = Model(module_name=model_module_name, class_name=model_class_name, params=model_params)
        jobs: list[Job] = sorted(job_manager.jobs_from_file(input_jobs_file_name))

        return system, model, jobs, results_file_name