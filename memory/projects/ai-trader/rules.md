---
type: project-rules
project: ai-trader
updated: 2026-04-19T04:35:36.037403Z
tags: [project/ai-trader, rules]
---

# ⚙️ Ai Trader - Project Rules

## ALWAYS DO

_None currently extracted._

## NEVER DO

- Do not expose a separate custom profile editor; editing should happen through the active-penalties controls instead.
- Do not show wash-sale or tax-lot cards while the related position is still open; those cards should only appear once the position is closed.
- Do not mirror the user's wording into the story description; rewrite the request into a clearer, interpreted summary.
- Do not duplicate the risk policy object in the config snapshot; present runtime/config values in a cleaner item-by-item format instead of raw arrays.

## CONDITIONAL RULES

- make all configuration knobs editable from the database-backed UI and keep a change history that records who changed what and when.
- show a performance line chart on the main control console that compares paper, Roth, and taxable/regular accounts, with separate lines for each paper strategy.
- remove the roll-request card and the roll transition from the UI; represent the relationship instead with a dotted link from the prior closed position to the new opened position, and update mocks accordingly.
- the conversation transcript document must preserve the original wording and order exactly, without paraphrasing.
- place the project inside the AITrader directory and do not create a separate OpenClaw top-level folder.
- the trade card view should include a chart image or annotated snapshot showing the pattern or setup that triggered the trade.
- provide a morning report before market open that lists the highest-scoring trades for the day and any planned closing trades, then continue collecting and analyzing new triggers during the trading session.
- keep knob settings stored in the database and editable from the UI; avoid requiring backend-side manual edits for routine knob changes.
- provide an audit history for knob changes, including when each change happened and what changed.
- populate every menu and submenu with mock data so the interface can be evaluated before live data is available.
- support standard time-range filters for the performance chart, including day, week, month, 3 months, 6 months, 1 year, YTD, 3 years, 5 years, and all time.
- place the Roth and taxable toggles before the paper-trade toggles in the UI.

## PROMOTED RULES (EXPLICIT)

- 35 explicit rule(s) are listed above by behavior bucket.

## INFERRED RULES

_None currently extracted._

## SCOPE NOTES

- Applies only to this project.

## RELATED

- [[Ai Trader Recent]]
- [[Ai Trader Rules]]
