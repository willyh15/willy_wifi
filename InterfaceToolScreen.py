from kivy.uix.screenmanager import Screen
from utils import get_interfaces, get_available_ssids

class InterfaceTool(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture_process = None
        self.selected_interface = None

    def on_interface_select(self, spinner, text):
        self.selected_interface = text
        self.refresh_ssids()

    def refresh_interfaces(self, instance):
        self.ids.interfaces_spinner.values = get_interfaces()

    def refresh_ssids(self, instance=None):
        if self.selected_interface:
            self.ids.ssid_spinner.values = get_available_ssids(self.selected_interface)

    def set_screen(self, screen_name):
        self.manager.current = screen_name
