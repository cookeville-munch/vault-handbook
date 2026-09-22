#!/usr/bin/env python3
"""
Generate a comprehensive module index and glossary for the kink handbook.
Processes all module README files to create:
- Module table of contents with descriptions
- Cross-references and terminology glossary
- Module dependency matrix
- Generated navigation structure
"""
import json
import re
import os
import argparse
from pathlib import Path
from datetime import datetime

def validate_readme_structure(readme_path):
    """Validate that a module README follows required structure."""
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check 1: Valid frontmatter structure
    has_frontmatter = bool(re.search(r'---\s*\n(.*?)\n---\s*\n', content, re.DOTALL))
    if not has_frontmatter:
        return {"valid": False, "error": "Missing frontmatter (--- ... ---)"}
    
    # Check 2: Title in frontmatter
    frontmatter_match = re.search(r'---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not frontmatter_match:
        return {"valid": False, "error": "Invalid frontmatter structure"}
    
    frontmatter = frontmatter_match.group(1)
    title_match = re.search(r'title\s*:\s*"?([^"\s]+)"?', frontmatter, re.IGNORECASE)
    if not title_match:
        return {"valid": False, "error": "Missing 'title' in frontmatter"}
    
    title = title_match.group(1)
    if not title or len(title) > 60:
        return {"valid": False, "error": f"Title invalid or too long: {title}"}
    
    # Check 3: H1 header with title
    title_header_match = re.search(r'^#\s+' + re.escape(title) + r'\s*$', content, re.MULTILINE)
    if not title_header_match:
        return {"valid": False, "error": "H1 header doesn't match frontmatter title"}
    
    # Check 4: Introduction paragraph
    intro_parser = re.search(r'^#\s+' + re.escape(title) + r'\s*\n\s*\n(.+?)\s*\n', content, re.MULTILINE | re.DOTALL)
    if not intro_parser:
        return {"valid": False, "error": "Missing introduction paragraph"}
    
    intro = intro_parser.group(1).strip()
    if not intro:
        return {"valid": False, "error": "Empty introduction"}
    
    # Check 5: At least 3 module references
    module_refs = re.findall(r'\[(\d{2}(?:-\w+)*)\]', content)
    if len(module_refs) < 3:
        return {"valid": False, "error": "At least 3 [module] references required"}
    
    return {"valid": True}

def extract_module_info(readme_path):
    """Extract metadata and content from a module README file."""
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Validate structure first
    validation = validate_readme_structure(readme_path)
    if not validation["valid"]:
        raise ValueError(f"README validation failed: {validation['error']}")
    
    # Extract metadata
    metadata = {}
    match = re.search(r'---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"\'')
    
    # Extract title from frontmatter or first h1
    if 'title' not in metadata:
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
    
    # Extract introduction
    intro = ""
    lines = content.split('\n')
    in_content = False
    for line in lines:
        if in_content and line.strip() and not line.startswith('#'):
            intro = line.strip()
            break
        if line.startswith('# ') and metadata.get('title'):
            in_content = True
    
    # Extract key terms/glossary terms from content
    glossary_terms = []
    glossary_matches = re.findall(r'\*\*([^\*\*]+)\*\*:\s*([^\n]+)', content)
    glossary_terms.extend([term for term, _ in glossary_matches])
    
    # Extract references to other modules
    module_refs = []
    module_matches = re.findall(r'\[(\d{2}-[^\]]*)\]', content)
    module_refs.extend(module_matches)
    
    return {
        'metadata': metadata,
        'introduction': intro,
        'glossary_terms': glossary_terms[:10],
        'module_references': module_refs,
        'path': str(readme_path.parent)
    }

def generate_module_toc(modules_info):
    """Generate markdown table of contents for modules."""
    toc = "# Module Table of Contents\n\n"
    toc += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    
    # Table headers
    toc += "| Module | Title | Description | Key Terms | References |\n"
    toc += "|--------|-------|-------------|-----------|------------|\n"
    
    for module_name, info in sorted(modules_info.items()):
        # Format module name for display
        display_name = module_name.replace('-', ' ').title()
        
        # Extract title from metadata
        title = info['metadata'].get('title', 'Untitled')
        
        # Truncate description
        description = info['introduction'][:100] + "..." if info['introduction'] and len(info['introduction']) > 100 else info['introduction'] or "(No introduction found)"
        
        # Format glossary terms (limit to 3)
        glossary_display = ', '.join(info['glossary_terms'][:3])
        
        # Format module references
        refs_display = ', '.join(info['module_references'][:3])
        
        toc += f"| [{module_name}]({info['path']}/) | {title} | {description} | {glossary_display} | {refs_display} |\n"
    
    toc += f"\n**Total Modules:** {len(modules_info)}\n"
    return toc

def generate_glossary(modules_info):
    """Generate a combined glossary of all module terms."""
    glossary = "# Combined Terminology Glossary\n\n"
    glossary += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    
    all_terms = {}
    
    # Aggregate terms from all modules
    for module_name, info in modules_info.items():
        for term in info['glossary_terms']:
            if term not in all_terms:
                all_terms[term] = {
                    'module': module_name,
                    'definition': "",  # We could extract this more intelligently
                    'module_path': info['path']
                }
    
    # Generate glossary sections
    glossary += "## Module-Specific Terms\n\n"
    
    for module_name in sorted(modules_info.keys()):
        module_terms = [term for term in modules_info[module_name]['glossary_terms'] if term in all_terms]
        if module_terms:
            glossary += f"### {module_name}\n\n"
            for term in module_terms:
                glossary += f"- **{term}** (defined in {module_name})\n"
            glossary += "\n"
    
    glossary += "## Complete Alphabetical List\n\n"
    for term in sorted(all_terms.keys()):
        glossary += f"- **{term}**\n"
    
    glossary += f"\n**Total Unique Terms:** {len(all_terms)}\n"
    return glossary

def generate_dependency_matrix(modules_info):
    """Generate a module dependency matrix."""
    matrix = "# Module Dependency Matrix\n\n"
    matrix += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    
    modules = sorted(modules_info.keys())
    
    # Header
    matrix += "| Module | Referenced Modules | Depended Upon By |\n"
    matrix += "|--------|-------------------|------------------|\n"
    
    for module_name in modules:
        info = modules_info[module_name]
        
        # Modules this module references
        refs = info['module_references']
        refs_display = ', '.join(refs)
        
        # Modules that reference this module
        referenced_by = []
        for other_name, other_info in modules_info.items():
            if other_name != module_name and module_name in other_info['module_references']:
                referenced_by.append(other_name)
        
        refs_by_display = ', '.join(referenced_by)
        
        matrix += f"| [{module_name}]({info['path']}/) | {refs_display} | {refs_by_display} |\n"
    
    matrix += "\n**Dependency Analysis:**\n"
    matrix += "- **Direct Dependencies:** Modules referenced directly via markdown links\n"
    matrix += "- **Indirect Dependencies:** Modules implied through content relationships\n"
    return matrix

def main():
    parser = argparse.ArgumentParser(description='Generate module index and glossary')
    parser.add_argument('--modules-dir', default='modules', help='Root directory containing module folders')
    parser.add_argument('--output-index', default='docs/index/generated_module_toc.md', help='Output path for module table of contents')
    parser.add_argument('--output-glossary', default='docs/glossary/generated_module_glossary.md', help='Output path for terminology glossary')
    parser.add_argument('--output-matrix', default='docs/dependencies/generated_dependency_matrix.md', help='Output path for dependency matrix')
    
    args = parser.parse_args()
    
    # Initialize modules info dictionary
    modules_info = {}
    
    # Process all modules (allow both pure numeric directories and digits-hyphen-name pattern)
    modules_dir = Path(args.modules_dir)
    for dir_path in sorted(modules_dir.iterdir()):
        if dir_path.is_dir():
            # Match directories that start with digits
            dir_name = dir_path.name
            match = re.match(r'^(\d{2})(-.+)?$', dir_name)
            if match:
                # Extract the numeric prefix for the key
                module_key = match.group(1)
                
                # Check for README.md or similar
                readme_path = dir_path / 'README.md'
                if readme_path.exists():
                    module_info = extract_module_info(readme_path)
                    modules_info[module_key] = module_info
    
    if not modules_info:
        print("WARNING: No modules found for processing")
        return
    
    # Generate and write outputs
    print(f"Processing {len(modules_info)} modules...")
    
    # Generate table of contents
    toc_content = generate_module_toc(modules_info)
    Path(args.output_index).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_index).write_text(toc_content, encoding='utf-8')
    print(f"Generated module TOC at {args.output_index}")
    
    # Generate glossary
    glossary_content = generate_glossary(modules_info)
    Path(args.output_glossary).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_glossary).write_text(glossary_content, encoding='utf-8')
    print(f"Generated module glossary at {args.output_glossary}")
    
    # Generate dependency matrix
    matrix_content = generate_dependency_matrix(modules_info)
    Path(args.output_matrix).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_matrix).write_text(matrix_content, encoding='utf-8')
    print(f"Generated dependency matrix at {args.output_matrix}")

if __name__ == '__main__':
    main()