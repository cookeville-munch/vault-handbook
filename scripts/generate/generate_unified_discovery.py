#!/usr/bin/env python3
"""
Unified discovery pipeline for the handbook.
Reads all_files_metadata.json and generates:
- Module table of contents (grouped by directory)
- Glossary
- Dependency matrix (file-level)
- Module-level aggregates JSON (for backward compatibility with dependency graph generator)
"""
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def load_all_files_metadata(metadata_path):
    """Load all files metadata from JSON."""
    with open(metadata_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_module_toc(all_files_info, output_path):
    """Generate markdown table of contents grouped by directory."""
    # Group files by their parent directory
    by_dir = defaultdict(list)
    for file_id, info in sorted(all_files_info.items()):
        dir_name = info['path']
        by_dir[dir_name].append((file_id, info))

    toc = "# Module Table of Contents\n\n"
    toc += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"

    # Table headers
    toc += "| Directory | File | Title | Description | Level | References |\n"
    toc += "|-----------|------|-------|-------------|-------|------------|\n"

    for dir_name in sorted(by_dir.keys()):
        files = sorted(by_dir[dir_name], key=lambda x: x[1]['file_id'])
        for file_id, info in files:
            display_name = file_id.split('/')[-1].replace('.md', '').replace('-', ' ').title()
            title = info['metadata'].get('title', 'Untitled')
            description = info['introduction'][:150] + '...' if len(info['introduction']) > 150 else info['introduction']
            level = info['level']
            refs = ', '.join(info['module_references'][:5])
            toc += f"| {dir_name} | {display_name} | {title} | {description} | {level} | {refs} |\n"

    toc += f"\n**Total files:** {len(all_files_info)}\n"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(toc, encoding='utf-8')
    print(f"Generated module TOC at {output_path}")


def generate_glossary(all_files_info, output_path):
    """Generate terminology glossary from all files."""
    glossary = "# Terminology Glossary\n\n"
    glossary += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"

    # Collect all terms with their definitions and source files
    all_terms = defaultdict(list)
    for file_id, info in all_files_info.items():
        for term in info['glossary_terms']:
            all_terms[term].append(file_id)

    for term in sorted(all_terms.keys()):
        sources = ', '.join(all_terms[term])
        glossary += f"## {term}\n\n"
        glossary += f"*Source files: {sources}*\n\n"
        glossary += "---\n\n"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(glossary, encoding='utf-8')
    print(f"Generated module glossary at {output_path}")


def generate_dependency_matrix(all_files_info, output_path):
    """Generate a file-level dependency matrix."""
    matrix = "# File-Level Dependency Matrix\n\n"
    matrix += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"

    files = sorted(all_files_info.keys())

    # Header
    matrix += "| File | Referenced Files | Referenced By |\n"
    matrix += "|------|------------------|---------------|\n"

    for file_id in files:
        info = all_files_info[file_id]
        refs = info['module_references']
        refs_display = ', '.join(refs[:10])

        # Files that reference this file
        referenced_by = []
        for other_id, other_info in all_files_info.items():
            if other_id != file_id and file_id in other_info['module_references']:
                referenced_by.append(other_id)

        refs_by_display = ', '.join(referenced_by[:10])

        display_name = file_id.split('/')[-1].replace('.md', '')
        matrix += f"| {display_name} | {refs_display} | {refs_by_display} |\n"

    matrix += "\n**Dependency Analysis:**\n"
    matrix += "- **Direct Dependencies:** Files referenced directly via markdown links\n"
    matrix += "- File IDs shown are basenames; full paths available in JSON\n"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(matrix, encoding='utf-8')
    print(f"Generated dependency matrix at {output_path}")


def generate_module_aggregates(all_files_info, output_path):
    """Generate module-level aggregates for the 10 core modules (directories matching double-dash digit prefix)."""
    # Group files by module directory (the first component of the path)
    modules = defaultdict(list)
    for file_id, info in all_files_info.items():
        parts = file_id.split('/')
        if len(parts) >= 1:
            mod_dir = parts[0]
            if re.match(r'^\d{2}-', mod_dir):
                modules[mod_dir].append((file_id, info))

    # Build module-level metadata
    modules_info = {}
    for mod_id, files in modules.items():
        # Use the first file's title as module title, or derive from directory name
        first_file = files[0][1]
        # Try to find a file that looks like a module overview (contains "Module" in title or is the first)
        module_title = first_file['metadata'].get('title', mod_id.replace('-', ' ').title())
        # Find the level - most files in a module should have the same level
        levels = [info['level'] for _, info in files]
        level = max(set(levels), key=levels.count) if levels else 'Unknown'

        # Aggregate word count and section count
        total_words = sum(info['word_count'] for _, info in files)
        total_sections = sum(info['section_count'] for _, info in files)
        avg_complexity = sum(info['complexity_score'] for _, info in files) / len(files)

        # Collect all module references from all files in this module
        # Only keep module-level references (matching module directory names like 01-orientation-consent)
        all_refs = set()
        for _, info in files:
            for ref in info['module_references']:
                # Only keep references that match module directory pattern
                if re.match(r'^\d{2}-[a-z0-9-]+$', ref) and ref in modules:
                    all_refs.add(ref)

        modules_info[mod_id] = {
            'metadata': {'title': module_title},
            'level': level,
            'word_count': total_words,
            'section_count': total_sections,
            'complexity_score': round(avg_complexity, 2),
            'module_references': sorted(all_refs),
            'files': [file_id for file_id, _ in files]
        }

    # Compute recommendations (same logic as before)
    all_modules = set(modules_info.keys())
    ready = set()
    remaining = set(all_modules)

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

    ready_list = sorted(ready, key=lambda m: modules_info[m]['complexity_score'])

    # Build progress structure
    progress = {
        'completed_modules': [],
        'last_accessed': None,
        'study_streak': 0,
        'total_modules_completed': 0,
        'completion_percentage': 0.0,
        'unlocked_modules': [],
        'blocked_modules': []
    }

    completed = progress['completed_modules']

    # Compute unlocked modules based on completed set
    unlocked = []
    blocked = []
    for mod_name in sorted(all_modules):
        refs = modules_info[mod_name]['module_references']
        # Unmet prerequisites: module-level references not in completed set
        unmet = [r for r in refs if r in all_modules and r not in completed]
        if not unmet:
            unlocked.append(mod_name)
        else:
            blocked.append({
                'module': mod_name,
                'unmet_prerequisites': unmet
            })

    progress['unlocked_modules'] = unlocked
    progress['blocked_modules'] = blocked

    # Build recommendations
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
            if candidate == mod_name or candidate in completed:
                continue
            candidate_refs = modules_info[candidate]['module_references']
            candidate_unmet = [r for r in candidate_refs if r in all_modules and r not in completed]
            if not candidate_unmet:
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
                break

        json_data['recommendations'][mod_name] = {
            'next_module': next_recs[0] if next_recs else None,
            'prerequisites_met': len([r for r in refs if r in ready]) / max(len(refs), 1) if refs else 1.0,
            'next_unlocked': next_unlocked[:3]
        }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"Generated module aggregates at {output_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Unified discovery pipeline')
    parser.add_argument('--metadata', default='modules/all_files_metadata.json', help='Input all files metadata JSON')
    parser.add_argument('--output-index', default='docs/index/generated_module_toc.md', help='Output TOC')
    parser.add_argument('--output-glossary', default='docs/glossary/generated_module_glossary.md', help='Output glossary')
    parser.add_argument('--output-matrix', default='docs/dependencies/generated_dependency_matrix.md', help='Output dependency matrix')
    parser.add_argument('--output-modules-json', default='modules/modules.json', help='Output module aggregates JSON')
    args = parser.parse_args()

    all_files_info = load_all_files_metadata(args.metadata)

    generate_module_toc(all_files_info, args.output_index)
    generate_glossary(all_files_info, args.output_glossary)
    generate_dependency_matrix(all_files_info, args.output_matrix)
    generate_module_aggregates(all_files_info, args.output_modules_json)

    print("Unified discovery pipeline complete")


if __name__ == '__main__':
    main()