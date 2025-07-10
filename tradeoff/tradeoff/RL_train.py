from env_RL_wrapper import SystemWrapper
from stable_baselines3 import PPO

"""
Trains the RL model on the provided configuration, infinitely generates jobs to present the model with

Args:
    config_file: name of the file containing the config information

Config (line separated):
    output_file
"""
config_file = "config\\rl_train_js1.txt"
env = SystemWrapper(config_file_name=config_file, max_containers=100, reward_ratio=10)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)