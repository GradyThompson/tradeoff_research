import gymnasium
from gymnasium import spaces
from gymnasium.core import Env
import numpy as np
import numpy.typing as npt
import typing
from controller import Controller
from simulated_system import SimulatedSystem
from job import Job
from model import Model
from container import Container

class MyCustomEnv(Env):
    """
    Constructor for the RL model
    
    Args:
        config_file_name: name of the file containing the system config information
        max_containers: maximum number of containers
        max_steps: the max steps the RL model will go for
    """
    def __init__(self, config_file_name: str, max_containers: int, max_steps: int, reward_ratio: float):
        super().__init__()

        self.action_space:spaces.Box = spaces.Discrete(max_containers)
        self.observation_space:spaces.Box = spaces.Box(low=-np.inf, high=np.inf, shape=(20,), dtype=np.float32)

        self.steps:int = 0
        self.max_steps:int = max_steps

        system, model, jobs, result_file_name = Controller.parse_config(config_file_name=config_file_name)
        self.controller: Controller = Controller(system=system, model=model, jobs=jobs, results_file_name=result_file_name)

        self.reward_ratio:float = reward_ratio
    """
    Generates the state for the RL model given the system and queued jobs
    
    Args:
        queued_jobs: jobs that are currently queued
        system: the system being scheduled on
        
    Returns:
        The state
        
    State (ndarray of floats): see Models/RL/parameters in README
    """
    def generate_observation(self)->npt.NDArray[np.float32]:
        jobs:list[Job] = self.controller.get_queued_jobs()
        job_receival_time:list[int] = [job.get_receival_time() for job in jobs]
        upper_job_execution_time:list[int] = [int(job.get_other_info(Job.EXECUTION_TIME_UPPER_BOUND)) for job in jobs]
        lower_job_execution_time: list[int] = [int(job.get_other_info(Job.EXECUTION_TIME_LOWER_BOUND)) for job in jobs]

        system:SimulatedSystem = self.controller.get_system()
        containers:set[Container] = system.get_containers()
        upper_container_completion_times: list[int] = \
            [container.time_until_done_other(Job.EXECUTION_TIME_UPPER_BOUND)
             for container in containers]
        lower_container_completion_times:list[int] = \
            [container.time_until_done_other(Job.EXECUTION_TIME_LOWER_BOUND)
             for container in containers]

        obs = np.ndarray([], dtype=np.float32)
        np.append(obs, len(system.get_containers())) # num containers
        np.append(obs, len(jobs))  # num queued jobs
        np.append(obs, min(upper_container_completion_times))  # U next container completion time
        np.append(obs, min(lower_container_completion_times))  # L next container completion time
        np.append(obs, np.average(upper_container_completion_times))  # U average container completion time
        np.append(obs, np.average(lower_container_completion_times))  # L average container completion time
        np.append(obs, max(upper_container_completion_times))  # U last container completion time
        np.append(obs, max(lower_container_completion_times))  # L last container completion time
        np.append(obs, min(job_receival_time))  # earliest queued job receival time
        np.append(obs, np.average(job_receival_time))  # average queued job receival time
        np.append(obs, max(job_receival_time))  # latest queued job receival time
        np.append(obs, sum(upper_job_execution_time))  # U queued job volume
        np.append(obs, sum(lower_job_execution_time))  # L queued job volume
        np.append(obs, min(upper_job_execution_time))  # U min queued job execution time
        np.append(obs, min(lower_job_execution_time))  # L min queued job execution time
        np.append(obs, max(upper_job_execution_time))  # U max queued job execution time
        np.append(obs, max(lower_job_execution_time))  # L max queued job execution time
        np.append(obs, int(jobs[0].get_other_info(Job.EXECUTION_TIME_UPPER_BOUND)))  # U earliest queued job execution time
        np.append(obs, int(jobs[0].get_other_info(Job.EXECUTION_TIME_LOWER_BOUND)))  # L earliest queued job execution time
        np.append(obs, system.get_startup_time())  # new container startup time

        return obs

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
        super().reset(seed=seed)
        self.controller.reset()
        self.steps = 0
        obs = self.generate_observation()
        return obs, {}

    """
    Generates the reward of the action given the initial state and the next state
    """
    def get_reward(self)->float:
        system:SimulatedSystem = self.controller.get_system()
        containers:set[Container] = system.get_containers()
        container_count:int = len(containers)
        max_job_delay = -1
        for container in containers:
            jobs = container.get_jobs()
            for job in jobs:
                job_queue_time = container.time_when_job_run(job) - job.get_receival_time()
                if job_queue_time > max_job_delay or max_job_delay == -1:
                    max_job_delay = job_queue_time
        if max_job_delay != -1:
            reward:float = -container_count - self.reward_ratio * max_job_delay
        else:
            reward:float = -container_count
        return reward

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
        self.steps += 1
        obs = self.generate_observation()
        reward = self.get_reward()
        done = self.controller.is_done()
        return obs, reward, done, {}

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