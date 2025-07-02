import typing

from job import Job
from container import Container

"""
Class containing action information

Type of action - parameters - description
activate_container - None - creates a new container
terminate_container - container - terminates the provided container
add_jobs - container, jobs - adds jobs to the provided container
remove_jobs - container, jobs - removes the provided jobs from the provided container
reorder_jobs - container, jobs - changes the order of jobs in the provided container
wait - time - scheduler requests to reevaluate after time
"""
class Action:
    ACTIVATE_CONTAINER = 1
    TERMINATE_CONTAINER = 2
    ADD_JOBS = 3
    REMOVE_JOBS = 4
    REORDER_JOBS = 5
    WAIT = 20

    """
    Action constructor

    Args:
        action_type: type of action
        container: container being acted upon
        jobs: Jobs being acted upon
    """
    def __init__(self, action_type:int, container:Container=None, jobs:list[Job]=None, time:int=0, other_information:typing.Dict[int, str]=None):
        self.action_type:int = action_type
        self.container:Container = container
        self.time:int = time
        if jobs is None:
            jobs:list[Job] = []
        self.jobs:list[Job] = jobs
        if other_information is None:
            other_information:typing.Dict[int, str] = {}
        self.other_information:typing.Dict[int, str] = other_information

    """
    Return the type of action being performed
    
    Returns:
        The action type
    """
    def get_action_type(self)->int:
        return self.action_type
    
    """
    Return the container the action is performed on
    
    Returns:
        The container
    """
    def get_container(self)->Container:
        return self.container
    
    """
    Returns the jobs the action is performed on
    
    Returns:
        The list of jobs
    """
    def get_jobs(self)->list[Job]:
        return self.jobs

    """
    Returns the time associated with the action

    Returns:
        The time
    """

    def get_time(self)->int:
        return self.time

    """
    Adds additional information
    
    Args:
        key: the key of the information
        value: the information
    """
    def add_other_information(self, key:int, value:str):
        self.other_information[key] = value

    """
    Returns other information
    
    Args:
        key: the key of the information
        
    Returns:
        The information associated with the key
    """
    def get_other_information(self, key:int)->str:
        return self.other_information.get(key)

    """
    Returns all other information
    
    Returns:
        The other information table
    """
    def get_all_other_information(self):
        return self.other_information