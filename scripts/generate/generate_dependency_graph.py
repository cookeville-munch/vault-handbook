#!/usr/bin/env python3
"""
Generate a dependency graph (Mermaid flowchart) of module dependencies.
Reads from modules.json (produced by generate_unified_discovery.py) to build
real cross-reference edges and complexity-based styling.
"""
import json
import re
import sys
import argparse
from pathlib import Path


def generate_mermaid(json_data):
    """Generate Mermaid flowchart from dependency graph JSON data."""
    lines = ['# Module Dependency Graph', '', '```mermaid', 'flowchart TD']

    level_colors = {
        'Foundational': '#4CAF50',
        'Intermediate': '#FF9800',
        'Advanced': '#F44336'
    }

    modules = json_data.get('modules', {})

    for mod_id, meta in sorted(modules.items()):
        color = level_colors.get(meta.get('level', 'Unknown'), '#9E9E9E')
        label = mod_id.replace('-', '\\n')
        lines.append(f'    {mod_id}[["{label}\\n{meta.get("level", "Unknown")}"]]')
        lines.append(f'    style {mod_id} fill:{color},color:white')

    lines.append('')

    edge_set = set()
    for mod_id, meta in sorted(modules.items()):
        deps = meta.get('module_references', [])
        for dep in sorted(deps):
            edge_key = (dep, mod_id)
            if edge_key not in edge_set and dep in modules:
                lines.append(f'    {dep} --> {mod_id}')
                edge_set.add(edge_key)

    lines.append('```')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate module dependency graph from modules.json')
    parser.add_argument('--modules-json', default='modules/modules.json', help='Path to modules.json metadata')
    parser.add_argument('--output', required=True, help='Output Mermaid .md file')
    args = parser.parse_args()

    json_path = Path(args.modules_json)
    if not json_path.exists():
        print(f"Error: {json_path} does not exist. Run generate_unified_discovery.py first.")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    print(f"Building dependency graph from {json_path}")
    mermaid = generate_mermaid(json_data)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(mermaid + '\n', encoding='utf-8')
    print(f"Generated dependency graph at {args.output}")

    modules = json_data.get('modules', {})
    total_deps = sum(len(m.get('module_references', [])) for m in modules.values())
    print(f"\nModules: {len(modules)}")
    print(f"Dependencies: {total_deps}")
    for mod_id, meta in sorted(modules.items()):
        print(f"  {mod_id}: {meta['level']} | {meta['word_count']} words | {meta['section_count']} sections | complexity: {meta['complexity_score']:.2f}")


if __name__ == '__main__':
    main()