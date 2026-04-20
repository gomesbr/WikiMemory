---
type: project-rules
project: ai-trader
updated: 2026-04-20T01:19:51.490777Z
tags: [project/ai-trader, rules]
---

# Ai Trader - Project Rules

## ALWAYS DO

- Phase 1 write restriction: only strategist may perform mutating AITrader actions; research/execution roles remain non-writing.
- Operational knobs must be UI-editable and DB-persisted for normal changes, and every knob change must be audit logged with actor, timestamp, old/new values, and reason.
- Default trade flow is approval-first via UI, with account-level toggle for full auto mode.
- Kill switch scope is global only.
- Persist full deterministic data snapshots required for exact trade replay.
- Webhook authentication must use an IP allowlist.
- Automation-gate incident checks use a rolling 30-day window.
- Backtest v1 scope is daily timeframe with one year support.

## NEVER DO

_No selected items from this evidence._

## CONDITIONAL RULES

- In mock mode, Strategy Lab and Command Center must use the same strategy IDs/data source so selections and metrics remain coherent across tabs.
- For taxable accounts after a realized loss, enforce a conservative 31-day block on both same symbol and same options contract to avoid wash sales.

## SCOPE NOTES

- Applies only to `ai-trader` unless a rule explicitly says otherwise.
