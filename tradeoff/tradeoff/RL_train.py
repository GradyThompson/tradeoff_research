from env_RL_wrapper import SystemWrapper
from stable_baselines3 import PPO

"""
Trains the RL model on the provided configuration, infinitely generates jobs to present the model with

Args:
    config_file: name of the file containing the config information
    model_file: where the model will be saved

Config (line separated):
    output_file
"""
config_file = "config\\rl_train_js1.txt"

max_reward_ratio = 5
reward_ratio_increase_factor = 1.5
reward_ratio_granularity = 0.1

reward_ratio = 1.9
while reward_ratio < max_reward_ratio:
    model_file = "model_data\\rl_rr" + str(reward_ratio) +  "_max100"

    env = SystemWrapper(config_file_name=config_file, max_containers=100, reward_cost_ratio=1,
                        complex_job_config_file_name="job_config\\rl_train_continuous_js1.txt")

    model = PPO("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=100000)
    model.save(model_file)

    print("Trained model: ", reward_ratio)

    new_ratio = (reward_ratio_increase_factor*reward_ratio//reward_ratio_granularity)*reward_ratio_granularity
    if abs(new_ratio - reward_ratio) < reward_ratio_granularity:
        reward_ratio += reward_ratio_granularity
    else:
        reward_ratio = new_ratio