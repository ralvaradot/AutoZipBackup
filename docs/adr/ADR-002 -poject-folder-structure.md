# ADR-002 — Project Folder Structure

**Project:** AutoZipBackup

**ADR:** 002

**Status:** Accepted

**Date:** 2026-08-06

**Decision Maker:** Project Architecture Team

**Supersedes:** None

**Superseded By:** None

---

# 1. Context

As the project grows, maintaining a predictable and well-organized directory structure becomes increasingly important.

A consistent structure allows developers to:

- Locate code quickly.
- Reduce onboarding time.
- Minimize coupling.
- Improve maintainability.
- Scale the project without reorganizing directories.

Several architectural styles were evaluated before freezing the project structure.

This ADR defines the official directory organization for the entire AutoZipBackup project.

---

# 2. Problem Statement

Without a formal directory structure, projects tend to evolve inconsistently.

Typical consequences include:

- Business logic scattered across multiple folders.
- Duplicate functionality.
- Circular dependencies.
- Difficult navigation.
- Large utility modules.
- Constant refactoring of folders.

These problems increase maintenance costs over time.

---

# 3. Decision Drivers

The selected structure must satisfy the following requirements:

- Feature-oriented organization.
- Easy navigation.
- Low coupling.
- High cohesion.
- Clear ownership.
- Scalability.
- Minimal cognitive load.
- Support long-term maintenance.

---

# 4. Alternatives Considered

## Alternative A — Layered Architecture

```
application/
domain/
infrastructure/
presentation/
```

### Advantages

- Well known.
- Strong separation of concerns.
- Common in enterprise applications.

### Disadvantages

- Excessive fragmentation.
- A single feature spans multiple directories.
- Navigation becomes slower.
- Higher cognitive load.

### Decision

Rejected.

---

## Alternative B — Traditional MVC

```
models/
views/
controllers/
```

### Advantages

- Familiar.
- Easy to understand.

### Disadvantages

- Controllers tend to accumulate business logic.
- Weak separation of responsibilities.
- Poor scalability.

### Decision

Rejected.

---

## Alternative C — Feature-Oriented Modular Structure

```
backup/
scheduler/
settings/
localization/
ui/
common/
resources/
```

### Advantages

- High cohesion.
- Clear ownership.
- Easy navigation.
- Easier future expansion.
- Reduced coupling.
- Natural mapping between requirements and source code.

### Disadvantages

- Requires discipline to prevent oversized modules.

### Decision

Accepted.

---

# 5. Decision

The project adopts a **feature-oriented modular directory structure**.

Each top-level package is responsible for a single functional area.

No module should contain unrelated responsibilities.

The official project structure is:

```text
src/
└── autozip/
    │
    ├── backup/
    ├── scheduler/
    ├── settings/
    ├── localization/
    ├── ui/
    │   ├── views/
    │   ├── dialogs/
    │   └── widgets/
    ├── common/
    └── resources/
```

This structure is considered stable for version 1.x.

---

# 6. Module Responsibilities

## backup

Responsible for:

- Backup execution
- ZIP creation
- Restore
- Checksum verification

Must never contain:

- UI code
- Scheduler configuration

---

## scheduler

Responsible for:

- APScheduler integration
- Job scheduling
- Task execution

Must never:

- Compress files
- Manipulate ZIP archives

---

## settings

Responsible for:

- Loading configuration
- Saving configuration
- Configuration validation

Only this module may access:

```
settings.json
```

---

## localization

Responsible for:

- Language loading
- Runtime language switching
- Translation services

---

## ui

Responsible for:

- Windows
- Dialogs
- Widgets
- User interaction

Business rules are forbidden.

---

## common

Contains reusable infrastructure.

Examples:

- Logger
- Exceptions
- Constants
- Events
- Shared utilities

This package must remain lightweight.

---

## resources

Contains static assets.

Examples:

- Icons
- Images
- Fonts
- Theme resources

---

# 7. Dependency Rules

Dependencies always point downward.

```text
UI

↓

Services

↓

Infrastructure

↓

Operating System
```

The following dependency is forbidden:

```text
backup

↓

ui
```

Business modules must never depend on presentation.

---

# 8. Directory Ownership

| Directory | Responsibility |
|-----------|----------------|
| backup | Backup subsystem |
| scheduler | Task scheduling |
| settings | Application configuration |
| localization | Language management |
| ui | User interface |
| common | Shared infrastructure |
| resources | Static assets |

Ownership prevents duplicated functionality.

---

# 9. Directory Creation Policy

The following directories are created automatically by the application:

```text
logs/

backups/
```

Users are not required to create them manually.

---

# 10. Future Extensions

New functionality should be introduced as new feature modules.

Examples:

```text
notifications/

cloud/

encryption/

plugins/
```

Existing modules should not be reorganized unless a new ADR explicitly approves the change.

---

# 11. Consequences

## Positive

- Predictable project organization.
- Easier onboarding.
- Faster navigation.
- Lower coupling.
- Better scalability.
- Stable architecture.

## Negative

- Developers must respect module boundaries.
- New functionality requires evaluating the correct module before implementation.

---

# 12. Compliance Rules

Every Pull Request should verify:

- Files are located in the correct module.
- Responsibilities remain unchanged.
- No circular dependencies are introduced.
- No feature spans unrelated modules unnecessarily.

---

# 13. Risks

Potential risks include:

- Oversized service modules.
- Utility classes accumulating unrelated logic.
- Incorrect placement of new functionality.

These risks should be mitigated through code reviews.

---

# 14. Impact

**Impact Level:** High

This ADR defines the official directory organization of the project.

Future development must comply with this structure.

Changes require a new ADR.

---

# 15. Related Documents

- architecture.md
- project-structure.md
- coding-standards.md
- decisions.md

---

# 16. Revision History

| Date | Version | Description |
|------|---------|-------------|
| 2026-08-06 | 1.0 | Initial version. Approved. |

---

# End of Document