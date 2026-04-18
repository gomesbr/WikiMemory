---
title: "AI Scientist"
page_id: "projects/ai-scientist/index"
domain: "ai-scientist"
bucket: "index"
page_type: "domain_index"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:28:33.307185Z
source_count: 2
claim_count: 8
tags:
  - wikimemory
  - project
  - ai-scientist
  - index
---
# AI Scientist

Navigation: [[projects/ai-scientist/index|AI Scientist]] | [[projects/ai-scientist/communication-preferences|AI Scientist - Communication Preferences]] | [[projects/ai-scientist/workflow-rules|AI Scientist - Workflow Rules]] | [[projects/ai-scientist/architecture|AI Scientist - Architecture]] | [[projects/ai-scientist/code-map|AI Scientist - Code Map]] | [[projects/ai-scientist/current-state|AI Scientist - Current State]] | [[projects/ai-scientist/tasks|AI Scientist - Tasks]] | [[projects/ai-scientist/outcomes|AI Scientist - Outcomes]] | [[projects/ai-scientist/failures|AI Scientist - Failures]] | [[projects/ai-scientist/decisions|AI Scientist - Decisions]] | [[projects/ai-scientist/next-steps|AI Scientist - Next Steps]] | [[projects/ai-scientist/open-questions|AI Scientist - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- The AI Scientist project has established workflow rules that include not asking to score weak benchmark cases and not approving reasoning modes that are incorrect despite valid questions or evidence. [latent: workflow_norms] [confidence: strong][^claim-1]
- The architecture of the AI Scientist project emphasizes the integration of communication preferences, decision-making processes, and the use of large language models to enhance recall of implicit knowledge. [latent: architecture_synthesis] [confidence: strong][^claim-2]
- The current state of the AI Scientist system indicates that it is functioning correctly and meeting its operational goals. [latent: current_state_synthesis] [confidence: strong][^claim-3]
- The project has identified several tasks and next steps, including the need to enforce evidence-family caps and the introduction of a representative-slice rebalance pass. [latent: implicit_next_steps] [confidence: inferred][^claim-4]

## Workflow Rules
Related page: [[projects/ai-scientist/workflow-rules|AI Scientist - Workflow Rules]]
- The AI Scientist project has established workflow rules that include not asking to score weak benchmark cases and not approving reasoning modes that are incorrect despite valid questions or evidence. [latent: workflow_norms] [confidence: strong][^claim-5]

### Preview Items
- `21` still do not [confidence: strong] [recurrence: 1]
- do not ask you to score weak benchmark cases [confidence: strong] [recurrence: 1]
- if the question/evidence are fine but the **reasoning mode is wrong**, do **not** approve it [confidence: strong] [recurrence: 1]

## Architecture
Related page: [[projects/ai-scientist/architecture|AI Scientist - Architecture]]
- The architecture of the AI Scientist project emphasizes the integration of communication preferences, decision-making processes, and the use of large language models to enhance recall of implicit knowledge. [latent: architecture_synthesis] [confidence: strong][^claim-6]

### Preview Items
- `communication_preference`, `do_rule`, `dont_rule`, `workflow_rule`, `decision`, `architecture_note`, `code_location`, `current_state`, `... [confidence: strong] [recurrence: 1]
- Introducing an LLM in Phase 5 now would mainly buy you better recall on messy, implicit knowledge: it can pull out decisions, preferences... [confidence: strong] [recurrence: 1]
- What makes systems like DeepMind’s automated research pipelines or Sakana’s AI Scientist compelling is that they explicitly operate on te... [confidence: strong] [recurrence: 1]

## Code Map
Related page: [[projects/ai-scientist/code-map|AI Scientist - Code Map]]
- No synthesized section summary yet.

### Preview Items
- - `bootstrap/projects/ai-scientist.md` [confidence: explicit] [recurrence: 1]

## Current State
Related page: [[projects/ai-scientist/current-state|AI Scientist - Current State]]
- The current state of the AI Scientist system indicates that it is functioning correctly and meeting its operational goals. [latent: current_state_synthesis] [confidence: strong][^claim-7]

### Preview Items
- Right now the system is doing the correct thing: [confidence: strong] [recurrence: 1]

## Tasks
Related page: [[projects/ai-scientist/tasks|AI Scientist - Tasks]]
- The project has identified several tasks and next steps, including the need to enforce evidence-family caps and the introduction of a representative-slice rebalance pass. [latent: implicit_next_steps] [confidence: inferred][^claim-8]

### Preview Items
- Should Phase 5 use this fixed v1 item taxonomy? [confidence: inferred] [recurrence: 1]
- adding [confidence: inferred] [recurrence: 1]
- It will enforce evidence-family caps in `critical/certification`, promote diverse donor cases into those sets, and then I’ll run it on th... [confidence: inferred] [recurrence: 1]
- I’m adding a representative-slice rebalance pass now. [confidence: inferred] [recurrence: 1]
- One high-impact gap remains before I lock the plan: the current reviewed benchmark has essentially no real `clarify_required` slice. [confidence: inferred] [recurrence: 1]

## Failures
Related page: [[projects/ai-scientist/failures|AI Scientist - Failures]]
- No synthesized section summary yet.

### Preview Items
- `communication_preference`, `do_rule`, `dont_rule`, `workflow_rule`, `decision`, `architecture_note`, `code_location`, `current_state`, `... [confidence: strong] [recurrence: 1]
- Should temporal items like `current_state`, `next_step`, `outcome`, and `failure` carry a lifecycle marker such as: [confidence: strong] [recurrence: 1]
- **The broader failure mode** [confidence: strong] [recurrence: 1]
- - **generator-quality failures** [confidence: strong] [recurrence: 1]
- - not **owner-calibration failures** [confidence: strong] [recurrence: 1]

## Decisions
Related page: [[projects/ai-scientist/decisions|AI Scientist - Decisions]]
- No synthesized section summary yet.

### Preview Items
- `communication_preference`, `do_rule`, `dont_rule`, `workflow_rule`, `decision`, `architecture_note`, `code_location`, `current_state`, `... [confidence: explicit] [recurrence: 1]
- I need these last decisions before I lock the Phase 5 plan: [confidence: explicit] [recurrence: 1]
- Introducing an LLM in Phase 5 now would mainly buy you better recall on messy, implicit knowledge: it can pull out decisions, preferences... [confidence: explicit] [recurrence: 1]
- - only cases with `admissionDecision.admitted = true` [confidence: explicit] [recurrence: 1]
- - the main issue is that several `Yes` decisions approved cases where the **question/evidence are okay, but the lens is wrong** [confidence: explicit] [recurrence: 1]

## Next Steps
Related page: [[projects/ai-scientist/next-steps|AI Scientist - Next Steps]]
- No synthesized section summary yet.

### Preview Items
- Introducing an LLM in Phase 5 now would mainly buy you better recall on messy, implicit knowledge: it can pull out decisions, preferences... [confidence: strong] [recurrence: 1]
- It will enforce evidence-family caps in `critical/certification`, promote diverse donor cases into those sets, and then I’ll run it on th... [confidence: strong] [recurrence: 1]

## Open Questions
Related page: [[projects/ai-scientist/open-questions|AI Scientist - Open Questions]]
- No synthesized section summary yet.

### Preview Items
- For contradictory extracted items, should Phase 5: [confidence: strong] [recurrence: 1]
- For Phase 5, the main implication is that extracted items should carry stable domain/item identifiers and future page-target hints cleanl... [confidence: strong] [recurrence: 1]
- should [confidence: strong] [recurrence: 1]
- Should Phase 5 use this fixed v1 item taxonomy? [confidence: strong] [recurrence: 1]
- Should temporal items like `current_state`, `next_step`, `outcome`, and `failure` carry a lifecycle marker such as: [confidence: strong] [recurrence: 1]

## Sources
[^claim-1]: items ai-scientist:dont_rule:44eabf42b1bd9ba3, ai-scientist:dont_rule:c4581cfbd41cf024, ai-scientist:dont_rule:fb7bb58bfd669516; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43654-43654; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43654-43654; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43343-43347
[^claim-2]: items ai-scientist:architecture_note:fcb46026457060e9, ai-scientist:architecture_note:d48bd10f9d650d5a, ai-scientist:architecture_note:da933550fc717b9f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 973-976; 019d837d-d249-71c3-9637-b8d6992ce805 lines 973-976; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31377-31377; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31378-31381
[^claim-3]: items ai-scientist:current_state:b1957aca678312a2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43654-43654
[^claim-4]: items ai-scientist:task_request:965bab3206a0dc32, ai-scientist:task_request:8486b027ce7b7537, ai-scientist:task_request:171942b1e8cc8773; 019d837d-d249-71c3-9637-b8d6992ce805 lines 973-976; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 48261-48262; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 48261-48262
[^claim-5]: items ai-scientist:dont_rule:44eabf42b1bd9ba3, ai-scientist:dont_rule:c4581cfbd41cf024, ai-scientist:dont_rule:fb7bb58bfd669516; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43654-43654; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43654-43654; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43343-43347
[^claim-6]: items ai-scientist:architecture_note:fcb46026457060e9, ai-scientist:architecture_note:d48bd10f9d650d5a, ai-scientist:architecture_note:da933550fc717b9f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 973-976; 019d837d-d249-71c3-9637-b8d6992ce805 lines 973-976; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31377-31377; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31378-31381
[^claim-7]: items ai-scientist:current_state:b1957aca678312a2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43654-43654
[^claim-8]: items ai-scientist:task_request:965bab3206a0dc32, ai-scientist:task_request:8486b027ce7b7537, ai-scientist:task_request:171942b1e8cc8773; 019d837d-d249-71c3-9637-b8d6992ce805 lines 973-976; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 48261-48262; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 48261-48262
