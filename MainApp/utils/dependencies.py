#$# Written by Daksh and Xuan Han #$#

import os
from MainApp.utils.constants import MODEL_GARDEN_PATH
from time import sleep

def download_dependencies():
    """
    This function will download the dependencies and models required for the app to run.
    """
    print("Welcome to Computing+ Group K Coursework! Code written by Daksh Thapar, Richard Tan and Tan Xuan Han")
    print("This script will now download the best performing model from Google Drive.")
    print()
    print("Seting up the environment and installing dependencies...")
    print()
    print(f"\033[91m This may take some time. Please wait.\033[00m")
    sleep(1)
    os.system("brew install portaudio")
    os.system("brew install protobuf")
    os.system("pip3 install -q -r requirements.txt")
    # Clone TensorFlow Model Garden if it has not been cloned yet
    if not os.path.exists(MODEL_GARDEN_PATH):
        os.system(f"git clone https://github.com/tensorflow/models {MODEL_GARDEN_PATH}")

    os.system(f"cd {MODEL_GARDEN_PATH}/research && protoc object_detection/protos/*.proto --python_out=. && cp object_detection/packages/tf2/setup.py . && pip install -q .")
    os.system("curl https://raw.githubusercontent.com/protocolbuffers/protobuf/main/python/google/protobuf/internal/builder.py -o coursework-venv/lib/python3.10/site-packages/google/protobuf/internal/builder.py")
    from MainApp.utils.model import download_model
    download_model()