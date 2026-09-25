#!/usr/bin/env python3
"""
Generate metadata for all .md files in the modules directory.
Processes all module files to create:
- All files metadata JSON (modules/all_files_metadata.json)
"""
import json
import re
import sys
from pathlib import Path


def extract_module_info(file_path, modules_dir):
    """Extract metadata and content from a .md file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title from H1
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else file_path.stem

    # Extract level badge
    level_match = re.search(r'\*\*Level:\s*(Foundational|Intermediate|Advanced)\*\*', content)
    level = level_match.group(1) if level_match else 'Unknown'

    # Extract introduction (first paragraph after Level badge, or after H1 if no Level badge)
    intro = ""
    lines = content.split('\n')
    # Find the line with the Level badge or the H1
    level_index = next((i for i, line in enumerate(lines) if re.search(r'\*\*Level:', line)), -1)
    h1_index = next((i for i, line in enumerate(lines) if line.startswith('# ')), -1)
    start_index = max(level_index, h1_index) + 1
    if start_index < len(lines):
        # Find the first non-empty line after start_index
        for i in range(start_index, len(lines)):
            if lines[i].strip() and not lines[i].startswith('#'):
                intro = lines[i].strip()
                break

    # Extract key terms/glossary terms from content
    glossary_terms = []
    glossary_matches = re.findall(r'\*\*([^\*\*]+)\*\*:\s*([^\n]+)', content)
    glossary_terms.extend([term for term, _ in glossary_matches])

    # Extract references to other modules/files (from See Also section)
    module_refs = []
    see_also_match = re.search(r'## See Also\n(.*?)(?=\n---|\n## |\Z)', content, re.DOTALL)
    if see_also_match:
        section = see_also_match.group(1)
        refs = re.findall(r'\[(\d{2}-[^\]\s]*)\]', section)
        module_refs.extend(refs)

    # Compute complexity score: word count × section count
    word_count = len(content.split())
    sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
    section_count = len(sections)
    complexity_score = round(word_count * section_count / 1000, 2)

    # Get file identifier (relative path from modules_dir)
    file_id = str(file_path.relative_to(modules_dir))

    return {
        'metadata': {'title': title},
        'introduction': intro,
        'glossary_terms': glossary_terms[:10],
        'module_references': module_refs,
        'path': str(file_path.relative_to(modules_dir).parent),  # directory of the file
        'word_count': word_count,
        'section_count': section_count,
        'complexity_score': complexity_score,
        'level': level,
        'file_id': file_id
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate metadata for all .md files in modules directory')
    parser.add_argument('--modules-dir', default='modules', help='Root directory containing module folders')
    parser.add_argument('--output', default='modules/all_files_metadata.json', help='Output JSON file')
    args = parser.parse_args()

    modules_dir = Path(args.modules_dir)
    if not modules_dir.exists():
        print(f"Error: Directory {modules_dir} does not exist")
        sys.exit(1)

    # Initialize modules info dictionary
    all_files_info = {}

    # Process all .md files in the modules directory tree
    for file_path in sorted(modules_dir.rglob('*.md')):
        try:
            file_info = extract_module_info(file_path, modules_dir)
            all_files_info[file_info['file_id']] = file_info
        except Exception as e:
            print(f"Skipping {file_path}: {e}")
            continue

    if not all_files_info:
        print("WARNING: No files found for processing")
        return

    print(f"Processing {len(all_files_info)} files...")

    # Write JSON metadata
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_files_info, f, indent=2, ensure_ascii=False)
    print(f"Generated all files metadata at {output_path}")


if __name__ == '__main__':
    main()