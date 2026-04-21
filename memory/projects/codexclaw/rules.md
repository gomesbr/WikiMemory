---
type: project-rules
project: codexclaw
updated: 2026-04-21T05:01:53.132338Z
tags: [project/codexclaw, rules]
---

# Codexclaw - Project Rules

## ALWAYS DO

- Only the `coder` agent should use Codex-oriented model behavior; `strategist`, `research`, and `execution` should use GPT-5-style chat behavior.
- Default user interaction should be natural free-form conversation via strategist-led routing, not rigid intake forms or menu/checklist replies.
- Treat configured `CODER_WORKDIR` and `CODER_ADD_DIRS` as writable by default; do not request extra access unless a command has already failed with concrete filesystem/permission evidence.

## NEVER DO

- CodexClaw Pro is a multi-agent trading orchestration system (Telegram/Telegraf + TypeScript + SQLite) for research, monitoring, platform development, and strategic coordination; it must never execute trades directly and should only produce advisory outputs or trade intents for external platforms.

## CONDITIONAL RULES

- Task/coder responses must include a `Completion Matrix` mapping each acceptance criterion to concrete evidence; when failures occur, include root cause, fix rationale, and non-recurrence evidence.
- UI skin source of truth is `src/ui/skin.ts`; reuse `renderOpenClawSkinCss()` and mirror the same token/component style across related apps unless the user explicitly requests a different theme.
- When applicable, emit `TRACKER_TASKS` for discovered follow-ups and `TRACKER_UPDATES` for status transitions (including `blockerReason` when blocked); machine directive blocks must be stripped from user-facing replies after internal processing.
- UI skin standard: `CodexClaw/src/ui/skin.ts` is source of truth; use `renderOpenClawSkinCss()` for CodexClaw and mirror same tokens/components in other apps unless explicitly asked for a new theme.
- For coder/reviewer task outputs, include a `Completion Matrix` mapping each acceptance criterion to evidence in `[pass|fail] <criterion> -> evidence: <tests/logs/files>` format; if blocked, mark fail with blocker explanation.
- For large analyses, send concise highlights in Telegram and clearly point to persisted full research instead of sending full text in-chat.
- When additional follow-ups are discovered, append a `TRACKER_TASKS` JSON block with required fields; use a `TRACKER_UPDATES` JSON block to move task status; if status is `blocked`, include the mandatory exact `blockerReason` describing required user input/access.

## SCOPE NOTES

- Applies only to `codexclaw` unless a rule explicitly says otherwise.
