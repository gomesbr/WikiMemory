---
type: project-rules
project: wikimemory
updated: 2026-04-19T04:35:36.332952Z
tags: [project/wikimemory, rules]
---

# ⚙️ Wikimemory - Project Rules

## ALWAYS DO

_None currently extracted._

## NEVER DO

_None currently extracted._

## CONDITIONAL RULES

- the autonomous corpus-load stage is intended as an autonomous full-corpus load loop that runs phases repeatedly without user intervention, checks each phase result, and either advances or revises the code holistically before retrying.
- for the WikiMemory project, only plan one phase at a time: ask clarifying questions first, then refine assumptions, and only then produce the detailed phase plan.
- the initial knowledge-building scope is limited to three projects, but the system should allow additional projects later through configuration and then run a full historical scan plus ongoing tracking for them.
- treat the audit stage as the validation/audit stage for artifacts from earlier phases. It should compare manifests and state for contradictions, duplicates, stale entries, missing provenance, and drift between wiki and bootstrap outputs, without parsing rendered markdown directly.
- the daily-refresh stage is the daily orchestration entrypoint for phases 1 through 8. It should choose full, scoped, or skipped refreshes based on upstream changes and config or schema invalidation.
- the README should be expanded into a detailed end-to-end project guide so another model can understand the system from that file alone.
- keep one representative input log in the repository as an example artifact that shows the source-data structure and content variety for downstream model understanding.
- use the provided Codex prompt template when handing off implementation work: concise output only, no reasoning narration, and multiple-choice questions if blocked.
- expand the repository README so it explains the project end to end in enough detail for another model to understand the system from that file alone.
- add one representative sample input log file to the repository so downstream tooling can inspect the source-data structure and content patterns.
- use numbered multiple-choice questions for any clarification requests so the user can answer with minimal typing.
- Prioritize the wiki pipeline to stop promoting transient commands, narration, and runtime-local instructions into durable wiki knowledge.

## PROMOTED RULES (EXPLICIT)

- 11 explicit rule(s) are listed above by behavior bucket.

## INFERRED RULES

_None currently extracted._

## SCOPE NOTES

- Applies only to this project.

## RELATED

- [[Wikimemory Recent]]
- [[Wikimemory Rules]]
