import subprocess
import re

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton

class CustomDropDown(MDRaisedButton):
    menu = None

    def show_dropdown(self, button):
        if not self.menu:
            self.menu = MDDropdownMenu(
                caller=button,
                items=[{"text": f"Interface {i}"} for i in range(5)],  # Replace with actual interface names
                width_mult=4,
            )
            self.menu.bind(on_release=self.set_item)

        self.menu.open()

    def set_item(self, instance_menu, instance_menu_item):
        def set_item(interval):
            self.text = instance_menu_item.text
            instance_menu.dismiss()
        Clock.schedule_once(set_item)

def run_sudo_command(command):
    app = MDApp.get_running_app()
    password = app.sudo_password
    full_command = f'echo {subprocess.list2cmdline([password])} | sudo -S {command}'
    process = subprocess.Popen(
        full_command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print(stdout)  # Handle the command output
    else:
        print(stderr)  # Handle the command error


def get_available_ssids(interface):
    try:
        scan_results = subprocess.check_output(['iwlist', interface, 'scan'], text=True)
        ssids = re.findall(r'ESSID:"([^"]+)"', scan_results)
        return list(set(ssids))
    except subprocess.CalledProcessError as e:
        print("Error scanning for SSIDs:", e)
        return []


class InterfaceToolScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_interface = None
        self.interface_menu = None
        self.ssid_menu = None
        Clock.schedule_once(lambda dt: self.refresh_interfaces())

    Builder.load_file('interface_tool_screen.kv')
    def get_interfaces(self):
        cmd = ["ip", "link", "show"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Failed to get interfaces:", result.stderr)
            return []
        interfaces = [line.split(":")[1].strip().split(' ')[0] for line in result.stdout.split('\n') if
                      'state' in line and not 'DOWN' in line]
        # split(' ')[0] is added to only get the interface name before the colon
        return interfaces

    def on_enter(self, *args):
        Clock.schedule_once(self.refresh_data, 1)

    def refresh_data(self, _):
        self.refresh_interfaces()

    def create_dropdown_menu(self, ref_input, data, selected_callback):
        menu_items = [{"text": item, "viewclass": "OneLineListItem",
                       "on_release": lambda x=item: selected_callback(x)} for item in data]
        caller_item = self.ids[ref_input]
        return MDDropdownMenu(
            caller=caller_item,
            items=menu_items,
            position="bottom",
            width_mult=4
        )

    def refresh_interfaces(self):
        interfaces = self.get_interfaces()  # This should return an iterable
        if interfaces and isinstance(interfaces, (list, tuple)):
            self.interface_menu = self.create_dropdown_menu('interface_input', interfaces, self.set_selected_interface)
        else:
            print("get_interfaces did not return an iterable")

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

