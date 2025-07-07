import gymnasium
from gymnasium import spaces
from gymnasium.core import Env
import numpy as np
import typing
from controller import Controller
from simulated_system import SimulatedSystem
from job import Job

class MyCustomEnv(Env):
    state: np.ndarray
    steps: int
    controller: Controller

    """
    Constructor for the RL model
    
    Args:
        config_file_name: name of the file containing the system config information
    """
    def __init__(self, config_file_name: str):
        super().__init__()
        self.steps = 0
        self.controller = Controller(config_file_name=config_file_name)

    """
    Generates the state for the RL model given the system and queued jobs
    """

    def generate_state(self, system:SimulatedSystem, jobs:list[Job])->np.ndarray:
        state: np.ndarray = np.ndarray([])
        return state

    """
    Resets the RL system
    
    Args:
        seed: the seed to generate the new system
        options: additional options for the new system
        
    Returns:
        Initial state of the system
        Additional information associated with the initial system
    """
    def reset(self, *, seed: int | None = None, options: dict | None = None) -> typing.Tuple[np.ndarray, typing.Dict[
        str, typing.Any]]:
        system: SimulatedSystem
        jobs: list[Job]

        super().reset(seed=seed)
        system, jobs = self.controller.reset()
        self.steps = 0
        self.state = self.generate_state(system, jobs)
        return self.state, {}

    """
    Generates the reward of the action given the initial state and the next state
    """
    def get_reward(self, prev_system:SimulatedSystem, new_system:SimulatedSystem):
        pass

    """
    Goes to the next step of the simulation
    
    Args:
        action: the next action to be performed on the system
        
    Returns:
        The state of the system after the action
        The reward received after the action
        Bool tracking if the system is done
        Other information associated with the system
    """
    def step(self, action: int) -> typing.Tuple[np.ndarray, float, bool, typing.Dict[str, typing.Any]]:
        reward = 0
        done = True
        self.steps += 1
        return self.state, reward, done, {} #TODO

    """
    Creates a human readable version of the system
    
    Args:
        mode: the mode of display (only option is human currently)
    """
    def render(self, mode: str = 'human'):
        pass #TODO

    """
    Closes the system
    """
    def close(self):
        pass #TODO