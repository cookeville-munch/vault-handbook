# Structure Overview of the Kink Handbook Repository

This document provides a comprehensive overview of the repository's organization, naming conventions, and migration strategy to ensure consistency and scalability.

## Directory Structure

```
├── content
│   └── modules
│       ├── 01-orientation-consent/
│       ├── 02-session-techniques/
│       ├── 03-special-populations/
│       ├── 04-advanced-topics/
│       ├── 05-assessment-evaluation/
│       ├── 06-digital-fetish-tools-technology-safety/
│       ├── 07-online-kink-community-moderation-safety/
│       ├── 08-financial-accessibility-economic-justice-in-education/
│       ├── 09-aging-elder-lifespan-education/
│       ├── fire-play/
│       │   └── 10-advanced-fire-play.md
│       └── sharps-play/
│           └── 11-advanced-sharps-play.md
│
├── diagrams/
│   └── contribution-workflow.js
│
├── docs/
│   ├── CONTRIBUTING.md
│   ├── PROTECTED-BRANCHES.md
│   └── structure.md          ← This document
│
├── .github/
│   └── workflows/
│       └── pr-validation.yml
│
├── README.md                 ← Updated with Advanced Topics navigation
├── new_toc.md                ← Updated with module navigation
└── scripts/
    └── cleanup_legacy_modules.sh
```

## Naming Conventions

| Element | Convention | Example |
|--------|----------|---------|
| **Module Directory** | `NN- descriptive-name` (two-digit prefix) | `10-advanced-fire-play` |
| **Content Files** | `NN-description.md` | `10-advanced-fire-play.md` |
| **Difficulty Level** | `foundation`, `intermediate`, `advanced`, `expert` | `difficulty-level: advanced` |
| **Numeric Prefix** | Sequential numbering with gaps for future additions | 01, 02, ..., 09, **10**, **11**, 12... |

### Resolution Strategy for Conflicts
When existing directory numbers conflict with new module numbers:
1. Use the **next available higher number** (e.g., if 05 exists, start new modules at 10)
2. **Preserve original directories** in `/modules` until migration is complete
3. **Update navigation automatically** via Script v3

## Migration Strategy

The migration from the legacy migration to the unified `modules/` structure enables:
- **Centralized organization** under a content container
- **Consistent numbering** for future expansion
- **Structured validation** via GitHub Actions
- **Automatic navigation updates** for README.md and new_toc.md

### Migration Phases
1. **Phase 1**: Copy existing modules to `modules/` (completed)
2. **Phase 2**: Create new advanced modules (10-advanced-fire-play, 11-advanced-sharps-play)
3. **Phase 3**: Clean up legacy `/modules` directory (pending)
4. **Phase 4**: Finalize cleanup script for legacy directory removal

## Directory Relationships

```
modules/               ← Primary location for all modules
  ├── fire-play/
  │   └── 10-advanced-fire-play.md
  ├── sharps-play/
  │   └── 11-advanced-sharps-play.md
  └── ... (existing modules 01-09)

modules/                     ← Current unified module location
  ├── 01-orientation-consent/
  ├── 02-session-techniques/
  ...
  └── superpowers/
```

## Future Expansion Protocol
1. **Add New Module**:
   - Choose next available number (12, 13...)
   - Create directory structure under `modules/NN-new-name/`
   - Add metadata in module file frontmatter
   - Content automatically appears in navigation

2. **Validation**:
   - GitHub Actions validates directory structure and naming
   - PR template requires evidence of shared need
   - Navigation updates automatically

## Naming Philosophy
The numbering system was designed to:
- **Prevent collisions** with existing modules (01-09)
- **Maintain progression** (10 → 11 → 12...)
- **Reflect advancement level** (10/11 = "advanced" topics)
- **Allow future additions** without renumbering
- **Signify priority** (higher numbers = more specialized topics)

This structure ensures that as the handbook evolves, new content will seamlessly integrate with existing material while maintaining organic growth patterns and easy discoverability.