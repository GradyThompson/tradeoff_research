import importlib
from simulated_system import SimulatedSystem
from job import Job
from action import Action
import typing
import types

"""
Wrapper for the models

Model methods
    __init__(self, params)
    determine_actions(system:SimulatedSystem, unassigned_jobs:list[Job])->list[Action]
"""
class Model:
    """
    Retrieves a models metadata from a file and imports the model

    Args:
        module_name: the name of the python module that contains the model
        class_name: the name of the python class with the model
        params: any additional params needed for the model

    File
    <module name>,<class name>,<params comma separated>
    """
    def __init__(self, module_name:str, class_name:str, params:list[str]):
        model_module:types.ModuleType = importlib.import_module(module_name)
        model_class:typing.Any = getattr(model_module, class_name)
        self.model = model_class(params)

    """
    Given a system and jobs, returns the actions to perform

    Args:
        system: the system
        unassigned_jobs: the jobs that have not been assigned to a container

    Return
        The list of actions to be performed
    """
    def determine_actions(self, system:SimulatedSystem, unassigned_jobs:list[Job])->list[Action]:
        return self.model.determine_actions(system, unassigned_jobs)