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

## / TTS IMPORTS /##
import pyttsx3
import speech_recognition as sr

## / OTHER IMPORTS /##
import cv2
import numpy as np
import time
import os
import threading
import matplotlib.pyplot as plt
import io

## / KIVY UI /##

KIVY_CONFIG = '''
WindowManager:
    HomeScreen:
    SettingsScreen:
    CameraInitScreen:
    CameraScreen:


<HomeScreen>:
    name: 'home'
    MDScreen:
        orientation: 'vertical'
        MDLabel:
            text: 'Welcome to Our App!'
            font_style: 'H4'
            halign: 'center'
        MDTextButton:
            text: 'Settings'
            pos_hint: {"center_x": 0.5}
            on_release: root.manager.current = 'settings'

        MDTextButton:
            text: 'Exit'
            pos_hint: {"center_x": 0.3}

<SettingsScreen>:
    name: 'settings'
    MDScreen:
        orientation: 'vertical'
        MDLabel:
            id: MyCoolID
            text: "Please select a setting"
            font_style: 'H6'
            halign: 'center'
        MDFlatButton:
            text: 'Sound Map'
            pos_hint: {"center_x": 0.3, "center_y": 0.3}
            md_bg_color: app.theme_cls.primary_light
            on_release: app.changeText("Sound")
        MDFlatButton:
            text: 'Audible Reminders'
            pos_hint: {"center_x": 0.7, "center_y": 0.3}
            md_bg_color: app.theme_cls.primary_light
            on_release: app.changeText("Audible")

<CameraInitScreen>:
    name: 'camerainit'
    MDScreen:
        orientation: 'vertical'
        MDLabel:
            text: 'Are you ready to start the camera?'
            font_style: 'H4'
            halign: 'center'
        MDFlatButton:
            text: 'Start Camera NOW!'
            pos_hint: {"center_x": 0.5, "center_y": 0.3}
            md_bg_color: app.theme_cls.primary_light
            on_release: app.prestartcam()

<CameraScreen>:
    name: 'camera'
    MDScreen:
        id : camera
        orientation: 'vertical'
        MDLabel:
            text: 'Camera Page'
            font_style: 'H4'
            pos_hint: {"center_x": 0.5, "center_y": 0.9}
        MDFlatButton:
            text: 'Stop Camera'
            pos_hint: {"center_x": 0.3, "center_y": 0.1}
            md_bg_color: app.theme_cls.primary_light
            on_release: app.stopcam(status="camerastop")
        MDFlatButton:
            text: 'Save Image'
            pos_hint: {"center_x": 0.7, "center_y": 0.1}
            md_bg_color: app.theme_cls.primary_light
            on_release: app.saveImage()
        MDBoxLayout:
            id: layout
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height

'''

# Class's written by Daksh


class HomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class CameraInitScreen(Screen):
    pass


class CameraScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass

## / MAIN CODE /##


class MainApp(MDApp):


    def build(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1)

        self.r = sr.Recognizer()
        self.mic = sr.Microphone()


        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "300"
        self.CAMERA = 0
        self.oncam = False


        return Builder.load_string(KIVY_CONFIG)
    
    
    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
    
    def destroy_all(self):
        self.stopcam(status="destroy")
    
    def hook_keyboard(self, window, key, *largs):
        self.destroy_all()
        if key == 27:
            if self.root.current == 'home':
                return False
            self.root.current = 'home'
            return True
    
    def changeText(self, word):
        text = self.root.get_screen("settings").ids.MyCoolID.text
        if text == "You selected " + word:
            self.root.current = 'camerainit'
        else:
            self.root.get_screen(
                "settings").ids.MyCoolID.text = "You selected " + word
    
    def prestartcam(self):
        self.image = Image()  # create image here as startcam is in another thread
        self.root.get_screen('camera').ids.camera.add_widget(
            self.image)
        self.root.transition = NoTransition()
        self.root.current = 'camera'
        self.oncam = True
        threading.Thread(target=self.startcam).start()
    
    def startcam(self):
        print("cam started")
        self.capture = cv2.VideoCapture(
            int(self.CAMERA))  # select camera input
        # load camera view at 30 frames per second
        _,frame = self.capture.read()
        Clock.schedule_interval(self.loadVideo(frame), 1.0/30.0)
        self.oncam = True
    
    def saveImage(self):
        cv2.imwrite("image.png", self.image_frame)
    
    def generate_texture(self):
        """Generate random numpy array, plot it, save it, and convert to Texture."""
        
        # numpy array
        arr = np.random.randint(0, 100, size=10, dtype=np.uint8)
        
        # plot
        plt.clf() # remove previous plot
        plt.plot(arr)
        
        # save in memory
        data = io.BytesIO()
        plt.savefig(data)
        
        data.seek(0)  # move to the beginning of file
        
        return CoreImage(data, ext='png').texture
    
    def loadVideo(self, dt):
        ret, frame = self.capture.read()
        if ret:
            self.image_frame = frame
            buf = cv2.flip(self.image_frame, 0).tobytes()
            texture = Texture.create(size=(self.image_frame.shape[1], self.image_frame.shape[0]), colorfmt='bgr').blit_buffer(
                buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = self.generate_texture()
    
    def stopcam(self, status):
        self.oncam = False
        self.capture.release()
        cv2.destroyAllWindows()
        if status == "camerastop":
            self.root.transition = SlideTransition(direction="left")
            self.root.current = 'camerainit'
    
    def textToSpeech(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    
    def speechToText(self):
        with self.mic as source:
            audio = self.r.listen(source)
        try:
            text = self.r.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))

def launchApp():
    
    MainApp().run()  # start Kivy app
