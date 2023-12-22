from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from GhostModeScreen import GhostModeScreen
from InterfaceToolScreen import InterfaceToolScreen
from NmapScreen import NmapScreen
from PostExploitationScreen import PostExploitationScreen
from PySharkScreen import PySharkScreen
from TSharkScreen import TSharkScreen
# import other necessary modules...

class MyApp(App):
    def build(self):
        # Load KV files
        Builder.load_file('GhostModeScreen.kv')
        Builder.load_file('InterfaceToolScreen.kv')
        Builder.load_file('NmapScreen.kv')
        Builder.load_file('PostExploitationScreen.kv')
        Builder.load_file('PySharkScreen.kv')
        Builder.load_file('TSharkScreen.kv')
        # Load other KV files if any...

        # Initialize the screen manager
        sm = ScreenManager()
        sm.add_widget(GhostModeScreen(name='ghostmode'))
        sm.add_widget(InterfaceToolScreen(name='interfacetool'))
        sm.add_widget(NmapScreen(name='nmap'))
        sm.add_widget(PostExploitationScreen(name='postexploit'))
        sm.add_widget(PySharkScreen(name='pyshark'))
        sm.add_widget(TSharkScreen(name='tshark'))
        # Add other screens to the manager...

        return sm

if __name__ == '__main__':
    MyApp().run()
