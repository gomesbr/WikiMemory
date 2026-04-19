---
type: project-rules
project: wikimemory
updated: 2026-04-19T04:21:45.687252Z
tags: [project/wikimemory, rules]
---

# ⚙️ Wikimemory - Project Rules

## ALWAYS DO

- No always-do rules selected yet.

## NEVER DO

- No never-do rules selected yet.

## CONDITIONAL RULES

- Follow this operating rule: add one representative sample input log file to the repository so downstream tooling can inspect the source-data structure and content patterns.
- Follow this operating rule: carry out all remaining steps in sequence without pausing between them.
- Follow this operating rule: expand the repository README so it explains the project end to end in enough detail for another model to understand the system from that file alone.
- Follow this operating rule: for the WikiMemory project, only plan one phase at a time: ask clarifying questions first, then refine assumptions, and only then produce the detailed phase plan.
- Follow this operating rule: keep one representative input log in the repository as an example artifact that shows the source-data structure and content variety for downstream model understanding.
- Follow this operating rule: phase 10 is intended as an autonomous full-corpus load loop that runs phases repeatedly without user intervention, checks each phase result, and either advances or revises the code holistically before retrying.
- Follow this operating rule: phase 2 should avoid duplicating the full raw corpus when a more storage-efficient pointer-based design is possible; the user is concerned about unnecessary replication before knowledge compression.
- Follow this operating rule: phase 2 should produce a lossless normalized artifact from committed JSONL events, preserving unknown event types as generic normalized records and surfacing them in reporting and audit logs.
- Follow this operating rule: phase 3 should reconstruct session flow and create non-overlapping segments from Phase 2 artifacts, while keeping labels, durable knowledge, and human summaries out of scope.
- Follow this operating rule: phase 4 should use a deterministic classifier to assign segments into the defined domain buckets, including a fallback for mixed project/global content.
- Follow this operating rule: phase 5 should extract structured knowledge deterministically for v1, keep the schema compatible with later LLM-based extraction, and attach stable target metadata for wiki or other destinations.
- Follow this operating rule: phase 9 is the daily orchestration entrypoint for phases 1 through 8. It should choose full, scoped, or skipped refreshes based on upstream changes and config or schema invalidation.
- Follow this operating rule: the README should be expanded into a detailed end-to-end project guide so another model can understand the system from that file alone.
- Follow this operating rule: the initial knowledge-building scope is limited to three projects, but the system should allow additional projects later through configuration and then run a full historical scan plus ongoing tracking for them.
- Follow this operating rule: the user wants the wiki pipeline to stop promoting transient commands, narration, and runtime-local instructions into durable wiki knowledge.
- Follow this operating rule: the workspace includes agent guidance in AGENTS.md, and the assistant should follow those local workspace preferences when operating in this repo.
- Follow this operating rule: treat Phase 8 as the validation/audit stage for artifacts from earlier phases. It should compare manifests and state for contradictions, duplicates, stale entries, missing provenance, and drift between wiki and bootstrap outputs, without parsing rendered markdown directly.
- Follow this operating rule: use numbered multiple-choice questions for any clarification requests so the user can answer with minimal typing.
- Follow this operating rule: use the provided Codex prompt template when handing off implementation work: concise output only, no reasoning narration, and multiple-choice questions if blocked.

## PROMOTED RULES (EXPLICIT)

- 11 explicit rule(s) are listed above by behavior bucket.

## INFERRED RULES

- Follow this operating rule: carry out all remaining steps in sequence without pausing between them. (confidence: strong; source_count: 3)
- Follow this operating rule: phase 2 should avoid duplicating the full raw corpus when a more storage-efficient pointer-based design is possible; the user is concerned about unnecessary replication before knowledge compression. (confidence: strong; source_count: 3)
- Follow this operating rule: phase 2 should produce a lossless normalized artifact from committed JSONL events, preserving unknown event types as generic normalized records and surfacing them in reporting and audit logs. (confidence: strong; source_count: 2)
- Follow this operating rule: phase 3 should reconstruct session flow and create non-overlapping segments from Phase 2 artifacts, while keeping labels, durable knowledge, and human summaries out of scope. (confidence: strong; source_count: 1)
- Follow this operating rule: phase 4 should use a deterministic classifier to assign segments into the defined domain buckets, including a fallback for mixed project/global content. (confidence: strong; source_count: 1)
- Follow this operating rule: phase 5 should extract structured knowledge deterministically for v1, keep the schema compatible with later LLM-based extraction, and attach stable target metadata for wiki or other destinations. (confidence: strong; source_count: 1)
- Follow this operating rule: the user wants the wiki pipeline to stop promoting transient commands, narration, and runtime-local instructions into durable wiki knowledge. (confidence: strong; source_count: 6)
- Follow this operating rule: the workspace includes agent guidance in AGENTS.md, and the assistant should follow those local workspace preferences when operating in this repo. (confidence: medium; source_count: 1)

## SCOPE NOTES

- Applies only to this project.

## RELATED

- [[Wikimemory Recent]]
- [[Wikimemory Rules]]
