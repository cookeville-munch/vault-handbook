# Sample Pull Request: Module Validation Workflow

This document demonstrates the CI validation process for module changes using the new validation workflows.

## Example PR: Update to 01-orientation-consent Module

### Title: "Update consent principles documentation"

### Description:
This PR updates the affirmative consent principles documentation in the 01-orientation-consent module to reflect updated guidelines.

### Files Changed:
- `modules/01-orientation-consent/01-affirmative-consent-principles.md`
- `modules/01-orientation-consent/02-ongoing-communication-checkins.md`

### Expected CI Validation Results:

```yaml
# .github/workflows/pr-validation.yml (excerpt)
jobs:
  foundational-module-validation:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Validate 01-orientation-consent
        if: github.ref != 'main'
        run: |
          if [ -d modules/01-orientation-consent ]; then
            python3 scripts/validation/validate_structure.py 01
          fi

      - name: Validate 02-session-techniques
        if: github.ref != 'main'
        run: |
          if [ -d modules/02-session-techniques ]; then
            python3 scripts/validation/validate_structure.py 02
          fi
```

### Expected Output:

```
✅ Validation passed for 01-orientation-consent
✅ All frontmatter fields present
✅ File naming conventions followed
✅ Cross-references valid
```

### Sample PR Comment from CI:

> **Module Validation Results**
> ```
> 🔍 01-orientation-consent:
> ✅ Status: PASS
> → Files validated: 7
> → Errors found: 0
> 
> 🔍 02-session-techniques:
> ✅ Status: PASS
> → Files validated: 5
> → Errors found: 0
> ```

### If Validation Fails:

```bash
# Example error output
🔍 01-orientation-consent:
❌ Status: FAIL
→ Files validated: 6
→ Errors found: 1
→ Error: Missing 'difficulty-level' in frontmatter of 01-affirmative-consent-principles.md
```

### Resolution Steps:
1. Fix the frontmatter in the affected file
2. Push updated commit to PR
3. CI will re-run validation automatically
4. PR will show green checkmarks when all validations pass

### Merge Requirements:
- All CI checks must pass
- At least 2 approvals from maintainers
- All conversations resolved
- No merge conflicts

---

## Testing the Workflow Locally

```bash
# Run validation locally before pushing
cd /path/to/kink-plans
python3 scripts/validation/validate_structure.py --modules-dir modules --modules 01 02 03

# Expected output:
# Validating modules in: modules
# 🔍 01-orientation-consent: ✅ PASS (7 files, 0 errors)
# 🔍 02-session-techniques: ✅ PASS (5 files, 0 errors)
# 🔍 03-special-populations: ✅ PASS (3 files, 0 errors)
```

---

*Last updated: 2026-07-11*
*Documentation version: 1.0*