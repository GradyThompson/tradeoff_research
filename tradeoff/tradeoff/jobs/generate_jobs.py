import argparse
import tradeoff.jobs.job_manager as job_manager
from tradeoff.system.job import Job

"""
Generates jobs to a specified file
"""
parser = argparse.ArgumentParser()
parser.add_argument("job_config_file", help="Name of config file containing job metadata")
parser.add_argument("jobs_file", help="Name of file where jobs will be saved")
parser.add_argument("--max_bound", help="Maximum bound size for jobs, if not specified than deterministic jobs are generated")
args = parser.parse_args()
config_file = args.job_config_file

if args.max_bound:
    jobs:list[Job] = job_manager.generate_bounded_jobs_from_file(job_meta_data_file_name=config_file,
                                                                 max_bound_size=int(args.max_bound))
else:
    jobs: list[Job] = job_manager.generate_jobs_from_file(job_meta_data_file_name=config_file)

job_manager.jobs_to_file(jobs, args.jobs_file)