# ADR-010 — Error Handling Strategy

**Project:** AutoZipBackup

**ADR:** 010

**Status:** Accepted

**Date:** 2026-08-06

**Decision Maker:** Project Architecture Team

**Supersedes:** None

**Superseded By:** None

---

# 1. Context

AutoZipBackup interacts with the operating system, the file system, background workers, scheduled tasks and external libraries.

These interactions may generate many different exceptions.

The application must handle failures consistently while presenting understandable information to the user.

---

# 2. Problem Statement

Allowing low-level exceptions to propagate throughout the application creates several problems.

Examples:

- UI displays technical messages.
- Business logic depends on OS exceptions.
- Error handling becomes inconsistent.
- Testing becomes more difficult.
- Logging varies across modules.

A unified error handling strategy is required.

---

# 3. Decision Drivers

The solution must:

- Centralize error handling.
- Hide implementation details.
- Produce user-friendly messages.
- Preserve technical diagnostics.
- Improve testability.
- Support localization.
- Reduce coupling.

---

# 4. Alternatives Considered

## Alternative A — Native Python Exceptions

Services raise built-in exceptions.

Examples

```
FileNotFoundError

PermissionError

OSError
```

### Advantages

- No additional classes.
- Standard Python behavior.

### Disadvantages

- High coupling.
- Poor user experience.
- Difficult localization.
- Difficult testing.

### Decision

Rejected.

---

## Alternative B — Generic Exception

```
raise Exception(...)
```

### Advantages

Simple.

### Disadvantages

No semantic meaning.

Impossible to distinguish failures.

Poor maintainability.

### Decision

Rejected.

---

## Alternative C — Domain Exceptions

Application-specific exceptions represent business failures.

Low-level exceptions are translated before leaving the infrastructure layer.

### Advantages

- Clear intent.
- Better architecture.
- Easier testing.
- Better localization.
- Cleaner UI.

### Decision

Accepted.

---

# 5. Decision

The application adopts a layered exception hierarchy.

```
Operating System

↓

Python Exceptions

↓

ExceptionMapper

↓

Application Exceptions

↓

UI
```

The presentation layer never receives raw operating system exceptions.

---

# 6. Exception Hierarchy

```
ApplicationError

├── BackupError

├── SchedulerError

├── ConfigurationError

├── LocalizationError

├── ValidationError

├── CompressionError

├── VerificationError

└── UnexpectedApplicationError
```

Every application exception derives from `ApplicationError`.

---

# 7. ExceptionMapper

Responsibilities

- Catch low-level exceptions.
- Translate exceptions into domain exceptions.
- Preserve original exception information.
- Maintain exception chaining.

Example

```
PermissionError

↓

BackupError
```

---

# 8. ErrorPresenter

Responsibilities

- Convert exceptions into localized messages.
- Select appropriate dialog type.
- Prevent technical details from reaching end users.

Example

Instead of:

```
PermissionError: WinError 5
```

Display:

```
The application does not have permission to access the selected folder.
```

---

# 9. Logging

Every unexpected exception must be logged.

Logs include:

- Timestamp
- Exception type
- Message
- Stack trace
- Related task identifier (when available)

User messages remain concise.

Logs preserve technical details.

---

# 10. Localization

User-visible error messages are translated through the localization subsystem.

Example translation keys

```
error_permission_denied

error_invalid_folder

error_zip_creation_failed

error_configuration_invalid
```

Exception classes never contain localized text.

---

# 11. Error Recovery

Whenever possible, the application should recover gracefully.

Examples

- Invalid configuration → load defaults.
- Missing log directory → create it.
- Missing backup folder → notify the user.
- Scheduler failure → disable scheduler while keeping the UI available.

Unexpected failures should never terminate the application without first being logged.

---

# 12. Thread Safety

Worker threads report failures through domain exceptions.

Exceptions are transformed into events before reaching the UI.

Background threads never display dialogs directly.

---

# 13. Event Integration

Application failures generate events.

Examples

```
BackupFailed

ConfigurationLoadFailed

SchedulerFailed

UnexpectedError
```

The UI reacts to events instead of catching worker thread exceptions.

---

# 14. Future Extensions

The architecture supports:

- Error telemetry.
- Crash reports.
- Automatic diagnostics.
- Online error reporting.
- AI-assisted troubleshooting.

No architectural changes are required.

---

# 15. Consequences

## Positive

- Consistent error handling.
- Better user experience.
- Localized messages.
- Easier testing.
- Reduced coupling.
- Better maintainability.

## Negative

- Additional classes.
- Exception mapping layer.

---

# 16. Compliance Rules

Every code review should verify:

- Business modules raise only ApplicationError subclasses.
- Infrastructure exceptions are translated.
- UI never displays raw Python exceptions.
- Exceptions are logged before propagation.
- User messages come from localization resources.
- Generic `except Exception:` blocks are used only at application boundaries.

---

# 17. Risks

Potential risks

- Incomplete exception mapping.
- Hidden programming errors.
- Duplicate error messages.

Mitigation

- Unit tests for exception mapping.
- Preserve exception chaining.
- Centralized presentation layer.

---

# 18. Impact

**Impact Level:** High

This ADR defines the official error handling strategy for AutoZipBackup.

All future modules must adopt this exception model.

---

# 19. Related Documents

- architecture.md
- coding-standards.md
- ADR-001 Project Architecture
- ADR-003 Configuration Management
- ADR-004 Logging Strategy
- ADR-005 Event Dispatcher Architecture
- ADR-007 Localization Strategy
- ADR-009 Backup Engine Architecture

---

# 20. Revision History

| Date | Version | Description |
|------|---------|-------------|
| 2026-08-06 | 1.0 | Initial version. Approved. |

---

# End of Document