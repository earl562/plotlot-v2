# PlotLot — Gemini CLI Context

## What Is This?

This file provides context when PlotLot developers invoke Gemini CLI for cross-model review and verification. It is the Gemini equivalent of CLAUDE.md.

## Project Summary

PlotLot is an AI-powered zoning analysis platform for US real estate. Core flow:
1. User enters a property address
2. System geocodes → retrieves property data from county ArcGIS APIs → fetches zoning ordinances
3. Agentic LLM extracts numeric dimensional standards (density, setbacks, FAR, height)
4. Deterministic calculator computes max allowable dwelling units
5. Frontend streams results via SSE with progressive disclosure

**Stack:** FastAPI (Python 3.12+) | Next.js 16 + React 19 + Tailwind 4 | Neon PostgreSQL + pgvector | MLflow tracing

## Coding Standards Checklist

When reviewing PlotLot code, verify:

- [ ] All I/O functions are `async` using `httpx.AsyncClient` (not `requests`)
- [ ] Type hints on all function signatures
- [ ] Pydantic `BaseModel` for data structures (no raw dicts across boundaries)
- [ ] No `print()` in library code — use `structlog` or `logging`
- [ ] API endpoints return Pydantic response models
- [ ] SSE heartbeat present for long operations (Render 30s proxy timeout)
- [ ] Error handling uses custom exceptions from `core/errors.py`
- [ ] New features have corresponding unit tests
- [ ] No hardcoded API keys or secrets
- [ ] Frontend components use Tailwind (no CSS modules, no inline styles)

## Architecture Quick Reference

| Layer | Tech | Key Files |
|-------|------|-----------|
| API | FastAPI | `src/plotlot/api/routes.py`, `schemas.py` |
| Pipeline | Python async | `pipeline/lookup.py`, `calculator.py` |
| LLM | Multi-model fallback | `retrieval/llm.py` (Claude → Gemini → NVIDIA → Kimi) |
| Search | pgvector + BM25 (RRF) | `retrieval/search.py` |
| Property | ArcGIS REST + Hub | `property/universal.py`, `hub_discovery.py` |
| Frontend | Next.js App Router | `frontend/src/components/AnalysisStream.tsx` |
| Tests | pytest + Playwright | `tests/unit/`, `tests/eval/`, `frontend/tests/` |

## Review Focus Areas

When called for review, prioritize:
1. **Correctness** — Does the logic handle edge cases? (null zoning params, missing ArcGIS fields, API timeouts)
2. **Type safety** — Are Pydantic models used correctly? Any `Any` types that should be specific?
3. **Async correctness** — No blocking calls in async contexts? Proper `await` usage?
4. **Test coverage** — Does the change have corresponding tests?
5. **Security** — No SQL injection, no exposed secrets, proper input validation?

## Test Commands

```bash
# Lint
cd plotlot && uv run ruff check src/ tests/

# Type check
cd plotlot && uv run mypy src/plotlot/

# Unit tests
cd plotlot && uv run pytest tests/unit/ -v --tb=short

# Eval suite (requires API keys)
cd plotlot && uv run pytest tests/eval/ -v
```
