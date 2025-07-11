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
model_file = "model_data\\rl_max100"

env = SystemWrapper(config_file_name=config_file, max_containers=100)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=200000)
model.save(model_file)