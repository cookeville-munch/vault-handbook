#!/usr/bin/env python3
"""
Validate module README structure for the kink handbook.
Checks for required frontmatter, sections, and references.
"""
import re
import sys
from pathlib import Path

def validate_readme(readme_path):
    """Validate a single module README.md file."""
    errors = []
    warnings = []
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"valid": False, "errors": [f"Failed to read file: {e}"], "warnings": []}
    
    # Check 1: Valid frontmatter structure
    frontmatter_match = re.search(r'---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not frontmatter_match:
        errors.append("Missing frontmatter (--- ... ---)")
    else:
        frontmatter = frontmatter_match.group(1)
        
        # Check for title in frontmatter
        title_match = re.search(r'title\s*:\s*"?([^"\s]+)"?', frontmatter, re.IGNORECASE)
        if not title_match:
            errors.append("Missing 'title' in frontmatter")
        else:
            title = title_match.group(1)
            if not title:
                errors.append("Title is empty in frontmatter")
            elif len(title) > 60:
                warnings.append(f"Title is long ({len(title)} chars): {title}")
    
    # Check 2: H1 header matching title
    if frontmatter_match and title_match:
        title = title_match.group(1)
        h1_match = re.search(r'^#\s+' + re.escape(title) + r'\s*$', content, re.MULTILINE)
        if not h1_match:
            # Try case-insensitive match
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if h1_match:
                errors.append(f"H1 header '{h1_match.group(1)}' doesn't match frontmatter title '{title}'")
            else:
                errors.append("Missing H1 header")
    
    # Check 3: Introduction paragraph after title
    if frontmatter_match and title_match:
        title = title_match.group(1)
        # Find content after H1
        intro_parser = re.search(r'^#\s+' + re.escape(title) + r'\s*\n\s*\n(.+?)\s*\n', content, re.MULTILINE | re.DOTALL)
        if not intro_parser:
            errors.append("Missing introduction paragraph after H1")
        else:
            intro = intro_parser.group(1).strip()
            if not intro:
                errors.append("Empty introduction paragraph")
            elif len(intro) < 50:
                warnings.append(f"Introduction very short ({len(intro)} chars)")
            elif len(intro) > 500:
                warnings.append(f"Introduction very long ({len(intro)} chars)")
    
    # Check 4: At least 3 module references
    module_refs = re.findall(r'\[(\d{2}[-\w]*)\]\([^)]+\)', content)
    if len(module_refs) < 3:
        errors.append(f"Need at least 3 module references (found {len(module_refs)}): {module_refs}")
    else:
        # Verify referenced modules exist
        for ref in module_refs:
            ref_path = readme_path.parent.parent / ref / "README.md"
            if not ref_path.exists():
                warnings.append(f"Referenced module doesn't exist: {ref}")
    
    # Check 5: Required sections
    required_sections = ["## Overview", "## Key Terms", "## Related Modules"]
    for section in required_sections:
        if section not in content:
            warnings.append(f"Missing recommended section: {section}")
    
    # Check 6: Glossary terms in Key Terms section
    key_terms_section = re.search(r'## Key Terms\n(.+?)(?=\n## |\Z)', content, re.DOTALL)
    if key_terms_section:
        terms_content = key_terms_section.group(1)
        # Count bold terms
        bold_terms = re.findall(r'\*\*([^\*\*]+)\*\*', terms_content)
        if len(bold_terms) < 3:
            warnings.append(f"Key Terms section has only {len(bold_terms)} bold terms (recommend 3+)")
    else:
        warnings.append("Key Terms section not found")
    
    # Check 7: Learning Objectives
    if "## Learning Objectives" not in content:
        warnings.append("Missing Learning Objectives section")
    
    # Check 8: Quick Reference table
    if "## Quick Reference" not in content:
        warnings.append("Missing Quick Reference table")
    
    # Check 9: Practice Examples
    if "## Practice Examples" not in content:
        warnings.append("Missing Practice Examples section")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_structure.py <modules_dir>")
        sys.exit(1)
    
    modules_dir = Path(sys.argv[1])
    if not modules_dir.exists():
        print(f"Error: Directory {modules_dir} does not exist")
        sys.exit(1)
    
    print(f"Validating modules in {modules_dir}")
    print("=" * 60)
    
    all_valid = True
    for dir_path in sorted(modules_dir.iterdir()):
        if not dir_path.is_dir():
            continue
        
        # Match directories that start with digits
        dir_name = dir_path.name
        match = re.match(r'^(\d{2})(-.+)?$', dir_name)
        if not match:
            continue
        
        readme_path = dir_path / "README.md"
        if not readme_path.exists():
            print(f"\n⚠ {dir_name}: No README.md found")
            continue
        
        result = validate_readme(readme_path)
        
        if result["valid"]:
            print(f"\n✓ {dir_name}: VALID")
        else:
            print(f"\n✗ {dir_name}: INVALID")
            all_valid = False
        
        for error in result["errors"]:
            print(f"  ERROR: {error}")
        for warning in result["warnings"]:
            print(f"  WARN:  {warning}")
    
    print("\n" + "=" * 60)
    if all_valid:
        print("All modules passed validation!")
        sys.exit(0)
    else:
        print("Some modules failed validation!")
        sys.exit(1)

if __name__ == "__main__":
    main()