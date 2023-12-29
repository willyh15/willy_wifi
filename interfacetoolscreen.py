from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from utils import get_interfaces, get_available_ssids
from kivy.metrics import dp

class InterfaceToolScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_interface = None
        self.interface_menu = None
        self.ssid_menu = None

    def on_kv_post(self, base_widget):
        # Refresh data after the kv rules have been applied
        self.refresh_data()

    def refresh_data(self, *args):
        # Refresh interface and SSID dropdowns
        self.refresh_interfaces()
        self.refresh_ssids()

    def refresh_interfaces(self):
        interfaces = get_interfaces()
        menu_items = [{"text": iface, "viewclass": "OneLineListItem",
                       "on_release": lambda x=iface: self.set_interface(x)} for iface in interfaces]
        self.interface_menu = MDDropdownMenu(
            caller=self.ids.interface_input,
            items=menu_items,
            position="bottom",
            width_mult=4
        )

    def set_interface(self, interface_name):
        self.ids.interface_input.text = interface_name
        self.selected_interface = interface_name
        self.interface_menu.dismiss()
        self.refresh_ssids()

    def refresh_ssids(self):
        if self.selected_interface:
            ssids = get_available_ssids(self.selected_interface)
            menu_items = [{"text": ssid, "viewclass": "OneLineListItem",
                           "on_release": lambda x=ssid: self.set_ssid(x)} for ssid in ssids]
            self.ssid_menu = MDDropdownMenu(
                caller=self.ids.ssid_input,
                items=menu_items,
                position="bottom",
                width_mult=4
            )

    def set_ssid(self, ssid_name):
        self.ids.ssid_input.text = ssid_name
        self.ssid_menu.dismiss()

    def show_interface_dropdown(self):
        # Open interface dropdown menu
        if self.interface_menu:
            self.interface_menu.open()

    def show_ssid_dropdown(self):
        # Open SSID dropdown menu
        if self.ssid_menu:
            self.ssid_menu.open()
