from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.switch import MDSwitch
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
import subprocess
from threading import Thread
from utils import get_interfaces, analyze_packet, send_prompt_to_language_model
from kivy.clock import Clock

class TSharkScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.interfaces_spinner = MDSpinner()
        self.filter_input = MDTextField()
        self.monitor_mode_switch = MDSwitch()
        self.destination_ip_input = MDTextField()
        self.payload_input = MDTextField()
        self.language_model_input = MDTextField()
        self.packet_display = MDLabel()
        self.stats_display = MDLabel()
        self.model_advice_display = MDLabel()
        self.setup_ui()

    def setup_ui(self):
        # Set up your UI elements here
        self.add_widget(self.interfaces_spinner)
        self.add_widget(self.filter_input)
        self.add_widget(self.monitor_mode_switch)
        self.add_widget(MDRaisedButton(text="Start Capture", on_release=self.start_capture))
        self.add_widget(MDRaisedButton(text="Apply Filter", on_release=self.apply_filter))
        self.add_widget(MDRaisedButton(text="Save Capture", on_release=self.save_capture))
        self.add_widget(self.destination_ip_input)
        self.add_widget(self.payload_input)
        self.add_widget(MDRaisedButton(text="Send Packet", on_release=self.craft_and_send_packet))
        self.add_widget(self.language_model_input)
        self.add_widget(MDRaisedButton(text="Query Language Model", on_release=self.query_language_model))
        self.add_widget(self.packet_display)
        self.add_widget(self.stats_display)
        self.add_widget(self.model_advice_display)

    def apply_filter(self, instance):
        self.start_capture(None, self.filter_input.text)

    def save_capture(self, instance):
        self.start_capture(None, self.filter_input.text, save=True)

    def start_capture(self, instance, filter_string='', save=False):
        interface = self.interfaces_spinner.text
        monitor_mode = self.monitor_mode_switch.active
        self.run_tshark(interface, monitor_mode, filter_string, save)
        self.live_analysis = True  # Flag to indicate if live analysis should be done

    def read_from_process(self):
        while True:
            line = self.capture_process.stdout.readline()
            if line != '':
                if self.live_analysis:
                    self.analyze_live_packet(line)
                Clock.schedule_once(lambda dt: self.update_display(line), 0)
            else:
                break

    def analyze_live_packet(self, packet_data):
        stats = analyze_packet(packet_data)  # Analyze and get stats
        Clock.schedule_once(lambda dt: self.update_stats_display(stats), 0)

    def update_stats_display(self, stats):
        self.stats_display.text += stats

    def export_capture(self, instance):
        # Logic to export the captured data
        pass

    def import_capture(self, instance):
        # Logic to import and display previously captured data
        pass

    def run_tshark(self, interface, monitor_mode, filter_string, save):
        if monitor_mode:
            subprocess.run(['sudo', 'iwconfig', interface, 'mode', 'monitor'])
        tshark_command = ['tshark', '-i', interface, '-V']
        if filter_string:
            tshark_command.extend(['-f', filter_string])
        if save:
            file_path = '/path/to/save/capture.pcap'  # Define the file path
            tshark_command.extend(['-w', file_path])

        self.capture_process = subprocess.Popen(tshark_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.capture_thread = Thread(target=self.read_from_process)
        self.capture_thread.daemon = True
        self.capture_thread.start()

    def craft_and_send_packet(self, instance):
        dst_ip = self.destination_ip_input.text.strip()
        payload = self.payload_input.text.strip()

        # Simple example: crafting an IP packet with Ether as the transport layer
        packet = Ether() / IP(dst=dst_ip) / payload
        sendp(packet, iface=self.interfaces_spinner.text)

        # Optionally, display information about the crafted packet
        self.packet_display.text += f'\nSent packet to {dst_ip} with payload: {payload}'

    def query_language_model(self, instance):
        prompt = self.language_model_input.text
        advice = send_prompt_to_language_model(prompt)
        self.model_advice_display.text = advice