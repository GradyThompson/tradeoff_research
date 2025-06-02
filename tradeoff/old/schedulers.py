import task
import container
import random
import math

#Possible actions
NEW_CONTAINER = 1
ASSIGN_CONTAINER = 2
WAIT = 3
NEW_FIXED_CONTAINER = 4
NEW_EPOCH_CONTAINER = 5

"""
Schedulers

Contains functions that generate what operation should be performed by a system when presented with a new task.

Inputs
state - the system state represented by a mapping of system variables to there values
containers - the set of containers in the system
tasks - the set of tasks being added
time - the current time
beta - parameter that models the tradeoff of queue time and cost, higher beta is lower cost, lower beta is lower queue  time
delta - the startup time

Returns a list of list, where each element is an action to perform, with each action containing the chosen action and any parameters of the action [<action type>, ... <additional parameters>]
Possible actions
NEW_CONTAINER - give list of tasks being added - [NEW_CONTAINER, [<tasks>]]
ASSIGN_CONTAINER - give list of tasks being added - [ASSIGN_CONTAINER, <container>, [<tasks>]]
WAIT - give a list of tasks to perform no action on until the specified time - [WAIT, <wait time in milliseconds>, [<tasks>]]
NEW_FIXED_CONTAINER - give list of tasks being added - [NEW_FIXED_CONTAINER, [<tasks>]]
NEW_EPOCH_CONTAINER - give list of tasks being added - [NEW_EPOCH_CONTAINER, <epoch>, [<tasks>]]
"""

"""
Random scheduler:
Assigns all tasks to random containers (including new containers)
"""
def random_scheduler(state, containers, tasks, time, beta, delta):

    #Creates a list of containers to maintain an order
    container_list = list(containers)
    
    #Assigns each container an index for random selection, and initializes a map to store tasks assigned to that container
    container_map = {}
    for container in range(len(containers)):
        container_map[container] = []

    #Initializes a set to track new containers, that need to be created
    new_containers = set()

    #Chooses containers for each task
    for task in tasks:
        #Select a random option: if choice < len(container_list), then the container at that index is chosen, else if choice == len(container_list) a new container is created
        choice = random.randint(0, len(container_map))
        if choice not in container_map.keys():
            new_containers.add(choice)
            container_map[choice] = [task]
        else:
            container_map[choice].append(task)

    #Creates action list
    actions = []

    for container in container_map.keys():
        if container in new_containers:
            actions.append([NEW_CONTAINER, container_map.get(container)])
        elif not container_map.get(container).isempty():
            actions.append([ASSIGN_CONTAINER, container_list[container], container_map.get(container)])
    
    return actions

"""
Deterministic scheduler:
Schedules the given tasks based on a deterministic time (mean, median, etc)
"""
def deterministic_scheduler(state, containers, tasks, time, beta, delta):
    tasks = sorted(tasks, key = lambda x: x.get_receival_time())

    actions = []

    #Creates a list of tasks sorted by release time
    task_ind = 0

    #Assign tasks to containers that have low queue times
    for container in containers:
        assigned_tasks = []
        curr_time = container.get_remaining_time()

        #While tasks can be assigned such that they do not have queue time, assign them
        while task_ind < len(tasks) and time - tasks[task_ind].get_receival_time() + curr_time <= beta + delta:
            curr_time += tasks[task_ind].get_execution_time()
            assigned_tasks.append(tasks[task_ind])
            task_ind += 1
        
        if len(assigned_tasks) > 0:
            actions.append([ASSIGN_CONTAINER, container, assigned_tasks])

    #Assign tasks to new containers
    while task_ind < len(tasks) and time - tasks[task_ind].get_receival_time() + sum([task.get_execution_time() for task in tasks[task_ind:]]) >= beta:
        curr_time = 0
        assigned_tasks = []
        while task_ind < len(tasks) and curr_time <= beta:
            assigned_tasks.append(tasks[task_ind])
            curr_time += tasks[task_ind].get_execution_time()
            task_ind += 1
        if len(assigned_tasks) > 0:
            actions.append([NEW_CONTAINER, assigned_tasks])

    #Wait on remaining tasks
    if task_ind < len(tasks):
        wait_time = beta - (time - tasks[task_ind].get_receival_time() + sum([task.get_execution_time() for task in tasks[task_ind:]]))
        actions.append([WAIT, wait_time, tasks[task_ind:]])

    return actions

"""
Bounded scheduler:
Schedules the given tasks based on a bounded time (min, max)
"""
def bounded_scheduler(state, containers, tasks, time, beta, delta):
    tasks = sorted(tasks, key = lambda x: x.get_receival_time())

    actions = []

    #Creates a list of tasks sorted by release time
    task_ind = 0

    #Assign tasks to containers that have low queue times
    for container in containers:
        assigned_tasks = []
        curr_time = container.get_remaining_time()

        #While tasks can be assigned such that they do not have queue time, assign them
        while task_ind < len(tasks) and time - tasks[task_ind].get_receival_time() + curr_time <= beta + delta:
            curr_time += tasks[task_ind].get_bounds()[1]
            assigned_tasks.append(tasks[task_ind])
            task_ind += 1
        
        if len(assigned_tasks) > 0:
            actions.append([ASSIGN_CONTAINER, container, assigned_tasks])

    #Assign tasks to new containers
    while task_ind < len(tasks) and time - tasks[task_ind].get_receival_time() + sum([task.get_bounds()[1] for task in tasks[task_ind:]]) >= beta:
        curr_time = 0
        assigned_tasks = []
        while task_ind < len(tasks) and curr_time <= beta:
            assigned_tasks.append(tasks[task_ind])
            curr_time += tasks[task_ind].get_bounds()[1]
            task_ind += 1
        if len(assigned_tasks) > 0:
            actions.append([NEW_CONTAINER, assigned_tasks])

    #Wait on remaining tasks
    if task_ind < len(tasks):
        wait_time = beta - (time - tasks[task_ind].get_receival_time() + sum([task.get_bounds()[1] for task in tasks[task_ind:]]))
        actions.append([WAIT, wait_time, tasks[task_ind:]])

    return actions

"""
EDF scheduler:
Schedules the given tasks using EDF with a fixed number of containers (number of containers is in state.num_containers)
"""
def EDF_scheduler(state, containers, tasks, time, beta, delta):
    sorted_tasks = sorted(tasks, key = lambda x: x.get_receival_time())

    num_containers = int(state.get("num_containers"))
    if num_containers == None or num_containers == -1:
        print("ERROR: Incorrect parameters for EDF scheduler, missing number of containers")
        quit()
    
    assignments = {}
    for container in containers:
        assignments[container] = [[], container.get_remaining_time()]

    new_containers = {}

    containers_to_add = max(0, num_containers - len(containers))
    for container in range(containers_to_add):
        new_containers[containers_to_add] = [[], 0]

    while len(sorted_tasks) > 0:
        task = sorted_tasks.pop(0)
        #Find best container
        best_container = None
        best_time = -1
        for container in assignments.keys():
            if best_time == -1 or assignments.get(container)[1] < best_time:
                best_container = container
                best_time = assignments.get(container)[1]
        for container in new_containers.keys():
            if best_time == -1 or new_containers.get(container)[1] < best_time:
                best_container = container
                best_time = new_containers.get(container)[1]

        #Assign to best container
        if best_container in assignments.keys():
            assignments[best_container][0].append(task)
            assignments[best_container][1] += task.get_execution_time()
        else:
            new_containers[best_container][0].append(task)
            new_containers[best_container][1] += task.get_execution_time()

    #Formulate action list
    actions = []
    for container in assignments.keys():
        if len(assignments.get(container)[0]) > 0:
            actions.append([ASSIGN_CONTAINER, container, assignments.get(container)[0]])
    for container in new_containers:
        actions.append([NEW_CONTAINER, new_containers.get(container)[0]])
    return actions

"""
Bounded doubling scheduler:
Based on paper, method for bounded execution times that double containers
"""
def bounded_double_scheduler(state, containers, tasks, time, beta, delta):

    E = 4*beta

    sorted_tasks = sorted(tasks, key = lambda x: x.get_receival_time())
    epochs = {}

    #Sort tasks into their epochs
    if len(sorted_tasks) > 0:
        curr_task = 0
        curr_time = 0
        while curr_task < len(sorted_tasks) and curr_time < time:
            epochs[curr_time] = []
            while curr_task < len(sorted_tasks) and sorted_tasks[curr_task].get_receival_time() < E + curr_time:
                epochs[curr_time].append(sorted_tasks[curr_task])
                curr_task += 1
            curr_time += E

    waiting_jobs = []
    waiting_time = E + delta - time % (delta + E)
    if waiting_time < 0.001:
        waiting_time = delta + E

    actions = []
    #Check if jobs should be assigned
    for epoch in epochs.keys():

        #If it is a new epoch, add to the system
        if not epoch in state["epochs"].keys():
            state["epochs"][epoch] = [epoch + E + delta, set(), math.ceil(len(epochs.get(epoch))*sum([task.get_bounds()[0] for task in epochs.get(epoch)])/E)]

        remove_containers = set()

        #Update containers
        for container in state["epochs"].get(epoch)[1]:
            container.update(time)
            if container.get_remaining_time() < 0.001 and len(epochs.get(epoch)) > 0:
                task = epochs.get(epoch).pop(0)
                actions.append([ASSIGN_CONTAINER, container, [task]])
                if waiting_time > task.get_execution_time():
                    waiting_time = task.get_execution_time()
            elif container.get_remaining_time() < 0.001:
                remove_containers.add(container)
            elif waiting_time > container.get_remaining_time():
                waiting_time = container.get_remaining_time()

        #Remove unused containers
        for container in remove_containers:
            state["epochs"].get(epoch)[1].remove(container)

        #Check if new containers need to be created
        if abs(state["epochs"].get(epoch)[0] - (epoch + E + delta)) < 0.001 and abs(time - (epoch + E + delta)) < 0.001:
            #Initial containers
            container = 1
            while container <= state["epochs"].get(epoch)[2] and len(epochs.get(epoch)) > 0:
                task = epochs.get(epoch).pop(0)
                if task.get_execution_time() + delta < waiting_time:
                    waiting_time = task.get_execution_time() + delta
                actions.append([NEW_EPOCH_CONTAINER, epoch, [task]])
                container += 1
        elif state["epochs"].get(epoch)[0] + E + delta <= time + 0.001:
            #Stale epoch
            if len(epochs.get(epoch)) > 0:
                state["epochs"].get(epoch)[2] *= 2
            if state["epochs"].get(epoch)[2] == 0:
                print(state["epochs"])
                quit()
            container = 1
            while container <= state["epochs"].get(epoch)[2] and len(epochs.get(epoch)) > 0:
                task = epochs.get(epoch).pop(0)
                if task.get_execution_time() + delta < waiting_time:
                    waiting_time = task.get_execution_time() + delta
                actions.append([NEW_EPOCH_CONTAINER, epoch, [task]])
                container += 1
            state["epochs"].get(epoch)[0] += E + delta
        else:
            #If it is not time to update, then 
            if state["epochs"].get(epoch)[0] + E + delta - time < waiting_time and len(epochs.get(epoch)) > 0:
                waiting_time = state["epochs"].get(epoch)[0] + E + delta - time
            waiting_jobs.extend(epochs.get(epoch))

    actions.append([WAIT, waiting_time, waiting_jobs])
    return actions