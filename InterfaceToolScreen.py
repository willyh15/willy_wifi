from kivymd.uix.screen import MDScreen
from utils import get_interfaces, get_available_ssids
from kivy.uix.screenmanager import ScreenManager, Screen

sm = ScreenManager()

sm.current = 'interfacetool'
class InterfaceToolScreen(MDScreen):
    def __init__(self, **kwargs):
        super(InterfaceToolScreen, self).__init__(**kwargs)
        self.capture_process = None
        self.selected_interface = None

    def on_enter(self):
        self.refresh_interfaces()
        self.refresh_ssids()

    def on_interface_select(self, spinner, text):
        self.selected_interface = text
        self.refresh_ssids()

    def refresh_interfaces(self):
        if 'interfaces_spinner' in self.ids:
            self.ids.interfaces_spinner.values = get_interfaces()

    def refresh_ssids(self):
        if self.selected_interface and 'ssid_spinner' in self.ids:
            self.ids.ssid_spinner.values = get_available_ssids(self.selected_interface)

    def set_screen(self, screen_name):
        if self.manager:
            self.manager.current = screen_name
