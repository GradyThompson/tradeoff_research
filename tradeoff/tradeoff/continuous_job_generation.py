from job import Job
import job_manager
import random

"""
Class that can be used to generate a continuous stream of jobs
"""
class ContinuousJobGeneration:
    """
    Constructor

    Args:
        config_file_name: name of the file containing the config data

    config_file:
        <execution time distributions>
        <min num jobs in batch>,<max num jobs in batch>,<min job release range>,<max job release range>,"max_bound_size"

    execution time distributions:
        ; (semicolon) separated
        <distribution_name>,<min parameters comma separated>,<max parameters comma separated>
    """
    def __init__(self, config_file_name:str):
        self.id_count = 0
        with open(config_file_name) as config_file:
            file_lines: list[str] = [line.strip() for line in config_file.readlines()]

            self.exec_time_dists = []
            exec_time_dists:list[str] = file_lines[0].split(";")
            for exec_time_dist in exec_time_dists:
                exec_name = exec_time_dist.split(",")[0]
                params = []

                params_input = exec_time_dist.split(",")[1:]
                param_num = 0
                while param_num < len(params_input)//2:
                    params.append([int(params_input[param_num]), int(params_input[param_num+1])])
                    param_num += 2

                self.exec_time_dists.append([exec_name, params])

            job_info:list[str] = file_lines[1].split(",")
            self.min_num_jobs = int(job_info[0])
            self.max_num_jobs = int(job_info[1])
            self.min_release_range = int(job_info[2])
            self.max_release_range = int(job_info[3])
            self.max_bound_size = int(job_info[4])

    """
    Returns a list of jobs generated using the stored config information, with the release times of the jobs starting
    at the given time.
    
    Args:
        time: the time when jobs start releasing
        
    Returns:
        List of generated jobs
    """
    def generate_bounded_jobs(self, time: int)->list[Job]:
        jobs:list[Job]

        num_jobs:int = random.randint(self.min_num_jobs, self.max_num_jobs)
        id_prefix:str = str(self.id_count)
        end_time:int = time + random.randint(self.min_release_range, self.max_release_range)

        dist = random.choice(self.exec_time_dists)
        dist_name:str = dist[0]
        dist_param_bounds = dist[1]
        dist_params:list[float] = []
        min_to_max_offset = len(dist_param_bounds)//2
        dist_param_ind = 0
        while dist_param_ind < dist_param_bounds:
            param_min = dist_param_bounds[dist_param_ind]
            param_max = dist_param_bounds[dist_param_ind + min_to_max_offset]
            dist_params.append(random.uniform(param_min, param_max))

        jobs = job_manager.generate_bounded_jobs(num_jobs=num_jobs, id_prefix=id_prefix, start_time=time,
                                                           end_time=end_time, dist_name=dist_name,
                                                           dist_params=dist_params, max_bound_size=self.max_bound_size)
        self.id_count += 1
        return jobs