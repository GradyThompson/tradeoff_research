import task as T

"""
Container

Input
tasks - a list of tasks that the container is initially assigned
time - time of creating the container
delta - the start up time
keep_alive - the amount of time to keep alive after the container finishes all tasks
fixed - if the container remains alive indefinitely (fixed number of containers)

Internal variables
tasks - the current tasks queued to run in the container
time - the last time the container was updated
progress - time that commputation has already been performed on the first task 

Stores and runs tasks
"""
class Container:
    def __init__(self, tasks: list[T.Task], time, delta, keep_alive: float = 0.0, fixed: bool = False):
        self.tasks = list(tasks)
        self.time = time + delta
        self.progress = 0.0
        self.start_time = time
        self.keep_alive = keep_alive
        self.finish_time = 0.0
        self.fixed = fixed
        self.is_dead = False
        
        #Stores when each task is run
        self.run_times = {}

    def get_is_dead(self):
        return self.is_dead

    def get_finish_time(self):
        return self.finish_time

    def get_tasks(self):
        return list(self.tasks)

    def add_tasks(self, tasks):
        self.tasks.extend(tasks)

    #Removes all tasks that will finish by the inputed time
    def update(self, time):
        #The time that the next task is starting
        start_time = self.time - self.progress

        #Run tasks until the current time
        while len(self.tasks) > 0 and start_time + self.tasks[0].get_execution_time() <= time:
            self.run_times[self.tasks[0]] = start_time - self.tasks[0].get_receival_time()
            start_time += self.tasks.pop(0).get_execution_time()

        if len(self.tasks) == 0:
            self.progress = 0.0
            if time > self.time + self.keep_alive and not self.fixed:
                self.finish_time = start_time + self.keep_alive
                self.is_dead = True
        else:
            #Update the current progress
            self.progress = time - start_time

        self.time = time

    """
    Finish the simulation and flush the container
    """
    def finish(self):
        #The time that the next task is starting
        start_time = self.time-self.progress

         #Run tasks until done
        while len(self.tasks) > 0:
            self.run_times[self.tasks[0]] = start_time - self.tasks[0].get_receival_time()
            start_time += self.tasks.pop(0).get_execution_time()

        self.progress = 0.0
        self.time = start_time + self.keep_alive
        self.finish_time = self.time
        self.is_dead = True
        return self.time

    def get_remaining_time(self):
        remaining_time = -self.progress
        for task in self.tasks:
            remaining_time += task.get_execution_time()
        if self.finish_time != 0.0:
            remaining_time += max(self.keep_alive + self.finish_time - self.time, 0)
        else:
            remaining_time += self.keep_alive
        return remaining_time
    
    """
    Container waits till given time

    Inputs
    time - what time till wait until
    """
    def wait(self, time):
        self.time = time

    """
    Returns the cost of the container
    """
    def get_cost(self):
        return self.time - self.start_time + self.get_remaining_time()