from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


KIVY_CONFIG = '''
ScreenManager:
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
        MDTextButton:
            text: 'Settings'
            pos_hint: {"center_x": 0.5}
            on_press: root.manager.current = 'settings'

<SettingsScreen>:
    name: 'settings'
    MDScreen:
        orientation: 'vertical'
        MDLabel:
            id: MyCoolID
            text: "Hi"
            font_style: 'H6'
            halign: 'center'
        MDFlatButton:
            text: 'Sound Map'
            pos_hint: {"center_x": 0.5, "center_y": 0.9}
            md_bg_color: app.theme_cls.primary_light
            on_press: app.changeText("Sound")
        MDFlatButton:
            text: 'Audible Reminders'
            color: "#FF346"
            pos_hint: {"center_x": 0.5, "center_y": 0.8}
            md_bg_color: app.theme_cls.primary_light
            on_press: app.changeText("Audible")
'''


class HomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "300"

        return Builder.load_string(KIVY_CONFIG)

    def changeText(self, text):
        self.root.get_screen("settings").ids.MyCoolID.text = text


if __name__ == '__main__':
    MainApp().run()
