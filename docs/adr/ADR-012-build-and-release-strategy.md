# ADR-012 — Build and Release Strategy

**Project:** AutoZipBackup

**ADR:** 012

**Status:** Accepted

**Date:** 2026-08-06

**Decision Maker:** Project Architecture Team

**Supersedes:** None

**Superseded By:** None

---

# 1. Context

AutoZipBackup is a desktop application developed in Python using ttkbootstrap.

The application must be distributed to end users without requiring a Python installation.

The release process must be reproducible, deterministic and independent from the development environment.

---

# 2. Problem Statement

If application packaging is performed manually:

- Releases become inconsistent.
- Different developers may generate different executables.
- Version tracking becomes unreliable.
- Deployment errors increase.

A standardized build and release process is required.

---

# 3. Decision Drivers

The solution must:

- Produce standalone executables.
- Be repeatable.
- Support automated builds.
- Generate versioned releases.
- Minimize manual intervention.
- Be compatible with Continuous Integration.

---

# 4. Alternatives Considered

## Alternative A — Execute Python Source Directly

Users install Python and project dependencies.

### Advantages

- Simple development.
- No packaging step.

### Disadvantages

- Poor user experience.
- Dependency conflicts.
- Difficult installation.

### Decision

Rejected.

---

## Alternative B — Nuitka

Compile Python to native binaries.

### Advantages

- High performance.
- Better source protection.

### Disadvantages

- Longer build times.
- More complex configuration.
- Greater maintenance effort.

### Decision

Rejected for Version 1.x.

May be reconsidered in Version 2.x.

---

## Alternative C — PyInstaller

Generate standalone executable packages.

### Advantages

- Mature.
- Stable.
- Widely adopted.
- Good Windows support.
- Easy integration.

### Decision

Accepted.

---

# 5. Decision

The project adopts the following release pipeline.

```text
Source Code

↓

Static Analysis

↓

Automated Tests

↓

Build

↓

Package

↓

Release
```

Each phase has a single responsibility.

---

# 6. Build Phase

Responsibilities

- Install dependencies.
- Validate source code.
- Execute static analysis.
- Execute automated tests.
- Verify architecture rules.

A failed build never produces release artifacts.

---

# 7. Package Phase

Packaging tool

```
PyInstaller
```

Generated artifacts

```
AutoZipBackup.exe
```

Supporting resources

```
resources/

languages/

themes/

icons/
```

Resources are packaged together with the executable.

---

# 8. Release Phase

Every release contains:

- Executable
- LICENSE
- README
- CHANGELOG
- Version information

Release packages are immutable after publication.

---

# 9. Versioning

The project adopts Semantic Versioning.

```
MAJOR.MINOR.PATCH
```

Examples

```
1.0.0

1.1.0

1.2.4

2.0.0
```

---

# 10. Build Configuration

Official build configuration

```
pyproject.toml
```

Packaging configuration

```
AutoZipBackup.spec
```

No developer-specific configuration should affect the generated executable.

---

# 11. Reproducible Builds

Two identical source trees should produce functionally equivalent release artifacts.

Build configuration must be stored in version control.

---

# 12. Platform Support

Official Version 1.x

- Windows 10
- Windows 11

Future versions may support:

- Linux
- macOS

The architecture remains platform independent.

---

# 13. Continuous Integration

Every release executes:

- Static analysis.
- Unit tests.
- Integration tests.
- Architecture tests.
- Packaging.
- Artifact validation.

Only successful builds may be published.

---

# 14. Signing

Executable signing is not mandatory for Version 1.x.

Future releases may include:

- Code signing certificates.
- Trusted publisher verification.

---

# 15. Logging

Build failures are logged.

Release artifacts include version metadata.

The application logs its version during startup.

---

# 16. Future Extensions

Possible future improvements

- Automatic updater.
- Delta updates.
- MSI installer.
- Microsoft Store package.
- Winget distribution.
- Chocolatey package.

The architecture supports these additions without structural changes.

---

# 17. Consequences

## Positive

- Reproducible releases.
- Consistent packaging.
- Easier deployment.
- Better automation.
- Reduced manual errors.

## Negative

- Additional build infrastructure.
- Packaging configuration maintenance.

---

# 18. Compliance Rules

Every code review should verify:

- Build scripts remain under version control.
- Packaging configuration is updated with new resources.
- Version numbers follow Semantic Versioning.
- Release artifacts are generated only through the official build process.
- No manual modifications are made to packaged executables.

---

# 19. Risks

Potential risks

- Missing packaged resources.
- Antivirus false positives.
- Platform-specific packaging issues.

Mitigation

- Automated packaging validation.
- Smoke testing of release artifacts.
- Resource verification before publishing.

---

# 20. Impact

**Impact Level:** Medium

This ADR defines the official build, packaging and release strategy for AutoZipBackup.

---

# 21. Related Documents

- architecture.md
- development-environment.md
- roadmap.md
- coding-standards.md
- ADR-011 Testing Strategy

---

# 22. Revision History

| Date | Version | Description |
|------|---------|-------------|
| 2026-08-06 | 1.0 | Initial version. Approved. |

---

# End of Document