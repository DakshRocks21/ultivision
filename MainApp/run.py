
## / KIVY IMPORTS /##
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDTextButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image, CoreImage
from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition, SlideTransition
from kivy.graphics.texture import Texture
from kivy.base import EventLoop
from kivymd.icon_definitions import md_icons
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

## / TTS IMPORTS /##
from playsound import playsound

##/ UTILS IMPORTS /##
from MainApp.utils.config import load_config, change_config
from MainApp.utils.constants import LABELMAP_FILENAME, DATA_PATH, LABELMAP_FILENAME_PATH, CASE

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

KV = """
WindowManager:
    HomeScreen:
    LoadingScreen:
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

<LoadingScreen>:
    name: 'loading'
    MDScreen:
        orientation: 'vertical'
        MDLabel:
            text: 'Loading...'
            font_style: 'H4'
            halign: 'center'

<SettingsScreen>:
    name: 'settings'
    MDScreen:
        orientation: 'vertical'
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
        MDSwitch:
            id: switch
            pos_hint: {'center_x': .3, 'center_y': .1}
            on_active: app.on_switch_active(*args)

        MDRectangleFlatIconButton:
            id: button
            text: "Woah Dropdown"
            icon: "language-python"
            pos_hint: {"center_x": .7, "center_y": .1}
            on_release: app.dropdown1.open()

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
            on_press: app.stopcam(True)
"""


class HomeScreen(Screen):
    pass

class LoadingScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass


class CameraScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):

    def build(self):        
        self.tensorflowThread = Thread(target=tensorflow, args=(inputQ, outputQ))
        self.tensorflowThread.start()

        self.image = Image()
        self.get_labels()
        self.json_config = load_config()
        self.theme_cls.theme_style = self.json_config['theme']['style']
        self.theme_cls.primary_palette = self.json_config['theme']['palette']
        self.theme_cls.primary_hue = self.json_config['theme']['hue']
        self.CAMERA = self.json_config['camera']['number']
        self.oncam = False
        
        return Builder.load_string(KV)

    def get_labels(self):
        self.category_index = label_map_util.create_category_index_from_labelmap(LABELMAP_FILENAME_PATH, use_display_name=True)
        for key, value in self.category_index.items():
            labels.append(value["name"].lower())
    
    def goBackToCamera(self):
        self.oncam = True
        self.startcam()
        self.root.transition = SlideTransition(direction="right")
        self.root.current = 'camera'

    def on_switch_active(self, switch, value):
        if value:
            change_config(1, "blind_mode")
        else:
            change_config(0, "blind_mode")

    def on_start(self):
        if self.json_config['blind_mode'] == 1:
            self.root.get_screen("settings").ids.switch.active = True
            # switch to camera screen
            self.startcam()

    def open_settings(self):
        self.root.transition = SlideTransition(direction="left")
        self.root.current = 'settings'
        self.stopcam(False)
        try:
            self.root.get_screen('camera').ids.layout.remove_widget(self.image)
        except:
            pass
        menu_items = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.read()[0]:
                menu_items.append({
                    "viewclass": "OneLineListItem",
                    "text": "Camera " + str(i),
                    "on_release": lambda x=i: self.selectCamera(x),
                })
                cap.release()

        self.dropdown1 = MDDropdownMenu(items=menu_items, width_mult=4, caller=self.root.get_screen("settings").ids.button) 
    
    def selectCamera(self, i):
        print("Camera " + str(i) + " selected")
        self.CAMERA = int(i)
        self.dropdown1.dismiss()

    def changeText(self, word):
        text = self.root.get_screen("settings").ids.MyCoolID.text 
        if text == "You selected " + word:
            self.startcam()
            self.root.transition = SlideTransition(direction="right")
            self.root.current = 'camera'
        else:
            self.root.get_screen("settings").ids.MyCoolID.text = "You selected " + word
        

    def on_stop(self):
        stop_threads = True
        self.tensorflowThread.join(timeout=1)
        if self.oncam:
            self.stopcam(0)


    def startcam(self):
        self.root.transition = SlideTransition(direction="right")
        self.root.current = 'loading'
        self.capture = cv2.VideoCapture(int(self.CAMERA))
        self.oncam = True
        self.root.get_screen('camera').ids.layout.add_widget(self.image)
        Clock.schedule_interval(self.loadVideo, 1.0/30.0)
        self.root.transition = SlideTransition(direction="left")
        self.root.current = 'camera'
    
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

    def stopcam(self, condition):
        self.oncam = False
        self.capture.release()
        self.root.get_screen('camera').ids.layout.remove_widget(self.image)
        if condition:
            self.root.transition = SlideTransition(direction="right")
            self.root.current = 'home'


def tensorflow(output, input1):
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
        return detections

    category_index = label_map_util.create_category_index_from_labelmap(LABELMAP_FILENAME_PATH)
    
    while not stop_threads: 
        frame = input1.get()
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
                    min_score_thresh=min_score_thresh,
                    agnostic_mode=False)

        input1.task_done()

        highest_prob = detections['detection_scores'][0]
        if highest_prob > min_score_thresh:
            object = detections['detection_classes'][0]
            try:
                playsound(f"{DATA_PATH}/sound/{labels[object]}.mp3" , block=False)
            except:
                pass

        output.put(image_np_with_detections)


def launchApp():
    global stop_threads
    global labels
    global min_score_thresh
    global blind_mode
    
    configs = load_config()

    if configs['blind_mode'] == 1:
        blind_mode = True
    else:
        blind_mode = False

    min_score_thresh = 0.5
    stop_threads = False
    labels = []

    global inputQ, outputQ
    inputQ = Queue()
    outputQ = Queue()

    MainApp().run()
    