"""Unit tests for live-data harness tool seams.

These tests follow the harness TDD direction from the local PRD/test-spec:
the autonomous agent should expose explicit Municode/OpenData tool contracts
and return structured, replayable payloads.
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest

from plotlot.api.chat import (
    CHAT_TOOLS,
    _execute_municode_live_search,
    _execute_open_data_discovery,
    _execute_tool,
    _get_tools_for_turn,
    _sessions,
)
from plotlot.core.types import MunicodeConfig, TocNode
from plotlot.property.models import DatasetInfo


class _FakeScraper:
    def __init__(self, *args, **kwargs):
        pass

    async def walk_toc(self, client, config, root_node_id, max_depth=3):
        return [
            TocNode(
                node_id="n1",
                heading="RS-8 Residential District",
                has_children=False,
                depth=1,
                parent_heading="Zoning",
            ),
            TocNode(
                node_id="n2",
                heading="Setback Requirements",
                has_children=False,
                depth=1,
                parent_heading="RS-8 Residential District",
            ),
            TocNode(
                node_id="n3",
                heading="Noise Regulations",
                has_children=False,
                depth=1,
                parent_heading="General",
            ),
        ]

    async def get_section_content(self, client, config, node_id):
        if node_id == "n2":
            return "<p>Minimum front setback 25 feet. Rear setback 15 feet.</p>"
        return "<p>RS-8 permits single-family residential uses.</p>"


def test_chat_tools_expose_live_tool_metadata() -> None:
    functions = {
        tool["function"]["name"]: tool["function"]
        for tool in CHAT_TOOLS
        if tool.get("type") == "function"
    }

    municode = functions["search_municode_live"]
    assert "Municode" in municode["description"]
    assert municode["parameters"]["required"] == ["municipality", "query"]

    open_data = functions["discover_open_data_layers"]
    assert "ArcGIS/Open Data" in open_data["description"]
    assert open_data["parameters"]["required"] == ["county", "lat", "lng"]


def test_get_tools_for_turn_exposes_live_tools_in_core_runtime_set() -> None:
    _sessions._datasets.clear()

    tools = _get_tools_for_turn("session-1", "What zoning setbacks apply here?")
    names = [tool["function"]["name"] for tool in tools]

    assert "search_zoning_ordinance" in names
    assert "search_municode_live" in names
    assert "discover_open_data_layers" in names


@pytest.mark.asyncio
async def test_execute_open_data_discovery_returns_serialized_datasets() -> None:
    with patch(
        "plotlot.property.hub_discovery.discover_datasets",
        new=AsyncMock(
            return_value=(
                DatasetInfo(
                    dataset_id="p1",
                    name="Parcel Layer",
                    url="https://example.com/FeatureServer",
                    layer_id=0,
                    dataset_type="parcels",
                    county="Broward",
                    state="FL",
                    fields=["FOLIO", "OWNER"],
                ),
                DatasetInfo(
                    dataset_id="z1",
                    name="Zoning Layer",
                    url="https://example.com/Zoning/FeatureServer",
                    layer_id=9,
                    dataset_type="zoning",
                    county="Broward",
                    state="FL",
                    fields=["ZONE", "DESC"],
                ),
            )
        ),
    ):
        payload = json.loads(await _execute_open_data_discovery("Broward", "FL", 26.1, -80.1))

    assert payload["status"] == "success"
    assert payload["county"] == "Broward"
    assert payload["parcels_dataset"]["dataset_type"] == "parcels"
    assert payload["zoning_dataset"]["fields_preview"] == ["ZONE", "DESC"]


@pytest.mark.asyncio
async def test_execute_municode_live_search_returns_matching_sections() -> None:
    config = MunicodeConfig(
        municipality="Fort Lauderdale",
        county="broward",
        client_id=1,
        product_id=2,
        job_id=3,
        zoning_node_id="root",
    )

    with patch(
        "plotlot.ingestion.discovery.get_municode_configs",
        new=AsyncMock(return_value={"fort_lauderdale": config}),
    ), patch("plotlot.ingestion.scraper.MunicodeScraper", _FakeScraper):
        payload = json.loads(await _execute_municode_live_search("Fort Lauderdale", "RS-8 setbacks"))

    assert payload["status"] == "success"
    assert payload["source_type"] == "municode_live"
    assert any(row["heading"] == "Setback Requirements" for row in payload["results"])
    assert any("25 feet" in row["snippet"] for row in payload["results"])


@pytest.mark.asyncio
async def test_execute_tool_routes_new_live_tools() -> None:
    with patch(
        "plotlot.api.chat._execute_open_data_discovery",
        new=AsyncMock(return_value=json.dumps({"status": "success", "kind": "open_data"})),
    ), patch(
        "plotlot.api.chat._execute_municode_live_search",
        new=AsyncMock(return_value=json.dumps({"status": "success", "kind": "municode"})),
    ):
        open_data_payload = json.loads(
            await _execute_tool(
                "discover_open_data_layers",
                {"county": "Broward", "state": "FL", "lat": 26.1, "lng": -80.1},
                session_id="s1",
            )
        )
        municode_payload = json.loads(
            await _execute_tool(
                "search_municode_live",
                {"municipality": "Fort Lauderdale", "query": "RS-8 setbacks"},
                session_id="s1",
            )
        )

    assert open_data_payload["kind"] == "open_data"
    assert municode_payload["kind"] == "municode"
