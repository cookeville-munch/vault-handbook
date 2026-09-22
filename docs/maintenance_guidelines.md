# Module Maintenance Guidelines

## Overview
This document outlines best practices for maintaining the kink handbook module structure, ensuring consistency, accessibility, and long-term sustainability.

## Maintenance Schedule

### Daily Tasks
- [ ] Monitor GitHub Actions for PR validation status
- [ ] Review new PR submissions for compliance with standards
- [ ] Check for any failed CI/CD workflows
- [ ] Respond to community questions about module content

### Weekly Tasks
- [ ] Run validation script on recent changes
- [ ] Update navigation files if needed (`./update_navigation.sh`)
- [ ] Review test modules for cleanup candidates
- [ ] Check link integrity in README.md and new_toc.md

### Monthly Tasks
- [ ] Review and update frontmatter for all modules
- [ ] Verify numbering consistency across all modules
- [ ] Check for duplicate content or outdated information
- [ ] Validate cross-references between modules
- [ ] Update module creation template if needed
- [ ] Run comprehensive accessibility audit

### Quarterly Tasks
- [ ] Archive or remove obsolete test modules
- [ ] Update structure documentation to reflect current organization
- [ ] Review and refresh maintenance scripts
- [ ] Conduct accessibility compliance review (WCAG 2.1 AA)
- [ ] Generate module usage statistics report
- [ ] Review and update safety protocols as needed

### Bi-Annual Tasks
- [ ] Conduct full structure audit and numbering verification
- [ ] Remove legacy test files from module directories
- [ ] Update contribution guidelines based on community feedback
- [ ] Review and enhance module templates
- [ ] Perform security audit of all content
- [ ] Update migration guide with lessons learned

## Maintenance Scripts

### Update Navigation Script
```bash
./update_navigation.sh
```
- Updates README.md and new_toc.md with current module listings
- Should be run after adding/removing modules
- Safe to run frequently - only modifies navigation sections

### Module Creation Script
```bash
./scripts/create_new_module.sh [number] [topic] [author] [difficulty]
```
- Generates standardized module templates
- Automatically updates navigation
- Follows established naming conventions

### Legacy Cleanup Script
```bash
./scripts/cleanup_legacy_modules.sh
```
- Safely removes original `/modules` directory after migration verification
- Includes safety checks to prevent accidental data loss
- Requires manual confirmation before execution

### Structure Validation Script
```bash
python3 scripts/validate_structure.py
```
- Checks frontmatter consistency
- Verifies directory structure integrity
- Tests cross-reference validity
- Reports naming convention compliance

## Content Quality Standards

### Frontmatter Requirements
All modules must include:
- `title`: Clear, descriptive title (e.g., "Advanced Fire Play")
- `date`: Creation/update date in YYYY-MM-DD format
- `author`: Primary contributor or responsible team
- `difficulty-level`: One of: foundation, intermediate, advanced, expert

### Naming Conventions
- **Module directories**: `NN-description` (two-digit number followed by descriptive name)
- **Content files**: `NN-description.md` (matching directory name)
- **Numbers**: Sequential, starting at 01 for foundational topics
- **Special cases**: Advanced topics start at 10 to maintain spacing

### Structure Requirements
- Each module must be in its own directory under `modules/`
- All content files must be Markdown (.md) extension
- Module directories should contain at least one content file
- Avoid nesting modules within other modules unless logically grouped

## Validation Workflow

### Pre-Commit Checks
1. Run local validation:
   ```bash
   # Check frontmatter
   grep -L "title:" modules/*/*/*.md
   
   # Verify naming
   find modules -name "*.md" | grep -vE "^modules/[0-9]{2}-advanced-[a-z0-9-]+\.md$"
   ```
2. Run navigation update
3. Commit with descriptive message

### CI/CD Pipeline Checks
The GitHub Actions workflow (`pr-validation.yml`) automatically validates:
- Markdown and YAML linting
- Accessibility compliance (WCAG 2.1 AA)
- Mermaid diagram validation
- Link checking
- Frontmatter requirements
- Directory structure integrity

## Troubleshooting Common Issues

### Navigation Not Updating
**Symptoms**: New modules not appearing in README.md or new_toc.md
**Solutions**:
1. Ensure module follows naming convention (`NN-description.md`)
2. Run `./update_navigation.sh` manually
3. Check for typos in module directory names
4. Verify script has execute permissions

### Validation Failures
**Symptoms**: PR validation workflow failing
**Common Causes**:
1. Missing frontmatter fields
2. Incorrect file naming
3. Broken links in content
4. Accessibility violations
**Solutions**:
1. Add missing frontmatter fields
2. Rename files to match convention
3. Fix or remove broken links
4. Address accessibility issues (alt text, contrast, etc.)

### Content Migration Issues
**Symptoms**: Content discrepancies between old and new locations
**Solutions**:
1. Run diff check: `diff -r modules/ modules/`
2. Verify file permissions
3. Check for symbolic link issues
4. Re-run migration if necessary

## Documentation Updates

### When to Update Docs
- After significant structural changes
- When adding new maintenance procedures
- Upon discovering common validation issues
- When updating contribution guidelines
- Before/after major version releases

### Documentation Files
- `/docs/structure.md` - Current module hierarchy
- `/docs/migration_guide.md` - Migration procedures
- `/docs/maintenance_guidelines.md` - This document
- `/docs/PROTECTED-BRANCHES.md` - Branch protection rules
- `CONTRIBUTING.md` - Contribution procedures

## Emergency Procedures

### Content Corruption
1. Immediately stop all commits
2. Verify backup integrity
3. Restore from latest known good state
4. Document cause and prevention measures

### Accidental Deletion
1. Check Git history for deleted content
2. Restore from most recent commit
3. If not in history, check backups
4. Implement additional safety checks

### Validation Failures in CI
1. Examine workflow logs for specific errors
2. Fix issues locally before retrying
3. Consider temporary workflow adjustments if needed
4. Document resolution for future reference

## Contact Information

For maintenance questions or emergencies:
- Primary Maintainer: [Your Name/Team]
- Backup Contact: [Secondary Contact]
- Emergency Procedure: Refer to this document's Emergency Procedures section
- Documentation Location: `/docs/maintenance_guidelines.md`

## Version History
- **Version 1.0**: Initial release (2026-07-11)
- **Version 1.1**: Added validation workflow details
- **Version 1.2**: Included emergency procedures
- **Version 1.3**: Updated troubleshooting section

---
*Last updated: 2026-07-11*
*Maintained by: Kink Handbook Maintenance Team*