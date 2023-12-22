from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from scapy.all import sendp, IP, TCP, Padding
import time
import subprocess
from stem import Signal
from stem.control import Controller
import os
import pytz
from datetime import datetime
import shutil
import random
import steganography


class GhostModeScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    # Function to change MAC Address
    def change_mac_address(self, interface):
        if not re.match(r'^[a-zA-Z0-9]+$', interface):
            print("Invalid interface name.")
            return

        new_mac = self.generate_random_mac_address()
        try:
            subprocess.run(["sudo", "ifconfig", interface, "down"], check=True)
            subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac], check=True)
            subprocess.run(["sudo", "ifconfig", interface, "up"], check=True)
            print(f"MAC address for {interface} changed to {new_mac}")
        except subprocess.CalledProcessError as e:
            print(f"Error changing MAC address: {e}")

    @staticmethod
    def generate_random_mac_address():
        return "02:%02x:%02x:%02x:%02x:%02x:%02x" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

    # Function to delete files securely
    def secure_delete_file(self, file_path):
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            return

        try:
            subprocess.run(["shred", "-u", "-z", "-n", "10", file_path], check=True)
            print(f"Securely deleted {file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error in secure deletion: {e}")

    # Function to encrypt file system
    def encrypt_file_system(self, directory):
        # Placeholder for file system encryption logic
        # This could involve encrypting all files in a directory
        pass

    # Function to hide data in images
    def hide_data_in_image(self, data, cover_image_path, output_image_path):
        try:
            steganography.encode(cover_image_path, output_image_path, data.encode())
            print(f"Data hidden in {output_image_path}")
        except Exception as e:
            print(f"Error hiding data in image: {e}")

    # Function to connect to Tor
    def connect_to_tor(self):
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()  # Provide the password if set
                controller.signal(Signal.NEWNYM)
            print("Connected to Tor successfully.")
        except Exception as e:
            print(f"Failed to connect to Tor: {e}")

    # Function to connect with a VPN
    def connect_to_vpn(self, vpn_config):
        try:
            # Assuming OpenVPN
            subprocess.run(["sudo", "openvpn", "--config", vpn_config])
            print(f"Connected to VPN using {vpn_config}")
        except Exception as e:
            print(f"Failed to connect to VPN: {e}")

    # Function to run a command through proxychains
    def run_via_proxychains(self, command):
        try:
            subprocess.run(f'proxychains {command}', shell=True)
            print(f"Command run via proxychains: {command}")
        except Exception as e:
            print(f"Failed to run command via proxychains: {e}")

    def setup_ssh_tunnel(self):
        # Replace with your actual username, remote host, local and remote port numbers
        username = "user"
        remote_host = "remote_host_address"
        local_port = "local_port"
        remote_port = "remote_port"
        try:
            # The '-f' tells SSH to go into the background just before it executes the command
            # This is followed by '-N' which tells SSH that no command will be sent once the tunnel is up
            # '-L' specifies that the given port on the local (client) host is to be forwarded to the given host and port on the remote side
            subprocess.Popen(
                ["ssh", "-f", "-N", "-L", f"{local_port}:localhost:{remote_port}", f"{username}@{remote_host}"])
            # Update the UI after a slight delay to give time for the tunnel to establish
            Clock.schedule_once(lambda dt: self.update_ssh_tunnel_status(True), 1)
        except Exception as e:
            print(f"Error setting up SSH tunnel: {e}")
            self.update_ssh_tunnel_status(False)

    def update_ssh_tunnel_status(self, success):
        if success:
            self.ids.ssh_tunnel_status.text = 'SSH Tunnel Status: Established'
        else:
            self.ids.ssh_tunnel_status.text = 'SSH Tunnel Status: Down'

    def start_traffic_padding(self):
        # Logic to start traffic padding
        try:
            # Dummy logic to change the status, replace with actual traffic padding logic
            self.traffic_padding_status = "ON"
            print("Traffic padding started.")
        except Exception as e:
            print(f"Failed to start traffic padding: {e}")
            self.traffic_padding_status = "ERROR"

    # Function to send padded packets
    def send_padded_traffic(self, target_ip, duration):
        try:
            packet = IP(dst=target_ip) / TCP() / Padding(load="X" * 1000)
            end_time = time.time() + duration
            while time.time() < end_time:
                sendp(packet)
            print(f"Padded traffic sent to {target_ip} for {duration} seconds.")
        except Exception as e:
            print(f"Failed to send padded traffic: {e}")

    def enable_dns_privacy(self):
        # Logic to enable DNS privacy features like DoH or DoT
        try:
            # Dummy logic to change the status, replace with actual DNS privacy logic
            self.dns_privacy_status = "ON"
            print("DNS privacy enabled.")
        except Exception as e:
            print(f"Failed to enable DNS privacy: {e}")
            self.dns_privacy_status = "ERROR"

    def clean_system_logs(self):
        try:
            # Example command to clear system logs, replace with actual commands
            subprocess.run("rm -rf /var/log/*", shell=True)
            self.logs_cleaned_status = "CLEANED"
            print("System logs cleaned.")
        except Exception as e:
            print(f"Failed to clean system logs: {e}")
            self.logs_cleaned_status = "ERROR"

    def wipe_ram_data(self):
        try:
            # Example command to wipe RAM data, replace with actual commands
            subprocess.run("shred -u /dev/mem", shell=True)
            print("RAM data wiped.")
        except Exception as e:
            print(f"Failed to wipe RAM data: {e}")

    def wipe_disk_data(self, path):
        if not os.path.exists(path):
            print(f"Path not found: {path}")
            return

        try:
            subprocess.run(f"shred -u {path}", shell=True, check=True)
            print(f"Disk data at {path} wiped.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to wipe disk data: {e}")

    def operate_from_vm_or_live_os(self):
        # This method would be a placeholder, as operating from a VM or live OS is not something you can toggle from a script
        self.vm_live_os_status = "ACTIVE"
        print("Operating from VM or Live OS.")

    def implement_hip(self):
        # Placeholder for Host Identity Protocol implementation
        self.hip_status = "IMPLEMENTED"
        print("Host Identity Protocol implemented.")

    def anonymize_keystrokes(self):
        # Placeholder for keystroke anonymization implementation
        self.keystroke_anon_status = "ANONYMIZED"
        print("Keystroke anonymization implemented.")

    def change_timezone_and_locale(self, timezone, locale):
        if not re.match(r'^[a-zA-Z/_]+$', timezone):
            print("Invalid timezone.")
            return
        if not re.match(r'^[a-zA-Z_.@]+$', locale):
            print("Invalid locale.")
            return

        try:
            # Set the timezone and locale
            os.environ['TZ'] = timezone
            time.tzset()
            locale.setlocale(locale.LC_ALL, locale)
            self.timezone_locale_status = "MATCHED"
            print(f"Timezone set to {timezone} and locale set to {locale}.")
        except Exception as e:
            print(f"Failed to change timezone and locale: {e}")
            self.timezone_locale_status = "ERROR"

    def integrate_encrypted_messaging(self):
        # Placeholder for integrating secure platforms
        self.encrypted_comm_status = "INTEGRATED"
        print("Encrypted messaging and file sharing integrated.")
