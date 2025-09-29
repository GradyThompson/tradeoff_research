import argparse
from tradeoff.system.controller import Controller

parser = argparse.ArgumentParser()
parser.add_argument("model_name", help="Name of model (<config folder>\\<model_name>.txt")
parser.add_argument("job_set", help="Name of job set (<job set folder>\\<job_set>.txt")
parser.add_argument("startup_time", help="Startup time of the system")
args = parser.parse_args()

startup_time = int(args.startup_time)
model_name = args.model_name
job_set = args.job_set

model_config_folder = "model_config\\"
job_set_folder = "job_sets\\"
results_folder = "result_data\\"

model_config_file = model_config_folder + model_name + ".txt"
jobs_file = job_set_folder + job_set + ".txt"
results_file = results_folder + model_name + "_" + job_set + ".txt"

controller = Controller(startup_duration=startup_time, model_config_file=model_config_file, jobs_file=jobs_file, results_file=results_file)
controller.control_loop()