# Adversarial Stress Testing Loop

You are running an autonomous stress testing loop for PlotLot. Your goal is to find edge cases that break the pipeline.

## Instructions

LOOP FOREVER:
1. Pick a challenging address category:
   - County boundary (address right on the border between two counties)
   - Unusual zoning (PUD, planned unit development, overlay districts)
   - Mixed-use zoning (commercial + residential)
   - Historic district (different rules apply)
   - Very large parcel (100+ acres -- agricultural/ranch)
   - Very small lot (< 2,000 sqft -- urban infill)
   - No zoning data available (unincorporated area)
   - Recently annexed area (may have transitional zoning)

2. Find a real address matching that category (web search for examples)

3. Run the full pipeline:
   ```bash
   curl -s -X POST http://localhost:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"address": "ADDRESS"}' 2>&1 | head -50
   ```

4. Analyze the result:
   - Did it crash? (500 error, timeout, unhandled exception)
   - Did it return incorrect data? (wrong zoning, wrong lot size)
   - Did it handle the edge case gracefully? (appropriate error message)

5. Log to stress.tsv (append):
   ```
   address\tcategory\texpected\tactual\tseverity\ttimestamp
   ```

6. If a crash or incorrect result is found:
   - Write a new test case in `tests/eval/` or `tests/unit/`
   - Record the golden expected values

7. Never stop. Find the next edge case.

## Severity Levels
- critical: crash, unhandled exception, data loss
- high: incorrect zoning code, wrong lot size, wrong max units
- medium: missing optional data, degraded accuracy
- low: cosmetic issues, slow response

## Output File
`stress.tsv` in the repo root.
