---
type: project-rules
project: wikimemory
updated: 2026-04-19T13:07:42.179851Z
tags: [project/wikimemory, rules]
---

# ⚙️ Wikimemory - Project Rules

## ALWAYS DO

_None currently extracted._

## NEVER DO

- Do not replace existing agent markdown files; append new information to the user-owned markdown file so prior user content is preserved.
- Do not promote transient commands, progress chatter, or one-off runtime instructions into durable wiki knowledge; extraction should favor stable, generalizable content and suppress noise that only reflects the current interaction.

## CONDITIONAL RULES

- When developing a new Wikimemory version that is not yet in production use, do not preserve backward compatibility with the previous version by default. Treat the new version as a clean system unless the user explicitly asks for migration or compatibility support.
- the project should treat each memory entry as if the system is being evaluated from scratch, without assuming backward compatibility with an older version unless that is explicitly required.
- Validate memory and extraction changes against real data before treating them as correct.
- Prioritize the full-data run to be managed as an autonomous loop: run a phase or chunk, evaluate the result, fix issues holistically if needed, then continue without asking for intervention.
- during the full-data loop, the implementation must check disk growth after each run and avoid letting the corpus exceed the configured space cap.
- implement all remaining steps in sequence without pausing between them unless blocked.
- the extraction pipeline should favor useful candidate recall over overly strict filtering, because the log corpus is large and shallow output is a sign that the selection rules are too narrow.
- memory pages must be written so a new agent can understand every line without hidden context; if a line depends on missing background, it should be rewritten or removed.
- the WikiMemory system should be designed one phase at a time: ask clarifying questions first, refine assumptions with the user, then produce the detailed plan only after ambiguity is removed.
- for the WikiMemory project, treat external Codex session logs as immutable source data: discover them from configurable roots, index them without copying raw logs into the project, and support append-aware tracking.
- the initial WikiMemory scope is limited to three target projects, but the system should allow additional projects to be added later through configuration and then fully rescanned across the root history.
- the WikiMemory scheduler should run daily and include notification support so the user is aware of updates and can plan code changes accordingly.

## PROMOTED RULES (EXPLICIT)

- 44 explicit rule(s) are listed above by behavior bucket.

## INFERRED RULES

_None currently extracted._

## SCOPE NOTES

- Applies only to this project.

## RELATED

- [[Wikimemory Recent]]
- [[Wikimemory Rules]]
