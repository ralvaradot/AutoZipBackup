# ADR-005 — Event Dispatcher Architecture

**Project:** AutoZipBackup

**ADR:** 005

**Status:** Accepted

**Date:** 2026-08-06

**Decision Maker:** Project Architecture Team

**Supersedes:** None

**Superseded By:** None

---

# 1. Context

AutoZipBackup executes long-running background operations.

Examples:

- ZIP creation
- Restore
- File verification
- Scheduler execution

The graphical interface must remain responsive while these operations execute.

A communication mechanism is required between background services and the user interface.

---

# 2. Problem Statement

Without an event system:

- Services become coupled to the UI.
- Background threads update widgets directly.
- Code becomes difficult to test.
- The UI must constantly poll operation status.
- Future extensions become difficult.

A communication mechanism with low coupling is required.

---

# 3. Decision Drivers

The solution must:

- Decouple services from the UI.
- Be thread-safe.
- Support multiple listeners.
- Avoid polling.
- Be easy to test.
- Be extensible.
- Keep implementation simple.

---

# 4. Alternatives Considered

## Alternative A — Direct UI Calls

```
BackupService

↓

MainWindow.update_progress()
```

### Advantages

Simple.

### Disadvantages

High coupling.

Impossible to reuse services.

Not testable.

### Decision

Rejected.

---

## Alternative B — Polling

The UI periodically checks service status.

### Advantages

Simple implementation.

### Disadvantages

Waste of CPU.

Delayed updates.

Poor responsiveness.

### Decision

Rejected.

---

## Alternative C — Generic Event Bus

Advantages

Very flexible.

### Disadvantages

Too generic.

Harder to debug.

Hidden communication paths.

### Decision

Rejected.

---

## Alternative D — Typed Event Dispatcher

Services publish strongly typed events.

The dispatcher delivers them to registered listeners.

### Advantages

Simple.

Explicit.

Easy to debug.

Easy to test.

Low coupling.

### Decision

Accepted.

---

# 5. Decision

The project adopts a centralized Event Dispatcher.

```
Service

↓

Event Dispatcher

↓

Registered Listeners

↓

UI
```

Services never know who receives the events.

Listeners never know who generated them.

---

# 6. Responsibilities

## EventDispatcher

Responsibilities

- Register listeners.
- Remove listeners.
- Dispatch events.
- Preserve event ordering.

The dispatcher contains no business logic.

---

## Events

Events are immutable.

Each event represents something that already happened.

Examples

```
BackupStarted

BackupProgressChanged

BackupCompleted

BackupFailed

SettingsChanged

LanguageChanged

ThemeChanged

SchedulerStarted

SchedulerStopped
```

---

## Listeners

Listeners react to events.

Examples

MainWindow

StatusBar

ProgressDialog

NotificationService

Logger

---

# 7. Event Lifecycle

```
User starts backup

↓

BackupService

↓

BackupStarted

↓

Dispatcher

↓

ProgressDialog

↓

ProgressChanged

↓

Dispatcher

↓

StatusBar

↓

BackupCompleted

↓

Dispatcher

↓

NotificationService
```

Every event flows through the dispatcher.

---

# 8. Thread Safety

Background workers publish events.

The dispatcher is responsible for safely delivering them.

Background threads never manipulate widgets directly.

UI updates occur only on the main thread.

---

# 9. Event Design Rules

Events must:

- Be immutable.
- Represent completed facts.
- Contain only required data.
- Never contain business logic.

Example

Good

```
BackupCompleted
```

Bad

```
ExecuteBackupNow
```

Commands are not events.

---

# 10. Naming Convention

Events use PascalCase.

Examples

```
BackupStarted

BackupProgressChanged

BackupCompleted

BackupFailed

SettingsSaved

LanguageChanged
```

---

# 11. Future Events

The architecture supports additional events.

Examples

```
RestoreStarted

RestoreCompleted

ChecksumCompleted

CloudUploadCompleted

PluginLoaded
```

Existing code should not require modification.

---

# 12. Error Handling

Listener failures must never prevent delivery to other listeners.

Exceptions should be:

- Logged.
- Isolated.
- Reported.

The dispatcher should continue processing remaining listeners.

---

# 13. Performance

Event dispatch should introduce minimal overhead.

Events should remain lightweight.

Large objects should not be transported inside events.

---

# 14. Consequences

## Positive

- Low coupling.
- Responsive UI.
- Easy testing.
- Better modularity.
- Easier future expansion.

## Negative

- Additional infrastructure.
- Developers must understand event flow.

---

# 15. Compliance Rules

Every code review should verify:

- Services never reference UI classes.
- Widgets never poll services.
- Background threads never update widgets directly.
- Events are immutable.
- Events contain no business logic.
- Communication occurs only through EventDispatcher.

---

# 16. Risks

Potential risks

- Excessive event generation.
- Duplicate listeners.
- Memory leaks due to unregistered listeners.

Mitigation

- Listener lifecycle management.
- Event documentation.
- Unit testing.

---

# 17. Impact

**Impact Level:** High

This ADR defines the official communication mechanism between modules.

All asynchronous communication must comply with this architecture.

---

# 18. Related Documents

- architecture.md
- coding-standards.md
- decisions.md
- ADR-001 Project Architecture
- ADR-002 Project Folder Structure

---

# 19. Revision History

| Date | Version | Description |
|------|---------|-------------|
| 2026-08-06 | 1.0 | Initial version. Approved. |

---

# End of Document