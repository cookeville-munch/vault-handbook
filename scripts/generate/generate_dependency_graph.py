#!/usr/bin/env python3
"""
Generate a dependency graph (Mermaid flowchart) of module dependencies.
Parses See Also sections from all modules to build real cross-reference edges.
Also produces complexity scoring and next-module recommendations.
"""
import json
import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict

def parse_module_refs(content):
    """Extract module references from markdown links like [01-something](...)"""
    return re.findall(r'\[(\d{2}-[^\]\s]*)\]', content)

def parse_see_also(content):
    """Extract See Also section content from a module file."""
    see_also_match = re.search(r'## See Also\n(.*?)(?=\n---|\n## |\Z)', content, re.DOTALL)
    if not see_also_match:
        return []
    section = see_also_match.group(1)
    refs = parse_module_refs(section)
    return [r for r in refs if re.match(r'^\d{2}-', r)]

def extract_module_metadata(filepath):
    """Extract key metadata from a module file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filepath.stem
    
    level_match = re.search(r'\*\*Level:\s*(Foundational|Intermediate|Advanced)\*\*', content)
    level = level_match.group(1) if level_match else 'Unknown'
    
    word_count = len(content.split())
    
    sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
    
    see_also = parse_see_also(content)
    
    return {
        'title': title,
        'level': level,
        'word_count': word_count,
        'section_count': len(sections),
        'see_also': see_also,
        'complexity_score': word_count * len(sections) / 1000 if word_count > 0 else 0
    }

def build_dependency_graph(modules_dir):
    """Build a dependency graph from all module files."""
    graph = {}
    metadata = {}
    
    for dir_path in sorted(Path(modules_dir).iterdir()):
        if not dir_path.is_dir():
            continue
        if not re.match(r'^\d{2}-', dir_path.name):
            continue
        
        md_files = list(dir_path.glob('*.md'))
        if not md_files:
            continue
        
        target = md_files[0]
        mod_id = dir_path.name
        meta = extract_module_metadata(target)
        metadata[mod_id] = meta
        graph[mod_id] = meta['see_also']
    
    return graph, metadata

def generate_mermaid(graph, metadata):
    """Generate Mermaid flowchart from dependency graph."""
    lines = ['# Module Dependency Graph', '', '```mermaid', 'flowchart TD']
    
    level_colors = {
        'Foundational': '#4CAF50',
        'Intermediate': '#FF9800',
        'Advanced': '#F44336'
    }
    
    for mod_id, meta in sorted(metadata.items()):
        color = level_colors.get(meta['level'], '#9E9E9E')
        label = mod_id.replace('-', '\\n')
        lines.append(f'    {mod_id}[["{label}\\n{meta["level"]}"]]')
        lines.append(f'    style {mod_id} fill:{color},color:white')
    
    lines.append('')
    
    edge_set = set()
    for mod_id, deps in sorted(graph.items()):
        for dep in sorted(deps):
            edge_key = (dep, mod_id)
            if edge_key not in edge_set and dep in metadata:
                lines.append(f'    {dep} --> {mod_id}')
                edge_set.add(edge_key)
    
    lines.append('```')
    return '\n'.join(lines)

def generate_recommendations(graph, metadata):
    """Generate "what to learn next" recommendations based on completed modules."""
    # Find modules with no unmet dependencies (can be started immediately)
    ready = []
    for mod_id, deps in sorted(graph.items()):
        unmet = [d for d in deps if d in metadata and d not in ready]
        if not unmet:
            ready.append(mod_id)
    
    # Sort by complexity (simpler first)
    ready.sort(key=lambda x: metadata.get(x, {}).get('complexity_score', 0))
    
    recs = []
    for mod_id in ready:
        meta = metadata.get(mod_id, {})
        recs.append({
            'module': mod_id,
            'title': meta.get('title', mod_id),
            'level': meta.get('level', 'Unknown'),
            'complexity': round(meta.get('complexity_score', 0), 2),
            'word_count': meta.get('word_count', 0)
        })
    
    return recs

def main():
    parser = argparse.ArgumentParser(description='Generate module dependency graph')
    parser.add_argument('--modules-dir', default='modules', help='Root directory containing module folders')
    parser.add_argument('--output', required=True, help='Output .md file')
    parser.add_argument('--json-output', default='modules/modules.json', help='Output JSON metadata file')
    args = parser.parse_args()
    
    modules_dir = Path(args.modules_dir)
    if not modules_dir.exists():
        print(f"Error: Directory {modules_dir} does not exist")
        sys.exit(1)
    
    print(f"Building dependency graph from {modules_dir}")
    graph, metadata = build_dependency_graph(modules_dir)
    
    mermaid = generate_mermaid(graph, metadata)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(mermaid + '\n', encoding='utf-8')
    print(f"Generated dependency graph at {args.output}")
    
    # Write JSON metadata
    json_path = Path(args.json_output)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'modules': metadata,
            'graph': {k: sorted(v) for k, v in sorted(graph.items())},
            'recommendations': generate_recommendations(graph, metadata)
        }, f, indent=2, ensure_ascii=False)
    print(f"Generated modules metadata at {json_path}")
    
    print(f"\nModules: {len(metadata)}")
    print(f"Dependencies: {sum(len(v) for v in graph.values())}")
    for mod_id, meta in sorted(metadata.items()):
        print(f"  {mod_id}: {meta['level']} | {meta['word_count']} words | {meta['section_count']} sections | complexity: {meta['complexity_score']:.2f}")

if __name__ == '__main__':
    main()