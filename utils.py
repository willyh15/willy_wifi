import subprocess
import openai
import re


def validate_ip_address(ip_addr):
    # A basic regular expression for IP address validation
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}(-\d{1,3})?$')
    return ip_pattern.match(ip_addr) is not None


# Function to list available network interfaces
def get_interfaces():
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
def analyze_packet():
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
