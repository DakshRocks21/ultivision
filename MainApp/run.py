
##/ KIVY IMPORTS /##
from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '1000')
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '800')

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


##/ TTS IMPORTS /##
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

##/ OTHER IMPORTS /##
import cv2
import numpy as np
import threading
from queue import Queue
import sys

##/ KIVY UI /##
#$# Written by Daksh and Richard #$#


KV = """
WindowManager:
    HomeScreen:
    SettingsScreen:
    CameraScreen:

<HomeScreen>:
    name: 'home'
    MDScreen:
        orientation: 'vertical'
        MDLabel:
            id: header
            text: 'Welcome to Our App!'
            font_style: 'H4' 
            halign: 'center'
        MDFlatButton:
            id: start_button
            text: 'Start'
            md_bg_color: app.theme_cls.primary_light
            font_style: 'Subtitle1' 
            pos_hint: {"center_x": 0.5, "center_y": 0.1}
            on_press: app.startcam()
<SettingsScreen>:
    name: 'settings'
    MDScreen:
        orientation: 'vertical'
        MDLabel:
            text: "Sound Library"
            pos_hint: {"center_x": 0.5, "center_y": 0.95}
            font_style: 'H5'
            halign: 'center'
        MDLabel:
            text: "Press any button to hear their respective audio files!"
            pos_hint: {"center_x": 0.5, "center_y": 0.90}
            font_style: 'H6'
            halign: 'center'
        MDFlatButton:
            text: 'Person'
            pos_hint: {"center_x": 0.30, "center_y": 0.800}
            size_hint: 0.30, 0.075
            md_bg_color: app.theme_cls.primary_light
            on_press: app.playAudio('person')
        MDFlatButton:
            text: 'Door'
            pos_hint: {"center_x": 0.30, "center_y": 0.705}
            size_hint: 0.30, 0.075
            md_bg_color: app.theme_cls.primary_light
            on_press: app.playAudio('door')
        MDFlatButton:
            text: 'Cat'
            pos_hint: {"center_x": 0.30, "center_y": 0.610}
            size_hint: 0.30, 0.075
            md_bg_color: app.theme_cls.primary_light
            on_press: app.playAudio('cat')
        MDFlatButton:
            text: 'Dog'
            pos_hint: {"center_x": 0.30, "center_y": 0.515}
            size_hint: 0.30, 0.075
            md_bg_color: app.theme_cls.primary_light
            on_press: app.playAudio('dog')
        MDFlatButton:
            text: 'Car'
            pos_hint: {"center_x": 0.30, "center_y": 0.420}
            size_hint: 0.30, 0.075
            md_bg_color: app.theme_cls.primary_light
            on_press: app.playAudio('car')
        MDFlatButton:
            text: 'Bus'
            pos_hint: {"center_x": 0.30, "center_y": 0.325}
            size_hint: 0.30, 0.075
            md_bg_color: app.theme_cls.primary_light
            on_press: app.playAudio('bus')
        MDFlatButton:
            text: 'Bicycle'
            pos_hint: {"center_x": 0.30, "center_y": 0.230}
            size_hint: 0.30, 0.075
            md_bg_color: app.theme_cls.primary_light
            on_press: app.playAudio('bicycle')
        MDFlatButton:
            text: 'Truck'
            pos_hint: {"center_x": 0.30, "center_y": 0.135}
            size_hint: 0.30, 0.075
            md_bg_color: app.theme_cls.primary_light
            on_press: app.playAudio('truck')
        MDFlatButton:
            text: 'Back to Settings'
            pos_hint: {"center_x": 0.70, "center_y": 0.2}
            size_hint: 0.30, 0.1
            md_bg_color: app.theme_cls.primary_light
            on_press: app.settingToCam()
        MDLabel:
            text: "Blind Mode"
            pos_hint: {"center_x": 0.7, "center_y": 0.70}
            font_style: 'H6'
            halign: 'center'
        MDLabel:
            text: "Toggle this to skip directly to Camera upon next launch!"
            pos_hint: {"center_x": 0.7, "center_y": 0.65}
            font_style: 'Caption'
            halign: 'center'
        MDSwitch:
            id: switch
            pos_hint: {'center_x': 0.7, 'center_y': .6}
            on_active: app.on_switch_active(*args)
        MDRectangleFlatIconButton:
            id: button
            text: "Camera Switcher"
            icon: "language-python"
            pos_hint: {"center_x": 0.7, "center_y": .4}
            size_hint: 0.30, 0.1
            on_release: app.dropdown1.open()

<CameraScreen>:
    name: 'camera'
    MDScreen:
        orientation: 'vertical'
        MDLabel:
            text: 'Camera Page'
            font_style: 'H4'
            halign: 'center'
            pos_hint: {"center_x": 0.5, "center_y": 0.9}
            size_hint: 0.8, 0.1
        BoxLayout:
            id: layout
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint: 0.8, 0.8
        MDFlatButton:
            text: 'Settings'
            pos_hint: {"center_x": 0.30, "center_y": 0.1}
            size_hint: 0.3, 0.1
            md_bg_color: app.theme_cls.primary_light
            on_press: app.open_settings()
        MDFlatButton:
            text: 'Exit'
            pos_hint: {"center_x": 0.70, "center_y": 0.1}
            size_hint: 0.3, 0.1
            md_bg_color: app.theme_cls.primary_light
            on_press: app.stopcam(True)
"""

#$# Written by Daksh #$#
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


##/ MainApp (KIVY) /##
#$# Written by Daksh #$#
class MainApp(MDApp):

    ### Kivy Build/Start/Stop Functions ###
    def build(self):        
        self.tensorflowThread = threading.Thread(target=tensorflow, args=(inputQ, outputQ))
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

    def on_start(self):
        """
        Kivy function
        Check if the app is in blind mode, if so, switch to camera screen
        """
        if self.json_config['blind_mode'] == 1:
            self.root.get_screen("settings").ids.switch.active = True
            # switch to camera screen
            self.startcam()
    
    def on_stop(self):
        """
        Kivy function
        Stop the camera and the tensorflow thread when then app is closed
        """
        stop_threads = True

        exit_event.set()

        if self.oncam:
            self.stopcam(0)
        
        self.tensorflowThread.join()
        # TODO : 


    ### Misc Functions ###
    def get_labels(self):
        """
        Get the labels from the labelmap file
        - to be used for the sound map
        """
        self.category_index = label_map_util.create_category_index_from_labelmap(LABELMAP_FILENAME_PATH, use_display_name=True)
        for key, value in self.category_index.items():
            labels.append(value["name"].lower())

    def playAudio(self, name):
        """
        Play the audio file
        """
        try:
            playsound(f"{DATA_PATH}/sound/{name}.mp3")
        except:
            pass
 
    ### SETTINGS SCREEN ###
    def open_settings(self):
        """
        Open the settings screen, stop the camera, remove the Image() and create the dropdown menu
        """
        self.root.transition = SlideTransition(direction="left")
        self.root.current = 'settings'
        # remove the loadvideo clock
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
        """
        Select the camera that was passed in
        """
        print("Camera " + str(i) + " selected")
        self.CAMERA = int(i)
        self.dropdown1.dismiss()

    def settingToCam(self):
        self.startcam()
    
    def on_switch_active(self, switch, value):
        """
        Switch between blind mode and normal mode
        """
        if value:
            change_config(1, "blind_mode")
        else:
            change_config(0, "blind_mode")



    ### CAMERA FUNCTIONS ###
    def startcam(self):
        """
        Start the camera and display the video on the screen
        1. Transition to the loading screen
        2. Start the camera
        3. Schedule the loadVideo function to run every 1/30 seconds
        4. Transition to the camera screen
        """
        self.root.current = 'home'
        self.root.get_screen('home').ids.header.text = "Loading..."
        # hide the start button
        self.root.get_screen('home').ids.start_button.opacity = 0
        self.capture = cv2.VideoCapture(int(self.CAMERA))
        self.oncam = True
        self.root.get_screen('camera').ids.layout.add_widget(self.image)
        Clock.schedule_interval(self.loadVideo, 1.0/30.0)
        self.root.transition = SlideTransition(direction="left")
        self.root.current = 'camera'

    def stopcam(self, condition):
        """
        Stop the camera and remove the image widget from the screen
        if condition is true, then it will go back to the home screen
        """
        self.oncam = False
        Clock.unschedule(self.loadVideo)
        inputQ.put(None)
        self.capture.release()
        self.root.get_screen('camera').ids.layout.remove_widget(self.image)
        if condition:
            self.root.transition = SlideTransition(direction="right")
            self.root.current = 'home'
            self.root.get_screen('home').ids.header.text = "Welcome to our app!"
            self.root.get_screen('home').ids.start_button.opacity = 100
    


    ### VIDEO RENDERING FUNCTIONS ###
    def loadVideo(self, dt):
        """
        Load the video from the camera and display it on the screen
        """
        if self.oncam and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                outputQ.put(frame)
                new_frame = inputQ.get()
                if new_frame is None:
                    return
                else:
                    buf = cv2.flip(new_frame, 0).tostring()
                    texture = Texture.create(size=(new_frame.shape[1], new_frame.shape[0]), colorfmt='bgr') 
                    texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                    self.image.texture = texture
                    inputQ.task_done()


##/  TENSORFLOW FUNCTIONS /##
#$# Written by Daksh #$#
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
        if frame is None:
            input1.task_done()
            outputQ.put(None)
        else:
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


            highest_prob = detections['detection_scores'][0]
            if highest_prob > min_score_thresh:
                object = detections['detection_classes'][0]
                try:
                    playsound(f"{DATA_PATH}/sound/{labels[object]}.mp3" , block=False)
                except:
                    pass
            input1.task_done()

            output.put(image_np_with_detections) 

##/  Start App /##
#$# Written by Daksh #$#
def launchApp():

    global exit_event
    exit_event = threading.Event()

    global blind_mode
    configs = load_config()
    if configs['blind_mode'] == 1:
        blind_mode = True
    else:
        blind_mode = False

    global min_score_thresh
    min_score_thresh = 0.5
    
    global stop_threads
    stop_threads = False
    
    global labels
    labels = []

    global inputQ, outputQ
    inputQ = Queue()
    outputQ = Queue()
    # hide all tensorflow errors

    MainApp().run()
    