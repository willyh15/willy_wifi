import socket
import os
import sys
import time
import subprocess
from threading import Thread

from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from interface_manager import get_interfaces
from kivymd.app import MDApp
from kivy.lang import Builder

KV = '''
InterfaceToolScreen:
'''

class InterfaceToolScreen(BoxLayout):
    root_interface = StringProperty('Select Interface')
    available_interfaces = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.init_interfaces()

        label = Label(text='Select an Interface', size_hint_y=None, height=48, color=(0, 0, 0, 1))
        self.add_widget(label)

        self.interface_button = Button(text='Select Interface', size_hint_x=0.5)
        self.interface_button.bind(on_release=self.open_interface_dropdown)
        self.add_widget(self.interface_button)

        self.interface_dropdown = None  # Initialize the dropdown here

        submit_button = Button(text='Submit', size_hint=(None, None), size=(200, 48), pos_hint={'center_x': 0.5})
        submit_button.bind(on_release=self.submit_request)
        self.add_widget(submit_button)

    def init_interfaces(self):
        interfaces = get_interfaces()
        if interfaces:
            self.available_interfaces = interfaces

    def open_interface_dropdown(self, instance):
        if not self.interface_dropdown:
            self.interface_dropdown = DropDown()
            for interface in self.available_interfaces:
                btn = Button(text=interface, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn_instance, x=interface: self.select_interface(x))
                self.interface_dropdown.add_widget(btn)
            self.interface_dropdown.open(self.interface_button)

    def select_interface(self, interface):
        self.root_interface = interface
        self.interface_button.text = interface
        self.interface_dropdown.dismiss()

    def submit_request(self, instance):
        # Here you can implement the logic to send the request to the backend
        command = "Your_Command_Here"
        response = self.send_request_to_backend(command)
        # Display the response or handle it as needed
        self.show_response_popup(response)

    def send_request_to_backend(self, command):
        # Implement your logic to send the request to the backend here
        pass

    def show_response_popup(self, response):
        # Implement a popup to display the response here
        pass

class MyApp(MDApp):
    def build(self):
        if not self.wait_for_server_ready("/tmp/backend_socket"):
            print("Backend server did not start in time. Exiting.")
            sys.exit(1)
        return InterfaceToolScreen()

    def set_active_interface(self, interface):
        self.root_interface = interface
        print(f"Active interface set to: {self.root_interface}")

    def wait_for_server_ready(self, server_address, attempts=5, delay=1):
        for _ in range(attempts):
            try:
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as test_socket:
                    test_socket.connect(server_address)
                    return True
            except FileNotFoundError:
                time.sleep(delay)
        return False

def start_backend_server():
    server_script = './backend.py'
    subprocess.Popen(['python3', server_script])
    time.sleep(2)

if __name__ == '__main__':
    print("Starting script...")
    if os.geteuid() != 0:
        print("Not running as root, launching terminal...")
        terminal_command = "gnome-terminal -- /bin/bash -c 'sudo /home/ufo/PycharmProjects/willy_wifi/venv/bin/python3 " + " ".join(
            sys.argv) + "; echo Press enter to continue; read'"
        os.system(terminal_command)
        sys.exit(0)
    else:
        print("Running as root, launching app...")
        start_backend_server()
        MyApp().run()
