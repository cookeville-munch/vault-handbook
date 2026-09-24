#!/usr/bin/env python3
"""
Generate a comprehensive module index and glossary for the kink handbook.
Processes all module README files to create:
- Module table of contents with descriptions
- Cross-references and terminology glossary
- Module dependency matrix
- Generated navigation structure
- JSON metadata with complexity scores and recommendations
"""
import json
import re
import os
import sys
import argparse
from collections import defaultdict
from pathlib import Path
from datetime import datetime


def extract_module_info(readme_path, modules_dir):
    """Extract metadata and content from a module file."""
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title from H1 or frontmatter title
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else readme_path.stem

    # Extract level badge
    level_match = re.search(r'\*\*Level:\s*(Foundational|Intermediate|Advanced)\*\*', content)
    level = level_match.group(1) if level_match else 'Unknown'

    # Extract introduction (first paragraph after Level badge)
    intro = ""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if re.search(r'\*\*Level:', line):
            # Get text after Level line until next heading or blank
            for j in range(i+1, len(lines)):
                if lines[j].startswith('#') or not lines[j].strip():
                    break
                intro = lines[j].strip()
                if intro:
                    break
            break

    # Extract key terms/glossary terms from content
    glossary_terms = []
    glossary_matches = re.findall(r'\*\*([^\*\*]+)\*\*:\s*([^\n]+)', content)
    glossary_terms.extend([term for term, _ in glossary_matches])

    # Extract references to other modules
    module_refs = extract_see_also_refs(content)

    # Compute complexity score: word count × section count
    word_count = len(content.split())
    sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
    section_count = len(sections)
    complexity_score = round(word_count * section_count / 1000, 2)

    # Get module directory name for recommendations
    mod_dir_name = readme_path.parent.name

    return {
        'metadata': {'title': title},
        'introduction': intro,
        'glossary_terms': glossary_terms[:10],
        'module_references': module_refs,
        'path': str(readme_path.parent.relative_to(modules_dir)),
        'word_count': word_count,
        'section_count': section_count,
        'complexity_score': complexity_score,
        'level': level,
        'module_id': mod_dir_name
    }


def extract_see_also_refs(content):
    """Extract module references from See Also section."""
    see_also_match = re.search(r'## See Also\n(.*?)(?=\n---|\n## |\Z)', content, re.DOTALL)
    if not see_also_match:
        return []
    section = see_also_match.group(1)
    refs = re.findall(r'\[(\d{2}-[^\]\s]*)\]', section)
    return [r for r in refs if re.match(r'^\d{2}-', r)]


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

        # Format introduction as description
        description = info['introduction'][:150] + '...' if len(info['introduction']) > 150 else info['introduction']

        # Format key terms
        key_terms = ', '.join(info['glossary_terms'][:5])

        # Format references
        refs = ', '.join(info['module_references'])

        toc += f"| {display_name} | {title} | {description} | {key_terms} | {refs} |\n"

    return toc


def generate_glossary(modules_info):
    """Generate terminology glossary from module key terms."""
    glossary = "# Terminology Glossary\n\n"
    glossary += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"

    # Collect all terms with their definitions and source modules
    all_terms = defaultdict(list)
    for module_name, info in modules_info.items():
        for term in info['glossary_terms']:
            all_terms[term].append(module_name)

    for term in sorted(all_terms.keys()):
        sources = ', '.join(all_terms[term])
        glossary += f"## {term}\n\n"
        glossary += f"*Source modules: {sources}*\n\n"
        glossary += "---\n\n"

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


def generate_modules_json(modules_info, output_path):
    """Generate a comprehensive JSON metadata index of all modules with progress tracking."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    # Build reference lookup
    ref_lookup = defaultdict(set)
    for mod_name, info in modules_info.items():
        for ref in info['module_references']:
            ref_lookup[ref].add(mod_name)

    # Compute recommendations: modules with no unmet prerequisites
    all_modules = set(modules_info.keys())
    ready = set()
    remaining = set(all_modules)

    # Iteratively find modules whose referenced modules are all present
    while remaining:
        found = False
        for mod in list(remaining):
            refs = modules_info[mod]['module_references']
            if all(r in ready or r in all_modules for r in refs):
                ready.add(mod)
                remaining.discard(mod)
                found = True
                break
        if not found:
            ready.update(remaining)
            break

    # Sort ready modules by complexity (simpler first)
    ready_list = sorted(ready, key=lambda m: modules_info[m]['complexity_score'])

    # Build progress tracking structure
    progress = {
        'completed_modules': [],
        'last_accessed': None,
        'study_streak': 0,
        'total_modules_completed': 0,
        'completion_percentage': 0.0,
        'unlocked_modules': [],
        'blocked_modules': []
    }

    # Compute unlocked modules based on empty completed set
    unlocked = []
    blocked = []
    for mod_name in sorted(all_modules):
        refs = modules_info[mod_name]['module_references']
        unmet = [r for r in refs if r in all_modules and r not in progress['completed_modules']]
        if not unmet:
            unlocked.append(mod_name)
        else:
            blocked.append({
                'module': mod_name,
                'unmet_prerequisites': unmet
            })

    progress['unlocked_modules'] = unlocked
    progress['blocked_modules'] = blocked

    json_data = {
        'modules': {},
        'recommendations': {},
        'progress': progress,
        'generated': datetime.now().isoformat()
    }

    for mod_name in sorted(modules_info.keys()):
        info = modules_info[mod_name]
        refs = info['module_references']

        # Compute what's unlocked if this module is completed
        next_unlocked = []
        for candidate in all_modules:
            if candidate == mod_name or candidate in progress['completed_modules']:
                continue
            candidate_refs = modules_info[candidate]['module_references']
            candidate_met = [r for r in candidate_refs if r in progress['completed_modules'] or r not in all_modules]
            if len(candidate_met) == len(candidate_refs):
                next_unlocked.append(candidate)

        json_data['modules'][mod_name] = {
            'level': info['level'],
            'title': info['metadata'].get('title', mod_name),
            'word_count': info['word_count'],
            'section_count': info['section_count'],
            'complexity_score': info['complexity_score'],
            'module_references': refs,
            'complexity_rank': 'simple' if info['complexity_score'] < 50 else ('medium' if info['complexity_score'] < 200 else 'complex'),
            'next_unlocked': next_unlocked
        }

        # Determine what to learn next
        next_recs = []
        for candidate in ready_list:
            if candidate != mod_name and candidate not in refs:
                next_info = modules_info[candidate]
                next_recs.append({
                    'module': candidate,
                    'title': next_info['metadata'].get('title', candidate),
                    'level': next_info['level'],
                    'complexity': next_info['complexity_score']
                })
                break  # Just first recommendation

        json_data['recommendations'][mod_name] = {
            'next_module': next_recs[0] if next_recs else None,
            'prerequisites_met': len([r for r in refs if r in ready]) / max(len(refs), 1) if refs else 1.0,
            'next_unlocked': next_unlocked[:3]
        }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    return str(output)


def main():
    parser = argparse.ArgumentParser(description='Generate module index and glossary')
    parser.add_argument('--modules-dir', default='modules', help='Root directory containing module folders')
    parser.add_argument('--output-index', default='docs/index/generated_module_toc.md', help='Output path for module table of contents')
    parser.add_argument('--output-glossary', default='docs/glossary/generated_module_glossary.md', help='Output path for terminology glossary')
    parser.add_argument('--output-matrix', default='docs/dependencies/generated_dependency_matrix.md', help='Output path for dependency matrix')
    parser.add_argument('--output-json', default='modules/modules.json', help='Output path for modules JSON metadata')
    args = parser.parse_args()

    modules_dir = Path(args.modules_dir)
    if not modules_dir.exists():
        print(f"Error: Directory {modules_dir} does not exist")
        sys.exit(1)

    # Initialize modules info dictionary
    modules_info = {}

    # Process all modules
    for dir_path in sorted(modules_dir.iterdir()):
        if not dir_path.is_dir():
            continue
        match = re.match(r'^(\d{2})(-.+)?$', dir_path.name)
        if not match:
            continue

        readme_path = dir_path / 'README.md'
        if not readme_path.exists():
            # Try the .md file with matching name
            md_files = list(dir_path.glob('*.md'))
            readme_path = md_files[0] if md_files else None
            if not readme_path:
                continue

        try:
            module_info = extract_module_info(readme_path, modules_dir)
            modules_info[dir_path.name] = module_info
        except ValueError as e:
            print(f"Skipping {dir_path.name}: {e}")
            continue

    if not modules_info:
        print("WARNING: No modules found for processing")
        return

    print(f"Processing {len(modules_info)} modules...")

    toc_content = generate_module_toc(modules_info)
    Path(args.output_index).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_index).write_text(toc_content, encoding='utf-8')
    print(f"Generated module TOC at {args.output_index}")

    glossary_content = generate_glossary(modules_info)
    Path(args.output_glossary).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_glossary).write_text(glossary_content, encoding='utf-8')
    print(f"Generated module glossary at {args.output_glossary}")

    matrix_content = generate_dependency_matrix(modules_info)
    Path(args.output_matrix).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_matrix).write_text(matrix_content, encoding='utf-8')
    print(f"Generated dependency matrix at {args.output_matrix}")

    # Generate modules.json with metadata and recommendations
    json_output = generate_modules_json(modules_info, args.output_json)
    print(f"Generated modules metadata at {json_output}")

    # Print complexity summary
    print("\nComplexity Summary:")
    for mod_name in sorted(modules_info.keys()):
        info = modules_info[mod_name]
        print(f"  {mod_name}: {info['level']} | {info['word_count']} words | {info['section_count']} sections | complexity: {info['complexity_score']}")


if __name__ == '__main__':
    main()