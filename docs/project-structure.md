# Project Structure

**Project:** AutoZipBackup

**Version:** 1.0

**Status:** Approved

**Last Update:** 2026-08-06

---

# 1. Purpose

This document defines the official directory structure of the AutoZipBackup project.

Every source file must be placed according to the rules described here.

A consistent folder structure improves:

- Readability
- Maintainability
- Discoverability
- Scalability

---

# 2. Root Directory

```
AutoZipBackup/
│
├── app.py
├── pyproject.toml
├── requirements.txt
├── settings.json
├── README.md
├── LICENSE
├── .gitignore
│
├── docs/
├── src/
├── tests/
├── backups/
└── logs/
```

The root directory only contains project-level files.

Business logic is never placed here.

---

# 3. app.py

Application entry point.

Responsibilities

- Initialize the application
- Configure logging
- Load settings
- Build the dependency graph
- Create the main window
- Start the GUI loop

Forbidden

- Business logic
- ZIP operations
- Scheduler logic
- File manipulation

---

# 4. docs/

Contains all project documentation.

```
docs/
│
├── architecture.md
├── coding-standards.md
├── development-environment.md
├── project-structure.md
├── roadmap.md
├── changelog.md
├── decisions.md
│
└── adr/
```

No Python files belong here.

---

# 5. src/

Contains the application source code.

```
src/
└── autozip/
```

Only application code is stored here.

---

# 6. backup/

```
backup/
│
├── backup_service.py
├── zip_service.py
├── checksum_service.py
├── restore_service.py
└── models.py
```

Responsibilities

- Backup execution
- ZIP creation
- Restore
- SHA256 verification

Forbidden

- GUI code
- Scheduler configuration

---

# 7. scheduler/

```
scheduler/
│
├── scheduler_service.py
├── task_executor.py
└── models.py
```

Responsibilities

- APScheduler
- Job management
- Daily execution
- Schedule validation

Forbidden

- ZIP creation
- File compression

---

# 8. settings/

```
settings/
│
├── settings_service.py
├── models.py
└── validator.py
```

Responsibilities

- Load settings
- Save settings
- Validate configuration
- Application settings model

Only this module may access settings.json.

---

# 9. localization/

```
localization/
│
├── language_service.py
└── translator.py
```

Responsibilities

- Load translations
- Switch language
- Translate UI strings

Forbidden

- UI widgets
- Business logic

---

# 10. ui/

Contains the graphical interface.

```
ui/
│
├── views/
│
├── widgets/
│
└── dialogs/
```

Responsibilities

- Windows
- Dialogs
- Custom widgets

Forbidden

- ZIP logic
- Scheduler logic
- Settings persistence

The UI displays information only.

---

# 11. common/

Contains shared components.

```
common/
│
├── logger.py
├── constants.py
├── exceptions.py
├── events.py
├── helpers.py
└── types.py
```

Responsibilities

- Logging
- Shared constants
- Common exceptions
- Event definitions
- Utility helpers

Common modules must not depend on feature modules.

---

# 12. resources/

Contains application resources.

```
resources/
│
├── icons/
├── images/
├── themes/
└── fonts/
```

Only static resources belong here.

---

# 13. languages/

Contains translation files.

```
languages/
│
├── es.json
└── en.json
```

Each language file must contain exactly the same keys.

---

# 14. tests/

```
tests/
│
├── backup/
├── scheduler/
├── settings/
├── localization/
└── common/
```

The test structure mirrors the source structure whenever practical.

Every service should have unit tests.

---

# 15. backups/

Stores generated ZIP files.

The application creates this directory automatically.

No source code belongs here.

---

# 16. logs/

Stores application log files.

Example

```
logs/

autozip.log
```

The directory is created automatically.

---

# 17. Import Rules

Allowed

```
ui

↓

backup

↓

common
```

Forbidden

```
backup

↓

ui
```

Business modules never depend on the graphical interface.

---

# 18. File Naming Convention

Python files

snake_case.py

Examples

```
backup_service.py

settings_service.py

main_window.py
```

Classes

PascalCase

Examples

```
BackupService

Logger

SettingsManager
```

Methods

snake_case

Variables

snake_case

Constants

UPPER_CASE

---

# 19. Maximum Module Size

Recommended

300 lines

Maximum

500 lines

Split larger modules.

---

# 20. One Responsibility Per File

Whenever practical

One class

↓

One file

Exceptions

- Enumerations
- Small DTOs
- Related dataclasses

---

# 21. Directory Creation Rules

The application creates automatically

- backups/
- logs/

Never require the user to create them manually.

---

# 22. Future Growth

Future modules should follow the same organizational principles.

Possible additions

```
notifications/

cloud/

plugins/

encryption/

database/
```

Existing folders should not be reorganized.

---

# 23. Directory Ownership

Folder | Owner
-------|------------------------
backup | Backup subsystem
scheduler | Scheduling subsystem
settings | Configuration subsystem
localization | Translation subsystem
ui | Presentation layer
common | Shared infrastructure
resources | Static assets
tests | Test suite
docs | Documentation

Ownership helps define responsibilities and avoid coupling.

---

# 24. Project Organization Principles

The project structure follows these principles

- Feature-oriented organization
- Low coupling
- High cohesion
- Clear ownership
- Explicit responsibilities
- Easy navigation
- Scalable growth

---

# End of Document