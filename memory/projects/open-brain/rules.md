---
type: project-rules
project: open-brain
updated: 2026-04-19T13:07:41.786085Z
tags: [project/open-brain, rules]
---

# ⚙️ Open Brain - Project Rules

## ALWAYS DO

_None currently extracted._

## NEVER DO

- Do not narrow generation to only historically successful domains; the process should continue to work across the broader dataset without relying on user-provided examples.
- Do not use mocked embeddings for persisted data; embeddings must come from the real source content, and any mock data already inserted should be regenerated with the real embedding provider.
- Do not stop the group immediately when one strategy succeeds; continue running the remaining strategies in that group until the group finishes.
- Do not change code while the user is actively reviewing cases unless they explicitly ask for implementation changes.
- Do not modify the file currently under manual review; the user is inspecting the 'they' file and wants it left untouched during that review pass.
- Do not require the user to be present in a conversation for it to count as an actor interaction candidate.
- Do not limit duplicate cleanup to one status bucket; inspect and prune duplicates across the entire case set, including both reviewed and unreviewed records.
- Do not force the agent to answer from memory when the task is to produce retrieval-oriented subqueries; the agent should only return answers grounded in system evidence, not guesses.

## CONDITIONAL RULES

- When developing a new Open Brain version that is not yet in production use, do not preserve backward compatibility with the previous version by default. Treat the new version as a clean system unless the user explicitly asks for migration or compatibility support.
- backward compatibility is not required for this OpenBrain branch; API, UI, and type changes can be breaking because the product is still experimental.
- treat names marked with a leading tilde as non-suspicious once the user confirms they are valid contacts, and remove the specific group chat entry the user identified from the suspicious list.
- after the initial Mission Control redesign, continue with the the normalization stage polish pass to address the empty-feeling layout and improve density, fetch timing, caching, keyboard navigation, and responsive side-panel behavior.
- the import script should be adjusted to process the newly available Grok export archive as an additional source input for the same ingestion flow.
- Prioritize the memory system sized for the final combined dump, then multiplied by roughly ten for long-term growth, and wants the architecture reconsidered now if the current database choice will not scale to that horizon.
- Prioritize a comprehensive life taxonomy and analysis-lens model covering many domains, not a narrow subset, so future design should keep the schema extensible for broad personal analytics.
- the frontend should be optimized for visual exploration, with graphs and charts as primary presentation modes for insights.
- use a single consistent date representation when inserting imported records into the database to avoid compatibility problems.
- add a percentage-complete column to the source breakdown view and keep the per-source summary aligned with the existing row counts.
- ensure date values and date formats are inserted consistently across every source type, and add a sanity check to catch malformed date handling.
- when a load finishes, start the aggregation job even if some rows failed during the load; do not block on those row-level failures.

## PROMOTED RULES (EXPLICIT)

- 130 explicit rule(s) are listed above by behavior bucket.

## INFERRED RULES

_None currently extracted._

## SCOPE NOTES

- Applies only to this project.

## RELATED

- [[Open Brain Recent]]
- [[Open Brain Rules]]
