#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_BASE="${NEXT_PUBLIC_API_URL:-http://127.0.0.1:8000}"
FRONTEND_PORT="${PLAYWRIGHT_PORT:-3003}"
BACKEND_PID=""

log() {
  printf '\n\033[1;36m==> %s\033[0m\n' "$*"
}

run() {
  printf '\033[1;34m$ %s\033[0m\n' "$*"
  "$@"
}

cleanup() {
  if [[ -n "$BACKEND_PID" ]]; then
    kill "$BACKEND_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

clean_playwright_artifacts() {
  rm -rf frontend/test-results frontend/playwright-report
}

wait_for_backend() {
  local attempts=60
  for _ in $(seq 1 "$attempts"); do
    if curl -fsS "$API_BASE/health" >/tmp/plotlot-live-agent-health.json 2>/dev/null; then
      return 0
    fi
    sleep 1
  done
  return 1
}

assert_agent_ready() {
  python3 - "$API_BASE" <<'PY'
from __future__ import annotations

import json
import sys
import urllib.request

api_base = sys.argv[1].rstrip("/")
with urllib.request.urlopen(f"{api_base}/health", timeout=5) as response:
    body = json.load(response)

details = body.get("capability_details", {}).get("agent_chat_ready", {})
capabilities = body.get("capabilities", {})
ready = details.get("ready")
if ready is None:
    ready = capabilities.get("agent_chat_ready", False)

if not ready:
    reason = details.get("reason", "agent_chat_ready=false")
    raise SystemExit(f"Backend is reachable, but live agent chat is not ready: {reason}")

print("Backend live agent readiness: READY")
PY
}

cd "$ROOT_DIR"

clean_playwright_artifacts

log "Credential/auth readiness snapshot"
run python3 scripts/check_auth_readiness.py

if curl -fsS "$API_BASE/health" >/tmp/plotlot-live-agent-health.json 2>/dev/null; then
  log "Using existing backend at $API_BASE"
else
  log "Starting backend at $API_BASE"
  mkdir -p .omx/logs
  MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI:-file:///tmp/plotlot-mlruns}" \
    uv run uvicorn plotlot.api.main:app --host 127.0.0.1 --port 8000 \
    >.omx/logs/live-agent-e2e-backend.log 2>&1 &
  BACKEND_PID="$!"
  wait_for_backend || {
    cat .omx/logs/live-agent-e2e-backend.log >&2 || true
    printf 'Backend did not become reachable at %s\n' "$API_BASE" >&2
    exit 1
  }
fi

log "Checking backend agent readiness"
assert_agent_ready

log "Running live served frontend agent E2E"
(
  cd frontend
  PLOTLOT_LIVE_AGENT_E2E=1 \
    NEXT_PUBLIC_API_URL="$API_BASE" \
    PLAYWRIGHT_PORT="$FRONTEND_PORT" \
    npx playwright test tests/agent-live.e2e.spec.ts --project=chromium
)

clean_playwright_artifacts
