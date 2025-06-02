#Utility
import importlib
import queue

#System classes
import simulated_system
import job_generator
import job
import model

"""
Controls a statebased simulated system of jobs and machines

Internal variables
system_simulator - SimulatedSystem - manages containers
model - Model - determines next actions
jobs - Set<Job> - set of all jobs in the system
queued_jobs - PriorityQueue<Job> - all jobs that have yet to run
"""
class Controller:
    """
    Initializes controller

    Inputs:
    input_jobs - Set<Job> - jobs inputed into the system
    model_meta_data_file_name - String - file name with model meta data
    """
    def __init__(self, input_jobs, model_meta_data_file_name):
        self.system_simulator = simulated_system.SimulatedSystem()
        self.model = model.Model(model_meta_data_file_name)
        self.jobs = input_jobs
        self.queued_jobs = queue.PriorityQueue()
        self.time = 0
        for job in self.jobs:
            self.queued_jobs.put(job)

    """
    Resets the system, this removes all current containers
    """
    def reset_system(self):
        self.system.reset()

    """
    Resets the job history to an empty priority queue
    """
    def reset_job_history(self):
        self.job_history = set()

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
