from tradeoff.system.simulated_system import SimulatedSystem
from tradeoff.system.job import Job
from tradeoff.system.action import Action
from stable_baselines3 import PPO
from tradeoff.util.env_RL_wrapper import SystemWrapper
import numpy as np

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
        self.max_containers = int(params[1])
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
        obs:np.ndarray = SystemWrapper.generate_observation(jobs=pending_jobs, system=system)
        action, _ = self.model.predict(observation=obs, deterministic=True)
        target_num_containers = SystemWrapper.rescale_action(action, self.max_containers)
        actions:list[Action] = SystemWrapper.determine_actions(jobs=pending_jobs, system=system,
                                                               target_num_containers=target_num_containers)
        return actions