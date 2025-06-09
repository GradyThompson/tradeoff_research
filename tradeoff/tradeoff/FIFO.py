import simulated_system as sim_sys
from job import Job
from action import Action
from container import Container
import typing

"""
FIFO algorithm
"""
class FIFO:
    """
    Constructor

    Args:
        params a list of parameters (length 1) 1. number of containers
    """
    def __init__(self, params:list):
        self.num_containers:int = int(params[0])

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

        existing_containers:list[Container] = list(system.get_containers())
        existing_container_job_assignment:typing.Dict[Container, list[Job]] = {}
        existing_container_assigned_time:typing.Dict[Container, int] = {}
        for container in existing_containers:
            existing_container_job_assignment[container] = []
            existing_container_assigned_time[container] = 0

        new_container_job_assignment:typing.Dict[int, list[Job]] = {}
        new_container_assigned_time: typing.Dict[int, int] = {}
        for container in range(max(self.num_containers - len(existing_containers), 0)):
            new_container_job_assignment[container] = []
            new_container_assigned_time[container] = 0

        for job in sorted_jobs:
            best_existing_container:Container = None
            best_existing_time:int = -1

            for container in existing_containers:
                if (best_existing_time == -1 or
                        container.time_until_done() + existing_container_assigned_time.get(container) < best_existing_time):
                    best_existing_time = existing_container_assigned_time.get(container)
                    best_existing_container = container

            best_new_container:int = -1
            best_new_time:int = -1

            for container in new_container_job_assignment.keys():
                if best_new_time == -1 or new_container_assigned_time.get(container) < best_new_time:
                    best_new_time = new_container_assigned_time.get(container)
                    best_new_container = container

            if ((best_existing_time != -1 and best_existing_time <= best_new_time)
                    or best_new_time == -1):
                existing_container_job_assignment.get(best_existing_container).append(job)
                existing_container_assigned_time[best_existing_container] += job.get_execution_time()
            else:
                new_container_job_assignment.get(best_new_container).append(job)
                new_container_assigned_time[best_new_container] += job.get_execution_time()

        for container in existing_container_job_assignment.keys():
            jobs:list[Job] = existing_container_job_assignment.get(container)
            if len(jobs) >= 1:
                actions.append(Action(action_type=Action.ADD_JOBS, container=container, jobs=jobs))

        for container in new_container_job_assignment.keys():
            jobs:list[Job] = new_container_job_assignment.get(container)
            if len(jobs) >= 1:
                actions.append(Action(action_type=Action.ACTIVATE_CONTAINER, jobs=jobs))

        return actions