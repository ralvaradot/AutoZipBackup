# Roadmap

**Project:** AutoZipBackup

**Version:** 1.0

**Status:** Active

**Last Update:** 2026-08-06

---

# 1. Purpose

This roadmap defines the planned evolution of the AutoZipBackup project.

It serves as the official planning document for future releases and helps ensure that new functionality is implemented in a controlled and predictable manner.

The roadmap may evolve over time, but completed milestones should never be modified.

---

# 2. Project Vision

AutoZipBackup aims to become a modern, reliable and extensible desktop application for automated file backups.

The application should provide:

- Simple configuration
- Reliable execution
- Professional logging
- Easy restoration
- Modern user interface
- High maintainability
- Future extensibility

---

# 3. Guiding Principles

Every new feature should satisfy at least one of the following goals:

- Improve usability
- Improve reliability
- Improve maintainability
- Improve performance
- Improve security
- Improve extensibility

Features that do not contribute to these goals should be carefully evaluated before implementation.

---

# 4. Current Status

Current Version

```
v1.0.0
```

Project Phase

```
Foundation
```

Current Sprint

```
Sprint 1
```

Architecture Status

```
Frozen
```

---

# 5. Release Plan

| Version | Status | Objective |
|----------|--------|-----------|
| 1.0 | In Development | Core desktop application |
| 1.1 | Planned | Usability improvements |
| 1.2 | Planned | Backup enhancements |
| 1.5 | Planned | Enterprise features |
| 2.0 | Vision | Cloud-ready architecture |

---

# 6. Version 1.0

## Goal

Deliver a stable desktop application capable of performing scheduled ZIP backups.

---

### Epic 1

Project Foundation

Status

Completed when:

- Project structure
- Documentation
- Logging
- Configuration
- Development environment

---

### Epic 2

Application Configuration

Features

- Settings management
- Persistent configuration
- Validation
- Theme selection
- Language selection

---

### Epic 3

Localization

Features

- Spanish
- English
- Runtime language switching

---

### Epic 4

Themes

Features

- Dark mode
- Light mode
- Theme persistence

---

### Epic 5

Backup Engine

Features

- Folder selection
- ZIP generation
- Timestamp naming
- Compression
- Destination folder

---

### Epic 6

Scheduler

Features

- Daily execution
- Enable/disable tasks
- Manual execution
- Startup scheduling

---

### Epic 7

Logging

Features

- File logging
- Log rotation
- Error logging
- Debug mode

---

### Epic 8

Main User Interface

Features

- Dashboard
- Task list
- Toolbar
- Status bar
- Progress dialog

---

### Epic 9

Restore

Features

- Restore ZIP
- Destination selection
- Validation

---

### Epic 10

Testing

Features

- Unit tests
- Integration tests
- Manual test checklist

---

# 7. Version 1.1

Goal

Improve user experience.

Planned Features

- Recent folders
- Search tasks
- Duplicate task
- Better notifications
- Improved dialogs
- Keyboard shortcuts
- Better progress window

---

# 8. Version 1.2

Goal

Improve backup reliability.

Planned Features

- SHA256 verification
- Backup history
- Retry mechanism
- Backup validation
- File filters
- Excluded folders
- Compression levels

---

# 9. Version 1.5

Goal

Advanced functionality.

Planned Features

- Multiple backup profiles
- Backup templates
- Scheduled cleanup
- Export configuration
- Import configuration
- Portable mode

---

# 10. Version 2.0

Long-term vision.

Possible Features

- Cloud storage
- Plugin system
- Encryption
- Incremental backups
- Differential backups
- Command-line interface
- REST API
- Windows Service
- Linux Service

---

# 11. Technical Debt

Current Known Debt

None.

Technical debt should be documented before implementation whenever possible.

---

# 12. Risks

Current Risks

- Operating system file locking
- Very large folders
- Long-running operations
- Unexpected shutdown during backup

Mitigation strategies will be documented as they are implemented.

---

# 13. Success Metrics

Version 1.0 is considered complete when:

- Scheduled backups work reliably.
- Manual backups work correctly.
- Restore works correctly.
- Logging is complete.
- Localization is functional.
- Themes can be switched.
- Unit tests pass.
- Documentation is complete.

---

# 14. Sprint Strategy

Each sprint should include:

- New functionality
- Unit tests
- Documentation updates
- Logging improvements
- Refactoring (if necessary)

Every sprint must produce a working application.

---

# 15. Out of Scope (Version 1.x)

The following features are intentionally excluded from version 1.x:

- Cloud synchronization
- Network backup
- Database storage
- Mobile application
- Web interface
- User authentication
- Collaborative features

---

# 16. Release Policy

Patch Releases

```
1.0.1
```

Bug fixes only.

Minor Releases

```
1.1
```

Backward-compatible new features.

Major Releases

```
2.0
```

Breaking architectural changes.

Semantic Versioning (SemVer) will be followed.

---

# 17. Quality Gates

No release shall be published unless:

- All tests pass.
- No critical bugs remain.
- Documentation is updated.
- Ruff reports no issues.
- Type checking passes.
- Logging has been verified.
- Manual validation has been completed.

---

# 18. Long-Term Vision

AutoZipBackup should remain:

- Simple
- Stable
- Predictable
- Extensible
- Easy to maintain

Growth should occur through well-defined modules rather than architectural rewrites.

---

# End of Document