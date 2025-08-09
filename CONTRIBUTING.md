# Contributing to Microsoft 365 License Tracker

Thank you for your interest in contributing to Microsoft 365 License Tracker! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and considerate of others.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported by searching the [Issues](https://github.com/jaquanwatson/m365-license-tracker/issues).
2. If the bug hasn't been reported, [open a new issue](https://github.com/jaquanwatson/m365-license-tracker/issues/new/choose) using the Bug Report template.
3. Provide a clear title and description, along with steps to reproduce the bug.
4. Include any relevant screenshots or error messages.

### Suggesting Features

1. Check if the feature has already been suggested by searching the [Issues](https://github.com/jaquanwatson/m365-license-tracker/issues).
2. If the feature hasn't been suggested, [open a new issue](https://github.com/jaquanwatson/m365-license-tracker/issues/new/choose) using the Feature Request template.
3. Provide a clear title and description of the feature.
4. Explain why this feature would be valuable to the project.

### Pull Requests

1. Fork the repository.
2. Create a new branch from `main` for your changes.
3. Make your changes, following the coding standards and guidelines.
4. Add tests for your changes if applicable.
5. Ensure all tests pass.
6. Update documentation if necessary.
7. Submit a pull request to the `main` branch.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/m365-license-tracker.git
   cd m365-license-tracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure authentication:
   ```bash
   cp config.example.json config.json
   # Edit config.json with your Azure app details
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Run tests:
   ```bash
   pytest
   ```

## Project Structure

```
m365-license-tracker/
├── src/                  # Source code
│   ├── dashboard.py      # Dashboard UI components
│   └── license_manager.py # License management logic
├── static/               # Static assets (CSS, JS)
├── templates/            # HTML templates
├── tests/                # Test files
├── app.py                # Main application entry point
├── config.json           # Configuration file
└── requirements.txt      # Python dependencies
```

## Coding Standards

- Follow PEP 8 style guide for Python code.
- Use meaningful variable and function names.
- Write docstrings for all functions, classes, and modules.
- Include comments for complex code sections.
- Keep functions focused on a single responsibility.
- Use type hints where appropriate.

## Frontend Development

- Follow modern JavaScript best practices.
- Use CSS variables for consistent theming.
- Ensure responsive design for all UI components.
- Optimize for performance, especially with large datasets.
- Follow accessibility best practices.

## Testing

- Write unit tests for new functionality.
- Include integration tests for API endpoints.
- Test dashboard components with different datasets.
- Ensure all tests pass before submitting a pull request.
- Aim for high test coverage for new code.

## Documentation

- Update documentation for any changes to functionality.
- Document API endpoints with examples.
- Include screenshots for UI changes.
- Update configuration documentation if needed.

## Review Process

1. All pull requests will be reviewed by the maintainers.
2. Feedback may be provided for necessary changes.
3. Once approved, the pull request will be merged.

Thank you for contributing to Microsoft 365 License Tracker!