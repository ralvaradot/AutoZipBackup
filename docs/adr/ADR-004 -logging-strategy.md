# ADR-004 — Logging Strategy

**Project:** AutoZipBackup

**ADR:** 004

**Status:** Accepted

**Date:** 2026-08-06

**Decision Maker:** Project Architecture Team

**Supersedes:** None

**Superseded By:** None

---

# 1. Context

AutoZipBackup performs long-running operations involving the operating system,
file compression, scheduling and configuration management.

To diagnose failures, audit application behavior and support future maintenance,
a centralized logging strategy is required.

Logging must be:

- Consistent
- Structured
- Configurable
- Extensible
- Independent from business logic

---

# 2. Problem Statement

If every module creates and configures its own logger:

- Log formats become inconsistent.
- Multiple handlers may be registered accidentally.
- Log files become fragmented.
- Configuration is duplicated.
- Maintenance becomes difficult.

A centralized logging architecture is required.

---

# 3. Decision Drivers

The logging solution must:

- Use a single configuration.
- Produce consistent output.
- Support multiple destinations.
- Be thread-safe.
- Be easy to test.
- Avoid duplicated configuration.
- Allow future extensions.

---

# 4. Alternatives Considered

## Alternative A — Direct use of Python logging

Each module creates its own logger.

```python
logger = logging.getLogger(__name__)
```

### Advantages

- Very simple.
- Standard library.

### Disadvantages

- Configuration duplicated.
- Difficult to control handlers.
- Risk of inconsistent formatting.

### Decision

Rejected.

---

## Alternative B — Static LoggerService

```
LoggerService.info(...)
```

### Advantages

- Easy to use.

### Disadvantages

- Hidden global dependency.
- Difficult to mock.
- Difficult unit testing.

### Decision

Rejected.

---

## Alternative C — Logger + LogManager

A LogManager configures the logging subsystem.

Logger instances are injected into services.

### Advantages

- Single configuration.
- Easy testing.
- Extensible.
- Clean architecture.
- Supports Dependency Injection.

### Decision

Accepted.

---

# 5. Decision

The project adopts the following logging architecture.

```
Application

↓

LogManager

↓

Logger

↓

Handlers

↓

File / Console / Future Providers
```

Business modules never configure logging.

They only consume a logger.

---

# 6. Components

## LogManager

Responsibilities

- Configure logging.
- Register handlers.
- Configure formatters.
- Configure log level.
- Configure rotation.

Created once during application startup.

---

## Logger

Responsibilities

- Record log messages.
- Record exceptions.
- Expose a simple logging API.

Every service receives a logger instance.

---

## Log Handlers

Initial handlers

- File Handler

Future handlers

- Console
- Database
- Cloud
- Windows Event Log
- Syslog

Handlers are managed exclusively by LogManager.

---

# 7. Log Levels

Supported levels

DEBUG

Detailed diagnostic information.

Used only during development.

---

INFO

Normal application operations.

Examples

- Backup started
- Backup completed
- Settings loaded

---

WARNING

Recoverable situations.

Examples

- Destination folder already exists.
- Missing optional configuration.

---

ERROR

Unexpected failures.

Examples

- ZIP creation failed.
- Configuration could not be saved.

---

CRITICAL

Application integrity compromised.

Examples

- Scheduler initialization failed.
- Settings unavailable.
- Unrecoverable startup failure.

---

# 8. Log Format

Every log entry should include:

- Timestamp
- Level
- Module
- Function
- Message

Recommended format

```
2026-08-06 18:30:15
INFO
BackupService
execute_backup

Backup completed successfully.
```

Machine-readable formats (JSON) may be introduced in future versions.

---

# 9. Log File

Default location

```
logs/
```

Default filename

```
autozip.log
```

The directory must be created automatically if it does not exist.

---

# 10. Log Rotation

Version 1.0

RotatingFileHandler

Recommended configuration

Maximum file size

10 MB

Maximum backups

10

Older log files are automatically removed.

---

# 11. Exception Logging

Unexpected exceptions must always be logged.

Preferred

```python
logger.exception(exception)
```

Forbidden

```python
except Exception:
    pass
```

Stack traces must be preserved.

---

# 12. Thread Safety

The logging subsystem must support background worker threads.

No additional synchronization should be required by business modules.

---

# 13. Performance

Logging should not noticeably impact application performance.

Expensive string formatting should be avoided when the log level disables the message.

Example

```python
logger.debug("Backup finished: %s", filename)
```

instead of

```python
logger.debug(f"Backup finished: {filename}")
```

when formatting is expensive.

---

# 14. Future Extensions

The architecture allows additional handlers.

Examples

- SQLite
- SQL Server
- Elasticsearch
- Azure Monitor
- AWS CloudWatch
- Email notifications

No business module should require modification.

---

# 15. Consequences

## Positive

- Consistent logs.
- Centralized configuration.
- Easy troubleshooting.
- Easy testing.
- Extensible architecture.
- Better maintainability.

## Negative

- Slightly more infrastructure.
- Requires dependency injection.

---

# 16. Compliance Rules

Every code review should verify:

- Only LogManager configures logging.
- Services never create handlers.
- Services never call basicConfig().
- Services receive logger instances.
- Exceptions are logged before propagation.
- print() is never used for diagnostics.

---

# 17. Risks

Potential risks

- Excessive logging.
- Sensitive information in logs.
- Large log files.

Mitigation

- Appropriate log levels.
- Log rotation.
- Avoid logging confidential data.

---

# 18. Impact

**Impact Level:** High

This ADR defines the official logging strategy for the project.

Future logging changes must comply with this architecture.

---

# 19. Related Documents

- architecture.md
- coding-standards.md
- development-environment.md
- decisions.md

---

# 20. Revision History

| Date | Version | Description |
|------|---------|-------------|
| 2026-08-06 | 1.0 | Initial version. Approved. |

---

# End of Document