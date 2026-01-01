# Contributing to EDC Group Permission Automation

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 🎯 Ways to Contribute

- 🐛 Report bugs and issues
- 💡 Suggest new features or enhancements
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new features
- 🧪 Write tests
- 🌐 Translate documentation

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/edc-group-automation.git
cd edc-group-automation
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 3. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b bugfix/issue-number-description
```

## 📋 Development Guidelines

### Code Style

We follow PEP 8 style guidelines for Python code.

#### Use a Linter

```bash
# Install flake8
pip install flake8

# Run linter
flake8 *.py

# Or use pylint
pip install pylint
pylint *.py
```

#### Code Formatting

```bash
# Install black
pip install black

# Format code
black *.py
```

### Code Standards

1. **Function Documentation**

   ```python
   def function_name(param1, param2):
       """
       Brief description of what the function does.

       Args:
           param1 (type): Description of param1
           param2 (type): Description of param2

       Returns:
           type: Description of return value

       Raises:
           ExceptionType: When this exception is raised
       """
       pass
   ```

2. **Error Handling**

   ```python
   try:
       # Code that might raise an exception
       result = risky_operation()
   except SpecificException as e:
       logging.error(f"Specific error occurred: {e}")
       # Handle appropriately
   except Exception as e:
       logging.error(f"Unexpected error: {e}", exc_info=True)
       # Handle appropriately
   ```

3. **Logging**

   ```python
   # Use appropriate log levels
   logging.debug("Detailed information for debugging")
   logging.info("General information about program flow")
   logging.warning("Warning about potential issues")
   logging.error("Error that prevented operation")
   logging.critical("Critical error causing program termination")
   ```

4. **Constants**
   ```python
   # Use UPPER_CASE for constants
   MAX_RETRIES = 3
   DEFAULT_TIMEOUT = 30
   API_VERSION = "1.0"
   ```

### Testing

#### Write Tests

```python
# In tests/test_resources.py
import unittest
from resources import Resources

class TestResources(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.resource_manager = Resources()

    def test_set_permission_read(self):
        """Test READ permission setting"""
        result = self.resource_manager.setPermission(
            "TestResource",
            "READ",
            "Oracle"
        )
        self.assertEqual(result["resourceName"], "TestResource")
        self.assertEqual(
            result["classFilters"][0]["permission"],
            "READ"
        )

    def tearDown(self):
        """Clean up after tests"""
        pass
```

#### Run Tests

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests/test_resources.py

# With coverage
pip install coverage
coverage run -m unittest discover tests/
coverage report
```

## 🐛 Bug Reports

### Before Submitting

- Check existing issues to avoid duplicates
- Verify the bug exists in the latest version
- Collect relevant information

### Bug Report Template

```markdown
**Description**
A clear description of the bug.

**To Reproduce**
Steps to reproduce:

1. Configure with '...'
2. Run command '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**

- OS: [e.g., Ubuntu 20.04]
- Python Version: [e.g., 3.8.10]
- EDC Version: [e.g., 10.4.1]

**Logs**
```

Relevant log output

```

**Screenshots**
If applicable, add screenshots.

**Additional Context**
Any other relevant information.
```

## 💡 Feature Requests

### Before Submitting

- Check if the feature already exists
- Search existing feature requests
- Consider if it fits the project scope

### Feature Request Template

```markdown
**Problem Statement**
Describe the problem this feature would solve.

**Proposed Solution**
Describe your proposed solution.

**Alternatives Considered**
Other solutions you've considered.

**Use Case**
Real-world scenario where this would be useful.

**Priority**

- [ ] High - Critical for operations
- [ ] Medium - Would significantly improve usability
- [ ] Low - Nice to have
```

## 📝 Pull Requests

### PR Checklist

Before submitting your pull request:

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated (if needed)
- [ ] Commit messages are clear and descriptive
- [ ] No credentials or sensitive data in code
- [ ] CHANGELOG.md updated
- [ ] PR description clearly explains changes

### PR Template

```markdown
**Description**
Brief description of changes.

**Type of Change**

- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

**Related Issue**
Fixes #(issue number)

**Testing**
Describe testing performed:

- Test case 1
- Test case 2

**Screenshots**
If applicable, add screenshots.

**Checklist**

- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] Added tests
- [ ] All tests pass
- [ ] No new warnings generated
```

### Commit Message Guidelines

Format: `<type>(<scope>): <subject>`

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:

```bash
git commit -m "feat(groups): add support for nested groups"
git commit -m "fix(resources): handle null resource names"
git commit -m "docs(readme): update installation instructions"
```

## 🔍 Code Review Process

### For Contributors

1. Submit PR with clear description
2. Respond to review comments promptly
3. Update PR based on feedback
4. Be patient - reviews may take a few days

### For Reviewers

1. Be respectful and constructive
2. Focus on code, not the person
3. Explain reasoning for suggestions
4. Approve when ready or request changes

### Review Checklist

- [ ] Code is readable and maintainable
- [ ] Logic is correct and efficient
- [ ] Error handling is appropriate
- [ ] Security concerns addressed
- [ ] Tests are adequate
- [ ] Documentation is clear
- [ ] No hardcoded credentials
- [ ] Follows project conventions

## 📚 Documentation

### Documentation Standards

1. **Inline Comments**

   - Explain "why", not "what"
   - Keep comments up to date
   - Use clear, concise language

2. **README Updates**

   - Keep examples current
   - Update version information
   - Add new features to feature list

3. **API Documentation**
   - Document all public functions
   - Include parameter types
   - Provide usage examples

## 🏗️ Project Structure

```
edc-group-automation/
├── main.py                 # Main entry point
├── config.py              # Configuration settings
├── globalparams.py.example # Configuration template
├── excel.py               # Excel file handling
├── groups.py              # Group management
├── resources.py           # Resource management
├── requirements.txt       # Python dependencies
├── requirements-dev.txt   # Development dependencies
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── SECURITY.md           # Security guidelines
├── CONTRIBUTING.md       # This file
├── CHANGELOG.md          # Version history
├── LICENSE               # License information
└── tests/                # Test files
    ├── test_excel.py
    ├── test_groups.py
    └── test_resources.py
```

## 🎓 Learning Resources

### Python

- [Python Official Documentation](https://docs.python.org/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Real Python Tutorials](https://realpython.com/)

### Informatica EDC

- [Informatica Documentation](https://docs.informatica.com/)
- [EDC REST API Reference](https://docs.informatica.com/)

### Git & GitHub

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)

## 📞 Getting Help

- 💬 **Discussions:** Use GitHub Discussions for questions
- 🐛 **Issues:** Report bugs via GitHub Issues
- 📧 **Email:** Contact maintainers (see README)
- 📖 **Docs:** Check documentation first

## 🙏 Recognition

Contributors will be recognized in:

- CONTRIBUTORS.md file
- Release notes
- Project README

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to EDC Group Permission Automation! 🎉

````

## Quick Reference

```bash
# Setup
git clone <fork>
cd edc-group-automation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Develop
git checkout -b feature/my-feature
# Make changes
git add .
git commit -m "feat: add new feature"

# Test
python -m unittest discover tests/

# Submit
git push origin feature/my-feature
# Create PR on GitHub
````
