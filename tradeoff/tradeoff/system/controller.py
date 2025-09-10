from system.simulated_system import SimulatedSystem
from system.job import Job
from schedulers.model import Model
from jobs import job_manager
from system.action import Action
from results import result_manager
import typing
import heapq

"""
Controls a state-based simulated system of jobs and machines
"""
class Controller:
    """
    Initializes controller

    Args:
        startup_duration: the startup time of the system
        model_config_file: name of the file containing the model configuration information (empty if manual)
        jobs_file: the file containing the jobs (empty if manual)
        results_file: file where results will be stored (empty if manual)
        manual_control: true if the system is manually controlled, false if system is automatically controlled

    model_config_file:
        <model_module_name>,<model_class_name>,<model params (comma separated)>

    jobs_file:
        <id>,<receival_time>,<execution_time>,<deadline>
            or
        <id>,<receival_time>,<execution_time>,<deadline>,<lower_bound>,<upper_bound>
    """
    def __init__(self, startup_duration:int, model_config_file:str="",  jobs_file:str="", results_file:str="", manual_control:bool=False):
        if not manual_control:
            with open(model_config_file) as config_file:
                config_file_lines: list[str] = [line.strip() for line in config_file.readlines()]
            model_info: list[str] = config_file_lines[0].split(",")
            model_module_name: str = model_info[0]
            model_class_name: str = model_info[1]
            model_params: list[str] = model_info[2:]
            model = Model(module_name=model_module_name, class_name=model_class_name, params=model_params)
            self.model: Model = model
            self.results_file_name: str = results_file

        if jobs_file != "":
            self.jobs: list[Job] = sorted(job_manager.jobs_from_file(file_name=jobs_file))
        else:
            self.jobs: list[Job] = []
        heapq.heapify(self.jobs)
        self.job_ind: int = 0
        self.queued_jobs: list[Job] = []

        self.system:SimulatedSystem = SimulatedSystem(startup_duration=startup_duration, curr_time=0)

        self.time:int = 0

    """
    Adds jobs to the system
    
    Args:
        jobs: the jobs to add
    """
    def add_jobs(self, jobs:list[Job]):
        for job in jobs:
            heapq.heappush(self.jobs, job)

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
    def get_queued_jobs(self)->list[Job]:
        return self.queued_jobs

    """
    Returns the time
    
    Returns:
        The time
    """
    def get_time(self)->int:
        return self.time

    """
    Moves the controller to the next step, continues until the earlier of the wait time and the next job release time
    
    Args:
        actions: list of actions to perform if not using the set model
    
    Returns:
        The simulated system and queued jobs
    """
    def next_step(self, actions:list[Action] = None)->typing.Tuple[SimulatedSystem, list[Job]]:
        if not hasattr(self, "model") and actions is None:
            raise ValueError("No model nor action")
        if self.is_done():
            return self.system, self.queued_jobs

        # Get and handle actions
        if actions is None:
            actions = self.model.determine_actions(system=self.system, unassigned_jobs=self.queued_jobs)
        wait_time = -1
        for action in actions:
            if action.get_action_type() == Action.WAIT:
                wait_time = action.get_time()
        self.system.perform_actions(actions=actions)

        # Remove assigned jobs from queued
        jobs_to_remove: list[Job] = []
        assigned_jobs: set[Job] = self.system.get_assigned_jobs()
        for job in self.queued_jobs:
            if job in assigned_jobs:
                jobs_to_remove.append(job)
        for job in jobs_to_remove:
            self.queued_jobs.remove(job)

        if wait_time == -1 and self.job_ind == len(self.jobs):
            next_time = self.time + self.system.get_time_until_done()
        elif wait_time == -1:
            next_time = self.jobs[self.job_ind].get_receival_time()
        elif self.job_ind == len(self.jobs):
            next_time = wait_time
        else:
            next_time = min(self.jobs[self.job_ind].get_receival_time(), wait_time)

        next_time = max(next_time, self.time + 1)

        self.system.run(next_time)

        while self.job_ind < len(self.jobs) and self.jobs[self.job_ind].get_receival_time() <= self.system.get_time():
            self.queued_jobs.append(self.jobs[self.job_ind])
            self.job_ind += 1

        self.time = next_time

        return self.system, self.queued_jobs

    """
    Resets the system
    """
    def reset(self):
        self.system.reset()
        self.queued_jobs = []
        self.job_ind = 0
        self.time:int = 0

    """
    Checks if the simulation is done
    
    Returns:
        True if the system is done and False otherwise
    """
    def is_done(self):
        return self.job_ind >= len(self.jobs) and len(self.queued_jobs) == 0 and self.system.get_time_until_done() == 0

    """
    Runs the system until completion
        
    Returns:
        The name of the file with the results
    """
    def control_loop(self)->str:
        if not hasattr(self, "model"):
            raise ValueError("No model")
        while not self.is_done():
            self.next_step()
        result_manager.save_system_performance(self.system, self.jobs, self.results_file_name)
        return self.results_file_name