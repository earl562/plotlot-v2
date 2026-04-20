# Quality Improvement Loop

You are running an autonomous prompt optimization loop for PlotLot. Your goal is to improve LLM extraction accuracy by iterating on prompt templates.

## Instructions

LOOP FOREVER:
1. Read the current system prompt and tool definitions in `src/plotlot/retrieval/llm.py`

2. Identify one specific improvement to try. Examples:
   - Add explicit examples for ambiguous zoning codes
   - Improve numeric parsing instructions (e.g., "25 units per acre" -> 25.0)
   - Better handling of conditional/overlay zoning
   - Clearer instructions for FAR vs density distinction

3. Make the modification to the prompt template

4. Run the eval suite:
   ```bash
   cd plotlot && uv run pytest tests/eval/test_eval_experiment.py -v --tb=short 2>&1
   ```

5. Parse results. For each golden case, check:
   - Zoning code matches expected
   - Lot size within 5% of expected
   - Year built exact match
   - Max units within expected range

6. Decision:
   - If metrics improved or stayed equal -> keep the change, commit
   - If any metric regressed -> `git checkout -- src/plotlot/retrieval/llm.py` (revert)

7. Log to quality.tsv (append):
   ```
   iteration\tchange_description\tzoning_match_before\tzoning_match_after\taction\ttimestamp
   ```

8. Never stop. Try the next improvement.

## Output File
`quality.tsv` in the repo root.

## Branch
Create branch `autoresearch/quality-YYYY-MM-DD` before starting.
