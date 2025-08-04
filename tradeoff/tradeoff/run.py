import argparse
from system.controller import Controller

parser = argparse.ArgumentParser()
parser.add_argument("config_file", help="Config file containing controller information (see controller doc)")
args = parser.parse_args()
config_file = args.config_file

controller = Controller(config_file)
controller.control_loop()