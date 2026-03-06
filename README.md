# Network Automation & Configuration Toolkit

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Netmiko](https://img.shields.io/badge/Netmiko-Supported-green.svg)
![Jinja2](https://img.shields.io/badge/Jinja2-Templating-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Roadmap](#roadmap)

## Project Overview

The **Network Automation & Configuration Toolkit** is a powerful and flexible Python-based solution designed to streamline common network engineering tasks. From automated configuration backups to templated deployments and operational state gathering, this toolkit aims to reduce manual effort, minimize errors, and improve the efficiency of managing network infrastructure.

Built with modularity in mind, it leverages industry-standard libraries like `Netmiko` for device connectivity and `Jinja2` for configuration templating, making it adaptable to various network vendors and scenarios.

## Features

*   **Automated Configuration Backup**: Securely connect to network devices (Cisco IOS, Juniper Junos, Arista EOS, etc.) and save their running configurations.
*   **Templated Configuration Deployment**: Utilize Jinja2 templates to generate and deploy standardized configurations.
*   **Operational State Gathering**: Execute "show" commands across multiple devices and collect their outputs for analysis or reporting.
*   **Device Inventory Management**: Easy-to-manage YAML-based inventory for device details and connection parameters.
*   **Extensible Architecture**: Easily add support for new device types, automation tasks, and custom reports.
*   **Secure Credential Handling**: Encourages best practices for managing sensitive information.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/).
*   **pip**: Python package installer (usually comes with Python).

## Installation

Follow these steps to set up the project locally:

1.  **Clone the Repository**:
    First, ensure you have Git installed. Then, open your terminal or command prompt and run:
    ```bash
    git clone https://github.com/tech-by-nasa/Network-Automation-Toolkit.git
    cd Network-Automation-Toolkit
    ```

2.  **Create a Virtual Environment (Recommended)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # .\venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Before running any automation tasks, you need to configure your device inventory and potentially credentials.

1.  **`inventory.yaml`**:
    This file holds the details of your network devices. Rename `inventory.yaml.example` to `inventory.yaml` and populate it with your device information.
    **IMPORTANT**: Ensure this file is properly secured and *never* commit sensitive credentials directly into this file if it's meant for public viewing. Use environment variables or a secure vault for production credentials.

    Example `inventory.yaml` structure:
    ```yaml
    devices:
      - name: router-a
        host: 192.168.1.1
        device_type: cisco_ios
        groups: ['routers', 'core']
        # You might include per-device credentials here, but it's recommended
        # to manage them centrally or via environment variables for security.
        # username: admin
        # password: password
      - name: switch-b
        host: 192.168.1.2
        device_type: juniper_junos
        groups: ['switches', 'access']
    ```

2.  **`config.py`**:
    This file is intended for global configuration settings, including default credentials or paths.
    **SECURITY NOTE**: For production environments, it is strongly recommended to use environment variables (`os.getenv()`) or a dedicated secret management system (e.g., HashiCorp Vault, AWS Secrets Manager) for credentials instead of hardcoding them here.

    Example `config.py` (replace placeholders):
    ```python
    # Default device credentials (use environment variables in production!)
    DEFAULT_USERNAME = "your_username"
    DEFAULT_PASSWORD = "your_password"
    DEFAULT_SECRET = "your_enable_secret" # For Cisco 'enable' mode

    # Paths
    BACKUP_DIR = "data/backups"
    LOG_DIR = "data/logs"
    TEMPLATES_DIR = "templates"
    ```

## Usage

Once configured, you can run various automation tasks using `main.py`.

### Backup Configurations

To backup configurations for all devices listed in `inventory.yaml`:
```bash
python main.py backup --all
```
To backup a specific device:
```bash
python main.py backup --device router-a
```

### Deploy Configurations

To deploy a template to a specific device:
```bash
python main.py deploy --device switch-b --template juniper_bgp_template.j2
```
Ensure your template (`templates/juniper_bgp_template.j2`) exists and is properly formatted.

### Gather Operational State

To run a specific command (e.g., `show ip interface brief`) on a device:
```bash
python main.py gather --device router-a --command "show ip interface brief"
```
To run multiple commands or predefined commands on multiple devices, you would extend `main.py` and `modules/gather_state.py`.

### Getting Help
```bash
python main.py --help
python main.py backup --help
```

## Project Structure

*   `.gitignore`: Specifies intentionally untracked files to ignore.
*   `LICENSE`: The MIT License for the project.
*   `README.md`: This comprehensive guide to the project.
*   `CONTRIBUTING.md`: Guidelines for contributing to the project.
*   `requirements.txt`: Lists all Python dependencies.
*   `main.py`: The primary entry point for executing automation tasks. Uses `argparse` for command-line arguments.
*   `config.py`: Stores global configuration settings, paths, and default credentials.
*   `inventory.yaml`: YAML file containing the inventory of network devices.
*   `modules/`: Contains reusable Python modules for specific automation functions.
    *   `__init__.py`: Makes the directory a Python package.
    *   `backup.py`: Logic for backing up device configurations.
    *   `deploy.py`: Logic for deploying configurations using templates.
    *   `gather_state.py`: Logic for gathering operational states (e.g., `show` commands).
    *   `utils.py`: Utility functions (e.g., loading inventory, logging).
*   `templates/`: Directory for Jinja2 configuration templates.
*   `data/`: Stores dynamic data like backups and logs.
    *   `backups/`: Saved device configurations.
    *   `logs/`: Log files generated by the automation scripts.
*   `tests/`: Unit and integration tests for the project.

## Contributing

We welcome contributions! Please refer to `CONTRIBUTING.md` for guidelines on how to submit issues, features, and pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Roadmap

Future enhancements may include:
*   Adding support for more device types and APIs (e.g., RESTCONF, NETCONF).
*   Implementing a web-based UI for task management.
*   Integrating with a secret management solution (e.g., HashiCorp Vault).
*   Adding CI/CD pipelines for automated testing and deployment of the toolkit itself.
*   Advanced reporting and analytics features for gathered data.
*   Support for scheduling tasks.
