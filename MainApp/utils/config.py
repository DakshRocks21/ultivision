#$# Written by Daksh #$#

import json
from MainApp.utils.constants import CONFIG_PATH

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def create_config():
    config = {
        "isOnboardingCompleted" : False,
        "tts" : {"rate": 150, "volume": 1},
        "camera" : {"number": 0},
        "theme" : {"style": "Light", "palette": "Orange", "hue": "300"},
        "settings" : {"mode": 1},
        "largest_checkpoint_num" : "",
        "model_name" : "",
        "blind_mode" : 0
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)

def check_if_config_exists():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        create_config()


def change_config(value, key):
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    config[key] = value
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)