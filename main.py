# main.py
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from GhostModeScreen import GhostModeScreen
from InterfaceToolScreen import InterfaceToolScreen
from NmapScreen import NmapScreen
from PostExploitationScreen import PostExploitationScreen
from PySharkScreen import PySharkScreen
from TSharkScreen import TSharkScreen

class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GhostModeScreen(name='ghostmode'))
        sm.add_widget(InterfaceToolScreen(name='interfacetool'))
        sm.add_widget(NmapScreen(name='nmap'))
        sm.add_widget(PostExploitationScreen(name='postexploit'))
        sm.add_widget(PySharkScreen(name='pyshark'))
        sm.add_widget(TSharkScreen(name='tshark'))
        return sm

if __name__ == '__main__':
    MyApp().run()
