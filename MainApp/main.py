##/ MISC IMPORTS/##
import os
from MainApp.utils.constants import PREFERRED_FILENAME
from MainApp.utils.dependencies import download_model_files

##/ GOOGLE DRIVE AUTHENTICATION IMPORTS/##
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

##/ TENSORFLOW IMPORTS/##
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util


# Authenticate and create the PyDrive client.
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)
file_list = drive.ListFile({'q': f"'1ruOhPNfDMYdz8P2FNRYrlXOwc8yEVJIL' in parents and trashed=false and title='{PREFERRED_FILENAME}'"}).GetList()
file_list[0].GetContentFile(PREFERRED_FILENAME)

with open(PREFERRED_FILENAME) as f:
    model_name = f.readline()
print(f"Found best performing model: {model_name}")

largest_checkpoint_num = download_model_files(model_name)

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(f"{model_name}/pipeline.config")
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(f"{model_name}/ckpt-{largest_checkpoint_num}").expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections
