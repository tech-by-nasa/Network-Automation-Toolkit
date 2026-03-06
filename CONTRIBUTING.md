# Contributing to Network Automation & Configuration Toolkit

We welcome contributions to make this toolkit even better! Please read this document carefully to understand how you can help.

## How to Contribute

1.  **Fork the Repository**: Start by forking the `Network-Automation-Toolkit` repository to your GitHub account.
2.  **Clone Your Fork**: Clone your forked repository to your local machine.
    ```bash
    git clone https://github.com/YOUR_USERNAME/Network-Automation-Toolkit.git
    cd Network-Automation-Toolkit
    ```
3.  **Create a New Branch**: Always work on a new branch for your features or bug fixes.
    ```bash
    git checkout -b feature/your-new-feature-name
    # OR
    git checkout -b bugfix/issue-description
    ```
4.  **Make Your Changes**: Implement your changes, ensuring code quality, comments, and adherence to the existing style.
    *   **Code Style**: Follow PEP 8 guidelines. We recommend using `black` for formatting and `flake8` for linting.
    *   **Documentation**: Update the `README.md` if your changes impact installation, configuration, or usage. Add docstrings to new functions/classes.
    *   **Tests**: If you add new features, please add corresponding unit or integration tests in the `tests/` directory. If you fix a bug, consider adding a test that would have caught it.
5.  **Test Your Changes**: Run existing tests and any new tests you've added.
    ```bash
    pytest
    ```
6.  **Commit Your Changes**: Write clear, concise commit messages.
    ```bash
    git commit -m "feat: Add new feature to XYZ module"
    # OR
    git commit -m "fix: Resolve bug in configuration deployment"
    ```
    (We recommend using [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages.)
7.  **Push to Your Fork**:
    ```bash
    git push origin feature/your-new-feature-name
    ```
8.  **Create a Pull Request**: Go to your forked repository on GitHub and create a "New Pull Request" to the `main` branch of the original `tech-by-nasa/Network-Automation-Toolkit` repository.
    *   **Provide a clear description** of your changes.
    *   **Reference any related issues** (e.g., "Closes #123").
    *   **Explain the problem your PR solves** and how it solves it.

## Reporting Issues

If you find a bug or have a feature request, please open an issue on the GitHub repository.

*   **Bug Reports**:
    *   Clearly describe the bug, including steps to reproduce it.
    *   Mention your operating system, Python version, and any relevant traceback.
    *   Provide any relevant configuration or input data (sanitized of sensitive info).
*   **Feature Requests**:
    *   Clearly describe the desired feature and why it would be beneficial.
    *   Provide examples of how it would be used.

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project, you agree to abide by its terms.

Thank you for contributing!