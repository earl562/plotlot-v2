#!/usr/bin/env bash
set -euo pipefail

# pi-ralph.sh
#
# Start pi in RPC mode and launch the PlotLot /ralph loop.
#
# Usage:
#   scripts/pi-ralph.sh [--max N] [--session-dir DIR] [--session] [--] <goal...>
#   scripts/pi-ralph.sh "continue reviewing top-down arXiv queue"
#
# Notes:
# - Defaults to --no-session (ephemeral). Use --session to persist pi sessions.
# - Auto-approves extension confirm dialogs.

MAX_ITERATIONS=50
SESSION_DIR=""
NO_SESSION=1

usage() {
  cat <<EOF
Usage:
  $0 [--max N] [--session-dir DIR] [--session] [--] <goal...>

Examples:
  $0 --max 50 -- "Review next P0 arXiv stub and update dashboards"
  $0 "Review next P0 arXiv stub and update dashboards"

Options:
  --max N            Max iterations (default: 50)
  --session          Persist pi session (default: ephemeral --no-session)
  --session-dir DIR  Custom session dir (implies --session)
EOF
}

# Parse args
GOAL_WORDS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --max)
      MAX_ITERATIONS="${2:-$MAX_ITERATIONS}"
      shift 2
      ;;
    --max=*)
      MAX_ITERATIONS="${1#--max=}"
      shift 1
      ;;
    --session)
      NO_SESSION=0
      shift 1
      ;;
    --session-dir)
      SESSION_DIR="${2:-}"
      NO_SESSION=0
      shift 2
      ;;
    --session-dir=*)
      SESSION_DIR="${1#--session-dir=}"
      NO_SESSION=0
      shift 1
      ;;
    --)
      shift
      GOAL_WORDS+=("$@")
      break
      ;;
    *)
      GOAL_WORDS+=("$1")
      shift
      ;;
  esac
done

GOAL="${GOAL_WORDS[*]:-}"
if [[ -z "${GOAL// }" ]]; then
  usage
  exit 1
fi

if ! command -v pi >/dev/null 2>&1; then
  echo "ERR: pi not found in PATH" >&2
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERR: python3 not found in PATH" >&2
  exit 1
fi

export PI_RALPH_GOAL="$GOAL"
export PI_RALPH_MAX_ITERATIONS="$MAX_ITERATIONS"
export PI_RALPH_SESSION_DIR="$SESSION_DIR"
export PI_RALPH_NO_SESSION="$NO_SESSION"

python3 - <<'PY'
import json
import os
import re
import subprocess
import sys

goal = os.environ.get("PI_RALPH_GOAL", "").strip()
max_iter = int(os.environ.get("PI_RALPH_MAX_ITERATIONS", "50"))
session_dir = os.environ.get("PI_RALPH_SESSION_DIR", "").strip()
no_session = os.environ.get("PI_RALPH_NO_SESSION", "1") == "1"

cmd = ["pi", "--mode", "rpc"]
if no_session:
    cmd.append("--no-session")
if session_dir:
    cmd.extend(["--session-dir", session_dir])

proc = subprocess.Popen(
    cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1,
)
assert proc.stdin is not None
assert proc.stdout is not None


def send(obj: dict):
    proc.stdin.write(json.dumps(obj, ensure_ascii=False) + "\n")
    proc.stdin.flush()

# Start Ralph loop (skip confirmation; the extension still enforces tool safety via skill behavior).
send({"type": "prompt", "message": f"/ralph --yes --max {max_iter} {goal}"})

terminal_re = re.compile(r"RALPH_STATUS:\s*(COMPLETE|BLOCKED|MAXED)", re.IGNORECASE)

try:
    for raw in proc.stdout:
        raw = raw.strip("\r\n")
        if not raw:
            continue
        try:
            evt = json.loads(raw)
        except Exception:
            continue

        etype = evt.get("type")

        if etype == "extension_ui_request":
            method = evt.get("method")
            req_id = evt.get("id")

            # Surface notifications (and use them as a termination signal when Ralph stops via the extension).
            if method == "notify":
                msg = str(evt.get("message") or "")
                sys.stderr.write(f"[pi-ui] {msg}\n")
                sys.stderr.flush()
                if any(
                    s in msg.lower()
                    for s in [
                        "ralph complete",
                        "ralph blocked",
                        "ralph stopped",
                        "ralph hit max iterations",
                    ]
                ):
                    sys.stderr.write("[pi-ralph] ralph termination notify detected; exiting.\n")
                    sys.stderr.flush()
                    break

            if not req_id:
                continue

            # Dialog methods require responses; fire-and-forget UI methods do not.
            if method == "confirm":
                send({"type": "extension_ui_response", "id": req_id, "confirmed": True})
            elif method in {"select", "input", "editor"}:
                send({"type": "extension_ui_response", "id": req_id, "cancelled": True})
            else:
                pass
            continue

        if etype == "message_update":
            ame = evt.get("assistantMessageEvent") or {}
            if ame.get("type") == "text_delta":
                sys.stdout.write(ame.get("delta", ""))
                sys.stdout.flush()
            continue

        if etype == "message_end":
            msg = evt.get("message") or {}
            if msg.get("role") != "assistant":
                continue
            sys.stdout.write("\n")
            sys.stdout.flush()

            content = msg.get("content")
            text_parts = []
            if isinstance(content, str):
                text_parts.append(content)
            elif isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "text":
                        text_parts.append(str(c.get("text") or ""))
            full_text = "\n".join(text_parts)

            if terminal_re.search(full_text):
                sys.stderr.write("[pi-ralph] terminal status detected; exiting.\n")
                sys.stderr.flush()
                break
            continue

        if etype == "tool_execution_end":
            tool_name = evt.get("toolName") or "(tool)"
            result = evt.get("result") or {}
            out = []
            for c in (result.get("content") or []):
                if isinstance(c, dict) and c.get("type") == "text":
                    out.append(str(c.get("text") or ""))
            tool_text = "\n".join(out).strip()
            if tool_text:
                sys.stderr.write(f"--- tool: {tool_name} ---\n{tool_text}\n---\n")
                sys.stderr.flush()
            continue

finally:
    try:
        proc.stdin.close()
    except Exception:
        pass
    try:
        proc.terminate()
    except Exception:
        pass
    try:
        proc.wait(timeout=2)
    except Exception:
        pass
PY
