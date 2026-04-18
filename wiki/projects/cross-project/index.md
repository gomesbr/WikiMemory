---
title: "Cross-Project"
page_id: "projects/cross-project/index"
domain: "cross-project"
bucket: "index"
page_type: "domain_index"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:33:16.583496Z
source_count: 3
claim_count: 11
tags:
  - wikimemory
  - cross-project
  - cross-project
  - index
---
# Cross-Project

Navigation: [[projects/cross-project/index|Cross-Project]] | [[projects/cross-project/communication-preferences|Cross-Project - Communication Preferences]] | [[projects/cross-project/workflow-rules|Cross-Project - Workflow Rules]] | [[projects/cross-project/architecture|Cross-Project - Architecture]] | [[projects/cross-project/code-map|Cross-Project - Code Map]] | [[projects/cross-project/current-state|Cross-Project - Current State]] | [[projects/cross-project/tasks|Cross-Project - Tasks]] | [[projects/cross-project/outcomes|Cross-Project - Outcomes]] | [[projects/cross-project/failures|Cross-Project - Failures]] | [[projects/cross-project/decisions|Cross-Project - Decisions]] | [[projects/cross-project/next-steps|Cross-Project - Next Steps]] | [[projects/cross-project/open-questions|Cross-Project - Open Questions]]
Related Domains: [[projects/ai-scientist/index|AI Scientist]], [[projects/ai-trader/index|AI Trader]], [[projects/open-brain/index|Open Brain]]

## Summary
- The cross-project collaboration emphasizes the importance of not causing intentional harm to each other. [latent: implicit_dos_and_donts] [confidence: strong][^claim-1]
- Approval should not be given if the reasoning mode is incorrect, even if the evidence is sound. [latent: implicit_dos_and_donts] [confidence: strong][^claim-2]
- Understanding the entire system is crucial before making changes to avoid breaking functionality. [latent: workflow_norms] [confidence: strong][^claim-3]

## Workflow Rules
Related page: [[projects/cross-project/workflow-rules|Cross-Project - Workflow Rules]]
- Team members should never intentionally harm each other. [latent: implicit_dos_and_donts] [confidence: strong][^claim-4]
- Approval should not be granted if the reasoning mode is incorrect, regardless of the quality of evidence. [latent: implicit_dos_and_donts] [confidence: strong][^claim-5]

### Preview Items
- `we never did harm each other intentionally. [confidence: strong] [recurrence: 1]
- don’t try to minimize your lie!!! [confidence: strong] [recurrence: 1]
- if the question/evidence are fine but the **reasoning mode is wrong**, do **not** approve it [confidence: strong] [recurrence: 1]
- Also, for the other changes, make sure you understand the whole system so this change does not break anything else [confidence: strong] [recurrence: 1]
- Removing data is always a terrible idea if you don't know what you are doing or WHY that data exists. [confidence: strong] [recurrence: 1]

## Architecture
Related page: [[projects/cross-project/architecture|Cross-Project - Architecture]]
- The architecture of the project is being developed to integrate new orchestration into existing systems. [latent: architecture_synthesis] [confidence: strong][^claim-6]
- Current pipeline hooks have been confirmed as part of the architecture setup. [latent: architecture_synthesis] [confidence: strong][^claim-7]
- The architecture is grounded in existing pipeline and rollout hooks to ensure compatibility. [latent: architecture_synthesis] [confidence: strong][^claim-8]

### Preview Items
- architecture [confidence: strong] [recurrence: 1]
- I’m wiring the new full-load orchestration into the existing phase pipeline, state model, and tests first so it stays aligned with the cu... [confidence: strong] [recurrence: 1]
- I’ve confirmed the current pipeline hooks. [confidence: strong] [recurrence: 1]
- I’m grounding in the current pipeline and rollout hooks first so the full-run loop plan matches what the repo can already do and where it... [confidence: strong] [recurrence: 1]
- - Yes, the pipeline is ready for a full run. [confidence: strong] [recurrence: 1]

## Code Map
Related page: [[projects/cross-project/code-map|Cross-Project - Code Map]]
- No synthesized section summary yet.

### Preview Items
- - open_brain_runbook.md: CodexClaw/docs/operations/open_brain_runbook.md [confidence: explicit] [recurrence: 1]
- - runbook.md: CodexClaw/docs/operations/runbook.md [confidence: explicit] [recurrence: 1]
- - strategist.md: CodexClaw/personas/strategist.md [confidence: explicit] [recurrence: 1]
- - research.md: CodexClaw/personas/research.md [confidence: explicit] [recurrence: 1]
- + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetContentCommand [confidence: explicit] [recurrence: 1]

## Current State
Related page: [[projects/cross-project/current-state|Cross-Project - Current State]]
- The current state of the project is actively monitored and documented. [latent: current_state_synthesis] [confidence: strong][^claim-9]
- Current state synthesis includes examples of what is built and what is pending. [latent: current_state_synthesis] [confidence: strong][^claim-10]
- The current repo state indicates that Phase 3 code is in place but lacks certain artifacts. [latent: current_state_synthesis] [confidence: strong][^claim-11]

### Preview Items
- Current state: [confidence: strong] [recurrence: 2]
- Current state synthesis [confidence: strong] [recurrence: 1]
- Examples: what is currently built, what is sample-only, what is still pending, what design direction is currently winning. [confidence: strong] [recurrence: 1]
- I’m checking the current state/CLI patterns first so the extractor follows the same atomic and incremental workflow as the earlier phases. [confidence: strong] [recurrence: 1]
- Current repo state: the Phase 3 code is in place, but there are no persisted `normalized/` or `segmented/` artifacts checked into this re... [confidence: strong] [recurrence: 1]

## Tasks
Related page: [[projects/cross-project/tasks|Cross-Project - Tasks]]
- No synthesized section summary yet.

### Preview Items
- PLEASE IMPLEMENT THIS PLAN: [confidence: inferred] [recurrence: 2]
- that’s fixed. [confidence: inferred] [recurrence: 1]
- - Implemented the pointer-first Phase 2 migration. [confidence: inferred] [recurrence: 1]
- - This fixes the root storage problem: Phase 2 no longer mirrors the raw corpus while preserving exact provenance and on-demand recovery. [confidence: inferred] [recurrence: 1]
- - Validation passed: `73` local tests green (`1` skipped live test by default), and the env-gated real-data live suite passed on the fixe... [confidence: inferred] [recurrence: 1]

## Outcomes
Related page: [[projects/cross-project/outcomes|Cross-Project - Outcomes]]
- No synthesized section summary yet.

### Preview Items
- I’ve finished the migration hooks for classification and extraction. [confidence: strong] [recurrence: 1]
- - last completed phase [confidence: strong] [recurrence: 1]
- - started/finished timestamps [confidence: strong] [recurrence: 1]
- - the top-level refresh report records the last completed phase and the failure point [confidence: strong] [recurrence: 1]
- Examples: tensions or unresolved choices visible across multiple sessions even when no single message says “open question”. [confidence: strong] [recurrence: 1]

## Failures
Related page: [[projects/cross-project/failures|Cross-Project - Failures]]
- No synthesized section summary yet.

### Preview Items
- failure [confidence: strong] [recurrence: 2]
- I’ve patched the real-data failure mode and added a regression test. [confidence: strong] [recurrence: 1]
- I’ve got the exact live failure cluster now. [confidence: strong] [recurrence: 1]
- The live error count is still dropping, which means the fix path is right. [confidence: strong] [recurrence: 1]
- The remaining audit errors are still false contradictions, now from `next_step` and a generic `current_state` pronoun key. [confidence: strong] [recurrence: 1]

## Decisions
Related page: [[projects/cross-project/decisions|Cross-Project - Decisions]]
- No synthesized section summary yet.

### Preview Items
- decision [confidence: explicit] [recurrence: 2]
- ## Locked Decisions [confidence: explicit] [recurrence: 1]
- `quality_decisions` [confidence: explicit] [recurrence: 1]
- I’ve got the tradeoff decisions. [confidence: explicit] [recurrence: 1]
- The main remaining plan decisions are about quality gates, API-backed phases, and how aggressive the autonomous retry loop should be. [confidence: explicit] [recurrence: 1]

## Next Steps
Related page: [[projects/cross-project/next-steps|Cross-Project - Next Steps]]
- No synthesized section summary yet.

### Preview Items
- I’m running the focused extraction/audit tests first, then the env-gated live sample suite. [confidence: strong] [recurrence: 1]
- I’m patching the contradiction policy at the audit layer and the last generic subject-key fallback, then I’ll rerun the targeted and live... [confidence: strong] [recurrence: 1]
- I’ve isolated the remaining live-data gap in Phase 8 and I’m tightening the contradiction policy plus the last generic subject-key cases,... [confidence: strong] [recurrence: 1]
- I’m making the extraction tests use the temp source-roots config end to end, then adding one regression where the signal exists only past... [confidence: strong] [recurrence: 1]
- I’m bumping the Phase 2 schema and then moving straight into the new tests, including the real-data suite. [confidence: strong] [recurrence: 1]

## Open Questions
Related page: [[projects/cross-project/open-questions|Cross-Project - Open Questions]]
- No synthesized section summary yet.

### Preview Items
- **Why** [confidence: strong] [recurrence: 2]
- What changed [confidence: strong] [recurrence: 2]
- should [confidence: strong] [recurrence: 2]
- The main remaining plan decisions are about quality gates, API-backed phases, and how aggressive the autonomous retry loop should be. [confidence: strong] [recurrence: 1]
- I’m grounding in the current pipeline and rollout hooks first so the full-run loop plan matches what the repo can already do and where it... [confidence: strong] [recurrence: 1]

## Sources
[^claim-1]: items cross-project:dont_rule:6ed6b0f5b361b67e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 49264-49264
[^claim-2]: items cross-project:dont_rule:fb7bb58bfd669516; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43342-43342
[^claim-3]: items cross-project:do_rule:fdf1c6f102e218fb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22241-22245
[^claim-4]: items cross-project:dont_rule:6ed6b0f5b361b67e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 49264-49264
[^claim-5]: items cross-project:dont_rule:fb7bb58bfd669516; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43342-43342
[^claim-6]: items cross-project:architecture_note:2dd956131d50b401; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4337-4348
[^claim-7]: items cross-project:architecture_note:7f9d06d89c04c553; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4264-4278
[^claim-8]: items cross-project:architecture_note:0430d86fceb4f4d5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4251-4262
[^claim-9]: items cross-project:current_state:019eff189191b65f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 10436-10461; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^claim-10]: items cross-project:current_state:1ede86080333232e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^claim-11]: items cross-project:current_state:d9db2873945289d7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
