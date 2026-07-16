#!/usr/bin/env bash
# generate_changelog.sh
# Generates a changelog from git tags and commits since a given date.
# Requires: git (and optionally git-changelog if installed)

set -e

OUTPUT="${1:-docs/_draft/CHANGELOG.md}"
SINCE="${2:-2026-01-01}"
PATTERN="${3:-content/modules/*}"
STYLE="${4:-* Changes: %s}"

mkdir -p "$(dirname "$OUTPUT")"

echo "# Changelog" > "$OUTPUT"
echo "" >> "$OUTPUT"
echo "Generated on $(date -u '+%Y-%m-%d %H:%M:%S' UTC) from commits since $SINCE" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Use git log to list commits touching the pattern
git log --since="$SINCE" --pretty=format:"%h %ad %s" --date=short -- "$PATTERN" |
while read -r hash date msg; do
    echo "$STYLE" | sed "s|%s|$msg|; s|%h|$hash|; s|%ad|$date|" >> "$OUTPUT"
done

echo "" >> "$OUTPUT"
echo "---" >> "$OUTPUT"
echo "*End of auto-generated changelog.*" >> "$OUTPUT"

echo "Changelog written to $OUTPUT"