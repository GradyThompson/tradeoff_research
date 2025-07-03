import typing

from simulated_system import SimulatedSystem
from job import Job
from action import Action
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

"""
RL Algorithm
"""
class RL:
    """
    Constructor, saves epsilon to a class variable

    Args:
        params a list of parameters (comma separated) - length 1
            model - model to be loaded using stable baselines
    """

    def __init__(self, params: list):
        model_name = params[0]
        self.model = PPO.load(model_name)

    """
    Wrapper for model output to be used by the simulated system

    Args:
        system: The system being scheduled upon
        pending_jobs: a list of pending jobs

    Return:
        A list of actions to be performed on the system
    """

    def determine_actions(self, system: SimulatedSystem, pending_jobs: list[Job]) -> list[Action]:
        actions:list[Action] = []
        return actions