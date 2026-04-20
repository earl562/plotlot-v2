#!/usr/bin/env bash
# Post-edit hook: run relevant unit tests after modifying a Python source file
# Non-blocking — runs tests and reports results

set -euo pipefail

FILE=$(cat | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))")

# Only process Python files within plotlot
if [[ "$FILE" != *.py ]]; then
    exit 0
fi
if [[ "$FILE" != */plotlot/* ]]; then
    exit 0
fi

# Extract module name
BASENAME=$(basename "$FILE" .py)

# If editing a test file, run that test file directly
if [[ "$BASENAME" == test_* ]]; then
    cd /Users/earlperry/Desktop/Projects/EP/plotlot
    uv run pytest "tests/unit/${BASENAME}.py" -x -q 2>&1 | tail -5
    exit 0
fi

# If editing a source file, look for corresponding test
TEST_FILE="/Users/earlperry/Desktop/Projects/EP/plotlot/tests/unit/test_${BASENAME}.py"
if [[ -f "$TEST_FILE" ]]; then
    cd /Users/earlperry/Desktop/Projects/EP/plotlot
    uv run pytest "tests/unit/test_${BASENAME}.py" -x -q 2>&1 | tail -5
fi

exit 0
