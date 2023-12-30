from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.metrics import dp
import subprocess
import openai
import re

from utils import get_interfaces


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
            interfaces = self.get_interfaces()
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
                ssids = self.get_available_ssids(self.selected_interface)
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

    def validate_ip_address(ip_addr):
        # A basic regular expression for IP address validation
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}(-\d{1,3})?$')
        return ip_pattern.match(ip_addr) is not None

    # Function to list available network interfaces
    def get_interfaces(self):
        cmd = ["ip", "link", "show"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Failed to get interfaces:", result.stderr)
            return []
        interfaces = [line.split(":")[1].strip() for line in result.stdout.split('\n') if
                      'state' in line and not 'DOWN' in line]
        return interfaces

    # Function to scan for available SSIDs
    def get_available_ssids(interface):
        try:
            scan_results = subprocess.check_output(['iwlist', interface, 'scan'], text=True)
            ssids = re.findall(r'ESSID:"([^"]+)"', scan_results)
            return list(set(ssids))
        except subprocess.CalledProcessError as e:
            print("Error scanning for SSIDs:", e)
            return []

    # Function to analyze live packets
    def analyze_packet(self):
        pass

    def send_prompt_to_language_model(prompt):
        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=150
            )

            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error in querying the language model: {e}")
            return "Error in generating response."

