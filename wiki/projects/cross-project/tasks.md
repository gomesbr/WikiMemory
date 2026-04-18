---
title: "Cross-Project - Tasks"
page_id: "projects/cross-project/tasks"
domain: "cross-project"
bucket: "tasks"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:10:53.151209Z
source_count: 3
claim_count: 6
tags:
  - wikimemory
  - cross-project
  - cross-project
  - bucket
  - tasks
---
# Cross-Project - Tasks

Navigation: [[projects/cross-project/index|Cross-Project]] | [[projects/cross-project/communication-preferences|Cross-Project - Communication Preferences]] | [[projects/cross-project/workflow-rules|Cross-Project - Workflow Rules]] | [[projects/cross-project/architecture|Cross-Project - Architecture]] | [[projects/cross-project/code-map|Cross-Project - Code Map]] | [[projects/cross-project/current-state|Cross-Project - Current State]] | [[projects/cross-project/outcomes|Cross-Project - Outcomes]] | [[projects/cross-project/failures|Cross-Project - Failures]] | [[projects/cross-project/decisions|Cross-Project - Decisions]] | [[projects/cross-project/next-steps|Cross-Project - Next Steps]] | [[projects/cross-project/open-questions|Cross-Project - Open Questions]]
Related Domains: [[projects/ai-scientist/index|AI Scientist]], [[projects/ai-trader/index|AI Trader]], [[projects/open-brain/index|Open Brain]]

## Summary
- The task requests include various implementations and fixes related to the project. [latent: project_identity_and_scope] [confidence: inferred][^claim-1]
- Validation tests have been conducted to ensure the functionality of the implemented changes. [latent: current_state_synthesis] [confidence: inferred][^claim-2]
- There are ongoing efforts to improve the extraction validator and address live error counts. [latent: implicit_next_steps] [confidence: inferred][^claim-3]
- The project is currently focused on live-corpus validation against fixed sample sets. [latent: workflow_norms] [confidence: inferred][^claim-4]

## Task Request
- The plan for implementation has been outlined and is currently active. [latent: project_identity_and_scope] [confidence: inferred][^claim-5]
- The pointer-first Phase 2 migration has been successfully implemented, addressing storage issues. [latent: architecture_synthesis] [confidence: inferred][^claim-6]

### Canonical Items
- PLEASE IMPLEMENT THIS PLAN: [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-1]
- that’s fixed. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-2]
- - Implemented the pointer-first Phase 2 migration. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-3]
- - This fixes the root storage problem: Phase 2 no longer mirrors the raw corpus while preserving exact provenance and on-demand recovery. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-4]
- - Validation passed: `73` local tests green (`1` skipped live test by default), and the env-gated real-data live suite passed on the fixed representative sample set. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-5]
- I’ve patched the real-data failure mode and added a regression test. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-6]
- I’m adding a narrow regression test so the live-data fix stays locked: repeated `next_step` items on the same file/path should warn, not fail the audit. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-7]
- I’m fixing that policy at the audit layer and tightening the generic `current_state` subject key one last time. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-8]
- The live error count is still dropping, which means the fix path is right. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-9]
- I’m fixing that at the extraction validator instead of weakening the live test. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-10]
- The extraction validator fix is in. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-11]
- I’m doing the opt-in live-corpus validation now against the fixed real sample set with temp outputs and stubbed LLM calls. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-12]
- That keeps the fix targeted instead of guessing. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-13]
- I’m fixing that by carrying exact total text length as metadata instead of weakening the segmentation logic. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-14]
- I’m checking whether that’s a real behavior change from the new bounded text and fixing it at the segmentation layer, not by loosening the expectation blindly. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-15]
- I’m making the extraction tests use the temp source-roots config end to end, then adding one regression where the signal exists only past the bounded Phase 2 text cutoff. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-16]
- It will copy only the fixed real sample files into a temp root, so it exercises real data without touching the whole corpus or inflating disk usage. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-17]
- I’m adding the opt-in live-corpus suite now. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-18]
- I’m editing Phase 2 now: dropping persisted `raw_event`, adding event digests and bounded text, and switching validation to the new resolver. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-19]
- fixed [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-20]
- I’ve got the fixed source IDs. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-21]
- I’m locking the fixed live sample manifest now so the new real-data suite runs on stable real files instead of broad corpus scans. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-22]
- I’m checking the schema catalog and existing state/version boundaries now so the implementation lands with the right invalidation behavior. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-23]
- I’m implementing the pointer-first migration now. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-24]
- - `session.json` adds: [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-25]
- - Add a fixed live-data sample manifest for robust real-data tests. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-26]
- - Add a shared `RawEventResolver` used across Phases 2-6. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-27]
- - Add an opt-in robust live-corpus test suite that runs against a fixed representative real-data sample with temp outputs and stubbed LLM calls. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-28]
- - add helper seam so future heuristics can hydrate only flagged/truncated events [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-29]
- - Chosen real-data testing mode: env-gated fixed live sample, not dynamic auto-sampling. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-30]
- - New config fixture with explicit representative real source IDs [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-31]
- - No persistent raw-event cache is added in v1 [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-32]
- - Prefer optional added metadata over shape churn. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-33]
- - runs the fixed sample set through Phases 1-8 using temp outputs [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-34]
- - Update downstream phases to consume the new Phase 2 contract. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-35]
- - Added lock handling, partial-failure recording, scoped refresh propagation, and aggregated refresh reporting [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-36]
- - Fixed refresh delta logic so `new -> stable` / `growing -> stable` lifecycle churn does not trigger unnecessary downstream work [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-37]
- - The delta fix generalizes beyond the sample by preventing downstream rebuilds on non-semantic discovery status changes while still propagating real source changes [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-38]
- One remaining failure is just the failure-injection test not actually reaching `classify` after the no-op skip fix. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-39]
- The delta fix is in. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-40]
- I’m fixing those first. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-41]
- adding [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-42]
- I’m adding the refresh tests now around the real phase chain with fake wiki/bootstrap synthesis. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-43]
- I’m adding `refresh.py` now, then I’ll wire the CLI and build a focused orchestration test matrix around real phase calls with fake LLMs. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-44]
- ## Implementation Changes [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-45]
- - `--source-id` updates only that source’s downstream slice [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-46]
- - Add a stale-safe lock so overlapping scheduled runs fail immediately unless the existing lock is clearly stale. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-47]
- - refresh updates `heartbeat_at` before each phase and after each phase [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-48]
- I’m adding a focused test matrix now for stale warnings, contradictions, provenance/drift errors, and scoped audit refresh so we can validate the stage before touching docs. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-49]
- - Fixed bootstrap staging and budget trimming so high-priority content survives within char limits [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-50]
- - Phase 7 is implemented end-to-end: extracted items + wiki manifests -> compact bootstrap markdown + sidecar manifest + state/run/audit logs [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-51]
- I’m patching the staging bug and adding a focused bootstrap test suite against the existing sample pipeline. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-52]
- add_argument [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-53]
- I’m adding the smallest targeted test coverage and repo wiring now so we can validate bootstrap without broad churn. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-54]
- Implementing Phase 7 now. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-55]
- I’m wiring tests and the last repo updates, then I’ll validate the bootstrap pipeline end-to-end locally. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-56]
- I’m adding the Phase 7 tests around the same sample-first harness used by wiki generation. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-57]
- I’m running a syntax pass now before I add the bootstrap tests. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-58]
- I’m adding the new module and config now, then I’ll hook the CLI/tests after the core pipeline is in place. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-59]
- I’m checking the ignore and packaging files before I add the new generated tree so I don’t leave Phase 7 half-wired. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-60]
- The index-page packet exposed all domain item ids to synthesis, but only preview items were actually renderable on the page, so citation enrichment crashed on real data. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-61]
- I’m fixing the wiki sample run now and will only report the result. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-62]
- - Added wiki outputs under `wiki/` plus manifest/state/audit support: [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-63]
- - This adds the missing human-facing layer on top of extracted knowledge: deterministic page structure plus bounded OpenAI-backed synthesis with claim manifests and provenance. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-64]
- added [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-65]
- One small usability gap showed up in the docs: the wiki phase now has a real OpenAI runtime dependency, so I’m adding the env var note before I wrap. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-66]
- I’m fixing that and then adding a focused `test_wiki.py` file that exercises the full discovery→wiki path with mocked synthesis. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-67]
- Phase 6 is partially scaffolded, and I’m tightening it by adding the wiki test coverage and then validating the full pipeline end to end. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-68]
- I’m adding the Phase 6 tests now. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-69]
- I’m doing a tight compile check before I add the wiki tests so we catch any structural issues in the new module first, then I’ll use the tests to harden the behavior around citations, manifests, and incremental rebuilds. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-70]
- I’ve got the implementation shape locked now: new wiki stage, config, page manifests, and an OpenAI-backed structured synthesis layer that can be patched in tests. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-71]
- I’m grounding the Phase 6 implementation against the current extraction/state model before I touch files. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-72]
- - folder naming conventions optimized for vault browsing [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-73]
- - later you can add `plain-markdown`, `mkdocs`, `docsify`, `html`, etc. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-74]
- Examples: prefers concise answers, dislikes unrelated refactors, wants phase-by-phase planning, wants clarification before planning, prefers provenance, prefers implementation over speculation. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-75]
- Examples: the user consistently optimizes for maintainability, auditability, minimal drift, and incremental correctness, even if each session phrases that differently. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-76]
- Examples: what the likely next implementation or validation action is, when it is implied by the work history rather than explicitly stated as “next step”. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-77]
- - Implemented deterministic item extraction for the Phase 5 taxonomy, with: [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-78]
- This closes the root capability gap between “classified segments” and “usable memory artifacts.” Instead of pushing raw segments straight into future wiki/bootstrap phases, the system now creates stable, provenance-backed knowledge items that can be merged,... [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-79]
- I’m adding the Phase 5 test file now, with the scenarios that matter most for later phases: mixed-domain extraction, dedupe/merge, code locations, weak-signal skips, conflicts, supersession, sample scoping, version invalidation, and tombstones. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-80]

## Sources
[^claim-1]: items cross-project:task_request:017361725bf6cd20, cross-project:task_request:8145db8fc7be9474, cross-project:task_request:9ce1808b659f8dec, cross-project:task_request:7b56a9c9424b23aa; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5695-5697; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20924-20924; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4240-4244; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4231-4235; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4231-4235
[^claim-2]: items cross-project:task_request:3cbb0a3d98312cf8, cross-project:task_request:2f58fd9289a86d2d, cross-project:task_request:b3a5d9c347a4ddc3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4231-4235; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4174-4187; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4161-4173
[^claim-3]: items cross-project:task_request:96dcb5b8aafdb6bc, cross-project:task_request:b3d4cd8509eef6c3, cross-project:task_request:ffca5d41ba98499d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4111-4124; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4097-4105; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4019-4037
[^claim-4]: items cross-project:task_request:6299549b7c5077ec, cross-project:task_request:03ccfc41997200d3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4019-4037; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3981-3996
[^claim-5]: items cross-project:task_request:017361725bf6cd20; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5695-5697; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20924-20924
[^claim-6]: items cross-project:task_request:9ce1808b659f8dec; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4231-4235
[^item-task_request-1]: items cross-project:task_request:017361725bf6cd20; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5695-5697; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20924-20924
[^item-task_request-2]: items cross-project:task_request:8145db8fc7be9474; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4240-4244
[^item-task_request-3]: items cross-project:task_request:9ce1808b659f8dec; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4231-4235
[^item-task_request-4]: items cross-project:task_request:7b56a9c9424b23aa; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4231-4235
[^item-task_request-5]: items cross-project:task_request:3cbb0a3d98312cf8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4231-4235
[^item-task_request-6]: items cross-project:task_request:2f58fd9289a86d2d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4174-4187
[^item-task_request-7]: items cross-project:task_request:b3a5d9c347a4ddc3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4161-4173
[^item-task_request-8]: items cross-project:task_request:96dcb5b8aafdb6bc; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4111-4124
[^item-task_request-9]: items cross-project:task_request:b3d4cd8509eef6c3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4097-4105
[^item-task_request-10]: items cross-project:task_request:ffca5d41ba98499d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4019-4037
[^item-task_request-11]: items cross-project:task_request:6299549b7c5077ec; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4019-4037
[^item-task_request-12]: items cross-project:task_request:03ccfc41997200d3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3981-3996
[^item-task_request-13]: items cross-project:task_request:3925534a9d65b7a4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3981-3996
[^item-task_request-14]: items cross-project:task_request:cbbb05e9292764d7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3954-3964
[^item-task_request-15]: items cross-project:task_request:ab08a4f54162a6ce; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3939-3947
[^item-task_request-16]: items cross-project:task_request:ad9dffc172e5e044; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3908-3918
[^item-task_request-17]: items cross-project:task_request:f2c56f9d12d2429b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3887-3892
[^item-task_request-18]: items cross-project:task_request:126bf913b3f510a6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3887-3892
[^item-task_request-19]: items cross-project:task_request:e833fffca75ba405; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3765-3770
[^item-task_request-20]: items cross-project:task_request:432616184f4f7819; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3758-3759
[^item-task_request-21]: items cross-project:task_request:e88e13a2c751bdaf; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3758-3759
[^item-task_request-22]: items cross-project:task_request:bc364fd3904a0e89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3735-3751
[^item-task_request-23]: items cross-project:task_request:2c2304b80ede46f5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3640-3651
[^item-task_request-24]: items cross-project:task_request:112f9bdd240802a6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3627-3638
[^item-task_request-25]: items cross-project:task_request:5f95a908d5dd9c68; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-task_request-26]: items cross-project:task_request:e70246a111476ecc; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-task_request-27]: items cross-project:task_request:4a8fc0211d14e8d7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-task_request-28]: items cross-project:task_request:6e40935c6cbed875; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-task_request-29]: items cross-project:task_request:30b0fa08d9da9fbc; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-task_request-30]: items cross-project:task_request:1c5acb3251623ed3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-task_request-31]: items cross-project:task_request:9ac0d72faaa58d9a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-task_request-32]: items cross-project:task_request:c88ce4a90b27690d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-task_request-33]: items cross-project:task_request:ad2f492baa1c71f7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-task_request-34]: items cross-project:task_request:937259459c140eb4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-task_request-35]: items cross-project:task_request:39292760416886ab; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-task_request-36]: items cross-project:task_request:230a0cfc710408ef; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3432-3437
[^item-task_request-37]: items cross-project:task_request:cfd489db2169aef5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3432-3437
[^item-task_request-38]: items cross-project:task_request:8dada2f09470ab3e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3432-3437
[^item-task_request-39]: items cross-project:task_request:8d38d4a7886990ef; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3394-3401
[^item-task_request-40]: items cross-project:task_request:4521f89838b23ef2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3386-3393; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3394-3401
[^item-task_request-41]: items cross-project:task_request:870cee57d5636643; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3288-3311
[^item-task_request-42]: items cross-project:task_request:8f74563b1ab9708e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 835-836; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2702-2703; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3271-3272
[^item-task_request-43]: items cross-project:task_request:c246dfd61c361747; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3271-3272
[^item-task_request-44]: items cross-project:task_request:cf4c702f7d0699a7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3225-3226
[^item-task_request-45]: items cross-project:task_request:ffa4e5da689f8ee3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-task_request-46]: items cross-project:task_request:1a3590e4cea4b114; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-task_request-47]: items cross-project:task_request:a3e6c19335bb6ef6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-task_request-48]: items cross-project:task_request:dbe3bb29a6833449; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-task_request-49]: items cross-project:task_request:9d81406d7e95eb45; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3100-3101
[^item-task_request-50]: items cross-project:task_request:21bd0cc6ec74771e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2912-2917
[^item-task_request-51]: items cross-project:task_request:5bff201aa4476eba; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2912-2917
[^item-task_request-52]: items cross-project:task_request:bf7b34eadb087392; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2831-2847
[^item-task_request-53]: items cross-project:task_request:635c640d1be91164; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2804-2811
[^item-task_request-54]: items cross-project:task_request:66c04fcd14726de3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2779-2790
[^item-task_request-55]: items cross-project:task_request:3f958672eefa5945; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2763-2777
[^item-task_request-56]: items cross-project:task_request:f3f6bf2e453f3e80; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2763-2777
[^item-task_request-57]: items cross-project:task_request:667979049796f080; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2742-2753
[^item-task_request-58]: items cross-project:task_request:0f171ef84f0aba3e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2742-2753
[^item-task_request-59]: items cross-project:task_request:e66c1df5b5cfbcc7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2702-2703
[^item-task_request-60]: items cross-project:task_request:e98af1089549d919; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2678-2700
[^item-task_request-61]: items cross-project:task_request:3f9eb2a641c416df; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2362-2368
[^item-task_request-62]: items cross-project:task_request:8a881afa58715f7a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2342-2350
[^item-task_request-63]: items cross-project:task_request:fac3b30ac1cb4323; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1593-1600; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1601-1605
[^item-task_request-64]: items cross-project:task_request:c633f156278ab6f2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1593-1600; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1601-1605
[^item-task_request-65]: items cross-project:task_request:2c6ff262a33dde01; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1601-1605
[^item-task_request-66]: items cross-project:task_request:b3c186d24dc8f55f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1593-1600
[^item-task_request-67]: items cross-project:task_request:a650629a41842997; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1552-1558
[^item-task_request-68]: items cross-project:task_request:535b295e6260ab75; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1489-1500
[^item-task_request-69]: items cross-project:task_request:f5c80a866aebaa6b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1471-1479
[^item-task_request-70]: items cross-project:task_request:b107f2666a31df00; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1448-1469
[^item-task_request-71]: items cross-project:task_request:0f74e705cb1e400a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1408-1409
[^item-task_request-72]: items cross-project:task_request:35ff1583999139e2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1387-1398
[^item-task_request-73]: items cross-project:task_request:d688dec2bfb20d47; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1340-1347
[^item-task_request-74]: items cross-project:task_request:cb1dd6559c08a9ab; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1340-1347
[^item-task_request-75]: items cross-project:task_request:5d0b000565b59394; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-task_request-76]: items cross-project:task_request:1fe5b7cc946941f1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-task_request-77]: items cross-project:task_request:28236b681d7a5be9; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-task_request-78]: items cross-project:task_request:231b2be6e2f0ba66; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1275-1280; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1281-1285
[^item-task_request-79]: items cross-project:task_request:6c09e8ed0fe774e0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1275-1280; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1281-1285
[^item-task_request-80]: items cross-project:task_request:849fcb439ff29f76; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1181-1201
