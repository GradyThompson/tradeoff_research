import incomplete.simulated_system as sim_sys
from job import Job
from tradeoff.action import Action

"""
Unknown job duration algorithm 1
"""
class UJD1:
    """
    Constructor, saves epsilon to a class variable

    Args:
        params a list of parameters (length 1) 1. epsilon
    """

    def __init__(self, params: list):
        self.epsilon = params[0]

    """
    Decides system actions based on the deterministic execution time of tasks

    Args:
        system: The system being scheduled upon
        pending_jobs: a list of pending jobs
    """

    def determine_actions(self, system:sim_sys.SimulatedSystem, pending_jobs:list[Job])->list:
        actions:list = []

        delta:int = system.get_startup_time()
        E:int = int(4*delta/self.epsilon)
        time:int = system.get_time()

        if time % E != 0:
            actions.append([Action.WAIT, E - time%E])

        return actions