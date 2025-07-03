import gymnasium
from gymnasium import spaces
from gymnasium.core import Env
import numpy as np
from typing import Tuple, Dict, Any

class MyCustomEnv(Env):
    state: np.ndarray

    def __init__(self):
        pass #TODO

    def reset(self, *, seed: int | None = None, options: dict | None = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        return self.state, {} #TODO

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict[str, Any]]:
        reward = 0
        done = True
        return self.state, reward, done, {} #TODO

    def render(self, mode: str = 'human'):
        pass #TODO

    def close(self):
        pass #TODO