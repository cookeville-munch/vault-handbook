#!/usr/bin/env bash
# generate_all.sh
# Runs all generators to produce up-to-date handbook artifacts.
# Usage: ./scripts/generate/generate_all.sh [--clean]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

cd "$PROJECT_ROOT"

echo "=== Running handbook generators ==="
echo ""

# Create output directories
mkdir -p docs/index docs/glossary docs/dependencies docs/_draft modules

# Generate dependency graph
echo "[1/7] Generating dependency graph..."
python3 scripts/generate/generate_dependency_graph.py \
    --output docs/dependencies/generated_dependency_graph.md \
    --json-output modules/modules.json

# Generate module index (TOC, glossary, matrix, JSON)
echo "[2/7] Generating module index..."
python3 scripts/generate/generate_module_index.py

# Generate TOC via existing generator
echo "[3/7] Generating module table of contents..."
python3 scripts/generate/generate_module_toc.py --output docs/index/generated_module_toc.md

# Generate changelog
echo "[4/7] Generating changelog..."
bash scripts/generate/generate_changelog.sh docs/_draft/CHANGELOG.md

# Generate automation tools
echo "[5/7] Generating automation tools..."
python3 scripts/generate/generate_automation_tools.py

# Validate all modules
echo ""
echo "=== Validating module structure ==="
python3 scripts/validation/validate_structure.py modules

# Run link validation
echo ""
echo "=== Validating links ==="
python3 scripts/validation/validate_links.py 2>/dev/null || echo "Link validation script not found, skipping..."

echo ""
echo "=== All generators complete ==="
