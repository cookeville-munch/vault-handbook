#!/usr/bin/env python3
"""
Validate module structure for the kink handbook.
Checks for required structural elements in all handbook modules.
"""
import re
import sys
import os
from pathlib import Path

# Directories to validate (exclude superpowers submodule)
VALIDATE_DIRS = [
    "01-orientation-consent",
    "02-session-techniques", 
    "03-special-populations",
    "04-advanced-topics",
    "05-assessment-evaluation",
    "06-digital-fetish-tools-technology-safety",
    "07-online-kink-community-moderation-safety",
    "08-financial-accessibility-economic-justice-in-education",
    "09-aging-elder-lifespan-education",
    "instructor-resources",
    "community-resources",
    "participant-materials",
    "training",
]

# Required structural elements
REQUIRED_ELEMENTS = [
    ("level_badge", r"\*\*Level: (Foundational|Intermediate|Advanced)\*\*"),
    ("learning_objectives", r"## Learning Objectives"),
    ("key_takeaways", r"## Key Takeaways"),
    ("see_also", r"## See Also"),
]

SKIP_FILES = {
    "AGENTS.md", "CLAUDE.md", "CODE_OF_CONDUCT.md", "GEMINI.md", 
    "README.md", "RELEASE-NOTES.md", "CONTRIBUTING.md", "CONTRIBUTING-ONBOARDING.md"
}

def check_file(filepath):
    """Check a single markdown file for required structural elements."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"valid": False, "errors": [f"Failed to read file: {e}"], "warnings": []}
    
    basename = os.path.basename(filepath)
    errors = []
    
    for element_name, pattern in REQUIRED_ELEMENTS:
        if not re.search(pattern, content, re.MULTILINE):
            errors.append(f"Missing: {element_name}")
    
    if not errors:
        return {"valid": True, "errors": [], "warnings": []}
    else:
        return {"valid": False, "errors": errors, "warnings": []}

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_structure.py <modules_dir>")
        sys.exit(1)
    
    modules_dir = Path(sys.argv[1])
    if not modules_dir.exists():
        print(f"Error: Directory {modules_dir} does not exist")
        sys.exit(1)
    
    print(f"Validating handbook modules in {modules_dir}")
    print("=" * 70)
    
    all_valid = True
    total_files = 0
    passing = 0
    failing = 0
    
    for mod_dir in VALIDATE_DIRS:
        mod_path = modules_dir / mod_dir
        if not mod_path.exists() or not mod_path.is_dir():
            print(f"⚠ {mod_dir}: Directory not found")
            continue
        
        for root, dirs, files in os.walk(mod_path):
            # Skip superpowers submodule
            if "superpowers" in root:
                continue
            
            for f in sorted(files):
                if not f.endswith('.md'):
                    continue
                if f in SKIP_FILES:
                    continue
                
                filepath = os.path.join(root, f)
                result = check_file(filepath)
                total_files += 1
                
                if result["valid"]:
                    passing += 1
                    print(f"✅ {filepath}")
                else:
                    failing += 1
                    all_valid = False
                    print(f"❌ {filepath}")
                    for error in result["errors"]:
                        print(f"   ERROR: {error}")
    
    print("=" * 70)
    print(f"Total files: {total_files}")
    print(f"Passing: {passing}")
    print(f"Failing: {failing}")
    
    if all_valid:
        print("All modules passed validation!")
        sys.exit(0)
    else:
        print("Some modules failed validation!")
        sys.exit(1)

if __name__ == "__main__":
    main()
