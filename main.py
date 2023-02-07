##/ KIVY IMPORTS /##
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition, SlideTransition
from kivy.graphics.texture import Texture

##/ TTS IMPORTS /##
import pyttsx3
import speech_recognition as sr

##/ OTHER IMPORTS /##
import cv2
import numpy as np
import time
import os
import threading




##/ KIVY UI /##
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
            on_press: root.manager.current = 'settings'

<SettingsScreen>:
    name: 'settings'
    MDScreen:
        orientation: 'vertical'
        MDFillRoundFlatIconButton:
            icon: "back"
            text: "Back"
            pos_hint: {"center_x": 0.1, "center_y": 0.9}
            font_style: 'Caption'
            text_color: 1, 1, 1, 1
            border_color: 0, 0, 0, 0
        MDLabel:
            text: "Settings"
            pos_hint: {"center_x": 0.5, "center_y": 0.9}
            font_style: 'H5'
            halign: 'center'
        MDLabel:
            id: MyCoolID
            text: "Choose your preferred mode!"
            pos_hint: {"center_x": 0.5, "center_y": 0.7}
            font_style: 'H4'
            halign: 'center'
        MDFlatButton:
            text: 'Sound Map'
            pos_hint: {"center_x": 0.3, "center_y": 0.3}
            size_hint: 0.35, 0.45
            md_bg_color: app.theme_cls.primary_light
            on_press: app.changeText("Sound")
        MDFlatButton:
            text: 'Audible Reminders'
            pos_hint: {"center_x": 0.7, "center_y": 0.3}
            size_hint: 0.35, 0.45
            md_bg_color: app.theme_cls.primary_light
            on_press: app.changeText("Audible")

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
            on_press: app.prestartcam()

<CameraScreen>:
    name: 'camera'
    MDScreen:
        orientation: 'vertical'
        MDLabel:
            text: 'Camera Page'
            font_style: 'H4'
            pos_hint: {"center_x": 0.5, "center_y": 0.9}
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
        MDBoxLayout:
            id: layout
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height

'''


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

##/ MAIN CODE /##
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "300"
        self.CAMERA = 0
        self.oncam = False

        return Builder.load_string(KIVY_CONFIG)

    def changeText(self, word):
        text = self.root.get_screen("settings").ids.MyCoolID.text
        if text == "You selected " + word:
            self.root.current = 'camerainit'
        else:
            self.root.get_screen("settings").ids.MyCoolID.text = "You selected " + word

    def prestartcam(self):
        self.root.transition = NoTransition()
        self.root.current = 'camera'
        if self.oncam == True:
            self.oncam = False
            self.stopcam()
        self.startcam()
        if self.oncam == False:
            self.oncam = True
            self.startcam()    

    def startcam(self):
        self.image = Image() #Initialize image
        print("cam started") 
        self.capture = cv2.VideoCapture(int(self.CAMERA)) #select camera input
        Clock.schedule_interval(self.loadVideo, 1.0/30.0) #load camera view at 30 frames per second
        self.root.get_screen('camera').ids.layout.add_widget(self.image) #add image view to camera page
        self.oncam = True

    def saveImage(self):
        cv2.imwrite("image.png", self.image_frame)

    def loadVideo(self, dt):
        ret, frame = self.capture.read()
        
        self.image_frame = frame

        buf1 = cv2.flip(frame, 0)
        buf = buf1.tobytes()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture1

    def stopcam(self):
        self.oncam = False
        self.capture.release()
        cv2.destroyAllWindows()
        self.root.transition = SlideTransition(direction="left")
        self.root.current = 'camerainit'

    def textToSpeech(self, text):
        engine.say(text)
        engine.runAndWait()

    def speechToText(self):
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == '__main__':
    engine = pyttsx3.init() # start TTS engine
    #r = sr.Recognizer()
    MainApp().run() # start Kivy app
