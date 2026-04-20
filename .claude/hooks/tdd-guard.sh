#!/usr/bin/env bash
# Post-edit hook: warn when a source file is modified without a corresponding test file
# Non-blocking — warns but does not block the edit

set -euo pipefail

FILE=$(cat | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))")

# Only process Python source files (not test files)
if [[ "$FILE" != *.py ]]; then
    exit 0
fi
if [[ "$FILE" == *test_* || "$FILE" == *tests/* || "$FILE" == *conftest* ]]; then
    exit 0
fi
if [[ "$FILE" != */plotlot/src/* && "$FILE" != */plotlot/src/plotlot/* ]]; then
    exit 0
fi

# Extract module name from file path
BASENAME=$(basename "$FILE" .py)

# Check if a corresponding test file exists
TEST_DIR="/Users/earlperry/Desktop/Projects/EP/plotlot/tests/unit"
if [[ ! -f "$TEST_DIR/test_${BASENAME}.py" ]]; then
    echo "⚠ TDD: No test file found at tests/unit/test_${BASENAME}.py — consider writing tests for this change"
fi

exit 0
