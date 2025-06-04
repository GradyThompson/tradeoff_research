from tradeoff.container import Container

"""
Class simulates a state based system of containers

Internal variables:
containers - set[Container] - the set of containers in the system
time - int - the current time of the system
accrued_cost - int - cost incurred so far from shutdown containers
"""
class SimulatedSystem:
    """
    Constructor, initializes a simulated system with no containers

    Args
        startup_time: time for container to startup
        curr_time: the start time of the simulation
    """
    def __init__(self, startup_time:int, curr_time:int=0):
        self.containers:set[Container] = set()
        self.time = curr_time
        self.startup_time = startup_time
        self.accrued_cost = 0

    """
    Performs the inputed actions
    
    input
    actions - List[Action] - a list of actions to perform (performed in order)
    """
    def perform_actions(self, actions):
        for action in actions:
            action_type = action.get_action_type()
            if action_type == "activate_container":
                self.activate_container()
            elif action_type == "terminate_container":
                self.terminate_container(action.get_container())
            elif action_type == "add_jobs":
                self.assign_jobs(action.get_jobs(), action.get_container())
            elif action_type == "remove_jobs":
                self.remove_jobs(action.get_jobs(), action.get_container())
            elif action_type == "reorder_jobs":
                self.reorder_jobs(action.get_jobs(), action.get_containe())

    """
    Returns the set of containers in the system
    
    Returns
        The container set
    """
    def get_containers(self):
        return self.containers

    """
    Returns the system time
    
    Returns
        the system time
    """
    def get_time(self):
        return self.time

    """
    Adds a new container to the system
    """
    def activate_container(self):
        self.containers.add(Container())

    """
    Removes a container from the system

    Input
    container - Container - the container to remove
    """
    def terminate_container(self, container):
        self.accrued_cost += container.get_time_alive()
        self.containers.remove(container)

    """
    Assigns the given jobs to the given container

    Inputs
    jobs - List[Jobs] - the jobs to be added
    container - Container - the container being added to
    """
    def assign_jobs(self, jobs, container):
        for job in jobs:
            container.add_job(job)

    """
    Removes jobs from a container

    Inputs
    jobs - List[Job] - the jobs to be removed
    container - Container - the container being removed from
    """
    def remove_jobs(self, jobs, container):
        for job in jobs:
            container.remove_job(job)

    """
    Reorders the jobs to the new order on a container

    Inputs
    new_job_order - List[Job] - the jobs in a new order
    container - Container - the container being reordered
    """
    def reorder_jobs(self, new_job_order, container):
        container.new_job_order(new_job_order)

    """
    Run the system until the provided time

    Inputs:
    time - int - time to run until
    """
    def run(self, time):
        for container in self.containers:
            container.run(time)
        self.time = time

    """
    Returns the cost incurred by the system so far
    """
    def get_cost(self):
        cost = self.accrued_cost
        for container in self.containers:
            cost += container.get_time_alive()
        return cost
    
    """
    Sets the cost to 0
    """
    def reset_cost(self):
        self.accrued_cost = 0

    """
    Resets the system
    """
    def reset(self, curr_time=0):
        self.containers = set()
        self.time = curr_time
        self.accrued_cost = 0

    """
    Completes all jobs in the system and closes all containers
    """
    def finish(self):
        for container in self.containers:
            container.finish()
            self.terminate_container(container=container)

    """
    Checks if all work is completed
    """
    def is_done(self):
        for container in self.containers:
            if container.is_done() == False:
                return False
        return True

    """
    Returns the startup time of a container
    
    :returns container startup time
    """
    def get_startup_time(self):
        return self.startup_time