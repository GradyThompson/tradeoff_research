from job import Job

"""
Class containing action information

Type of action - parameters - description
activate_container - None - creates a new container
terminate_container - container - terminates the provided container
add_jobs - container, jobs - adds jobs to the provided container
remove_jobs - container, jobs - removes the provided jobs from the provided container
reorder_jobs - container, jobs - changes the order of jobs in the provided container
wait - time - with no new information scheduler waits until <time> to perform action
"""
class Action:
    ACTIVATE_CONTAINER = 1
    TERMINATE_CONTAINER = 2
    ADD_JOBS = 3
    REMOVE_JOBS = 4
    REORDER_JOBS = 5
    WAIT = 6

    """
    Action constructor

    Args:
        action_type: - type of action
        container: - container being acted upon
        jobs: - Jobs being acted upon
    """
    def __init__(self, action_type, container=None, jobs=None, time:int=0, other_information=None):
        if jobs is None:
            jobs = []
        self.action_type = action_type
        self.container = container
        self.jobs:list[Job] = jobs
        self.time:int = time
        self.other_information = other_information

    """
    Return the type of action being performed
    
    Returns:
        The action type
    """
    def get_action_type(self):
        return self.action_type
    
    """
    Return the container the action is performed on
    
    Returns:
        The container
    """
    def get_container(self):
        return self.container
    
    """
    Returns the jobs the action is performed on
    
    Returns:
        The list of jobs
    """
    def get_jobs(self):
        return self.jobs

    """
    Returns the time associated with the action

    Returns:
        The time
    """

    def get_time(self):
        return self.time

    """
    Adds additional information
    """
    def add_other_information(self, key, value):
        self.other_information[key] = value

    """
    Returns other information
    """
    def get_other_information(self, key):
        return self.other_information.get(key)
