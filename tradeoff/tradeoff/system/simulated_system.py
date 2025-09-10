import typing

from tradeoff.system.container import Container
from tradeoff.system.job import Job
from tradeoff.system.action import Action

"""
System with the following properties:
    cost = total units of time that containers are alive for
    execution time of jobs is uncorrelated across containers
    serial computation
"""
class SimulatedSystem:
    """
    Constructor, initializes a simulated system with no containers

    Args
        startup_duration: time required to startup for a job
        curr_time: time the system starts at
    """
    def __init__(self, startup_duration:int, curr_time:int = 0):
        self.containers:set[Container] = set()
        self.time:int = curr_time
        self.startup_time:int = startup_duration
        self.accrued_cost:int = 0
        self.assigned_jobs:set[Job] = set()

    """
    Performs the provided actions on the system
    
    Args:
        actions: the actions to be performed
    """
    def perform_actions(self, actions:list[Action]):
        for action in actions:
            action_type:int = action.get_action_type()
            if action_type == Action.ACTIVATE_CONTAINER:
                self.activate_container(initial_jobs=action.get_jobs(), other_information=action.get_all_other_information())
            elif action_type == Action.TERMINATE_CONTAINER:
                self.terminate_container(action.get_container())
            elif action_type == Action.ADD_JOBS:
                self.assign_jobs(action.get_jobs(), action.get_container())
            elif action_type == Action.REMOVE_JOBS:
                self.remove_jobs(action.get_jobs(), action.get_container())
            elif action_type == Action.REORDER_JOBS:
                self.reorder_jobs(action.get_jobs(), action.get_container())

    """
    Returns the set of containers in the system
    
    Returns:
        The container set
    """
    def get_containers(self)->set[Container]:
        return set(self.containers)

    """
    Returns the system time
    
    Returns:
        The system time
    """
    def get_time(self)->int:
        return self.time

    """
    Adds a new container to the system
    """
    def activate_container(self, initial_jobs:list[Job], other_information:typing.Dict[int, str]=None):
        self.assigned_jobs.update(initial_jobs)
        if other_information is None:
            other_information:typing.Dict[int, str] = {}
        self.containers.add(Container(curr_time=self.time, startup_time=self.startup_time, initial_jobs=initial_jobs, other_information=other_information))

    """
    Removes a container from the system

    Args:
        container: the container to remove
    """
    def terminate_container(self, container:Container):
        self.accrued_cost += container.get_time_alive()
        self.containers.remove(container)

    """
    Assigns the given jobs to the given container

    Args:
        jobs: the jobs to be added
        container: the container being added to
    """
    def assign_jobs(self, jobs:list[Job], container:Container):
        self.assigned_jobs.update(jobs)
        for job in jobs:
            container.add_job(job)

    """
    Removes jobs from a container

    Args:
        jobs: the jobs to be removed
        container: the container being removed from
    """
    def remove_jobs(self, jobs:list[Job], container:Container):
        for job in jobs:
            container.remove_job(job)

    """
    Reorders the jobs to the new order on a container

    Args:
        new_job_order: the jobs in a new order
        container: the container being reordered
    """
    def reorder_jobs(self, new_job_order:list[Job], container:Container):
        container.new_job_order(new_job_order)

    """
    Returns the jobs that have been assigned to containers in the system
    """
    def get_assigned_jobs(self):
        return self.assigned_jobs

    """
    Run the system until the provided time

    Args:
        time: time to run until
    """
    def run(self, time:int):
        for container in self.containers:
            container.run(time)
        self.time = time

    """
    Returns the cost incurred by the system so far
    
    Returns:
        The cost incurred by the system so far
    """
    def get_cost(self)->int:
        cost = self.accrued_cost
        for container in self.containers:
            cost += container.get_time_alive()
        return cost
    
    """
    Sets the cost to 0
    """
    def reset_cost(self):
        self.accrued_cost = 0

    """
    Resets the system
    
    Args:
        curr_time: the time the system is set to
    """
    def reset(self, curr_time=0):
        self.containers = set()
        self.time = curr_time
        self.accrued_cost = 0

    """
    Gets the time until all containers are finished all work
    
    Returns:
        The time until all container are done
    """
    def get_time_until_done(self)->int:
        max_time:int = 0
        for container in self.containers:
            max_time = max(max_time, container.time_until_done())
        return max_time

    """
    Checks if all work is completed
    
    Returns:
        True if all work completed, False otherwise
    """
    def is_done(self)->bool:
        for container in self.containers:
            if not container.is_done():
                return False
        return True

    """
    Returns the startup time of a container
    
    :returns container startup time
    """
    def get_startup_time(self)->int:
        return self.startup_time