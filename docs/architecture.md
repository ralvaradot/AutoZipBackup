# Architecture

**Project:** AutoZipBackup

**Version:** 1.0

**Status:** Approved

**Last Update:** 2026-08-06

---

# 1. Purpose

AutoZipBackup is a desktop application developed in Python that automates the creation of scheduled ZIP backups through a modern graphical interface built with ttkbootstrap.

The application is designed to be reliable, maintainable, extensible and easy to understand.

This document defines the official software architecture for the project.

The architecture described here is considered frozen for version 1.x.

---

# 2. Architectural Goals

The project has the following objectives.

- Maintainability
- Readability
- Extensibility
- Low coupling
- High cohesion
- Testability
- Simplicity

Every architectural decision must support these goals.

---

# 3. Architectural Style

AutoZipBackup adopts a **Service-Oriented Modular Architecture**.

The system is organized into independent functional modules.

Each module owns its own business logic and exposes services to the rest of the application.

The graphical user interface is intentionally thin.

Business rules are never implemented inside the UI.

---

# 4. High-Level Architecture

```
                   +---------------------------+
                   |      User Interface       |
                   |       ttkbootstrap        |
                   +------------+--------------+
                                |
                                v
                   +---------------------------+
                   |         Services          |
                   | Backup / Settings / Logs  |
                   +------------+--------------+
                                |
                                v
                   +---------------------------+
                   |      Infrastructure       |
                   | ZIP / Scheduler / Files   |
                   +------------+--------------+
                                |
                                v
                   +---------------------------+
                   |      Operating System     |
                   +---------------------------+
```

The UI never communicates directly with the operating system.

All interactions occur through services.

---

# 5. Project Structure

```
AutoZipBackup/
│
├── app.py
├── pyproject.toml
├── settings.json
│
├── docs/
│
├── src/
│   └── autozip/
│       │
│       ├── backup/
│       ├── scheduler/
│       ├── settings/
│       ├── localization/
│       ├── ui/
│       ├── common/
│       └── resources/
│
├── backups/
├── logs/
└── tests/
```

---

# 6. Module Responsibilities

## backup

Responsible for every backup-related operation.

Responsibilities

- ZIP creation
- Backup execution
- Integrity verification
- Restore
- Compression

---

## scheduler

Responsible for scheduled execution.

Responsibilities

- APScheduler configuration
- Daily jobs
- Startup scheduling
- Stop scheduling

The scheduler never performs backups directly.

---

## settings

Responsible for application configuration.

Responsibilities

- Load settings
- Save settings
- Validate configuration
- Manage application state

Only this module accesses settings.json.

---

## localization

Responsible for language management.

Responsibilities

- Load translations
- Switch language
- Provide localized strings

---

## ui

Responsible only for presentation.

Responsibilities

- Windows
- Dialogs
- Widgets
- User interaction

No business rules belong here.

---

## common

Contains shared components.

Examples

- Logger
- Exceptions
- Constants
- Events
- Utilities

---

## resources

Application resources.

Examples

Icons

Images

Themes

Fonts

---

# 7. Dependency Rules

Dependencies always move in one direction.

```
UI

↓

Services

↓

Infrastructure

↓

Filesystem
```

Lower layers never reference upper layers.

Circular dependencies are forbidden.

---

# 8. Event Flow

Long-running operations communicate through events.

Example

```
User clicks Backup

↓

BackupService

↓

BackupStarted

↓

ProgressChanged

↓

BackupCompleted

↓

UI updates
```

The UI never polls background operations.

---

# 9. Threading Model

The graphical interface always runs on the main thread.

Heavy operations execute in worker threads.

Examples

- ZIP creation
- Restore
- SHA256 calculation
- Large file operations

Workers never manipulate widgets directly.

---

# 10. Configuration

Application settings are loaded once during startup.

Configuration remains in memory.

Changes are written only when explicitly saved.

Configuration is represented by typed Python objects.

---

# 11. Logging

Every relevant operation generates log entries.

Logging is centralized.

No module creates its own logger.

Log levels

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

---

# 12. Error Handling

Unexpected exceptions are never ignored.

Exceptions are

- Logged
- Reported
- Converted into user-friendly messages

Whenever appropriate, custom exceptions are preferred.

---

# 13. Localization

All user-visible text is externalized.

Language files

```
languages/

    es.json

    en.json
```

No hardcoded UI strings are allowed.

---

# 14. Themes

The UI supports runtime theme switching.

Initial themes

- Darkly
- Flatly
- Superhero
- Cosmo
- Litera

The selected theme is persisted.

---

# 15. Backup Workflow

```
User

↓

BackupService

↓

Validation

↓

Compression

↓

Verification

↓

Move ZIP

↓

Logging

↓

Notification

↓

Completed
```

Each step has a single responsibility.

---

# 16. Scheduler Workflow

```
Application

↓

Scheduler

↓

TaskExecutor

↓

BackupService
```

The scheduler never performs ZIP operations directly.

---

# 17. Design Principles

The project follows these principles.

- Single Responsibility Principle
- Separation of Concerns
- Composition over Inheritance
- Explicit Dependencies
- Small Modules
- Readable Code

---

# 18. Performance

Readability is prioritized over micro-optimizations.

Optimization occurs only after measuring.

Large backups execute outside the UI thread.

---

# 19. Testing Strategy

Business logic must be testable independently of the graphical interface.

The UI is considered an integration layer.

Unit tests focus on services.

---

# 20. Future Extension Points

The architecture intentionally allows future support for

- Cloud storage
- Encryption
- Multiple compression algorithms
- Database logging
- Windows Service
- Command Line Interface
- Notification providers
- Plugin system

These features must be added without modifying existing modules.

---

# 21. Architecture Freeze

The architecture defined in this document is frozen for version 1.x.

Future architectural changes require a new Architecture Decision Record (ADR).

---

# End of Document