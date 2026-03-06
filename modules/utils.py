import yaml
import datetime
import os
import logging
import config

# Setup logging
os.makedirs(config.LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(config.LOG_DIR, "automation.log"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_inventory(filepath):
    """
    Loads device inventory from a YAML file.
    """
    if not os.path.exists(filepath):
        logging.error(f"Inventory file not found: {filepath}")
        return []
    try:
        with open(filepath, 'r') as f:
            inventory = yaml.safe_load(f)
            return inventory.get('devices', [])
    except yaml.YAMLError as e:
        logging.error(f"Error parsing inventory YAML file: {e}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading inventory: {e}")
        return []

def get_timestamp():
    """
    Returns a formatted timestamp string.
    """
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def log_message(level, message):
    """
    Logs a message using the configured logger.
    """
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
    elif level == "debug":
        logging.debug(message)
    print(message) # Also print to console