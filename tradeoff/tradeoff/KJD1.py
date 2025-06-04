import incomplete.simulated_system as sim_sys
from job import Job
from tradeoff.action import Action

"""
Known job duration algorithm 1
"""


class KJD1:
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
        A list of actions to be performed on the system
    """

    def determine_actions(self, system: sim_sys.SimulatedSystem, pending_jobs: list[Job])->list[Action]:
        actions:list[Action] = []

        delta:int = system.get_startup_time()
        e_star:int = int(2 * delta/ self.epsilon)
        time:int = system.get_time()
        short_jobs:list[Job] = []
        sorted_jobs:list[Job] = sorted(pending_jobs, key=lambda x: x.get_receival_time())
        accumulated_volume:int = 0

        for job in sorted_jobs:
            if job.get_execution_time() >= e_star:
                actions.append(Action(action_type=Action.ACTIVATE_CONTAINER, jobs=[job]))
            else:
                short_jobs.append(job)
                accumulated_volume += job.get_execution_time()
                if accumulated_volume >= e_star:
                    actions.append(Action(action_type=Action.ACTIVATE_CONTAINER, jobs=short_jobs))
                    short_jobs = []
                    accumulated_volume = 0

        if len(short_jobs) >= 1 and time >= short_jobs[0].get_receival_time() + e_star - delta:
            actions.append(Action(action_type=Action.ACTIVATE_CONTAINER, jobs=short_jobs))

        return actions