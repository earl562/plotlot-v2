"""Loopback-only structured-evidence workbench; no credentials or external calls.

Run from the canonical application workspace:
    PYTHONPATH=src python scripts/readiness_demo.py --port 8765
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import uvicorn  # noqa: E402
from fastapi import FastAPI  # noqa: E402

from plotlot.api.readiness import router  # noqa: E402


def create_app() -> FastAPI:
    app = FastAPI(title="PlotLot local readiness workbench", version="1.0.0")
    app.include_router(router, prefix="/api/v1")
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("Choose a port between 1024 and 65535")
    print(f"Local workbench: http://127.0.0.1:{args.port}/api/v1/readiness/workbench", flush=True)
    print("Saving requires the authenticated main application. No local auth bypass is provided.", flush=True)
    uvicorn.run(create_app(), host="127.0.0.1", port=args.port)
