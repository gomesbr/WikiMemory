---
title: "Open Brain - Tasks"
page_id: "projects/open-brain/tasks"
domain: "open-brain"
bucket: "tasks"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:28:24.679565Z
source_count: 4
claim_count: 6
tags:
  - wikimemory
  - project
  - open-brain
  - bucket
  - tasks
---
# Open Brain - Tasks

Navigation: [[projects/open-brain/index|Open Brain]] | [[projects/open-brain/communication-preferences|Open Brain - Communication Preferences]] | [[projects/open-brain/workflow-rules|Open Brain - Workflow Rules]] | [[projects/open-brain/architecture|Open Brain - Architecture]] | [[projects/open-brain/code-map|Open Brain - Code Map]] | [[projects/open-brain/current-state|Open Brain - Current State]] | [[projects/open-brain/outcomes|Open Brain - Outcomes]] | [[projects/open-brain/failures|Open Brain - Failures]] | [[projects/open-brain/decisions|Open Brain - Decisions]] | [[projects/open-brain/next-steps|Open Brain - Next Steps]] | [[projects/open-brain/open-questions|Open Brain - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- The task requests emphasize implementing plans with minimal complexity and avoiding unnecessary changes. [latent: workflow_norms] [confidence: inferred][^claim-1]
- There are specific guidelines for fixing bugs and implementing changes in the project. [latent: implicit_dos_and_donts] [confidence: inferred][^claim-2]
- New configurations and tests have been added to enhance the project. [latent: project_identity_and_scope] [confidence: inferred][^claim-3]

## Task Request
- The plan should be implemented with minimal output and at the right abstraction layer. [latent: workflow_norms] [confidence: inferred][^claim-4]
- Avoid adding complexity for edge cases and renaming unless necessary. [latent: implicit_dos_and_donts] [confidence: inferred][^claim-5]
- A sequence should be followed before proposing or implementing changes. [latent: workflow_norms] [confidence: inferred][^claim-6]

### Canonical Items
- PLEASE IMPLEMENT THIS PLAN: [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-1]
- - Avoid one-off domain hints and fixed thresholds as primary logic. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-2]
- - Do not add large new schema/process complexity to solve one edge case. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-3]
- - Do not rename files, functions, or variables unless required for the fix. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-4]
- - Fix with minimal output. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-5]
- - Implement the fix at the right abstraction layer so similar issues are also prevented. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-6]
- - Prefer minimal architectural fixes that improve many cases. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-7]
- Use this sequence before proposing or implementing changes: [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-8]
- When fixing a bug: [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-9]
- implementing [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-10]
- - Added [config/full_load_config.json](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/config/full_load_config.json) [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-11]
- - Added [tests/test_full_load.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/tests/test_full_load.py) [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-12]
- - Added Phase 10 full-corpus orchestration in [wikimemory/full_load.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/wikimemory/full_load.py) [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-13]
- - Added [wikimemory/raw_event_resolver.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/wikimemory/raw_event_resolver.py). [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-14]
- - Added real-data coverage with [tests/fixtures/live_corpus_manifest.json](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/tests/fixtures/live_corpus_manifest.json) and [tests/test_live_corpus.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/W... [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-15]
- - Added [config/refresh_config.json](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/config/refresh_config.json) [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-16]
- - Added [tests/test_refresh.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/tests/test_refresh.py) [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-17]
- - Added [config/audit_config.json](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/config/audit_config.json) [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-18]
- - Added [tests/test_audit.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/tests/test_audit.py) [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-19]
- - Add `python -m wikimemory audit` as a deterministic quality-control stage over Phase 5-7 artifacts. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-20]
- - Added [config/bootstrap_config.json](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/config/bootstrap_config.json) [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-21]
- - Added bootstrap tests in [tests/test_bootstrap.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/tests/test_bootstrap.py) [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-22]
- I’m making the minimal runtime fix and then I’ll run the focused Phase 7 suite to catch any remaining issues. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-23]
- I’m wiring config and CLI next so I can run the new stage end to end before adding tests. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-24]
- ## Implementation Changes [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-25]
- - Add `python -m wikimemory bootstrap` to generate compact agent-start memory from Phase 5 extracted items and Phase 6 wiki manifests. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-26]
- - conflicts included in output must be marked in the manifest and in the bullet text with a short `(conflict)` suffix [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-27]
- - markdown body uses short bullets prefixed with stable ids like `[B01]` [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-28]
- - No exact tokenizer dependency is added in v1 [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-29]
- - no new latent knowledge is created in Phase 7 [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-30]
- - Verify source-scoped rebuild updates only touched domains [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-31]
- - Add `python -m wikimemory bootstrap` [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-32]
- I’m checking the current repo shape around Phase 6 outputs so the Phase 7 plan fits what’s already implemented. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-33]
- - I also fixed a real Windows integration bug the smoke test exposed: BOM-encoded JSON config/state files are now accepted across the pipeline in [wikimemory/discovery.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/wikimemory/discovery.py),... [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-34]
- - Added [config/wiki_config.json](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/config/wiki_config.json) for page layout, renderer, OpenAI provider/model settings, and approved latent synthesis types. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-35]
- - Added [tests/test_wiki.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/tests/test_wiki.py) covering rendered pages, manifests, citations, scoped rebuilds, deterministic item stability, low-confidence/conflict surfacing, and rollback on inva... [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-36]
- - Add a new `python -m wikimemory wiki` stage that reads Phase 5 extracted artifacts and generates a human-facing wiki under `wiki/`. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-37]
- - Updated [config/extraction_rules.json](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/config/extraction_rules.json), [README.md](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/README.md), [.gitignore](/c:/Users/Fabio/Cursor%20AI%20... [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-38]
- Added Phase 5 extraction to `WikiMemory`. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-39]
- ## Fixed Item Taxonomy [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-40]
- - Add a deterministic extraction stage that reads Phase 4 classified segments and emits structured knowledge items with provenance, recurrence tracking, and future wiki/bootstrap targeting hints. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-41]
- - Add a new CLI entry: [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-42]
- - Add a new config artifact: [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-43]
- - Add a new extractor module that follows the same file-based, atomic-promotion, incremental pattern used by segmentation and classification. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-44]
- - Add extraction outputs: [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-45]
- - define extraction rule version, fixed item taxonomy, rule patterns, domain resolution defaults, and target-page mappings [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-46]
- Should Phase 5 use this fixed v1 item taxonomy? [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-47]
- - Added [config/classification_taxonomy.json](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/config/classification_taxonomy.json) for weighted aliases, keywords, path hints, repo hints, and global-pattern rules. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-48]
- - Added Phase 4 classification in [wikimemory/classification.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/wikimemory/classification.py) with a new `run_classification(...)` pipeline that: [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-49]
- - Added [tests/test_segmentation.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/tests/test_segmentation.py) covering idempotent reruns, sample-scoped segmentation, guardrail-driven splits, incremental upstream changes, and tombstones. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-50]
- - Added Phase 3 segmentation in [wikimemory/segmentation.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/wikimemory/segmentation.py) with a new `run_segmentation(...)` pipeline that: [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-51]
- - Added [schema/normalization_catalog.json](</c:/Users/Fabio/Cursor AI projects/Projects/WikiMemory/schema/normalization_catalog.json>) for known event signatures and canonical kinds. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-52]
- - Added Phase 2 normalization to `WikiMemory` with a new CLI command: `python -m wikimemory normalize`. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-53]
- - Added a CLI: `python -m wikimemory discover`. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-54]
- - Created a new git project at `WikiMemory` with a Python-based Phase 1 discovery/indexing tool. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-55]
- I’m setting up `WikiMemory` as a new standalone project and checking the local tooling so I can implement the Phase 1 indexer with the smallest durable stack. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-56]
- - The first execution task after leaving Plan Mode is to scaffold a new git project named `WikiMemory` and create the config/state/manifests structure needed for this phase. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-57]
- Please create a git project called WikiMemory [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-58]
- Right now I only want to create the knowledge for those 3 projects, but there will be more projects in the future I'd like to build wikis on. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-59]
- When they come, I should be able to add them (maybe some config with project name, or keywords, not sure) in some config and the process should do a full run to all files (past and present) under the root to find references of those, and track them after in... [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-60]
- - Hash only small parts of the file, like prefix/suffix [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-61]
- - Phase 1 should not implement downstream parsing/resume behavior [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-62]
- I'd prefer not to have any db if possible, but if any other phase of the project will require a db, so you can add that to that db as well. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-63]
- `Phase 9 — Incremental Update Orchestration` [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-64]
- Define how humans review the wiki, how agents consume bootstrap memory, and how approvals/refresh cycles work in practice. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-65]
- Generate and update structured markdown wiki pages that are human-readable, navigable, and provenance-backed. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-66]
- Process only new or changed source material and update only the affected downstream artifacts. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-67]
- When Phase 1 hits unreadable, partial, or corrupted files, should the run continue with flags, stop immediately, or quarantine those sources for manual review? [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-68]
- - Added plateau-safe pruning logic so the pool can shrink gradually while preserving or improving stem-balance gaps instead of getting stuck. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-69]
- - Fixing it at the pruning layer generalizes beyond this one rebalance: [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-70]
- - Rebalanced the active review pool for experiment `53761995-3341-4ca2-9af1-b63b9bace516` and kept it gap-free. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-71]
- - we preserve phase readiness while keeping review work lower [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-72]
- I found the main issue: the minimizer is still scoring removable stems against the old fixed floors, so it’s not aggressively shrinking the pool toward the new 10%-of-live-pool target. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-73]
- I’m fixing that at the pruning layer first, because that should get us to a smaller, balanced pool without generating more review work. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-74]
- I’ve confirmed the live issue: the pool is only failing on `who` and `where`, and because the 10% rule is based on live pool size, the cleanest fix may be to prune excess cases rather than add more. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-75]
- The remaining mismatch is that the pool uses fixed stem floors, while your requirement is percentage-based. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-76]
- I’m running a targeted positive refill next so we add only the missing stem types, then I’ll prune back the excess `what` inventory. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-77]
- adding [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-78]
- I’m adding the actual minimizer now. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-79]
- I’m patching two things together: stricter stem targets and a final “minimal balanced pool” pass after refill, so we don’t fix the mix and then immediately drift back to an oversized queue. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-80]

## Sources
[^claim-1]: items open-brain:task_request:017361725bf6cd20, open-brain:task_request:55ff0320459be3d3, open-brain:task_request:05f604c681ec5630, open-brain:task_request:c14827929a58e169, open-brain:task_request:394a82b8ae0a6c11, open-brain:task_request:e83452c02e481519, open-brain:task_request:89b39e2dc5e2d17c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3847-3847; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3848-3850; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 9318-9318; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82500-82502; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4-5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82500-82502; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4-5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-2]: items open-brain:task_request:90cde7625b821a6c, open-brain:task_request:154c538a4c485e29, open-brain:task_request:b3dde22ca2b46735; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2045-2046; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3853-3854; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 7318-7320
[^claim-3]: items open-brain:task_request:bc57419bf256dfa2, open-brain:task_request:c0902efb5b92cb95; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4462-4467; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4462-4467
[^claim-4]: items open-brain:task_request:017361725bf6cd20, open-brain:task_request:394a82b8ae0a6c11, open-brain:task_request:e83452c02e481519; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3847-3847; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3848-3850; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 9318-9318; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82500-82502; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4-5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-5]: items open-brain:task_request:55ff0320459be3d3, open-brain:task_request:05f604c681ec5630, open-brain:task_request:c14827929a58e169; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82500-82502; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4-5
[^claim-6]: items open-brain:task_request:90cde7625b821a6c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-task_request-1]: items open-brain:task_request:017361725bf6cd20; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3847-3847; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3848-3850; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 9318-9318
[^item-task_request-2]: items open-brain:task_request:55ff0320459be3d3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-task_request-3]: items open-brain:task_request:05f604c681ec5630; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-task_request-4]: items open-brain:task_request:c14827929a58e169; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82500-82502; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4-5
[^item-task_request-5]: items open-brain:task_request:394a82b8ae0a6c11; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82500-82502; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4-5
[^item-task_request-6]: items open-brain:task_request:e83452c02e481519; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-task_request-7]: items open-brain:task_request:89b39e2dc5e2d17c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-task_request-8]: items open-brain:task_request:90cde7625b821a6c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-task_request-9]: items open-brain:task_request:154c538a4c485e29; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-task_request-10]: items open-brain:task_request:b3dde22ca2b46735; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2045-2046; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3853-3854; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 7318-7320
[^item-task_request-11]: items open-brain:task_request:bc57419bf256dfa2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4462-4467
[^item-task_request-12]: items open-brain:task_request:c0902efb5b92cb95; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4462-4467
[^item-task_request-13]: items open-brain:task_request:debb818b60c05a91; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4462-4467
[^item-task_request-14]: items open-brain:task_request:d1c87ba3ff9c6b62; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4230-4230; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4231-4235
[^item-task_request-15]: items open-brain:task_request:006d32c79959ee66; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4230-4230; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4231-4235
[^item-task_request-16]: items open-brain:task_request:35c514f42308773c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3432-3437
[^item-task_request-17]: items open-brain:task_request:806136dc53e51f33; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3432-3437
[^item-task_request-18]: items open-brain:task_request:982ac061c24e3bf4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3132-3137
[^item-task_request-19]: items open-brain:task_request:a53fb4e7e95be96e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3132-3137
[^item-task_request-20]: items open-brain:task_request:60d8506f80ed3ee0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-task_request-21]: items open-brain:task_request:5b24b29c24390e84; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2912-2917
[^item-task_request-22]: items open-brain:task_request:6ab23027825cc007; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2912-2917
[^item-task_request-23]: items open-brain:task_request:b58c972f9874729d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2857-2870
[^item-task_request-24]: items open-brain:task_request:072362f9f93fc0a0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2731-2732
[^item-task_request-25]: items open-brain:task_request:ffa4e5da689f8ee3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-task_request-26]: items open-brain:task_request:7527027068866f79; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-task_request-27]: items open-brain:task_request:02befb31a862e95e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-task_request-28]: items open-brain:task_request:ad09a6c256335df5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-task_request-29]: items open-brain:task_request:f1f0ccffdea58dab; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-task_request-30]: items open-brain:task_request:bc4aef57ad933e05; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-task_request-31]: items open-brain:task_request:59e2713b59be359a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-task_request-32]: items open-brain:task_request:7a29c298f685cd28; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2609-2609; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2610-2613
[^item-task_request-33]: items open-brain:task_request:67c40b81dbf3828b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2599-2607
[^item-task_request-34]: items open-brain:task_request:77842401770c618e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1824-1824; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1825-1828
[^item-task_request-35]: items open-brain:task_request:9d47005e477f93eb; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1593-1600; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1601-1605
[^item-task_request-36]: items open-brain:task_request:5fa16fbb28e59d14; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1593-1600; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1601-1605
[^item-task_request-37]: items open-brain:task_request:3b5db8c995a471df; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1377-1380; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1383-1383; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1384-1385
[^item-task_request-38]: items open-brain:task_request:e5070aadc1c42c46; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1275-1280; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1281-1285
[^item-task_request-39]: items open-brain:task_request:a5856a0adc82dd93; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1275-1280; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1281-1285
[^item-task_request-40]: items open-brain:task_request:84757bb34e637699; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-task_request-41]: items open-brain:task_request:b3c71cb53e126b41; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-task_request-42]: items open-brain:task_request:1ca284d16c92ff22; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-task_request-43]: items open-brain:task_request:63a708caee99e0ea; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-task_request-44]: items open-brain:task_request:67beb855a4ebf508; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-task_request-45]: items open-brain:task_request:13079f42cc4f7e45; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-task_request-46]: items open-brain:task_request:5c8e6b347771711c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-task_request-47]: items open-brain:task_request:965bab3206a0dc32; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-task_request-48]: items open-brain:task_request:e102e996a38f681d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 930-940; 019d837d-d249-71c3-9637-b8d6992ce805 lines 941-945
[^item-task_request-49]: items open-brain:task_request:21aedd507ce137dd; 019d837d-d249-71c3-9637-b8d6992ce805 lines 930-940; 019d837d-d249-71c3-9637-b8d6992ce805 lines 941-945
[^item-task_request-50]: items open-brain:task_request:793d00cc927ab927; 019d837d-d249-71c3-9637-b8d6992ce805 lines 728-738; 019d837d-d249-71c3-9637-b8d6992ce805 lines 739-742
[^item-task_request-51]: items open-brain:task_request:2ce0e82708ec6c23; 019d837d-d249-71c3-9637-b8d6992ce805 lines 728-738; 019d837d-d249-71c3-9637-b8d6992ce805 lines 739-742
[^item-task_request-52]: items open-brain:task_request:be83dc898584d435; 019d837d-d249-71c3-9637-b8d6992ce805 lines 468-468; 019d837d-d249-71c3-9637-b8d6992ce805 lines 469-472
[^item-task_request-53]: items open-brain:task_request:684a02fefc3fe857; 019d837d-d249-71c3-9637-b8d6992ce805 lines 468-468; 019d837d-d249-71c3-9637-b8d6992ce805 lines 469-472
[^item-task_request-54]: items open-brain:task_request:66933bb730cea654; 019d837d-d249-71c3-9637-b8d6992ce805 lines 229-236; 019d837d-d249-71c3-9637-b8d6992ce805 lines 237-241
[^item-task_request-55]: items open-brain:task_request:2b216055b6e48086; 019d837d-d249-71c3-9637-b8d6992ce805 lines 229-236; 019d837d-d249-71c3-9637-b8d6992ce805 lines 237-241
[^item-task_request-56]: items open-brain:task_request:3f897fe24842aa87; 019d837d-d249-71c3-9637-b8d6992ce805 lines 122-134
[^item-task_request-57]: items open-brain:task_request:6cd9480d4e6952dd; 019d837d-d249-71c3-9637-b8d6992ce805 lines 112-115; 019d837d-d249-71c3-9637-b8d6992ce805 lines 118-118; 019d837d-d249-71c3-9637-b8d6992ce805 lines 119-120
[^item-task_request-58]: items open-brain:task_request:701092d577b53fd2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 106-108
[^item-task_request-59]: items open-brain:task_request:cb10bb4e4b13dedb; 019d837d-d249-71c3-9637-b8d6992ce805 lines 95-97
[^item-task_request-60]: items open-brain:task_request:7097014397326b10; 019d837d-d249-71c3-9637-b8d6992ce805 lines 95-97
[^item-task_request-61]: items open-brain:task_request:c6f248999424b39e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-task_request-62]: items open-brain:task_request:b5d44b87a30bdea8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-task_request-63]: items open-brain:task_request:64f0df53abc6cc45; 019d837d-d249-71c3-9637-b8d6992ce805 lines 19-21
[^item-task_request-64]: items open-brain:task_request:4656bd819bd8aba2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-task_request-65]: items open-brain:task_request:296be0f840f2744b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-task_request-66]: items open-brain:task_request:f414799bf676e9e2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-task_request-67]: items open-brain:task_request:b7b6dc918afd2bc4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-task_request-68]: items open-brain:task_request:aaec0ab8628fef36; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-task_request-69]: items open-brain:task_request:a1fbc4d07cb4c042; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88082-88085
[^item-task_request-70]: items open-brain:task_request:f93fcc8b0a893401; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88082-88085
[^item-task_request-71]: items open-brain:task_request:39fe943787ef6830; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88082-88085
[^item-task_request-72]: items open-brain:task_request:c6ac056c7eb616a2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88082-88085
[^item-task_request-73]: items open-brain:task_request:9761563653ceaffa; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88038-88044
[^item-task_request-74]: items open-brain:task_request:01d47fb2e7754f12; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88038-88044
[^item-task_request-75]: items open-brain:task_request:9f456213962ffbea; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88014-88020
[^item-task_request-76]: items open-brain:task_request:393c07d06bb2c5f6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87935-87941
[^item-task_request-77]: items open-brain:task_request:5362df707f885585; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87781-87787
[^item-task_request-78]: items open-brain:task_request:8f74563b1ab9708e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4006-4016; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13814-13815; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13943-13943
[^item-task_request-79]: items open-brain:task_request:ba803367ac860b4a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87745-87746
[^item-task_request-80]: items open-brain:task_request:33cbc24a097d5b94; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87693-87694
