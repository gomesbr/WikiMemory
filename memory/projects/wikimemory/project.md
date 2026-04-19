---
type: project-memory
project: wikimemory
updated: 2026-04-19T04:21:45.680264Z
tags: [project/wikimemory, memory]
---

# 🧠 Wikimemory - Project Memory

## PURPOSE

- The project is designed to preserve provenance, stay incremental, and keep the raw source logs outside the repo. The raw logs remain the source of truth. Everything inside this repository is a derived artifact, control file, config, test, or generated knowledge output.
- Project context: Append-aware tracking 6-Filenames are system generated and won't change.
- Project context: The project’s memory pipeline is intended to convert raw session logs into normalized events, segmented work units, deterministic classifications, extracted knowledge, wiki pages, bootstrap memory, and audit findings while preserving provenance and keeping raw logs outside the repository.

## CORE COMPONENTS

- Use this architecture context: wikiMemory is a file-based memory pipeline for external Codex session logs.
- Use this architecture context: wikiMemory solves that by building a layered pipeline.
- Respect this constraint: use real data for testing instead of mocked fixtures when validating the pipeline.
- Use this architecture context: the pipeline should stay incremental and preserve provenance across stages instead of rebuilding or losing traceability.

## CURRENT ARCHITECTURE

- Use this architecture context: phase 1 for WikiMemory is the external source discovery and indexing layer, which should index session metadata and file locations without copying raw logs into the project.
- Use this architecture context: phase 2 should be migrated to a provenance-first design that stores pointers plus bounded canonical text instead of duplicating raw events, while keeping Phase 1 unchanged and preserving later phases where possible through lazy hydration.
- Use this architecture context: phase 7 should generate compact bootstrap memory from phase 5 items and phase 6 wiki manifests, using deterministic selection plus LLM compression, with provenance kept in a sidecar manifest rather than the main markdown.
- Use this architecture context: prefer generalizable architecture over one-off patches.
- Use this architecture context: the wiki model should remain usable even if the user chooses a destination other than Obsidian.
- Use this architecture context: the wiki synthesis stage should remain valid even if the storage or note-taking tool changes; keep the model tool-agnostic unless a specific integration is required.

## DESIGN PRINCIPLES

- Respect this constraint: bootstrap is hybrid but strictly compressive: - deterministic code selects, ranks, budgets, and structures the evidence - the LLM compresses only the selected evidence into short bullets - no new latent knowledge is created in Phase 7 - Provenance stays out of the main markdown body to save tokens.

## KEY CONSTRAINTS

- Respect this constraint: raw logs are the source of truth; repository contents should remain derived artifacts, configuration, tests, or generated outputs rather than primary session data.
- Respect this constraint: the WikiMemory system should support notifications so the user is aware of important events and can avoid planning code upgrades at the wrong time.
- Respect this constraint: after Phase 1 is planned, we will: * implement it * test it * validate it * approve it ONLY THEN we move to Phase 2.
- Respect this constraint: codex session logs contain a large amount of useful information, but they are difficult to reuse directly they are append-only raw traces, they mix user intent, agent reasoning, tool calls, code work, status chatter, and planning, they are not organized by project/domain knowledge, they are too large and noisy to load directly into future sessions.
- Respect this constraint: do not overwrite agent-authored markdown files; only append user-related information so existing user content is preserved.
- Respect this constraint: during the full-load loop, the process must monitor disk growth after each run and avoid exceeding the available storage budget.

## OPEN PROBLEMS

- Respect this constraint: return only: - what changed - why - files modified/created - commands to run for validation - If blocked, ask questions using numbered multiple-choice format: 1- A) ...

## RELATED

- [[Wikimemory Recent]]
- [[Wikimemory Rules]]
- [[Global User Rules]]
