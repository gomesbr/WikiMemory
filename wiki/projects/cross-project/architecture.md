---
title: "Cross-Project - Architecture"
page_id: "projects/cross-project/architecture"
domain: "cross-project"
bucket: "architecture"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:10:33.736771Z
source_count: 2
claim_count: 7
tags:
  - wikimemory
  - cross-project
  - cross-project
  - bucket
  - architecture
---
# Cross-Project - Architecture

Navigation: [[projects/cross-project/index|Cross-Project]] | [[projects/cross-project/communication-preferences|Cross-Project - Communication Preferences]] | [[projects/cross-project/workflow-rules|Cross-Project - Workflow Rules]] | [[projects/cross-project/code-map|Cross-Project - Code Map]] | [[projects/cross-project/current-state|Cross-Project - Current State]] | [[projects/cross-project/tasks|Cross-Project - Tasks]] | [[projects/cross-project/outcomes|Cross-Project - Outcomes]] | [[projects/cross-project/failures|Cross-Project - Failures]] | [[projects/cross-project/decisions|Cross-Project - Decisions]] | [[projects/cross-project/next-steps|Cross-Project - Next Steps]] | [[projects/cross-project/open-questions|Cross-Project - Open Questions]]
Related Domains: [[projects/ai-scientist/index|AI Scientist]], [[projects/ai-trader/index|AI Trader]], [[projects/open-brain/index|Open Brain]]

## Summary
- The architecture is being developed to ensure alignment with existing systems. [latent: architecture_synthesis] [confidence: strong][^claim-1]
- The new full-load orchestration is being integrated into the existing phase pipeline and state model. [latent: architecture_synthesis] [confidence: strong][^claim-2]
- Current pipeline hooks have been confirmed as part of the architecture validation process. [latent: architecture_synthesis] [confidence: strong][^claim-3]
- The architecture will include grounding in the current pipeline and rollout hooks to match existing capabilities. [latent: architecture_synthesis] [confidence: strong][^claim-4]

## Architecture Note
- The pipeline is confirmed to be ready for a full run, indicating successful architecture integration. [latent: architecture_synthesis] [confidence: strong][^claim-5]
- A real-data extraction failure was encountered, prompting a reproduction of the pipeline stage to address the issue. [latent: recurring_failure_patterns] [confidence: strong][^claim-6]
- Next steps include wiring the resolver and validating the live sample set through the pipeline. [latent: implicit_next_steps] [confidence: strong][^claim-7]

### Canonical Items
- architecture [confidence: strong] [recurrence: 1][^item-architecture_note-1]
- I’m wiring the new full-load orchestration into the existing phase pipeline, state model, and tests first so it stays aligned with the current refresh/audit architecture. [confidence: strong] [recurrence: 1][^item-architecture_note-2]
- I’ve confirmed the current pipeline hooks. [confidence: strong] [recurrence: 1][^item-architecture_note-3]
- I’m grounding in the current pipeline and rollout hooks first so the full-run loop plan matches what the repo can already do and where it needs orchestration logic. [confidence: strong] [recurrence: 1][^item-architecture_note-4]
- - Yes, the pipeline is ready for a full run. [confidence: strong] [recurrence: 1][^item-architecture_note-5]
- test_live_sample_pipeline_is_pointer_first_and_stable [confidence: strong] [recurrence: 1][^item-architecture_note-6]
- The live suite hit a real-data extraction failure, so I’m reproducing just that pipeline stage now and printing the fatal summary. [confidence: strong] [recurrence: 1][^item-architecture_note-7]
- next step is wiring the resolver and the new pointer-first artifact shape, then I’ll validate the live sample set through the pipeline. [confidence: strong] [recurrence: 1][^item-architecture_note-8]
- I’m checking all call sites now so I can thread the new optional source-root config through without breaking the existing pipeline. [confidence: strong] [recurrence: 1][^item-architecture_note-9]
- I’m patching the staging bug and adding a focused bootstrap test suite against the existing sample pipeline. [confidence: strong] [recurrence: 1][^item-architecture_note-10]
- I’m wiring tests and the last repo updates, then I’ll validate the bootstrap pipeline end-to-end locally. [confidence: strong] [recurrence: 1][^item-architecture_note-11]
- I’m adding the new module and config now, then I’ll hook the CLI/tests after the core pipeline is in place. [confidence: strong] [recurrence: 1][^item-architecture_note-12]
- - Real-sample wiki pipeline now succeeds with the same real sample using a stubbed synthesizer: [confidence: strong] [recurrence: 1][^item-architecture_note-13]
- I’m running them first in isolation so we can tighten the wiki contracts without muddying the rest of the pipeline. [confidence: strong] [recurrence: 1][^item-architecture_note-14]
- I’ve got the core wiki pipeline in place. [confidence: strong] [recurrence: 1][^item-architecture_note-15]
- Phase 6 is partially scaffolded, and I’m tightening it by adding the wiki test coverage and then validating the full pipeline end to end. [confidence: strong] [recurrence: 1][^item-architecture_note-16]
- Next I’m checking the exact extracted artifact shapes and the existing test patterns so the wiki stage plugs in cleanly and stays incremental like the rest of the pipeline. [confidence: strong] [recurrence: 1][^item-architecture_note-17]
- Architecture synthesis [confidence: strong] [recurrence: 1][^item-architecture_note-18]
- Examples: the real conceptual pipeline, which layers are canonical, which artifacts are intermediate, where human-facing vs agent-facing outputs diverge. [confidence: strong] [recurrence: 1][^item-architecture_note-19]
- I’ve confirmed the current pipeline shape. [confidence: strong] [recurrence: 1][^item-architecture_note-20]
- I’m doing a quick syntax and structure pass now before I wire the CLI and tests, so any contract drift shows up early instead of after the full pipeline is connected. [confidence: strong] [recurrence: 1][^item-architecture_note-21]
- I’m adding the taxonomy config, classifier module, CLI wiring, and tests together so the scoring logic and the audit/state behavior land as one coherent feature rather than a half-wired pipeline. [confidence: strong] [recurrence: 1][^item-architecture_note-22]
- I’m implementing Phase 4 on top of the current segmentation pipeline, and I’m checking the existing state/output patterns first so classification fits the same atomic, incremental flow instead of inventing a separate path. [confidence: strong] [recurrence: 1][^item-architecture_note-23]
- ## High-level architecture [confidence: strong] [recurrence: 1][^item-architecture_note-24]
- ## TARGET ARCHITECTURE (CONCEPTUAL) [confidence: strong] [recurrence: 1][^item-architecture_note-25]
- * architecture note [confidence: strong] [recurrence: 1][^item-architecture_note-26]
- * architecture terms [confidence: strong] [recurrence: 1][^item-architecture_note-27]
- * architecture/code map [confidence: strong] [recurrence: 1][^item-architecture_note-28]
- Focus on architecture, phases, data flow, and implementation strategy. [confidence: strong] [recurrence: 1][^item-architecture_note-29]
- Pipeline: [confidence: strong] [recurrence: 1][^item-architecture_note-30]
- Implementing the `Network` screen and its data pipeline now. [confidence: strong] [recurrence: 1][^item-architecture_note-31]
- Next I’ll focus only on the requested UI readout/pipeline fixes and the loop kick-off. [confidence: strong] [recurrence: 1][^item-architecture_note-32]
- I’ll compare the current runtime behavior against the experiment/readiness stack so the re-scope lands cleanly without inventing a second parallel architecture. [confidence: strong] [recurrence: 1][^item-architecture_note-33]
- I’ve added pronoun support to the summary pipeline. [confidence: strong] [recurrence: 1][^item-architecture_note-34]
- - Question: `What areas in robotics did the assistant suggest would be a good fit for someone with experience in data integration and pipelines?` [confidence: strong] [recurrence: 1][^item-architecture_note-35]
- or fix the pipeline so they also become reviewable on screen [confidence: strong] [recurrence: 1][^item-architecture_note-36]
- I’m checking which one it is before I hand this back, so the pipeline is actually complete rather than “almost complete.” [confidence: strong] [recurrence: 1][^item-architecture_note-37]
- I’m looking specifically for underused metadata/facets and for places where the authoring pipeline is discarding otherwise-valid domain/lens coverage. [confidence: strong] [recurrence: 1][^item-architecture_note-38]
- ## Information Architecture (Evolution Module) [confidence: strong] [recurrence: 1][^item-architecture_note-39]
- - `/v2/experiments/:id/components/leaderboard` [confidence: strong] [recurrence: 1][^item-architecture_note-40]

## Sources
[^claim-1]: items cross-project:architecture_note:d122884e061c87d0; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5628-5629; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20565-20567
[^claim-2]: items cross-project:architecture_note:2dd956131d50b401; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4337-4348
[^claim-3]: items cross-project:architecture_note:7f9d06d89c04c553; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4264-4278
[^claim-4]: items cross-project:architecture_note:0430d86fceb4f4d5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4251-4262
[^claim-5]: items cross-project:architecture_note:a85e3329ed6314cd; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4240-4244
[^claim-6]: items cross-project:architecture_note:48fe2e88ecfb53e7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3981-3996
[^claim-7]: items cross-project:architecture_note:ab434fd5f11ecdf0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3758-3759
[^item-architecture_note-1]: items cross-project:architecture_note:d122884e061c87d0; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5628-5629; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20565-20567
[^item-architecture_note-2]: items cross-project:architecture_note:2dd956131d50b401; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4337-4348
[^item-architecture_note-3]: items cross-project:architecture_note:7f9d06d89c04c553; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4264-4278
[^item-architecture_note-4]: items cross-project:architecture_note:0430d86fceb4f4d5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4251-4262
[^item-architecture_note-5]: items cross-project:architecture_note:a85e3329ed6314cd; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4240-4244
[^item-architecture_note-6]: items cross-project:architecture_note:fd117d7fc95274af; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3981-3996; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4038-4042; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4071-4079
[^item-architecture_note-7]: items cross-project:architecture_note:48fe2e88ecfb53e7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3981-3996
[^item-architecture_note-8]: items cross-project:architecture_note:ab434fd5f11ecdf0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3758-3759
[^item-architecture_note-9]: items cross-project:architecture_note:fd54d59ca9618f56; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3712-3720
[^item-architecture_note-10]: items cross-project:architecture_note:5e730a24b68fb5a8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2831-2847
[^item-architecture_note-11]: items cross-project:architecture_note:3a15ca186860c5be; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2763-2777
[^item-architecture_note-12]: items cross-project:architecture_note:eae5c31ff4da6365; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2702-2703
[^item-architecture_note-13]: items cross-project:architecture_note:0fcb93aac91a29b7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2376-2381
[^item-architecture_note-14]: items cross-project:architecture_note:91f14c73fd0f8e1b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1564-1576
[^item-architecture_note-15]: items cross-project:architecture_note:e40975f6eaa40d0e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1502-1513
[^item-architecture_note-16]: items cross-project:architecture_note:c87abf68bd4346b4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1489-1500
[^item-architecture_note-17]: items cross-project:architecture_note:e21cf25d076de7a0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1387-1398
[^item-architecture_note-18]: items cross-project:architecture_note:74450be2762a1c3f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-architecture_note-19]: items cross-project:architecture_note:6651b610b018966f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-architecture_note-20]: items cross-project:architecture_note:f3aec2409ca1008e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1011-1022
[^item-architecture_note-21]: items cross-project:architecture_note:a1f3ea1f03961255; 019d837d-d249-71c3-9637-b8d6992ce805 lines 873-881
[^item-architecture_note-22]: items cross-project:architecture_note:9ac10df0d8277557; 019d837d-d249-71c3-9637-b8d6992ce805 lines 835-836
[^item-architecture_note-23]: items cross-project:architecture_note:650dc78fb46c22c5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 809-820
[^item-architecture_note-24]: items cross-project:architecture_note:fff3fdb417f87998; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-architecture_note-25]: items cross-project:architecture_note:3dca9f5aa42ac210; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-architecture_note-26]: items cross-project:architecture_note:bea5d09f71834b91; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-architecture_note-27]: items cross-project:architecture_note:61ec610cd195a575; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-architecture_note-28]: items cross-project:architecture_note:b3479a4c5884286e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-architecture_note-29]: items cross-project:architecture_note:9b521097fc0e29ba; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-architecture_note-30]: items cross-project:architecture_note:b62cbeca6b5af990; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-architecture_note-31]: items cross-project:architecture_note:bfd74c4b71ad7333; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71727-71745
[^item-architecture_note-32]: items cross-project:architecture_note:71e348f45ae49d96; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 67889-67906
[^item-architecture_note-33]: items cross-project:architecture_note:a09655d08653507f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57265-57279
[^item-architecture_note-34]: items cross-project:architecture_note:bbf7644abafe0f48; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 50840-50854
[^item-architecture_note-35]: items cross-project:architecture_note:85993302cd46e0f6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43631-43631; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43632-43636
[^item-architecture_note-36]: items cross-project:architecture_note:c7be8725e416b004; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43631-43631; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43632-43636
[^item-architecture_note-37]: items cross-project:architecture_note:c0b538b25d55d4ce; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43615-43621
[^item-architecture_note-38]: items cross-project:architecture_note:a8c4366f7f3c1689; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 40881-40892
[^item-architecture_note-39]: items cross-project:architecture_note:8d7a0e5cffbfd7c4; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 34450-34457
[^item-architecture_note-40]: items cross-project:architecture_note:9c322ef9990fce5c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 34450-34457
