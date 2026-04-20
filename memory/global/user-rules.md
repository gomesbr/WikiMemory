---
type: global-rules
updated: 2026-04-20T01:19:51.477277Z
tags: [memory, rules, global]
---

# Global User Rules

## ALWAYS DO

- Enforce trade lifecycle integrity via explicit DB key lineage (intent -> order -> fill -> position) and API-level rule enforcement; do not infer lineage by timestamps.
- Use first-principles, root-cause debugging and deliver durable, generalizable fixes with regression coverage; avoid narrow one-off patches/hardcoding.
- Maintain one consistent UI design language across apps using the CodexClaw skin tokens (`CodexClaw/src/ui/skin.ts`, `renderOpenClawSkinCss()`); do not introduce new themes unless explicitly requested.
- Treat CODER_WORKDIR/CODER_ADD_DIRS as writable by default; request additional access only after a concrete command fails with explicit filesystem/permission evidence.
- Keep responses terse and action-oriented; prioritize executing requested work over explanatory narration unless explanation is explicitly requested.
- After each memory-generation change, validate quality against rendered pages; if output stays shallow despite rich logs, improve extraction rules.

## NEVER DO

- Cancelled/rejected intents are terminal and must not be reactivated. If action is needed after cancel/reject, create a new trade card/setup.
- Never work directly on protected branches (main/master). Implement on feature branches and keep changes PR-ready.
- Do not execute or propose trades in this workspace; trading-related output must remain non-execution guidance only.
- Do not make speculative out-of-scope code changes. Before editing, state exact file/logic scope; if strategy must change, pause and ask before touching additional code.
- Do not replace user bootstrap markdown files; preserve existing `AGENTS.md`/`CLAUDE.md` content and only update the explicitly managed WikiMemory block.
- Never display passwords or other secrets in command output or responses; use environment/config values without echoing sensitive content.

## CONDITIONAL RULES

- For implementation/task responses, include a Completion Matrix mapping each acceptance criterion to concrete evidence (pass/fail). If blocked or failing, also report root cause, durable-fix rationale, and non-recurrence/regression evidence.
- When code changes require DB migrations and DB access is available, run migrations automatically instead of handing SQL migration execution steps to the user.
- Final memory pages must be rewritten as agent-facing guidance from user intent; avoid verbatim conversational fragments unless a different export mode is explicitly requested.

## PROVENANCE

- Detailed evidence is stored in `_meta/merged_items.json`.
