---
type: project-memory
project: wikimemory
updated: 2026-04-19T02:18:21.170067Z
tags: [project/wikimemory, memory]
---

# 🧠 Wikimemory - Project Memory

## PURPOSE

- Its job is to turn raw `.jsonl` session traces into structured normalized events, segmented conversational/work units, deterministic domain classification, extracted knowledge items, synthesized wiki pages, compact bootstrap memory for future agents. <!-- c1bbd2a92d11ec58 -->
- The project is designed to preserve provenance, stay incremental, and keep the raw source logs outside the repo. The raw logs remain the source of truth. Everything inside this repository is a derived artifact, control file, config, test, or generated knowledge output. <!-- 012baf20042f73a9 -->
- WikiMemory is a file-based memory pipeline for external Codex session logs. <!-- fe4676a51c699ae4 -->

## CORE COMPONENTS

- WikiMemory is a file-based memory pipeline for external Codex session logs. <!-- fe4676a51c699ae4 -->
- WikiMemory solves that by building a layered pipeline <!-- d524110090917d64 -->

## CURRENT ARCHITECTURE

- The project is designed to preserve provenance, stay incremental, and keep the raw source logs outside the repo. The raw logs remain the source of truth. Everything inside this repository is a derived artifact, control file, config, test, or generated knowledge output. <!-- 012baf20042f73a9 -->
- WikiMemory is a file-based memory pipeline for external Codex session logs. <!-- fe4676a51c699ae4 -->
- WikiMemory solves that by building a layered pipeline <!-- d524110090917d64 -->

## DESIGN PRINCIPLES

- Its job is to turn raw `.jsonl` session traces into structured normalized events, segmented conversational/work units, deterministic domain classification, extracted knowledge items, synthesized wiki pages, compact bootstrap memory for future agents. <!-- c1bbd2a92d11ec58 -->
- The project is designed to preserve provenance, stay incremental, and keep the raw source logs outside the repo. The raw logs remain the source of truth. Everything inside this repository is a derived artifact, control file, config, test, or generated knowledge output. <!-- 012baf20042f73a9 -->

## KEY CONSTRAINTS

- Codex session logs contain a large amount of useful information, but they are difficult to reuse directly they are append-only raw traces, they mix user intent, agent reasoning, tool calls, code work, status chatter, and planning, they are not organized by project/domain knowledge, they are too large and noisy to load directly into future sessions. <!-- 7a345702576c5779 -->

## OPEN PROBLEMS

- No open project-level problems extracted yet.

## RELATED

- [[Wikimemory Recent]]
- [[Wikimemory Rules]]
- [[Global User Rules]]
