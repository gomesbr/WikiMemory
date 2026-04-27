# Adapter Extension Guide

SessionMemory keeps machine-specific paths in config and keeps parsing logic behind adapters.

## Current Adapter Types

- `log_source`: reads agent conversation logs.
- `project_delta_source`: reads project state changes.
- `markdown_renderer`: renders compact memory files.
- `bootstrap_renderer`: renders the agent startup entry file.

## Adding a Log Adapter

1. Add an adapter id to `sessionmemory/adapters.py`.
2. Add config keys to `config/product_config.json`.
3. Normalize source records into the canonical evidence shape used by `sessionmemory/ingest.py`.
4. Preserve provenance fields: source id, line/byte location where possible, timestamp, actor type, and content surfaces.
5. Add a real sample log under `examples/source-logs/` if it can be safely shared.
6. Add a test that runs through ingest, memory, bootstrap, and lint.

## Canonical Evidence Shape

Log evidence should emit:

- `evidence_id`
- `evidence_type = log_event`
- `source_adapter`
- `source_id`
- `project_hint`
- `actor_type`
- `timestamp`
- `content_surfaces[]`
- `provenance`
- `metadata`

Project delta evidence should emit the same provenance-first shape with `evidence_type` values such as `git_head` or `git_status_item`.

## Policy

- User-authored content should be preferred over agent reasoning.
- Agent reasoning should not become durable memory by default.
- One-off commands should become recent context, not durable rules.
- Explicit promotion language wins over repetition.
