---
type: project-rules
project: codexclaw
updated: 2026-04-20T01:19:51.502464Z
tags: [project/codexclaw, rules]
---

# Codexclaw - Project Rules

## ALWAYS DO

_No selected items from this evidence._

## NEVER DO

_No selected items from this evidence._

## CONDITIONAL RULES

- For UI work, use src/ui/skin.ts as source of truth and reuse renderOpenClawSkinCss(); keep visual tokens/components consistent across related apps unless the user explicitly requests a different theme.
- When analysis output is large, send concise highlights in Telegram and provide explicit pointer(s) to the persisted full report (e.g., report ID/path).
- When non-coder roles are configured to use the OpenAI API provider, OPENAI_API_KEY must be set; otherwise non-coder flows fail even if coder flows still work.
- When work yields follow-ups/status changes, include machine-readable TRACKER_TASKS and TRACKER_UPDATES blocks; blocked updates must include exact blockerReason.
- For production/daily Mission Control usage, run from main aligned with origin/main; treat WIP branches as development-only.

## SCOPE NOTES

- Applies only to `codexclaw` unless a rule explicitly says otherwise.
