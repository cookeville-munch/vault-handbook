#!/usr/bin/env python3
"""
Validation Script for Kink Handbook Modules

Validates module structure, frontmatter, and naming conventions
with different standards for existing vs new modules.
"""

import os
import re
import json
import sys
import argparse

def validate_frontmatter(file_path):
    """Validate frontmatter requirements"""
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
            return False, "Missing opening --- separator"
        
        if '---' not in content.split('---')[1]:
            return False, "Missing closing --- separator"
            
        return True, "Frontmatter validation passed"
        
    except Exception as e:
        return False, f"Error validating frontmatter: {str(e)}"

def validate_naming(file_path):
    """Validate file naming conventions"""
    filename = os.path.basename(file_path)
    
    # Must end with .md
    if not filename.endswith('.md'):
        return False, "File must have .md extension"
    
    # Must follow NN-description.md pattern
    if not re.match(r'^[0-9]{2}-.*\.md$', filename):
        return False, f"Violates naming convention: {filename}"
    
    # Check module number (01-09 for foundational, 10+ for advanced)
    module_number = filename.split('-')[0]
    if not re.match(r'^[0-9]{2}$', module_number):
        return False, f"Invalid module number pattern: {module_number}"
    
    return True, "Naming validation passed"

def validate_content(file_path):
    """Validate content structure"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        errors = []
        
        # Must have H1 heading
        if '# ' not in content:
            errors.append("Missing H1 title (should start with '#')")
        
        # Should contain section markers (flexible)
        section_count = 0
        if '## Overview' in content:
            section_count += 1
        if '## Core Principles' in content or '## Principles' in content:
            section_count += 1
        if '## Techniques' in content or '## Methods' in content:
            section_count += 1
        if '## Case Studies' in content:
            section_count += 1
        if '## Safety Protocols' in content or '## Safety' in content:
            section_count += 1
        
        # Require at least 2 sections for substantial content
        if section_count < 2:
            errors.append("Insufficient section structure (need at least 2 of: Overview, Principles, Techniques, Case Studies, Safety)")
        
        # Content length check
        if len(content.strip()) < 300:
            errors.append("Content too short (< 300 characters)")
        
        if errors:
            return False, "; ".join(errors)
        else:
            return True, "Content validation passed"
            
    except Exception as e:
        return False, f"Error validating content: {str(e)}"

def validate_module_structure(modules_dir):
    """Validate modules with different standards for existing vs new"""
    # Get all module directories that match the pattern
    modules = []
    try:
        for item in os.listdir(modules_dir):
            item_path = os.path.join(modules_dir, item)
            if os.path.isdir(item_path):
                # Only validate directories that look like module directories
                # (NN-name or NN-name where NN is 01-99)
                if re.match(r'^[0-9]{2}-', item):
                    modules.append(item)
    except PermissionError:
        pass
    
    results = {}
    
    for module in modules:
        module_path = os.path.join(modules_dir, module)
        try:
            module_files = [f for f in os.listdir(module_path) if f.endswith('.md')]
        except (PermissionError, FileNotFoundError):
            results[module] = {"status": "ERROR", "message": "Cannot access module directory", "files": []}
            continue
        
        if not module_files:
            results[module] = {"status": "ERROR", "message": "No .md files in module", "files": []}
            continue
        
        module_results = {"files": [], "status": "OK", "messages": []}
        
        # Determine if this is a new module (starts with 10 or higher) or existing
        is_new_module = re.match(r'^(1[0-9]|[2-9][0-9])-', module)
        
        for file in module_files:
            file_path = os.path.join(module_path, file)
            
            # Validate frontmatter - required for new modules, optional for existing
            frontmatter_ok, frontmatter_msg = validate_frontmatter(file_path)
            if is_new_module and not frontmatter_ok:
                frontmatter_ok = False  # Keep the failure for new modules
            elif not frontmatter_ok:
                frontmatter_ok = True  # Accept missing frontmatter for existing modules
                frontmatter_msg = "Frontmatter optional for existing modules"
            
            # Validate naming convention
            naming_ok, naming_msg = validate_naming(file_path)
            
            # Validate content structure
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
            
            # Track errors - be stricter for new modules
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
                print(f"   Files validated: {len(module_data.get('files', []))}")
                print(f"   Errors found: 0")
                print(f"   Modules validated: {module}")
            else:
                print(f"❌ Status: FAIL")
                print(f"   Files validated: {len(module_data.get('files', []))}")
                print(f"   Errors found: {len(module_data.get('messages', []))}")
                print("   Error details:")
                for error in module_data.get('messages', []):
                    print(f"     {error}")
                
                overall_status = "FAILURE"
            print()
        else:
            print(f"❌ Status: ERROR - {module_data}")
            overall_status = "FAILURE"
    
    print("\n" + "=" * 80)
    if overall_status == "SUCCESS":
        print("VALIDATION RESULT: SUCCESS - All modules are properly structured")
    else:
        print("VALIDATION RESULT: FAILURE - Some modules have issues")
    print("=" * 80)
    
    return overall_status == "SUCCESS"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate module structure")
    parser.add_argument("--modules-dir", default="content/modules", help="Directory containing modules")
    args = parser.parse_args()
    
    print(f"Validating modules in: {args.modules_dir}")
    
    # Validate modules
    results = validate_module_structure(args.modules_dir)
    
    # Print results
    success = print_validation_results(results)
    
    # Generate detailed JSON report
    report = {
        "timestamp": "2026-07-11T00:00:00Z",
        "modules_dir": args.modules_dir,
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
        "overall_status": "PASS" if total_files > 0 and valid_files == total_files else "FAIL",
        "error_count": len(errors)
    }
    
    # Write JSON report
    report_path = os.path.join(args.modules_dir, "validation_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\nValidation report written to: {report_path}")
    
    sys.exit(0 if success else 1)