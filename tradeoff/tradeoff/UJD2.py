import tradeoff.simulated_system as sim_sys
from tradeoff.container import Container
from job import Job
from tradeoff.action import Action

"""
Unknown job duration algorithm 2
"""
class UJD2:
    """
    Constructor, saves epsilon to a class variable

    Args:
        params a list of parameters (length 1) 1. epsilon
    """
    def __init__(self, params: list):
        self.epsilon = params[0]

    """
    Decides system actions based on the deterministic execution time of jobs

    Args:
        system: The system being scheduled upon
        pending_jobs: a list of pending jobs
        
    Return:
        returns list of actions to perform
    """

    def determine_actions(self, system:sim_sys.SimulatedSystem, pending_jobs:list[Job])->list[Action]:
        actions:list[Action] = []

        delta: int = system.get_startup_time()
        max_delay: int = int(delta * (1 + 1 / self.epsilon))
        time: int = system.get_time()
        containers: set[Container] = system.get_containers()
        sorted_jobs: list[Job] = sorted(pending_jobs, key=lambda x: x.get_receival_time())
        job_ind: int = 0

        # Assign jobs to underfull containers
        for container in containers:
            assigned_jobs: list[Job] = []
            curr_container_time: int = container.time_until_done()
            while (job_ind < len(sorted_jobs)
                   and curr_container_time + time - sorted_jobs[job_ind].get_receival_time() <= max_delay):
                curr_container_time += sorted_jobs[job_ind].get_execution_time()
                assigned_jobs.append(sorted_jobs[job_ind])
                job_ind += 1

            if len(assigned_jobs) > 0:
                actions.append(Action(action_type=Action.ADD_JOBS, container=container, jobs=assigned_jobs))

        # Assign Jobs to new containers
        while (job_ind < len(sorted_jobs)
               and time + sum([job.get_execution_time() for job in sorted_jobs[job_ind:]])
               >= sorted_jobs[job_ind].get_receival_time() + max_delay - delta):
            curr_job_time = 0
            assigned_jobs = []
            while job_ind < len(sorted_jobs) and delta + curr_job_time <= max_delay:
                assigned_jobs.append(sorted_jobs[job_ind])
                curr_job_time += sorted_jobs[job_ind].get_execution_time()
                job_ind += 1
            if len(assigned_jobs) > 0:
                actions.append(Action(action_type=Action.ACTIVATE_CONTAINER, jobs=assigned_jobs))

        return actions