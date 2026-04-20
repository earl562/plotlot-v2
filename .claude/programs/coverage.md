# Coverage Expansion Loop

You are running an autonomous coverage expansion loop for PlotLot. Your goal is to systematically test which US counties work with the UniversalProvider.

## Instructions

LOOP FOREVER:
1. Pick the next US county by metro population. Start with the top 50 MSAs. Use this order:
   - Already covered: Miami-Dade FL, Broward FL, Palm Beach FL, Mecklenburg NC
   - Next: Harris TX, Los Angeles CA, Cook IL, Maricopa AZ, San Diego CA, Orange CA, Dallas TX, King WA, Clark NV, Tarrant TX, Bexar TX, Hillsborough FL, Orange FL, Alameda CA, Wayne MI, Hennepin MN, Cuyahoga OH, Franklin OH, Travis TX, Denver CO...

2. For each county:
   a. Run Hub discovery:
      ```bash
      cd plotlot && uv run python -c "
      import asyncio
      from plotlot.property.hub_discovery import discover_datasets
      p, z = asyncio.run(discover_datasets(0, 0, 'COUNTY', 'STATE'))
      print(f'Parcels: {p.name if p else None}')
      print(f'Zoning: {z.name if z else None}')
      "
      ```
   b. Find a real address in that county (use web search or known addresses)
   c. Test the pipeline (if the backend is running):
      ```bash
      curl -s -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d '{"address": "ADDRESS"}' | head -20
      ```

3. Record to coverage.tsv (append):
   ```
   county\tstate\tparcels_found\tzoning_found\tpipeline_status\tfailure_mode\ttimestamp
   ```

4. Commit progress every 5 counties:
   ```bash
   git add coverage.tsv && git commit -m "chore: coverage expansion - N counties tested"
   ```

5. Never stop. Move to the next county.

## Output File
`coverage.tsv` in the repo root.

## Branch
Create branch `autoresearch/coverage-YYYY-MM-DD` before starting.
