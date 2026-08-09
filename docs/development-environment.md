# Development Environment

**Project:** AutoZipBackup

**Version:** 1.0

**Status:** Approved

**Last Update:** 2026-08-06

---

# 1. Purpose

This document describes the official development environment for the AutoZipBackup project.

All contributors should use this configuration to ensure a consistent development experience across different machines.

---

# 2. Supported Operating Systems

Development is officially supported on:

- Windows 11 (Primary)
- Windows 10
- Ubuntu 24.04 LTS (Experimental)
- macOS 15+ (Experimental)

The application is primarily designed for Windows.

---

# 3. Python Version

Required version:

Python **3.13.x**

Verify your installation:

```bash
python --version
```

Expected output:

```text
Python 3.13.x
```

---

# 4. Recommended IDE

The recommended IDE is:

**Visual Studio Code**

Download:

https://code.visualstudio.com/

Other supported IDEs:

- PyCharm Professional
- PyCharm Community

---

# 5. Recommended Visual Studio Code Extensions

Install the following extensions before starting development.

### Python

Publisher

Microsoft

---

### Pylance

Publisher

Microsoft

Provides IntelliSense and type analysis.

---

### Ruff

Publisher

Astral Software

Provides:

- Formatting
- Linting
- Import organization

---

### GitLens

Improves Git history visualization.

---

### Error Lens

Displays diagnostics inline.

---

### Better Comments

Improves code comment readability.

---

### Markdown All in One

Recommended for editing project documentation.

---

# 6. Clone Repository

```bash
git clone https://github.com/ralvaradot/AutoZipBackup.git
```

Enter the project:

```bash
cd AutoZipBackup
```

---

# 7. Virtual Environment

Create a virtual environment.

Windows

```bash
python -m venv .venv
```

Activate

PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Command Prompt

```cmd
.venv\Scripts\activate.bat
```

Linux/macOS

```bash
source .venv/bin/activate
```

---

# 8. Install Dependencies

Upgrade pip.

```bash
python -m pip install --upgrade pip
```

Install project dependencies.

```bash
pip install -e .
```

Install development tools.

```bash
pip install -e .[dev]
```

---

# 9. Verify Installation

Verify Ruff

```bash
ruff --version
```

Verify mypy

```bash
mypy --version
```

Verify pytest

```bash
pytest --version
```

---

# 10. Running the Application

Execute

```bash
python app.py
```

During early development, the application may only display a basic window while features are implemented incrementally.

---

# 11. Running Tests

Execute all tests.

```bash
pytest
```

Run a specific test.

```bash
pytest tests/settings
```

Generate coverage report.

```bash
pytest --cov=src
```

---

# 12. Static Analysis

Run Ruff.

```bash
ruff check .
```

Automatically fix issues when possible.

```bash
ruff check . --fix
```

Format the project.

```bash
ruff format .
```

---

# 13. Type Checking

Run mypy.

```bash
mypy src
```

All new code should pass type checking.

---

# 14. Recommended Workflow

Before starting work:

```bash
git pull
```

Create a feature branch.

```bash
git checkout -b feature/backup-engine
```

Implement changes.

Run:

```bash
ruff check .
ruff format .
mypy src
pytest
```

Commit.

Push.

Create Pull Request.

---

# 15. Git Commit Convention

Use Conventional Commits.

Examples

```text
feat: add backup service

fix: correct scheduler execution

docs: update architecture

test: add settings unit tests

refactor: simplify logger

chore: update dependencies
```

---

# 16. Project Directories

The following directories are automatically created by the application if they do not exist.

```text
logs/

backups/
```

Do not create them manually unless necessary.

---

# 17. Line Endings

Source files

LF

Markdown

LF

JSON

LF

UTF-8 encoding.

---

# 18. Source Formatting

Maximum line length

100 characters

Indentation

4 spaces

Tabs are forbidden.

---

# 19. Debugging

Use the Visual Studio Code debugger.

Do not insert temporary print() statements.

Use logging instead.

---

# 20. Logging During Development

Preferred levels

DEBUG

Development diagnostics

INFO

Normal operations

WARNING

Recoverable issues

ERROR

Unexpected failures

CRITICAL

Application integrity compromised

---

# 21. Pull Request Checklist

Before opening a Pull Request verify:

- Project builds successfully.
- Ruff reports no issues.
- Code is formatted.
- Type hints are complete.
- Tests pass.
- Documentation is updated.
- No debug code remains.
- No commented-out code remains.

---

# 22. Backup Test Data

Never commit:

- Generated ZIP files
- Temporary files
- Log files
- Personal documents

Use synthetic test data only.

---

# 23. Security

Never commit:

- Credentials
- API keys
- Passwords
- Personal information

Sensitive configuration must never be stored in the repository.

---

# 24. Updating Dependencies

Before upgrading dependencies:

- Review release notes.
- Verify compatibility with Python 3.13.
- Run the complete test suite.
- Update documentation if required.

---

# 25. Definition of a Healthy Development Environment

A correctly configured environment satisfies:

- Python 3.13 installed.
- Virtual environment active.
- Dependencies installed.
- Ruff passes.
- mypy passes.
- Tests pass.
- Application starts successfully.

---

# End of Document