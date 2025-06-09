from scipy.stats import poisson, expon, skewnorm
import numpy as np
from job import Job
import typing

"""
Generate a list jobs using meta data from a file, currently does not add deadlines

Args:
    job_meta_data_file_name: The name of the file that contains the meta data
    id_prefix: prefix to the job id
    
Returns:
    returns a list of generated jobs

File:
    Each line is different set of jobs:
    <num_jobs>,<start_time>,<end_time>,<execution time distribution>,<execution time distribution parameters comma seperated>
    start_time, end_time - jobs are received uniformly in this time

Execution time distribution:
    poisson - location,rate
    exponential - location,scale
    skew_normal - location,scale,shape
"""
def generate_jobs(job_meta_data_file_name:str, id_prefix:str="")->list[Job]:
    file:typing.TextIO = open(job_meta_data_file_name, "r")
    jobs:list[Job] = []
    id_suffix:int = 1
    for line in file:
        split_line:list[str] = line.split(",")
        num_jobs:int = int(split_line[0])
        start_time:int = int(split_line[1])
        end_time:int = int(split_line[2])
        distribution_name:str = split_line[3]
        params:list[float] = [float(i) for i in split_line[4:]]

        execution_times:list[int] = []

        #Create distribution, called as distribution(num_samples), generates integer list of vals
        if distribution_name == "poisson":
            loc:float = params[0]
            mu:float = params[1]
            execution_times = [int(round(i)) for i in np.atleast_1d(poisson.rvs(mu=mu, loc=loc, size=num_jobs))]
        elif distribution_name == "exponential":
            loc:float = params[0]
            scale:float = params[1]
            execution_times = [int(round(i)) for i in np.atleast_1d(expon.rvs(loc=loc,scale=scale,size=num_jobs))]
        elif distribution_name == "skew_normal":
            loc = params[0]
            scale = params[1]
            a = params[2]
            execution_times = [int(round(i)) for i in np.atleast_1d(skewnorm.rvs(loc=loc,scale=scale,a=a,size=num_jobs))]
        else:
            raise ValueError('Metadata file did not specify a valid distribution name: ' + distribution_name)

        receival_times:list[int] = list(np.random.randint(low=start_time, high=end_time+1, size=num_jobs))

        #Generate jobs
        for job_num in range(num_jobs):
            job_id:str = id_prefix + str(id_suffix)
            execution_time:int = execution_times[job_num]
            receival_time:int = receival_times[job_num]
            jobs.append(Job(id=job_id, execution_time=execution_time, receival_time=receival_time))
            id_suffix += 1
        
    return jobs

"""
Returns a string representation of the job - <id>,<execution_time>,<receival_time>,<deadline>

Args:
    job: the job
"""
def job_to_string(job:Job)->str:
    s = str(job.get_id()) + "," + str(job.get_execution_time()) + "," + str(job.get_receival_time())
    return s
    
"""
Returns a job from a string representation

Args:
    s: string representation
"""
def job_from_string(s:str)->Job:
    split_s:list[str] = s.split(",")
    job_id:str = split_s[0]
    execution_time:int = int(split_s[1])
    receival_time:int = int(split_s[2])
    job = Job(job_id=job_id, execution_time=execution_time, receival_time=receival_time)
    return job

"""
Writes a list of jobs to a file

Args:
    jobs: list of jobs
    file_name: file jobs will be saved to
"""
def jobs_to_file(jobs:list[Job], file_name:str):
    file:typing.TextIO = open(file_name, "w")
    for i, job in enumerate(jobs):
        s:str = job_to_string(job)
        if i != len(jobs)-1:
            file.write(s + "\n")
        else:
            file.write(s)


"""
Loads a list of jobs from a file

Args:
    file_name: the name of the file
"""
def jobs_from_file(file_name:str)->list[Job]:
    jobs:list[Job] = []
    file:typing.TextIO = open(file_name, "r")
    for line in file.readlines():
        job:Job = job_from_string(line)
        jobs.append(job)
    return jobs