import typing
from system.simulated_system import SimulatedSystem
from system.action import Action
from system.container import Container

"""
Terminates the containers that have no work left to do and returns the time of the next container shutdown if no 
further updates to the system

Args:
    system: the system that runs the jobs
    actions: the list of actions that are going to be performed on the system

Returns:
    Time until the next container needs to be shutdown without further updates to the system
"""


def terminate_stale_containers(system: SimulatedSystem, actions: list[Action]) -> int:
    next_time: int = -1
    existing_container_time_to_complete: typing.Dict[Container, int] = {}
    for container in system.get_containers():
        existing_container_time_to_complete[container] = container.time_until_done()

    for action in actions:
        if action.get_action_type() == Action.ACTIVATE_CONTAINER:
            new_time_to_complete = system.get_startup_time() + sum(
                [job.get_execution_time() for job in action.get_jobs()])
            if new_time_to_complete < next_time or next_time == -1:
                next_time = new_time_to_complete

        if action.get_action_type() == Action.ADD_JOBS:
            existing_container_time_to_complete[action.get_container()] += sum(
                [job.get_execution_time() for job in action.get_jobs()])

    existing_next_time: int = -1
    for container in system.get_containers():
        remaining_time: int = existing_container_time_to_complete.get(container)
        if remaining_time <= 0:
            actions.append(Action(Action.TERMINATE_CONTAINER, container=container))
        elif existing_next_time == -1 or remaining_time < existing_next_time:
            existing_next_time = remaining_time

    if existing_next_time != -1 and (existing_next_time < next_time or next_time == -1):
        next_time = existing_next_time

    return next_time