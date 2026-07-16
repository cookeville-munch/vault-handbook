#!/usr/bin/env python3
"""
Generate a table-of-contents markdown file listing each module with:
- Module name
- Description (first non-empty line after heading in README or first .md file)
- Status (validated/pass if in validation_report.json else unknown)
- Path link
"""
import os, re, json, argparse
from pathlib import Path

def extract_description(md_path):
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        return None
    # Skip frontmatter if present
    in_frontmatter = False
    start = 0
    if lines and lines[0].strip() == '---':
        in_frontmatter = True
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == '---':
                start = i+1
                break
    # Find first non-empty line after a heading or just first non-empty line
    for line in lines[start:]:
        stripped = line.strip()
        if not stripped:
            continue
        # Remove markdown syntax for heading markers
        cleaned = re.sub(r'^#+\s*', '', stripped)
        # If it's a heading, we might want the next line as description
        # For simplicity, just return cleaned as description
        if len(cleaned) > 3:  # reasonable length
            return cleaned[:120]  # truncate
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--modules-dir', default='content/modules', help='Root directory containing module folders')
    parser.add_argument('--validation-report', default='content/modules/validation_report.json', help='Validation report JSON')
    parser.add_argument('--output', required=True, help='Output markdown file path')
    args = parser.parse_args()

    modules_dir = Path(args.modules_dir)
    validation_data = {}
    vpath = Path(args.validation_report)
    if vpath.exists():
        try:
            with open(vpath) as f:
                data = json.load(f)
                # validation_data structure may vary; we assume keys are module names with status
                if isinstance(data, dict):
                    for mod, info in data.items():
                        if isinstance(info, dict) and 'status' in info:
                            validation_data[mod] = info['status']
                        elif isinstance(info, str):
                            validation_data[mod] = info
                # If it's a list under summary, try to parse differently
        except Exception:
            pass

    rows = []
    for mod_dir in sorted(modules_dir.iterdir()):
        if not mod_dir.is_dir():
            continue
        # Only consider directories that look like module folders (e.g., 01-something)
        if not re.match(r'^\d{2}-', mod_dir.name):
            continue
        mod_name = mod_dir.name
        # Find a markdown file in the directory (prefer README.md)
        md_files = list(mod_dir.glob('*.md'))
        readme = next((f for f in md_files if f.name.lower() == 'readme.md'), None)
        target_md = readme or (md_files[0] if md_files else None)
        description = ''
        if target_md and target_md.exists():
            description = extract_description(target_md) or ''
        # Determine status
        status = 'Unknown'
        if validation_data:
            # Try exact match
            if mod_name in validation_data:
                status = validation_data[mod_name]
            else:
                # Try with hyphen replaced by space? Not needed
                pass
        else:
            status = 'Not checked'
        # Format status badge
        if status.lower().startswith('pass') or status.lower() == 'validated':
            badge = '[✅ Validated](<#>)'
        elif status.lower().startswith('fail'):
            badge = '[❌ Failed](<#>)'
        else:
            badge = '[⏳ Pending](<#>)'
        # Build row
        rows.append({
            'module': mod_name,
            'description': description or '(no description)',
            'status': badge,
            'path': f'[{mod_name}]({mod_dir.as_posix()}/)'
        })

    # Write markdown table
    out_lines = [
        '# Module Table of Contents',
        '',
        f'Generated on {__import__("datetime").datetime.now().isoformat(timespec="seconds")}',
        '',
        '| Module | Description | Status | Path |',
        '|--------|-------------|--------|------|',
    ]
    for r in rows:
        # Escape pipe characters in description
        desc = r['description'].replace('|', '\\|')
        out_lines.append(f"| {r['module']} | {desc} | {r['status']} | {r['path']} |")
    out_lines.append('')
    out_lines.append(f'Total modules: {len(rows)}')

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n'.join(out_lines), encoding='utf-8')
    print(f'Generated TOC at {output_path}')

if __name__ == '__main__':
    main()