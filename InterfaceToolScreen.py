from kivymd.uix.screen import MDScreen
from utils import get_interfaces, get_available_ssids

class InterfaceToolScreen(MDScreen):
    def __init__(self, **kwargs):
        super(InterfaceToolScreen, self).__init__(**kwargs)
        self.capture_process = None
        self.selected_interface = None

    def on_enter(self):
        # It's safe to call these methods here as the widgets have been loaded
        self.refresh_interfaces()
        self.refresh_ssids()

    def on_interface_select(self, spinner, text):
        self.selected_interface = text
        self.refresh_ssids()

    def refresh_interfaces(self):
        # Safeguard in case the spinner is not loaded yet
        if 'interfaces_spinner' in self.ids:
            self.ids.interfaces_spinner.values = get_interfaces()

    def refresh_ssids(self):
        # Update SSID spinner only if an interface is selected
        if self.selected_interface and 'ssid_spinner' in self.ids:
            self.ids.ssid_spinner.values = get_available_ssids(self.selected_interface)

    def set_screen(self, screen_name):
        # Change the current screen using the screen manager
        if self.manager:
            self.manager.current = screen_name
