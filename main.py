import argparse
import os
import sys

# Ensure the modules directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules import backup, deploy, gather_state, utils
import config

def main():
    parser = argparse.ArgumentParser(
        description="Network Automation & Configuration Toolkit",
        epilog="Use 'python main.py <command> --help' for specific command options."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Backup Command ---
    backup_parser = subparsers.add_parser("backup", help="Backup configurations from network devices.")
    backup_parser.add_argument("--device", help="Specify a single device to backup by its name.")
    backup_parser.add_argument("--all", action="store_true", help="Backup configurations from all devices in inventory.")
    backup_parser.set_defaults(func=run_backup)

    # --- Deploy Command ---
    deploy_parser = subparsers.add_parser("deploy", help="Deploy configurations to network devices.")
    deploy_parser.add_argument("--device", required=True, help="Specify the device to deploy configuration to by its name.")
    deploy_parser.add_argument("--template", required=True, help="Path to the Jinja2 template for configuration.")
    deploy_parser.set_defaults(func=run_deploy)

    # --- Gather State Command ---
    gather_parser = subparsers.add_parser("gather", help="Gather operational state (e.g., 'show' commands) from network devices.")
    gather_parser.add_argument("--device", required=True, help="Specify the device to gather state from by its name.")
    gather_parser.add_argument("--command", required=True, help="The 'show' command to execute on the device.")
    gather_parser.set_defaults(func=run_gather_state)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    # Load inventory once for all commands
    devices = utils.load_inventory("inventory.yaml")
    if not devices:
        print("Error: No devices found in inventory.yaml or file not found.")
        sys.exit(1)

    args.func(args, devices)

def run_backup(args, devices):
    if args.all:
        print("Starting backup for all devices...")
        for device_entry in devices:
            device_name = device_entry.get("name")
            print(f"  Attempting backup for {device_name}...")
            backup.backup_device_config(
                device_entry,
                username=config.DEFAULT_USERNAME,
                password=config.DEFAULT_PASSWORD,
                secret=config.DEFAULT_SECRET,
                backup_dir=config.BACKUP_DIR
            )
        print("Backup process completed for all devices.")
    elif args.device:
        device_entry = next((d for d in devices if d.get("name") == args.device), None)
        if device_entry:
            print(f"Starting backup for device: {args.device}")
            backup.backup_device_config(
                device_entry,
                username=config.DEFAULT_USERNAME,
                password=config.DEFAULT_PASSWORD,
                secret=config.DEFAULT_SECRET,
                backup_dir=config.BACKUP_DIR
            )
            print(f"Backup process completed for {args.device}.")
        else:
            print(f"Error: Device '{args.device}' not found in inventory.")
    else:
        print("Error: Please specify either --device <name> or --all for backup.")
        sys.exit(1)

def run_deploy(args, devices):
    device_entry = next((d for d in devices if d.get("name") == args.device), None)
    if device_entry:
        print(f"Starting deployment for device: {args.device} using template: {args.template}")
        deploy.deploy_config_template(
            device_entry,
            template_name=args.template,
            template_dir=config.TEMPLATES_DIR,
            username=config.DEFAULT_USERNAME,
            password=config.DEFAULT_PASSWORD,
            secret=config.DEFAULT_SECRET
        )
        print(f"Deployment process completed for {args.device}.")
    else:
        print(f"Error: Device '{args.device}' not found in inventory.")
        sys.exit(1)

def run_gather_state(args, devices):
    device_entry = next((d for d in devices if d.get("name") == args.device), None)
    if device_entry:
        print(f"Gathering state from device: {args.device} with command: '{args.command}'")
        output = gather_state.gather_device_state(
            device_entry,
            command=args.command,
            username=config.DEFAULT_USERNAME,
            password=config.DEFAULT_PASSWORD
        )
        if output:
            print(f"\n--- Output for {args.device} ---\n{output}\n---------------------------\n")
            # Optionally, save to a log file
            log_filename = os.path.join(config.LOG_DIR, f"{args.device}_{args.command.replace(' ', '_')}_{utils.get_timestamp()}.log")
            os.makedirs(os.path.dirname(log_filename), exist_ok=True)
            with open(log_filename, 'w') as f:
                f.write(output)
            print(f"Output saved to {log_filename}")

    else:
        print(f"Error: Device '{args.device}' not found in inventory.")
        sys.exit(1)

if __name__ == "__main__":
    main()