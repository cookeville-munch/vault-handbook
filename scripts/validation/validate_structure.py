#!/usr/bin/env python3
"""Module validation script for foundational modules 01-03

Validates module structure, frontmatter, and naming conventions
specifically for modules 01-orientation-consent, 02-session-techniques, and 03-special-populations.
"""

import os
import json
import argparse
from pathlib import Path

def validate_frontmatter(file_path):
    """Validate frontmatter requirements for modules 01-03"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Check for required frontmatter fields
        required_fields = ['title', 'date', 'author', 'difficulty-level']
        
        for field in required_fields:
            if f'{field}:' not in content:
                return False, f"Missing required frontmatter field: {field}"
        
        # Check frontmatter format
        if not content.startswith('---'):
            return False, "Invalid frontmatter: missing opening separator"
            
        if '---' not in content[3:]:
            return False, "Invalid frontmatter: missing closing separator"
            
        return True, "Frontmatter validation passed"
        
    except Exception as e:
        return False, f"Error validating frontmatter: {str(e)}"

def validate_naming(file_path):
    """Validate file naming conventions"""
    filename = os.path.basename(file_path)
    
    # Check extension
    if not filename.endswith('.md'):
        return False, "File must have .md extension"
    
    # Check naming pattern (NN-description.md for modules 01-09)
    if not re.match(r'^[0-9]{2}-.*\.md$', filename):
        return False, f"Invalid naming pattern: {filename}"
        
    # Check module number (01-03 are foundational)
    module_number = filename.split('-')[0]
    if not module_number in ['01', '02', '03']:
        return False, f"Invalid module number: {module_number}"
        
    return True, "Naming validation passed"

def validate_content(file_path):
    """Validate content structure"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for structure markers
        errors = []
        
        if '# ' not in content:
            errors.append("Missing H1 title")
            
        if '## Overview' not in content:
            errors.append("Missing Overview section")
            
        if '## Technical Requirements' not in content:
            errors.append("Missing Technical Requirements section")
            
        if len(content.strip()) < 500:
            errors.append("Content too short (< 500 characters)")
            
        return len(errors) == 0, "; ".join(errors) if errors else "Content validation passed"
        
    except Exception as e:
        return False, f"Error validating content: {str(e)}"

def validate_module_structure(modules_dir):
    """Validate modules 01-03 structure"""
    modules = ['01-orientation-consent', '02-session-techniques', '03-special-populations']
    results = {}
    
    for module in modules:
        module_path = os.path.join(modules_dir, module)
        if not os.path.isdir(module_path):
            results[module] = {"status": "ERROR", "message": "Module directory not found"}
            continue
        
        module_files = [f for f in os.listdir(module_path) if f.endswith('.md')]
        
        if not module_files:
            results[module] = {"status": "ERROR", "message": "No .md files in module"}
            continue
        
        module_results = {"files": [], "status": "OK", "messages": []}
        
        for file in module_files:
            file_path = os.path.join(module_path, file)
            
            # Validate frontmatter
            frontmatter_ok, frontmatter_msg = validate_frontmatter(file_path)
            
            # Validate naming
            naming_ok, naming_msg = validate_naming(file_path)
            
            # Validate content
            content_ok, content_msg = validate_content(file_path)
            
            file_info = {
                "filename": file,
                "path": file_path,
                "frontmatter_valid": frontmatter_ok,
                "naming_valid": naming_ok,
                "content_valid": content_ok,
                "frontmatter_msg": frontmatter_msg,
                "naming_msg": naming_msg,
                "content_msg": content_msg
            }
            
            module_results["files"].append(file_info)
            
            # Check for any errors
            if not (frontmatter_ok and naming_ok and content_ok):
                module_results["status"] = "ERROR"
                module_results["messages"].append(f"  File {file}: {frontmatter_msg}; {naming_msg}; {content_msg}")
        
        results[module] = module_results
    
    return results

def print_validation_results(results):
    """Print validation results in a readable format"""
    print("=" * 80)
    print("MODULE VALIDATION REPORT")
    print("=" * 80)
    
    overall_status = "SUCCESS"
    
    for module, module_data in results.items():
        print(f"\n{module}:")
        print("-" * 40)
        
        if isinstance(module_data, dict) and "status" in module_data:
            if module_data["status"] == "OK":
                print(f"✅ Status: PASS")
                print(f"   Files validated: {len(module_data['files'])}")
                print(f"   Errors found: 0")
            else:
                print(f"❌ Status: FAIL")
                print(f"   Files validated: {len(module_data['files'])}")
                print(f"   Errors found: {len(module_data['messages'])}")
                print("   Error details:")
                for error in module_data["messages"]:
                    print(f"     {error}")
                
                overall_status = "FAILURE"
        else:
            print(f"❌ Status: ERROR - {module_data}")
            overall_status = "FAILURE"
    
    print("\n" + "=" * 80)
    if overall_status == "SUCCESS":
        print("VALIDATION RESULT: SUCCESS - All modules 01-03 are properly structured")
    else:
        print("VALIDATION RESULT: FAILURE - Some modules have issues")
    print("=" * 80)
    
    return overall_status == "SUCCESS"

def main():
    parser = argparse.ArgumentParser(description="Validate modules 01-03 structure")
    parser.add_argument("--modules-dir", default="content/modules", help="Directory containing modules")
    
    args = parser.parse_args()
    modules_dir = args.modules_dir
    
    if not os.path.exists(modules_dir):
        print(f"Error: Directory '{modules_dir}' does not exist")
        return 1
    
    print(f"Validating modules in: {modules_dir}")
    
    # Validate modules
    results = validate_module_structure(modules_dir)
    
    # Print results
    success = print_validation_results(results)
    
    # Generate detailed JSON report
    report = {
        "timestamp": "2026-07-11T00:00:00Z",
        "modules_dir": modules_dir,
        "summary": {},
        "detailed_results": results
    }
    
    # Calculate summary statistics
    total_files = 0
    valid_files = 0
    errors = []
    
    for module, module_data in results.items():
        if isinstance(module_data, dict) and "files" in module_data:
            for file_data in module_data["files"]:
                total_files += 1
                if (file_data["frontmatter_valid"] and 
                    file_data["naming_valid"] and 
                    file_data["content_valid"]):
                    valid_files += 1
                else:
                    errors.append(f"{module}/{file_data['filename']}: {file_data['naming_msg']}")
    
    report["summary"] = {
        "total_files": total_files,
        "valid_files": valid_files,
        "invalid_files": total_files - valid_files,
        "overall_status": "PASS" if success else "FAIL",
        "error_count": len(errors)
    }
    
    # Write JSON report
    import json
    with open(f"{modules_dir}/validation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\nValidation report written to: {modules_dir}/validation_report.json")
    
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())