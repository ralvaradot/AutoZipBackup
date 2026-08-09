# ADR-006 — Scheduler Architecture

**Project:** AutoZipBackup

**ADR:** 006

**Status:** Accepted

**Date:** 2026-08-06

**Decision Maker:** Project Architecture Team

**Supersedes:** None

**Superseded By:** None

---

# 1. Context

AutoZipBackup automates the execution of recurring backup tasks.

Users must be able to configure backups to run automatically at a specific time each day without user intervention.

The scheduling subsystem must operate reliably while remaining independent from the backup implementation.

---

# 2. Problem Statement

If the scheduler invokes business services directly:

- Scheduling logic becomes coupled to backup logic.
- Supporting additional scheduled tasks becomes difficult.
- Testing the scheduler independently is complicated.
- Error handling is duplicated.

A dedicated scheduling architecture is required.

---

# 3. Decision Drivers

The scheduling solution must:

- Support recurring daily execution.
- Keep the user interface responsive.
- Prevent unnecessary coupling.
- Support future task types.
- Be testable.
- Be reliable.
- Be extensible.

---

# 4. Alternatives Considered

## Alternative A — Native Python sched

### Advantages

- Included in the standard library.
- Minimal dependencies.

### Disadvantages

- Limited functionality.
- No persistent scheduling.
- Weak support for long-running desktop applications.

### Decision

Rejected.

---

## Alternative B — Windows Task Scheduler

### Advantages

- Native to Windows.
- Reliable.

### Disadvantages

- Platform dependent.
- Difficult to manage from the application.
- Prevents future cross-platform support.

### Decision

Rejected.

---

## Alternative C — APScheduler Direct Execution

```
APScheduler

↓

BackupService
```

### Advantages

- Simple.

### Disadvantages

- Tight coupling.
- Difficult to extend.
- Scheduler becomes aware of business services.

### Decision

Rejected.

---

## Alternative D — SchedulerManager + TaskExecutor

```
APScheduler

↓

SchedulerManager

↓

TaskExecutor

↓

Business Services
```

### Advantages

- Excellent separation of concerns.
- Easy testing.
- Supports multiple task types.
- Better scalability.

### Decision

Accepted.

---

# 5. Decision

The project adopts APScheduler as the scheduling engine.

The scheduling architecture is defined as follows:

```text
Application

↓

SchedulerManager

↓

APScheduler

↓

TaskExecutor

↓

BackupService
```

Business services never interact directly with APScheduler.

---

# 6. Responsibilities

## SchedulerManager

Responsibilities

- Initialize APScheduler.
- Start scheduler.
- Stop scheduler.
- Register jobs.
- Remove jobs.
- Load persisted schedules.
- Persist schedule changes.

Must never execute business logic.

---

## TaskExecutor

Responsibilities

- Receive scheduled executions.
- Validate execution context.
- Log execution start.
- Invoke the appropriate service.
- Capture execution results.
- Publish completion events.

Must never manage scheduler configuration.

---

## BackupService

Responsibilities

- Execute backup.
- Compress folders.
- Verify output.
- Move generated ZIP.
- Publish backup events.

Must never schedule itself.

---

# 7. Scheduler Lifecycle

```text
Application Start

↓

Settings Loaded

↓

SchedulerManager

↓

Register Jobs

↓

Wait

↓

Scheduled Time

↓

TaskExecutor

↓

BackupService

↓

Events

↓

Logging
```

---

# 8. Scheduling Policy

Version 1.0 supports:

- Daily execution.
- One execution time per task.
- Enable/disable tasks.
- Manual execution.
- Immediate execution on user request.

Future recurrence patterns may be added without changing the overall architecture.

---

# 9. Job Identification

Each scheduled task must have a unique identifier.

Recommended format:

```text
task_<uuid>
```

Identifiers remain stable across application restarts.

---

# 10. Persistence

Task definitions are stored in the application configuration.

Persisted information includes:

- Task identifier.
- Source folder.
- Destination folder.
- Execution time.
- Enabled status.

The scheduler rebuilds its state during application startup.

---

# 11. Error Handling

Scheduler failures must:

- Be logged.
- Not terminate the application.
- Not stop unrelated scheduled tasks.

Task execution failures must not prevent future scheduled executions.

---

# 12. Threading Model

APScheduler executes jobs in background worker threads.

Business services execute outside the UI thread.

The UI is notified exclusively through the EventDispatcher.

No scheduler thread may manipulate UI components directly.

---

# 13. Logging

Scheduler operations generate log entries for:

- Scheduler startup.
- Scheduler shutdown.
- Job registration.
- Job removal.
- Job execution.
- Job success.
- Job failure.

---

# 14. Future Extensions

The architecture supports additional scheduled operations.

Examples:

- Restore tasks.
- Automatic cleanup.
- Integrity verification.
- Cloud synchronization.
- Notification delivery.

These additions should require only new TaskExecutor mappings.

---

# 15. Consequences

## Positive

- Low coupling.
- Clear separation of responsibilities.
- Extensible scheduling model.
- Easier testing.
- Better maintainability.

## Negative

- Additional abstraction.
- More infrastructure components.

---

# 16. Compliance Rules

Every code review should verify:

- Only SchedulerManager interacts with APScheduler.
- SchedulerManager never executes business logic.
- TaskExecutor delegates work to services.
- Business services never import APScheduler.
- Scheduled tasks execute outside the UI thread.
- UI updates occur only through EventDispatcher.

---

# 17. Risks

Potential risks:

- Missed executions after system sleep.
- Long-running backups overlapping scheduled times.
- Invalid task configuration.

Mitigation strategies:

- Validate task definitions before scheduling.
- Log skipped executions.
- Prevent concurrent execution of the same task.
- Support configurable misfire handling in APScheduler.

---

# 18. Impact

**Impact Level:** High

This ADR defines the official scheduling architecture for AutoZipBackup.

All future scheduled functionality must conform to this design.

---

# 19. Related Documents

- architecture.md
- project-structure.md
- coding-standards.md
- ADR-001 Project Architecture
- ADR-003 Configuration Management
- ADR-004 Logging Strategy
- ADR-005 Event Dispatcher Architecture

---

# 20. Revision History

| Date | Version | Description |
|------|---------|-------------|
| 2026-08-06 | 1.0 | Initial version. Approved. |

---

# End of Document