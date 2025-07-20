import typing
from controller import Controller

"""
Performs an end to end test of a model

Args:
    config_file: the configuration file for the controller
    expected_file_name: the name of the file containing the expected output
"""
def end_to_end_model_test(config_file_name:str, expected_file_name:str):
    controller:Controller = Controller(config_file_name=config_file_name)
    results_file_name:str = controller.control_loop()

    with open(results_file_name, 'r') as results_file, open(expected_file_name, 'r') as expected_file:
        job_queue_times:typing.Dict[int, int] = {}
        cost:int = 0
        expected_job_queue_times:typing.Dict[int, int] = {}
        expected_cost:int = 0

        for line_num, line in enumerate(results_file.readlines()):
            if line_num == 0:
                cost = int(line[5:])
            else:
                formated_line:list[str] = line.split(",")
                job = int(formated_line[0])
                job_queue_times[job] = int(formated_line[1])

        for line_num, line in enumerate(expected_file.readlines()):
            if line_num == 0:
                expected_cost = int(line[5:])
            else:
                formated_line = line.split(",")
                job = int(formated_line[0])
                expected_job_queue_times[job] = int(formated_line[1])

        if len(job_queue_times) < len(expected_job_queue_times):
            print(f"Result file is too small, expected {len(expected_job_queue_times)} "
                  f"and result is {len(job_queue_times)}")

        if len(job_queue_times) > len(expected_job_queue_times):
            print(f"Result file is too large, expected {len(expected_job_queue_times)} "
                  f"and result is {len(job_queue_times)}")

        if cost < expected_cost:
            print(f"Cost too small, expected {expected_cost} and result is {cost}.")

        if cost > expected_cost:
            print(f"Cost too large, expected {expected_cost} and result is {cost}.")

        for job in job_queue_times.keys():
            result = job_queue_times.get(job)
            expected = expected_job_queue_times.get(job)
            if result != expected:
                print(f"Different for job {job}, expected {expected}, but result was {result}")
                return
        print("Files are identical.")