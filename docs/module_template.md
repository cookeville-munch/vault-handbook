# Documenting the dependencies and relationships between modules

This document maintains visibility of how our kink handbook modules connect and interact with each other. It serves multiple purposes:

1. **Navigation Aid**: Helps users find related content
2. **Validation Tool**: Ensures proper documentation structure
3. **Development Guide**: Shows where to add new dependencies

## Module Structure
Each module should follow this pattern in its README.md:

### Header Hierarchy
- Use H1 for module title
- H2 for section headers
- Avoid nested H3+ unless absolutely necessary

### Required Frontmatter
```yaml
---
(title: "Module Title")
---

### Content Requirements
- First paragraph should be a clear summary (<150 words)
- Include **bold** key terms with definitions
- List related modules with [markdown links](submodule-path)

### Validation Checks
- [x] Title in frontmatter
- [ ] Glossary terms defined
- [ ] At least 3 related modules
- [ ] Dependency matrix entries