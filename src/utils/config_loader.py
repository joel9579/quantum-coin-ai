import os
import yaml

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
CONFIG_DIR = os.path.join(BASE_DIR, "configs")

def load_config(config_name="default.yaml"):
    """
    Load YAML configuration from the configs directory.
    
    Args:
        config_name (str): The name of the YAML config file to load.
    
    Returns:
        dict: Parsed YAML config as a dictionary.
    """
    config_path = os.path.join(CONFIG_DIR, config_name)
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config


def get_path_config():
    """
    Convenience loader for file path configurations.
    
    Returns:
        dict: Contains important app directory paths.
    """
    return {
        "BASE_DIR": BASE_DIR,
        "FORECAST_DIR": os.path.join(BASE_DIR, "reports/forecast"),
        "VISUALS_DIR": os.path.join(BASE_DIR, "reports/visuals"),
        "UNPACKED_DIR": os.path.join(BASE_DIR, "data/unpacked"),
        "TEMPLATES_DIR": os.path.join(BASE_DIR, "src/app/templates"),
        "STATIC_DIR": os.path.join(BASE_DIR, "src/app/static"),
    }
