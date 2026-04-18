---
title: "Cross-Project - Workflow Rules"
page_id: "projects/cross-project/workflow-rules"
domain: "cross-project"
bucket: "workflow-rules"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:33:22.818240Z
source_count: 1
claim_count: 7
tags:
  - wikimemory
  - cross-project
  - cross-project
  - bucket
  - workflow-rules
---
# Cross-Project - Workflow Rules

Navigation: [[projects/cross-project/index|Cross-Project]] | [[projects/cross-project/communication-preferences|Cross-Project - Communication Preferences]] | [[projects/cross-project/architecture|Cross-Project - Architecture]] | [[projects/cross-project/code-map|Cross-Project - Code Map]] | [[projects/cross-project/current-state|Cross-Project - Current State]] | [[projects/cross-project/tasks|Cross-Project - Tasks]] | [[projects/cross-project/outcomes|Cross-Project - Outcomes]] | [[projects/cross-project/failures|Cross-Project - Failures]] | [[projects/cross-project/decisions|Cross-Project - Decisions]] | [[projects/cross-project/next-steps|Cross-Project - Next Steps]] | [[projects/cross-project/open-questions|Cross-Project - Open Questions]]
Related Domains: [[projects/ai-trader/index|AI Trader]], [[projects/open-brain/index|Open Brain]]

## Summary
- Understanding the whole system is crucial to ensure that changes do not break anything else. [latent: implicit_dos_and_donts] [confidence: strong][^claim-1]
- Removing data is a terrible idea if the purpose of that data is not understood. [latent: implicit_dos_and_donts] [confidence: strong][^claim-2]
- If data deletions are necessary, ensure they are executed properly. [latent: implicit_dos_and_donts] [confidence: strong][^claim-3]
- Always verify that the system is not in mock mode before making changes. [latent: implicit_dos_and_donts] [confidence: strong][^claim-4]

## Do Rule
- Login page should always appear on open and reload. [latent: workflow_norms] [confidence: strong][^claim-5]
- Refresh behavior should always re-prompt for login. [latent: workflow_norms] [confidence: strong][^claim-6]
- The app should always open to the login page. [latent: workflow_norms] [confidence: strong][^claim-7]

### Canonical Items
- Also, for the other changes, make sure you understand the whole system so this change does not break anything else [confidence: strong] [recurrence: 1][^item-do_rule-1]
- Removing data is always a terrible idea if you don't know what you are doing or WHY that data exists. [confidence: strong] [recurrence: 1][^item-do_rule-2]
- Also if those deletes are needed, make sure they are done [confidence: strong] [recurrence: 1][^item-do_rule-3]
- Make sure is not in mock mode [confidence: strong] [recurrence: 1][^item-do_rule-4]
- also make sure its also clean now [confidence: strong] [recurrence: 1][^item-do_rule-5]
- Login page always appears on open and reload. [confidence: strong] [recurrence: 1][^item-do_rule-6]
- Refresh behavior always re-prompts login. [confidence: strong] [recurrence: 1][^item-do_rule-7]
- App always opens to login page. [confidence: strong] [recurrence: 1][^item-do_rule-8]
- Privacy watermark always visible: `PRIVATE`, `SHARE-SAFE`, or `DEMO`. [confidence: strong] [recurrence: 1][^item-do_rule-9]

## Dont Rule
- No synthesized section summary yet.

### Canonical Items
- `we never did harm each other intentionally. [confidence: strong] [recurrence: 1][^item-dont_rule-1]
- don’t try to minimize your lie!!! [confidence: strong] [recurrence: 1][^item-dont_rule-2]
- if the question/evidence are fine but the **reasoning mode is wrong**, do **not** approve it [confidence: strong] [recurrence: 1][^item-dont_rule-3]
- Removing data is always a terrible idea if you don't know what you are doing or WHY that data exists. [confidence: strong] [recurrence: 1][^item-dont_rule-4]
- capability-only tests (do not require user data presence) [confidence: strong] [recurrence: 1][^item-dont_rule-5]
- Low-confidence artifacts never appear in trusted graph outputs. [confidence: strong] [recurrence: 1][^item-dont_rule-6]
- Don’t prebuild lots of domain-specific tables for every edge case. [confidence: strong] [recurrence: 1][^item-dont_rule-7]
- JSON-escape via serializer (`JSON.stringify`), never manual concatenation [confidence: strong] [recurrence: 1][^item-dont_rule-8]
- Never strip structural symbols [confidence: strong] [recurrence: 1][^item-dont_rule-9]
- Strange, I don't see speed increase, and CPU is lower now. [confidence: strong] [recurrence: 1][^item-dont_rule-10]
- Oh, I don't remember the 3/8. [confidence: strong] [recurrence: 1][^item-dont_rule-11]
- Don't remember if we made changes on it [confidence: strong] [recurrence: 1][^item-dont_rule-12]
- Don't worry about those, run the aggregation load anyways. [confidence: strong] [recurrence: 1][^item-dont_rule-13]
- Demo mode never returns real raw message content or real identifiers. [confidence: strong] [recurrence: 1][^item-dont_rule-14]
- Do not partition immediately under current size. [confidence: strong] [recurrence: 1][^item-dont_rule-15]

## Sources
[^claim-1]: items cross-project:do_rule:fdf1c6f102e218fb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22241-22245
[^claim-2]: items cross-project:do_rule:3fd9c7d861ed83cb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22229-22233
[^claim-3]: items cross-project:do_rule:1fc24033d06cb422; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 18588-18592
[^claim-4]: items cross-project:do_rule:1397bc00b43d2e09; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 12859-12879
[^claim-5]: items cross-project:do_rule:392d9b715ee6851f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5689-5692; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5695-5697
[^claim-6]: items cross-project:do_rule:7264207190952ea0; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5689-5692; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5695-5697
[^claim-7]: items cross-project:do_rule:aa0e820328130094; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5678-5681
[^item-do_rule-1]: items cross-project:do_rule:fdf1c6f102e218fb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22241-22245
[^item-do_rule-2]: items cross-project:do_rule:3fd9c7d861ed83cb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22229-22233
[^item-do_rule-3]: items cross-project:do_rule:1fc24033d06cb422; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 18588-18592
[^item-do_rule-4]: items cross-project:do_rule:1397bc00b43d2e09; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 12859-12879
[^item-do_rule-5]: items cross-project:do_rule:402b15f81b8c7427; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 10153-10171
[^item-do_rule-6]: items cross-project:do_rule:392d9b715ee6851f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5689-5692; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5695-5697
[^item-do_rule-7]: items cross-project:do_rule:7264207190952ea0; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5689-5692; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5695-5697
[^item-do_rule-8]: items cross-project:do_rule:aa0e820328130094; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5678-5681
[^item-do_rule-9]: items cross-project:do_rule:29f159818167ec48; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5678-5681
[^item-dont_rule-1]: items cross-project:dont_rule:6ed6b0f5b361b67e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 49264-49264
[^item-dont_rule-2]: items cross-project:dont_rule:f2b9bf1ff86469b5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 49264-49264
[^item-dont_rule-3]: items cross-project:dont_rule:fb7bb58bfd669516; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43342-43342
[^item-dont_rule-4]: items cross-project:dont_rule:fa951ce8f56fa995; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22229-22233
[^item-dont_rule-5]: items cross-project:dont_rule:f615d742e9bb119a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20924-20924; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20925-20928
[^item-dont_rule-6]: items cross-project:dont_rule:e3a5c1d2be223d26; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20924-20924; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20925-20928
[^item-dont_rule-7]: items cross-project:dont_rule:91ec9c0266f818a8; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20675-20679
[^item-dont_rule-8]: items cross-project:dont_rule:8a1049d298f1d7af; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 17493-17499
[^item-dont_rule-9]: items cross-project:dont_rule:d55f9de17c195bee; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 17493-17499
[^item-dont_rule-10]: items cross-project:dont_rule:a022665c98f15703; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 17181-17198
[^item-dont_rule-11]: items cross-project:dont_rule:c9e5665b66aad451; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 16832-16853
[^item-dont_rule-12]: items cross-project:dont_rule:820068fc07fc2a65; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 12928-12938
[^item-dont_rule-13]: items cross-project:dont_rule:8f1f1a4bdbca143f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11333-11344
[^item-dont_rule-14]: items cross-project:dont_rule:e4793cb9737012cf; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5689-5692; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5695-5697
[^item-dont_rule-15]: items cross-project:dont_rule:a1cd5a0b92dcb5a7; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5689-5692; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5695-5697
