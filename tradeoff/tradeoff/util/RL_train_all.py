from env_RL_wrapper import SystemWrapper
from stable_baselines3 import PPO

"""
Trains the RL model on the provided configuration, infinitely generates jobs to present the model with
"""
jobs_file = "job_sets\\rl_train_js1.txt"
startup_duration = 1

max_reward_ratio = 10
reward_ratio_increase_factor = 1.5
reward_ratio_granularity = 0.1
max_containers = 100

reward_ratio = reward_ratio_granularity
while reward_ratio < max_reward_ratio:
    model_name = "rl_rr" + str(round(reward_ratio, 3)) +  "_max100"
    model_file = "model_data\\" + model_name

    env = SystemWrapper(startup_duration=startup_duration, jobs_file=jobs_file, max_containers=max_containers, reward_cost_ratio=1,
                        complex_job_config_file_name="job_config\\rl_train_continuous_js1.txt")

    model = PPO("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=400000)
    model.save(model_file)

    #< model_module_name >, < model_class_name >, < model params(comma separated) >
    module_name = "tradeoff.schedulers.RL"
    class_name = "RL"
    model_config = ",".join([module_name, class_name, model_file, str(max_containers)])

    model_config_file = "model_config\\" + model_name + ".txt"
    with open(model_config_file, "w") as f:
        f.write(model_config)

    print("Trained model: ", reward_ratio)

    new_ratio = (reward_ratio_increase_factor*reward_ratio//reward_ratio_granularity)*reward_ratio_granularity
    if abs(new_ratio - reward_ratio) < reward_ratio_granularity:
        reward_ratio += reward_ratio_granularity
    else:
        reward_ratio = new_ratio