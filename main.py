from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

# Import your screen classes
from interfacetoolscreen import InterfaceToolScreen
from pysharkscreen import PySharkScreen
from tsharkscreen import TSharkScreen
from ghostmodescreen import GhostModeScreen
from postexploitationscreen import PostExploitationScreen

class MainApp(MDApp):
    def build(self):
        # Create a ScreenManager
        sm = ScreenManager()

        # Add your screens
        sm.add_widget(InterfaceToolScreen(name='interfacetool'))
        sm.add_widget(PySharkScreen(name='pyshark'))
        sm.add_widget(TSharkScreen(name='tshark'))
        sm.add_widget(GhostModeScreen(name='ghostmode'))
        sm.add_widget(PostExploitationScreen(name='postexploitation'))

        return sm

    def on_start(self):
        # Any additional startup logic if needed
        pass

if __name__ == '__main__':
    MainApp().run()
