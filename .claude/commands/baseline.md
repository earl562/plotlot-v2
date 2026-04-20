---
model: haiku
allowed-tools: Bash, Read
---
Run full health check and report a dashboard.

## Steps

1. Lint check:
   ```bash
   cd plotlot && uv run ruff check src/ tests/ 2>&1 | tail -3
   ```

2. Type check:
   ```bash
   cd plotlot && uv run mypy src/plotlot/ 2>&1 | tail -3
   ```

3. Unit tests:
   ```bash
   cd plotlot && uv run pytest tests/unit/ -v --tb=short 2>&1 | tail -5
   ```

4. Playwright (frontend):
   ```bash
   cd plotlot/frontend && npx playwright test --grep @no-db 2>&1 | tail -5
   ```

5. Health endpoint:
   ```bash
   curl -s http://localhost:8000/health 2>&1
   ```

Report a compact dashboard:

| Check | Status | Details |
|-------|--------|---------|
| ruff | pass/fail | error count |
| mypy | pass/fail | error count |
| pytest | pass/fail | X passed, Y failed |
| playwright | pass/fail | X/8 passed |
| health | pass/fail | response |
