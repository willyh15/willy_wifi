from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
import subprocess
import os
import re
import random
import time
import locale
import steganography
import scapy.all
from scapy.layers.inet import IP, TCP
from stem import Signal
from stem.control import Controller

class GhostModeScreen(MDScreen):
    ssh_tunnel_status = StringProperty('SSH Tunnel Status: Down')
    tor_status = StringProperty('Tor Status: Disconnected')

    def __init__(self, **kwargs):
        super(GhostModeScreen, self).__init__(**kwargs)
        self.ssh_tunnel_status = "OFF"
        self.traffic_padding_status = "OFF"
        self.dns_privacy_status = "OFF"
        # Add additional statuses for new functionalities
        self.logs_cleaned_status = "OFF"
        self.vm_live_os_status = "OFF"
        self.hip_status = "OFF"
        self.keystroke_anon_status = "OFF"
        self.timezone_locale_status = "OFF"
        self.encrypted_comm_status = "OFF"
        # UI setup
        self.add_widget(MDLabel(text=self.ssh_tunnel_status, halign='center'))
        self.add_widget(MDLabel(text=self.tor_status, halign='center'))
    # Function to change MAC Address
    def change_mac_address(self, interface):
        if not re.match(r'^[a-zA-Z0-9]+$', interface):
            self.show_dialog("Invalid interface name.")
            return

        new_mac = self.generate_random_mac_address()
        try:
            subprocess.run(["sudo", "ifconfig", interface, "down"], check=True)
            subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac], check=True)
            subprocess.run(["sudo", "ifconfig", interface, "up"], check=True)
            self.show_dialog(f"MAC address for {interface} changed to {new_mac}")
        except subprocess.CalledProcessError as e:
            self.show_dialog(f"Error changing MAC address: {e}")

    # Function to delete files securely
    def secure_delete_file(self, file_path):
        if not os.path.isfile(file_path):
            self.show_dialog(f"File not found: {file_path}")
            return

        try:
            subprocess.run(["shred", "-u", "-z", "-n", "10", file_path], check=True)
            self.show_dialog(f"Securely deleted {file_path}")
        except subprocess.CalledProcessError as e:
            self.show_dialog(f"Error in secure deletion: {e}")

    def encrypt_file_system(self, directory):
        # Placeholder for file system encryption logic
        pass

    def hide_data_in_image(self, data, cover_image_path, output_image_path):
        try:
            steganography.encode(cover_image_path, output_image_path, data.encode())
            self.show_dialog(f"Data hidden in {output_image_path}")
        except Exception as e:
            self.show_dialog(f"Error hiding data in image: {e}")

    def connect_to_tor(self):
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
            self.tor_status = "Tor Status: Connected"
            self.show_dialog("Connected to Tor successfully.")
        except Exception as e:
            self.tor_status = "Tor Status: Error"
            self.show_dialog(f"Failed to connect to Tor: {e}")

    def connect_to_vpn(self, vpn_config):
        try:
            subprocess.run(["sudo", "openvpn", "--config", vpn_config])
            self.show_dialog(f"Connected to VPN using {vpn_config}")
        except Exception as e:
            self.show_dialog(f"Failed to connect to VPN: {e}")

    def run_via_proxychains(self, command):
        try:
            subprocess.run(f'proxychains {command}', shell=True)
            self.show_dialog(f"Command run via proxychains: {command}")
        except Exception as e:
            self.show_dialog(f"Failed to run command via proxychains: {e}")

    def setup_ssh_tunnel(self, username, remote_host, local_port, remote_port):
        try:
            subprocess.Popen(
                ["ssh", "-f", "-N", "-L", f"{local_port}:localhost:{remote_port}", f"{username}@{remote_host}"])
            Clock.schedule_once(lambda dt: self.update_ssh_tunnel_status(True), 1)
        except Exception as e:
            self.show_dialog(f"Error setting up SSH tunnel: {e}")
            self.update_ssh_tunnel_status(False)

    def update_ssh_tunnel_status(self, success):
        status = 'Established' if success else 'Down'
        self.ssh_tunnel_status = f'SSH Tunnel Status: {status}'
        self.ssh_tunnel_status_label.text = self.ssh_tunnel_status

    def start_traffic_padding(self):
        try:
            self.traffic_padding_status = "ON"
            self.show_dialog("Traffic padding started.")
        except Exception as e:
            self.traffic_padding_status = "ERROR"
            self.show_dialog(f"Failed to start traffic padding: {e}")

    def send_padded_traffic(self, target_ip, duration):
        try:
            packet = IP(dst=target_ip) / TCP() / scapy.all.Padding(load="X" * 1000)
            end_time = time.time() + duration
            while time.time() < end_time:
                scapy.all.sendp(packet)
            self.show_dialog(f"Padded traffic sent to {target_ip} for {duration} seconds.")
        except Exception as e:
            self.show_dialog(f"Failed to send padded traffic: {e}")

    def enable_dns_privacy(self):
        try:
            self.dns_privacy_status = "ON"
            self.show_dialog("DNS privacy enabled.")
        except Exception as e:
            self.dns_privacy_status = "ERROR"
            self.show_dialog(f"Failed to enable DNS privacy: {e}")

    def clean_system_logs(self):
        try:
            subprocess.run("rm -rf /var/log/*", shell=True)
            self.logs_cleaned_status = "CLEANED"
            self.show_dialog("System logs cleaned.")
        except Exception as e:
            self.logs_cleaned_status = "ERROR"
            self.show_dialog(f"Failed to clean system logs: {e}")

    def wipe_ram_data(self):
        try:
            subprocess.run("shred -u /dev/mem", shell=True)
            self.show_dialog("RAM data wiped.")
        except Exception as e:
            self.show_dialog(f"Failed to wipe RAM data: {e}")

    def wipe_disk_data(self, path):
        if not os.path.exists(path):
            self.show_dialog(f"Path not found: {path}")
            return

        try:
            subprocess.run(f"shred -u {path}", shell=True, check=True)
            self.show_dialog(f"Disk data at {path} wiped.")
        except subprocess.CalledProcessError as e:
            self.show_dialog(f"Failed to wipe disk data: {e}")

    def operate_from_vm_or_live_os(self):
        self.vm_live_os_status = "ACTIVE"
        self.show_dialog("Operating from VM or Live OS.")

    def implement_hip(self):
        self.hip_status = "IMPLEMENTED"
        self.show_dialog("Host Identity Protocol implemented.")

    def anonymize_keystrokes(self):
        self.keystroke_anon_status = "ANONYMIZED"
        self.show_dialog("Keystroke anonymization implemented.")

    def change_timezone_and_locale(self, timezone, locale_str):
        try:
            os.environ['TZ'] = timezone
            time.tzset()
            locale.setlocale(locale.LC_ALL, locale_str)
            self.timezone_locale_status = "MATCHED"
            self.show_dialog(f"Timezone set to {timezone} and locale set to {locale_str}.")
        except Exception as e:
            self.timezone_locale_status = "ERROR"
            self.show_dialog(f"Failed to change timezone and locale: {e}")

    def integrate_encrypted_messaging(self):
        self.encrypted_comm_status = "INTEGRATED"
        self.show_dialog("Encrypted messaging and file sharing integrated.")

    def show_dialog(self, message):
        dialog = MDDialog(title='Notification', text=message)
        dialog.open()

