import job

"""
Container class, that models a machine/container in the system, that can run jobs sequentially

Internal variables
jobs - [Job] - a list of the jobs waiting to be executed
curr_time - int - the time the container is at
start_time - int - the time the container started
job_progress - int - time already spent on current job
"""
class Container:
    """
    Instantiate a container

    inputs
    curr_time - the time at the creation of the container
    other_information - additional information that might be needed
    """
    def __init__(self, curr_time, other_information):
        self.jobs = []
        self.curr_time = curr_time
        self.start_time = curr_time
        self.job_progress = 0
        self.other_information = other_information

    """
    Add a job to the container's job queue

    input
    job - Job - the job being added
    """
    def add_job(self, job):
        self.jobs.append(job)

    """
    Removes a job, if the job is the current job, progress is reset

    Input
    job - Job - the job being removed
    """
    def remove_job(self, job):
        if len(self.jobs) >= 1 and self.jobs[0] == job:
            self.job_progress = 0
        self.jobs.remove(job)

    """
    Reorders the jobs, resets progress if the current job changes

    Input
    new_job_order - List[Job] - a list of jobs in the new order
    """
    def new_job_order(self, new_job_order):
        if ((len(self.jobs) >= 1 and len(new_job_order) >= 1 and self.jobs[0] != new_job_order[0]) or
                len(new_job_order) == 0):
            self.job_progress = 0

    """
    Run the container/machine until the provided time

    input
    time - int - the time to run the container until
    """
    def run(self, time):
        time_delta = time - self.curr_time
        while len(self.jobs) > 0 and self.jobs[0].get_execution_time() - self.job_progress <= time_delta:
            finished_job = self.jobs.pop(0)
            self.curr_time += finished_job.get_execution_time() - self.job_progress
            finished_job.complete(self.curr_time)
            self.job_progress = 0

        #Update job progress of unfinished job
        if len(self.jobs) >= 1:
            self.job_progress = time - self.curr_time

        self.curr_time = time

    """
    Returns the time until all jobs in the queue are completed
    """
    def time_until_done(self):
        time_until_done = 0
        for job in self.jobs:
            time_until_done += job.get_execution_time()
        time_until_done -= self.job_progress
        return time_until_done

    """
    Returns the time until done given a different information model
    """
    def time_until_done_other(self, other_metric):
        time_until_done = 0
        for job in self.jobs:
            time_until_done += job.get_other_info(other_metric)
        time_until_done -= self.job_progress
        return time_until_done

    """
    Completes all jobs assigned to container
    """
    def finish(self):
        self.run(self.curr_time + self.time_until_done())
    
    """
    Checks if all work is done
    """
    def is_done(self):
        return self.time_until_done() == 0

    """
    Returns the time that the container has been alive
    """
    def get_time_alive(self):
        return self.curr_time - self.start_time

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