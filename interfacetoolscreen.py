from kivymd.uix.screen import MDScreen
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from utils import get_interfaces, get_available_ssids
from kivy.uix.screenmanager import ScreenManager

sm = ScreenManager()
sm.current = 'interfacetool'

class InterfaceToolScreen(MDScreen):
    def __init__(self, **kwargs):
        super(InterfaceToolScreen, self).__init__(**kwargs)
        self.capture_process = None
        self.selected_interface = None

        # UI Components
        self.interfaces_spinner = MDSpinner()
        self.add_widget(self.interfaces_spinner)

        self.ssid_spinner = MDSpinner()
        self.add_widget(self.ssid_spinner)

        self.refresh_button = MDFlatButton(text="Refresh", on_release=self.refresh_data)
        self.add_widget(self.refresh_button)

        self.info_label = MDLabel()
        self.add_widget(self.info_label)

        # Refresh data on initialization
        self.refresh_data()

    def on_enter(self):
        self.refresh_data()

    def refresh_data(self, *args):
        self.refresh_interfaces()
        self.refresh_ssids()

    def refresh_interfaces(self):
        self.interfaces_spinner.values = get_interfaces()

    def refresh_ssids(self):
        if self.selected_interface:
            self.ssid_spinner.values = get_available_ssids(self.selected_interface)

    def set_screen(self, screen_name):
        if self.manager:
            self.manager.current = screen_name
