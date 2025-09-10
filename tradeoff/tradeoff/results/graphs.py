import tradeoff.results.result_manager as result_manager
import os

result_data_folder = "result_data"
job_set = "js1"

model_config_folder = "model_config"
job_set_folder = "job_sets"
results_folder = "result_data"

model_data = {}
model_names = [os.path.splitext(f)[0] for f in os.listdir(model_config_folder) if os.path.isfile(os.path.join(model_config_folder, f))]
for model_name in model_names:
    model_data[model_name] = result_data_folder + "/" + model_name + "_" + job_set + ".txt"

result_manager.plot_max_queue_v_cost(model_data)
result_manager.plot_avg_queue_v_cost(model_data)