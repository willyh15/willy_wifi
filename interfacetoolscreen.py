from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.metrics import dp
from utils import get_available_ssids, get_interfaces

class InterfaceToolScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_interface = None
        self.interface_menu = None
        self.ssid_menu = None
        self.bind(on_kv_post=self.refresh_data)

    def on_enter(self, *args):
        Clock.schedule_once(self.refresh_data, 1)

    def refresh_data(self, instance, value):
        self.refresh_interfaces()

    def create_dropdown_menu(self, ref_input, data, selected_callback):
        menu_items = [{"text": item, "viewclass": "OneLineListItem",
                       "on_release": lambda x=item: selected_callback(x)} for item in data]
        return MDDropdownMenu(
            caller=self.ids[ref_input],
            items=menu_items,
            position="bottom",
            width_mult=4
        )

    def refresh_interfaces(self):
        interfaces = get_interfaces()
        self.interface_menu = self.create_dropdown_menu('interface_input', interfaces, self.set_selected_interface)

    def set_selected_interface(self, interface_name):
        self.ids.interface_input.text = interface_name
        self.selected_interface = interface_name
        self.interface_menu.dismiss()
        self.refresh_ssids()

    def refresh_ssids(self):
        if self.selected_interface:
            ssids = get_available_ssids(self.selected_interface)
            self.ssid_menu = self.create_dropdown_menu('ssid_input', ssids, self.set_selected_ssid)

    def set_selected_ssid(self, ssid_name):
        self.ids.ssid_input.text = ssid_name
        self.ssid_menu.dismiss()

    def show_interface_dropdown(self):
        if self.interface_menu:
            self.interface_menu.open()

    def show_ssid_dropdown(self):
        if self.ssid_menu:
            self.ssid_menu.open()
