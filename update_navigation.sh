#!/bin/bash
# Navigation update script for kink handbook

MODULES_DIR="content/modules"
README_PATH="README.md"
TOC_PATH="new_toc.md"

# Function to generate module list for README
generate_readme_modules() {
    find "$MODULES_DIR" -type f -name "*.md" | grep -E '[0-9]{2}-advanced-' | sort | while read file; do
        # Extract module name from path
        module_name=$(basename "$(dirname "$file")")
        title=$(head -n 1 "$file" | sed 's/^# //')
        echo "- [$title]($file)"
    done
}

# Function to generate module list for TOC (directory-based)
generate_toc_modules() {
    find "$MODULES_DIR" -mindepth 1 -maxdepth 1 -type d | sort | while read dir; do
        # Extract module name from path
        module_name=$(basename "$dir")
        # Get the first .md file in the directory to get title
        first_md=$(find "$dir" -type f -name "*.md" | head -n 1)
        if [ -n "$first_md" ]; then
            title=$(head -n 1 "$first_md" | sed 's/^# //')
            # Handle numbered directories
            if [[ "$module_name" =~ ^[0-9]+-(.*) ]]; then
                num="${BASH_REMATCH[1]}"
                display_name="$num"
            else
                display_name="$module_name"
            fi
            echo "  - [$display_name]($dir/)"
        fi
    done
}

# Update README.md Advanced Topics section
echo "Updating README.md..."
sed -i '/### Advanced Topics/,/---/{
    /### Advanced Topics/!{
        /---/!d
    }
}' "$README_PATH"

# Insert new module list after ### Advanced Topics
sed -i "/### Advanced Topics/a\\
$(generate_readme_modules)\\
" "$README_PATH"

# Update new_toc.md Module Navigation section
echo "Updating new_toc.md..."
sed -i '/### Module Navigation/,/---/{
    /### Module Navigation/!{
        /---/!d
    }
}' "$TOC_PATH"

# Insert new module list after ### Module Navigation
sed -i "/### Module Navigation/a\\
$(generate_toc_modules)\\
" "$TOC_PATH"

echo "✅ Navigation updated successfully!"
echo "Changes made to:"
echo "  - $README_PATH"
echo "  - $TOC_PATH"
