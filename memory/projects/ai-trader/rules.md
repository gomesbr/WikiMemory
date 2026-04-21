---
type: project-rules
project: ai-trader
updated: 2026-04-21T05:01:53.120434Z
tags: [project/ai-trader, rules]
---

# Ai Trader - Project Rules

## ALWAYS DO

- Git workflow policy: do not merge/push directly to protected branches (`main`, `master`); perform work in feature branches and prepare PR-ready changes.
- Lineage edge identity is defined by `from`/`to` node IDs only.
- drag/reorder may change geometry.
- Enforce wash policy at DB and API levels (not app-layer only), and keep mock/demo wash data lifecycle-consistent without fake fallback rows.
- Place system contents directly under `AITrader`; do not create a nested `openclaw` root folder.
- Deterministic replay is required: persist full `data_snapshot` inputs needed to reproduce each trade exactly.
- TrendSpider webhook authentication must use IP allowlisting.
- Execution gate policy: approval UI is the default; account-level toggle may enable full auto mode.
- Kill switch scope is global-only.
- Lineage lifecycle linking must be enforced by DB PK/FK constraints and API rules; timestamp-based inference is not acceptable.
- Lineage UI rules: place card-level incidents under Summary; place linked incidents one column right of their anchor node; order position cards by timestamp; order tax-lot/wash-sale cards chronologically by `close_date` fallback `open_date` with `lot.id` tie-breaker.
- Per setup, allow only one `close` intent; additional close-like intents must be `roll_close`.

## NEVER DO

- `cancelled` and `rejected` are final for intents/setups and must never be reactivated; subsequent action requires creating a new trade card/setup.
- Do not appear to change linkage semantics.
- UI constraints: dark mode with clean spacing and subtle glass/translucent feel; no horizontal page scrolling; avoid layout jitter during refresh; hover states must not move elements (lighter-color hover only).
- `Execution -> Order Intents` must show only active/open intents (`planned`, `ready`); terminal statuses (`filled`, `cancelled`) must not appear there regardless of selected top date.
- Do not generate synthetic lineage records or integrity fallback artifacts; lineage must come from real DB entities, with missing data fixed in DB. Do not use `setup -> order` fallback edges.
- Tax lot and wash sale nodes/edges may appear only for closed positions, never open positions.
- Top date control must not filter lineage lifecycle history; lineage should display full lifecycle beyond selected top date.
- `View Lineage` must open lineage on the current screen (not a separate left-nav page), with a single explicit `Maximize`/`Minimize` toggle state and reserved page space so lineage never overlays/hides main content.

## CONDITIONAL RULES

- For AITrader coding responses, include a `Completion Matrix` mapping each acceptance criterion to concrete pass/fail evidence.
- For taxable accounts, enforce ultra-conservative wash-sale protection: after a realized loss, block new entries for 31 days at both symbol level and exact option-contract level.
- Lifecycle rule: `closed` is the true final setup/card status after `executed`; move from `executed` to `closed` only when `total_positions > 0` and `closed_positions === total_positions`.
- For rollovers/rollups/rolldowns to stay in the same trade-card lifecycle, rolled positions must keep the same `source_setup_id`.
- Lineage must render discrete chronological lifecycle records with hard entity links (`trade_card -> open_intent -> open_order -> open_fill -> position_opened -> close_intent -> close_order -> close_fill -> position_closed -> tax_lot` when applicable), using dotted lifecycle continuity only where explicitly allowed.

## SCOPE NOTES

- Applies only to `ai-trader` unless a rule explicitly says otherwise.
