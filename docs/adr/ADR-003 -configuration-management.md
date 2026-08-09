# ADR-003 — Configuration Management

**Project:** AutoZipBackup

**ADR:** 003

**Status:** Accepted

**Date:** 2026-08-06

**Decision Maker:** Project Architecture Team

**Supersedes:** None

**Superseded By:** None

---

# 1. Context

AutoZipBackup requires persistent application settings.

Examples include:

- Language
- Theme
- Backup tasks
- Scheduler configuration
- Logging configuration
- Default folders

The application must provide fast access to configuration data while avoiding unnecessary disk operations.

The configuration mechanism should also be extensible to support future storage providers.

---

# 2. Problem Statement

If every module reads or writes the configuration file directly:

- Configuration becomes inconsistent.
- Disk access increases.
- Validation is duplicated.
- Testing becomes difficult.
- Future migration becomes expensive.

A centralized configuration strategy is required.

---

# 3. Decision Drivers

The selected solution must:

- Load configuration only once.
- Keep configuration in memory.
- Validate configuration before use.
- Prevent concurrent writes.
- Be easy to test.
- Support future storage providers.
- Minimize coupling.

---

# 4. Alternatives Considered

## Alternative A — Direct JSON Access

Each module opens and updates `settings.json`.

### Advantages

- Very simple.

### Disadvantages

- High coupling.
- Repeated file access.
- Duplicate validation.
- Difficult testing.
- Error-prone.

### Decision

Rejected.

---

## Alternative B — Static Configuration Class

A static singleton exposes configuration globally.

### Advantages

- Easy access.

### Disadvantages

- Hidden dependencies.
- Difficult mocking.
- Difficult unit testing.
- Global mutable state.

### Decision

Rejected.

---

## Alternative C — Settings Manager + Repository

A manager owns the in-memory configuration.

A repository performs persistence.

### Advantages

- Single source of truth.
- Excellent testability.
- Separation of responsibilities.
- Easy future migration.
- Reduced coupling.

### Disadvantages

- Slightly more classes.

### Decision

Accepted.

---

# 5. Decision

The configuration subsystem consists of two primary components.

```
Application

↓

SettingsManager

↓

SettingsRepository

↓

settings.json
```

Only the repository accesses the file system.

Only the manager exposes configuration to the rest of the application.

---

# 6. Responsibilities

## SettingsManager

Responsibilities

- Load configuration during startup.
- Keep configuration in memory.
- Expose typed configuration objects.
- Coordinate save operations.
- Notify interested components when configuration changes.

Must never:

- Parse JSON directly.
- Access the file system.

---

## SettingsRepository

Responsibilities

- Read `settings.json`.
- Write `settings.json`.
- Serialize configuration.
- Deserialize configuration.
- Validate file existence.

Must never:

- Contain business logic.
- Decide application behavior.

---

# 7. Configuration Lifecycle

```
Application Start

↓

SettingsRepository.load()

↓

SettingsManager

↓

Application Uses Configuration

↓

Configuration Changes

↓

SettingsManager.save()

↓

SettingsRepository.save()

↓

settings.json
```

Configuration is loaded once and remains in memory.

---

# 8. Configuration Model

Configuration is represented by strongly typed dataclasses.

Example:

```python
AppSettings
```

The application must avoid manipulating raw dictionaries.

Preferred:

```python
settings.language
```

Forbidden:

```python
settings["language"]
```

---

# 9. Validation

Configuration must be validated before becoming available.

Validation includes:

- Required fields.
- Data types.
- Valid paths.
- Supported language.
- Supported theme.
- Scheduler values.

Invalid configuration should fall back to safe defaults whenever possible.

---

# 10. File Format

The official persistence format is JSON.

Reasons:

- Human-readable.
- Portable.
- Easy to debug.
- Native Python support.

The JSON schema may evolve over time while preserving backward compatibility whenever practical.

---

# 11. Future Compatibility

The repository abstraction allows replacing JSON with:

- SQLite
- Windows Registry
- Cloud Storage
- Remote API

without modifying business modules.

---

# 12. Thread Safety

Configuration modifications should be serialized.

Background workers must not write configuration directly.

All updates should be coordinated by the SettingsManager.

---

# 13. Error Handling

Configuration failures should:

- Be logged.
- Generate user-friendly messages.
- Never crash the application unexpectedly.

If the configuration file cannot be loaded:

- Default settings should be created.
- The application should continue whenever possible.

---

# 14. Consequences

## Positive

- Single source of truth.
- Better testability.
- Lower coupling.
- Better maintainability.
- Reduced disk access.
- Easier future migration.

## Negative

- Additional abstraction.
- More classes than a direct JSON implementation.

---

# 15. Compliance Rules

Every code review should verify:

- Only `SettingsRepository` accesses `settings.json`.
- Only `SettingsManager` exposes configuration.
- No module manipulates raw JSON.
- No module keeps its own configuration cache.
- Configuration objects are strongly typed.

---

# 16. Risks

Potential risks:

- Unsaved changes if the application closes unexpectedly.
- Corrupted configuration file.
- Invalid user edits.

Mitigation:

- Validation before saving.
- Atomic file writes.
- Automatic backup of the previous configuration (future enhancement).

---

# 17. Impact

**Impact Level:** High

This ADR defines the official configuration management strategy for the entire application.

---

# 18. Related Documents

- architecture.md
- project-structure.md
- coding-standards.md
- decisions.md

---

# 19. Revision History

| Date | Version | Description |
|------|---------|-------------|
| 2026-08-06 | 1.0 | Initial version. Approved. |

---

# End of Document