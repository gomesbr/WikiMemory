---
type: project-rules
project: ai-trader
updated: 2026-04-19T13:07:41.128984Z
tags: [project/ai-trader, rules]
---

# ⚙️ Ai Trader - Project Rules

## ALWAYS DO

_None currently extracted._

## NEVER DO

- Do not add role-based permissions for now because the platform is currently intended for a single user.
- Do not reinstate canceled or rejected states; if one was created in error, the correction must be a new trade card rather than reopening the old one.
- Do not invent extra subtasks that the user did not ask for, especially when they are unrelated older requests that keep resurfacing.
- Do not add a separate custom profile editor; keep penalty editing and auditability centered in the active penalties and audit views.
- Do not show wash-sale or tax-lot cards while the related position is still open; those cards are only valid after the position is closed.
- Do not let node/card dragging reorder or visually shift edge attachment points; links should remain stable while cards move.
- Do not show tax-lot profit and loss in the lineage graph if it confuses the analysis; keep that node as a tax-event indicator only.
- Do not create extra research artifacts such as video-related markdown files unless they are explicitly needed for the task.

## CONDITIONAL RULES

- When developing a new Ai Trader version that is not yet in production use, do not preserve backward compatibility with the previous version by default. Treat the new version as a clean system unless the user explicitly asks for migration or compatibility support.
- make all configuration knobs database-backed and editable from the UI, with no need to change backend code for routine tuning.
- the UI should present JSON-heavy fields in a more approachable way, with the raw JSON still accessible elsewhere for inspection. Audit-trail rows should support expanding to reveal additional hidden details, and label/value spacing should be tightened so fields read as a single unit.
- the strategy configuration area should support multiple strategies per account, with only one active strategy for Roth and taxable accounts at a time, while paper accounts may have multiple strategies active or available. The UI should let users choose a strategy to view or edit, and save strategy names and values per account.
- fix the lineage graph so links render from the correct nodes instead of clustering in the top-left, and ensure the graph can display complete chains without missing backward connections.
- the roll-request card should be removed from the UI, and the roll transition should be replaced with a dotted visual link from the prior closed position to the new opened position.
- allow intents to be canceled before they become trades. The intent lifecycle should distinguish read, planned, submitted, and ready states, with the ready label reflecting a validated state only if the code actually enforces that transition.
- when generating the conversation document, preserve the transcript in exact chronological order and keep speaker labels clear so another agent can read it easily.
- place the new trading system inside the AITrader folder and do not create a separate top-level OpenClaw directory.
- support a daily operating flow with a pre-market report of best-scored entries and planned exits, daytime order placement within defined windows, continuous signal collection and analysis, and an end-of-day wrap-up.
- add an audit trail for configuration changes so each knob update records what changed and when it changed.
- make every configurable knob persist in the database and expose editing controls in the UI; do not require backend-side manual edits for routine knob changes. Also keep a change history that records each knob update with its timestamp.

## PROMOTED RULES (EXPLICIT)

- 65 explicit rule(s) are listed above by behavior bucket.

## INFERRED RULES

_None currently extracted._

## SCOPE NOTES

- Applies only to this project.

## RELATED

- [[Ai Trader Recent]]
- [[Ai Trader Rules]]
