#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PLOTLOT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

if [[ ! -x "${PLOTLOT_ROOT}/.venv/bin/python" ]]; then
  echo "Missing ${PLOTLOT_ROOT}/.venv/bin/python. Run \`make install\` (or \`uv sync --extra dev\`) first." >&2
  exit 1
fi

# Opt-in to loading the Codex OAuth token from ~/.codex/auth.json.
export PLOTLOT_USE_CODEX_OAUTH=1

# Local dev defaults: Codex OAuth can be rate-limited for larger models.
# Keep this overrideable by exporting OPENAI_MODEL / OPENAI_REASONING_EFFORT.
export OPENAI_MODEL="${OPENAI_MODEL:-gpt-4.1-mini}"
export OPENAI_REASONING_EFFORT="${OPENAI_REASONING_EFFORT:-low}"

if [[ ! -f "${PLOTLOT_CODEX_AUTH_FILE:-$HOME/.codex/auth.json}" ]]; then
  echo "Codex OAuth token file not found. Run ./scripts/login_with_codex_oauth.sh first." >&2
  exit 1
fi

cd "${PLOTLOT_ROOT}"
exec "${PLOTLOT_ROOT}/.venv/bin/python" -m uvicorn plotlot.api.main:app --host 127.0.0.1 --port 8000
