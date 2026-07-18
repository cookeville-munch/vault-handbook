# Module Validation Checklist Template

This checklist ensures all modules in the kink handbook meet documentation standards for consistency, accessibility, and cross-referencing.

## Required Elements (All Must Pass)

### 1. Frontmatter & Title
- [ ] YAML frontmatter exists (`---` delimiters)
- [ ] `title` field present and non-empty
- [ ] Title length ≤ 60 characters
- [ ] H1 header (`# Title`) matches frontmatter title exactly

### 2. Introduction
- [ ] Introduction paragraph follows H1 header
- [ ] Length: 50-500 characters
- [ ] Clear summary of module purpose

### 3. Module References (Minimum 3)
- [ ] At least 3 `[module-name](path)` references
- [ ] All referenced modules exist in `content/modules/`
- [ ] References use numeric prefix format (e.g., `01-test`)

### 4. Required Sections
- [ ] `## Overview` - Detailed module description
- [ ] `## Key Terms` - Bold terms with definitions
- [ ] `## Related Modules` - Categorized connections
- [ ] `## Practice Examples` - Practical applications
- [ ] `## Common Challenges` - Anticipated difficulties
- [ ] `## Learning Objectives` - Numbered outcomes
- [ ] `## Further Exploration` - Advanced topics
- [ ] `## References` - Source citations

### 5. Key Terms Quality
- [ ] Minimum 3 bold terms (`**Term**`) in Key Terms section
- [ ] Each term has clear definition after colon
- [ ] Terms relevant to module domain

### 6. Cross-References
- [ ] "Builds upon" category with prerequisite modules
- [ ] "Connects with" category with peer modules
- [ ] "Shares concepts with" category for related topics

## Recommended Elements (Should Include)

### 7. Quick Reference Table
- [ ] `## Quick Reference` table with columns
- [ ] At least 3 concept/definition pairs

### 8. Practice Examples
- [ ] Minimum 2 numbered examples
- [ ] Each example has practical context
- [ ] Examples demonstrate different complexity levels

### 9. Common Challenges
- [ ] Minimum 2 specific challenges
- [ ] Each has mitigation strategy

### 10. Learning Objectives
- [ ] Minimum 3 measurable outcomes
- [ ] Use active verbs (demonstrate, apply, analyze)

## Accessibility & Formatting

### 11. Markdown Standards
- [ ] No trailing whitespace
- [ ] Consistent heading hierarchy (H1→H2→H3)
- [ ] Tables use pipes and dashes correctly
- [ ] Code blocks specify language

### 12. Link Validity
- [ ] All internal links resolve
- [ ] External links use HTTPS
- [ ] No bare URLs (use descriptive link text)

### 13. Terminology Consistency
- [ ] Terms match glossary definitions
- [ ] No duplicate term definitions
- [ ] Acronyms defined on first use

## Validation Commands

```bash
# Run structural validation
python3 scripts/validation/validate_structure.py content/modules

# Check link integrity
npx markdown-link-check content/modules/**/*.md

# Validate Mermaid diagrams (if present)
npx mmdc -i diagrams/module-flow.js -o /dev/null --quiet
```

## CI/CD Integration (Future)

When enabled, these checks will run automatically:
```yaml
# .github/workflows/module-validation.yml
- name: Validate Module Structure
  run: python3 scripts/validation/validate_structure.py content/modules
  
- name: Check Links
  run: npx markdown-link-check content/modules/**/*.md
  
- name: Generate Docs
  run: python3 scripts/generate/generate_module_index.py
```

## Migration Notes

For existing modules not meeting standards:
1. Add missing frontmatter
2. Ensure H1 matches title
3. Add introduction paragraph
4. Create 3+ valid module references
5. Add required sections
6. Define 3+ bold key terms
7. Run validation to confirm