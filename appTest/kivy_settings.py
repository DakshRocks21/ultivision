#$# Written by Daksh #$#

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

KV = """
WindowManager:
    HomeScreen:
    SettingsScreen:

<HomeScreen>:
    name: 'home'
    MDScreen:
        orientation: 'vertical'
        MDLabel:
            text: 'Welcome to Our App!'
            font_style: 'H4'
            halign: 'center'
        MDFlatButton:
            text: 'Settings'
            md_bg_color: app.theme_cls.primary_light
            font_style: 'Subtitle1'
            pos_hint: {"center_x": 0.5, "center_y": 0.1}
            on_press: app.root.current = 'settings'

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

"""


class HomeScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        return Builder.load_string(KV)

    def changeText(self, word):
        text = self.root.get_screen("settings").ids.MyCoolID.text 
        if text == "You selected " + word:
            self.root.get_screen("settings").ids.MyCoolID.text = "Choose your preferred mode!"
        else:
            self.root.get_screen("settings").ids.MyCoolID.text = "You selected " + word
    
    def on_switch_active(self, switch, value):
        if value:
            print("Switch on")
        else:
            print("Switch off")

    def on_start(self):      
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Option1",
                "on_release": lambda *args: self.callback()
            }
        ]

        self.dropdown1 = MDDropdownMenu(items=menu_items, width_mult=4, caller=self.root.get_screen("settings").ids.button) 

    def on_stop(self):
        pass