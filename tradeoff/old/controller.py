import schedulers as S
import container as C
import task as T

"""
Controller

Inputs
tasks - a list of tasks
scheduler - the scheduler being used
beta - parameter choice for tradeoff between queue time and cost
delta - the startup time of a container

Internal variables
time - current system time in milliseconds
state - mapping of system variables to values
containers - the current containers running in the system
scheduler - a function that models the scheduler
tasks - the list of tasks sorted by release time
keep_alive - time that containers are kept alive after
num_containers - the number of containers kept alive when it is constant

State variables
wait_time - integer set to 0 if no wait time set, otherwise wait at most this time before repolling scheduler
"""
class Controller:
    def __init__(self, tasks: list[T.Task], scheduler, delta: float, epsilon: float = 0.5, keep_alive: float = 0.0, num_containers:int = -1, precision:float = 0.01):
        self.time = 0
        self.containers = set()
        self.scheduler = scheduler
        self.beta = delta/epsilon
        self.delta = delta
        self.precision = precision

        #System state
        self.state = {}
        self.state["wait_time"] = 0
        self.state["keep_alive"] = keep_alive
        self.state["num_containers"] = num_containers

        #Epoch data, key is epoch, value is [time, containers set, max_containers]
        self.state["epochs"] = {}

        #Sort tasks by release times
        self.tasks = sorted(tasks, key = lambda x: x.get_receival_time())

        #Stores the tasks that have not been assigned to a container yet
        self.pending_tasks = set()

        #Current task index
        self.task_index = 0

        #When tasks began
        self.task_start = {}

        #Tracks when containers were alive, key is container, value is [start_time, end_time], end_time is -1 if not set yet
        self.container_life = {}

    """
    Runs the simulation until completion

    Returns the cost
    """
    def run(self):
        done = False
        while not done:
            if self.update():
                done = True

        for container in self.containers:
            self.time = max(self.time, container.finish())

        for epoch in self.state.get("epochs").keys():
            for container in self.state.get("epochs").get(epoch)[1]:
                self.time = max(self.time, container.finish())

        return self.get_cost()

    """
    Updates the system to the next time the scheduler needs to be called

    Returns whether the simulation is done or not
    """
    def update(self):
        #End if no more tasks to be scheduled
        if self.task_index >= len(self.tasks) and len(self.pending_tasks) == 0:
            return True

        #Next time is minimum of the next released task or wait time
        wait_time = self.state.get("wait_time")
        next_time = self.time + wait_time
        if self.task_index < len(self.tasks) and (self.state.get("wait_time") <= self.precision or self.tasks[self.task_index].get_receival_time() < next_time):
            next_time = self.tasks[self.task_index].get_receival_time()

        #Gets tasks that are released by the next time
        #Add prec to avoid floating point error
        self.time = next_time
        while self.task_index < len(self.tasks) and self.tasks[self.task_index].get_receival_time() <= self.time:
            self.pending_tasks.add(self.tasks[self.task_index])
            self.task_index += 1

        #Updates the containers
        removed_containers = set()
        for container in self.containers:
            container.update(self.time)
            #TODO use is_done in container + finish time
            if (self.state.get("num_containers") == -1 or self.state.get("num_containers") < len(self.containers)) and container.get_remaining_time() == 0 and not container.fixed:
                removed_containers.add(container)

        for container in removed_containers:
            self.task_start.update(container.run_times)
            self.containers.remove(container)
            self.container_life[container][1] = self.time

        #Get next schedule
        actions = self.scheduler(self.state, self.containers, self.pending_tasks, self.time, beta=self.beta, delta=self.delta)

        #Reset the wait time
        self.state[wait_time] = 0

        for action in actions:
            if action[0] == S.NEW_CONTAINER:
                tasks = action[1]
                self.containers.add(C.Container(tasks, self.time, self.delta))
                self.container_life[container] = [self.time, -1]
                self.pending_tasks -= set(tasks)
            elif action[0] == S.ASSIGN_CONTAINER:
                container = action[1]
                tasks = action[2]
                container.add_tasks(tasks)
                self.pending_tasks -= set(tasks)
            elif action[0] == S.WAIT:
                self.state["wait_time"] = action[1]
            elif action[0] == S.NEW_FIXED_CONTAINER:
                tasks = action[1]
                self.containers.add(C.Container(tasks, self.time, self.delta, fixed=True))
                self.container_life[container] = [self.time, -1]
                self.pending_tasks -= set(tasks)
            elif action[0] == S.NEW_EPOCH_CONTAINER:
                #TODO make so container is not fixed
                epoch = action[1]
                tasks = action[2]
                container = C.Container(tasks, self.time, self.delta, fixed=True)
                self.container_life[container] = [self.time, -1]
                self.state.get("epochs").get(epoch)[1].add(container)
                self.pending_tasks -= set(tasks)
            else:
                print("Invalid Action ", action)
                quit()

        return False

    """
    Get queue times
    """
    def get_queue_times(self):
        for container in self.containers:
            self.task_start.update(container.run_times)
        for epoch in self.state.get("epochs").keys():
            for container in self.state.get("epochs").get(epoch)[1]:
                self.task_start.update(container.run_times)
        return self.task_start.values()

    """
    Get the cost of running the containers
    """
    def get_cost(self):
        cost = 0
        for container in self.container_life.keys():
            if self.container_life.get(container)[1] == -1:
                cost += self.time - self.container_life.get(container)[0]
            else:
                cost += self.container_life.get(container)[1] - self.container_life.get(container)[0]
        return cost