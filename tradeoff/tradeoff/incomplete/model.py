import importlib

"""
Wrapper for the models

Internal variables:
model - <model type> - the scheduling model
"""
class Model:
    """
    Retrieves the model from file

    Model
    Requires input of list of strings

    Input
    file - String - the file name

    File
    <module name>,<class name>,<params comma seperated>
    """
    def __init__(self, file_name):
        file = open(file_name, "r")
        data = file.read().split(",")
        module_name = data[0]
        class_name = data[1]
        params = data[2:]
        model_module = importlib.import_module(module_name)
        model_class = getattr(model_module, class_name)
        self.model = model_class(params)

    """
    Given a system and jobs, returns the actions to perform

    Inputs
    system - SimulatedSystem - the system
    unassigned_jobs - List[Job] - the jobs that have not been assigned to a container

    Return
    List<action> - list of actions to be performed
    """
    def determine_actions(self, system, unassigned_jobs):
        return self.model.determine_actions(system, unassigned_jobs)