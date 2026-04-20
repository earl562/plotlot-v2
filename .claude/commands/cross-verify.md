---
model: haiku
allowed-tools: Bash, Read
---
Send the current git diff to Gemini CLI for post-implementation verification.

## Steps

1. Capture the diff:
   ```bash
   git diff --cached 2>/dev/null || git diff
   ```

2. Send to Gemini for verification:
   ```bash
   gemini -p "Verify this code change for PlotLot (FastAPI + Next.js zoning analysis app). Check: type safety, async correctness, Pydantic model usage, test coverage, no print() in library code. Report issues only.\n\n$(git diff --cached 2>/dev/null || git diff)"
   ```

3. Report Gemini's findings.
