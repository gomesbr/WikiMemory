---
type: project-rules
project: open-brain
updated: 2026-04-21T05:01:53.140725Z
tags: [project/open-brain, rules]
---

# Open Brain - Project Rules

## ALWAYS DO

- Benchmark/test cases and expected answers must be grounded in real DB/published evidence with provenance; synthetic expected answers are not allowed.
- Use JSON-based communication for agent-to-agent interactions.
- Prioritize quality over speed; avoid lower-quality shortcuts, and minimize repeated full re-ingests by preferring in-place corrective passes plus a final remediation pass.
- Answer contract must cite actor + timestamp + anchor + supporting context; if attribution is uncertain, state uncertainty explicitly and ask follow-up.
- Maintain continuous autonomous strategy-loop operation (including failed-group research/code-wave continuation) without waiting for user input, except agreed stop conditions.
- Enforce CPU safety: avoid sustained 100% utilization; if high CPU persists per guard policy, throttle services stepwise and stop loop at minimum caps with logging.
- Provide status updates whenever each strategy/experiment item finishes.
- Keep runtime DB schema in sync with latest code before smoke tests or handoff; stop services if needed, migrate/update, then restart cleanly.
- Scope improvements and generation to the whole published corpus/dataset rather than narrow domain-only/refill-only patches.
- Maintain diversity across source/conversation types and prioritize human conversations (WhatsApp individual/group) over assistant-centric threads.
- Runtime knobs should be UI-editable and DB-backed for routine operations, and every config change must be audit-logged with actor, timestamp/date, old/new values, and reason.
- Docker runtime must pass required embedding/provider env vars into `openbrain-api` (including `OPENAI_API_KEY`, `OPENAI_BASE_URL`, embedding mode/fallback, metadata provider settings) to prevent unintended fallback behavior.

## NEVER DO

- Apply confidence gating across all entity/artifact types; low-confidence outputs must not be promoted downstream until adjudicated.
- Never display secrets (application passwords, tokens, credentials) in commands/output shown to the user.
- Never use mock embeddings for production/backfills; run in OpenAI mode with no mock fallback, and if credits/tokens are exhausted, stop and notify the user.
- Avoid overbuilding domain-specific permanent tables; keep most interpretation logic in the agent loop with bounded context/thread reads and strong indexing.

## CONDITIONAL RULES

- When explicitly requested, perform in-depth research first (including user-provided materials/web), present learnings and an ordered experiment plan, then implement.
- For intelligence-dependent stages, use agent-driven adjudication/corrections and add agents where reasoning is needed instead of relying only on static rules.
- If timeout/infra failures dominate, fix infra first and validate on baseline (`S0`) before comparative strategy evaluation; if timeouts recur later, stop at that strategy, fix/retest, then resume.
- When user asks for capability changes, implement them directly; do not respond by only updating backlog documentation.
- When user is away, run and monitor pipeline continuously with periodic checks (including 3-minute watchdog cadence): detect stalls/failures, inspect rejects, fix invalid rejection causes, relaunch, and keep quality checks active.
- Synthesis answers must explicitly call out missing direct evidence, provide best indirect estimate with basis/components, include confidence/caveats, and ask a quick confirmation when appropriate.
- When ambiguity is detected, ask exactly one short, specific, open-ended clarification question and stop before final answering.
- When user requests analysis-only, do not make code changes unless explicitly asked.
- For WhatsApp content, separate quoted/tagged text from authored text (`@mentions` are references, not sender identity), and ensure evidence includes exact answer-bearing phrases with the directly answering row prioritized.
- Apply holistic retroactive fixes across existing active/calibration inventory when a failure class is found; do not ship one-off screenshot-specific patches.
- Clarify-first should trigger only for true missing-anchor queries; avoid unnecessary clarification when retrieval anchors/keywords are already sufficient.
- For the referenced fix loop, keep changes narrowly scoped to `src/v2_experiments.ts` unless explicitly requested otherwise.

## SCOPE NOTES

- Applies only to `open-brain` unless a rule explicitly says otherwise.
