import json
from MainApp.utils.constants import CONFIG_PATH

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def create_config():
    config = {
        "tts" : {"rate": 150, "volume": 1},
        "camera" : {"number": 0},
        "theme" : {"style": "Dark", "palette": "Orange", "hue": "300"}
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)

def check_if_config_exists():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        create_config()
