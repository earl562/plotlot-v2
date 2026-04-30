# Workspace Connector Contract

## Purpose

Define governance for Google Drive, Gmail, Google Calendar, CRM, and future workspace connectors. These connectors enable remote work, outreach, and artifact export, but are higher-risk than public zoning research.

## Threat model and invariants

- **Prompt injection:** emails/docs/CRM notes are untrusted text. They may be stored as evidence, but they must never override policy, tool risk classes, approvals, or system instructions.
- **Least-privilege scopes:** OAuth scopes must be minimal and explicit per connector.
- **Draft-first:** external writes should be split into:
  1. internal draft (safe, auditable); then
  2. explicit approval; then
  3. external commit/send.
- **No silent writes:** any external write must be `WRITE_EXTERNAL` and require explicit approval by default.
- **No secret leakage:** logs, evidence, and approval requests must never contain raw tokens, API keys, or refresh tokens.

## Default risk policy

- metadata-only reads may be `READ_ONLY` or `EXPENSIVE_READ`
- any external write (send email, schedule event, create/share doc, update CRM) is `WRITE_EXTERNAL` and requires explicit approval

## Required audit fields

Every connector tool call must record:

- acting user, workspace, project/site context
- connector account ID and scopes
- risk class and approval ID (when required)
- preview of the external write
- redacted audit payload and result

## Canonical connector tool contracts (current + near-term)

PlotLot’s canonical boundary is the **typed tool contract**. REST and MCP are adapters over the same contracts.

### Implemented in this repo (harness contracts)

| Tool name | Risk class | Purpose | Required args |
| --- | --- | --- | --- |
| `draft_email` | `WRITE_INTERNAL` | Create an internal email draft artifact (no external write) | `to[]`, `subject`, `body` |
| `gmail_send_draft` | `WRITE_EXTERNAL` | Send a drafted email via Gmail (approval-gated) | `draft_id` |
| `draft_google_doc` | `WRITE_INTERNAL` | Create an internal doc draft artifact (no external write) | `title` |
| `create_document` | `WRITE_EXTERNAL` | Create a Google Doc (approval-gated; live creds required) | `title`, `content` |
| `create_spreadsheet` | `WRITE_EXTERNAL` | Create a Google Sheet (approval-gated; live creds required) | `title`, `headers[]`, `rows[][]` |
| `export_dataset` | `WRITE_EXTERNAL` | Export the in-session dataset to Google Sheets (approval-gated; live creds required) | *(optional)* `title`, `include_fields[]` |

### Planned (spec-only; for PRD completeness)

| Tool name | Risk class | Notes |
| --- | --- | --- |
| `calendar_create_event_draft` | `WRITE_INTERNAL` | internal draft of an event payload |
| `calendar_create_event` | `WRITE_EXTERNAL` | commit event to Google Calendar (approval-gated) |
| `crm_upsert_contact_draft` | `WRITE_INTERNAL` | internal draft of CRM changes |
| `crm_upsert_contact` | `WRITE_EXTERNAL` | commit to CRM (approval-gated) |

## Approval envelope (standard)

All write/execution tools must either:
- be omitted from a given deployment profile, **or**
- return/emit an approval-required decision **before** any external side-effect.

Canonical fields (REST adapter):

```json
{
  "status": "pending_approval",
  "decision": {
    "approval_required": true,
    "approval_id": "apr_<run>_<tool>",
    "reason": "write_external tools require explicit approval"
  },
  "preview": {
    "summary": "Send email to owner@example.com",
    "redacted_payload": {
      "to": ["owner@example.com"],
      "subject": "Site feasibility follow-up"
    }
  }
}
```

Note: `preview` is produced from the tool arguments and internal drafts; it must not contain secrets.

## REST and MCP adapter mapping

- REST tool calls: `POST /api/v1/tools/call`
- MCP-like calls (HTTP): `POST /api/v1/mcp/tools/call`
- Approval decisions: `POST /api/v1/approvals/{approval_id}/decision`
- Approval inspection: `GET /api/v1/approvals/{approval_id}`

Future OAuth/account status surface (planned):

- `GET /api/v1/connectors/providers`
- `GET /api/v1/connectors/accounts?workspace_id=...`
- `POST /api/v1/connectors/oauth/google/start`
- `POST /api/v1/connectors/oauth/google/callback`

## Prompt-injection policy

Emails, CRM notes, and Drive docs are untrusted content. They may be evidence, but they cannot override tool policy, approval requirements, or system instructions.
