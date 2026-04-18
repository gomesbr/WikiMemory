---
title: "AI Trader - Decisions"
page_id: "projects/ai-trader/decisions"
domain: "ai-trader"
bucket: "decisions"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:07:43.968213Z
source_count: 61
claim_count: 7
tags:
  - wikimemory
  - project
  - ai-trader
  - bucket
  - decisions
---
# AI Trader - Decisions

Navigation: [[projects/ai-trader/index|AI Trader]] | [[projects/ai-trader/communication-preferences|AI Trader - Communication Preferences]] | [[projects/ai-trader/workflow-rules|AI Trader - Workflow Rules]] | [[projects/ai-trader/architecture|AI Trader - Architecture]] | [[projects/ai-trader/code-map|AI Trader - Code Map]] | [[projects/ai-trader/current-state|AI Trader - Current State]] | [[projects/ai-trader/tasks|AI Trader - Tasks]] | [[projects/ai-trader/outcomes|AI Trader - Outcomes]] | [[projects/ai-trader/failures|AI Trader - Failures]] | [[projects/ai-trader/next-steps|AI Trader - Next Steps]] | [[projects/ai-trader/open-questions|AI Trader - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- The strategist is responsible for orchestration and final decision communication. [latent: decision_synthesis] [confidence: strong][^claim-1]
- User input should only be requested when truly blocked by missing access, data, or decision. [latent: decision_synthesis] [confidence: strong][^claim-2]
- Ambiguity in routing and decision contracts should be removed. [latent: decision_synthesis] [confidence: strong][^claim-3]
- A decision standard is established for clarity in decision-making processes. [latent: decision_synthesis] [confidence: strong][^claim-4]

## Decision
- The strategist remains the decision owner throughout the process. [latent: decision_synthesis] [confidence: strong][^claim-5]
- Decisions should be made with a clear understanding of the required data for trade cards. [latent: decision_synthesis] [confidence: strong][^claim-6]
- The status maps should be reproduced directly to ensure precise scope decisions. [latent: decision_synthesis] [confidence: strong][^claim-7]

### Canonical Items
- - `strategist`: orchestration and final decision communication [confidence: explicit] [recurrence: 36][^item-decision-1]
- - Only request user input when truly blocked by missing access/data/decision. [confidence: explicit] [recurrence: 17][^item-decision-2]
- - Remove ambiguity in routing/decision contracts [confidence: explicit] [recurrence: 17][^item-decision-3]
- Decision standard: [confidence: explicit] [recurrence: 17][^item-decision-4]
- decision [confidence: explicit] [recurrence: 4][^item-decision-5]
- ### Locked Decisions [confidence: explicit] [recurrence: 2][^item-decision-6]
- Remember, you are the strategist that will create the trade cards, so It is your decision to know what kind of data you need inside the application. [confidence: explicit] [recurrence: 2][^item-decision-7]
- strategist remains decision owner. [confidence: explicit] [recurrence: 1][^item-decision-8]
- routing_decisions [confidence: explicit] [recurrence: 1][^item-decision-9]
- I’m reproducing the status maps directly so I can patch the exact scope decisions instead of broad changes. [confidence: explicit] [recurrence: 1][^item-decision-10]
- I’m grounding Phase 8 against the current repo shape first so the audit plan matches the existing state/models and doesn’t leave implementation decisions open. [confidence: explicit] [recurrence: 1][^item-decision-11]
- decision_type [confidence: explicit] [recurrence: 1][^item-decision-12]
- - `wiki/projects/ai-trader/decisions.md` [confidence: explicit] [recurrence: 1][^item-decision-13]
- - durable pages like `workflow-rules`, `communication-preferences`, `architecture`, `decisions` grouped by recurrence/support, not just recency [confidence: explicit] [recurrence: 1][^item-decision-14]
- Before I lock the Phase 6 plan, I need these decisions: [confidence: explicit] [recurrence: 1][^item-decision-15]
- `durable items` like preferences, rules, decisions, architecture notes [confidence: explicit] [recurrence: 1][^item-decision-16]
- Before I lock the Phase 5 plan, I need these decisions: [confidence: explicit] [recurrence: 1][^item-decision-17]
- Before I produce the Phase 3 plan, I need these decisions: [confidence: explicit] [recurrence: 1][^item-decision-18]
- Before I lock the Phase 2 plan, I need these decisions: [confidence: explicit] [recurrence: 1][^item-decision-19]
- Phase 1 is now decision-complete: [confidence: explicit] [recurrence: 1][^item-decision-20]
- Three decisions remain before the final Phase 1 plan: [confidence: explicit] [recurrence: 1][^item-decision-21]
- Then I’ll turn that into a decision-complete refactor plan instead of a generic architecture essay. [confidence: explicit] [recurrence: 1][^item-decision-22]
- **Locked Decisions (from your choices)** [confidence: explicit] [recurrence: 1][^item-decision-23]
- - hypothesis decision (`confirmed`, `partial`, `rejected`) [confidence: explicit] [recurrence: 1][^item-decision-24]
- Dominant topic was trading platform/API + IRA automation decisions (Fidelity vs alternatives), not just balance reporting. [confidence: explicit] [recurrence: 1][^item-decision-25]
- | daily aggregate + `a07c9e11-3574-44a6-bbf6-5fc8759ba9df`, `9765b6d9-7124-4a90-bcb1-e304dff5c452` | Outlier day 2026-02-23 (highest in last 120 days): compliance-blocked deployment + rollback/diagnosis decision. [confidence: explicit] [recurrence: 1][^item-decision-26]
- Add a `quality_decisions` ledger with: artifact id/type, confidence, decision, deciding agent, reason codes, model/version, timestamp. [confidence: explicit] [recurrence: 1][^item-decision-27]
- I’m now editing `approval_ui` to add the Phase 2 execution action API paths (`positions/open`, `positions/actions`, pending queue, decision`) on top of your existing agent auth/idempotency/audit pattern. [confidence: explicit] [recurrence: 1][^item-decision-28]
- applysetupdecision [confidence: explicit] [recurrence: 1][^item-decision-29]
- Add `POST /agent/v1/positions/actions/:actionId/decision` for human approve/reject only. [confidence: explicit] [recurrence: 1][^item-decision-30]
- AITrader Phase 2 public API additions: execution-position read endpoint, execution action create endpoint, pending-action list endpoint, human decision endpoint. [confidence: explicit] [recurrence: 1][^item-decision-31]
- Human remains approval authority for trade decisions in Phase 1. [confidence: explicit] [recurrence: 1][^item-decision-32]
- Pre-open decision point: strategist reviews candidate artifact, submits trade cards via AITrader API, then presents concise review pack to you. [confidence: explicit] [recurrence: 1][^item-decision-33]
- One final safety decision is needed for the Phase 2 execution-agent design before I finalize the roadmap. [confidence: explicit] [recurrence: 1][^item-decision-34]
- I need three architecture choices to make the roadmap fully decision-complete. [confidence: explicit] [recurrence: 1][^item-decision-35]
- auto-running strategist on top can duplicate messages and reduce your control over decision synthesis. [confidence: explicit] [recurrence: 1][^item-decision-36]
- I’ll send quick multiple-choice decisions now. [confidence: explicit] [recurrence: 1][^item-decision-37]
- - Existing manual decision endpoints continue to work. [confidence: explicit] [recurrence: 1][^item-decision-38]
- - Keep human decision endpoints unchanged (`/setups/:setupId/decision`) for manual approval flow. [confidence: explicit] [recurrence: 1][^item-decision-39]
- This plan is decision-complete and uses your selected flow: **Restore then polish**. [confidence: explicit] [recurrence: 1][^item-decision-40]
- I need three decisions to lock the automation part of the plan without leaving implementation choices open. [confidence: explicit] [recurrence: 1][^item-decision-41]
- I need one lock-in decision to finalize the Phase 2 plan. [confidence: explicit] [recurrence: 1][^item-decision-42]
- ### Locked implementation decisions [confidence: explicit] [recurrence: 1][^item-decision-43]
- For each symbol at decision time: [confidence: explicit] [recurrence: 1][^item-decision-44]
- | Data Domain | Strategist Draft | Final Decision | [confidence: explicit] [recurrence: 1][^item-decision-45]
- I have enough decisions now to produce a decision-complete plan. [confidence: explicit] [recurrence: 1][^item-decision-46]
- I need two scope decisions to finalize a concrete ingestion plan. [confidence: explicit] [recurrence: 1][^item-decision-47]
- This is what my strategist agent gave me based on what he need to make its trading decisions. [confidence: explicit] [recurrence: 1][^item-decision-48]
- API/automation allowance, free-tier quotas, and usage constraints are not fully validated per source.","Risk handling is not complete for a high-impact story: options/IV data limitations are mentioned but no deterministic free implementation path or explici... [confidence: explicit] [recurrence: 1][^item-decision-49]
- ## 1) Locked Decisions [confidence: explicit] [recurrence: 1][^item-decision-50]

## Sources
[^claim-1]: items ai-trader:decision:83a4883aa32aca68; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-2]: items ai-trader:decision:43fc5d7f9e3f053c; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-3]: items ai-trader:decision:a88ca3a8027af8a9; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-4]: items ai-trader:decision:0bcfd184b3ab82f0; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-5]: items ai-trader:decision:06cd4cd3c42a81ba; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 201-201; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 202-205; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 282-282
[^claim-6]: items ai-trader:decision:bdb5795e5ad2f1a9; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 218-218; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 219-221; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 262-262
[^claim-7]: items ai-trader:decision:f832e6bfe2b256c2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3337-3347
[^item-decision-1]: items ai-trader:decision:83a4883aa32aca68; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-decision-2]: items ai-trader:decision:43fc5d7f9e3f053c; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-decision-3]: items ai-trader:decision:a88ca3a8027af8a9; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-decision-4]: items ai-trader:decision:0bcfd184b3ab82f0; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-decision-5]: items ai-trader:decision:ab4c3a9625ce2272; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 8345-8349; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 14690-14697; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 800-806
[^item-decision-6]: items ai-trader:decision:7d5e949ab4244662; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 2728-2731; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 2733-2733; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 2734-2736
[^item-decision-7]: items ai-trader:decision:bdb5795e5ad2f1a9; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 218-218; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 219-221; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 262-262
[^item-decision-8]: items ai-trader:decision:06cd4cd3c42a81ba; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 201-201; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 202-205; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 282-282
[^item-decision-9]: items ai-trader:decision:e78ceafe7e176993; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 11075-11088; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 11257-11266; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 13591-13598
[^item-decision-10]: items ai-trader:decision:f832e6bfe2b256c2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3337-3347
[^item-decision-11]: items ai-trader:decision:0d71ab882c5c396f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2933-2944
[^item-decision-12]: items ai-trader:decision:200f2b1654a7ad25; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1879-1887
[^item-decision-13]: items ai-trader:decision:1b01b11ccda4e4cc; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1290-1290; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1291-1295
[^item-decision-14]: items ai-trader:decision:c1cfe6048e403558; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1290-1290; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1291-1295
[^item-decision-15]: items ai-trader:decision:5fb8c227a36e39c3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1290-1290; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1291-1295
[^item-decision-16]: items ai-trader:decision:e86881407f6a7dc2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 963-963; 019d837d-d249-71c3-9637-b8d6992ce805 lines 964-968
[^item-decision-17]: items ai-trader:decision:a96db9cac1cd2f9b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 963-963; 019d837d-d249-71c3-9637-b8d6992ce805 lines 964-968
[^item-decision-18]: items ai-trader:decision:83b7a247e2806c97; 019d837d-d249-71c3-9637-b8d6992ce805 lines 518-521
[^item-decision-19]: items ai-trader:decision:3b9ef35ae46c4f91; 019d837d-d249-71c3-9637-b8d6992ce805 lines 269-269; 019d837d-d249-71c3-9637-b8d6992ce805 lines 270-273
[^item-decision-20]: items ai-trader:decision:9c578f9e53a28e25; 019d837d-d249-71c3-9637-b8d6992ce805 lines 111-111; 019d837d-d249-71c3-9637-b8d6992ce805 lines 112-115
[^item-decision-21]: items ai-trader:decision:9e16ec0e05ac133a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 99-103
[^item-decision-22]: items ai-trader:decision:375771bf9cb68f64; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57229-57239
[^item-decision-23]: items ai-trader:decision:4e8103098a86de89; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31394-31394
[^item-decision-24]: items ai-trader:decision:5c7ab2603eb1d1b9; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31394-31394
[^item-decision-25]: items ai-trader:decision:cc48b3c60e6a3888; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26354-26354
[^item-decision-26]: items ai-trader:decision:d828f75bc5079847; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26354-26354
[^item-decision-27]: items ai-trader:decision:40c56908ecb10a3a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13534-13540; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13541-13544
[^item-decision-28]: items ai-trader:decision:21f005fecaa0dc42; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2631-2653
[^item-decision-29]: items ai-trader:decision:a2883d1818015d71; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2299-2316
[^item-decision-30]: items ai-trader:decision:6c859739d33c774e; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2175-2178; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2180-2180; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2181-2183
[^item-decision-31]: items ai-trader:decision:8f6ae5478ad3dbfa; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2175-2178; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2180-2180; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2181-2183
[^item-decision-32]: items ai-trader:decision:ba3a6af6acdad1b7; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2175-2178; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2180-2180; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2181-2183
[^item-decision-33]: items ai-trader:decision:6911cba42b45d0e3; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2175-2178; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2180-2180; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2181-2183
[^item-decision-34]: items ai-trader:decision:d0094f6d6fdfcc12; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2165-2174
[^item-decision-35]: items ai-trader:decision:b07bec5514610da7; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2068-2083
[^item-decision-36]: items ai-trader:decision:3e0b8bb3203c31d0; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1914-1924
[^item-decision-37]: items ai-trader:decision:1b1a8fb1e1be14f4; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1914-1924
[^item-decision-38]: items ai-trader:decision:2ef4d1530161b9ca; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1145-1148; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1150-1150; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1151-1153
[^item-decision-39]: items ai-trader:decision:8fb4117c9d7ab963; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1145-1148; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1150-1150; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1151-1153
[^item-decision-40]: items ai-trader:decision:36ae0782b69ca530; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 10579-10582
[^item-decision-41]: items ai-trader:decision:88d0cd676b8a7f3b; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1110-1125
[^item-decision-42]: items ai-trader:decision:c33a9bccf4c9bf8d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 10551-10578
[^item-decision-43]: items ai-trader:decision:d3ac5f85ce0b1546; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 873-876
[^item-decision-44]: items ai-trader:decision:90d2871077c7f80c; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 873-876
[^item-decision-45]: items ai-trader:decision:9bd1b31094892c8b; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 873-876
[^item-decision-46]: items ai-trader:decision:8dedfc0ef12e4b6f; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 778-795
[^item-decision-47]: items ai-trader:decision:25c62dd08334d87a; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 768-777
[^item-decision-48]: items ai-trader:decision:0a8c9f01ed0e8c73; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 6-6; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 7-12
[^item-decision-49]: items ai-trader:decision:a0edbd53bcefb539; 019cba69-7058-72e0-805d-180f5372e2bd lines 9-15
[^item-decision-50]: items ai-trader:decision:3e6836a60312bd90; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 9313-9316
