# Data Ingestion Loop

You are running an autonomous ingestion loop for PlotLot. Your goal is to systematically ingest zoning ordinances from Municode for all discoverable municipalities.

## Instructions

LOOP FOREVER:
1. List all discoverable municipalities:
   ```bash
   cd plotlot && uv run plotlot-search --list-municipalities 2>&1
   ```

2. Check which are already ingested:
   ```bash
   cd plotlot && uv run python -c "
   from plotlot.storage.db import get_chunk_counts
   print(get_chunk_counts())
   "
   ```

3. Pick the next un-ingested municipality (prioritize by county coverage):
   - Miami-Dade municipalities first (largest county)
   - Then Broward municipalities
   - Then Palm Beach municipalities

4. Run ingestion:
   ```bash
   cd plotlot && uv run plotlot-ingest --municipality "MUNICIPALITY_NAME" 2>&1
   ```

5. Verify search quality:
   ```bash
   cd plotlot && uv run plotlot-search --municipality "MUNICIPALITY_NAME" \
     --query "residential zoning density" --limit 3 2>&1
   ```

6. Log to ingest.tsv (append):
   ```
   municipality\tcounty\tchunks_ingested\tsearch_quality\tstatus\ttimestamp
   ```

7. Commit progress every 3 municipalities:
   ```bash
   git add ingest.tsv && git commit -m "chore: ingested MUNICIPALITY_NAME (N chunks)"
   ```

8. Never stop. Ingest the next municipality.

## Output File
`ingest.tsv` in the repo root.

## Branch
Create branch `autoresearch/ingest-YYYY-MM-DD` before starting.
