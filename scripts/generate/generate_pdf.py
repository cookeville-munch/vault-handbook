#!/usr/bin/env python3
"""
Generate a printable PDF handbook from the handbook modules.
Uses fpdf2 to produce a clean, readable PDF from Markdown content.
"""
import json
import re
import sys
from pathlib import Path
from fpdf import FPDF


def strip_markdown(text):
    """Convert basic Markdown to plain text for PDF."""
    # Remove headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    # Remove italics
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove horizontal rules
    text = re.sub(r'^---', '', text, flags=re.MULTILINE)
    # Remove non-Latin-1 characters (em dashes, quotes, etc.)
    text = re.sub(r'[^\x00-\x7f]', ' ', text)
    return text


def load_modules():
    """Load all modules from modules directory."""
    modules_dir = Path('modules')
    all_modules = []

    for md_file in sorted(modules_dir.rglob('*.md')):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract title
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else md_file.stem

        # Extract level
        level_match = re.search(r'\*\*Level:\s*(Foundational|Intermediate|Advanced)\*\*', content)
        level = level_match.group(1) if level_match else 'Unknown'

        # Extract introduction
        intro = ""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'\*\*Level:', line):
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and not lines[j].startswith('#'):
                        intro = lines[j].strip()
                        break
                break

        all_modules.append({
            'title': title.replace('\u2014', ' ').replace('\u2013', '-').replace('\u2018', "'").replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"'),
            'level': level,
            'intro': intro,
            'content': strip_markdown(content),
            'path': str(md_file.relative_to(modules_dir))
        })

    return all_modules


def generate_pdf(modules, output_path):
    """Generate PDF from modules."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title page
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 15, 'Vault Handbook', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Total modules: {len(modules)}', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)

    # Table of Contents
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Table of Contents', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.set_font('Arial', '', 10)
    for i, mod in enumerate(modules, 1):
        level_str = f'[{mod["level"]}]'
        pdf.cell(0, 6, f'{i}. {mod["title"]} {level_str}', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Module content
    for i, mod in enumerate(modules):
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'{i+1}. {mod["title"]}', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, f'Level: {mod["level"]} | File: {mod["path"]}', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        # Content
        content_lines = mod['content'].split('\n')
        for line in content_lines:
            line = line.strip()
            if not line:
                continue
            if len(line) > 200:
                # Split long lines
                for j in range(0, len(line), 200):
                    chunk = line[j:j+200]
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(0, 5, chunk, new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.set_font('Arial', '', 9)
                pdf.cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pdf.output(output_path)
    print(f"Generated PDF at {output_path}")
    return str(output_path)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate PDF handbook')
    parser.add_argument('--output', default='docs/_draft/handbook.pdf', help='Output PDF path')
    args = parser.parse_args()

    print("Loading modules...")
    modules = load_modules()
    print(f"Loaded {len(modules)} modules")

    print("Generating PDF...")
    generate_pdf(modules, args.output)


if __name__ == '__main__':
    main()