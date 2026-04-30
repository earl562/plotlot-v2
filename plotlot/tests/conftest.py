"""Shared test fixtures."""

from pathlib import Path
import tempfile
from unittest.mock import patch

import mlflow
import pytest


_MLFLOW_TEST_DIR = Path(tempfile.gettempdir()) / "plotlot-mlflow-tests"
_MLFLOW_TEST_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(autouse=True)
def _disable_mlflow_tracing():
    """Disable MLflow tracing during tests — no side effects, no mlruns/ writes."""
    previous_tracking_uri = mlflow.get_tracking_uri()
    mlflow.set_tracking_uri(_MLFLOW_TEST_DIR.as_uri())
    mlflow.tracing.disable()
    yield
    mlflow.tracing.enable()
    mlflow.set_tracking_uri(previous_tracking_uri)


@pytest.fixture(autouse=True)
def _clear_discovery_cache():
    """Clear discovery cache before each test and disable disk cache."""
    from plotlot.ingestion.discovery import clear_cache

    clear_cache()
    with (
        patch("plotlot.ingestion.discovery._read_disk_cache", return_value=None),
        patch("plotlot.ingestion.discovery._write_disk_cache"),
    ):
        yield
    clear_cache()
