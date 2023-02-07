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

##/ UTILS IMPORTS /##
from MainApp.utils.config import load_config

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
            font_style: 'Subtitle1' 
            pos_hint: {"center_x": 0.5, "center_y": 0.1}
            on_press: root.manager.current = 'settings'
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
<CameraInitScreen>:
    name: 'camerainit'
    MDScreen:
        orientation: 'vertical'
        MDLabel:
            text: 'Camera'
            font_style: 'H4'
            halign: 'center'
        MDFlatButton:
            text: 'Start Camera'
            pos_hint: {"center_x": 0.5, "center_y": 0.3}
            md_bg_color: app.theme_cls.primary_light
            on_press: app.startcam()
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
            text: 'Stop Camera'
            pos_hint: {"center_x": 0.3, "center_y": 0.1}
            md_bg_color: app.theme_cls.primary_light
            on_press: app.stopcam()
        MDFlatButton:
            text: 'Save Image'
            pos_hint: {"center_x": 0.7, "center_y": 0.1}
            md_bg_color: app.theme_cls.primary_light
            on_press: app.saveImage()
        
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
        self.config = load_config()

        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', self.config['tts']['rate'])
        self.engine.setProperty('volume', self.config['tts']['volume'])

        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

        self.config = load_config()

        self.theme_cls.theme_style = self.config['theme']['style']
        self.theme_cls.primary_palette = self.config['theme']['palette']
        self.theme_cls.primary_hue = self.config['theme']['hue']
        self.CAMERA = self.config['camera']['number']
        self.oncam = False


        return Builder.load_string(KIVY_CONFIG)
    

    def changeText(self, word):
        text = self.root.get_screen("settings").ids.MyCoolID.text 
        if text == "You selected " + word:
            self.root.current = 'camerainit'
        else:
            self.root.get_screen("settings").ids.MyCoolID.text = "You selected " + word

    def on_stop(self):
        if self.oncam:
            self.stopcam()
        self.engine.stop()
        self.engine.runAndWait()


    def startcam(self):
        self.image = Image()  # create image here as startcam is in another thread
        self.root.get_screen('camera').ids.layout.add_widget(self.image)
        self.root.transition = NoTransition()
        self.root.current = 'camera'
        self.oncam = True
        print("cam started")
        self.capture = cv2.VideoCapture(
            int(self.CAMERA))  # select camera input
        # load camera view at 30 frames per second
        Clock.schedule_interval(self.loadVideo, 1.0/30.0)
    
    def saveImage(self):
        cv2.imwrite("image.png", self.image_frame)

    
    def loadVideo(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        self.image_frame = frame
        if ret:
            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.image.texture = texture

    def stopcam(self):
        self.oncam = False
        self.capture.release()
        self.root.get_screen('camera').ids.layout.remove_widget(self.image)
        cv2.destroyAllWindows()
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