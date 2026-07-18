#!/usr/bin/env bash
"""
Convert Mermaid diagram JS files to SVG using mermaid-cli.
Handles errors gracefully and logs conversion results.
"""

# Convert to strict mode
set -euo pipefail

# Function to convert a single JS file to SVG
convert_file() {
    local js_file="$1"
    local svg_file="${js_file%.js}.svg"
    
    if [[ ! -f "$js_file" ]]; then
        echo "ERROR: Input file does not exist: $js_file" >&2
        return 1
    fi
    
    echo "Converting $js_file to $svg_file..."
    
    # Run mermaid-cli conversion
    if command -v mmdc >/dev/null 2>&1; then
        mmdc -i "$js_file" -o "$svg_file" --format=svg --quiet
        echo "✓ Successfully converted $js_file to $svg_file"
        return 0
    else
        echo "ERROR: mermaid-cli not found. Install with: npm install @mermaid-js/mermaid-cli" >&2
        return 1
    fi
}

# Main execution
main() {
    echo "=== SVG Conversion Utility ==="
    echo "Current directory: $(pwd)"
    echo
    
    # Check for mermaid files
    local mermaid_files
    mermaid_files=$(find diagrams -name "*.js" -not -path "./node_modules/*" -not -path "./modules/superpowers/*" 2>/dev/null || true)
    
    if [[ -z "$mermaid_files" ]]; then
        echo "No Mermaid diagram files (.js) found in diagrams/ directory."
        echo "Place your Mermaid diagram files in diagrams/"
        exit 1
    fi
    
    echo "Found $(echo "$mermaid_files" | wc -l) Mermaid diagram files:"
    echo "$mermaid_files"
    echo
    
    # Counters
    local success_count=0
    local total_count=$(echo "$mermaid_files" | wc -l)
    
    # Process each file
    while IFS= read -r file; do
        if convert_file "$file"; then
            ((success_count++))
        else
            echo "✗ Failed to convert $file"
        fi
    done <<< "$mermaid_files"
    
    echo
    echo "=== Summary ==="
    echo "Successful conversions: $success_count / $total_count"
    
    if [[ $success_count -eq $total_count ]]; then
        echo "✓ All diagrams converted successfully"
        exit 0
    else
        echo "✗ Some conversions failed"
        exit 1
    fi
}

# Execute main function with all arguments
main "$@"