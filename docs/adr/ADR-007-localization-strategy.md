# ADR-007 — Localization Strategy

**Project:** AutoZipBackup

**ADR:** 007

**Status:** Accepted

**Date:** 2026-08-06

**Decision Maker:** Project Architecture Team

**Supersedes:** None

**Superseded By:** None

---

# 1. Context

AutoZipBackup is intended to be usable by users speaking different languages.

Version 1.0 officially supports:

- Spanish (default)
- English

The application must allow language switching at runtime without requiring a restart.

Localization must remain independent from business logic.

---

# 2. Problem Statement

Embedding user-visible text directly into the source code creates several problems:

- Difficult maintenance.
- Impossible runtime language switching.
- Duplicate translations.
- Hardcoded UI strings.
- Difficult addition of new languages.

A centralized localization strategy is required.

---

# 3. Decision Drivers

The solution must:

- Support multiple languages.
- Allow runtime language changes.
- Keep business logic language-independent.
- Avoid duplicated translations.
- Be easy to extend.
- Be easy to test.

---

# 4. Alternatives Considered

## Alternative A — Hardcoded Strings

```python
label.config(text="Backup completed")
```

### Advantages

Simple.

### Disadvantages

- Impossible localization.
- Duplicate text.
- Difficult maintenance.

### Decision

Rejected.

---

## Alternative B — Constants Module

```python
STRINGS.BACKUP_COMPLETED
```

### Advantages

Centralized.

### Disadvantages

- Requires rebuilding for new languages.
- Difficult runtime switching.

### Decision

Rejected.

---

## Alternative C — JSON Translation Files

```
languages/

    es.json

    en.json
```

Loaded through a translation provider.

### Advantages

- Runtime switching.
- Easy to maintain.
- Human-readable.
- Easy to add languages.

### Decision

Accepted.

---

# 5. Decision

Localization is implemented using three components.

```text
UI

↓

LocalizationManager

↓

TranslationProvider

↓

languages/*.json
```

The business layer is completely unaware of the active language.

---

# 6. Components

## LocalizationManager

Responsibilities

- Keep track of the active language.
- Notify listeners when the language changes.
- Coordinate translation updates.

Must never read JSON files directly.

---

## TranslationProvider

Responsibilities

- Load translation files.
- Validate translation keys.
- Provide translated strings.
- Cache loaded translations.

Must never update the user interface.

---

## Localizable Widgets

Responsibilities

- Register with LocalizationManager.
- Refresh displayed text after language changes.

Widgets remain responsible only for presentation.

---

# 7. Translation Files

Official location:

```text
src/autozip/resources/languages/
```

Initial files:

```text
es.json

en.json
```

Each file must contain the same set of keys.

---

# 8. Translation Keys

Keys use snake_case.

Examples

```text
app_title

backup_started

backup_completed

backup_failed

settings

theme

language
```

Keys must be stable across versions.

---

# 9. Runtime Language Switching

Language changes follow this flow.

```text
User

↓

Settings Dialog

↓

LocalizationManager

↓

LanguageChanged Event

↓

Registered Widgets

↓

UI Refresh
```

The application should not require restarting.

---

# 10. Missing Translations

If a translation key is missing:

1. Try the default language.
2. Log a warning.
3. Display the key name only as a last resort.

The application must continue running.

---

# 11. Configuration

The selected language is persisted through the configuration subsystem.

Example:

```json
{
  "language": "es"
}
```

The localization module never writes configuration directly.

---

# 12. Event Integration

Language changes publish an event.

Example:

```text
LanguageChanged
```

Interested components update themselves after receiving the event.

---

# 13. Thread Safety

Language changes are initiated from the UI thread.

Translation loading may be cached internally.

UI updates must occur only on the main thread.

---

# 14. Future Extensions

The architecture supports additional languages.

Examples

- French
- German
- Portuguese
- Italian
- Japanese

No code changes should be required beyond adding new translation files.

---

# 15. Consequences

## Positive

- Runtime language switching.
- Low coupling.
- Easy maintenance.
- Easy addition of new languages.
- Clean separation of concerns.

## Negative

- Additional infrastructure.
- Translation files must remain synchronized.

---

# 16. Compliance Rules

Every code review should verify:

- No user-visible text is hardcoded.
- Translation keys use snake_case.
- Only TranslationProvider loads language files.
- Only LocalizationManager manages the active language.
- Widgets update through LanguageChanged events.
- Translation files contain matching keys.

---

# 17. Risks

Potential risks

- Missing translation keys.
- Inconsistent translation files.
- Untranslated new features.

Mitigation

- Validation during application startup.
- Automated key comparison tests.
- Warning logs for missing entries.

---

# 18. Impact

**Impact Level:** High

This ADR defines the official localization strategy for AutoZipBackup.

All future user-visible text must follow this architecture.

---

# 19. Related Documents

- architecture.md
- project-structure.md
- coding-standards.md
- ADR-001 Project Architecture
- ADR-003 Configuration Management
- ADR-005 Event Dispatcher Architecture

---

# 20. Revision History

| Date | Version | Description |
|------|---------|-------------|
| 2026-08-06 | 1.0 | Initial version. Approved. |

---

# End of Document