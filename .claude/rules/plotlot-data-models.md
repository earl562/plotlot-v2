# PlotLot Data Model Reference

## `NumericZoningParams` (core/types.py)
All fields are `Optional[float] = None`. The LLM extracts what it can find; the calculator handles `None` gracefully.

Key fields: `max_density_units_per_acre`, `min_lot_area_sqft`, `max_far`, `max_lot_coverage_pct`, `max_height_ft`, `setback_front_ft`, `setback_side_ft`, `setback_rear_ft`, `min_unit_size_sqft`, `max_stories`

## `DensityAnalysis` (core/types.py)
Result of the calculator. Contains:
- `max_units` — final answer (integer)
- `governing_constraint` — which of the 4 constraints limited the result
- `constraints` — list of `ConstraintResult` with each constraint's individual max-units
- `buildable_area_sqft` — lot area minus setbacks
- `parameters` — the `NumericZoningParams` used

## `PropertyRecord` (core/types.py)
Property data from ArcGIS: `folio`, `address`, `owner`, `municipality`, `county`, `lot_size_sqft`, `lot_dimensions`, `zoning_code`, `zoning_description`, `land_use_code`, `year_built`, `assessed_value`, `market_value`, `lat`, `lng`, `parcel_geometry`, `zoning_layer_url`

## `ComparableSale` (core/types.py)
Comp data: `address`, `sale_price`, `sale_date`, `lot_size_sqft`, `zoning_code`, `distance_miles`, `price_per_acre`, `price_per_unit`, `adjustments`

## `CompAnalysis` (core/types.py)
Comp results: `comparables`, `median_price_per_acre`, `estimated_land_value`, `adv_per_unit`, `confidence`

## `ProForma` (core/types.py)
Financial analysis: `gross_development_value`, `hard_costs`, `soft_costs`, `builder_margin`, `max_land_price`, `cost_per_door`, `construction_cost_psf`, `adv_per_unit`, `max_units`

## `ZoningReport` (core/types.py)
Full pipeline output: address, municipality, county, zoning district, allowed/conditional/prohibited uses, setbacks, dimensional standards, property_record, numeric_params, density_analysis, comp_analysis, pro_forma, sources, confidence
