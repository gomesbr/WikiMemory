---
type: project-memory
project: wikimemory
updated: 2026-04-19T13:07:42.075807Z
tags: [project/wikimemory, memory]
---

# 🧠 Wikimemory - Project Memory

## PURPOSE

- The project is designed to preserve provenance, stay incremental, and keep the raw source logs outside the repo. The raw logs remain the source of truth. Everything inside this repository is a derived artifact, control file, config, test, or generated knowledge output.
- Append-aware tracking 6-Filenames are system generated and won't change.
- Keep the system focused on making large Codex trace logs reusable by separating mixed content into structured project knowledge instead of loading raw traces directly.

## CORE COMPONENTS

- it is a pipeline flaw: extracted statements can be rendered into the wrong section before proving they are standalone, role-correct, and useful to a new agent.
- wikiMemory is a file-based memory pipeline for external Codex session logs.
- wikiMemory solves that by building a layered pipeline.
- build the pipeline to preserve provenance and support incremental processing from raw logs through normalized events, segmented units, classification, knowledge extraction, wiki synthesis, bootstrap memory, and audit outputs.
- prefer generalizable architecture over one-off patches.

## CURRENT ARCHITECTURE

- roles: `purpose`, `architecture`, `constraint`, `rule`, `recent_state`, `decision`, `lesson`, `discard`.

## DESIGN PRINCIPLES

- bootstrap is hybrid but strictly compressive: - deterministic code selects, ranks, budgets, and structures the evidence - the LLM compresses only the selected evidence into short bullets - no new latent knowledge is created in the bootstrap-memory stage - Provenance stays out of the main markdown body to save tokens.

## KEY CONSTRAINTS

- after the source-discovery stage is planned, we will: * implement it * test it * validate it * approve it ONLY THEN we move to the normalization stage.
- codex session logs contain a large amount of useful information, but they are difficult to reuse directly they are append-only raw traces, they mix user intent, agent reasoning, tool calls, code work, status chatter, and planning, they are not organized by project/domain knowledge, they are too large and noisy to load directly into future sessions.
- high signal only.
- keep Phases 3-9 behaviorally the same where possible, but teach them to lazily hydrate raw events through a shared resolver only when bounded the normalization stage text is insufficient.
- keep the current phase structure and page model, but harden the knowledge-extraction stage extraction, add strict wiki eligibility/ranking, suppress empty pages, and add audit checks that fail on durable-rule poll.
- only new data into existing files and/or new files 5-Yes, it can.

## OPEN PROBLEMS

_None currently extracted._

## RELATED

- [[Wikimemory Recent]]
- [[Wikimemory Rules]]
- [[Global User Rules]]
