import traceback
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from interfacetoolscreen import InterfaceToolScreen
from pysharkscreen import PySharkScreen
from tsharkscreen import TSharkScreen
from ghostmodescreen import GhostModeScreen
from postexploitationscreen import PostExploitationScreen

KV_FILE_SUFFIX = '.kv'
SCREEN_CONTAINER = {
    'interface_tool': InterfaceToolScreen,
    'py_shark': PySharkScreen,
    't_shark': TSharkScreen,
    'ghost_mode': GhostModeScreen,
    'post_exploitation': PostExploitationScreen
}


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.sm = MDScreenManager()

    def build(self):
        self.configure_window()
        self.load_kv_files()
        self.add_screens()
        return self.sm

    def configure_window(self):
        Window.size = (360, 640)
        Config.set('graphics', 'width', '360')
        Config.set('graphics', 'height', '640')

    def load_kv_files(self):
        for screen in SCREEN_CONTAINER.keys():
            try:
                Builder.load_file(f'{screen}{KV_FILE_SUFFIX}')
            except FileNotFoundError:
                print(f"{screen}{KV_FILE_SUFFIX} not found.")
            except Exception as e:
                print(f"Error loading {screen}{KV_FILE_SUFFIX} : {str(e)}, {traceback.format_exc()}")

    def add_screens(self):
        for screen, screen_class in SCREEN_CONTAINER.items():
            try:
                self.sm.add_widget(screen_class(name=f'{screen}{KV_FILE_SUFFIX}'))
            except Exception as e:
                print(f"Error adding {screen} : {str(e)}, {traceback.format_exc()}")

    def on_start(self):
        # Any additional startup logic if needed
        pass


    def on_stop(self):
        # Any cleanup logic if needed
        pass

if __name__ == '__main__':
    try:
        MainApp().run()
    except Exception as e:
        print(f"Application exited with error: {str(e)}, {traceback.format_exc()}")
        # Optionally, exit with a non-zero error code
        # sys.exit(1)