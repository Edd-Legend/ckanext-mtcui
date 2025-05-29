# Contributing to ckanext-mtcui

Thank you for your interest in contributing to ckanext-mtcui! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Edd-Legend/ckanext-mtcui.git
   cd ckanext-mtcui
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

3. Push your branch to GitHub:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request (PR) from your branch to master.

## Code Style

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused on a single task
- Write unit tests for new functionality

## Testing

1. Run the test suite:
   ```bash
   pytest
   ```

2. Run tests with coverage:
   ```bash
   pytest --cov=ckanext.mtcui
   ```

## Pull Request Process

1. Ensure your code passes all tests
2. Update documentation if necessary
3. Add comments to complex code sections
4. Request review from at least one team member
5. Address any feedback from code reviews
6. Ensure your branch is up to date with master before merging

## Commit Messages

Follow these guidelines for commit messages:
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add user authentication feature

- Implement login functionality
- Add password reset capability
- Update documentation

Fixes #123
```

## Documentation

- Update README.md for significant changes
- Document new features in the code
- Add comments for complex logic
- Keep documentation up to date with code changes

## Reporting Bugs

When reporting bugs, please include:
1. A clear description of the issue
2. Steps to reproduce the problem
3. Expected behavior
4. Actual behavior
5. Screenshots if applicable
6. Environment details (OS, Python version, CKAN version)

## Feature Requests

When suggesting new features:
1. Provide a clear description of the feature
2. Explain why this feature would be useful
3. Suggest implementation details if possible
4. Consider potential impacts on existing functionality

## Questions and Support

For questions and support:
1. Check the existing documentation
2. Search existing issues
3. Create a new issue if needed
4. Tag issues appropriately

## License

By contributing to this project, you agree that your contributions will be licensed under the project's LICENSE file.

Thank you for contributing to ckanext-mtcui! 