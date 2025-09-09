from env_RL_wrapper import SystemWrapper
from stable_baselines3 import PPO
from system.controller import Controller

training = False

reward_ratio = 10
jobs_file = "job_sets\\rl_train_js1.txt"
startup_duration = 1
max_containers = 500

model_name = "rl_test_rr" + str(round(reward_ratio, 3)) +  "_max" + str(max_containers)
model_file = "model_data\\" + model_name

env = SystemWrapper(startup_duration=startup_duration, jobs_file=jobs_file, max_containers=max_containers, reward_cost_ratio=reward_ratio,
                    complex_job_config_file_name="job_config\\rl_train_continuous_js1.txt")

module_name = "schedulers.RL"
class_name = "RL"
model_config = ",".join([module_name, class_name, model_file, str(max_containers)])

job_set = "js1"

model_config_folder = "model_config\\"
job_set_folder = "job_sets\\"
results_folder = "result_data\\"

model_config_file = model_config_folder + model_name + ".txt"
jobs_file = job_set_folder + job_set + ".txt"
results_file = results_folder + model_name + "_" + job_set + ".txt"

if training:
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=300000)
    model.save(model_file)

    with open(model_config_file, "w") as f:
        f.write(model_config)
else:
    controller = Controller(startup_duration=startup_duration, model_config_file=model_config_file, jobs_file=jobs_file, results_file=results_file)
    controller.control_loop()