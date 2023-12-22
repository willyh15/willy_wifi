from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen
import subprocess
import json
from datetime import datetime
from threading import Thread
from kivy.clock import Clock
from utils import validate_ip_address, send_prompt_to_language_model


SCAN_HISTORY_FILE = "scan_history.json"

class NmapScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def advanced_target_discovery(self, instance):
        ip_range = self.ip_input.text.strip()
        if validate_ip_address(ip_range):
            # TODO: Implement your discover_targets method
            print("Advanced target discovery is not yet implemented")
        else:
            self.scan_results.text = 'Invalid IP address format for discovery.'

    def vulnerability_scan(self, instance):
        target_ip = self.ip_input.text.strip()
        if validate_ip_address(target_ip):
            # TODO: Implement your vulnerability scanning logic
            print("Vulnerability scanning is not yet implemented")
        else:
            self.scan_results.text = 'Invalid IP address format for vulnerability scan.'

    def automated_vulnerability_assessment(self):
        # This is a placeholder. You'll need to implement logic to analyze scan results.
        # You can use regex to parse common vulnerabilities from the scan output
        # and match them against a database of known vulnerabilities.
        print("Performing automated vulnerability assessment...")

    def execute_nse_script(self, script_name, target):
        try:
            output = subprocess.check_output(['nmap', '--script', script_name, target], text=True)
            self.scan_results.text = output
        except subprocess.CalledProcessError as e:
            self.scan_results.text = f"Error executing NSE script: {e}"

    # This would involve saving and loading custom scan configurations.
    # You can use JSON or a similar format to save these profiles.

    def start_real_time_monitoring(self):
        # Implement logic for real-time monitoring. This could be a background thread
        # that periodically scans the network and updates the UI with any changes.
        print("Starting real-time network monitoring...")

    def integrate_with_metasploit(self, target):
        # Placeholder for integration with Metasploit.
        # This might involve running Metasploit commands and capturing their output.
        print("Integrating with Metasploit for target:", target)

    def ai_assisted_analysis(self, scan_data):
        # Use AI model to analyze scan data
        # This could involve sending data to an AI API and getting insights
        insights = send_prompt_to_language_model("Analyze scan data: " + scan_data)
        self.scan_results.text += "\nAI Insights: " + insights

    def map_network_topology(self, instance):
        target_ip = self.ip_input.text.strip()
        if validate_ip_address(target_ip):
            # TODO: Implement your network topology mapping logic
            print("Network topology mapping is not yet implemented")
        else:
            self.scan_results.text = 'Invalid IP address format for network mapping.'

    def start_scan(self, instance):
        target_ip = self.ip_input.text.strip()
        if validate_ip_address(target_ip):
            self.perform_nmap_scan(self.scan_type_spinner.text, target_ip)
        else:
            self.scan_results.text = 'Invalid IP address format.'
            self.scan_progress_bar.value = 0  # Reset progress bar
            Clock.schedule_interval(self.update_progress_bar, 1)  # Update every second
            # Start scan in a new thread if blocking
            Thread(target=self.perform_nmap_scan, args=(self.scan_type_spinner.text, target_ip)).start()

    def perform_nmap_scan(self, scan_type, target_ip):
        try:
            if scan_type in ['Quick Scan', 'Intense Scan', 'Port Scan']:
                command = self.map_scan_type_to_command(scan_type)
                scan_output = subprocess.check_output(['nmap'] + command.split(), text=True)
                self.scan_results.text = scan_output
            elif scan_type == 'Custom Scan':
                custom_options = self.custom_command_input.text.strip()
                nmap_command = ['nmap'] + custom_options.split() + [target_ip]
                scan_output = subprocess.check_output(nmap_command, text=True)
                self.scan_results.text = scan_output
        except subprocess.CalledProcessError as e:
            self.scan_results.text = f"An error occurred: {e}"
            self.save_scan_result(scan_type, target_ip, scan_output)

    def map_scan_type_to_command(self, scan_type):
        # TODO: Maps scan type to actual nmap command
        return "command_based_on_scan_type"

    def send_openai_prompt(self, instance):
        prompt = self.openai_prompt_input.text.strip()
        if prompt:
            response = send_prompt_to_language_model(prompt)
            self.openai_response_display.text = response
        else:
            self.openai_response_display.text = 'Please enter a prompt.'

    def update_progress_bar(self, *args):
            self.scan_progress_bar.value += 1  # Increment progress
        if self.scan_progress_bar.value >= 100:
            Clock.unschedule(self.update_progress_bar)  # Stop updating when scan is complete


    def generate_nmap_command(self, instance):
        intent = self.intent_input.text.strip()
        if intent:
            # Send intent to OpenAI model to get command suggestion
            suggested_command = send_prompt_to_language_model(f"Generate an nmap command for: {intent}")
            self.generated_command_display.text = suggested_command
        else:
            self.generated_command_display.text = 'Please enter your scanning intent.'

    def execute_generated_command(self, instance):
        command = self.generated_command_display.text.strip()
        if command:
            try:
                scan_output = subprocess.check_output(command.split(), text=True)
                self.scan_results.text = scan_output
            except subprocess.CalledProcessError as e:
                self.scan_results.text = f"An error occurred: {e}"
        else:
            self.scan_results.text = 'No command to execute.'


     def save_scan_result(self, scan_type, target_ip, result):
        # Load existing data
        try:
            with open(SCAN_HISTORY_FILE, 'r') as file:
            history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

    # Append new scan result
        history.append({
        "type": scan_type,
        "target": target_ip,
        "result": result,
        "timestamp": datetime.now().isoformat()
    })

    # Save updated history
    with open(SCAN_HISTORY_FILE, 'w') as file:
        json.dump(history, file, indent=4)

    def load_scan_history(self):
    try:
        with open(SCAN_HISTORY_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    # Load and display scan history
    def update_history_spinner(self):
        history = self.load_scan_history()
        self.history_spinner.values = [f"{h['timestamp']} - {h['type']} - {h['target']}" for h in history]

    def on_history_select(self, spinner, text):
        history = self.load_scan_history()
        for h in history:
            if text.startswith(h['timestamp']):
                self.scan_results.text = h['result']
            break
        self.history_spinner.bind(text=self.on_history_select)
        
    def generate_network_graph(self, scan_results):
    G = nx.Graph()
    # Assuming scan_results is a list of tuples (node1, node2)
    for node1, node2 in scan_results:
        G.add_edge(node1, node2)

    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, font_weight='bold')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return CoreImage(buf, ext='png')
    
    def update_network_map(self, scan_results):
    img = self.generate_network_graph(scan_results)
    self.network_map_image.texture = img.texture
