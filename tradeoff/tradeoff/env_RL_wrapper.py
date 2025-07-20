import gymnasium
from gymnasium import spaces
from gymnasium.core import Env
import numpy as np
import numpy.typing as npt
import typing
from controller import Controller
from simulated_system import SimulatedSystem
from job import Job
from container import Container
from action import Action
import heapq

class SystemWrapper(Env):
    """
    Constructor for the RL model
    
    Args:
        config_file_name: name of the file containing the system config information
        max_containers: maximum number of containers
        reward_cost_ratio: ratio of cost to speed in reward function (higher cost ratio, is higher incentive to lower cost)
    """
    def __init__(self, config_file_name: str, max_containers: int, reward_cost_ratio: float):
        super().__init__()

        self.action_space:spaces.Box = spaces.Box(low=0.0, high=max_containers, shape=(1,), dtype=np.float32)
        self.observation_space:spaces.Box = spaces.Box(low=-np.inf, high=np.inf, shape=(20,), dtype=np.float32)

        self.reward_cost_ratio:float = reward_cost_ratio

        self.controller: Controller = Controller(config_file_name=config_file_name, no_model=True)

    """
    Generates the state for the RL model given the system and queued jobs
    
    Args:
        queued_jobs: jobs that are currently queued
        system: the system being scheduled on
        
    Returns:
        The state
        
    State (ndarray of floats): see Models/RL/parameters in README
    """
    @staticmethod
    def generate_observation(jobs:list[Job], system:SimulatedSystem)->npt.NDArray[np.float32]:
        job_receival_time:list[int] = [job.get_receival_time() for job in jobs]
        upper_job_execution_time:list[int] = [int(job.get_other_info(Job.EXECUTION_TIME_UPPER_BOUND)) for job in jobs]
        lower_job_execution_time: list[int] = [int(job.get_other_info(Job.EXECUTION_TIME_LOWER_BOUND)) for job in jobs]

        containers:set[Container] = system.get_containers()
        upper_container_completion_times: list[int] = \
            [container.time_until_done_other(Job.EXECUTION_TIME_UPPER_BOUND)
             for container in containers]
        lower_container_completion_times:list[int] = \
            [container.time_until_done_other(Job.EXECUTION_TIME_LOWER_BOUND)
             for container in containers]

        obs = np.ndarray([20], dtype=np.float32)
        obs[0] = len(system.get_containers()) # num containers
        obs[1] = len(jobs)  # num queued jobs
        if len(upper_container_completion_times) > 0:
            obs[2] = min(upper_container_completion_times)  # U next container completion time
            obs[3] = np.average(upper_container_completion_times)  # U average container completion time
            obs[4] = max(upper_container_completion_times)  # U last container completion time
        if len(lower_container_completion_times) > 0:
            obs[5] = min(lower_container_completion_times)  # L next container completion time
            obs[6] = np.average(lower_container_completion_times)  # L average container completion time
            obs[7] = max(lower_container_completion_times)  # L last container completion time
        if len(job_receival_time) > 0:
            obs[8] = min(job_receival_time)  # earliest queued job receival time
            obs[9] = np.average(job_receival_time)  # average queued job receival time
            obs[10] = max(job_receival_time)  # latest queued job receival time
        if len(upper_job_execution_time) > 0:
            obs[11] = sum(upper_job_execution_time)  # U queued job volume
            obs[12] = min(upper_job_execution_time)  # U min queued job execution time
            obs[13] = max(upper_job_execution_time)  # U max queued job execution time
        if len(lower_job_execution_time) > 0:
            obs[14] = sum(lower_job_execution_time)  # L queued job volume
            obs[15] = min(lower_job_execution_time)  # L min queued job execution time
            obs[16] = max(lower_job_execution_time)  # L max queued job execution time
        if len(jobs) > 0:
            obs[17] = jobs[0].get_other_info(Job.EXECUTION_TIME_UPPER_BOUND) # U earliest queued job execution time
            obs[18] = jobs[0].get_other_info(Job.EXECUTION_TIME_LOWER_BOUND)  # L earliest queued job execution time
        obs[19] = system.get_startup_time() # new container startup time

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
        obs = self.generate_observation(jobs=self.controller.get_queued_jobs(), system=self.controller.get_system())
        return obs, {}

    """
    Determines when each job would be run if the system is not changed
    
    Returns:
        The list of job queue times
    """
    def get_job_queue_times(self)->list[int]:
        system:SimulatedSystem = self.controller.get_system()
        containers:set[Container] = system.get_containers()

        job_queue_times:list[int] = []

        container_times:list[int] = []
        heapq.heapify(container_times)
        for container in containers:
            jobs = container.get_jobs()
            for job in jobs:
                job_queue_time = container.time_when_job_run(job) - job.get_receival_time()
                job_queue_times.append(job_queue_time)
            heapq.heappush(container_times, container.time_until_done())

        for job in self.controller.get_queued_jobs():
            start_time = heapq.heappop(container_times)
            end_time = start_time + job.get_execution_time()
            heapq.heappush(container_times, end_time)
            job_queue_times.append(start_time)

        return job_queue_times

    """
    Generates the reward of the action given the initial state and the next state
    """
    def get_reward(self, start_containers:int, end_containers:int)->float:
        curr_job_queue_times: list[int] = self.get_job_queue_times()

        reward: float = self.reward_cost_ratio*(start_containers - end_containers)
        if len(curr_job_queue_times) > 0:
            reward += max(curr_job_queue_times)
            reward += np.average(curr_job_queue_times)
        return reward

    """
    Determines the actions given a target number of containers:
        if target < existing, completed containers are shutdown until target is reached
        if target == existing nothing done
        if target > existing, containers are started until the target
    
    Args:
        jobs: the queued jobs
        system: the system being analyzed
        target_num_containers: the target number of containers
        
    Returns:
        The list of actions to perform on the system
    """
    @staticmethod
    def determine_actions(jobs:list[Job], system:SimulatedSystem, target_num_containers:int)->list[Action]:
        actions:list[Action] = []
        job_ind:int = 0
        containers:set[Container] = system.get_containers()
        removed_containers:set[Container] = set()

        wait_time:int = -1

        #Remove completed containers above target
        if len(containers) > target_num_containers:
            for container in containers:
                if len(containers) - len(removed_containers) <= target_num_containers:
                    break
                if container.is_done():
                    removed_containers.add(container)
                    actions.append(Action(action_type=Action.TERMINATE_CONTAINER, container=container))

        #Add jobs to remaining open containers
        for container in containers:
            if job_ind >= len(jobs):
                break
            if container.is_done() and container not in removed_containers:
                actions.append(Action(action_type=Action.ADD_JOBS, container=container, jobs=[jobs[job_ind]]))
                if wait_time == -1 or wait_time < jobs[job_ind].get_execution_time():
                    wait_time = system.get_time() + jobs[job_ind].get_execution_time()
                job_ind += 1

        #Activate new containers
        if len(containers) < target_num_containers:
            if wait_time == -1 or wait_time < system.get_time() + system.get_startup_time():
                wait_time = system.get_time() + system.get_startup_time()
            for new_container in range(target_num_containers - len(containers)):
                actions.append(Action(action_type=Action.ACTIVATE_CONTAINER, jobs=[]))

        if wait_time != -1:
            actions.append(Action(action_type=Action.WAIT, time=wait_time))

        return actions

    """
    Goes to the next step of the simulation
    
    Args:
        action: the target number of containers in the system (rounded to the nearest int)
        
    Returns:
        The state of the system after the action
        The reward received after the action
        Bool tracking if the system is done
        Other information associated with the system
    """
    def step(self, action:np.float32) -> typing.Tuple[np.ndarray, float, bool, bool, typing.Dict[str, typing.Any]]:
        jobs:list[Job] = self.controller.get_queued_jobs()
        system:SimulatedSystem = self.controller.get_system()
        target_num_containers:int = np.rint(action).astype(int)
        actions:list[Action] = self.determine_actions(jobs=jobs, system=system, target_num_containers=target_num_containers)
        start_containers:int = len(system.get_containers())
        self.controller.next_step(actions=actions)
        end_containers: int = len(system.get_containers())
        obs = self.generate_observation(jobs=jobs, system=system)
        reward = self.get_reward(start_containers=start_containers, end_containers=end_containers)
        done = self.controller.is_done()

        return obs, reward, done, False, {}

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