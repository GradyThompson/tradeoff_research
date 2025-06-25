from job import Job
import typing

"""
Container class, that models a machine/container in the system, that can run jobs sequentially
"""
class Container:
    JOB_EPOCH = 1

    """
    Instantiate a container

    Args:
        curr_time: the time at the creation of the container
        other_information: additional information that might be needed
    """
    def __init__(self, curr_time:int, initial_jobs:list[Job] = None, other_information:typing.Dict[int, str]=None):
        if initial_jobs is None:
            self.jobs:list[Job] = []
        else:
            self.jobs:list[Job] = initial_jobs
        self.curr_time:int = curr_time
        self.start_time:int = curr_time
        self.job_progress:int = 0
        if other_information is None:
            self.other_information:typing.Dict[int, str] = {}
        else:
            self.other_information:typing.Dict[int, str] = other_information

    """
    Add a job to the container's job queue

    Args:
        job: the job being added
    """
    def add_job(self, job:Job):
        self.jobs.append(job)

    """
    Removes a job, if the job is the current job, progress is reset

    Args:
        job: the job being removed
    """
    def remove_job(self, job:Job):
        if len(self.jobs) >= 1 and self.jobs[0] == job:
            self.job_progress = 0
        self.jobs.remove(job)

    """
    Reorders the jobs, resets progress if the current job changes

    Args:
        new_job_order: a list of jobs in the new order
    """
    def new_job_order(self, new_job_order:list[Job]):
        if ((len(self.jobs) >= 1 and len(new_job_order) >= 1 and self.jobs[0] != new_job_order[0]) or
                len(new_job_order) == 0):
            self.job_progress = 0
        self.jobs = list(new_job_order)

    """
    Run the container/machine until the provided time

    Args
        time: the time to run the container until
    """
    def run(self, time:int):
        while len(self.jobs) > 0 and self.curr_time + self.jobs[0].get_execution_time() - self.job_progress <= time:
            finished_job:Job = self.jobs.pop(0)
            self.curr_time += finished_job.get_execution_time() - self.job_progress
            finished_job.complete(self.curr_time)
            self.job_progress = 0

        if len(self.jobs) >= 1:
            self.job_progress = time - self.curr_time
        self.curr_time = time

    """
    Returns the time until all jobs in the queue are completed
    
    Returns:
        The time until completion
    """
    def time_until_done(self)->int:
        time_until_done:int = 0
        for job in self.jobs:
            time_until_done += job.get_execution_time()
        time_until_done -= self.job_progress
        return time_until_done

    """
    Returns the time until done given a different information model
    
    Args:
        other_metric: The other time metric that is used to determine time until completion (exp. 
        Job.EXECUTION_TIME_UPPER_BOUND)
        
    Returns:
        The time until completion under the different metric
    """
    def time_until_done_other(self, other_metric:int):
        time_until_done:int = 0
        for job in self.jobs:
            time_until_done += int(job.get_other_info(other_metric))
        time_until_done -= self.job_progress
        return time_until_done

    """
    Completes all jobs assigned to container
    """
    def finish(self):
        self.run(self.curr_time + self.time_until_done())
    
    """
    Checks if all work is done
    
    Returns:
        True if computation is done and false otherwise
    """
    def is_done(self)->bool:
        return self.time_until_done() == 0

    """
    Returns the time that the container has been alive
    
    Returns:
        The time the container has been alive
    """
    def get_time_alive(self)->int:
        return self.curr_time - self.start_time

    """
    Adds additional information
    
    Args:
        key: the key of the other information
        value: the value of the other information
    """
    def add_other_information(self, key:int, value:str):
        self.other_information[key] = value

    """
    Returns other information
    
    Args:
        key: the key of the other information
        
    Returns:
        The value of the other information
    """
    def get_other_information(self, key:int)->str:
        return self.other_information.get(key)