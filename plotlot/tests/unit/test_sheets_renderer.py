"""Tests for the Google Sheets pro forma renderer.

Google Sheets API calls are mocked — we test data formatting and
the wrapper logic, not actual Google API connectivity.
"""

from unittest.mock import AsyncMock, patch

import pytest

from plotlot.clauses.renderers.sheets_renderer import (
    SheetsProFormaResult,
    _build_pro_forma_rows,
    render_google_sheets,
)
from plotlot.clauses.schema import (
    AssemblyConfig,
    DealContext,
    DealType,
    DocumentType,
)
from plotlot.retrieval.google_workspace import SpreadsheetResult


def _proforma_context() -> DealContext:
    return DealContext(
        property_address="7940 Plantation Blvd, Miramar, FL 33023",
        municipality="Miramar",
        county="Broward",
        state_code="FL",
        apn="5040-19-02-0010",
        lot_size_sqft=15000.0,
        zoning_district="RS-4",
        max_units=4,
        governing_constraint="density",
        median_price_per_acre=450000.0,
        estimated_land_value=155000.0,
        comp_count=8,
        gross_development_value=1600000.0,
        hard_costs=800000.0,
        soft_costs=120000.0,
        builder_margin=0.12,
        max_land_price=488000.0,
        cost_per_door=230000.0,
        adv_per_unit=400000.0,
        deal_type=DealType.land_deal,
        purchase_price=155000.0,
        earnest_money=5000.0,
    )


def _minimal_context() -> DealContext:
    return DealContext(
        property_address="123 Main St, Miami, FL",
        state_code="FL",
    )


# ---------------------------------------------------------------------------
# _build_pro_forma_rows — pure function, no mocking needed
# ---------------------------------------------------------------------------


class TestBuildProFormaRows:
    def test_returns_headers_and_rows(self):
        headers, rows = _build_pro_forma_rows(_proforma_context())
        assert headers == ["Category", "Metric", "Value"]
        assert len(rows) > 10

    def test_includes_property_data(self):
        _, rows = _build_pro_forma_rows(_proforma_context())
        flat = [cell for row in rows for cell in row]
        assert "7940 Plantation Blvd, Miramar, FL 33023" in flat
        assert "Miramar" in flat

    def test_includes_cost_data(self):
        _, rows = _build_pro_forma_rows(_proforma_context())
        flat = [cell for row in rows for cell in row]
        assert "$800,000" in flat  # hard costs

    def test_includes_revenue_data(self):
        _, rows = _build_pro_forma_rows(_proforma_context())
        flat = [cell for row in rows for cell in row]
        assert "$1,600,000" in flat  # GDV

    def test_includes_comp_data(self):
        _, rows = _build_pro_forma_rows(_proforma_context())
        flat = [cell for row in rows for cell in row]
        assert "$450,000" in flat  # median price per acre

    def test_includes_roi(self):
        _, rows = _build_pro_forma_rows(_proforma_context())
        flat = [cell for row in rows for cell in row]
        # Check that ROI row exists
        assert any("ROI" in cell for cell in flat)

    def test_minimal_context_produces_rows(self):
        headers, rows = _build_pro_forma_rows(_minimal_context())
        assert headers == ["Category", "Metric", "Value"]
        assert len(rows) > 5  # at least property + costs + returns

    def test_subject_to_includes_mortgage(self):
        ctx = DealContext(
            property_address="456 Oak Ave, Fort Lauderdale, FL",
            deal_type=DealType.subject_to,
            financing_type="subject_to",
            purchase_price=350000.0,
            existing_mortgage_balance_1=280000.0,
            existing_mortgage_payment=1850.0,
        )
        _, rows = _build_pro_forma_rows(ctx)
        flat = [cell for row in rows for cell in row]
        assert "$280,000" in flat
        assert "Existing Mortgage" in flat

    def test_seller_carryback_included(self):
        ctx = DealContext(
            property_address="789 Pine St, Miami, FL",
            seller_carryback_amount=200000.0,
            seller_carryback_rate=6.0,
        )
        _, rows = _build_pro_forma_rows(ctx)
        flat = [cell for row in rows for cell in row]
        assert "$200,000" in flat
        assert "Seller Carryback" in flat

    def test_no_comps_when_zero(self):
        ctx = DealContext(
            property_address="No Comps Dr, Miami, FL",
            median_price_per_acre=0.0,
        )
        _, rows = _build_pro_forma_rows(ctx)
        flat = [cell for row in rows for cell in row]
        assert "Median $/Acre" not in flat


# ---------------------------------------------------------------------------
# render_google_sheets — mock the Google API call
# ---------------------------------------------------------------------------


class TestRenderGoogleSheets:
    @pytest.fixture
    def mock_create_spreadsheet(self):
        with patch(
            "plotlot.clauses.renderers.sheets_renderer.create_spreadsheet",
            new_callable=AsyncMock,
        ) as mock:
            mock.return_value = SpreadsheetResult(
                spreadsheet_id="fake-id-123",
                spreadsheet_url="https://docs.google.com/spreadsheets/d/fake-id-123",
                title="PlotLot Pro Forma — 7940 Plantation Blvd",
            )
            yield mock

    async def test_calls_create_spreadsheet(self, mock_create_spreadsheet):
        config = AssemblyConfig(
            document_type=DocumentType.proforma_spreadsheet,
            output_format="google_sheets",
        )
        context = _proforma_context()
        await render_google_sheets([], config, context)

        mock_create_spreadsheet.assert_called_once()
        call_args = mock_create_spreadsheet.call_args
        assert call_args.kwargs["title"].startswith("PlotLot Pro Forma")
        assert len(call_args.kwargs["headers"]) == 3
        assert len(call_args.kwargs["rows"]) > 10

    async def test_returns_sheets_result(self, mock_create_spreadsheet):
        config = AssemblyConfig(
            document_type=DocumentType.proforma_spreadsheet,
            output_format="google_sheets",
        )
        context = _proforma_context()
        result = await render_google_sheets([], config, context)

        assert isinstance(result, SheetsProFormaResult)
        assert result.spreadsheet_id == "fake-id-123"
        assert "docs.google.com" in result.spreadsheet_url

    async def test_title_includes_address(self, mock_create_spreadsheet):
        config = AssemblyConfig(
            document_type=DocumentType.proforma_spreadsheet,
            output_format="google_sheets",
        )
        context = _proforma_context()
        await render_google_sheets([], config, context)

        call_title = mock_create_spreadsheet.call_args.kwargs["title"]
        assert "7940 Plantation Blvd" in call_title

    async def test_minimal_context_works(self, mock_create_spreadsheet):
        config = AssemblyConfig(
            document_type=DocumentType.proforma_spreadsheet,
            output_format="google_sheets",
        )
        context = _minimal_context()
        result = await render_google_sheets([], config, context)

        mock_create_spreadsheet.assert_called_once()
        assert result.spreadsheet_id == "fake-id-123"
