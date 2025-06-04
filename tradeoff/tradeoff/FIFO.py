import tradeoff.simulated_system as sim_sys
from job import Job
from tradeoff.action import Action
from tradeoff.container import Container
import typing

"""
FIFO algorithm
"""
class FIFO:
    """
    Constructor
    """
    def __init__(self, params:list):
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
        actions:list[Action] = []

        sorted_jobs:list[Job] = sorted(pending_jobs, key=lambda x: x.get_receival_time())
        containers:list[Container] = list(system.get_containers())

        container_job_assignment: typing.Dict[Container, list[Job]] = {}
        container_assigned_time: typing.Dict[Container, int] = {}
        for job in sorted_jobs:
            best_container = containers[0]
            best_time = containers[0].time_until_done() + container_assigned_time.get(containers[0])
            for container in containers:
                if container.time_until_done() + container_assigned_time.get(container) < best_time:
                    best_time = container_assigned_time.get(container)
                    best_container = container
            container_job_assignment.get(best_container).append(job)
            container_assigned_time[best_container] += job.get_execution_time()

        return actions