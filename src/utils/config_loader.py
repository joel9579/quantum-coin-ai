import yaml
import os

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "../../configs")

def load_config(name):
    with open(os.path.join(CONFIG_DIR, name), "r") as file:
        return yaml.safe_load(file)
