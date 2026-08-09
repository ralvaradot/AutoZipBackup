# Decisions

**Project:** AutoZipBackup

**Version:** 1.0

**Status:** Active

**Last Update:** 2026-08-06

---

# Purpose

This document records engineering decisions that do not justify an Architecture Decision Record (ADR), but must be consistently followed throughout the project.

These decisions are considered mandatory development standards.

---

# General Rules

## D-001 Architecture Freeze

The project architecture is frozen.

No architectural changes shall be introduced unless a technical limitation prevents fulfilling a functional requirement.

Minor refactoring is allowed.

Folder restructuring is not allowed.

---

## D-002 Single Responsibility

Every class must have only one responsibility.

If a class starts having multiple responsibilities, it must be split.

---

## D-003 Dependency Direction

UI

↓

Services

↓

Repositories

↓

Filesystem

Dependencies must always point downward.

Lower layers must never know upper layers.

---

## D-004 Business Logic

Business logic shall never be implemented inside the UI.

Views only display information.

Views never make business decisions.

---

## D-005 Configuration

The application loads the configuration once during startup.

Configuration remains in memory.

Changes are persisted only when requested.

---

## D-006 Logging

Every important operation must be logged.

Examples:

Application startup

Configuration loading

Backup started

Backup finished

Backup failed

ZIP creation

ZIP verification

Restore operation

Unexpected exceptions

---

## D-007 Exceptions

Never ignore exceptions.

Never use:

except:
    pass

Always log exceptions.

Whenever possible raise custom exceptions.

---

## D-008 Type Hints

Every public function must include type hints.

Example

def save(settings: AppSettings) -> None

---

## D-009 Docstrings

Public classes

Public methods

Public modules

must contain docstrings.

Private methods are optional.

---

## D-010 Path Handling

Never concatenate paths manually.

Forbidden

"C:\\Folder\\" + filename

Required

pathlib.Path

---

## D-011 Constants

Magic numbers are forbidden.

Every constant belongs in constants.py.

---

## D-012 Strings

User interface strings must never be hardcoded.

All visible text belongs in:

languages/es.json

languages/en.json

---

## D-013 Thread Safety

Long-running operations must never execute in the UI thread.

Examples

ZIP

Restore

Verification

SHA256

---

## D-014 Scheduler

The Scheduler never performs backups directly.

Scheduler

↓

TaskExecutor

↓

BackupService

---

## D-015 Compression

Compression logic belongs only inside ZipService.

No other class shall use zipfile directly.

---

## D-016 Logging Responsibility

Only LoggerService accesses the logging package.

No other class creates loggers.

---

## D-017 Configuration Responsibility

Only SettingsService reads or writes settings.json.

---

## D-018 UI Updates

Background threads never update widgets directly.

Communication must use events.

---

## D-019 Event Driven

Important operations publish events.

Examples

BackupStarted

BackupProgress

BackupCompleted

BackupFailed

---

## D-020 Naming

Classes

PascalCase

Variables

snake_case

Methods

snake_case

Constants

UPPER_CASE

Private attributes

_prefix

---

## D-021 Imports

Imports order

Python Standard Library

Third-party Libraries

Internal Modules

---

## D-022 Maximum Function Size

Functions should preferably remain below 40 lines.

Maximum acceptable

60 lines

Beyond that consider refactoring.

---

## D-023 Maximum Class Size

Target

300 lines

Maximum

500 lines

Beyond that split responsibilities.

---

## D-024 Backup Verification

Every generated ZIP should optionally be verified.

Verification must be independent of compression.

---

## D-025 Future Features

Future requirements must not modify existing architecture.

Extend.

Never rewrite.

---

## D-026 Testing

Business logic must be testable without opening the UI.

---

## D-027 Comments

Explain WHY.

Never explain WHAT.

Bad

Increment i

Good

Retry because Windows may temporarily lock ZIP files.

---

## D-028 Logging Levels

DEBUG

Development only

INFO

Normal operations

WARNING

Recoverable issues

ERROR

Failures

CRITICAL

Application integrity compromised

---

## D-029 Encoding

UTF-8 everywhere.

Without exception.

---

## D-030 Formatting

Maximum line length

100 characters

Trailing whitespace forbidden.

---

## D-031 File Organization

One class per file whenever practical.

Avoid utility files with unrelated functionality.

---

## D-032 Future Compatibility

Code should remain compatible with future modules.

Cloud backup

Encryption

Compression algorithms

Notification providers

Database logging

---

## D-033 Performance

Readability first.

Premature optimization is forbidden.

Optimize only after measuring.

---

## D-034 Security

Never delete user files automatically.

Never overwrite existing ZIP files without confirmation or explicit configuration.

---

## D-035 Development Philosophy

Simple solutions over clever solutions.

Readable code over short code.

Maintainability over premature optimization.

Consistency over personal preference.

---

# End of Document