import os
from MainApp.utils.constants import MODEL_GARDEN_PATH

def download_dependencies():
    print("Welcome to Computing+ Group K Coursework! Code written by Daksh Thapar, Richard Tan and Tan Xuan Han")
    print("This script will now download the best performing model from Google Drive.")
    print()
    print("Seting up the environment and installing dependencies...")
    os.system("pip3 install -q -r requirements.txt")

    # Clone TensorFlow Model Garden if it has not been cloned yet
    if not os.path.exists(MODEL_GARDEN_PATH):
        os.system(f"git clone https://github.com/tensorflow/models {MODEL_GARDEN_PATH}")

    # Install TensorFlow Object Detection API
    os.system("pip3 install -q protobuf")
    os.system(f"cd {MODEL_GARDEN_PATH}/research && protoc object_detection/protos/*.proto --python_out=. && cp object_detection/packages/tf2/setup.py . && pip install -q .")
    os.system("curl https://raw.githubusercontent.com/protocolbuffers/protobuf/main/python/google/protobuf/internal/builder.py -o coursework-test/lib/python3.10/site-packages/google/protobuf/internal/builder.py")


def download_model_files(model_name: str):
    global drive
    
    if not os.path.exists(model_name):
        os.mkdir(model_name)
    
    file_list = drive.ListFile({'q': f"'1ruOhPNfDMYdz8P2FNRYrlXOwc8yEVJIL' in parents and trashed=false and title='{model_name}'"}).GetList()
    model_folder_id = file_list[0]["id"]
    model_files_list = drive.ListFile({'q': f"'{model_folder_id}' in parents and trashed=false"}).GetList()

    largest_checkpoint_num = 0
    largest_checkpoint_index_file = None
    largest_checkpoint_data_file = None
    download_files = []
    for file in model_files_list:
        file_name = file["title"]
        if file_name == "pipeline.config":
            download_files.append(file)
            continue
        if file_name.startswith("ckpt-"):
            checkpoint_id = file_name.split(".")[0]
            checkpoint_num = int(checkpoint_id.split("-")[1])
            checkpoint_type = file_name.split(".")[1]
            if checkpoint_num >= largest_checkpoint_num:
                largest_checkpoint_num = checkpoint_num
                if checkpoint_type == "index":
                    largest_checkpoint_index_file = file
                else:
                    largest_checkpoint_data_file = file

    print("Downloading model files...")
    print(f"Downloading checkpoint {largest_checkpoint_num}...")
    download_files.append(largest_checkpoint_index_file)
    download_files.append(largest_checkpoint_data_file)

    for file in download_files:
        file.GetContentFile(f"{model_name}/{file['title']}")
    
    return largest_checkpoint_num
