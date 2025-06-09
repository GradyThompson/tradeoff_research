from simulated_system import SimulatedSystem
from job import Job
from model import Model
import job_manager
import heapq
from action import Action
import result_manager

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

        self.jobs:list[Job] = job_manager.jobs_from_file(input_jobs_file_name)
        self.queued_jobs:list[Job] = []
        for job in self.jobs:
            heapq.heappush(self.queued_jobs, job)

    """
    Runs the system until completion
    
    Args:
        results_file_name: where the results of the system are stored
        
    Returns:
        The name of the file with the results
    """
    def control_loop(self)->str:
        wait_time:int = -1
        while len(self.queued_jobs) > 0:
            #Prepare next set of batches and update system
            next_time:int = self.queued_jobs[0].get_receival_time()
            if wait_time != -1:
                next_time = min(next_time, wait_time)
            wait_time = -1
            new_jobs:list[Job] = []
            while len(self.queued_jobs) > 0 and self.queued_jobs[0].get_receival_time() <= next_time:
                new_jobs.append(self.queued_jobs.pop(0))
            self.system.run(next_time)

            #Get and handle actions
            actions:list[Action] = self.model.determine_actions(system=self.system, unassigned_jobs=new_jobs)
            for action in actions:
                if action.get_action_type() == Action.WAIT:
                    wait_time = action.get_time()
            self.system.perform_actions(actions=actions)
            self.time = next_time
        self.system.finish()
        result_manager.save_system_performance(self.system, self.jobs, self.results_file_name)
        return self.results_file_name