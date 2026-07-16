#!/usr/bin/env python3
"""
Generate a module index markdown file from validation data.
Reads validation_report.json and module READMEs to create a structured index.
"""
import json
import os
import argparse
from pathlib import Path

def parse_frontmatter(readme_path):
    """Extract frontmatter from a markdown file."""
    if not readme_path.exists():
        return {}
    
    content = readme_path.read_text()
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            import yaml
            try:
                return yaml.safe_load(parts[1])
            except:
                return {}
    return {}

def get_module_status(module_dir, validation_data):
    """Determine module validation status from validation report."""
    module_name = module_dir.name
    if module_name in validation_data.get('detailed_results', {}):
        result = validation_data['detailed_results'][module_name]
        if isinstance(result, dict) and 'status' in result:
            return '✅ Validated' if result['status'] == 'OK' else '❌ Failed'
    return '⏳ Pending'

def main():
    parser = argparse.ArgumentParser(description='Generate module index markdown')
    parser.add_argument('--output', required=True, help='Output markdown file path')
    parser.add_argument('--modules-dir', default='content/modules', help='Modules directory')
    parser.add_argument('--validation-report', default='content/modules/validation_report.json')
    parser.add_argument('--badge-template', default='[![{status}](https://img.shields.io/badge/{name}-{status}-brightgreen)]')
    parser.add_argument('--sort-by', default='validation_status', choices=['name', 'validation_status', 'files'])
    args = parser.parse_args()

    # Load validation data
    validation_data = {}
    if os.path.exists(args.validation_report):
        with open(args.validation_report) as f:
            validation_data = json.load(f)

    modules_dir = Path(args.modules_dir)
    modules = []

    for module_path in sorted(modules_dir.iterdir()):
        if not module_path.is_dir() or not module_path.name[0].isdigit():
            continue
        
        # Count markdown files
        md_files = list(module_path.rglob('*.md'))
        md_count = len([f for f in md_files if not f.name.startswith('.')])
        
        # Get validation status
        status = get_module_status(module_path, validation_data)
        
        # Read README frontmatter
        readme = module_path / 'README.md'
        frontmatter = parse_frontmatter(readme)
        
        modules.append({
            'name': module_path.name,
            'title': frontmatter.get('title', module_path.name.replace('-', ' ').title()),
            'description': frontmatter.get('description', ''),
            'files': md_count,
            'status': status,
            'path': f'content/modules/{module_path.name}/'
        })

    # Sort modules
    if args.sort_by == 'validation_status':
        status_order = {'✅ Validated': 0, '⏳ Pending': 1, '❌ Failed': 2}
        modules.sort(key=lambda m: status_order.get(m['status'], 3))
    elif args.sort_by == 'files':
        modules.sort(key=lambda m: -m['files'])
    else:
        modules.sort(key=lambda m: m['name'])

    # Generate markdown
    lines = [
        '# Module Index & Navigation Map',
        '',
        f'*Auto-generated on {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")}*',
        '',
        '| Module | Status | Files | Description |',
        '|--------|--------|-------|-------------|'
    ]

    for m in modules:
        badge = args.badge_template.format(
            name=m['name'],
            status=m['status'].split()[1] if ' ' in m['status'] else m['status']
        ).replace(' ', '%20')
        desc = m['description'][:80] + '...' if len(m['description']) > 80 else m['description']
        lines.append(f"| [{m['title']}]({m['path']}) | {m['status']} | {m['files']} | {desc} |")

    # Summary
    validated = sum(1 for m in modules if m['status'].startswith('✅'))
    total = len(modules)
    total_files = sum(m['files'] for m in modules)
    
    lines.extend([
        '',
        f'**Total: {validated}/{total} modules validated | {total_files} markdown files**',
        '',
        '---',
        '',
        '## Quick Navigation',
        ''
    ])

    for m in modules:
        lines.append(f"- [{m['title']}]({m['path']}) — {m['status']}")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text('\n'.join(lines))
    print(f"Generated module index: {args.output}")

if __name__ == '__main__':
    main()