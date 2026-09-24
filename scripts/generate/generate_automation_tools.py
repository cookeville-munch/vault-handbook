#!/usr/bin/env python3
"""
Generate comprehensive automation tools for the handbook.
Produces: link health monitoring, search index, complexity trends,
study paths, completion tracking, dependency gaps, reference validation,
study schedules, and term frequency dashboard.
"""
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def analyze_link_health(modules_dir):
    """Detect broken module references across all markdown files."""
    issues = []
    all_refs = defaultdict(list)
    all_modules = set()

    # Find all module directories
    for mod_dir in Path(modules_dir).iterdir():
        if mod_dir.is_dir() and re.match(r'^\d{2}-', mod_dir.name):
            all_modules.add(mod_dir.name)

    # Scan for references
    for md_file in Path(modules_dir).rglob('*.md'):
        refs = re.findall(r'\[([a-f0-9a-f-]{36})\]', md_file.read_text())
        for ref in refs:
            all_refs[ref].append(str(md_file))

        md_refs = re.findall(r'\[(\d{2}-[^\]\s]*)\]', md_file.read_text())
        for ref in md_refs:
            all_refs[ref].append(str(md_file))

    # Check for broken references
    for ref, files in sorted(all_refs.items()):
        if ref.startswith('01') and '-' in ref.split('[')[0]:
            continue
        if ref not in all_modules and not re.match(r'^[a-f0-9a-f-]{36}$', ref):
            issues.append({
                'type': 'broken_module_ref',
                'reference': ref,
                'files': files
            })

    return {'issues': issues, 'total_references': sum(len(v) for v in all_refs.values()), 'total_modules': len(all_modules)}


def generate_search_index(modules_dir, output_path):
    """Build an inverted index of glossary terms across all modules."""
    index = defaultdict(list)
    modules_info = {}

    for mod_dir in sorted(Path(modules_dir).iterdir()):
        if not mod_dir.is_dir():
            continue
        if not re.match(r'^\d{2}-', mod_dir.name):
            continue

        md_files = list(mod_dir.glob('*.md'))
        if not md_files:
            continue

        content = md_files[0].read_text()
        level_match = re.search(r'\*\*Level:\s*(Foundational|Intermediate|Advanced)\*\*', content)
        level = level_match.group(1) if level_match else 'Unknown'

        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else mod_dir.name

        modules_info[mod_dir.name] = {'title': title, 'level': level, 'path': str(mod_dir.relative_to(modules_dir))}

        glossary_matches = re.findall(r'\*\*([^\*\*]+)\*\*:\s*([^\n]+)', content)
        for term, _ in glossary_matches:
            index[term.lower()].append(mod_dir.name)

    output = {
        'generated': datetime.now().isoformat(),
        'total_terms': len(index),
        'total_modules': len(modules_info),
        'terms': {k: {'modules': v, 'count': len(v)} for k, v in sorted(index.items())},
        'modules': modules_info
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(output, indent=2), encoding='utf-8')
    return str(output_path)


def generate_complexity_trends(modules_dir, output_path):
    """Analyze complexity trends by module and section count."""
    trends = []

    for mod_dir in sorted(Path(modules_dir).iterdir()):
        if not mod_dir.is_dir():
            continue
        if not re.match(r'^\d{2}-', mod_dir.name):
            continue

        md_files = list(mod_dir.glob('*.md'))
        if not md_files:
            continue

        content = md_files[0].read_text()
        word_count = len(content.split())
        sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        complexity = round(word_count * len(sections) / 1000, 2)

        trends.append({
            'module': mod_dir.name,
            'word_count': word_count,
            'section_count': len(sections),
            'sections': [s.strip() for s in sections],
            'complexity_score': complexity,
            'complexity_tier': 'simple' if complexity < 50 else ('medium' if complexity < 200 else 'complex')
        })

    # Sort by complexity
    trends.sort(key=lambda x: x['complexity_score'])

    output = {
        'generated': datetime.now().isoformat(),
        'total_modules': len(trends),
        'trends': trends,
        'summary': {
            'avg_complexity': round(sum(t['complexity_score'] for t in trends) / len(trends), 2) if trends else 0,
            'max_complexity': max(t['complexity_score'] for t in trends) if trends else 0,
            'min_complexity': min(t['complexity_score'] for t in trends) if trends else 0
        }
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(output, indent=2), encoding='utf-8')
    return str(output_path)


def generate_study_path(start_module, completed, modules_info, output_path):
    """Generate a printable study path based on completion status."""
    plan = {
        'start_module': start_module,
        'completed': list(completed),
        'generated': datetime.now().isoformat(),
        'path': [],
        'estimated_hours': 0
    }

    # Build dependency graph
    ready = set(completed)
    remaining = set(modules_info.keys())

    for mod in list(remaining):
        refs = modules_info[mod].get('module_references', [])
        if all(r in ready or r not in modules_info for r in refs):
            plan['path'].append(mod)

    # Sort by complexity
    plan['path'].sort(key=lambda m: modules_info[m]['complexity_score'])

    # Estimate hours
    plan['estimated_hours'] = round(sum(modules_info[m]['complexity_score'] * 0.5 for m in plan['path']), 1)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(plan, indent=2), encoding='utf-8')
    return str(output_path)


def generate_completion_notifier(completed, modules_info, output_path):
    """List modules unlocked by current completion status."""
    ready = set(completed)
    unlocked = []

    for mod_name, info in modules_info.items():
        if mod_name in completed:
            continue
        refs = info.get('module_references', [])
        if all(r in ready or r not in modules_info for r in refs):
            unlocked.append({
                'module': mod_name,
                'title': info.get('title', mod_name),
                'level': info.get('level', 'Unknown'),
                'complexity': info.get('complexity_score', 0),
                'prerequisites_met': len([r for r in refs if r in ready]) / max(len(refs), 1)
            })

    unlocked.sort(key=lambda x: x['complexity'])

    output = {
        'completed': list(completed),
        'unlocked': unlocked,
        'total_unlocked': len(unlocked),
        'generated': datetime.now().isoformat()
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(output, indent=2), encoding='utf-8')
    return str(output_path)


def generate_dependency_gaps(modules_dir, output_path):
    """Analyze which modules have unmet prerequisites."""
    gaps = []
    all_modules = set()

    for mod_dir in sorted(Path(modules_dir).iterdir()):
        if not mod_dir.is_dir():
            continue
        if not re.match(r'^\d{2}-', mod_dir.name):
            continue
        all_modules.add(mod_dir.name)

    for mod_name in sorted(all_modules):
        mods = {mod_name: {'references': []}}

        for md_file in (Path(modules_dir) / mod_name).glob('*.md'):
            refs = re.findall(r'\[(\d{2}-[^\]\s]*)\]', md_file.read_text())
            mods[mod_name]['references'].extend(refs)

        refs = mods[mod_name]['references']
        missing = [r for r in refs if r in all_modules and r != mod_name]
        missing = [r for r in missing if not (Path(modules_dir) / r).exists()]

        if missing:
            gaps.append({
                'module': mod_name,
                'missing_prerequisites': missing
            })

    output = {
        'generated': datetime.now().isoformat(),
        'total_modules': len(all_modules),
        'modules_with_gaps': len(gaps),
        'gaps': gaps
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(output, indent=2), encoding='utf-8')
    return str(output_path)


def generate_reference_validation(modules_dir, output_path):
    """Validate that all module references point to existing directories or files."""
    errors = []
    warnings = []

    all_modules = set()
    all_files = set()

    for mod_dir in Path(modules_dir).iterdir():
        if mod_dir.is_dir() and re.match(r'^\d{2}-', mod_dir.name):
            all_modules.add(mod_dir.name)
            for f in mod_dir.glob('*.md'):
                rel_path = f.relative_to(Path(modules_dir)).as_posix()
                all_files.add(rel_path)

    for md_file in Path(modules_dir).rglob('*.md'):
        content = md_file.read_text()
        for ref in re.findall(r'\[(\d{2}-[^\]\s]*)\]', content):
            # Module-level reference (matches directory)
            if ref in all_modules:
                continue

            # File-level reference (matches file within a module directory)
            file_md = f'{ref}.md'
            found = any(f'{mod_id}/{file_md}' in all_files for mod_id in all_modules)

            # Cross-module file reference (matches module/file)
            if not found and '/' in ref:
                found = f'{ref}.md' in all_files

            if not found:
                errors.append({
                    'type': 'invalid_module_reference',
                    'reference': ref,
                    'file': str(md_file),
                    'message': f'Reference to non-existent module or file: {ref}'
                })

    output = {
        'generated': datetime.now().isoformat(),
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'total_references_checked': sum(len(re.findall(r'\[\d{2}-[^\]]*\]', f.read_text())) for f in Path(modules_dir).rglob('*.md'))
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(output, indent=2), encoding='utf-8')
    return str(output_path)


def generate_study_schedule(duration_weeks=4, modules_dir='modules', output_path='docs/_draft/study_schedule.json'):
    """Generate a study schedule based on module complexity."""
    modules_info = {}

    for mod_dir in sorted(Path(modules_dir).iterdir()):
        if not mod_dir.is_dir() or not re.match(r'^\d{2}-', mod_dir.name):
            continue

        md_files = list(mod_dir.glob('*.md'))
        if not md_files:
            continue

        content = md_files[0].read_text()
        word_count = len(content.split())
        sections = len(re.findall(r'^##\s+', content, re.MULTILINE))
        complexity = word_count * sections / 1000

        modules_info[mod_dir.name] = {
            'complexity': complexity,
            'title': re.search(r'^#\s+(.+)$', content, re.MULTILINE).group(1).strip() if re.search(r'^#\s+(.+)$', content, re.MULTILINE) else mod_dir.name,
            'level': re.search(r'\*\*Level:\s*(Foundational|Intermediate|Advanced)\*\*', content).group(1) if re.search(r'\*\*Level:\s*(Foundational|Intermediate|Advanced)\*\*', content) else 'Unknown'
        }

    sorted_modules = sorted(modules_info.keys(), key=lambda m: modules_info[m]['complexity'])

    weekly_chunks = [sorted_modules[i:i+3] for i in range(0, len(sorted_modules), 3)]
    schedule = []

    for week in range(min(duration_weeks, len(weekly_chunks))):
        schedule.append({
            'week': week + 1,
            'date_range': f"Week {week+1}",
            'modules': [{
                'id': m,
                'title': modules_info[m]['title'],
                'level': modules_info[m]['level'],
                'estimated_hours': round(modules_info[m]['complexity'] * 0.5, 1)
            } for m in weekly_chunks[week]],
            'total_estimated_hours': round(sum(modules_info[m]['complexity'] * 0.5 for m in weekly_chunks[week]), 1)
        })

    output = {
        'generated': datetime.now().isoformat(),
        'total_weeks': len(schedule),
        'total_modules': len(sorted_modules),
        'schedule': schedule
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(output, indent=2), encoding='utf-8')
    return str(output_path)


def generate_term_frequency(modules_dir, output_path):
    """Generate cross-module term frequency dashboard."""
    term_modules = defaultdict(set)
    all_terms = defaultdict(int)

    for mod_dir in sorted(Path(modules_dir).iterdir()):
        if not mod_dir.is_dir():
            continue

        md_files = list(mod_dir.glob('*.md'))
        for md_file in md_files:
            content = md_file.read_text()
            glossary_matches = re.findall(r'\*\*([^\*\*]+)\*\*:\s*([^\n]+)', content)

            for term, definition in glossary_matches:
                term_lower = term.strip().lower()
                mod_name = mod_dir.name
                term_modules[term_lower].add(mod_name)
                all_terms[term_lower] += 1

    frequency_data = []
    for term, count in sorted(all_terms.items()):
        modules = list(term_modules[term])
        frequency_data.append({
            'term': term,
            'count': count,
            'modules': modules,
            'module_count': len(modules),
            'coverage': len(modules) / 151 if term_modules else 0
        })

    frequency_data.sort(key=lambda x: x['coverage'], reverse=True)
    low_coverage = [f for f in frequency_data if f['coverage'] < 0.03]
    high_usage = [f for f in frequency_data if f['coverage'] > 0.05]

    output = {
        'generated': datetime.now().isoformat(),
        'total_unique_terms': len(all_terms),
        'term_frequency_distribution': frequency_data,
        'coverage_issues': low_coverage,
        'high_usage_terms': high_usage,
        'summary': {
            'avg_appearances_per_term': round(sum(all_terms.values()) / len(all_terms), 2) if all_terms else 0,
            'terms_in_single_module': len([t for t, c in all_terms.items() if c == 1]),
            'most_common_term': max(all_terms.items(), key=lambda x: x[1])[0] if all_terms else None
        }
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(output, indent=2), encoding='utf-8')
    return str(output_path)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate automation tools for the handbook')
    parser.add_argument('--modules-dir', default='modules', help='Root modules directory')
    parser.add_argument('--output-dir', default='docs/_draft', help='Output directory for generated files')
    parser.add_argument('--completed', nargs='*', default=[], help='List of completed module IDs')
    parser.add_argument('--start-module', default='01-orientation-consent', help='Starting module for study path')
    parser.add_argument('--weeks', type=int, default=4, help='Study schedule duration in weeks')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load modules.json if exists
    modules_json_path = Path(args.modules_dir) / 'modules.json'
    modules_info = {}
    progress = {}

    if modules_json_path.exists():
        with open(modules_json_path) as f:
            data = json.load(f)
            modules_info = data.get('modules', {})
            progress = data.get('progress', {})

    # Generate link health report
    health = analyze_link_health(args.modules_dir)
    print(f"Link health: {len(health['issues'])} issues, {health['total_references']} references in {health['total_modules']} modules")

    # Generate search index
    print(f"Generating search index...")
    generate_search_index(args.modules_dir, output_dir / 'search_index.json')

    # Generate complexity trends
    print(f"Generating complexity trends...")
    generate_complexity_trends(args.modules_dir, output_dir / 'complexity_trends.json')

    # Generate study path
    print(f"Generating study path...")
    generate_study_path(args.start_module, set(progress.get('completed_modules', [])), modules_info, output_dir / 'study_path.json')

    # Generate completion notifier
    print(f"Generating completion notifier...")
    generate_completion_notifier(set(progress.get('completed_modules', [])), modules_info, output_dir / 'completion_notifier.json')

    # Generate dependency gaps
    print(f"Generating dependency gap analysis...")
    generate_dependency_gaps(args.modules_dir, output_dir / 'dependency_gaps.json')

    # Generate reference validation
    print(f"Validating references...")
    generate_reference_validation(args.modules_dir, output_dir / 'reference_validation.json')

    # Generate study schedule
    print(f"Generating study schedule...")
    generate_study_schedule(args.weeks, args.modules_dir, output_dir / 'study_schedule.json')

    # Generate term frequency dashboard
    print(f"Generating term frequency dashboard...")
    generate_term_frequency(args.modules_dir, output_dir / 'term_frequency.json')

    print(f"All automation tools generated in {output_dir}")


if __name__ == '__main__':
    main()