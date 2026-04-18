---
title: "Open Brain"
page_id: "projects/open-brain/index"
domain: "open-brain"
bucket: "index"
page_type: "domain_index"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:32:57.861970Z
source_count: 4
claim_count: 28
tags:
  - wikimemory
  - project
  - open-brain
  - index
---
# Open Brain

Navigation: [[projects/open-brain/index|Open Brain]] | [[projects/open-brain/communication-preferences|Open Brain - Communication Preferences]] | [[projects/open-brain/workflow-rules|Open Brain - Workflow Rules]] | [[projects/open-brain/architecture|Open Brain - Architecture]] | [[projects/open-brain/code-map|Open Brain - Code Map]] | [[projects/open-brain/current-state|Open Brain - Current State]] | [[projects/open-brain/tasks|Open Brain - Tasks]] | [[projects/open-brain/outcomes|Open Brain - Outcomes]] | [[projects/open-brain/failures|Open Brain - Failures]] | [[projects/open-brain/decisions|Open Brain - Decisions]] | [[projects/open-brain/next-steps|Open Brain - Next Steps]] | [[projects/open-brain/open-questions|Open Brain - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- The project emphasizes the importance of fixing the root filter to avoid cleaning out useful cases. [latent: implicit_dos_and_donts] [confidence: strong][^claim-1]
- There is a gap in good human cases in stale inventory, which affects the cleanup process. [latent: implicit_dos_and_donts] [confidence: strong][^claim-2]
- The project aims to avoid creating a complex new subsystem for cleanup processes. [latent: implicit_dos_and_donts] [confidence: strong][^claim-3]

## Workflow Rules
Related page: [[projects/open-brain/workflow-rules|Open Brain - Workflow Rules]]
- If we don’t fix that root filter, we’ll keep cleaning good junk out and then failing to bring back the right kinds of cases. [latent: implicit_dos_and_donts] [confidence: strong][^claim-4]
- The remaining gap is coming from supply shape, not cleanup correctness: we don’t have enough good human cases in stale inventory. [latent: implicit_dos_and_donts] [confidence: strong][^claim-5]
- Do not add a new UI module in this phase. [latent: implicit_dos_and_donts] [confidence: strong][^claim-6]

### Preview Items
- If we don’t fix that root filter, we’ll keep cleaning good junk out and then failing to bring back the right kinds of cases. [confidence: strong] [recurrence: 1]
- The remaining gap is coming from supply shape, not cleanup correctness: we don’t have enough good human cases in stale inventory, so clea... [confidence: strong] [recurrence: 1]
- That gives us the retroactive “don’t make me review this junk again” behavior without turning cleanup into a giant new subsystem. [confidence: strong] [recurrence: 1]
- Do not add a new UI module in this phase. [confidence: strong] [recurrence: 1]
- Keep cheaper deterministic screening for obvious rejects and anchor sufficiency, but do not let deterministic paraphrase logic remain the... [confidence: strong] [recurrence: 1]

## Architecture
Related page: [[projects/open-brain/architecture|Open Brain - Architecture]]
- Prefer generalizable architecture over one-off patches. [latent: architecture_synthesis] [confidence: strong][^claim-7]
- The `component_registry` is an important aspect of the architecture. [latent: architecture_synthesis] [confidence: strong][^claim-8]

### Preview Items
- - Prefer generalizable architecture over one-off patches. [confidence: strong] [recurrence: 2]
- component_performance [confidence: strong] [recurrence: 1]
- `component_registry` [confidence: strong] [recurrence: 1]
- `component_pair_performance` [confidence: strong] [recurrence: 1]
- `strategy_component_bindings` [confidence: strong] [recurrence: 1]

## Code Map
Related page: [[projects/open-brain/code-map|Open Brain - Code Map]]
- No synthesized section summary yet.

### Preview Items
- - loop_2efee43d-c2a8-48a6-aeb4-cb947357c6ac.log: OpenBrain/generated/strategy_program/loop_2efee43d-c2a8-48a6-aeb4-cb947357c6ac.log [confidence: explicit] [recurrence: 2]
- - sms_state_2efee43d-c2a8-48a6-aeb4-cb947357c6ac.json: OpenBrain/generated/strategy_program/sms_state_2efee43d-c2a8-48a6-aeb4-cb947357c6a... [confidence: explicit] [recurrence: 2]
- - `OpenBrain/README.md` [confidence: explicit] [recurrence: 2]
- - prod-grok-backend.json: c:\Users\Fabio\AppData\Local\Temp\e2ddf759-eba7-489f-8946-d78e822532bd_6496f4fc-d714-437a-bcbc-a845241a02b7.zip... [confidence: explicit] [recurrence: 2]
- - Loop log: `OpenBrain/generated/strategy_program/loop_b922379a-73be-44a8-891e-d635c9ed1ab0.log` [confidence: explicit] [recurrence: 2]

## Current State
Related page: [[projects/open-brain/current-state|Open Brain - Current State]]
- Right now I only want to create the knowledge for those 3 projects, but there will be more projects in the future I'd like to build wikis for. [latent: current_state_synthesis] [confidence: strong][^claim-9]
- There are currently `86` `.jsonl` files. [latent: current_state_synthesis] [confidence: strong][^claim-10]
- One active file is currently locked for ordinary reads, which reinforces your append-aware requirement. [latent: current_state_synthesis] [confidence: strong][^claim-11]

### Preview Items
- Right now I only want to create the knowledge for those 3 projects, but there will be more projects in the future I'd like to build wikis... [confidence: strong] [recurrence: 1]
- - There are currently `86` `.jsonl` files. [confidence: strong] [recurrence: 1]
- One active file is currently locked for ordinary reads, which reinforces your append-aware requirement. [confidence: strong] [recurrence: 1]
- I currently assume it stops before full JSON parsing and only does discovery, identity, manifesting, and processing-state tracking. [confidence: strong] [recurrence: 1]
- I’ve confirmed the stem logic is half-upgraded right now, so I’m finishing that plumbing first. [confidence: strong] [recurrence: 1]

## Tasks
Related page: [[projects/open-brain/tasks|Open Brain - Tasks]]
- PLEASE IMPLEMENT THIS PLAN: [latent: implicit_next_steps] [confidence: inferred][^claim-12]
- Avoid one-off domain hints and fixed thresholds as primary logic. [latent: implicit_next_steps] [confidence: inferred][^claim-13]
- Do not add large new schema/process complexity to solve one edge case. [latent: implicit_next_steps] [confidence: inferred][^claim-14]

### Preview Items
- PLEASE IMPLEMENT THIS PLAN: [confidence: inferred] [recurrence: 2]
- - Avoid one-off domain hints and fixed thresholds as primary logic. [confidence: inferred] [recurrence: 2]
- - Do not add large new schema/process complexity to solve one edge case. [confidence: inferred] [recurrence: 2]
- - Do not rename files, functions, or variables unless required for the fix. [confidence: inferred] [recurrence: 2]
- - Fix with minimal output. [confidence: inferred] [recurrence: 2]

## Outcomes
Related page: [[projects/open-brain/outcomes|Open Brain - Outcomes]]
- For actively growing files, should the system process only fully completed lines and leave any partial trailing line untouched until the next run? [latent: partially_explicit_open_questions] [confidence: strong][^claim-15]
- I’ve finished the gap math. [latent: current_state_synthesis] [confidence: strong][^claim-16]
- Now that this change is done, can you run the retroactive cleanup to check if the pending review cases are up to standard? [latent: partially_explicit_open_questions] [confidence: strong][^claim-17]

### Preview Items
- For actively growing files, should the system process only fully completed lines and leave any partial trailing line untouched until the... [confidence: strong] [recurrence: 1]
- I’ve finished the gap math. [confidence: strong] [recurrence: 1]
- it left the pool half-pruned before refill completed. [confidence: strong] [recurrence: 1]
- I’m aligning that request shape now so the refill can use the intended model successfully. [confidence: strong] [recurrence: 1]
- Now that this change is done, can you run the retroactive cleanup to check if the pending review cases are up to standard [confidence: strong] [recurrence: 1]

## Failures
Related page: [[projects/open-brain/failures|Open Brain - Failures]]
- Example pattern: "data linkage issue" vs "one bad graph node". [latent: recurring_failure_patterns] [confidence: strong][^claim-18]
- Identify the broader failure mode. [latent: recurring_failure_patterns] [confidence: strong][^claim-19]
- Implement the fix at the right abstraction layer so similar issues are also prevented. [latent: recurring_failure_patterns] [confidence: strong][^claim-20]

### Preview Items
- - Example pattern: "data linkage issue" vs "one bad graph node". [confidence: strong] [recurrence: 2]
- - Identify the broader failure mode. [confidence: strong] [recurrence: 2]
- - Implement the fix at the right abstraction layer so similar issues are also prevented. [confidence: strong] [recurrence: 2]
- - State the underlying class of failure, not the single symptom. [confidence: strong] [recurrence: 2]
- When fixing a bug: [confidence: strong] [recurrence: 2]

## Decisions
Related page: [[projects/open-brain/decisions|Open Brain - Decisions]]
- Locked Decisions are documented for clarity. [latent: decision_synthesis] [confidence: strong][^claim-21]
- Current repo state and the Phase 1-6 decisions are enough to lock Phase 7. [latent: decision_synthesis] [confidence: strong][^claim-22]
- The decision to transition from `decision` to `decisions` is noted. [latent: decision_synthesis] [confidence: strong][^claim-23]

### Preview Items
- ## Locked Decisions [confidence: explicit] [recurrence: 1]
- reviewdecision [confidence: explicit] [recurrence: 1]
- - `current_state`, `decision`, `architecture_note`, `task_request`, `next_step`, `open_question`, `failure`, project-scoped rules [confidence: explicit] [recurrence: 1]
- Current repo state and the Phase 1-6 decisions are enough to lock Phase 7. [confidence: explicit] [recurrence: 1]
- - `decision` -> `decisions` [confidence: explicit] [recurrence: 1]

## Next Steps
Related page: [[projects/open-brain/next-steps|Open Brain - Next Steps]]
- I’m making the minimal runtime fix and then I’ll run the focused Phase 7 suite to catch any remaining issues. [latent: implicit_next_steps] [confidence: strong][^claim-24]
- Introducing an LLM in Phase 5 now would mainly buy you better recall on messy, implicit knowledge. [latent: implicit_next_steps] [confidence: strong][^claim-25]
- I’ll wait for your answers, then I’ll refine Phase 1 and only after that produce the detailed Phase 1 plan. [latent: implicit_next_steps] [confidence: strong][^claim-26]

### Preview Items
- I’m making the minimal runtime fix and then I’ll run the focused Phase 7 suite to catch any remaining issues. [confidence: strong] [recurrence: 1]
- - temporal items: `active > historical > superseded`, then last_seen desc [confidence: strong] [recurrence: 1]
- Introducing an LLM in Phase 5 now would mainly buy you better recall on messy, implicit knowledge: it can pull out decisions, preferences... [confidence: strong] [recurrence: 1]
- I’m grounding Phase 2 in the current `WikiMemory` state and the real trace structure first, then I’ll ask only the normalization decision... [confidence: strong] [recurrence: 1]
- I’ll wait for your answers, then I’ll refine Phase 1 and only after that produce the detailed Phase 1 plan. [confidence: strong] [recurrence: 1]

## Open Questions
Related page: [[projects/open-brain/open-questions|Open Brain - Open Questions]]
- Should we explain how the change generalizes beyond the immediate example? [latent: partially_explicit_open_questions] [confidence: strong][^claim-27]
- Show how evidence links to actors, timestamps, and context. [latent: partially_explicit_open_questions] [confidence: strong][^claim-28]

### Preview Items
- should [confidence: strong] [recurrence: 2]
- Why: [confidence: strong] [recurrence: 2]
- - Explain how the change generalizes beyond the immediate example. [confidence: strong] [recurrence: 2]
- - Show how evidence links to actors, timestamps, and context. [confidence: strong] [recurrence: 2]
- - Solve the class of problem, not just the exact example shown. [confidence: strong] [recurrence: 2]

## Sources
[^claim-1]: items open-brain:dont_rule:b3c5b1269df003e2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86141-86152
[^claim-2]: items open-brain:dont_rule:84552e87048eb43f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85820-85828
[^claim-3]: items open-brain:dont_rule:29d7b2e0cd37f2da; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85253-85264
[^claim-4]: items open-brain:dont_rule:b3c5b1269df003e2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86141-86152
[^claim-5]: items open-brain:dont_rule:84552e87048eb43f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85820-85828
[^claim-6]: items open-brain:dont_rule:4e93ef3675605b2b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84001-84004; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84007-84007; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84008-84010
[^claim-7]: items open-brain:architecture_note:ba3e4d767bf8af2c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-8]: items open-brain:architecture_note:4beda0bb4b4f276f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31363-31366; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31407-31410; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31431-31434
[^claim-9]: items open-brain:current_state:46f59a53b84dfb86; 019d837d-d249-71c3-9637-b8d6992ce805 lines 95-97
[^claim-10]: items open-brain:current_state:9be580847d907a4f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^claim-11]: items open-brain:current_state:7c2d8253cd6c3472; 019d837d-d249-71c3-9637-b8d6992ce805 lines 53-61
[^claim-12]: items open-brain:task_request:017361725bf6cd20; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3847-3847; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3848-3850; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 9318-9318
[^claim-13]: items open-brain:task_request:55ff0320459be3d3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-14]: items open-brain:task_request:05f604c681ec5630; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-15]: items open-brain:outcome:9aaf19c68e8ff0e0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^claim-16]: items open-brain:outcome:76f8b9259a0e5266; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87223-87230
[^claim-17]: items open-brain:outcome:943a832b19fc4ad5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85454-85457
[^claim-18]: items open-brain:failure:9d16f84343f86972; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-19]: items open-brain:failure:54f56486df5e778c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-20]: items open-brain:failure:6b056873095a1b28; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-21]: items open-brain:decision:7d5e949ab4244662; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6648-6651; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6760-6763; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20919-20922
[^claim-22]: items open-brain:decision:eb622fa20778b52a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2634-2634; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638
[^claim-23]: items open-brain:decision:856262d525fee182; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^claim-24]: items open-brain:next_step:41b6953d3dcac215; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2857-2870
[^claim-25]: items open-brain:next_step:799ee148372a62de; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^claim-26]: items open-brain:next_step:3130e45447ac2895; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^claim-27]: items open-brain:open_question:92bc866d058a855d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-28]: items open-brain:open_question:130d625e58d39f19; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
