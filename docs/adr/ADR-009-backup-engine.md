# ADR-009 — Backup Engine Architecture

**Project:** AutoZipBackup

**ADR:** 009

**Status:** Accepted

**Date:** 2026-08-06

**Decision Maker:** Project Architecture Team

**Supersedes:** None

**Superseded By:** None

---

# 1. Context

The primary purpose of AutoZipBackup is to automate the creation of compressed ZIP backups.

Each backup execution must:

- Validate the source folder.
- Create a ZIP archive.
- Verify the generated archive.
- Move the archive to the destination folder.
- Produce detailed logs.
- Notify the user interface through events.

The backup engine must remain independent from the scheduler and the graphical interface.

---

# 2. Problem Statement

A monolithic backup service quickly becomes responsible for:

- Validation
- Compression
- File naming
- Verification
- Logging
- Moving files
- Error handling

Such an implementation violates the Single Responsibility Principle and becomes difficult to maintain and test.

---

# 3. Decision Drivers

The backup engine must:

- Produce reliable ZIP archives.
- Be modular.
- Be testable.
- Support future enhancements.
- Keep business rules isolated.
- Allow replacement of individual components.

---

# 4. Alternatives Considered

## Alternative A — Single BackupService

```
BackupService
```

### Advantages

- Simple.
- Small number of classes.

### Disadvantages

- Large class.
- Difficult testing.
- High maintenance cost.
- Violates SRP.

### Decision

Rejected.

---

## Alternative B — Modular Backup Engine

```
BackupOrchestrator

↓

CompressionService

↓

VerificationService

↓

ArchiveMover

↓

NamingStrategy
```

### Advantages

- Excellent separation of concerns.
- Easy unit testing.
- Extensible.
- Easier maintenance.

### Disadvantages

- More classes.

### Decision

Accepted.

---

# 5. Decision

The backup subsystem is composed of the following components.

```text
BackupOrchestrator

↓

ValidationService

↓

NamingStrategy

↓

CompressionService

↓

VerificationService

↓

ArchiveMover

↓

Events

↓

Logging
```

The orchestrator coordinates the workflow.

Each component performs exactly one responsibility.

---

# 6. Components

## BackupOrchestrator

Responsibilities

- Coordinate backup execution.
- Invoke pipeline components.
- Publish events.
- Handle workflow errors.

Must never implement compression algorithms.

---

## ValidationService

Responsibilities

- Validate source folder.
- Validate destination folder.
- Check permissions.
- Verify available disk space (future enhancement).

---

## NamingStrategy

Responsibilities

Generate archive names.

Version 1.0 format:

```
<FolderName>_YYYYMMDD_HHMMSS.zip
```

Example

```
Documents_20260806_183000.zip
```

The naming strategy must be replaceable.

---

## CompressionService

Responsibilities

- Compress folder.
- Create ZIP archive.
- Preserve directory structure.

Uses Python's standard `zipfile` module in version 1.0.

---

## VerificationService

Responsibilities

- Verify ZIP existence.
- Verify archive readability.
- Validate archive structure.

Future versions may include SHA-256 verification.

---

## ArchiveMover

Responsibilities

- Move archive to destination.
- Replace existing archive according to policy.
- Report failures.

---

## BackupContext

Contains execution data.

Examples

- Source path.
- Destination path.
- Start time.
- Generated filename.
- Task identifier.

Business services receive BackupContext instead of many independent parameters.

---

# 7. Backup Workflow

```text
Backup Requested

↓

ValidationService

↓

NamingStrategy

↓

CompressionService

↓

VerificationService

↓

ArchiveMover

↓

BackupCompleted Event

↓

Logging
```

If any step fails, execution stops and an appropriate event is published.

---

# 8. Compression Policy

Version 1.0

- ZIP format.
- Standard Deflate compression.
- Preserve folder hierarchy.
- Preserve file names.
- Skip unsupported filesystem objects when necessary.

Future compression formats may be added through additional services.

---

# 9. Naming Policy

Archive names are deterministic.

Format:

```
<FolderName>_YYYYMMDD_HHMMSS.zip
```

Requirements

- No invalid filename characters.
- Stable formatting.
- Independent from operating system locale.

---

# 10. Error Handling

Failures should:

- Generate log entries.
- Publish BackupFailed events.
- Preserve partially created files only when useful for diagnostics.

Unexpected exceptions should never crash the application.

---

# 11. Threading

Backup execution always occurs outside the UI thread.

The backup engine never manipulates graphical components.

Progress information is published through events.

---

# 12. Logging

Every execution records:

- Start time.
- End time.
- Source folder.
- Destination folder.
- Generated filename.
- Compression duration.
- Success or failure.

---

# 13. Future Extensions

The architecture supports:

- Encrypted ZIP.
- 7z archives.
- TAR archives.
- Incremental backup.
- Differential backup.
- Compression levels.
- Exclusion rules.
- Backup history.

These features should integrate without architectural changes.

---

# 14. Consequences

## Positive

- Small focused components.
- Excellent testability.
- Easy maintenance.
- Easy future expansion.
- Clear workflow.

## Negative

- More infrastructure classes.
- Requires orchestration.

---

# 15. Compliance Rules

Every code review should verify:

- BackupOrchestrator coordinates but does not implement compression.
- CompressionService only creates archives.
- NamingStrategy only generates archive names.
- VerificationService performs no compression.
- ArchiveMover only handles archive movement.
- BackupContext is used instead of long parameter lists.
- No UI code exists inside the backup subsystem.

---

# 16. Risks

Potential risks

- Very large folders.
- Locked files.
- Insufficient disk space.
- Interrupted execution.

Mitigation

- Detailed logging.
- Validation before compression.
- Graceful failure handling.
- Future retry support.

---

# 17. Impact

**Impact Level:** Critical

This ADR defines the core business architecture of AutoZipBackup.

All backup-related functionality must comply with this design.

---

# 18. Related Documents

- architecture.md
- project-structure.md
- coding-standards.md
- ADR-001 Project Architecture
- ADR-003 Configuration Management
- ADR-004 Logging Strategy
- ADR-005 Event Dispatcher Architecture
- ADR-006 Scheduler Architecture

---

# 19. Revision History

| Date | Version | Description |
|------|---------|-------------|
| 2026-08-06 | 1.0 | Initial version. Approved. |

---

# End of Document