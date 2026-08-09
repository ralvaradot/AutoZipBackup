# ADR-008 — Theme Management Strategy

**Project:** AutoZipBackup

**ADR:** 008

**Status:** Accepted

**Date:** 2026-08-06

**Decision Maker:** Project Architecture Team

**Supersedes:** None

**Superseded By:** None

---

# 1. Context

AutoZipBackup provides a modern desktop interface built with ttkbootstrap.

The application must allow users to switch between light and dark themes at runtime while maintaining a consistent visual experience.

Theme management must remain independent from business logic and user interface implementation details.

---

# 2. Problem Statement

If every window changes the ttkbootstrap theme independently:

- Theme changes become inconsistent.
- Code duplication increases.
- Future maintenance becomes difficult.
- UI components become tightly coupled to ttkbootstrap.

A centralized theme management strategy is required.

---

# 3. Decision Drivers

The selected solution must:

- Support runtime theme switching.
- Persist the selected theme.
- Minimize coupling.
- Be easy to extend.
- Support future custom themes.
- Avoid duplicated code.

---

# 4. Alternatives Considered

## Alternative A — Direct ttkbootstrap Calls

Each window executes:

```python
style.theme_use("darkly")
```

### Advantages

- Simple.
- Minimal code.

### Disadvantages

- High coupling.
- Theme changes scattered across the UI.
- Difficult maintenance.

### Decision

Rejected.

---

## Alternative B — Static Theme Helper

```
Theme.change(...)
```

### Advantages

- Easy access.

### Disadvantages

- Global mutable state.
- Difficult testing.
- Limited extensibility.

### Decision

Rejected.

---

## Alternative C — ThemeManager + ThemeProvider

A centralized manager controls the active theme.

A provider exposes available themes and validates requests.

### Advantages

- Clear responsibilities.
- Easy testing.
- Runtime switching.
- Extensible architecture.
- Consistent behavior.

### Decision

Accepted.

---

# 5. Decision

Theme management follows this architecture.

```text
UI

↓

ThemeManager

↓

ThemeProvider

↓

ttkbootstrap.Style
```

Only ThemeManager communicates with ttkbootstrap.

---

# 6. Components

## ThemeManager

Responsibilities

- Keep track of the active theme.
- Apply themes.
- Notify listeners.
- Persist the selected theme through the configuration subsystem.

Must never access configuration files directly.

---

## ThemeProvider

Responsibilities

- Register available themes.
- Validate theme names.
- Provide metadata.

Must never manipulate UI components.

---

## ThemeChanged Event

Published whenever the active theme changes.

Subscribers update their visual appearance accordingly.

---

# 7. Supported Themes

Version 1.0 officially supports:

Light themes

- Flatly
- Cosmo
- Litera

Dark themes

- Darkly
- Superhero

Additional themes may be added without modifying the architecture.

---

# 8. Runtime Theme Switching

Theme changes follow this flow.

```text
User

↓

Settings Dialog

↓

ThemeManager

↓

ThemeChanged Event

↓

Registered Windows

↓

Visual Refresh
```

Application restart is not required.

---

# 9. Theme Persistence

The selected theme is stored by the configuration subsystem.

Example:

```json
{
  "theme": "darkly"
}
```

ThemeManager requests persistence through SettingsManager.

It never writes JSON directly.

---

# 10. Validation

Before applying a theme:

- Verify the theme exists.
- Verify it is supported.
- Log invalid requests.

If validation fails:

- Apply the default theme.
- Record a warning.

---

# 11. Default Theme

Version 1.0 default:

```text
darkly
```

Default language remains:

```text
es
```

---

# 12. Thread Safety

Theme changes occur only on the UI thread.

Background workers must never apply or modify themes.

---

# 13. Event Integration

Changing the theme publishes:

```text
ThemeChanged
```

Interested components refresh themselves after receiving the event.

---

# 14. Future Extensions

Possible enhancements:

- User-defined themes.
- Corporate branding.
- Automatic OS theme detection.
- Scheduled theme changes.
- High-contrast accessibility themes.

These features should integrate without changing existing modules.

---

# 15. Consequences

## Positive

- Centralized theme management.
- Runtime switching.
- Low coupling.
- Easy maintenance.
- Future extensibility.

## Negative

- Additional infrastructure.
- Requires event propagation.

---

# 16. Compliance Rules

Every code review should verify:

- Only ThemeManager applies themes.
- Only ThemeProvider validates theme names.
- No window calls style.theme_use() directly.
- Theme changes publish ThemeChanged events.
- The selected theme is persisted through SettingsManager.
- Business modules remain independent of ttkbootstrap.

---

# 17. Risks

Potential risks

- Unsupported theme names.
- Third-party theme incompatibilities.
- Widgets not refreshing correctly.

Mitigation

- Theme validation.
- Automated UI smoke tests.
- Centralized refresh mechanism.

---

# 18. Impact

**Impact Level:** Medium

This ADR defines the official theme management strategy for AutoZipBackup.

Future theme-related functionality must comply with this architecture.

---

# 19. Related Documents

- architecture.md
- project-structure.md
- coding-standards.md
- ADR-001 Project Architecture
- ADR-003 Configuration Management
- ADR-005 Event Dispatcher Architecture
- ADR-007 Localization Strategy

---

# 20. Revision History

| Date | Version | Description |
|------|---------|-------------|
| 2026-08-06 | 1.0 | Initial version. Approved. |

---

# End of Document