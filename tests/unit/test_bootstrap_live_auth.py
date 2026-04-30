from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "bootstrap_live_auth.py"


def run_script(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=True,
        env=merged_env,
        cwd=ROOT,
    )


def test_bootstrap_from_env_and_enable_codex_oauth(tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "GEOCODIO_API_KEY=\nPLOTLOT_USE_CODEX_OAUTH=0\n",
        encoding="utf-8",
    )

    result = run_script(
        "--env-file",
        str(env_file),
        "--from-env",
        "GEOCODIO_API_KEY",
        "--enable-codex-oauth",
        env={"GEOCODIO_API_KEY": "test-geocodio-token"},
    )

    updated = env_file.read_text(encoding="utf-8")
    assert "GEOCODIO_API_KEY=test-geocodio-token" in updated
    assert "PLOTLOT_USE_CODEX_OAUTH=1" in updated
    assert "PLOTLOT_CODEX_AUTH_FILE=~/.codex/auth.json" in updated
    assert "GEOCODIO_API_KEY" in result.stdout
    assert "test-geocodio-token" not in result.stdout


def test_bootstrap_dry_run_does_not_write(tmp_path: Path):
    env_file = tmp_path / ".env"
    before = "JINA_API_KEY=\n"
    env_file.write_text(before, encoding="utf-8")

    result = run_script(
        "--env-file",
        str(env_file),
        "--set",
        "JINA_API_KEY=should-not-write",
        "--dry-run",
    )

    after = env_file.read_text(encoding="utf-8")
    assert after == before
    assert "Dry run" in result.stdout
    assert "JINA_API_KEY" in result.stdout
