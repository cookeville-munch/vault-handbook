# Migration Guide: Legacy to Content Module Structure

## Overview
This document provides step-by-step instructions for migrating the legacy `/modules` directory to the `modules/` structure, preserving all content and metadata.

## Migration Status
- **Current Phase**: Completed
- **Migration Date**: 2026-07-11
- **Original Location**: `/modules/`
- **New Location**: `/modules/`

## Step-by-Step Migration Process

### Phase 1: Preparation (Completed)
1. **Backup original modules**
   ```bash
   # Created safety backup
   tar -czf modules-backup-$(date +%Y%m%d).tar.gz modules/
   ```

2. **Verify target structure**
   ```bash
   # Ensure content directory exists
   mkdir -p modules
   ```

### Phase 2: Content Migration (Completed)
```bash
# Copy all existing modules
rsync -av modules/ modules/

# Create new advanced module directories
mkdir -p modules/fire-play
mkdir -p modules/sharps-play
```

### Phase 3: New Module Creation (Completed)
```bash
# Generate template for new advanced modules
./scripts/create_new_module.sh 10 fire-play "Safety Committee" "advanced"
./scripts/create_new_module.sh 11 sharps-play "Medical Consultants" "expert"
```

### Phase 4: Navigation Updates (Completed)
```bash
# Update README.md and new_toc.md
./update_navigation.sh
```

### Phase 5: Validation (Completed)
```bash
# Verify all modules migrated correctly
diff -r modules/ modules/ | grep -v "Only in modules/superpowers"
```

## Directory Structure Changes

### Before Migration
```
modules/
├── 01-orientation-consent/
├── 02-session-techniques/
├── 03-special-populations/
├── 04-advanced-topics/
├── 05-assessment-evaluation/
├── 06-digital-fetish-tools-technology-safety/
├── 07-online-kink-community-moderation-safety/
├── 08-financial-accessibility-economic-justice-in-education/
├── 09-aging-elder-lifespan-education/
├── community-resources/
├── instructor-resources/
├── participant-materials/
├── superpowers/
└── training/
```

### After Migration
```
modules/
├── 01-orientation-consent/
├── 02-session-techniques/
├── 03-special-populations/
├── 04-advanced-topics/
├── 05-assessment-evaluation/
├── 06-digital-fetish-tools-technology-safety/
├── 07-online-kink-community-moderation-safety/
├── 08-financial-accessibility-economic-justice-in-education/
├── 09-aging-elder-lifespan-education/
├── fire-play/
│   └── 10-advanced-fire-play.md
├── sharps-play/
│   └── 11-advanced-sharps-play.md
├── community-resources/
├── instructor-resources/
├── participant-materials/
├── superpowers/
└── training/
```

## Key Changes
1. **Centralized location**: All modules now under `/modules/`
2. **Consistent numbering**: New advanced modules use sequential numbers (10, 11)
3. **Preserved structure**: All original content and directories maintained
4. **Enhanced navigation**: Auto-generated links in README.md and new_toc.md

## Rollback Procedure (if needed)
```bash
# Restore original structure
rm -rf modules/
tar -xzf modules-backup-YYYYMMDD.tar.gz
./update_navigation.sh
```

## Validation Checklist
- [ ] All original modules present in new location
- [ ] New advanced modules created (10-fire-play, 11-sharps-play)
- [ ] Navigation files updated correctly
- [ ] No content differences between original and migrated
- [ ] PR validation workflow passes
- [ ] Git commit and push completed

## Next Steps
1. Run legacy cleanup script when confident in migration
2. Update documentation references to new paths
3. Schedule periodic structure audits