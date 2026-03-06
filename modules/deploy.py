from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
import os
from modules.utils import log_message
import config

def deploy_config_template(device_entry, template_name, template_dir, username, password, secret=None, commit=True):
    """
    Generates and deploys a configuration from a Jinja2 template to a network device.

    Args:
        device_entry (dict): Dictionary containing device details.
        template_name (str): Name of the Jinja2 template file.
        template_dir (str): Directory where templates are stored.
        username (str): Username for device login.
        password (str): Password for device login.
        secret (str, optional): Enable password for Cisco IOS devices. Defaults to None.
        commit (bool, optional): Whether to commit the changes (Juniper) or save (Cisco). Defaults to True.
    """
    host = device_entry.get("host")
    device_type = device_entry.get("device_type")
    device_name = device_entry.get("name", host)

    if not all([host, device_type]):
        log_message("error", f"Skipping deployment for {device_name}: Missing host or device_type.")
        return

    device_username = device_entry.get("username", username)
    device_password = device_entry.get("password", password)
    device_secret = device_entry.get("secret", secret)

    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    try:
        template = env.get_template(template_name)
    except Exception as e:
        log_message("error", f"Failed to load template {template_name}: {e}")
        return

    # Render template with device-specific data
    # You can pass more data to the template via device_entry.get('data', {})
    rendered_config = template.render(device=device_entry, **device_entry.get('data', {}))

    log_message("info", f"Rendered configuration for {device_name} from {template_name}:\n{rendered_config}")

    device_params = {
        "device_type": device_type,
        "host": host,
        "username": device_username,
        "password": device_password,
        "secret": device_secret,
        "port": 22,
        "timeout": config.CONNECT_TIMEOUT,
    }

    try:
        log_message("info", f"Connecting to {device_name} ({host}) for configuration deployment...")
        with ConnectHandler(**device_params) as net_connect:
            log_message("info", f"Sending configuration to {device_name}...")

            # Netmiko's send_config_set handles different device types
            output = net_connect.send_config_set(rendered_config.splitlines(), cmd_verify=True, exit_config_mode=True)
            log_message("info", f"Configuration output from {device_name}:\n{output}")

            # Specific actions for certain device types after config_set
            if commit:
                if device_type.startswith("juniper_junos"):
                    log_message("info", f"Committing changes on Juniper device {device_name}...")
                    net_connect.send_command("commit and-quit")
                elif device_type.startswith("cisco_ios") or device_type.startswith("arista_eos"):
                    # On Cisco/Arista, send_config_set usually applies changes directly,
                    # but 'write mem' or 'copy run start' is needed to save to startup-config
                    log_message("info", f"Saving configuration on {device_name} (Cisco/Arista-like)...")
                    net_connect.send_command("write memory")
                else:
                    log_message("warning", f"No explicit commit/save command for device type {device_type}. Assuming changes are live.")

            log_message("info", f"Configuration deployment for {device_name} successful.")

    except Exception as e:
        log_message("error", f"Failed to deploy configuration to {device_name} ({host}): {e}")