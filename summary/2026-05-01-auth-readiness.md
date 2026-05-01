# 2026-05-01 — Auth readiness snapshot (what’s required for live E2E)

Branch: `codex/dev-branch-pipeline`

This snapshot was captured via:

```bash
cd plotlot
make auth-readiness
```

## What’s needed for a true “served live agent” E2E

To run `make live-agent-e2e` successfully, you’ll typically need:

- **Database**: `DATABASE_URL` (and a reachable Postgres; `make db-up` for local Docker)
- **LLM agent**: at least one provider configured (e.g. `OPENAI_API_KEY` or Codex OAuth)
- **Any live tools you want to exercise**:
  - `GEOCODIO_API_KEY` for geocoding
  - `JINA_API_KEY` for web search
  - Google Workspace OAuth vars for Docs/Sheets tools, etc.

## Readiness output

- `deterministic_local`: READY
- `database_backed_e2e`: BLOCKED (missing `DATABASE_URL`)
- `llm_agent`: BLOCKED (missing LLM credentials)
- `geocoding`: BLOCKED (missing `GEOCODIO_API_KEY`)
- `web_search`: BLOCKED (missing `JINA_API_KEY`)
- `google_workspace`: BLOCKED (missing Google OAuth vars)
- `google_rendering`: BLOCKED (missing `GOOGLE_API_KEY`)
- `google_maps_enhanced`: READY (key optional; OSM fallback exists)
- `stripe_billing`: BLOCKED (missing Stripe vars)
- `clerk_auth`: READY (keys optional unless auth enforced)
- `fal_video`: BLOCKED (missing `FAL_KEY`)
- `huggingface_embeddings`: BLOCKED (missing `HF_TOKEN`)
- `observability`: READY (optional)

