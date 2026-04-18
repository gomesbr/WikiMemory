---
title: "Open Brain - Decisions"
page_id: "projects/open-brain/decisions"
domain: "open-brain"
bucket: "decisions"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:09:06.477749Z
source_count: 3
claim_count: 6
tags:
  - wikimemory
  - project
  - open-brain
  - bucket
  - decisions
---
# Open Brain - Decisions

Navigation: [[projects/open-brain/index|Open Brain]] | [[projects/open-brain/communication-preferences|Open Brain - Communication Preferences]] | [[projects/open-brain/workflow-rules|Open Brain - Workflow Rules]] | [[projects/open-brain/architecture|Open Brain - Architecture]] | [[projects/open-brain/code-map|Open Brain - Code Map]] | [[projects/open-brain/current-state|Open Brain - Current State]] | [[projects/open-brain/tasks|Open Brain - Tasks]] | [[projects/open-brain/outcomes|Open Brain - Outcomes]] | [[projects/open-brain/failures|Open Brain - Failures]] | [[projects/open-brain/next-steps|Open Brain - Next Steps]] | [[projects/open-brain/open-questions|Open Brain - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- Locked decisions are documented and durable. [latent: decision_synthesis] [confidence: strong][^claim-1]
- Current state, decisions, architecture notes, task requests, next steps, open questions, and failures are governed by project-scoped rules. [latent: decision_synthesis] [confidence: strong][^claim-2]
- The current repository state and decisions from phases 1-6 are sufficient to lock phase 7. [latent: decision_synthesis] [confidence: strong][^claim-3]

## Decision
- Decisions are explicitly documented using direct phrases and project naming conventions. [latent: communication_preferences] [confidence: strong][^claim-4]
- Introducing an LLM in Phase 5 can enhance recall of implicit knowledge related to decisions and architecture notes. [latent: current_state_synthesis] [confidence: strong][^claim-5]
- Normalization decisions that materially affect design will be asked after grounding Phase 2 in the current WikiMemory state. [latent: implicit_next_steps] [confidence: strong][^claim-6]

### Canonical Items
- ## Locked Decisions [confidence: explicit] [recurrence: 1][^item-decision-1]
- reviewdecision [confidence: explicit] [recurrence: 1][^item-decision-2]
- - `current_state`, `decision`, `architecture_note`, `task_request`, `next_step`, `open_question`, `failure`, project-scoped rules [confidence: explicit] [recurrence: 1][^item-decision-3]
- Current repo state and the Phase 1-6 decisions are enough to lock Phase 7. [confidence: explicit] [recurrence: 1][^item-decision-4]
- - `decision` -> `decisions` [confidence: explicit] [recurrence: 1][^item-decision-5]
- - `decision`, `architecture_note`, `code_location`, `current_state`, `task_request`, `outcome`, `failure`, `next_step`, `open_question` default to the best non-global segment domain [confidence: explicit] [recurrence: 1][^item-decision-6]
- - `explicit` for direct phrases like “communication preference”, “workflow rule”, “we decided”, explicit project naming, or explicit path/module mentions [confidence: explicit] [recurrence: 1][^item-decision-7]
- `communication_preference`, `do_rule`, `dont_rule`, `workflow_rule`, `decision`, `architecture_note`, `code_location`, `current_state`, `task_request`, `outcome`, `failure`, `next_step`, `open_question` [confidence: explicit] [recurrence: 1][^item-decision-8]
- I need these last decisions before I lock the Phase 5 plan: [confidence: explicit] [recurrence: 1][^item-decision-9]
- Introducing an LLM in Phase 5 now would mainly buy you better recall on messy, implicit knowledge: it can pull out decisions, preferences, next steps, and architecture notes even when they’re phrased indirectly or spread across a segment. [confidence: explicit] [recurrence: 1][^item-decision-10]
- I’m grounding Phase 2 in the current `WikiMemory` state and the real trace structure first, then I’ll ask only the normalization decisions that still materially affect the design. [confidence: explicit] [recurrence: 1][^item-decision-11]
- 11-Give me some pros and cons of each so I can make the decision [confidence: explicit] [recurrence: 1][^item-decision-12]
- 9-This is architectural decision I'll leave to you. [confidence: explicit] [recurrence: 1][^item-decision-13]
- Before I plan it, I need these decisions clarified: [confidence: explicit] [recurrence: 1][^item-decision-14]
- Turn classified segments into durable knowledge items such as preferences, rules, decisions, architecture notes, outcomes, and open questions. [confidence: explicit] [recurrence: 1][^item-decision-15]
- The remaining issues were exactly the kind we want typecheck to catch: preserving verifier provenance when we override admission decisions, and making sure the blocker summary uses the canonical failure-bucket shape. [confidence: explicit] [recurrence: 1][^item-decision-16]
- Typecheck caught two real consistency issues: the repaired admission-decision override needs to preserve the verifier metadata, and my blocker summary call was using the wrong helper shape. [confidence: explicit] [recurrence: 1][^item-decision-17]
- Feed review decisions back into the loop [confidence: explicit] [recurrence: 1][^item-decision-18]
- Two decisions will materially change the implementation plan, so I’m locking them before I finalize it. [confidence: explicit] [recurrence: 1][^item-decision-19]
- hascandidatedecision [confidence: explicit] [recurrence: 1][^item-decision-20]
- I’m wiring the last pieces together now: final run decisions will only count when trusted, and the Evolution overview will get the new persisted scoreboard instead of ad hoc status text. [confidence: explicit] [recurrence: 1][^item-decision-21]
- I’ve reached the remaining old decision path in the experiment core. [confidence: explicit] [recurrence: 1][^item-decision-22]
- strategyreviewdecision [confidence: explicit] [recurrence: 1][^item-decision-23]
- - A borderline strategy triggers GPT‑5.4 review and records the review tier/decision. [confidence: explicit] [recurrence: 1][^item-decision-24]
- - last evaluator decision and model tier [confidence: explicit] [recurrence: 1][^item-decision-25]
- - use hybrid GPT‑5.4 routing for review/research decisions [confidence: explicit] [recurrence: 1][^item-decision-26]
- I just need to lock two high-impact decisions so the plan is implementable without guessing. [confidence: explicit] [recurrence: 1][^item-decision-27]
- I’m grounding the experiment-loop plan against the current harness shape so we can lock the right decisions and avoid planning a refactor that fights the existing system. [confidence: explicit] [recurrence: 1][^item-decision-28]
- - Your review decisions should continuously update the judge rubric and queue scoring. [confidence: explicit] [recurrence: 1][^item-decision-29]
- - reviewed totals count all owner-labeled `yes/no` decisions [confidence: explicit] [recurrence: 1][^item-decision-30]
- - graphability decision correctness [confidence: explicit] [recurrence: 1][^item-decision-31]
- I need one UI decision so the flow is concrete. [confidence: explicit] [recurrence: 1][^item-decision-32]
- Add a graphability decision` [confidence: explicit] [recurrence: 1][^item-decision-33]
- The fix generalizes because it moves the decision to the right abstraction layer: [confidence: explicit] [recurrence: 1][^item-decision-34]
- - `quality decision duplicates = 0` [confidence: explicit] [recurrence: 1][^item-decision-35]
- - `quality_decisions` duplicate trace rows: `1,418,340 -> 0` [confidence: explicit] [recurrence: 1][^item-decision-36]
- The plan needs to decide a few product-level choices before I can make it decision-complete. [confidence: explicit] [recurrence: 1][^item-decision-37]
- Using targeted repo inspection to ground the `Network` screen plan before locking visual/build decisions. [confidence: explicit] [recurrence: 1][^item-decision-38]
- A few last decisions will make the plan implementable without guesswork: chat behavior, evidence panel behavior, and how much inference we allow into the first data backfill. [confidence: explicit] [recurrence: 1][^item-decision-39]
- I’ve got the current graph path and your latest decisions. [confidence: explicit] [recurrence: 1][^item-decision-40]
- Your other decisions imply a strong default landing model: [confidence: explicit] [recurrence: 1][^item-decision-41]
- The background runner made foreground inspection awkward, so I’m running one explicit foreground batch next to see the actual insert decision path from the current code. [confidence: explicit] [recurrence: 1][^item-decision-42]
- I’m going to run one foreground batch with the current code so I can see the actual post-patch decision path immediately, then I’ll hand control back to the monitor. [confidence: explicit] [recurrence: 1][^item-decision-43]
- The reviewed pool is not actually `no`-heavy right now: labeled decisions are `36 yes / 31 no`. [confidence: explicit] [recurrence: 1][^item-decision-44]
- The actual human `yes/no` decisions live in `experiment_judge_calibration_labels`, not the items table. [confidence: explicit] [recurrence: 1][^item-decision-45]
- - admission decision [confidence: explicit] [recurrence: 1][^item-decision-46]
- I’m inspecting that inserted case now before restarting the background loop, because the next decision depends on whether this is a genuinely good human case or another semantically wrong accept. [confidence: explicit] [recurrence: 1][^item-decision-47]
- - `saliva results -> risk_safety_decisions` [confidence: explicit] [recurrence: 1][^item-decision-48]
- - `domain = risk_safety_decisions` [confidence: explicit] [recurrence: 1][^item-decision-49]
- - `risk_safety_decisions / descriptive` [confidence: explicit] [recurrence: 1][^item-decision-50]

## Sources
[^claim-1]: items open-brain:decision:7d5e949ab4244662; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6648-6651; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6760-6763; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20919-20922
[^claim-2]: items open-brain:decision:2b59dc35e9326921; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^claim-3]: items open-brain:decision:eb622fa20778b52a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2634-2634; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638
[^claim-4]: items open-brain:decision:910fcbf5d216df26; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^claim-5]: items open-brain:decision:0c274afb4836d334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^claim-6]: items open-brain:decision:fd91505e3c28e07e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 246-257
[^item-decision-1]: items open-brain:decision:7d5e949ab4244662; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6648-6651; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6760-6763; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20919-20922
[^item-decision-2]: items open-brain:decision:96676ca76a1b9102; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 29906-29913; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31955-31962; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 39787-39792
[^item-decision-3]: items open-brain:decision:2b59dc35e9326921; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-decision-4]: items open-brain:decision:eb622fa20778b52a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2634-2634; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638
[^item-decision-5]: items open-brain:decision:856262d525fee182; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-decision-6]: items open-brain:decision:86b40cdaa36510f7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-decision-7]: items open-brain:decision:910fcbf5d216df26; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-decision-8]: items open-brain:decision:8eb41dc129a061a6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-decision-9]: items open-brain:decision:e3cde8df3cd9e052; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-decision-10]: items open-brain:decision:0c274afb4836d334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-decision-11]: items open-brain:decision:fd91505e3c28e07e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 246-257
[^item-decision-12]: items open-brain:decision:4a41e46348148a73; 019d837d-d249-71c3-9637-b8d6992ce805 lines 19-21
[^item-decision-13]: items open-brain:decision:0fa42401edc3f9ef; 019d837d-d249-71c3-9637-b8d6992ce805 lines 19-21
[^item-decision-14]: items open-brain:decision:f52c6c9ef35bbfd9; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-decision-15]: items open-brain:decision:4c471421a8ddd1d6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-decision-16]: items open-brain:decision:43af01d23ebdce00; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85331-85339
[^item-decision-17]: items open-brain:decision:afe5d2ed984e48ad; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85300-85312
[^item-decision-18]: items open-brain:decision:78cb8434919f1d15; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84001-84004; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84007-84007; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84008-84010
[^item-decision-19]: items open-brain:decision:a2884527df964377; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 83992-83998
[^item-decision-20]: items open-brain:decision:70687b8703fa9774; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 83694-83699
[^item-decision-21]: items open-brain:decision:dcc9d4a8f0e5383d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 83613-83619
[^item-decision-22]: items open-brain:decision:d392e8e6d346e71e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 83595-83603
[^item-decision-23]: items open-brain:decision:140849f6fa0823ba; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 83474-83484
[^item-decision-24]: items open-brain:decision:e977c61c797a1939; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-decision-25]: items open-brain:decision:08565d517f1f7a4c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-decision-26]: items open-brain:decision:31333dd43c860860; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-decision-27]: items open-brain:decision:53a9bca03f8bf7cc; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82818-82824
[^item-decision-28]: items open-brain:decision:1652293d49c80c32; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82808-82816
[^item-decision-29]: items open-brain:decision:ae8ac60fed7c141b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82715-82715; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82716-82720
[^item-decision-30]: items open-brain:decision:57da7d638f70862c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 78303-78308
[^item-decision-31]: items open-brain:decision:e3e88055d1df31a6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 77331-77334; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 77337-77337; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 77338-77340
[^item-decision-32]: items open-brain:decision:0f9b6654ab1d6f16; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 77284-77290
[^item-decision-33]: items open-brain:decision:115f0f73231278ba; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 77231-77231; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 77232-77236
[^item-decision-34]: items open-brain:decision:b3f9057a56b40065; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 76137-76142
[^item-decision-35]: items open-brain:decision:0b553a14d265dc70; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 75564-75564; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 75565-75568
[^item-decision-36]: items open-brain:decision:f3afe0e05a4f31b7; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 75564-75564; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 75565-75568
[^item-decision-37]: items open-brain:decision:e592335b734891e5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72432-72444
[^item-decision-38]: items open-brain:decision:ead9d10ebec2c1fa; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72424-72430
[^item-decision-39]: items open-brain:decision:832038b3bcd5107b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71685-71692
[^item-decision-40]: items open-brain:decision:206c00b11aa65918; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71685-71692
[^item-decision-41]: items open-brain:decision:b8eb5827400c9367; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71675-71679
[^item-decision-42]: items open-brain:decision:38424bed483a2e89; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 64753-64759
[^item-decision-43]: items open-brain:decision:9069f634b61231b1; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 64737-64745
[^item-decision-44]: items open-brain:decision:c717181acb993b53; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 64306-64312
[^item-decision-45]: items open-brain:decision:0df8b1cf6a28a822; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 64296-64304
[^item-decision-46]: items open-brain:decision:ab447f46fdfe5622; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 64131-64136
[^item-decision-47]: items open-brain:decision:4cf67725bddb0676; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 63539-63549
[^item-decision-48]: items open-brain:decision:280411ac44d56ef6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 59485-59490
[^item-decision-49]: items open-brain:decision:4d3db55a7cdb5a4f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 59171-59171; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 59172-59176
[^item-decision-50]: items open-brain:decision:79c90bd3faa98243; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 59139-59144
