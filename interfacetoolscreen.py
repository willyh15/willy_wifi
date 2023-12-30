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
        Clock.schedule_once(lambda dt: self.refresh_interfaces())

    def on_enter(self, *args):
        Clock.schedule_once(self.refresh_data, 1)

    def refresh_data(self, instance, value=None):
        try:
            self.refresh_interfaces()
        except Exception as e:
            print(f"An error occurred while refreshing the data: {e}")
            return

    def create_dropdown_menu(self, ref_input, data, selected_callback):
        menu_items = [{"text": item, "viewclass": "OneLineListItem",
                       "on_release": lambda x=item: selected_callback(x)} for item in data]
        try:
            caller_item = self.ids[ref_input]
        except KeyError as e:
            print(f"An error occurred accessing id {ref_input}: {e}")
            return None

        return MDDropdownMenu(
            caller=caller_item,
            items=menu_items,
            position="bottom",
            width_mult=4
        )

    def refresh_interfaces(self):
        try:
            interfaces = get_interfaces()
        except Exception as e:
            print(f"An error occurred while getting interfaces: {e}")
            return

        self.interface_menu = self.create_dropdown_menu('interface_input', interfaces, self.set_selected_interface)

    def set_selected_interface(self, interface_name):
        try:
            self.ids.interface_input.text = interface_name
        except KeyError as e:
            print(f"An error occurred accessing id 'interface_input': {e}")
            return

        self.selected_interface = interface_name
        self.interface_menu.dismiss()
        self.refresh_ssids()

    def refresh_ssids(self):
        if self.selected_interface:
            try:
                ssids = get_available_ssids(self.selected_interface)
            except Exception as e:
                print(f"An error occurred while getting SSIDs: {e}")
                return

            self.ssid_menu = self.create_dropdown_menu('ssid_input', ssids, self.set_selected_ssid)

    def set_selected_ssid(self, ssid_name):
        try:
            self.ids.ssid_input.text = ssid_name
        except KeyError as e:
            print(f"An error occurred accessing id 'ssid_input': {e}")
            return

        self.ssid_menu.dismiss()

    def show_interface_dropdown(self):
        if self.interface_menu:
            self.interface_menu.open()

    def show_ssid_dropdown(self):
        if self.ssid_menu:
            self.ssid_menu.open()
