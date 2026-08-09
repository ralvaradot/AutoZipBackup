# ADR-011 — Testing Strategy

**Project:** AutoZipBackup

**ADR:** 011

**Status:** Accepted

**Date:** 2026-08-06

**Decision Maker:** Project Architecture Team

**Supersedes:** None

**Superseded By:** None

---

# 1. Context

AutoZipBackup is a desktop application composed of multiple independent modules.

The application performs:

- File system operations
- ZIP compression
- Task scheduling
- Configuration management
- Localization
- Theme management
- Event dispatching

Each subsystem must be verifiable independently while preserving the overall system reliability.

---

# 2. Problem Statement

Without a defined testing strategy:

- Bugs reach production.
- Refactoring becomes risky.
- Architectural rules degrade.
- Regression defects increase.
- Code quality becomes inconsistent.

A comprehensive testing strategy is required.

---

# 3. Decision Drivers

The testing strategy must:

- Encourage automated testing.
- Support continuous integration.
- Validate architectural rules.
- Be fast.
- Be deterministic.
- Avoid unnecessary dependencies.
- Support future growth.

---

# 4. Alternatives Considered

## Alternative A — Manual Testing Only

### Advantages

- No additional code.

### Disadvantages

- Error-prone.
- Slow.
- Not repeatable.
- High regression risk.

### Decision

Rejected.

---

## Alternative B — Unit Tests Only

### Advantages

- Fast.
- Easy to execute.

### Disadvantages

- Does not validate module integration.
- Limited confidence.

### Decision

Rejected.

---

## Alternative C — Multi-layer Testing Strategy

Testing is performed at several levels.

### Advantages

- High confidence.
- Good maintainability.
- Supports long-term evolution.

### Decision

Accepted.

---

# 5. Decision

The project adopts a layered testing strategy.

```text
UI Tests

↓

Integration Tests

↓

Component Tests

↓

Unit Tests
```

Each layer verifies a different aspect of the system.

---

# 6. Test Types

## Unit Tests

Purpose

Verify a single class or function.

Characteristics

- No external dependencies.
- No file system access.
- No network access.
- Fast execution.

Examples

- NamingStrategy
- ValidationService
- TranslationProvider
- ThemeProvider

---

## Component Tests

Purpose

Verify collaboration inside one module.

Examples

- Backup subsystem
- Scheduler subsystem
- Settings subsystem

External dependencies are mocked whenever practical.

---

## Integration Tests

Purpose

Verify interaction between modules.

Examples

- Scheduler → Backup
- Settings → Localization
- ThemeManager → UI
- EventDispatcher → MainWindow

Real components may be combined.

---

## UI Tests

Purpose

Verify visible application behavior.

Examples

- Language switching.
- Theme switching.
- Settings persistence.
- Backup creation workflow.

UI tests remain limited due to higher execution cost.

---

# 7. Test Directory Structure

The test project mirrors the production project.

```text
tests/

    backup/

    scheduler/

    settings/

    localization/

    ui/

    common/

    integration/
```

Developers should locate tests using the same navigation as production code.

---

# 8. Test Framework

Official framework

```
pytest
```

Additional tools

- pytest-mock
- pytest-cov
- unittest.mock

Future additions must be compatible with pytest.

---

# 9. Mocking Policy

Mock only external dependencies.

Examples

- File system
- Clock
- Scheduler
- Logging
- Configuration repository

Business logic should never be mocked.

---

# 10. Test Naming

Recommended format

```
test_<behavior>_<expected_result>()
```

Examples

```
test_generate_filename_returns_expected_format()

test_load_settings_when_file_missing_returns_defaults()

test_dispatch_event_notifies_registered_listeners()
```

---

# 11. Coverage Goals

Minimum overall coverage

```
90%
```

Critical modules

```
95%
```

Critical modules include:

- backup
- scheduler
- settings
- common

Coverage is an indicator, not the sole quality metric.

---

# 12. Test Data

Temporary files should use isolated directories.

Tests must never modify user data.

Generated files are automatically removed after execution.

---

# 13. Continuous Integration

Every Pull Request executes:

- Static analysis.
- Unit tests.
- Component tests.
- Integration tests.
- Coverage report.

Merging is blocked if mandatory tests fail.

---

# 14. Performance

Unit tests should execute in milliseconds.

The complete automated test suite should finish within a few minutes on a standard development workstation.

Performance tests are maintained separately.

---

# 15. Future Extensions

The testing architecture supports:

- Performance testing.
- Stress testing.
- Load testing.
- Mutation testing.
- Accessibility testing.
- Visual regression testing.

---

# 16. Consequences

## Positive

- Higher reliability.
- Easier refactoring.
- Better documentation of behavior.
- Faster defect detection.
- Long-term maintainability.

## Negative

- Increased initial development effort.
- Ongoing maintenance of test code.

---

# 17. Compliance Rules

Every code review should verify:

- New business logic includes automated tests.
- Tests follow the production directory structure.
- External dependencies are mocked appropriately.
- Tests remain deterministic.
- Tests do not depend on execution order.
- Failing tests block merging.

---

# 18. Risks

Potential risks

- Slow test suite.
- Excessive mocking.
- Fragile UI tests.

Mitigation

- Prioritize unit tests.
- Keep integration tests focused.
- Limit UI automation to critical workflows.

---

# 19. Impact

**Impact Level:** High

This ADR defines the official testing strategy for AutoZipBackup.

All future development must include automated tests aligned with this strategy.

---

# 20. Related Documents

- architecture.md
- coding-standards.md
- development-environment.md
- roadmap.md
- ADR-001 Project Architecture
- ADR-003 Configuration Management
- ADR-004 Logging Strategy
- ADR-005 Event Dispatcher Architecture
- ADR-009 Backup Engine Architecture
- ADR-010 Error Handling Strategy

---

# 21. Revision History

| Date | Version | Description |
|------|---------|-------------|
| 2026-08-06 | 1.0 | Initial version. Approved. |

---

# End of Document