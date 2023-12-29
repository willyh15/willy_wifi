from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder

from interfacetoolscreen import InterfaceToolScreen
from pysharkscreen import PySharkScreen
from tsharkscreen import TSharkScreen
from ghostmodescreen import GhostModeScreen
from postexploitationscreen import PostExploitationScreen

from kivy.core.window import Window
Window.size = (360, 640)

from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.sm = MDScreenManager()

        self.sm.current = 'interfacetool'


    def build(self):
        self.load_kv_files()
        self.add_screens()
        return self.sm

    def load_kv_files(self):
        kv_files = ['interfacetool', 'pyshark', 'tshark', 'ghostmode', 'postexploitation']
        for file in kv_files:
            try:
                Builder.load_file(f'{file}.kv')
            except Exception as e:
                print(f"Error loading {file}.kv : {str(e)}")

    def add_screens(self):
        screens = [
            InterfaceToolScreen(name='interfacetool'),
            PySharkScreen(name='pyshark'),
            TSharkScreen(name='tshark'),
            GhostModeScreen(name='ghostmode'),
            PostExploitationScreen(name='postexploitation')
        ]
        for screen in screens:
            try:
                self.sm.add_widget(screen)
            except Exception as e:
                print(f"Error adding {screen.name} : {str(e)}")

    def on_start(self):
        # Any additional startup logic if needed
        pass


if __name__ == '__main__':
    MainApp().run()
