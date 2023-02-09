
## / KIVY IMPORTS /##
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image, CoreImage
from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition, SlideTransition
from kivy.graphics.texture import Texture
from kivy.base import EventLoop
from kivymd.icon_definitions import md_icons
from kivymd.uix.dialog import MDDialog

## / TTS IMPORTS /##
import pyttsx3
import speech_recognition as sr

##/ UTILS IMPORTS /##
from MainApp.utils.config import load_config, create_config
from MainApp.utils.constants import LABELMAP_FILENAME, DATA_PATH, LABELMAP_FILENAME_PATH

##/ TENSOFLOW IMPORTS /##
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util

## / OTHER IMPORTS /##
import cv2
import numpy as np
import time
import os
from threading import Thread
from queue import Queue
import matplotlib.pyplot as plt
import io

## / KIVY UI /##

KIVY_CONFIG = '''
WindowManager:
    HomeScreen:
    SettingsScreen:
    CameraScreen:
<HomeScreen>:
    name: 'home'
    MDScreen:
        
        orientation: 'vertical'
        MDLabel:
            text: 'Welcome to Our App!'
            font_style: 'H4' 
            halign: 'center'
        MDFlatButton:
            text: 'Start'
            md_bg_color: app.theme_cls.primary_light
            font_style: 'Subtitle1' 
            pos_hint: {"center_x": 0.5, "center_y": 0.1}
            on_press: app.startcam()
<SettingsScreen>:
    name: 'settings'
    MDScreen:
        orientation: 'vertical'
        MDFillRoundFlatIconButton:
            icon: 'chevron_left'
            text: "Back"
            pos_hint: {"center_x": 0.1, "center_y": 0.95}
            font_style: 'Caption'
            text_color: 1, 1, 1, 1
            background_color: 0, 0, 0, 0
            on_press: app.root.current = 'camera'
        MDLabel:
            text: "Settings"
            pos_hint: {"center_x": 0.5, "center_y": 0.95}
            font_style: 'H5'
            halign: 'center'
        MDLabel:
            id: MyCoolID
            text: "Choose your preferred mode!"
            pos_hint: {"center_x": 0.5, "center_y": 0.8}
            font_style: 'H4'
            halign: 'center'
        MDFlatButton:
            text: 'Sound Map'
            pos_hint: {"center_x": 0.275, "center_y": 0.45}
            size_hint: 0.425, 0.525
            md_bg_color: app.theme_cls.primary_light
            on_press: app.changeText("Sound Map.")
        MDFlatButton:
            text: 'Audible Reminders'
            pos_hint: {"center_x": 0.725, "center_y": 0.45}
            size_hint: 0.425, 0.525
            md_bg_color: app.theme_cls.primary_light
            on_press: app.changeText("Audible Reminders.")
<CameraScreen>:
    name: 'camera'
    MDScreen:
        orientation: 'vertical'
        MDLabel:
            text: 'Camera Page'
            font_style: 'H4'
            pos_hint: {"center_x": 0.5, "center_y": 0.9}
        BoxLayout:
            id: layout
        MDFlatButton:
            text: 'Settings'
            pos_hint: {"center_x": 0.3, "center_y": 0.1}
            md_bg_color: app.theme_cls.primary_light
            on_press: app.open_settings()
        MDFlatButton:
            text: 'Exit'
            pos_hint: {"center_x": 0.7, "center_y": 0.1}
            md_bg_color: app.theme_cls.primary_light
            on_press: app.stopcam()
        
'''

# Class's written by Daksh


class HomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class CameraScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):

    def build(self):
        self.json_config = load_config()
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        self.config = load_config()
        self.theme_cls.theme_style = self.json_config['theme']['style']
        self.theme_cls.primary_palette = self.json_config['theme']['palette']
        self.theme_cls.primary_hue = self.json_config['theme']['hue']
        self.CAMERA = self.config['camera']['number']
        self.oncam = False
        return Builder.load_string(KIVY_CONFIG)

    def changeText(self, word):
        text = self.root.get_screen("settings").ids.MyCoolID.text 
        if text == "You selected " + word:
            self.root.transition = SlideTransition(direction="right")
            self.root.current = 'camera'
        else:
            self.root.get_screen("settings").ids.MyCoolID.text = "You selected " + word

    def on_stop(self):
        if self.oncam:
            self.stopcam()

    def startcam(self):
        self.image = Image()  # create image here as startcam is in another thread
        self.root.get_screen('camera').ids.layout.add_widget(self.image)
        self.root.transition = SlideTransition(direction="left")
        self.root.current = 'camera'
        self.oncam = True
        self.capture = cv2.VideoCapture(int(self.CAMERA))
        self.tensorflowThread = Thread(target=tensorflow, args=(inputQ, outputQ))
        self.tensorflowThread.start()
        Clock.schedule_interval(self.loadVideo, 1.0/30.0)


    
    def loadVideo(self, dt):
        if self.oncam and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                outputQ.put(frame)
                new_frame = inputQ.get()
                buf = cv2.flip(new_frame, 0).tostring()
                texture = Texture.create(size=(new_frame.shape[1], new_frame.shape[0]), colorfmt='bgr') 
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture
                inputQ.task_done()

    def stopcam(self):
        stop_threads = True
        self.oncam = False
        self.capture.release()
        self.root.get_screen('camera').ids.layout.remove_widget(self.image)
        self.root.transition = SlideTransition(direction="right")
        self.root.current = 'home'

    def open_settings(self):
        self.root.transition = SlideTransition(direction="left")
        self.root.current = 'settings'



def tensorflow(outputQ, inputQ):
    json_config = load_config()
    configs = config_util.get_configs_from_pipeline_file(f"{DATA_PATH}/{json_config['model_name']}/pipeline.config")
    detection_model = model_builder.build(model_config=configs['model'], is_training=False)
    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore(f"{DATA_PATH}/{json_config['model_name']}/ckpt-{json_config['largest_checkpoint_num'] }").expect_partial()

    @tf.function
    def detect_fn(image):
        image, shapes = detection_model.preprocess(image)
        prediction_dict = detection_model.predict(image, shapes)
        detections = detection_model.postprocess(prediction_dict, shapes)
        print("here")
        return detections

    category_index = label_map_util.create_category_index_from_labelmap(LABELMAP_FILENAME)
    print(stop_threads)
    while not stop_threads: 
        frame = inputQ.get()
        image_np = np.array(frame)
        
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)
        
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
        detections['num_detections'] = num_detections

        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        label_id_offset = 1
        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
                    image_np_with_detections,
                    detections['detection_boxes'],
                    detections['detection_classes']+label_id_offset,
                    detections['detection_scores'],
                    category_index,
                    use_normalized_coordinates=True,
                    max_boxes_to_draw=10,
                    min_score_thresh=.3,
                    agnostic_mode=False)

        outputQ.put(image_np_with_detections)


def launchApp():
    global stop_threads
    stop_threads = False
    global inputQ, outputQ
    inputQ = Queue()
    outputQ = Queue()
    MainApp().run()
    