import incomplete.simulated_system as sim_sys
from job import Job
from tradeoff.incomplete.action import Action

"""
FIFO algorithm
"""


class FIFO:
    """
    Constructor
    """

    def __init__(self):
        pass

    """
    Decides system actions based on the deterministic execution time of jobs

    Args:
        system: The system being scheduled upon
        pending_jobs: a list of pending jobs

    Return:
        A list of actions to be performed on the system
    """

    def determine_actions(self, system: sim_sys.SimulatedSystem, pending_jobs: list[Job]) -> list[Action]:
        actions: list[Action] = []

        return actions