# ADR-001 — Project Architecture

**Project:** AutoZipBackup

**ADR:** 001

**Status:** Accepted

**Date:** 2026-08-06

**Decision Maker:** Project Architecture Team

---

# Context

AutoZipBackup is a desktop application intended to automate scheduled ZIP backups through a graphical user interface.

The project is expected to evolve over time by incorporating additional functionality such as restore operations, backup verification, multiple backup profiles, cloud integration and notification providers.

The architecture must therefore support long-term evolution while remaining simple enough for a single-developer project.

---

# Problem

Choosing an architecture that is both maintainable and easy to understand.

The architecture should:

- Separate concerns clearly.
- Minimize coupling.
- Facilitate testing.
- Allow future extension.
- Avoid unnecessary complexity.

---

# Alternatives Considered

## Alternative 1

Traditional MVC

Advantages

- Simple
- Familiar

Disadvantages

- Business logic often leaks into controllers.
- Controllers grow excessively.
- Difficult to maintain in medium-sized projects.

Result

Rejected.

---

## Alternative 2

MVVM

Advantages

- Excellent for data binding.
- Widely used with WPF.

Disadvantages

- Tkinter does not provide native data binding.
- Introduces unnecessary complexity.

Result

Rejected.

---

## Alternative 3

Clean Architecture

Advantages

- Highly scalable.
- Excellent separation of concerns.

Disadvantages

- Too many abstractions for the expected project size.
- Excessive number of packages.
- Increased development effort.

Result

Rejected.

---

## Alternative 4

Service-Oriented Modular Architecture

Advantages

- Simple.
- Highly readable.
- Easy to extend.
- Suitable for desktop applications.
- Low cognitive load.

Disadvantages

- Requires discipline to avoid service classes becoming too large.

Result

Accepted.

---

# Decision

The project adopts a **Service-Oriented Modular Architecture**.

The source code is organized by functional modules.

Each module owns its responsibilities.

Business logic resides inside services.

The user interface is intentionally thin.

---

# Architectural Principles

The architecture follows:

- Single Responsibility Principle
- Separation of Concerns
- Composition over Inheritance
- Explicit Dependencies
- Feature-oriented organization

---

# Layer Responsibilities

UI

Responsible only for presentation.

Services

Responsible for business logic.

Infrastructure

Responsible for external resources.

Filesystem

Responsible for persistence.

---

# Dependency Direction

Dependencies always point downward.

```
User Interface

↓

Services

↓

Infrastructure

↓

Operating System
```

Reverse dependencies are forbidden.

---

# Benefits

- Easier maintenance.
- Better readability.
- Better modularity.
- Simplified testing.
- Easier onboarding.
- Lower coupling.

---

# Drawbacks

Requires discipline to maintain service boundaries.

---

# Impact

High.

This ADR defines the overall architecture of the project.

Future ADRs must comply with this decision.

---

# References

Architecture.md

Project Structure.md

Coding Standards.md

---

# History

2026-08-06

Initial version.

Accepted.