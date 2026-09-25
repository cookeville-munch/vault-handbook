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

# Generate all files metadata
echo "[1/6] Generating all files metadata..."
python3 scripts/generate/generate_all_files_metadata.py

# Generate unified discovery outputs
echo "[2/6] Running unified discovery pipeline..."
python3 scripts/generate/generate_unified_discovery.py

# Generate dependency graph
echo "[3/6] Generating dependency graph..."
python3 scripts/generate/generate_dependency_graph.py \
    --modules-json modules/modules.json \
    --output docs/dependencies/generated_dependency_graph.md

# Generate changelog
echo "[4/6] Generating changelog..."
bash scripts/generate/generate_changelog.sh docs/_draft/CHANGELOG.md

# Generate automation tools
echo "[5/6] Generating automation tools..."
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