from netmiko import ConnectHandler
import os
import time
from modules.utils import log_message, get_timestamp
import config

def backup_device_config(device_entry, username, password, secret=None, backup_dir=None):
    """
    Connects to a network device and backs up its running configuration.

    Args:
        device_entry (dict): Dictionary containing device details (host, device_type, name).
        username (str): Username for device login.
        password (str): Password for device login.
        secret (str, optional): Enable password for Cisco IOS devices. Defaults to None.
        backup_dir (str, optional): Directory to save backups. Defaults to config.BACKUP_DIR.
    """
    host = device_entry.get("host")
    device_type = device_entry.get("device_type")
    device_name = device_entry.get("name", host) # Use host if name not provided

    if not all([host, device_type]):
        log_message("error", f"Skipping backup for device {device_name}: Missing host or device_type.")
        return

    # Override global credentials if specified per device in inventory
    device_username = device_entry.get("username", username)
    device_password = device_entry.get("password", password)
    device_secret = device_entry.get("secret", secret)
    
    backup_dir = backup_dir if backup_dir else config.BACKUP_DIR

    device_params = {
        "device_type": device_type,
        "host": host,
        "username": device_username,
        "password": device_password,
        "secret": device_secret, # Only applicable for some device types (e.g., Cisco IOS enable mode)
        "port": 22, # Default SSH port
        "timeout": config.CONNECT_TIMEOUT,
    }

    try:
        log_message("info", f"Connecting to {device_name} ({host}) for backup...")
        with ConnectHandler(**device_params) as net_connect:
            if device_type.startswith("cisco_ios"):
                command = "show running-config"
            elif device_type.startswith("juniper_junos"):
                command = "show configuration | display set" # Or 'show configuration | display json'
            elif device_type.startswith("arista_eos"):
                command = "show running-config"
            else:
                log_message("warning", f"Unsupported device type '{device_type}' for backup on {device_name}.")
                return

            log_message("info", f"Executing '{command}' on {device_name}...")
            output = net_connect.send_command(command, use_textfsm=False)

            filename = os.path.join(backup_dir, f"{device_name}_{get_timestamp()}.cfg")
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                f.write(output)
            log_message("info", f"Backup for {device_name} saved to {filename}")

    except Exception as e:
        log_message("error", f"Failed to backup configuration for {device_name} ({host}): {e}")