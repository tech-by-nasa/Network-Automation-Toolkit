import os

# --- Default Credentials (for testing/dev, use ENV vars in production!) ---
# It's highly recommended to load these from environment variables or a secrets manager.
# Example:
# DEFAULT_USERNAME = os.getenv("NETWORK_USERNAME", "your_default_username")
# DEFAULT_PASSWORD = os.getenv("NETWORK_PASSWORD", "your_default_password")
# DEFAULT_SECRET = os.getenv("NETWORK_ENABLE_SECRET", "your_default_enable_secret")

DEFAULT_USERNAME = "your_network_username" # Change this!
DEFAULT_PASSWORD = "your_network_password" # Change this!
DEFAULT_SECRET = "your_enable_secret" # Change this if needed for enable mode (Cisco IOS)

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BACKUP_DIR = os.path.join(BASE_DIR, "data", "backups")
LOG_DIR = os.path.join(BASE_DIR, "data", "logs")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Ensure these directories exist
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# --- Other Settings ---
CONNECT_TIMEOUT = 10 # Seconds for device connection timeout