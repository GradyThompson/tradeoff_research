from system.simulated_system import SimulatedSystem
from system.job import Job
from system.action import Action
import util.scheduler_util as scheduler_util

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
        self.epsilon:float = float(params[0])

    """
    Decides system actions based on the deterministic execution time of jobs

    Args:
        system: The system being scheduled upon
        pending_jobs: a list of pending jobs
        
    Return:
        A list of actions to be performed on the system
    """

    def determine_actions(self, system: SimulatedSystem, pending_jobs: list[Job])->list[Action]:
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

        next_deadline: int = -1

        if len(short_jobs) >= 1 and time >= short_jobs[0].get_receival_time() + e_star - delta:
            actions.append(Action(action_type=Action.ACTIVATE_CONTAINER, jobs=short_jobs))
        elif len(short_jobs) >= 1:
            next_deadline = short_jobs[0].get_receival_time() + e_star - delta

        time_until_next_action: int = scheduler_util.terminate_stale_containers(system, actions)
        if next_deadline != -1:
            time_until_next_action = min(time_until_next_action, next_deadline)

        if time_until_next_action != -1:
            actions.append(Action(action_type=Action.WAIT, time=time+time_until_next_action))

        return actions