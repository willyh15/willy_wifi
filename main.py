import os
import subprocess
from kivymd.app import MDApp
from interface_tools_screen import InterfaceToolScreen

def is_root():
    return os.geteuid() == 0

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.interface_tool_screen = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"
        self.interface_tool_screen = InterfaceToolScreen()
        return self.interface_tool_screen

    def on_start(self):
        if not is_root():
            self.prompt_for_privileges()

    def prompt_for_privileges(self):
        # Implement the privilege escalation prompt using pkexec
        command = ["pkexec", "python3", os.path.abspath(__file__)]
        subprocess.Popen(command)

if __name__ == '__main__':
    MyApp().run()
