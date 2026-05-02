#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

SESSION_DIR="${SESSION_DIR:-$HOME/.pi-sessions/plotlot-obsidian-ralph}"
LOG_FILE="${LOG_FILE:-/tmp/plotlot_ralph_obsidian_loop.log}"
MAX_ITER_PER_RUN="${MAX_ITER_PER_RUN:-25}"
MAX_NO_PROGRESS="${MAX_NO_PROGRESS:-3}"
SLEEP_SECONDS="${SLEEP_SECONDS:-10}"

GOAL="${*:-Continue the Ralph loop until all paper-backed research in the Obsidian-driven backlog is analyzed. Prioritize unreviewed papers from the current repo queue, use full paper text not abstracts, keep updating knowledge-graph artifacts and Obsidian exports, save coherent changes, and only broaden beyond arXiv after the paper queue is exhausted.}"

mkdir -p "$(dirname "$SESSION_DIR")"
: > "$LOG_FILE"

log() {
  printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" | tee -a "$LOG_FILE"
}

get_counts_json() {
  node .pi/skills/autoresearch/scripts/list_unreviewed_notes.mjs 2>/dev/null | python3 -c 'import json,sys; print(json.dumps(json.load(sys.stdin)))'
}

get_stub_count() {
  get_counts_json | python3 -c 'import json,sys; print(json.load(sys.stdin)["stub"])'
}

get_reviewed_count() {
  get_counts_json | python3 -c 'import json,sys; print(json.load(sys.stdin)["reviewed"])'
}

save_progress_if_needed() {
  if [[ -z "$(git status --porcelain)" ]]; then
    log "No repo changes to save."
    return 1
  fi

  git add docs/research .pi scripts docs/harness plotlot/src plotlot/tests || true

  if git diff --cached --quiet; then
    log "Working tree changed, but no staged diff after scoped add."
    return 1
  fi

  local reviewed
  reviewed="$(get_reviewed_count || echo unknown)"
  local msg="chore(ralph): continue obsidian paper loop (reviewed ${reviewed})"
  git commit -m "$msg" >>"$LOG_FILE" 2>&1
  git push >>"$LOG_FILE" 2>&1
  log "Committed and pushed progress: $msg"
  return 0
}

if [[ "$(git branch --show-current)" != "pi-feature-branch" ]]; then
  log "Switching to pi-feature-branch"
  git switch pi-feature-branch >>"$LOG_FILE" 2>&1
fi

log "Starting continuous Ralph supervisor"
log "Repo: $ROOT_DIR"
log "Session dir: $SESSION_DIR"
log "Goal: $GOAL"

prev_stub="$(get_stub_count)"
no_progress=0
pass_num=0

while true; do
  pass_num=$((pass_num + 1))
  reviewed_before="$(get_reviewed_count || echo unknown)"
  stub_before="$prev_stub"
  log "Pass $pass_num starting (reviewed=$reviewed_before stub=$stub_before)"

  set +e
  ./scripts/pi-ralph.sh --session-dir "$SESSION_DIR" --max "$MAX_ITER_PER_RUN" -- "$GOAL" >>"$LOG_FILE" 2>&1
  ralph_exit=$?
  set -e
  log "Ralph pass $pass_num exited with code $ralph_exit"

  save_progress_if_needed || true

  reviewed_after="$(get_reviewed_count || echo unknown)"
  stub_after="$(get_stub_count || echo "$stub_before")"
  log "Pass $pass_num finished (reviewed=$reviewed_after stub=$stub_after)"

  if [[ "$stub_after" == "0" ]]; then
    log "Paper backlog exhausted for current arXiv note queue. Supervisor stopping cleanly."
    break
  fi

  if [[ "$stub_after" -lt "$stub_before" ]]; then
    no_progress=0
    prev_stub="$stub_after"
    log "Progress detected: stub count decreased from $stub_before to $stub_after"
  else
    no_progress=$((no_progress + 1))
    prev_stub="$stub_after"
    log "No stub-count progress on pass $pass_num (consecutive=$no_progress/$MAX_NO_PROGRESS)"
  fi

  if [[ $no_progress -ge $MAX_NO_PROGRESS ]]; then
    log "Stopping: hit no-progress guard. Manual steering likely needed."
    break
  fi

  sleep "$SLEEP_SECONDS"
done

log "Continuous Ralph supervisor exited."
