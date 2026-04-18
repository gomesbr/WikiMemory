---
title: "AI Trader - Open Questions"
page_id: "projects/ai-trader/open-questions"
domain: "ai-trader"
bucket: "open-questions"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:07:53.582734Z
source_count: 74
claim_count: 7
tags:
  - wikimemory
  - project
  - ai-trader
  - bucket
  - open-questions
---
# AI Trader - Open Questions

Navigation: [[projects/ai-trader/index|AI Trader]] | [[projects/ai-trader/communication-preferences|AI Trader - Communication Preferences]] | [[projects/ai-trader/workflow-rules|AI Trader - Workflow Rules]] | [[projects/ai-trader/architecture|AI Trader - Architecture]] | [[projects/ai-trader/code-map|AI Trader - Code Map]] | [[projects/ai-trader/current-state|AI Trader - Current State]] | [[projects/ai-trader/tasks|AI Trader - Tasks]] | [[projects/ai-trader/outcomes|AI Trader - Outcomes]] | [[projects/ai-trader/failures|AI Trader - Failures]] | [[projects/ai-trader/decisions|AI Trader - Decisions]] | [[projects/ai-trader/next-steps|AI Trader - Next Steps]]
Related Domains: [[global/index|Global]]

## Summary
- There are several open questions regarding how to effectively use skills in the AI Trader project. [latent: implicit_next_steps] [confidence: strong][^claim-1]
- Users should announce which skill(s) they are using and the reason for their choice. [latent: implicit_dos_and_donts] [confidence: strong][^claim-2]
- Progressive disclosure is recommended for explaining how to use a skill. [latent: workflow_norms] [confidence: strong][^claim-3]
- Specific trigger rules dictate when a skill must be used based on user input or task description. [latent: workflow_norms] [confidence: strong][^claim-4]

## Open Question
- If a user skips an obvious skill, they should explain why. [latent: implicit_dos_and_donts] [confidence: strong][^claim-5]
- A skill should be used when creating or updating skills that extend Codex's capabilities. [latent: project_identity_and_scope] [confidence: strong][^claim-6]
- Decomposition items should be implementable in single focused story runs. [latent: workflow_norms] [confidence: strong][^claim-7]

### Canonical Items
- ### How to use skills [confidence: strong] [status: active] [recurrence: 61][^item-open_question-1]
- - Announce which skill(s) you're using and why (one short line). [confidence: strong] [status: active] [recurrence: 61][^item-open_question-2]
- - How to use a skill (progressive disclosure): [confidence: strong] [status: active] [recurrence: 61][^item-open_question-3]
- - Trigger rules: If the user names a skill (with `$SkillName` or plain text) OR the task clearly matches a skill's description shown above, you must use that skill for that turn. [confidence: strong] [status: active] [recurrence: 61][^item-open_question-4]
- If you skip an obvious skill, say why. [confidence: strong] [status: active] [recurrence: 61][^item-open_question-5]
- This skill should be used when users want to create a new skill (or update an existing skill) that extends Codex's capabilities with specialized knowledge, workflows, or tool integrations. [confidence: strong] [status: active] [recurrence: 61][^item-open_question-6]
- - Decomposition items should be implementable in single focused story runs. [confidence: strong] [status: active] [recurrence: 17][^item-open_question-7]
- - If status is `blocked`, `blockerReason` is mandatory and must state exactly what user input/access is required. [confidence: strong] [status: active] [recurrence: 17][^item-open_question-8]
- - State why chosen fix is durable [confidence: strong] [status: active] [recurrence: 17][^item-open_question-9]
- [{"title":"<task title>","description":"<what/why>","status":"backlog|ready|blocked","priority":"low|normal|high","agent":"coder","blockerReason":"<required only for blocked>"}] [confidence: strong] [status: active] [recurrence: 17][^item-open_question-10]
- Cases should be stable, minimal, and sensitive to regressions in behavior. [confidence: strong] [status: active] [recurrence: 17][^item-open_question-11]
- Output should be concise, explicit, and directly usable inside a spec pack. [confidence: strong] [status: active] [recurrence: 15][^item-open_question-12]
- - Each item should be atomic and independently verifiable. [confidence: strong] [status: active] [recurrence: 14][^item-open_question-13]
- <story title> - <what changes> - <evidence> [confidence: strong] [status: active] [recurrence: 14][^item-open_question-14]
- - Implement only what is needed for this request. [confidence: strong] [status: active] [recurrence: 10][^item-open_question-15]
- - Implement or investigate only what is required for this request. [confidence: strong] [status: active] [recurrence: 6][^item-open_question-16]
- should [confidence: strong] [status: active] [recurrence: 5][^item-open_question-17]
- ### What I changed [confidence: strong] [status: active] [recurrence: 5][^item-open_question-18]
- ### What changed [confidence: strong] [status: active] [recurrence: 4][^item-open_question-19]
- 3) How urgent is this (now, today, this week)... [confidence: strong] [status: active] [recurrence: 4][^item-open_question-20]
- To make sure I hit the mark this time: 1) What exactly do you want me to try again (task/deliverable)? [confidence: strong] [status: active] [recurrence: 4][^item-open_question-21]
- why [confidence: strong] [status: active] [recurrence: 3][^item-open_question-22]
- What to do now: [confidence: strong] [status: active] [recurrence: 3][^item-open_question-23]
- - [2026-03-01T18:17:38.581Z] (user) No, just read my previous text about the workflow and tell me what you think [confidence: strong] [status: active] [recurrence: 3][^item-open_question-24]
- What I learned: [confidence: strong] [status: active] [recurrence: 2][^item-open_question-25]
- **What It Does** [confidence: strong] [status: active] [recurrence: 2][^item-open_question-26]
- ### What I fixed [confidence: strong] [status: active] [recurrence: 2][^item-open_question-27]
- What I verified: [confidence: strong] [status: active] [recurrence: 2][^item-open_question-28]
- - Do not explain how to use the agent. [confidence: strong] [status: active] [recurrence: 2][^item-open_question-29]
- - What are you talking about? [confidence: strong] [status: active] [recurrence: 2][^item-open_question-30]
- Remember, you are the strategist that will create the trade cards, so It is your decision to know what kind of data you need inside the application. [confidence: strong] [status: active] [recurrence: 2][^item-open_question-31]
- - [2026-02-28T20:21:32.072Z] (user) Hey bot, can you check why the coder can’t access the AITrader folder since he has access to the root folder (Projects)? [confidence: strong] [status: active] [recurrence: 2][^item-open_question-32]
- What to do: [confidence: strong] [status: active] [recurrence: 2][^item-open_question-33]
- I think you need more knowledge of the features in the trader app so you can understand what you and the team needs to inforce and what the app will enforce deterministically. [confidence: strong] [status: active] [recurrence: 2][^item-open_question-34]
- The coder should know to to circumvent that since it knows those are windows powershell commands. [confidence: strong] [status: active] [recurrence: 2][^item-open_question-35]
- A couple quick confirmations so I handle this correctly: 1) Which tracker should I operate on: our in-chat CodexClaw task tracker here, or an external tool (Notion/Jira/etc.)? [confidence: strong] [status: active] [recurrence: 2][^item-open_question-36]
- - I will then tell you what I believe your intention was for AITrader and what my role is in it. [confidence: strong] [status: active] [recurrence: 2][^item-open_question-37]
- Quick confirmers: 1) Should I prioritize Data Map v1 for Trade Cards, Peter DiCarlo strategy research, or run both in parallel? [confidence: strong] [status: active] [recurrence: 2][^item-open_question-38]
- ### What you should do now [confidence: strong] [status: active] [recurrence: 2][^item-open_question-39]
- **What I added** [confidence: strong] [status: active] [recurrence: 2][^item-open_question-40]
- How can I help today? [confidence: strong] [status: active] [recurrence: 2][^item-open_question-41]
- How can I help with CodexClaw today? [confidence: strong] [status: active] [recurrence: 2][^item-open_question-42]
- User says: Hey, how are you? [confidence: strong] [status: active] [recurrence: 2][^item-open_question-43]
- User message: Hey, how are you? [confidence: strong] [status: active] [recurrence: 2][^item-open_question-44]
- I’m starting the real full-corpus load now and I’ll handle it phase by phase, fixing only root-cause issues if they show up and stopping only on completion or the 10GB derived-data cap. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-45]
- Do what you supposed to do, now! [confidence: strong] [status: active] [recurrence: 1][^item-open_question-46]
- go back to my previous instructions and tell me what you should have done [confidence: strong] [status: active] [recurrence: 1][^item-open_question-47]
- I should have: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-48]
- that is NOT what I've asked you. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-49]
- What I completed was: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-50]
- - What I completed was: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-51]
- what is the final total size, size per phase and record count per phase? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-52]
- what went wrong and what changes did you make to fix it? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-53]
- I found one state-snapshot issue while reviewing the new module: full audit runs should replace prior target state, not carry stale keys forward. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-54]
- - Audit is manifest-first: it does **not** parse rendered wiki/bootstrap markdown beyond what is already represented in manifests. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-55]
- - detect repeated extracted domain items that should already have merged but still appear as separate canonical items [confidence: strong] [status: active] [recurrence: 1][^item-open_question-56]
- - durable item should not be marked stale [confidence: strong] [status: active] [recurrence: 1][^item-open_question-57]
- - no unaffected findings should change ids or timestamps [confidence: strong] [status: active] [recurrence: 1][^item-open_question-58]
- - superseded older temporal item should not produce a contradiction error [confidence: strong] [status: active] [recurrence: 1][^item-open_question-59]
- That means the next fix should be aggressive notice suppression/dedup for low-value weak candidates, not more label tuning. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-60]
- whats next? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-61]
- what is the unclassified cound now? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-62]
- The sample still showed “unchanged” because I’d already invalidated Phase 4 once during the previous pass, so I’m now forcing a clean rerun on the same temp real-data sample and rechecking the actual persisted counts. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-63]
- I’ve got the root fix: the remaining misses are two flavors of low-signal context, and they should be handled by the same inheritance mechanism instead of new domain rules. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-64]
- I’m debugging that override path directly instead of guessing, because those last seven should be mechanically explainable. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-65]
- this should tell us whether Phase 5 is merely less noisy or genuinely under control. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-66]
- I’m moving the filter up to the evidence intake layer so extraction only works from conversational/summary-bearing events, which should cut a whole class of noisy outputs at once. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-67]
- the other shows the code-location filter still needs to reject “example/documentation” prose more aggressively. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-68]
- - More importantly, the live sample shows the current Phase 4/5 heuristics are not production-ready for instruction-heavy sessions: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-69]
- I’m rerunning the full suite once so we keep the repo stable, then I’ll summarize the real-data findings separately from the code fix, because the live sample exposed some quality issues we shouldn’t blur together. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-70]
- I’m running the actual pipeline against your real Codex sessions on a small sample now, and I’ll report exactly what passed and where any real-data issue shows up. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-71]
- Phase 6 should start using llms already. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-72]
- Why the hold up? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-73]
- - but the actual output unit should still be page/domain rebuilds [confidence: strong] [status: active] [recurrence: 1][^item-open_question-74]
- - show them inline with clear markers [confidence: strong] [status: active] [recurrence: 1][^item-open_question-75]
- Do you want overview pages to contain short synthesized summaries, or should Phase 6 stay deterministic and mostly assemble structured extracted items without prose summarization? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-76]
- For temporal content, should page ordering prioritize recency? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-77]
- How should provenance show up in markdown? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-78]
- How visible should conflicts / low-confidence items be in the wiki? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-79]
- Should `cross-project` get its own first-class namespace? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-80]

## Sources
[^claim-1]: items ai-trader:open_question:7ceff77d2b51bfbc; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-2]: items ai-trader:open_question:8665e78469d967e0; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-3]: items ai-trader:open_question:3942f30e4ceacbb8; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-4]: items ai-trader:open_question:92a52a6e7964be67; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-5]: items ai-trader:open_question:362bb8d4b00230e6; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-6]: items ai-trader:open_question:e08f1715a6cd4319; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-7]: items ai-trader:open_question:127b0d432e12ac07; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-open_question-1]: items ai-trader:open_question:7ceff77d2b51bfbc; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-open_question-2]: items ai-trader:open_question:8665e78469d967e0; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-open_question-3]: items ai-trader:open_question:3942f30e4ceacbb8; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-open_question-4]: items ai-trader:open_question:92a52a6e7964be67; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-open_question-5]: items ai-trader:open_question:362bb8d4b00230e6; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-open_question-6]: items ai-trader:open_question:e08f1715a6cd4319; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-open_question-7]: items ai-trader:open_question:127b0d432e12ac07; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-open_question-8]: items ai-trader:open_question:5c1fe2ac70ef4b67; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-open_question-9]: items ai-trader:open_question:18dba11d86953887; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-open_question-10]: items ai-trader:open_question:1e3885cdedfdacea; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-open_question-11]: items ai-trader:open_question:597ed4b4ac0b08bc; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-open_question-12]: items ai-trader:open_question:ea9969a06f08d95a; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-open_question-13]: items ai-trader:open_question:95763cca930dae19; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-open_question-14]: items ai-trader:open_question:03247fa5d1a73686; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-open_question-15]: items ai-trader:open_question:1773732768fc47a5; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-open_question-16]: items ai-trader:open_question:e5a7d39faee279b2; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54; 019ca705-c215-7221-8e6a-d28b922add82 lines 55-58; 019ca705-c215-7221-8e6a-d28b922add82 lines 88-88
[^item-open_question-17]: items ai-trader:open_question:cf8bf799b7e5fe90; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 13-17; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 10720-10724; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 10732-10738
[^item-open_question-18]: items ai-trader:open_question:a0e554df0f8948d2; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1333-1358; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1359-1362; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3776-3780
[^item-open_question-19]: items ai-trader:open_question:bbb3d6d51857ecc3; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1606-1626; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1627-1630; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3414-3416
[^item-open_question-20]: items ai-trader:open_question:003ce9a6387cf97d; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 5-5; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 6-8; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 218-218
[^item-open_question-21]: items ai-trader:open_question:0dd359ddb00c5d8c; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 5-5; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 6-8; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 218-218
[^item-open_question-22]: items ai-trader:open_question:ff4950c23e2f1c40; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 18-21; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 77220-77220; 019d837d-d249-71c3-9637-b8d6992ce805 lines 229-236
[^item-open_question-23]: items ai-trader:open_question:1352adbd25f73a35; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4423-4441; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 838-842; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 9159-9163
[^item-open_question-24]: items ai-trader:open_question:3ef0ea42c23a1439; 019cab13-b21e-76f3-9029-bcd0333cd3eb lines 5-5; 019cab13-b21e-76f3-9029-bcd0333cd3eb lines 6-9; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 218-218
[^item-open_question-25]: items ai-trader:open_question:8b636daf9968e6d9; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 1053-1053; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 1054-1057; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 1065-1065
[^item-open_question-26]: items ai-trader:open_question:1a8147490bc8bc6e; 019c9f43-944f-7403-a8a0-8484dd96dfab lines 102-105; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 2400-2406
[^item-open_question-27]: items ai-trader:open_question:8d89f5c48626a883; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 11156-11156; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 11157-11160; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 12307-12311
[^item-open_question-28]: items ai-trader:open_question:1fb67c8d4126a36d; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 16581-16587; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 450-450; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 451-454
[^item-open_question-29]: items ai-trader:open_question:627e3f2d97cc3c5d; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 262-262; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 263-265; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 5-5
[^item-open_question-30]: items ai-trader:open_question:3e620b1b5efb2c4a; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 218-218; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 219-221; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 262-262
[^item-open_question-31]: items ai-trader:open_question:e7af4a6b2e046671; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 218-218; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 219-221; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 262-262
[^item-open_question-32]: items ai-trader:open_question:6bee616eb933d71f; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 5-5; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 6-9; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 5-5
[^item-open_question-33]: items ai-trader:open_question:775cdadc0633591d; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3469-3473; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 18131-18135
[^item-open_question-34]: items ai-trader:open_question:314aaf77a79cbb5d; 019caaa7-2fe4-7a72-9693-6b998656746e lines 5-5; 019caaa7-2fe4-7a72-9693-6b998656746e lines 6-9; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 5-5
[^item-open_question-35]: items ai-trader:open_question:9fb14a91ecb035f5; 019ca705-c215-7221-8e6a-d28b922add82 lines 88-88; 019ca705-c215-7221-8e6a-d28b922add82 lines 89-92; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 5-5
[^item-open_question-36]: items ai-trader:open_question:b61f0cb8aeca4410; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54; 019ca705-c215-7221-8e6a-d28b922add82 lines 55-58; 019ca705-c215-7221-8e6a-d28b922add82 lines 88-88
[^item-open_question-37]: items ai-trader:open_question:32c929cdf3819bad; 019ca705-c215-7221-8e6a-d28b922add82 lines 88-88; 019ca705-c215-7221-8e6a-d28b922add82 lines 89-92; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-open_question-38]: items ai-trader:open_question:7d126b3092249c32; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-open_question-39]: items ai-trader:open_question:cbbce8cdbe017d9c; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 6333-6347; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 6348-6351; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 10431-10444
[^item-open_question-40]: items ai-trader:open_question:72271bed635ff12e; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2233-2233; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2234-2237; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2802-2830
[^item-open_question-41]: items ai-trader:open_question:6a4bb50d7428a6ff; 019c9d6b-6077-7c33-bb98-d1504ca0d6d4 lines 5-15; 019c9d6f-34ed-7dc1-a7cc-4209d931f215 lines 5-16
[^item-open_question-42]: items ai-trader:open_question:91b611305ba3f8b4; 019c9d5b-b1a6-7fc1-a6c4-c7c8abe77031 lines 11-14; 019c9d6a-1df2-7290-9e8a-1e3b28e2feb9 lines 13-17
[^item-open_question-43]: items ai-trader:open_question:58a3edd91b6e6914; 019c9d57-dec5-7f12-9b7a-20330759fbfd lines 5-10; 019c9d60-390c-7251-8e71-54bb184c5607 lines 5-15
[^item-open_question-44]: items ai-trader:open_question:fd179e42cd22a14f; 019c9d5e-15f7-7483-a5de-bac1f5d3e835 lines 5-8; 019c9d5e-3ea5-7503-a2c9-74d8f75a220b lines 5-8
[^item-open_question-45]: items ai-trader:open_question:7b1a4750168b5e80; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4524-4540
[^item-open_question-46]: items ai-trader:open_question:dbf73513b471f02e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4520-4522
[^item-open_question-47]: items ai-trader:open_question:c61280dc26e966d8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4511-4519
[^item-open_question-48]: items ai-trader:open_question:57dfe066fc6c30e4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4511-4519
[^item-open_question-49]: items ai-trader:open_question:1aac3a8a39629a18; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4511-4519
[^item-open_question-50]: items ai-trader:open_question:4f91519c61e12d4a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4511-4519
[^item-open_question-51]: items ai-trader:open_question:2bb312226768eece; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4505-4505; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4506-4510
[^item-open_question-52]: items ai-trader:open_question:7e4accfefb001322; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4468-4470
[^item-open_question-53]: items ai-trader:open_question:f98d0f1ae7b96698; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4468-4470
[^item-open_question-54]: items ai-trader:open_question:278e798a1a113851; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3083-3094
[^item-open_question-55]: items ai-trader:open_question:b77681031a0ab55b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-open_question-56]: items ai-trader:open_question:dc5c97d7ad33c7fe; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-open_question-57]: items ai-trader:open_question:3abc78ba48ef4b57; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-open_question-58]: items ai-trader:open_question:579f042ff6bc66b6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-open_question-59]: items ai-trader:open_question:6a90e61f0eafe3f8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-open_question-60]: items ai-trader:open_question:0a9ed4bd31d395a7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2494-2502
[^item-open_question-61]: items ai-trader:open_question:6ccfdfaa995d224a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2279-2281
[^item-open_question-62]: items ai-trader:open_question:f02399aae7d85d25; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2270-2278
[^item-open_question-63]: items ai-trader:open_question:bdfe3b7de9cb0188; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2216-2228
[^item-open_question-64]: items ai-trader:open_question:6498fa201b38f567; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2148-2149
[^item-open_question-65]: items ai-trader:open_question:1e948a78ce1a7205; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2065-2070
[^item-open_question-66]: items ai-trader:open_question:bb88946c553918aa; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2035-2051
[^item-open_question-67]: items ai-trader:open_question:7c2128bf1c2608c7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2024-2034
[^item-open_question-68]: items ai-trader:open_question:70fe252e3cf7ee41; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1950-1951
[^item-open_question-69]: items ai-trader:open_question:9d25902a36fccc35; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1824-1824; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1825-1828
[^item-open_question-70]: items ai-trader:open_question:96ff4cccac9fa078; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1810-1815
[^item-open_question-71]: items ai-trader:open_question:6c6d3c95f9436fc8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1610-1624
[^item-open_question-72]: items ai-trader:open_question:7a2a23a80c9ffe65; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1296-1298
[^item-open_question-73]: items ai-trader:open_question:308a1b948ad10f1b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1296-1298
[^item-open_question-74]: items ai-trader:open_question:82dfbe286dea7147; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1290-1290; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1291-1295
[^item-open_question-75]: items ai-trader:open_question:143d36d4dbb3567e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1290-1290; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1291-1295
[^item-open_question-76]: items ai-trader:open_question:ec87c5075f1284cc; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1290-1290; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1291-1295
[^item-open_question-77]: items ai-trader:open_question:8366b3b8ee532294; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1290-1290; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1291-1295
[^item-open_question-78]: items ai-trader:open_question:0087a8f1cb6412e2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1290-1290; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1291-1295
[^item-open_question-79]: items ai-trader:open_question:48e8d5ae2209872d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1290-1290; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1291-1295
[^item-open_question-80]: items ai-trader:open_question:673bc4464deeb7b1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1290-1290; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1291-1295
