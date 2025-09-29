import argparse
from tradeoff.system.controller import Controller
import os

parser = argparse.ArgumentParser()
parser.add_argument("job_set", help="Name of job set (<job set folder>\\<job_set>.txt")
parser.add_argument("startup_time", help="Startup time of the system")
args = parser.parse_args()

startup_time = int(args.startup_time)
job_set = args.job_set

model_config_folder = "model_config"
job_set_folder = "job_sets"
results_folder = "result_data"

model_names = [os.path.splitext(f)[0] for f in os.listdir(model_config_folder) if os.path.isfile(os.path.join(model_config_folder, f))]
for model_name in model_names:
    print("Running", model_name)
    model_config_file = model_config_folder + "/" + model_name + ".txt"
    jobs_file = job_set_folder + "/" + job_set + ".txt"
    results_file = results_folder + "/" + model_name + "_" + job_set + ".txt"

    controller = Controller(startup_duration=startup_time, model_config_file=model_config_file, jobs_file=jobs_file, results_file=results_file)
    controller.control_loop()

    print("Complete")