import argparse
from tradeoff.controller import Controller
from itertools import zip_longest

parser = argparse.ArgumentParser()
parser.add_argument("config_file", help="Config file containing controller information (see controller doc)")
parser.add_argument("expected_file", help="File containing the expected result of the system")
args = parser.parse_args()
config_file = args.config_file
expected_file_name = args.expected_file

controller = Controller(config_file)
results_file_name = controller.control_loop()

with open(results_file_name, 'r') as results_file, open(expected_file_name, 'r') as expected_file:
    for line_num, (result, expected) in enumerate(zip_longest(results_file, expected_file), start=1):
        if result != expected:
            print(f"Different on line {line_num}:")
            if result is not None:
                print(f"Result {result}")
            else:
                print("Results is shorter than expected")

            if expected is not None:
                print(f"Expected {expected}")
            else:
                print("Results is longer than expected")
    else:
        print("Files are identical.")