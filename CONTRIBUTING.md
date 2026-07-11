# Contributing to the Kink Handbook

Thank you for your interest in contributing to the Kink Handbook! This document outlines our contribution process, coding standards, and community guidelines.

## How We Work

We use a **feature branch workflow** with the following principles:
- `master` branch is always production-ready
- All changes go through feature branches and pull requests
- Every release is tagged with semantic versioning (`vX.Y.Z`)
- Continuous Integration runs on all PRs and release tags

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/vault-handbook.git
   cd vault-handbook
   ```
3. **Set up the upstream remote**:
   ```bash
   git remote add upstream https://github.com/elijah/vault-handbook.git
   git fetch upstream
   ```
4. **Create a feature branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name upstream/master
   ```
   Use descriptive branch names like:
   - `feature/qr-code-integration`
   - `fix/accessibility-color-contrast`
   - `doc/update-lesson-plan`
   - `refactor/safety-protocols-section`

## Making Changes

### File Organization
- Core content: `modules/` directory
- Documentation: `docs/` directory  
- Diagrams: `diagrams/` folder (Mermaid `.js` and SVG files)
- Workflows: `.github/workflows/` (CI/CD)
- Data: `data/` folder for metrics and feedback

### Coding Standards
**Markdown Files:**
- Use `#` for document title, `##` for sections, `###` for subsections
- Keep line lengths under 100 characters where practical
- Use blank lines between sections
- Escape special characters in tables

**Mermaid Diagrams (.js files):**
- Follow flowchart syntax standards
- Use descriptive node labels
- Keep diagrams focused on single concepts
- Test with `npx mmdc -i file.js -o /dev/null`

**SVG Files:**
- Keep file sizes reasonable (<500KB when possible)
- Use viewBox for scalability
- Include semantic IDs for screen readers when needed
- Validate with online SVG validators

### Documentation Standards
- All public-facing documentation must be in Markdown
- Include clear examples where applicable
- Link to related sections using relative paths
- Keep version numbers and dates updated in headers
- Follow inclusive language principles

## Testing Your Changes

### Local Testing
Before submitting a PR, run these checks locally:

1. **Markdown linting**:
   ```bash
   npx markdownlint-cli '**/*.md' --ignore 'node_modules/**' --ignore 'modules/superpowers/**'
   ```

2. **YAML linting** (for workflow files):
   ```bash
   npx yaml-lint '**/*.yml' '**/*.yaml' --ignore 'node_modules/**' --ignore 'modules/superpowers/**'
   ```

3. **Mermaid validation**:
   ```bash
   find diagrams -name "*.js" -exec npx mmdc -i {} -o /dev/null \;
   ```

4. **Link checking**:
   ```bash
   npx markdown-link-check '**/*.md' --ignore 'node_modules/**' --ignore 'modules/superpowers/**' --config .markdown-link-check.json
   ```

5. **Accessibility checks** (install axe-core CLI first):
   ```bash
   npx axe "**/*.html" --tags wcag2aa --save --dir ./axe-results || true
   ```

### CI Pipeline
When you open a PR, our GitHub Actions will automatically run:
- Linting (Markdown, YAML)
- Accessibility audit (WCAG 2.1 AA)
- Mermaid diagram validation
- Link checking

All checks must pass before merging.

## Pull Request Process

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** from your fork's branch to `upstream/master`

3. **PR Template** - Please fill out all sections:
   - **Description**: Clear summary of changes
   - **Type**: Feature, Bug Fix, Documentation, Refactor, etc.
   - **Related Issues**: Reference any GitHub issues
   - **Testing Performed**: What you tested locally
   - **Screenshots**: For UI/content changes
   - **Accessibility**: How you ensured accessibility compliance

4. **Review Process**:
   - Minimum **two** approving reviews required
   - All CI checks must pass
   - Address all review comments
   - Keep PR focused on a single logical change

5. **Merging**:
   - Use "Squash and merge" for clean history
   - Delete feature branch after merge (both local and remote)
   - Squash commit message should follow conventional commits:
     ```
     type(scope): description

     [optional body]

     [optional footer]
     ```
     Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Issue Reporting

When reporting issues, please include:
- **Clear title** summarizing the problem
- **Detailed description** with steps to reproduce
- **Expected vs actual behavior**
- **Screenshots** (if applicable)
- **Environment** (browser, device, etc.)
- **Relevant files/modules** involved

Use the appropriate issue template:
- Bug Report
- Feature Request  
- Documentation Improvement
- Accessibility Concern

## Community Guidelines

We follow these principles to maintain an inclusive, respectful community:

1. **Assume good intent** in all interactions
2. **Use inclusive language** - avoid ableist, racist, sexist, or exclusionary terms
3. **Respect boundaries** - both personal and professional
4. **Credit contributions** appropriately
5. **Welcome diverse perspectives** - neurodiversity, disability, cultural differences
6. **Provide constructive feedback** - focus on ideas, not people
7. **Follow the [Code of Conduct](CODE_OF_CONDUCT.md)**

## Version Control Practices

### Branching Strategy
- `master`: Production-ready branch
- `feature/*`: New features and enhancements
- `fix/*`: Bug fixes
- `doc/*`: Documentation-only changes
- `refactor/*`: Code restructuring without behavior changes
- `hotfix/*`: Urgent fixes for production issues

### Tagging Strategy
We use **semantic versioning** with annotated tags:
- `vX.Y.Z` where:
  - **X** = Major version (incompatible changes)
  - **Y** = Minor version (new features, backward compatible)
  - **Z** = Patch version (bug fixes, backward compatible)

To create a release tag:
```bash
git checkout master
git pull upstream master
git tag -a v1.4.0 -m "Release notes summary"
git push upstream v1.4.0
```

### Release Process
1. Ensure all CI checks pass on `master`
2. Create annotated tag as above
3. Push tag to trigger GitHub Actions release workflow
4. The workflow will:
   - Run all validation checks
   - Build documentation artifacts
   - Create GitHub release with changelog
   - Upload diagram assets
   - Send community notifications

## Getting Help

If you're stuck or need clarification:
1. Check existing documentation in `docs/`
2. Look at recent commits for similar changes
3. Ask in the `#contributors` channel on Discord
4. Tag maintainers in a comment on your PR
5. Open a "Question" issue if needed

## Recognition

All contributors are acknowledged in:
- GitHub contributors graph
- Release notes (for significant contributions)
- Community acknowledgments section (periodically)
- Special thanks in major version releases

Thank you for helping make the Kink Handbook more inclusive, accessible, and valuable for everyone! 🌈

---

*Last updated: 2026-07-10*
*Version: 1.0*