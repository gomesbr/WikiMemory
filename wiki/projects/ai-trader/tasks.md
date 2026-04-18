---
title: "AI Trader - Tasks"
page_id: "projects/ai-trader/tasks"
domain: "ai-trader"
bucket: "tasks"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:27:44.634369Z
source_count: 74
claim_count: 7
tags:
  - wikimemory
  - project
  - ai-trader
  - bucket
  - tasks
---
# AI Trader - Tasks

Navigation: [[projects/ai-trader/index|AI Trader]] | [[projects/ai-trader/communication-preferences|AI Trader - Communication Preferences]] | [[projects/ai-trader/workflow-rules|AI Trader - Workflow Rules]] | [[projects/ai-trader/architecture|AI Trader - Architecture]] | [[projects/ai-trader/code-map|AI Trader - Code Map]] | [[projects/ai-trader/current-state|AI Trader - Current State]] | [[projects/ai-trader/outcomes|AI Trader - Outcomes]] | [[projects/ai-trader/failures|AI Trader - Failures]] | [[projects/ai-trader/decisions|AI Trader - Decisions]] | [[projects/ai-trader/next-steps|AI Trader - Next Steps]] | [[projects/ai-trader/open-questions|AI Trader - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- The skill should be used when users want to create a new skill or update an existing skill that extends Codex's capabilities with specialized knowledge, workflows, or tool integrations. [latent: project_identity_and_scope] [confidence: inferred][^claim-1]
- Idempotency and state guards should be added where duplication can occur. [latent: implicit_dos_and_donts] [confidence: inferred][^claim-2]
- Decomposition items should be implementable in single focused story runs. [latent: workflow_norms] [confidence: inferred][^claim-3]
- Do not choose a quick workaround if a fundamental fix is feasible in this iteration. [latent: implicit_dos_and_donts] [confidence: inferred][^claim-4]

## Task Request
- If implementation reveals additional engineering follow-ups, append this machine block. [latent: implicit_next_steps] [confidence: inferred][^claim-5]
- If something fails, report root cause, fix rationale, and evidence that the failure cannot recur via the same path. [latent: recurring_failure_patterns] [confidence: inferred][^claim-6]
- Prefer fundamental, root-cause fixes over quick symptom patches. [latent: implicit_dos_and_donts] [confidence: inferred][^claim-7]

### Canonical Items
- This skill should be used when users want to create a new skill (or update an existing skill) that extends Codex's capabilities with specialized knowledge, workflows, or tool integrations. [confidence: inferred] [status: active] [recurrence: 61][^item-task_request-1]
- - Add idempotency/state guards where duplication can occur [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-2]
- - Decomposition items should be implementable in single focused story runs. [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-3]
- - Do not choose a quick workaround if a fundamental fix is feasible in this iteration. [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-4]
- - If implementation reveals additional engineering follow-ups, append this machine block: [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-5]
- - If something fails, report root cause, fix rationale, and evidence that the failure cannot recur via the same path. [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-6]
- - Prefer fundamental, root-cause fixes over quick symptom patches. [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-7]
- - Provide implementation plans or code-level guidance for requested build tasks. [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-8]
- - Return concise root cause, fix applied, and verification output. [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-9]
- - State why chosen fix is durable [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-10]
- - Use first-principles debugging: identify root cause and implement durable fixes with regression coverage instead of quick local patches. [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-11]
- - Work in feature branches and prepare changes for PR review. [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-12]
- Add verification: [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-13]
- Create a complete coder spec with these sections: [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-14]
- Description: Build complete implementation spec packs for coder execution. [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-15]
- Description: Diagnose root cause from first principles and implement robust test-backed fixes over quick patches. [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-16]
- only split into additional stories/follow-up tasks when clearly necessary. [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-17]
- Prefer systemic fixes over local patches: [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-18]
- TRACKER_UPDATES: ```json [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-19]
- Use this doctrine whenever addressing failures, instability, or repeated operational friction. [confidence: inferred] [status: active] [recurrence: 17][^item-task_request-20]
- Description: Break a requirement into ordered,atomic implementation stories. [confidence: inferred] [status: active] [recurrence: 14][^item-task_request-21]
- - Implement only what is needed for this request. [confidence: inferred] [status: active] [recurrence: 10][^item-task_request-22]
- - Requested behavior is implemented end-to-end. [confidence: inferred] [status: active] [recurrence: 10][^item-task_request-23]
- Additional Notes: [confidence: inferred] [status: active] [recurrence: 10][^item-task_request-24]
- Clarify and restate implementation target. [confidence: inferred] [status: active] [recurrence: 10][^item-task_request-25]
- Implement code changes. [confidence: inferred] [status: active] [recurrence: 10][^item-task_request-26]
- - Treat configured `CODER_WORKDIR` and `CODER_ADD_DIRS` as writable by default [confidence: inferred] [status: active] [recurrence: 8][^item-task_request-27]
- Do not ask user for additional access there. [confidence: inferred] [status: active] [recurrence: 8][^item-task_request-28]
- - Implement or investigate only what is required for this request. [confidence: inferred] [status: active] [recurrence: 6][^item-task_request-29]
- Implement/fix minimally. [confidence: inferred] [status: active] [recurrence: 6][^item-task_request-30]
- create [confidence: inferred] [status: active] [recurrence: 5][^item-task_request-31]
- reviewing [confidence: inferred] [status: active] [recurrence: 5][^item-task_request-32]
- Fix rationale [confidence: inferred] [status: active] [recurrence: 4][^item-task_request-33]
- 3) If access fails, return exact blocker(s) and the minimum concrete fix needed. [confidence: inferred] [status: active] [recurrence: 4][^item-task_request-34]
- adding [confidence: inferred] [status: active] [recurrence: 3][^item-task_request-35]
- Fixed. [confidence: inferred] [status: active] [recurrence: 3][^item-task_request-36]
- File updated: [confidence: inferred] [status: active] [recurrence: 3][^item-task_request-37]
- review [confidence: inferred] [status: active] [recurrence: 3][^item-task_request-38]
- implementing [confidence: inferred] [status: active] [recurrence: 3][^item-task_request-39]
- - Add a `Completion Matrix` section. [confidence: inferred] [status: active] [recurrence: 3][^item-task_request-40]
- Implemented. [confidence: inferred] [status: active] [recurrence: 3][^item-task_request-41]
- - Escalate: missing access/tool/runtime blockers with exact error and minimum fix. [confidence: inferred] [status: active] [recurrence: 3][^item-task_request-42]
- 1) create the runbook. [confidence: inferred] [status: active] [recurrence: 3][^item-task_request-43]
- updated_at [confidence: inferred] [status: active] [recurrence: 3][^item-task_request-44]
- - Added endpoints: [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-45]
- Implemented end-to-end. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-46]
- - Pass only if output directly addresses the delegated task objective and acceptance criteria. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-47]
- Specialist output to review: [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-48]
- You are acting as reviewer 'coder' in an internal quality gate for strategist delegation. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-49]
- {"pass":true|false,"confidence":"high|medium|low","issues":["..."],"requiredFixes":["..."],"approvedSummary":"..."} [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-50]
- Implementation plan: [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-51]
- ### What I fixed [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-52]
- Please create new ones and only mark done when the work os completed [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-53]
- I’ll orchestrate and do final review [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-54]
- Go to the log, understand the ask and create the runbook. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-55]
- rejected by user approval settings' and PowerShell Add-Content was 'blocked by policy'. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-56]
- - Do not ask for additional inputs. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-57]
- Remember, you are the strategist that will create the trade cards, so It is your decision to know what kind of data you need inside the application. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-58]
- fixes [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-59]
- Root cause found and fixed. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-60]
- implement [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-61]
- Updated files: [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-62]
- created_at [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-63]
- update [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-64]
- TRACKER_UPDATES: ```json [ {"taskId":"self","status":"awaiting_approval"} ] ``` [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-65]
- fixing [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-66]
- Updated file: [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-67]
- Implemented exactly as requested. [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-68]
- addeventlistener [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-69]
- ### Files updated [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-70]
- updates [confidence: inferred] [status: active] [recurrence: 2][^item-task_request-71]
- I’m starting the real full-corpus load now and I’ll handle it phase by phase, fixing only root-cause issues if they show up and stopping only on completion or the 10GB derived-data cap. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-72]
- - fix real issues when they appeared [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-73]
- - rerun the same phase after each fix [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-74]
- - then report the actual per-phase outcomes, fixes made, sizes, and counts [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-75]
- I implemented infrastructure for the loop instead of performing the requested full run. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-76]
- - Everything went well for the **implementation/test run**, not for a real full-corpus execution. [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-77]
- - I fixed that by making the failure metric **corpus-based and stable across reruns** [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-78]
- - I fixed that by making the gate inspect the **persisted corpus outputs** holistically [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-79]
- - Issues I hit while implementing: [confidence: inferred] [status: active] [recurrence: 1][^item-task_request-80]

## Sources
[^claim-1]: items ai-trader:task_request:03f2e3bd1641e763; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-2]: items ai-trader:task_request:e88536899d8eeac1; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-3]: items ai-trader:task_request:8883c0c204db6b13; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-4]: items ai-trader:task_request:bd8bf5e28cc564ab; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-5]: items ai-trader:task_request:b9033d6f58a25d9d; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-6]: items ai-trader:task_request:d1f5389f8c14a256; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-7]: items ai-trader:task_request:808c48353ab5954b; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-1]: items ai-trader:task_request:03f2e3bd1641e763; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-task_request-2]: items ai-trader:task_request:e88536899d8eeac1; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-3]: items ai-trader:task_request:8883c0c204db6b13; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-4]: items ai-trader:task_request:bd8bf5e28cc564ab; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-5]: items ai-trader:task_request:b9033d6f58a25d9d; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-6]: items ai-trader:task_request:d1f5389f8c14a256; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-7]: items ai-trader:task_request:808c48353ab5954b; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-8]: items ai-trader:task_request:ebea07a78731f3a4; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-9]: items ai-trader:task_request:930340ed3cedbff2; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-10]: items ai-trader:task_request:a7471d55e82dd4be; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-11]: items ai-trader:task_request:a62057559703ce82; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-12]: items ai-trader:task_request:099e148c3d838626; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-13]: items ai-trader:task_request:83882dbbc6ec3631; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-14]: items ai-trader:task_request:6455105044d578c3; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-15]: items ai-trader:task_request:e5145d2db68bdfb6; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-16]: items ai-trader:task_request:388330e5486fb4a9; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-17]: items ai-trader:task_request:b64cc77a329da55a; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-18]: items ai-trader:task_request:0c3174e39162b22c; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-19]: items ai-trader:task_request:d0d42a2bb68f02c3; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 47-53
[^item-task_request-20]: items ai-trader:task_request:d8b4310888ee22a1; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-21]: items ai-trader:task_request:14995e7e92b44711; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-task_request-22]: items ai-trader:task_request:60d20e4e62580e74; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-task_request-23]: items ai-trader:task_request:a15a85d846f8d82f; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-task_request-24]: items ai-trader:task_request:047c07ebb5940033; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-task_request-25]: items ai-trader:task_request:e1ce1f4af2ec67c3; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-task_request-26]: items ai-trader:task_request:b14da891b5882f23; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-task_request-27]: items ai-trader:task_request:d25619f59309fe03; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 5-5; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 6-8; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 16-16
[^item-task_request-28]: items ai-trader:task_request:3fe602385b2f0018; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 5-5; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 6-8; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 16-16
[^item-task_request-29]: items ai-trader:task_request:22da4e43765f4868; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54; 019ca705-c215-7221-8e6a-d28b922add82 lines 55-58; 019ca705-c215-7221-8e6a-d28b922add82 lines 88-88
[^item-task_request-30]: items ai-trader:task_request:1d472de6921ee724; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54; 019ca705-c215-7221-8e6a-d28b922add82 lines 55-58; 019ca705-c215-7221-8e6a-d28b922add82 lines 88-88
[^item-task_request-31]: items ai-trader:task_request:c7bfa986a5d95715; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2294-2318; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 7520-7530; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 9468-9487
[^item-task_request-32]: items ai-trader:task_request:dad4383abf1f03e9; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 13499-13506; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 14249-14256; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 17898-17904
[^item-task_request-33]: items ai-trader:task_request:2759e52df1f7d5c4; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 413-413; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 414-417; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 461-463
[^item-task_request-34]: items ai-trader:task_request:325d3e6bbf8818be; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-task_request-35]: items ai-trader:task_request:8f74563b1ab9708e; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3719-3726; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4846-4847; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 6080-6080
[^item-task_request-36]: items ai-trader:task_request:55b4b1ce0652494c; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3801-3819; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4483-4500; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 7891-7908
[^item-task_request-37]: items ai-trader:task_request:1b34422b52d8b384; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3469-3473; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4303-4317; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4318-4321
[^item-task_request-38]: items ai-trader:task_request:7e9002f8706d2025; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1808-1812; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 12714-12721; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 17597-17603
[^item-task_request-39]: items ai-trader:task_request:b3dde22ca2b46735; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 827-828; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 5365-5368; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 9127-9128
[^item-task_request-40]: items ai-trader:task_request:ad9f2177b43084ad; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 1058-1058; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 1059-1062; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 16-16
[^item-task_request-41]: items ai-trader:task_request:3de31d667edd5549; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1606-1626; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1627-1630; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2233-2233
[^item-task_request-42]: items ai-trader:task_request:1f4277435edff859; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 5-5; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 6-9; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 1058-1058
[^item-task_request-43]: items ai-trader:task_request:12a5cffdf0677a10; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 5-5; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 6-8; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 16-16
[^item-task_request-44]: items ai-trader:task_request:9a2618710b8da88e; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3703-3707; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 9587-9594; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 9739-9746
[^item-task_request-45]: items ai-trader:task_request:92c69c41dab4fd72; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 8345-8349; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1790-1790; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1791-1794
[^item-task_request-46]: items ai-trader:task_request:7b44ef3d98b00c3b; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 8345-8349; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1790-1790; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1791-1794
[^item-task_request-47]: items ai-trader:task_request:eb7212f136618818; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 5-5; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 6-8; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 16-16
[^item-task_request-48]: items ai-trader:task_request:4992ab735ff315cd; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 5-5; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 6-8; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 16-16
[^item-task_request-49]: items ai-trader:task_request:39c111f2f430bbdd; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 5-5; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 6-8; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 16-16
[^item-task_request-50]: items ai-trader:task_request:4c4078aebbe3e28e; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 5-5; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 6-8; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 16-16
[^item-task_request-51]: items ai-trader:task_request:fc9f8d444d2a93d7; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2413-2443; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 9198-9198; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 9199-9202
[^item-task_request-52]: items ai-trader:task_request:a2a54c3c6700277f; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 11156-11156; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 11157-11160; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 12307-12311
[^item-task_request-53]: items ai-trader:task_request:45fbf51bdaaadb1f; 019cb162-d216-7f63-9eb0-f7c9cd446990 lines 5-5; 019cb162-d216-7f63-9eb0-f7c9cd446990 lines 6-8; 019cb166-459d-7a01-a948-70994c21d327 lines 5-5
[^item-task_request-54]: items ai-trader:task_request:2404661734b884e8; 019cab4e-ab00-7e31-b50f-faff8205252f lines 5-5; 019cab4e-ab00-7e31-b50f-faff8205252f lines 6-9; 019cb148-7e62-79a3-af96-9f74a1edaa78 lines 5-5
[^item-task_request-55]: items ai-trader:task_request:62ce06d88528fbd5; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 218-218; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 219-221; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 262-262
[^item-task_request-56]: items ai-trader:task_request:5b61db6a2e3559e4; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 213-213; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 214-217; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 206-206
[^item-task_request-57]: items ai-trader:task_request:1cf0e5148a427e3c; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 262-262; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 263-265; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 5-5
[^item-task_request-58]: items ai-trader:task_request:6affd791326c3220; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 218-218; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 219-221; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 262-262
[^item-task_request-59]: items ai-trader:task_request:6693e08cf31704ce; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 12739-12740; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 11154-11155; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 19559-19560
[^item-task_request-60]: items ai-trader:task_request:95c8318802694b32; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 10058-10064; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 15901-15907; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 18313-18318
[^item-task_request-61]: items ai-trader:task_request:b79dc8acea1e2340; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 14215-14216; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 16866-16867; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 16611-16612
[^item-task_request-62]: items ai-trader:task_request:107dea2e24220561; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4539-4543; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4853-4875; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 5928-5932
[^item-task_request-63]: items ai-trader:task_request:71a09b937846d256; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 8994-9016; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 11705-11711; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 11712-11730
[^item-task_request-64]: items ai-trader:task_request:fdd6b1e7d8adab27; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 5072-5078; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 6229-6231; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 6501-6517
[^item-task_request-65]: items ai-trader:task_request:a2eec996391a2522; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 131-131; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 132-135; 019caaa7-2fe4-7a72-9693-6b998656746e lines 5-5
[^item-task_request-66]: items ai-trader:task_request:4d7289d39072a60c; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 13925-13926; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1255-1256; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 5569-5570
[^item-task_request-67]: items ai-trader:task_request:e3a9c7bf7ce821f5; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3667-3687; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4423-4441; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4483-4500
[^item-task_request-68]: items ai-trader:task_request:e8ce1f5f70a257e6; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4828-4832; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 6844-6848; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 10238-10242
[^item-task_request-69]: items ai-trader:task_request:2b7751ea9b1109af; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 6918-6924; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 7000-7006; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 8012-8018
[^item-task_request-70]: items ai-trader:task_request:8092293fb1341502; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4655-4659; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4721-4725; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 7836-7849
[^item-task_request-71]: items ai-trader:task_request:3b18f167a8690d06; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 686-701; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 7305-7306; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 6072-6073
[^item-task_request-72]: items ai-trader:task_request:aa52e5ec0a83781d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4524-4540
[^item-task_request-73]: items ai-trader:task_request:73d07c9aaad2b795; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4511-4519
[^item-task_request-74]: items ai-trader:task_request:21f7f8094c91df33; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4511-4519
[^item-task_request-75]: items ai-trader:task_request:b6c2e2d508b81413; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4511-4519
[^item-task_request-76]: items ai-trader:task_request:db22558da45b1111; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4511-4519
[^item-task_request-77]: items ai-trader:task_request:002efa90a3ddc473; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4505-4505; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4506-4510
[^item-task_request-78]: items ai-trader:task_request:6e5ed4a289b9172f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4505-4505; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4506-4510
[^item-task_request-79]: items ai-trader:task_request:f943f1c8c3d1109f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4505-4505; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4506-4510
[^item-task_request-80]: items ai-trader:task_request:7f8b001e42a572be; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4505-4505; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4506-4510
