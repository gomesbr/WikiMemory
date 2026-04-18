---
title: "Open Brain - Architecture"
page_id: "projects/open-brain/architecture"
domain: "open-brain"
bucket: "architecture"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:08:29.206436Z
source_count: 3
claim_count: 5
tags:
  - wikimemory
  - project
  - open-brain
  - bucket
  - architecture
---
# Open Brain - Architecture

Navigation: [[projects/open-brain/index|Open Brain]] | [[projects/open-brain/communication-preferences|Open Brain - Communication Preferences]] | [[projects/open-brain/workflow-rules|Open Brain - Workflow Rules]] | [[projects/open-brain/code-map|Open Brain - Code Map]] | [[projects/open-brain/current-state|Open Brain - Current State]] | [[projects/open-brain/tasks|Open Brain - Tasks]] | [[projects/open-brain/outcomes|Open Brain - Outcomes]] | [[projects/open-brain/failures|Open Brain - Failures]] | [[projects/open-brain/decisions|Open Brain - Decisions]] | [[projects/open-brain/next-steps|Open Brain - Next Steps]] | [[projects/open-brain/open-questions|Open Brain - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- Prefer generalizable architecture over one-off patches. [latent: architecture_synthesis] [confidence: strong][^claim-1]
- The `component_registry` is an important element in the architecture. [latent: architecture_synthesis] [confidence: strong][^claim-2]
- `strategy_component_bindings` play a significant role in the architecture. [latent: architecture_synthesis] [confidence: strong][^claim-3]

## Architecture Note
- The architecture should prioritize generalizable solutions over one-off patches. [latent: architecture_synthesis] [confidence: strong][^claim-4]
- The `component_registry` is a key part of the architecture framework. [latent: architecture_synthesis] [confidence: strong][^claim-5]

### Canonical Items
- - Prefer generalizable architecture over one-off patches. [confidence: strong] [recurrence: 2][^item-architecture_note-1]
- component_performance [confidence: strong] [recurrence: 1][^item-architecture_note-2]
- `component_registry` [confidence: strong] [recurrence: 1][^item-architecture_note-3]
- `component_pair_performance` [confidence: strong] [recurrence: 1][^item-architecture_note-4]
- `strategy_component_bindings` [confidence: strong] [recurrence: 1][^item-architecture_note-5]
- modifiedcomponents [confidence: strong] [recurrence: 1][^item-architecture_note-6]
- `component_stability` [confidence: strong] [recurrence: 1][^item-architecture_note-7]
- component [confidence: strong] [recurrence: 1][^item-architecture_note-8]
- - `current_state`, `decision`, `architecture_note`, `task_request`, `next_step`, `open_question`, `failure`, project-scoped rules [confidence: strong] [recurrence: 1][^item-architecture_note-9]
- - `project`: `identity=4`, `current_state=6`, `architecture=5`, `project_rules=4`, `tasks=5`, `next_steps=5`, `open_questions=4`, `failures_risks=4` [confidence: strong] [recurrence: 1][^item-architecture_note-10]
- - I also fixed a real Windows integration bug the smoke test exposed: BOM-encoded JSON config/state files are now accepted across the pipeline in [wikimemory/discovery.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/wikimemory/discovery.py),... [confidence: strong] [recurrence: 1][^item-architecture_note-11]
- - `architecture_note` [confidence: strong] [recurrence: 1][^item-architecture_note-12]
- - `architecture_note` -> `architecture` [confidence: strong] [recurrence: 1][^item-architecture_note-13]
- - `decision`, `architecture_note`, `code_location`, `current_state`, `task_request`, `outcome`, `failure`, `next_step`, `open_question` default to the best non-global segment domain [confidence: strong] [recurrence: 1][^item-architecture_note-14]
- - store them in `code_location` and map them to `architecture_note` or `code_location` items depending on the triggering rule [confidence: strong] [recurrence: 1][^item-architecture_note-15]
- `communication_preference`, `do_rule`, `dont_rule`, `workflow_rule`, `decision`, `architecture_note`, `code_location`, `current_state`, `task_request`, `outcome`, `failure`, `next_step`, `open_question` [confidence: strong] [recurrence: 1][^item-architecture_note-16]
- Introducing an LLM in Phase 5 now would mainly buy you better recall on messy, implicit knowledge: it can pull out decisions, preferences, next steps, and architecture notes even when they’re phrased indirectly or spread across a segment. [confidence: strong] [recurrence: 1][^item-architecture_note-17]
- - Added Phase 4 classification in [wikimemory/classification.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/wikimemory/classification.py) with a new `run_classification(...)` pipeline that: [confidence: strong] [recurrence: 1][^item-architecture_note-18]
- - Added Phase 3 segmentation in [wikimemory/segmentation.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/wikimemory/segmentation.py) with a new `run_segmentation(...)` pipeline that: [confidence: strong] [recurrence: 1][^item-architecture_note-19]
- Turn classified segments into durable knowledge items such as preferences, rules, decisions, architecture notes, outcomes, and open questions. [confidence: strong] [recurrence: 1][^item-architecture_note-20]
- I’ve confirmed the experiment-loop work is already in these files, so I’m building the case-authoring hardening on top of that instead of fighting the existing architecture. [confidence: strong] [recurrence: 1][^item-architecture_note-21]
- I’ve confirmed the experiment loop already has the contract/trust pattern we want, so I’m mirroring that pattern into the authoring loop instead of inventing a second architecture. [confidence: strong] [recurrence: 1][^item-architecture_note-22]
- I’m tightening the judge layer and adding the batch/repair bookkeeping around that existing writer rather than replacing the whole pipeline. [confidence: strong] [recurrence: 1][^item-architecture_note-23]
- Reading the actual case-authoring loop entry points so the plan matches the existing architecture. [confidence: strong] [recurrence: 1][^item-architecture_note-24]
- - Added per-strategy `runContract`, explicit `trustState`, staged internal evaluation (`sentinel`, `discriminative`, `full/certification`), hybrid GPT‑5.4 review/research routing, stronger component-history ranking, and DB-backed `loopState` / best-trusted-... [confidence: strong] [recurrence: 1][^item-architecture_note-25]
- - strategy search now uses component history more directly instead of generic retry behavior [confidence: strong] [recurrence: 1][^item-architecture_note-26]
- - A rescue/research-generated strategy uses component-history ranking instead of generic retry-only logic. [confidence: strong] [recurrence: 1][^item-architecture_note-27]
- - Before enqueueing rescue/research strategies, rank components and component pairs by: [confidence: strong] [recurrence: 1][^item-architecture_note-28]
- - component deltas [confidence: strong] [recurrence: 1][^item-architecture_note-29]
- - Component history affects next-strategy composition in a measurable way. [confidence: strong] [recurrence: 1][^item-architecture_note-30]
- - contribute to component merit as if it were a clean run [confidence: strong] [recurrence: 1][^item-architecture_note-31]
- - current component-performance signals [confidence: strong] [recurrence: 1][^item-architecture_note-32]
- - exploit component-performance history more directly when generating next strategies [confidence: strong] [recurrence: 1][^item-architecture_note-33]
- - Generate new strategies by varying only a small number of components at a time. [confidence: strong] [recurrence: 1][^item-architecture_note-34]
- - Keep `component_performance`, `component_stability`, and `component_pair_performance` as the canonical component history. [confidence: strong] [recurrence: 1][^item-architecture_note-35]
- - recombining strong stable components [confidence: strong] [recurrence: 1][^item-architecture_note-36]
- Stronger use of component history [confidence: strong] [recurrence: 1][^item-architecture_note-37]
- This plan keeps the current experiment architecture and improves it in five ways: [confidence: strong] [recurrence: 1][^item-architecture_note-38]
- - `enqueueResearchCandidates(...)` exists, but the loop is still not exploiting `component_performance`, `component_stability`, and `component_pair_performance` aggressively enough when deciding what to test next [confidence: strong] [recurrence: 1][^item-architecture_note-39]
- - structured lessons and component-performance persistence [confidence: strong] [recurrence: 1][^item-architecture_note-40]

## Sources
[^claim-1]: items open-brain:architecture_note:ba3e4d767bf8af2c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-2]: items open-brain:architecture_note:4beda0bb4b4f276f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31363-31366; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31407-31410; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31431-31434
[^claim-3]: items open-brain:architecture_note:518c62e8e53bacec; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31363-31366; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31407-31410; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31431-31434
[^claim-4]: items open-brain:architecture_note:ba3e4d767bf8af2c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-5]: items open-brain:architecture_note:4beda0bb4b4f276f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31363-31366; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31407-31410; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31431-31434
[^item-architecture_note-1]: items open-brain:architecture_note:ba3e4d767bf8af2c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-architecture_note-2]: items open-brain:architecture_note:9abbec94c1f4cd0f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31345-31345; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31346-31349; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31363-31366
[^item-architecture_note-3]: items open-brain:architecture_note:4beda0bb4b4f276f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31363-31366; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31407-31410; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31431-31434
[^item-architecture_note-4]: items open-brain:architecture_note:f20e69831af7254f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31363-31366; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31407-31410; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31431-31434
[^item-architecture_note-5]: items open-brain:architecture_note:518c62e8e53bacec; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31363-31366; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31407-31410; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31431-31434
[^item-architecture_note-6]: items open-brain:architecture_note:69c1f020730ee686; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 32102-32109; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 83327-83332
[^item-architecture_note-7]: items open-brain:architecture_note:8a8ce2bc0dff4440; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31431-31434; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31436-31436; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31437-31440
[^item-architecture_note-8]: items open-brain:architecture_note:00c6379ef16d53a0; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 25501-25508; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31360-31362; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31363-31366
[^item-architecture_note-9]: items open-brain:architecture_note:02b4a8e04574bc78; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-architecture_note-10]: items open-brain:architecture_note:4a399bebb3a43fc1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-architecture_note-11]: items open-brain:architecture_note:21b7f68063651693; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1824-1824; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1825-1828
[^item-architecture_note-12]: items open-brain:architecture_note:2cc36c60ba034180; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-architecture_note-13]: items open-brain:architecture_note:19c44efa5f5361a0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-architecture_note-14]: items open-brain:architecture_note:730b0275a11988e7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-architecture_note-15]: items open-brain:architecture_note:a6893f532d3b48d0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-architecture_note-16]: items open-brain:architecture_note:fcb46026457060e9; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-architecture_note-17]: items open-brain:architecture_note:d48bd10f9d650d5a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-architecture_note-18]: items open-brain:architecture_note:b00bf1a1104b194c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 930-940; 019d837d-d249-71c3-9637-b8d6992ce805 lines 941-945
[^item-architecture_note-19]: items open-brain:architecture_note:ce9fbbcc082fb832; 019d837d-d249-71c3-9637-b8d6992ce805 lines 728-738; 019d837d-d249-71c3-9637-b8d6992ce805 lines 739-742
[^item-architecture_note-20]: items open-brain:architecture_note:49c53b82f492b660; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-architecture_note-21]: items open-brain:architecture_note:88b1b99133583dca; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84510-84520
[^item-architecture_note-22]: items open-brain:architecture_note:c94c81a1b735c5c4; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84157-84169
[^item-architecture_note-23]: items open-brain:architecture_note:e4e0a724701b463e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84118-84126
[^item-architecture_note-24]: items open-brain:architecture_note:e46ae29815aebeca; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 83982-83990
[^item-architecture_note-25]: items open-brain:architecture_note:c6d7e4291170de0b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 83939-83944
[^item-architecture_note-26]: items open-brain:architecture_note:2f072c9b74f39d83; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 83939-83944
[^item-architecture_note-27]: items open-brain:architecture_note:7062916e0bf4cd3a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-architecture_note-28]: items open-brain:architecture_note:0e82f7fb36303c58; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-architecture_note-29]: items open-brain:architecture_note:0703d030488257ac; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-architecture_note-30]: items open-brain:architecture_note:80b662daba01c821; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-architecture_note-31]: items open-brain:architecture_note:18ad3acb03e9c704; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-architecture_note-32]: items open-brain:architecture_note:0f281ebe322fd7c5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-architecture_note-33]: items open-brain:architecture_note:898af2ec69dd107a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-architecture_note-34]: items open-brain:architecture_note:e6174a1975bf8c65; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-architecture_note-35]: items open-brain:architecture_note:6642cfff44e389e8; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-architecture_note-36]: items open-brain:architecture_note:9e61fa69139cb433; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-architecture_note-37]: items open-brain:architecture_note:198afadbf7a905ff; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-architecture_note-38]: items open-brain:architecture_note:fa273851592771d5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-architecture_note-39]: items open-brain:architecture_note:8206694edcd2715a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82796-82796; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82797-82800
[^item-architecture_note-40]: items open-brain:architecture_note:ca87ed1fb906aa80; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82796-82796; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82797-82800
