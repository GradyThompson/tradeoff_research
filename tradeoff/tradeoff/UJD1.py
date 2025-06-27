import typing
import math
from simulated_system import SimulatedSystem
from job import Job
from action import Action
from container import Container


"""
Unknown job duration algorithm 1
"""
class UJD1:
    """
    Constructor

    Args:
        params a list of parameters (length 1) 1. epsilon
    """
    def __init__(self, params: list):
        self.epsilon:float = float(params[0])

    """
    Decides system actions based on the deterministic execution time of tasks

    Args:
        system: The system being scheduled upon
        pending_jobs: a list of pending jobs
    """

    def determine_actions(self, system:SimulatedSystem, pending_jobs:list[Job])->list:
        actions:list = []

        delta:int = system.get_startup_time()
        E:int = int(4*delta/self.epsilon)
        time:int = system.get_time()
        curr_epoch:int = time // E

        epoch_jobs:typing.Dict[int, list[Job]] = {}
        for epoch in range(curr_epoch + 1):
            epoch_jobs[epoch] = []

        for job in pending_jobs:
            job_epoch:int = job.get_receival_time() // E
            epoch_jobs[job_epoch].append(job)

        #Tracks the time until the next decision needs to be made
        time_until_next_action:int = E

        #Create mapping of epochs in containers
        epoch_containers:typing.Dict[int, set[Container]] = {}
        for container in system.get_containers():
            container_epoch:int = int(container.get_other_information(Container.JOB_EPOCH))
            if container_epoch not in epoch_containers.keys():
                epoch_containers[container_epoch] = set()
            epoch_containers.get(container_epoch).add(container)

        #Assign jobs to containers
        for epoch in epoch_containers.keys():
            offset:int = epoch*E
            cycle_offset:int = (time-offset)%(E + delta)
            if cycle_offset == 0:
                #Tracks job assignment for new containers
                new_container_job_assignment: typing.Dict[int, list[Job]] = {}
                new_container_assigned_time: typing.Dict[int, int] = {}
                for container in range(len(epoch_containers.get(epoch))):
                    new_container_job_assignment[container] = []
                    new_container_assigned_time[container] = 0

                #Tracks job assignment for existing containers
                existing_container_job_assignment: typing.Dict[Container, list[Job]] = {}
                existing_container_assigned_time: typing.Dict[Container, int] = {}
                for container in epoch_containers.get(epoch):
                    existing_container_job_assignment[container] = []
                    existing_container_assigned_time[container] = 0

                #Find the best container for each job
                for job in epoch_jobs.get(epoch):
                    best_new_container = -1
                    best_existing_container = None
                    best_time = delta + E + 1
                    for container in new_container_job_assignment.keys():
                        if new_container_assigned_time.get(container) < best_time:
                            best_time = new_container_assigned_time.get(container)
                            best_new_container = container
                    for container in epoch_containers.get(epoch):
                        if container.time_until_done() + existing_container_assigned_time.get(container) < best_time:
                            best_time = container.time_until_done()
                            best_existing_container = container
                            best_new_container = -1
                    if best_new_container != -1:
                        new_container_job_assignment.get(best_new_container).append(job)
                        new_container_assigned_time[best_new_container] += job.get_execution_time()
                    elif best_existing_container is not None:
                        existing_container_job_assignment.get(best_existing_container).append(job)
                        existing_container_assigned_time[best_existing_container] += job.get_execution_time()
                    else:
                        break

                #Actions to assign jobs to existing containers
                for container in existing_container_job_assignment.keys():
                    actions.append(Action(action_type=Action.ADD_JOBS,
                                          container=container,
                                          jobs=existing_container_job_assignment.get(container),
                                          other_information={Container.JOB_EPOCH:str(epoch)}))

                #Actions to create new containers
                for container in new_container_job_assignment.keys():
                    actions.append(Action(action_type=Action.ACTIVATE_CONTAINER,
                                          jobs=new_container_job_assignment.get(container),
                                          other_information={Container.JOB_EPOCH:str(epoch)}))
            else:
                time_until_next_action = min(time_until_next_action, E + delta - cycle_offset)

        #Check if a new epoch has completed
        if time % E != 0:
            time_until_next_action = min(time_until_next_action, E - time % E)
        else:
            sorted_epoch_jobs: list[Job] = sorted(epoch_jobs.get(curr_epoch - 1),
                                                  key=lambda x: x.get_receival_time())
            nk:int = len(sorted_epoch_jobs)
            e_minus:int = 0
            for job in sorted_epoch_jobs:
                e_minus += int(job.get_other_info(Job.EXECUTION_TIME_LOWER_BOUND))
            mk:int = math.ceil(nk * e_minus / E)

            # Determine job assignment for new containers (based on what would occur in real system), can be made more
            # efficient using a priority queue to determine assigned container
            container_job_assignment: typing.Dict[int, list[Job]] = {}
            container_assigned_time: typing.Dict[int, int] = {}
            for job in sorted_epoch_jobs:
                best_container:int = -1
                best_time:int = delta + E + 1
                for container in range(mk):
                    if container_assigned_time.get(container) < best_time:
                        best_time = container_assigned_time.get(container)
                        best_container = container
                if best_time <= delta + E:
                    container_job_assignment.get(best_container).append(job)
                    container_assigned_time[best_container] += job.get_execution_time()
                else:
                    break

            # Create new containers
            for new_container in range(mk):
                actions.append(Action(action_type=Action.ACTIVATE_CONTAINER,
                                      jobs=container_job_assignment.get(new_container),
                                      other_information={Container.JOB_EPOCH:str(curr_epoch-1)}))

        for container in system.get_containers():
            if container.get_time_alive() <= time:
                actions.append(Action(action_type=Action.TERMINATE_CONTAINER, container=container))
            else:
                time_until_next_action = min(time_until_next_action, container.time_until_done())

        actions.append(Action(action_type=Action.WAIT, time=time+time_until_next_action))

        return actions