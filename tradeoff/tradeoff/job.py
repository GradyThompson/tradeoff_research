import typing

"""
Job data type, stores all relevant information of a job
"""
class Job:
    #Other information keys
    EXECUTION_TIME_LOWER_BOUND = 1
    EXECUTION_TIME_UPPER_BOUND = 2

    """
    Constructor

    Args:
        id: unique identifier of the job
        execution_time: execution time of the job
        receival_time: the time the job is received
        deadline: time the jobs is due
    """
    def __init__(self, job_id:str, execution_time:int, receival_time:int, deadline:int=-1):
        self.job_id:str = job_id
        self.execution_time:int = execution_time
        self.receival_time:int = receival_time
        self.deadline:int = deadline
        self.completion_time:int = -1
        self.other_info:typing.Dict[int, str] = {}

    """
    Adds additional info to the job

    Args:
        key: the key the additional info can be accessed by
        value: the value stored
    """
    def add_other_info(self, key:int, value:str):
        self.other_info[key] = value

    """
    Gets additional info from the job

    Args:
        key: the key of the additional info
        
    Returns:
        The attached info
    """
    def get_other_info(self, key:int)->str:
        return self.other_info.get(key)

    """
    Gets set of other information
    
    Returns:
        The set of keys of all other information in the job
    """
    def get_all_other_info(self)->set[int]:
        return set(self.other_info.keys())

    """
    Returns the job id
    
    Returns:
        The job ID
    """
    def get_id(self)->str:
        return self.job_id
    
    """
    Returns the execution time
    
    Returns:
        The job execution time
    """
    def get_execution_time(self)->int:
        return self.execution_time
    
    """
    Returns the time that the job is received at
    
    Returns:
        The receival time of the job
    """
    def get_receival_time(self)->int:
        return self.receival_time
    
    """
    Returns the deadline of the job
    
    Returns:
        The job deadline
    """
    def get_deadline(self)->int:
        return self.deadline
    
    """
    Records the completion time

    Args:
        time: time of completion
    """
    def complete(self, time:int):
        self.completion_time = time

    """
    Returns the time the job was queued for
    
    Returns:
        The queue time or -1 if the job is incomplete
    """
    def get_queue_time(self):
        if self.completion_time == -1:
            return -1
        return self.completion_time - self.receival_time

    """
    Define less than to be based on receival time, making jobs sorted by receival time
    
    Args:
        other: the job being compared with
        
    Returns
        True if the receival time of this job is less than that of the other job
    """
    def __lt__(self, other:'Job')->bool:
        return self.receival_time < other.receival_time