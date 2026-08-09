# Coding Standards

**Project:** AutoZipBackup

**Version:** 1.0

**Status:** Approved

**Last Update:** 2026-08-06

---

# 1. Purpose

This document defines the coding standards for the AutoZipBackup project.

All contributors must follow these rules to ensure that the codebase remains:

- Consistent
- Readable
- Maintainable
- Testable
- Predictable

These standards apply to every Python source file.

---

# 2. Python Version

The project targets:

Python 3.13+

Do not introduce compatibility code for older versions unless explicitly approved.

---

# 3. Code Formatting

Formatting is enforced automatically.

Configuration:

- Ruff Formatter
- Ruff Linter

Maximum line length:

100 characters

Never manually align code using extra spaces.

---

# 4. Naming Conventions

## Classes

Use PascalCase.

Examples

```python
class BackupService:
    ...

class SettingsManager:
    ...
```

---

## Functions and Methods

Use snake_case.

```python
def execute_backup() -> None:
    ...

def load_settings() -> AppSettings:
    ...
```

---

## Variables

Use snake_case.

```python
backup_path = Path(...)
zip_file = Path(...)
```

Avoid abbreviations unless universally recognized.

Good

```python
destination_folder
compression_level
```

Bad

```python
dst
cmp_lvl
```

---

## Constants

Use UPPER_CASE.

```python
DEFAULT_LANGUAGE = "es"
DEFAULT_THEME = "darkly"
MAX_LOG_FILES = 10
```

---

## Private Members

Prefix with a single underscore.

```python
self._logger
self._settings
```

---

# 5. Type Hints

All public functions must include type hints.

Good

```python
def save(settings: AppSettings) -> None:
    ...
```

Bad

```python
def save(settings):
    ...
```

Return types are mandatory.

---

# 6. Docstrings

Every public:

- Module
- Class
- Function
- Method

must include a docstring.

Use Google Style.

Example

```python
def load_settings() -> AppSettings:
    """Load application settings from disk.

    Returns:
        AppSettings: Loaded application configuration.
    """
```

Private methods may omit docstrings if their intent is obvious.

---

# 7. Imports

Import order:

1. Standard Library
2. Third-party Libraries
3. Local Project Imports

Example

```python
from pathlib import Path

import ttkbootstrap as ttk

from autozip.settings.settings_service import SettingsService
```

Wildcard imports are forbidden.

```python
from module import *
```

---

# 8. Comments

Comments explain WHY.

Never explain WHAT.

Bad

```python
# Increment counter
counter += 1
```

Good

```python
# Retry because Windows may temporarily lock ZIP files.
```

---

# 9. Function Size

Recommended:

≤ 40 lines

Maximum:

60 lines

Large functions should be decomposed into smaller ones.

---

# 10. Class Size

Recommended:

≤ 300 lines

Maximum:

500 lines

If exceeded, split responsibilities.

---

# 11. Error Handling

Never ignore exceptions.

Forbidden

```python
except:
    pass
```

Good

```python
except OSError as ex:
    logger.exception(ex)
    raise
```

Catch the most specific exception possible.

---

# 12. Logging

Do not use print() for diagnostics.

Use LoggerService.

Good

```python
logger.info("Backup started.")
```

Bad

```python
print("Backup started")
```

Logging levels:

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

---

# 13. Paths

Use pathlib.Path exclusively.

Good

```python
backup_folder = Path("backups")
zip_file = backup_folder / filename
```

Bad

```python
backup_folder = "backups\\" + filename
```

---

# 14. Magic Numbers

Magic numbers are forbidden.

Bad

```python
if retries == 3:
```

Good

```python
MAX_RETRIES = 3

if retries == MAX_RETRIES:
```

---

# 15. Strings

User-visible text must never be hardcoded.

Good

```python
translator.get("backup_completed")
```

Bad

```python
label.config(text="Backup completed")
```

---

# 16. Thread Safety

The UI thread must never execute long-running operations.

Background tasks:

- ZIP creation
- Restore
- Checksum
- File copy

Workers communicate with the UI through events.

---

# 17. Single Responsibility Principle

Every class should have one reason to change.

If a class manages:

- ZIP
- Logging
- Settings

it should be split.

---

# 18. Dependency Direction

Dependencies flow downward.

```
UI
↓
Services
↓
Infrastructure
```

Lower layers never reference upper layers.

---

# 19. Testing

Business logic must be testable without creating a graphical interface.

Tests should avoid external dependencies whenever possible.

---

# 20. Performance

Readability is preferred over premature optimization.

Optimize only after measuring.

---

# 21. File Encoding

All source files:

UTF-8

Line endings:

LF

---

# 22. File Organization

Prefer:

One public class per file.

Small related dataclasses or enums may share a file.

---

# 23. TODO Comments

Use TODO comments sparingly.

Format

```python
# TODO(username): Short description.
```

Example

```python
# TODO(ralvaradot): Support encrypted ZIP archives.
```

---

# 24. Code Reviews

Every change should be evaluated according to:

- Correctness
- Readability
- Simplicity
- Maintainability
- Testability

Personal preferences should never override project standards.

---

# 25. Development Philosophy

Prefer:

- Explicit over implicit
- Readability over cleverness
- Composition over inheritance
- Small modules over large modules
- Stable APIs over frequent changes

---

# 26. Boy Scout Rule

Whenever modifying a file:

- Improve names
- Remove dead code
- Reduce duplication
- Improve documentation
- Keep behavior unchanged

Always leave the code better than you found it.

---

# 27. Definition of Done

A task is considered complete only if:

- The code builds successfully.
- Type hints are present.
- Ruff reports no issues.
- Unit tests pass.
- Documentation is updated if required.
- Logging has been added where appropriate.
- No TODOs remain unless explicitly accepted.

---

# End of Document