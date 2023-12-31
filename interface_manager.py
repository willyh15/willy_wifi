import netifaces

def get_interfaces():
    try:
        # Use the netifaces library to get network interfaces
        interfaces = netifaces.interfaces()
        return interfaces
    except Exception as e:
        print("Error getting interfaces:", str(e))
        return []