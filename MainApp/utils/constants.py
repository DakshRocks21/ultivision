#$# Written by Daksh #$#

DATA_PATH = "data"
DEPENDENCIES_PATH = f"{DATA_PATH}/dependencies"
MODEL_GARDEN_PATH = f"{DEPENDENCIES_PATH}/model_garden"

PREFERRED_FILENAME = f'preferred.txt'
PREFERRED_FILENAME_PATH = f"{DATA_PATH}/{PREFERRED_FILENAME}"
CONFIG_PATH = f"{DATA_PATH}/config.json"
SOUND_MAP_KEY = 0
AUDIBLE_REMINDERS_KEY = 1

LABELMAP_FILENAME = 'label_map.pbtxt'
LABELMAP_FILENAME_PATH = f"{DATA_PATH}/{LABELMAP_FILENAME}"

CASE =  {
        0: "person.mp3",
        1: "car.mp3",
        2: "bus.mp3",
        3: "truck.mp3",
        4: "bicycle.mp3",
        5: "dog.mp3",
        6: "cat.mp3",
        7: "door.mp3",
        }