#$# Written by Daksh #$#

import json
from MainApp.utils.constants import CONFIG_PATH

def load_config():
    """
    Loads the config file
    """
    with open(CONFIG_PATH) as f:
        return json.load(f)

def create_config():
    """
    Creates a config file
    """
    config = {
        "isOnboardingCompleted" : False,
        "camera" : {"number": 0},
        "theme" : {"style": "Light", "palette": "Orange", "hue": "300"},
        "settings" : {"mode": 1},
        "largest_checkpoint_num" : "",
        "model_name" : "",
        "blind_mode" : 0,
        "confidence_threshold" : 0.5,
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)

def check_if_config_exists():
    """
    Checks if the config file exists
    if not, creates a new config file
    """

    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        create_config()


def change_config(value, key):
    """
    Changes the value of a key in the config file
    """
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    config[key] = value
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)