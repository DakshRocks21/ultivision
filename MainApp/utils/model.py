from MainApp.utils.constants import LABELMAP_FILENAME, PREFERRED_FILENAME, DATA_PATH, PREFERRED_FILENAME_PATH, LABELMAP_FILENAME_PATH
from MainApp.utils.config import change_config
import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def download_model():
    def download_model_ckpt(model_name: str):
        
        if not os.path.exists(f"{DATA_PATH}/{model_name}"):
            os.mkdir(f"{DATA_PATH}/{model_name}")
        
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
            file.GetContentFile(f"{DATA_PATH}/{model_name}/{file['title']}")
        
        return largest_checkpoint_num

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    global drive
    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({'q': f"'1ruOhPNfDMYdz8P2FNRYrlXOwc8yEVJIL' in parents and trashed=false and title='{PREFERRED_FILENAME}'"}).GetList()
    file_list[0].GetContentFile(PREFERRED_FILENAME_PATH)

    with open(PREFERRED_FILENAME_PATH) as f:
        model_name = f.readline()
    print(f"Found best performing model: {model_name}")

    largest_checkpoint_num = download_model_ckpt(model_name)
    file_list = drive.ListFile({'q': f"'1AexnfttBHyjZysolrRy-7xxawWuMudm0' in parents and trashed=false and title='{LABELMAP_FILENAME}'"}).GetList()
    file_list[0].GetContentFile(LABELMAP_FILENAME_PATH)

    change_config(model_name, "model_name")
    change_config(largest_checkpoint_num, "largest_checkpoint_num")
