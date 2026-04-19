---
type: project-memory
project: wikimemory
updated: 2026-04-19T04:35:36.294124Z
tags: [project/wikimemory, memory]
---

# 🧠 Wikimemory - Project Memory

## PURPOSE

- The project is designed to preserve provenance, stay incremental, and keep the raw source logs outside the repo. The raw logs remain the source of truth. Everything inside this repository is a derived artifact, control file, config, test, or generated knowledge output.
- Append-aware tracking 6-Filenames are system generated and won't change.
- The project’s memory pipeline is intended to convert raw session logs into normalized events, segmented work units, deterministic classifications, extracted knowledge, wiki pages, bootstrap memory, and audit findings while preserving provenance and keeping raw logs outside the repository.

## CORE COMPONENTS

- wikiMemory is a file-based memory pipeline for external Codex session logs.
- wikiMemory solves that by building a layered pipeline.
- use real data for testing instead of mocked fixtures when validating the pipeline.
- the pipeline should stay incremental and preserve provenance across stages instead of rebuilding or losing traceability.

## CURRENT ARCHITECTURE

- the source-discovery stage for WikiMemory is the external source discovery and indexing layer, which should index session metadata and file locations without copying raw logs into the project.
- the normalization stage should be migrated to a provenance-first design that stores pointers plus bounded canonical text instead of duplicating raw events, while keeping the source-discovery stage unchanged and preserving later phases where possible through lazy hydration.
- the bootstrap-memory stage should generate compact bootstrap memory from the knowledge-extraction stage items and the wiki-synthesis stage wiki manifests, using deterministic selection plus LLM compression, with provenance kept in a sidecar manifest rather than the main markdown.
- prefer generalizable architecture over one-off patches.
- the wiki model should remain usable even if the user chooses a destination other than Obsidian.
- the wiki synthesis stage should remain valid even if the storage or note-taking tool changes; keep the model tool-agnostic unless a specific integration is required.

## DESIGN PRINCIPLES

- bootstrap is hybrid but strictly compressive: - deterministic code selects, ranks, budgets, and structures the evidence - the LLM compresses only the selected evidence into short bullets - no new latent knowledge is created in the bootstrap-memory stage - Provenance stays out of the main markdown body to save tokens.

## KEY CONSTRAINTS

- raw logs are the source of truth; repository contents should remain derived artifacts, configuration, tests, or generated outputs rather than primary session data.
- Notify the user about notable pipeline events so maintenance work happens at appropriate times.
- after the source-discovery stage is planned, we will: * implement it * test it * validate it * approve it ONLY THEN we move to the normalization stage.
- codex session logs contain a large amount of useful information, but they are difficult to reuse directly they are append-only raw traces, they mix user intent, agent reasoning, tool calls, code work, status chatter, and planning, they are not organized by project/domain knowledge, they are too large and noisy to load directly into future sessions.
- do not overwrite agent-authored markdown files; only append user-related information so existing user content is preserved.
- during the load loop, the process must monitor disk growth after each run and avoid exceeding the available storage budget.

## OPEN PROBLEMS

_None currently extracted._

## RELATED

- [[Wikimemory Recent]]
- [[Wikimemory Rules]]
- [[Global User Rules]]
