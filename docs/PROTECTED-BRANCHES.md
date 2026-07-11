# Protected Branch Configuration for `master`

This document defines the branch protection rules that should be applied to the `master` branch to ensure code quality, accessibility compliance, and community standards.

## Branch Protection Rules (to be configured in GitHub)

### 1. **Required Pull Request Reviews**
- **Required approving reviews**: 2
- **Dismiss stale pull request approvals when new commits are pushed**: ✓
- **Require review from Code Owners**: ✓
  - When a PR touches files with CODEOWNERS, those owners must review
- **Require approval of the most recent push**: ✓

### 2. **Status Checks Required**
The following checks must pass before merging:
- **markdownlint-cli** (Markdown linting)
- **yaml-lint** (YAML workflow linting)
- **accessibility-audit** (WCAG 2.1 AA via axe-core)
- **mermaid-validation** (Diagram syntax validation)
- **link-check** (Markdown link validation)
- **build-docs** (Documentation site build - for release tags)

### 3. **Include Administrators**
- Required status checks apply to administrators: ✓
- Required pull request reviews apply to administrators: ✓

### 4. **Restrict Who Can Push**
- **Allow specified actors to bypass required pull requests**: Empty (no bypass)
- **Allow specified actors to bypass required status checks**: Empty (no bypass)
- **Allow force pushes**: ✗ (disabled)
- **Allow deletions**: ✗ (disabled)

### 5. **Require Linear History**
- **Require a linear history**: ✓ (prevents merge commits, encourages squash-and-merge)
- **Allow force pushes**: ✗ (disabled)
- **Allow deletions**: ✗ (disabled)

### 6. **Require Conversation Resolution**
- **Require conversation resolution before merging**: ✓
  - All comments must be resolved before merge

### 7. **Restrict Merge Methods**
- **Allow merge commits**: ✗
- **Allow squash merging**: ✓ (recommended for clean history)
- **Allow rebase merging**: ✗
- **Automatically delete head branches**: ✓ (after merge)

## Special Protection for Certain Files

### Critical Content Areas
Files in these directories require additional review from domain experts:
- `modules/safety-protocols/` - Requires @safety-team review
- `docs/` and participant materials - Requires @accessibility-champion review
- `.github/workflows/` - Requires @devops-lead review

### Emergency Overrides
In case of critical security issues or legal compliance requirements:
- Repository administrators may bypass protections via GitHub UI
- All bypasses must be documented in the associated issue
- Emergency changes require post-implementation review within 24 hours

## Implementation Instructions

### Via GitHub UI:
1. Go to Settings → Branches → Branch protection rules
2. Click "Add rule" for branch `master`
3. Configure rules as specified above
4. Save changes

### Via GitHub CLI (gh):
```bash
# Set up branch protection
gh api \
  --method PUT \
  -f name="master" \
  -f required_approving_review_count=2 \
  -f dismiss_stale_reviews=true \
  -f require_code_owner_reviews=true \
  -f require_last_push_approval=true \
  -f required_status_checks[contexts][]="markdownlint-cli" \
  -f required_status_checks[contexts][]="yaml-lint" \
  -f required_status_checks[contexts][]="accessibility-audit" \
  -f required_status_checks[contexts][]="mermaid-validation" \
  -f required_status_checks[contexts][]="link-check" \
  -f required_status_checks[contexts][]="build-docs" \
  -f strict_required_status_checks_policy=true \
  -f enforce_admins=true \
  -f required_linear_history=true \
  -f allow_force_pushes=false \
  -f allow_deletions=false \
  -f required_resolve_threads=true \
  -f allow_squash_merge=true \
  -f allow_merge_commit=false \
  -f allow_rebase_merge=false \
  -f delete_branch_on_merge=true \
  /repos/:owner/:repo/branches/master/protection
```

## Verification
After applying protection rules, verify by:
1. Attempting to push directly to master (should be rejected)
2. Creating a PR with failing checks (should be blocked)
3. Creating a PR without required reviewers (should be blocked)
4. Confirming CODEOWNERS triggers correct review assignments

## Exceptions
These protection rules do NOT apply to:
- Documentation-only branches (if ever created for massive doc rewrites)
- Experimental feature branches (developers may force-push to their own feature branches)
- Release preparation branches (temporary branches for release coordination)

Protection rules apply only to the `master` branch which represents the official, released version of the handbook.