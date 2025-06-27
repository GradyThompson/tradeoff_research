import typing
from simulated_system import SimulatedSystem
from job import Job
from action import Action
from container import Container

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

        time_until_next_action: int = terminate_old_containers(system, actions)
        if next_deadline != -1:
            time_until_next_action = min(time_until_next_action, next_deadline)

        if time_until_next_action != -1:
            actions.append(Action(action_type=Action.WAIT, time=time+time_until_next_action))

        return actions

"""
Terminates the containers that have no work left to do and returns the time of the next container shutdown if no 
further updates to the system

Args:
    system: the system that runs the jobs
    actions: the list of actions that are going to be performed on the system
    
Returns:
    Time until the next container needs to be shutdown without further updates to the system
"""
def terminate_old_containers(system:SimulatedSystem, actions:list[Action])->int:
    next_time:int = -1
    existing_container_time_to_complete:typing.Dict[Container, int] = {}
    for container in system.get_containers():
        existing_container_time_to_complete[container] = container.time_until_done()

    for action in actions:
        if action.get_action_type() == Action.ACTIVATE_CONTAINER:
            new_time_to_complete = system.get_startup_time() + sum([job.get_execution_time() for job in action.get_jobs()])
            if new_time_to_complete < next_time or next_time == -1:
                next_time = new_time_to_complete

        if action.get_action_type() == Action.ADD_JOBS:
            existing_container_time_to_complete[action.get_container()] += sum([job.get_execution_time() for job in action.get_jobs()])

    existing_next_time:int = -1
    for container in system.get_containers():
        remaining_time:int = existing_container_time_to_complete.get(container)
        if remaining_time <= 0:
            actions.append(Action(Action.TERMINATE_CONTAINER, container=container))
        elif existing_next_time == -1 or remaining_time < existing_next_time:
            existing_next_time = remaining_time

    if existing_next_time != -1 and (existing_next_time < next_time or next_time == -1):
        next_time = existing_next_time

    return next_time