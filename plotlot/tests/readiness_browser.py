"""Run against the actual local API/workbench. Requires installed Playwright Chromium."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
from datetime import date

from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(os.environ.get("READINESS_BROWSER_OUTPUT", ROOT / ".readiness-browser"))
PORT = int(os.environ.get("READINESS_DEMO_PORT", "8765"))
URL = f"http://127.0.0.1:{PORT}/api/v1/readiness/workbench"


def sample(value=True):
    return {
        "site_id": "s1", "parcel_id": "p1", "scenario_id": "base",
        "intended_use": "Residential development",
        "requirements": [{"id": "access", "category": "access", "label": "Legal access",
                          "expected": True, "critical": True}],
        "evidence": [{"id": "e1", "requirement_id": "access", "site_id": "s1",
                      "parcel_id": "p1", "scenario_id": "base",
                      "intended_use": "Residential development", "value": value,
                      "source_kind": "professional_report", "source_title": "Synthetic survey",
                      "document_id": "demo-only", "locator": "Page 2", "excerpt": "Synthetic finding.",
                      "observed_on": date.today().isoformat(), "review_state": "source_checked",
                      "screening_only": False}],
    }


def apply_case(page, case):
    page.locator("#advanced").evaluate("node => node.open = true")
    page.locator("#case-json").fill(json.dumps(case))
    page.get_by_role("button", name="Apply JSON").click()
    page.get_by_role("button", name="Run review", exact=True).click()
    expect(page.get_by_role("button", name="Run review", exact=True)).to_be_enabled()


def main():
    assert (ROOT / "scripts/readiness_demo.py").exists(), "Demo runner has not been implemented"
    assert (ROOT / "src/plotlot/land_use/readiness/workbench.html").exists(), "Workbench missing"
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / "server.log").open("w") as log:
        process = subprocess.Popen([sys.executable, str(ROOT / "scripts/readiness_demo.py"),
                                    "--port", str(PORT)], stdout=log, stderr=log)
        try:
            for _ in range(100):
                if process.poll() is not None:
                    raise RuntimeError("Demo server exited; inspect server.log")
                try:
                    with urllib.request.urlopen(URL, timeout=1) as response:
                        if response.status == 200:
                            break
                except Exception:
                    time.sleep(0.1)
            else:
                raise RuntimeError("Demo server did not become ready")
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"],
                    executable_path=os.environ.get("READINESS_CHROMIUM_EXECUTABLE"),
                )
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(URL)
                page.locator("#site-id").fill("s1")
                page.locator("#parcel-id").fill("p1")
                page.locator("#intended-use").fill("Residential development")
                expect(page.locator("#requirements-count")).to_have_text("8 requirements")
                page.get_by_role("button", name="Run review", exact=True).click()
                expect(page.locator("#decision")).to_have_text("HOLD")
                checks = ["unknown evidence holds"]

                case = sample()
                case["evidence"].append({**case["evidence"][0], "id": "e2", "value": False,
                    "source_title": '<img src=x onerror="window.INJECTED=true">'})
                apply_case(page, case)
                expect(page.locator("#decision")).to_have_text("HOLD")
                expect(page.locator("#findings")).to_contain_text("Contradiction")
                assert page.evaluate("window.INJECTED") is None
                assert page.locator("#evidence-list img").count() == 0
                checks.extend(["contradictory records hold", "source text cannot execute HTML"])

                case["evidence"][1]["active"] = False
                apply_case(page, case)
                expect(page.locator("#decision")).to_have_text("READY FOR REVIEW")
                checks.append("explicitly inactive contradictory record no longer blocks")
                page.locator("#intended-use").fill("Data center")
                expect(page.locator("#stale-banner")).to_be_visible()
                expect(page.get_by_role("button", name="Export memo")).to_be_disabled()
                page.get_by_role("button", name="Run review", exact=True).click()
                expect(page.locator("#decision")).to_have_text("HOLD")
                checks.extend(["edited inputs invalidate visible memo", "changed use cannot reuse clearance"])

                apply_case(page, sample(False))
                expect(page.locator("#decision")).to_have_text("DO NOT PROCEED")
                checks.append("confirmed scenario conflict blocks proceeding")
                with page.expect_download() as download:
                    page.get_by_role("button", name="Export case").click()
                download.value.save_as(OUTPUT / "exported-case.json")
                exported = json.loads((OUTPUT / "exported-case.json").read_text())
                assert exported["parcel_id"] == "p1"
                checks.append("structured case export")

                page.locator("#workspace-id").fill("w1")
                page.get_by_role("button", name="Save revision").click()
                expect(page.locator("#notice")).to_contain_text("Authentication required")
                checks.append("unauthenticated persistence does not pretend to save")
                page.screenshot(path=str(OUTPUT / "workbench-desktop.png"), full_page=True)
                page.set_viewport_size({"width": 390, "height": 844})
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                page.screenshot(path=str(OUTPUT / "workbench-mobile.png"), full_page=True)
                checks.append("mobile layout fits viewport")
                assert not errors, errors
                checks.append("no browser JavaScript errors")
                browser.close()
                (OUTPUT / "results.json").write_text(json.dumps({"passed": len(checks), "checks": checks}, indent=2))
                print(json.dumps({"passed": len(checks), "checks": checks}, indent=2))
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    main()
