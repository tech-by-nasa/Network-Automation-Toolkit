from netmiko import ConnectHandler
from modules.utils import log_message
import config

def gather_device_state(device_entry, command, username, password):
    """
    Connects to a network device and executes a 'show' command to gather operational state.

    Args:
        device_entry (dict): Dictionary containing device details.
        command (str): The 'show' command to execute.
        username (str): Username for device login.
        password (str): Password for device login.

    Returns:
        str: The output of the command, or None if an error occurred.
    """
    host = device_entry.get("host")
    device_type = device_entry.get("device_type")
    device_name = device_entry.get("name", host)

    if not all([host, device_type]):
        log_message("error", f"Skipping state gathering for {device_name}: Missing host or device_type.")
        return None

    device_username = device_entry.get("username", username)
    device_password = device_entry.get("password", password)

    device_params = {
        "device_type": device_type,
        "host": host,
        "username": device_username,
        "password": device_password,
        "port": 22,
        "timeout": config.CONNECT_TIMEOUT,
    }

    try:
        log_message("info", f"Connecting to {device_name} ({host}) to execute command: '{command}'")
        with ConnectHandler(**device_params) as net_connect:
            output = net_connect.send_command(command, use_textfsm=False)
            log_message("info", f"Command '{command}' executed successfully on {device_name}.")
            return output
    except Exception as e:
        log_message("error", f"Failed to execute command '{command}' on {device_name} ({host}): {e}")
        return None