# main.py
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
# Import your screens here

class MyApp(MDApp):
    sm = ScreenManager()
if __name__ == '__main__':
    MyApp().run()
