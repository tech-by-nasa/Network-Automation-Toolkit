import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the parent directory to the path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.backup import backup_device_config
from modules.deploy import deploy_config_template
from modules.gather_state import gather_device_state
from modules.utils import load_inventory
import config

# Mock configuration for tests
@pytest.fixture(autouse=True)
def mock_config():
    with patch('config.DEFAULT_USERNAME', 'testuser'), \
         patch('config.DEFAULT_PASSWORD', 'testpass'), \
         patch('config.DEFAULT_SECRET', 'testsecret'), \
         patch('config.BACKUP_DIR', 'data/test_backups'), \
         patch('config.LOG_DIR', 'data/test_logs'), \
         patch('config.TEMPLATES_DIR', 'templates'):
        yield
    # Clean up test directories
    if os.path.exists('data/test_backups'):
        for f in os.listdir('data/test_backups'):
            os.remove(os.path.join('data/test_backups', f))
        os.rmdir('data/test_backups')
    if os.path.exists('data/test_logs'):
        for f in os.listdir('data/test_logs'):
            os.remove(os.path.join('data/test_logs', f))
        os.rmdir('data/test_logs')

# Mock Netmiko's ConnectHandler
@pytest.fixture
def mock_connect_handler():
    with patch('netmiko.ConnectHandler') as mock_ch:
        instance = MagicMock()
        instance.__enter__.return_value = instance
        instance.__exit__.return_value = False
        instance.send_command.return_value = "Mocked command output"
        instance.send_config_set.return_value = "Mocked config set output"
        mock_ch.return_value = instance
        yield mock_ch

def test_load_inventory_success(tmp_path):
    inventory_content = """
    devices:
      - name: test-device-1
        host: 1.1.1.1
        device_type: cisco_ios
    """
    p = tmp_path / "test_inventory.yaml"
    p.write_text(inventory_content)
    devices = load_inventory(str(p))
    assert len(devices) == 1
    assert devices[0]["name"] == "test-device-1"

def test_load_inventory_not_found():
    devices = load_inventory("non_existent_inventory.yaml")
    assert len(devices) == 0

def test_backup_device_config_success(mock_connect_handler, tmp_path):
    device = {"name": "test-router", "host": "10.0.0.1", "device_type": "cisco_ios"}
    backup_device_config(device, "user", "pass", backup_dir=str(tmp_path))
    mock_connect_handler.assert_called_once()
    assert any(f.startswith("test-router_") and f.endswith(".cfg") for f in os.listdir(tmp_path))

def test_deploy_config_template_success(mock_connect_handler, tmp_path):
    # Create a mock template directory and template file
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "test_template.j2").write_text("hostname {{ device.name }}")

    device = {"name": "test-router", "host": "10.0.0.1", "device_type": "cisco_ios"}
    deploy_config_template(device, "test_template.j2", str(template_dir), "user", "pass")
    mock_connect_handler.assert_called_once()
    mock_connect_handler.return_value.send_config_set.assert_called_once()

def test_gather_device_state_success(mock_connect_handler):
    device = {"name": "test-router", "host": "10.0.0.1", "device_type": "cisco_ios"}
    output = gather_device_state(device, "show version", "user", "pass")
    mock_connect_handler.assert_called_once()
    assert output == "Mocked command output"