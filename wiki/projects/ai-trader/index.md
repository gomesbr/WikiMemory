---
title: "AI Trader"
page_id: "projects/ai-trader/index"
domain: "ai-trader"
bucket: "index"
page_type: "domain_index"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:32:28.162425Z
source_count: 74
claim_count: 12
tags:
  - wikimemory
  - project
  - ai-trader
  - index
---
# AI Trader

Navigation: [[projects/ai-trader/index|AI Trader]] | [[projects/ai-trader/communication-preferences|AI Trader - Communication Preferences]] | [[projects/ai-trader/workflow-rules|AI Trader - Workflow Rules]] | [[projects/ai-trader/architecture|AI Trader - Architecture]] | [[projects/ai-trader/code-map|AI Trader - Code Map]] | [[projects/ai-trader/current-state|AI Trader - Current State]] | [[projects/ai-trader/tasks|AI Trader - Tasks]] | [[projects/ai-trader/outcomes|AI Trader - Outcomes]] | [[projects/ai-trader/failures|AI Trader - Failures]] | [[projects/ai-trader/decisions|AI Trader - Decisions]] | [[projects/ai-trader/next-steps|AI Trader - Next Steps]] | [[projects/ai-trader/open-questions|AI Trader - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- The architecture of AI Trader is based on a multi-agent system and includes runtime components. [latent: architecture_synthesis] [confidence: strong][^claim-1]
- Current state assessments are crucial for verifying the functionality and readiness of AI Trader. [latent: current_state_synthesis] [confidence: strong][^claim-2]

## Workflow Rules
Related page: [[projects/ai-trader/workflow-rules|AI Trader - Workflow Rules]]
- AI Trader has a rule to always issue a warning when necessary. [latent: implicit_dos_and_donts] [confidence: strong][^claim-3]
- Running the targeted suite again is essential to ensure the integrity of Phase 3. [latent: implicit_next_steps] [confidence: strong][^claim-4]
- It is advised to avoid making changes in the middle of a tight explicit chain unless absolutely necessary. [latent: implicit_dos_and_donts] [confidence: strong][^claim-5]

### Preview Items
- always `warning` [confidence: strong] [recurrence: 1]
- Running the targeted suite again now to make sure Phase 3 is solid end to end. [confidence: strong] [recurrence: 1]
- never in the middle of a tight explicit chain unless no better seam exists [confidence: strong] [recurrence: 1]
- Segmentation should optimize for coherent local context, but use a balanced cutoff so segments do not grow too large for downstream class... [confidence: strong] [recurrence: 1]
- For a source whose Phase 1 committed boundary and fingerprint are unchanged, do nothing. [confidence: strong] [recurrence: 1]

## Architecture
Related page: [[projects/ai-trader/architecture|AI Trader - Architecture]]
- The architecture of AI Trader includes a multi-agent framework to enhance functionality. [latent: architecture_synthesis] [confidence: strong][^claim-6]
- Runtime components are a critical part of the AI Trader architecture. [latent: architecture_synthesis] [confidence: strong][^claim-7]
- Constraint architecture must include guidelines for must, must not, prefer, and escalate actions. [latent: architecture_synthesis] [confidence: strong][^claim-8]

### Preview Items
- ## Multi-Agent Architecture [confidence: strong] [recurrence: 36]
- ## Runtime Components [confidence: strong] [recurrence: 36]
- - Constraint Architecture must include Must / Must Not / Prefer / Escalate. [confidence: strong] [recurrence: 17]
- - For other repos/apps, mirror this same token set and component style (colors, grid backdrop, panel/chip styling, typography) so all app... [confidence: strong] [recurrence: 17]
- ## constraint-architecture (C:\Users\Fabio\Cursor AI projects\Projects\CodexClaw\skills\constraint-architecture\SKILL.md) [confidence: strong] [recurrence: 15]

## Code Map
Related page: [[projects/ai-trader/code-map|AI Trader - Code Map]]
- Skills are defined as sets of local instructions stored in SKILL.md files. [latent: codebase_map_abstractions] [confidence: strong][^claim-9]
- The code map includes specific file paths for skill creators and installers. [latent: codebase_map_abstractions] [confidence: strong][^claim-10]

### Preview Items
- A skill is a set of local instructions to follow that is stored in a `SKILL.md` file. [confidence: explicit] [recurrence: 62]
- (file: C:/Users/Fabio/.codex/skills/.system/skill-creator/SKILL.md) [confidence: explicit] [recurrence: 61]
- (file: C:/Users/Fabio/.codex/skills/.system/skill-installer/SKILL.md) [confidence: explicit] [recurrence: 61]
- src/trading/scheduler.ts [confidence: explicit] [recurrence: 39]
- src/agents/runner.ts [confidence: explicit] [recurrence: 39]

## Current State
Related page: [[projects/ai-trader/current-state|AI Trader - Current State]]
- Verifying the current state before retrying actions is a recommended practice. [latent: current_state_synthesis] [confidence: strong][^claim-11]
- The current state includes awaiting approvals for specific tasks, indicating active project management. [latent: current_state_synthesis] [confidence: strong][^claim-12]

### Preview Items
- Reproduce or inspect current state. [confidence: strong] [recurrence: 6]
- verify current state before retrying. [confidence: strong] [recurrence: 2]
- Currently awaiting your CLI: - Approve Peter DiCarlo deep-dive (research) — need yes/no to start and any scope limits. [confidence: strong] [recurrence: 2]
- I’ve confirmed the real blocker risk up front: there is currently no `OPENAI_API_KEY` in this shell, so Phases 6-7 may hard-stop later. [confidence: strong] [recurrence: 1]
- Status in this workspace right now: [confidence: strong] [recurrence: 1]

## Tasks
Related page: [[projects/ai-trader/tasks|AI Trader - Tasks]]
- No synthesized section summary yet.

### Preview Items
- This skill should be used when users want to create a new skill (or update an existing skill) that extends Codex's capabilities with spec... [confidence: inferred] [recurrence: 61]
- - Add idempotency/state guards where duplication can occur [confidence: inferred] [recurrence: 17]
- - Decomposition items should be implementable in single focused story runs. [confidence: inferred] [recurrence: 17]
- - Do not choose a quick workaround if a fundamental fix is feasible in this iteration. [confidence: inferred] [recurrence: 17]
- - If implementation reveals additional engineering follow-ups, append this machine block: [confidence: inferred] [recurrence: 17]

## Outcomes
Related page: [[projects/ai-trader/outcomes|AI Trader - Outcomes]]
- No synthesized section summary yet.

### Preview Items
- [{"taskId":"self","status":"backlog|ready|in_progress|blocked|awaiting_approval|auto_merge_pending|done","blockerReason":"<optional>"}] [confidence: strong] [recurrence: 17]
- [{"taskId":"self","status":"done"}] [confidence: strong] [recurrence: 11]
- - Build/tests run successfully or blockers are clearly reported. [confidence: strong] [recurrence: 10]
- - [2026-03-01T03:18:50.145Z] (assistant) Outcome - Coder outcome for “Ok, this is my request”: Completed: request received and delivered... [confidence: strong] [recurrence: 5]
- Done. [confidence: strong] [recurrence: 4]

## Failures
Related page: [[projects/ai-trader/failures|AI Trader - Failures]]
- No synthesized section summary yet.

### Preview Items
- - Safety and fallback: If a skill can't be applied cleanly (missing files, unclear instructions), state the issue, pick the next-best app... [confidence: strong] [recurrence: 61]
- - If something fails, report root cause, fix rationale, and evidence that the failure cannot recur via the same path. [confidence: strong] [recurrence: 17]
- - Use first-principles debugging: identify root cause and implement durable fixes with regression coverage instead of quick local patches. [confidence: strong] [recurrence: 17]
- Define the failure precisely: [confidence: strong] [recurrence: 17]
- Failure Playbook [confidence: strong] [recurrence: 17]

## Decisions
Related page: [[projects/ai-trader/decisions|AI Trader - Decisions]]
- No synthesized section summary yet.

### Preview Items
- - `strategist`: orchestration and final decision communication [confidence: explicit] [recurrence: 36]
- - Only request user input when truly blocked by missing access/data/decision. [confidence: explicit] [recurrence: 17]
- - Remove ambiguity in routing/decision contracts [confidence: explicit] [recurrence: 17]
- Decision standard: [confidence: explicit] [recurrence: 17]
- decision [confidence: explicit] [recurrence: 4]

## Next Steps
Related page: [[projects/ai-trader/next-steps|AI Trader - Next Steps]]
- No synthesized section summary yet.

### Preview Items
- - If implementation reveals additional engineering follow-ups, append this machine block: [confidence: strong] [recurrence: 17]
- - Strengthen invariants and ownership boundaries [confidence: strong] [recurrence: 17]
- only split into additional stories/follow-up tasks when clearly necessary. [confidence: strong] [recurrence: 17]
- **Next step** [confidence: strong] [recurrence: 3]
- - I will then tell you what I believe your intention was for AITrader and what my role is in it. [confidence: strong] [recurrence: 2]

## Open Questions
Related page: [[projects/ai-trader/open-questions|AI Trader - Open Questions]]
- No synthesized section summary yet.

### Preview Items
- ### How to use skills [confidence: strong] [recurrence: 61]
- - Announce which skill(s) you're using and why (one short line). [confidence: strong] [recurrence: 61]
- - How to use a skill (progressive disclosure): [confidence: strong] [recurrence: 61]
- - Trigger rules: If the user names a skill (with `$SkillName` or plain text) OR the task clearly matches a skill's description shown abov... [confidence: strong] [recurrence: 61]
- If you skip an obvious skill, say why. [confidence: strong] [recurrence: 61]

## Sources
[^claim-1]: items ai-trader:architecture_note:e47dd819dd28e612, ai-trader:architecture_note:ee70e96a7701b57e, ai-trader:architecture_note:292489bfa18f9c2c, ai-trader:architecture_note:d0908719f9f4f947, ai-trader:architecture_note:4709e352d9a4e845; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-2]: items ai-trader:current_state:94406c24318bd45c, ai-trader:current_state:66fb79dd3d510ea2, ai-trader:current_state:19707aeb9f6d05b8, ai-trader:current_state:faed67f677b1d6e9, ai-trader:current_state:772a0c96003416a8; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54; 019ca705-c215-7221-8e6a-d28b922add82 lines 55-58; 019ca705-c215-7221-8e6a-d28b922add82 lines 88-88; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 22-23; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 30-30; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 14336-14336; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 468-468; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4524-4540; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4505-4505; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4506-4510
[^claim-3]: items ai-trader:do_rule:08e345b15367cc6c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^claim-4]: items ai-trader:do_rule:e139cdfe313a089c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 698-713
[^claim-5]: items ai-trader:dont_rule:09dd786c755b21a0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 541-544; 019d837d-d249-71c3-9637-b8d6992ce805 lines 547-547; 019d837d-d249-71c3-9637-b8d6992ce805 lines 548-549
[^claim-6]: items ai-trader:architecture_note:e47dd819dd28e612; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-7]: items ai-trader:architecture_note:ee70e96a7701b57e; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-8]: items ai-trader:architecture_note:292489bfa18f9c2c; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-9]: items ai-trader:code_location:83d54b094551d701; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4
[^claim-10]: items ai-trader:code_location:a6ed6e22c239d7eb, ai-trader:code_location:d8c39ff74733f2be; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-11]: items ai-trader:current_state:66fb79dd3d510ea2; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 22-23; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 30-30; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 14336-14336
[^claim-12]: items ai-trader:current_state:19707aeb9f6d05b8; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 468-468
