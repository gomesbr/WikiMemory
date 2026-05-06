---
type: project-rules
project: sessionmemory
updated: 2026-04-21T05:01:53.154669Z
tags: [project/sessionmemory, rules]
---

# SessionMemory - Project Rules

## ALWAYS DO

- Treat raw logs as external immutable source-of-truth: do not copy/rewrite raw logs in-repo, and process with streaming/append-aware reads that only commit complete lines.
- Maintain strict domain separation between GLOBAL and project namespaces (`AI Trader`, `Open Brain`, `AI Scientist`) while allowing explicit cross-project labeling; keep Open Brain and AI Scientist distinct even in shared repositories.
- LLM synthesis is allowed in bounded form, but every synthesized claim must be grounded in extracted evidence with provenance/citations.
- Generated wiki/memory pages should be deterministic rewrites; do not preserve manual edits inside generated managed content.
- Before implementation, inspect the repository deeply and present a phased, testable plan; do not jump directly to coding.
- Mock data must be deterministic and coherent across screens, seeded in PostgreSQL (not UI-only), with fully linked entities and trust-state values consistent with current incidents/active penalty profile.

## NEVER DO

- When generating bootstrap markdown files (e.g., `AGENTS.md`, `CLAUDE.md`), never replace user-authored content; only append/update a managed SessionMemory block so user information is preserved.
- Do not flatten logs into simple prompt/response form; preserve trace structures like `session_meta`, `response_item`, `event_msg`, and `turn_context`.
- Apply temporal invalidation rigorously: older open questions/open items must be marked resolved or superseded when newer evidence closes them, and should not remain rendered as open.
- Do not promote one-off commands, progress narration, runtime-local instructions, or schema scaffolding into durable rule/preference memory.

## CONDITIONAL RULES

- When DB access is available and changes require migrations, run migrations automatically and report results instead of asking the user to run SQL manually.
- In Obsidian, open the `wiki` subfolder via `Open folder as vault` rather than opening the whole repository.

## SCOPE NOTES

- Applies only to `sessionmemory` unless a rule explicitly says otherwise.
