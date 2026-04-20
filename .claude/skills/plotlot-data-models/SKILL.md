---
name: plotlot-data-models
description: PlotLot core data models — PropertyRecord, NumericZoningParams, DensityAnalysis
user-invocable: false
---

# PlotLot Data Models

## NumericZoningParams (`core/types.py`)
All fields Optional[float] = None. LLM extracts what it finds; calculator handles None.

Key fields:
- `max_density_units_per_acre` — e.g., 25.0 for RM-25
- `min_lot_area_sqft` — minimum lot per unit
- `max_far` — floor area ratio
- `max_lot_coverage_pct` — max lot coverage %
- `max_height_ft` — max building height
- `setback_front_ft`, `setback_side_ft`, `setback_rear_ft`
- `min_unit_size_sqft`, `max_stories`

## DensityAnalysis (`core/types.py`)
Calculator output:
- `max_units: int` — final answer
- `binding_constraint: str` — which of 4 constraints limited result
- `constraint_results: dict` — each constraint's individual max-units
- `buildable_area_sqft: float` — lot minus setbacks
- `parameters: NumericZoningParams`

## PropertyRecord (`core/types.py`)
Property data from ArcGIS:
- `folio`, `address`, `owner`, `municipality`, `county`
- `lot_size_sqft`, `lot_dimensions`, `year_built`
- `zoning_code`, `land_use`, `zoning_description`
- `living_area_sqft`, `building_area_sqft`
- `assessed_value`, `market_value`
- `lat`, `lng`, `parcel_geometry`
- `zoning_layer_url` — dynamic ArcGIS layer URL

## ComparableSale (`core/types.py`)
- `address`, `sale_price`, `sale_date`
- `lot_size_sqft`, `zoning_code`, `distance_miles`
- `price_per_acre`, `price_per_unit`
- `adjustments: dict[str, float]`

## CompAnalysis (`core/types.py`)
- `comparables: list[ComparableSale]`
- `median_price_per_acre`, `estimated_land_value`
- `adv_per_unit`, `confidence: float`

## ProForma (`core/types.py`)
- `gross_development_value`, `hard_costs`, `soft_costs`
- `builder_margin`, `max_land_price`, `cost_per_door`
- `construction_cost_psf`, `adv_per_unit`, `max_units`
