#!/usr/bin/env python3

import os
import glob
import math

# Directory containing the handbook modules
modules_dir = "modules"

# Output file for CSV data
output_file = "handbook_metrics.csv"

# Helper function to estimate time based on word count
def estimate_time_minutes(word_count):
    return math.ceil(word_count / 250)

# Get all .md files from modules directory, excluding superpowers submodule
md_files = []
for root, dirs, files in os.walk(modules_dir):
    # Skip the superpowers directory entirely
    if 'superpowers' in root.split(os.sep):
        continue
    for file in files:
        if file.endswith('.md'):
            # Get the file path
            file_path = os.path.join(root, file)
            # Get the relative path
            rel_path = os.path.relpath(file_path, ".")
            # Get section name from file path
            section_name = os.path.basename(rel_path).replace('.md', '')
            # Get word count
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                word_count = len(content.split())
            
            # Estimate time
            est_time = estimate_time_minutes(word_count)
            
            md_files.append({
                'section': section_name,
                'file_path': rel_path,
                'word_count': word_count,
                'est_time': est_time
            })

# Sort by file path for consistency
md_files.sort(key=lambda x: x['file_path'])

# Write to CSV
with open(output_file, 'w', encoding='utf-8') as f:
    # Write CSV header
    f.write("Section,File Path,Word Count,Est. Time (min)\n")
    
    # Write each section
    for item in md_files:
        f.write(f"{item['section']},{item['file_path']},{item['word_count']},{item['est_time']}\n")

print(f"Data collected for {len(md_files)} handbook sections (excluding superpowers).")
print(f"Saved to {output_file}")