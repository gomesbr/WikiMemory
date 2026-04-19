---
type: project-rules
project: ai-trader
updated: 2026-04-19T04:21:45.632541Z
tags: [project/ai-trader, rules]
---

# ⚙️ Ai Trader - Project Rules

## ALWAYS DO

- No always-do rules selected yet.

## NEVER DO

- Do not duplicate the risk policy object in the config snapshot; present runtime/config values in a cleaner item-by-item format instead of raw arrays.
- Do not expose a separate custom profile editor; editing should happen through the active-penalties controls instead.
- Do not mirror the user's wording into the story description; rewrite the request into a clearer, interpreted summary.
- Do not show wash-sale or tax-lot cards while the related position is still open; those cards should only appear once the position is closed.

## CONDITIONAL RULES

- Follow this operating rule: a skill-creator skill is available and should be used when adding or updating skills that extend the agent with specialized workflows or integrations.
- Follow this operating rule: a story may be closed once the acceptance criteria are met and the system understands completion; it does not need to remain open until manually closed by the user.
- Follow this operating rule: add a lineage-header indicator for whether the account is taxable or non-taxable so tax-card presence can be checked more easily.
- Follow this operating rule: add a trade-card history view that only includes cards after a decision is made, and keep the original decision control visible but disabled in history. In planning, cards should remain active until decided; once decided, they move out of planning and into history.
- Follow this operating rule: add a true terminal 'closed' state after execution; execution is not the final end state because positions can remain active through partial exits or roll actions until all related positions are finished.
- Follow this operating rule: add the position type to trade cards and propagate it through the rest of the application where that trade metadata is displayed.
- Follow this operating rule: allow entry and close intents to be canceled before they become trades.
- Follow this operating rule: apply the same planning-vs-history visibility behavior to order intents and close intents while they are still transient and not yet executed.
- Follow this operating rule: archive or clear out obsolete tasks when the user requests a reset so the workspace can start fresh.
- Follow this operating rule: audit the mock lineage data end to end and fill in missing backward links for any object, not just the previously mentioned cards.
- Follow this operating rule: avoid dense or repetitive layouts in this area; redesign it to reduce crowding and remove redundant elements.
- Follow this operating rule: changes to active penalties must create an audit entry in the audit section; do not rely on the edit screen to show that history.
- Follow this operating rule: compute trust score from the current mock data using the existing calculation logic, then update the displayed value so it matches the data.
- Follow this operating rule: design a lineage view that visually traces a trade card from trigger alert through configuration, generated trades, profit or loss, wash-sale effects, and final outcome using connected mini-cards or similar nodes.
- Follow this operating rule: design the user interface as a comprehensive control center with pages for configuration, trade review, auditing, and system visibility so the operator can manage nearly every adjustable setting from the UI.
- Follow this operating rule: enforce lineage integrity so an open intent cannot connect directly to a position; the chain must include the required order event in between, and the mock data should be corrected to match that rule.
- Follow this operating rule: fix the risk quality section so its tiles use consistent sizing.
- Follow this operating rule: for maximize/minimize controls, use a single toggle button only; the icon and label should switch between maximize and minimize, with no intermediate state.
- Follow this operating rule: for roll flows, the dotted linkage should originate from the closed position created by the roll-close intent and point to the opened position created by the roll-open intent; do not reverse that direction.
- Follow this operating rule: in audit trail rows, keep tag labels and values visually close together, and provide an expand control that reveals additional JSON details inline.
- Follow this operating rule: keep KPI snapshot tiles visually aligned and consistent in size, and adjust tile placement when the layout looks uneven.
- Follow this operating rule: keep hover interactions non-disruptive: buttons should not shift position on mouse-over; use a subtle color-lightening effect instead.
- Follow this operating rule: keep knob settings stored in the database and editable from the UI; avoid requiring backend-side manual edits for routine knob changes.
- Follow this operating rule: keep penalty audit details out of the editing screen to avoid clutter; the audit screen is the only place they need to appear.
- Follow this operating rule: keep runtime knobs focused on operational settings that belong inside the app; do not include schedule timing there because scheduling is handled externally by the agent.
- Follow this operating rule: keep strategy selections consistent across strategy lab and commander center so both tabs expose the same available strategies for retrieval and display.
- Follow this operating rule: keep the lineage view on the same screen when a user selects the lineage option; do not navigate into a separate lineage route behind the scenes.
- Follow this operating rule: keep the strategist in a clarification loop until the request is sufficiently clear before creating a story; avoid opening a story too early.
- Follow this operating rule: keep the visual layout of planning cards and history cards minimal by removing duplicated footer details; history should reuse the planning card presentation and only differ by showing the selected decision button.
- Follow this operating rule: keep trade cards visible in planning regardless of creation date until a decision is made, and show the creation date on the card so older cards can still be understood.
- Follow this operating rule: lineage edges must remain stable when cards are reordered visually; changing front/back placement of nodes must not cause links to move or reattach.
- Follow this operating rule: make all configuration knobs editable from the database-backed UI and keep a change history that records who changed what and when.
- Follow this operating rule: make the trade-card score highly prominent on the card so it is one of the first things the user notices.
- Follow this operating rule: mission Control needs a dedicated Scheduler area that separates configuration from execution logs and groups both by project.
- Follow this operating rule: no coder task was opened, and the strategist is asking me questions that should be asking the coder.
- Follow this operating rule: open order-intent entries should only remain visible while they are still active; once they are submitted or canceled, they should no longer appear in that section even if they were created on a past date.
- Follow this operating rule: persist mock data in the database rather than outside it, and keep the records linked coherently across pages so the test environment behaves like a realistic end-to-end system.
- Follow this operating rule: place the Roth and taxable toggles before the paper-trade toggles in the UI.
- Follow this operating rule: place the project inside the AITrader directory and do not create a separate OpenClaw top-level folder.
- Follow this operating rule: populate every menu and submenu with mock data so the interface can be evaluated before live data is available.
- Follow this operating rule: populate the database with mock linkage records that connect current alerts to trade cards, including cases where multiple alerts map to a single card.
- Follow this operating rule: prefer a robust root-cause fix over a narrow workaround when something is broken; optimize for an autonomous and resilient system rather than a quick patch.
- Follow this operating rule: provide a history view for trade cards so accepted and rejected decisions can be reviewed later.
- Follow this operating rule: provide a morning report before market open that lists the highest-scoring trades for the day and any planned closing trades, then continue collecting and analyzing new triggers during the trading session.
- Follow this operating rule: provide an audit history for knob changes, including when each change happened and what changed.
- Follow this operating rule: remove the best-day date tile because it looks unbalanced without the matching worst-day date tile.
- Follow this operating rule: remove the generic status label from planning cards when all cards are effectively awaiting a decision; the planning view should present them as pending decision rather than using the removed staging label.
- Follow this operating rule: remove the intent status guide from the interface.
- Follow this operating rule: remove the roll-request card and the roll transition from the UI; represent the relationship instead with a dotted link from the prior closed position to the new opened position, and update mocks accordingly.
- Follow this operating rule: remove the tax-lot profit and loss value from the tax lot node; keep that node as a tax-event indicator only.
- Follow this operating rule: represent the strategist as a single visible story with linked subtasks or follow-ups, so the user can track the coder work outside the parent story more easily.
- Follow this operating rule: show a performance line chart on the main control console that compares paper, Roth, and taxable/regular accounts, with separate lines for each paper strategy.
- Follow this operating rule: show the risk policy panel and other detailed panels below the graph; do not rely only on condensed graph cards for that information.
- Follow this operating rule: store mock records inside the database, not as external fixtures, and keep relationships between records intact so every page renders a coherent end-to-end scenario.
- Follow this operating rule: support standard time-range filters for the performance chart, including day, week, month, 3 months, 6 months, 1 year, YTD, 3 years, 5 years, and all time.
- Follow this operating rule: support wash-sale and tax-lot behavior for rollover positions, and verify the wash-blocking rules against the current screens and data before assuming a block should exist.
- Follow this operating rule: tax lot cards in the lineage graph should be sorted by date to improve readability.
- Follow this operating rule: the CLI agent should invoke the shell with only the needed command, not pass an entire prompt payload into the command line.
- Follow this operating rule: the command center should include a Projects area that links out to external project pages, starting with AITrader and opening the link in a new tab.
- Follow this operating rule: the conversation transcript document must preserve the original wording and order exactly, without paraphrasing.
- Follow this operating rule: the strategist should decompose user requests into one or more stories based on the actual work needed, using its own judgment rather than relying on the user to pre-split the request.
- Follow this operating rule: the task system should merge follow-up details into the same task when they belong to one semantic request, instead of creating duplicate tasks.
- Follow this operating rule: the trade card view should include a chart image or annotated snapshot showing the pattern or setup that triggered the trade.
- Follow this operating rule: the user has repeatedly asked for senior-engineer-level handling of the AITrader codebase, so responses should assume an experienced software engineering audience.
- Follow this operating rule: the user wants four agents with distinct responsibilities, and wants their skills adapted from the current project into separate skills and personas for transfer to each agent's own project.
- Follow this operating rule: the user wants the AITrader visual theme matched more closely to the reference skins, especially the color palette.
- Follow this operating rule: the user wants the assistant to review linked articles and comments thoroughly before answering, then summarize each link with the article title and practical ideas that could be applied to CodexClaw or AITrader.
- Follow this operating rule: trade cards should use a smaller layout similar to the trade history card size, and the screen must preserve horizontal scrolling so hidden content remains reachable.
- Follow this operating rule: treat each user story as the primary work item, with related tasks and follow-ups nested under it rather than spawning separate top-level stories for every clarification or dependency.
- Follow this operating rule: treat the AITrader and CodexClaw workstreams separately when planning enhancements; keep AITrader ideas parked for later while focusing implementation detail on CodexClaw first.
- Follow this operating rule: treat the penalty profile as incomplete unless a custom option exists that lets the user adjust individual knobs directly.
- Follow this operating rule: treat the repository as governed by local agent instructions in the project root; consult them before making changes and follow any referenced skill files when relevant.
- Follow this operating rule: treat the repository’s AGENTS.md and any referenced skill files as the primary local instructions before making changes.
- Follow this operating rule: treat the repository’s AGENTS.md guidance as the active local instruction source, and follow any referenced skill files when a task matches their scope.
- Follow this operating rule: treat the strategy lab as a DB-backed strategy configurator: users can edit strategy names and values per account, choose which strategy to load for viewing or editing, and maintain multiple inactive strategies alongside one active strategy for each live account type.
- Follow this operating rule: treat the system as a swing-trading platform that mainly gathers signals during the day and prepares entries for the next session, while intraday actions are mostly reserved for urgent exits or black-swan protection.
- Follow this operating rule: treat the system as greenfield when changing rules; do not infer new constraints from existing mock data, and do not allow canceled or rejected states to be reinstated.
- Follow this operating rule: use a dark, polished dashboard style with subtle translucent glass-like menus, clean spacing, and an organized layout.
- Follow this operating rule: use a friendlier presentation for JSON-heavy UI areas so users can inspect summarized fields in the app and only drill into raw JSON when needed.
- Follow this operating rule: use a kanban view where each story is a single card and its tasks or follow-ups are visible when expanded.
- Follow this operating rule: use realistic scenario data when populating the mock database so testing reflects actual product behavior before live data is introduced.
- Follow this operating rule: use the senior software engineer role as the working expectation for response quality and implementation judgment in this project.
- Follow this operating rule: use the skill-creator workflow when the user asks to create or update a skill that adds specialized knowledge, workflows, or tool integrations.
- Follow this operating rule: when a task is blocked by a follow-up question, keep it attached to the original task instead of splitting it into separate unrelated tasks.
- Follow this operating rule: when comparing AITrader and CodexClaw ideas, prioritize by impact so the response distinguishes high-value items from lower-value ones.
- Follow this operating rule: when schema changes require migration, apply the migration directly instead of handing off SQL files for manual execution.
- Follow this operating rule: when the custom option is selected, the active-penalties editor must open for updates.
- Follow this operating rule: when the user asks to consult another role such as coder or researcher, the strategist should delegate that work directly instead of asking the user questions that belong to the delegated role.
- Keep responses concise by default and avoid unnecessary process narration when token budget matters.

## PROMOTED RULES (EXPLICIT)

- 35 explicit rule(s) are listed above by behavior bucket.

## INFERRED RULES

- Do not duplicate the risk policy object in the config snapshot; present runtime/config values in a cleaner item-by-item format instead of raw arrays. (confidence: medium; source_count: 2)
- Do not expose a separate custom profile editor; editing should happen through the active-penalties controls instead. (confidence: strong; source_count: 4)
- Do not mirror the user's wording into the story description; rewrite the request into a clearer, interpreted summary. (confidence: strong; source_count: 2)
- Do not show wash-sale or tax-lot cards while the related position is still open; those cards should only appear once the position is closed. (confidence: strong; source_count: 2)
- Follow this operating rule: a skill-creator skill is available and should be used when adding or updating skills that extend the agent with specialized workflows or integrations. (confidence: medium; source_count: 1)
- Follow this operating rule: add a lineage-header indicator for whether the account is taxable or non-taxable so tax-card presence can be checked more easily. (confidence: strong; source_count: 2)
- Follow this operating rule: add a trade-card history view that only includes cards after a decision is made, and keep the original decision control visible but disabled in history. In planning, cards should remain active until decided; once decided, they move out of planning and into history. (confidence: strong; source_count: 3)
- Follow this operating rule: add a true terminal 'closed' state after execution; execution is not the final end state because positions can remain active through partial exits or roll actions until all related positions are finished. (confidence: strong; source_count: 2)
- Follow this operating rule: add the position type to trade cards and propagate it through the rest of the application where that trade metadata is displayed. (confidence: strong; source_count: 2)
- Follow this operating rule: allow entry and close intents to be canceled before they become trades. (confidence: strong; source_count: 2)
- Follow this operating rule: apply the same planning-vs-history visibility behavior to order intents and close intents while they are still transient and not yet executed. (confidence: medium; source_count: 2)
- Follow this operating rule: archive or clear out obsolete tasks when the user requests a reset so the workspace can start fresh. (confidence: medium; source_count: 2)
- Follow this operating rule: audit the mock lineage data end to end and fill in missing backward links for any object, not just the previously mentioned cards. (confidence: strong; source_count: 2)
- Follow this operating rule: avoid dense or repetitive layouts in this area; redesign it to reduce crowding and remove redundant elements. (confidence: strong; source_count: 2)
- Follow this operating rule: changes to active penalties must create an audit entry in the audit section; do not rely on the edit screen to show that history. (confidence: strong; source_count: 4)
- Follow this operating rule: compute trust score from the current mock data using the existing calculation logic, then update the displayed value so it matches the data. (confidence: strong; source_count: 4)
- Follow this operating rule: design the user interface as a comprehensive control center with pages for configuration, trade review, auditing, and system visibility so the operator can manage nearly every adjustable setting from the UI. (confidence: strong; source_count: 2)
- Follow this operating rule: for maximize/minimize controls, use a single toggle button only; the icon and label should switch between maximize and minimize, with no intermediate state. (confidence: strong; source_count: 2)
- Follow this operating rule: in audit trail rows, keep tag labels and values visually close together, and provide an expand control that reveals additional JSON details inline. (confidence: strong; source_count: 2)
- Follow this operating rule: keep KPI snapshot tiles visually aligned and consistent in size, and adjust tile placement when the layout looks uneven. (confidence: medium; source_count: 4)
- Follow this operating rule: keep hover interactions non-disruptive: buttons should not shift position on mouse-over; use a subtle color-lightening effect instead. (confidence: strong; source_count: 4)
- Follow this operating rule: keep penalty audit details out of the editing screen to avoid clutter; the audit screen is the only place they need to appear. (confidence: strong; source_count: 2)
- Follow this operating rule: keep runtime knobs focused on operational settings that belong inside the app; do not include schedule timing there because scheduling is handled externally by the agent. (confidence: strong; source_count: 2)
- Follow this operating rule: keep strategy selections consistent across strategy lab and commander center so both tabs expose the same available strategies for retrieval and display. (confidence: strong; source_count: 2)
- Follow this operating rule: keep the lineage view on the same screen when a user selects the lineage option; do not navigate into a separate lineage route behind the scenes. (confidence: strong; source_count: 2)
- Follow this operating rule: keep the strategist in a clarification loop until the request is sufficiently clear before creating a story; avoid opening a story too early. (confidence: strong; source_count: 2)
- Follow this operating rule: keep the visual layout of planning cards and history cards minimal by removing duplicated footer details; history should reuse the planning card presentation and only differ by showing the selected decision button. (confidence: strong; source_count: 2)
- Follow this operating rule: keep trade cards visible in planning regardless of creation date until a decision is made, and show the creation date on the card so older cards can still be understood. (confidence: strong; source_count: 3)
- Follow this operating rule: no coder task was opened, and the strategist is asking me questions that should be asking the coder. (confidence: medium; source_count: 1)
- Follow this operating rule: remove the generic status label from planning cards when all cards are effectively awaiting a decision; the planning view should present them as pending decision rather than using the removed staging label. (confidence: medium; source_count: 2)
- Follow this operating rule: remove the tax-lot profit and loss value from the tax lot node; keep that node as a tax-event indicator only. (confidence: strong; source_count: 2)
- Follow this operating rule: represent the strategist as a single visible story with linked subtasks or follow-ups, so the user can track the coder work outside the parent story more easily. (confidence: medium; source_count: 2)
- Follow this operating rule: show the risk policy panel and other detailed panels below the graph; do not rely only on condensed graph cards for that information. (confidence: strong; source_count: 3)
- Follow this operating rule: store mock records inside the database, not as external fixtures, and keep relationships between records intact so every page renders a coherent end-to-end scenario. (confidence: strong; source_count: 2)
- Follow this operating rule: support wash-sale and tax-lot behavior for rollover positions, and verify the wash-blocking rules against the current screens and data before assuming a block should exist. (confidence: medium; source_count: 4)
- Follow this operating rule: the CLI agent should invoke the shell with only the needed command, not pass an entire prompt payload into the command line. (confidence: strong; source_count: 4)
- Follow this operating rule: the strategist should decompose user requests into one or more stories based on the actual work needed, using its own judgment rather than relying on the user to pre-split the request. (confidence: medium; source_count: 2)
- Follow this operating rule: the user has repeatedly asked for senior-engineer-level handling of the AITrader codebase, so responses should assume an experienced software engineering audience. (confidence: strong; source_count: 2)
- Follow this operating rule: the user wants the assistant to review linked articles and comments thoroughly before answering, then summarize each link with the article title and practical ideas that could be applied to CodexClaw or AITrader. (confidence: strong; source_count: 2)
- Follow this operating rule: trade cards should use a smaller layout similar to the trade history card size, and the screen must preserve horizontal scrolling so hidden content remains reachable. (confidence: strong; source_count: 2)
- Follow this operating rule: treat each user story as the primary work item, with related tasks and follow-ups nested under it rather than spawning separate top-level stories for every clarification or dependency. (confidence: strong; source_count: 2)
- Follow this operating rule: treat the AITrader and CodexClaw workstreams separately when planning enhancements; keep AITrader ideas parked for later while focusing implementation detail on CodexClaw first. (confidence: strong; source_count: 2)
- Follow this operating rule: treat the penalty profile as incomplete unless a custom option exists that lets the user adjust individual knobs directly. (confidence: strong; source_count: 4)
- Follow this operating rule: treat the repository as governed by local agent instructions in the project root; consult them before making changes and follow any referenced skill files when relevant. (confidence: strong; source_count: 1)
- Follow this operating rule: treat the repository’s AGENTS.md and any referenced skill files as the primary local instructions before making changes. (confidence: strong; source_count: 1)
- Follow this operating rule: treat the repository’s AGENTS.md guidance as the active local instruction source, and follow any referenced skill files when a task matches their scope. (confidence: strong; source_count: 1)
- Follow this operating rule: treat the strategy lab as a DB-backed strategy configurator: users can edit strategy names and values per account, choose which strategy to load for viewing or editing, and maintain multiple inactive strategies alongside one active strategy for each live account type. (confidence: strong; source_count: 3)
- Follow this operating rule: treat the system as a swing-trading platform that mainly gathers signals during the day and prepares entries for the next session, while intraday actions are mostly reserved for urgent exits or black-swan protection. (confidence: strong; source_count: 2)
- Follow this operating rule: use a dark, polished dashboard style with subtle translucent glass-like menus, clean spacing, and an organized layout. (confidence: medium; source_count: 2)
- Follow this operating rule: use a friendlier presentation for JSON-heavy UI areas so users can inspect summarized fields in the app and only drill into raw JSON when needed. (confidence: strong; source_count: 4)
- Follow this operating rule: use a kanban view where each story is a single card and its tasks or follow-ups are visible when expanded. (confidence: medium; source_count: 2)
- Follow this operating rule: use realistic scenario data when populating the mock database so testing reflects actual product behavior before live data is introduced. (confidence: medium; source_count: 2)
- Follow this operating rule: use the senior software engineer role as the working expectation for response quality and implementation judgment in this project. (confidence: strong; source_count: 2)
- Follow this operating rule: use the skill-creator workflow when the user asks to create or update a skill that adds specialized knowledge, workflows, or tool integrations. (confidence: strong; source_count: 1)
- Follow this operating rule: when a task is blocked by a follow-up question, keep it attached to the original task instead of splitting it into separate unrelated tasks. (confidence: medium; source_count: 2)
- Follow this operating rule: when comparing AITrader and CodexClaw ideas, prioritize by impact so the response distinguishes high-value items from lower-value ones. (confidence: medium; source_count: 2)
- Follow this operating rule: when the custom option is selected, the active-penalties editor must open for updates. (confidence: strong; source_count: 2)
- Follow this operating rule: when the user asks to consult another role such as coder or researcher, the strategist should delegate that work directly instead of asking the user questions that belong to the delegated role. (confidence: strong; source_count: 4)

## SCOPE NOTES

- Applies only to this project.

## RELATED

- [[Ai Trader Recent]]
- [[Ai Trader Rules]]
