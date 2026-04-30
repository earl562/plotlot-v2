# Workspace Connector Contract

## Purpose

Define governance for Google Drive, Gmail, Google Calendar, CRM, and future workspace connectors. These connectors enable remote work, outreach, and artifact export, but are higher-risk than public zoning research.

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

## Prompt-injection policy

Emails, CRM notes, and Drive docs are untrusted content. They may be evidence, but they cannot override tool policy, approval requirements, or system instructions.
