---
title: "AI Trader - Workflow Rules"
page_id: "projects/ai-trader/workflow-rules"
domain: "ai-trader"
bucket: "workflow-rules"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:32:33.871426Z
source_count: 8
claim_count: 3
tags:
  - wikimemory
  - project
  - ai-trader
  - bucket
  - workflow-rules
---
# AI Trader - Workflow Rules

Navigation: [[projects/ai-trader/index|AI Trader]] | [[projects/ai-trader/communication-preferences|AI Trader - Communication Preferences]] | [[projects/ai-trader/architecture|AI Trader - Architecture]] | [[projects/ai-trader/code-map|AI Trader - Code Map]] | [[projects/ai-trader/current-state|AI Trader - Current State]] | [[projects/ai-trader/tasks|AI Trader - Tasks]] | [[projects/ai-trader/outcomes|AI Trader - Outcomes]] | [[projects/ai-trader/failures|AI Trader - Failures]] | [[projects/ai-trader/decisions|AI Trader - Decisions]] | [[projects/ai-trader/next-steps|AI Trader - Next Steps]] | [[projects/ai-trader/open-questions|AI Trader - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- No synthesized summary yet.

## Do Rule
- Always create setups with `status='pending_approval'`. [latent: implicit_dos_and_donts] [confidence: strong][^claim-1]
- Acceptance criteria always included: criteria are extracted/normalized from delegation contracts and embedded in story description. [latent: implicit_dos_and_donts] [confidence: strong][^claim-2]
- Make sure you're viewing the latest commit in `Files changed` (not an older commit diff). [latent: implicit_dos_and_donts] [confidence: strong][^claim-3]

### Canonical Items
- always `warning` [confidence: strong] [recurrence: 1][^item-do_rule-1]
- Running the targeted suite again now to make sure Phase 3 is solid end to end. [confidence: strong] [recurrence: 1][^item-do_rule-2]
- Your AITrader docs already reflect the new `/agent/v1` surface, so I’m checking actual implementation state in code to make sure the roadmap distinguishes “already done” vs “still needed” for each agent. [confidence: strong] [recurrence: 1][^item-do_rule-3]
- Always create setup with `status='pending_approval'`. [confidence: strong] [recurrence: 1][^item-do_rule-4]
- Make sure you’re viewing the latest commit in `Files changed` (not an older commit diff). [confidence: strong] [recurrence: 1][^item-do_rule-5]
- `#trackerTab` was always forced to `display: grid`, so Tracker never hid when switching tabs. [confidence: strong] [recurrence: 1][^item-do_rule-6]
- Anything trading-impacting, risk limits, execution/routing logic, auth/security, data integrity = **always high**. [confidence: strong] [recurrence: 1][^item-do_rule-7]
- Without write permission, the same failure path will always recur for any code change. [confidence: strong] [recurrence: 1][^item-do_rule-8]
- Acceptance criteria always included: criteria are extracted/normalized from delegation contracts (with fallback if missing) and embedded in story description. [confidence: strong] [recurrence: 1][^item-do_rule-9]
- Lane titles now always render from explicit labels** (`Backlog`, `Ready`, `In Progress`, etc.), so no blank header. [confidence: strong] [recurrence: 1][^item-do_rule-10]
- Strategist always gets core decomposition/spec skills loaded (intent/spec/constraints/decomposition/eval). [confidence: strong] [recurrence: 1][^item-do_rule-11]
- Otherwise always reuse current open story. [confidence: strong] [recurrence: 1][^item-do_rule-12]
- Blocked tasks now always have a reason (enforced, with fallback text if missing). [confidence: strong] [recurrence: 1][^item-do_rule-13]
- blocked status will always carry a reason (auto-fallback if missing), [confidence: strong] [recurrence: 1][^item-do_rule-14]
- Should stop sending vague tasks and always send a structured handoff. [confidence: strong] [recurrence: 1][^item-do_rule-15]
- `from` node always exits on its right side. [confidence: strong] [recurrence: 1][^item-do_rule-16]
- `to` node always enters on its left side. [confidence: strong] [recurrence: 1][^item-do_rule-17]
- Normalized setup timestamps so `setup.created_at` is always before lifecycle events. [confidence: strong] [recurrence: 1][^item-do_rule-18]
- `Custom profile editor` now always shows the weight fields. [confidence: strong] [recurrence: 1][^item-do_rule-19]
- Real data always wins. [confidence: strong] [recurrence: 1][^item-do_rule-20]

## Dont Rule
- No synthesized section summary yet.

### Canonical Items
- never in the middle of a tight explicit chain unless no better seam exists [confidence: strong] [recurrence: 1][^item-dont_rule-1]
- Segmentation should optimize for coherent local context, but use a balanced cutoff so segments do not grow too large for downstream classification. [confidence: strong] [recurrence: 1][^item-dont_rule-2]
- For a source whose Phase 1 committed boundary and fingerprint are unchanged, do nothing. [confidence: strong] [recurrence: 1][^item-dont_rule-3]
- never read the partial tail beyond that point. [confidence: strong] [recurrence: 1][^item-dont_rule-4]
- Unknown outer event types or payload subtypes do not fail normalization [confidence: strong] [recurrence: 1][^item-dont_rule-5]
- The remaining choices are about how we surface schema drift and how “lossless” should be represented so later phases never need to re-open raw logs just to recover important structure. [confidence: strong] [recurrence: 1][^item-dont_rule-6]
- "Nothing low-confidence goes straight to “person”." Nothing low confidence should go to anywhere, so don't create rules of high-low confidence just for people, but to every entity type. [confidence: strong] [recurrence: 1][^item-dont_rule-7]
- Never return a single hard number unless evidence is explicit and dominant (for example a row labeled `Current Balance` with recent timestamp). [confidence: strong] [recurrence: 1][^item-dont_rule-8]
- Do not implement anything, just help me think trough it [confidence: strong] [recurrence: 1][^item-dont_rule-9]
- Next I’m syncing the same contract wording changes from AITrader canonical and re-running contract sync/verify so we don’t leave checksum drift. [confidence: strong] [recurrence: 1][^item-dont_rule-10]
- Update research persona to emit schema-valid candidate artifacts only and never write to AITrader. [confidence: strong] [recurrence: 1][^item-dont_rule-11]
- Agent API never serves UI mock-card fallback. [confidence: strong] [recurrence: 1][^item-dont_rule-12]
- Real-Data Pipeline Gating (Do Not Activate Yet) [confidence: strong] [recurrence: 1][^item-dont_rule-13]
- If any required field missing or stale, return a typed data error and do not build setup. [confidence: strong] [recurrence: 1][^item-dont_rule-14]
- Do not add unrelated domains (calendar/team/office). [confidence: strong] [recurrence: 1][^item-dont_rule-15]
- Do not block cutover on AITrader [confidence: strong] [recurrence: 1][^item-dont_rule-16]
- For example, he has calendar tab, I don't have that here, so I don't need that, etc.. [confidence: strong] [recurrence: 1][^item-dont_rule-17]
- `#trackerTab` was always forced to `display: grid`, so Tracker never hid when switching tabs. [confidence: strong] [recurrence: 1][^item-dont_rule-18]
- For immediate message stop, use `/scheduler off` (or natural text like “don’t send updates/messages”). [confidence: strong] [recurrence: 1][^item-dont_rule-19]
- Added explicit silent-mode detection so messages like “don’t send updates/messages”, “remain silent”, “no need to send any msg” disable scheduler even without the word “scheduler”. [confidence: strong] [recurrence: 1][^item-dont_rule-20]
- Expand chat intent detection so explicit “don’t send messages/updates, stay silent” language disables scheduler even without saying the word “scheduler”. [confidence: strong] [recurrence: 1][^item-dont_rule-21]
- Don’t expect major acceleration for modern larger models. [confidence: strong] [recurrence: 1][^item-dont_rule-22]
- Non-actionable dashboard widgets that do not feed strategy/risk logic. [confidence: strong] [recurrence: 1][^item-dont_rule-23]
- This looks great but i don't know if we need that level of detail. [confidence: strong] [recurrence: 1][^item-dont_rule-24]
- `-a never` [confidence: strong] [recurrence: 1][^item-dont_rule-25]

## Sources
[^claim-1]: items ai-trader:do_rule:0e1f19677fca7dfd; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1145-1148; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1150-1150; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1151-1153
[^claim-2]: items ai-trader:do_rule:88c0a1528f4eac41; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 9930-9930
[^claim-3]: items ai-trader:do_rule:8a3ffde0a450166e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 2189-2204
[^item-do_rule-1]: items ai-trader:do_rule:08e345b15367cc6c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-do_rule-2]: items ai-trader:do_rule:e139cdfe313a089c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 698-713
[^item-do_rule-3]: items ai-trader:do_rule:3edac7477b6ab72a; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1982-1994
[^item-do_rule-4]: items ai-trader:do_rule:0e1f19677fca7dfd; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1145-1148; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1150-1150; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1151-1153
[^item-do_rule-5]: items ai-trader:do_rule:8a3ffde0a450166e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 2189-2204
[^item-do_rule-6]: items ai-trader:do_rule:e6c1a350bf383a71; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1014-1045
[^item-do_rule-7]: items ai-trader:do_rule:3e7bb1c4521a57c7; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 17519-17529
[^item-do_rule-8]: items ai-trader:do_rule:537f9656b0e12ccd; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 461-463; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 464-467
[^item-do_rule-9]: items ai-trader:do_rule:88c0a1528f4eac41; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 9930-9930
[^item-do_rule-10]: items ai-trader:do_rule:8b8d0b779d318a0a; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 9019-9023
[^item-do_rule-11]: items ai-trader:do_rule:fccb61e0880b051e; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 8993-8993
[^item-do_rule-12]: items ai-trader:do_rule:1f8e81fff6d77ab2; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 8579-8585
[^item-do_rule-13]: items ai-trader:do_rule:dff67d626f2075bb; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 6844-6848
[^item-do_rule-14]: items ai-trader:do_rule:5e9b40dc76f64a27; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 6688-6697
[^item-do_rule-15]: items ai-trader:do_rule:9dddd05365c67dc1; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 3995-3997; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 5426-5426; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 5427-5430
[^item-do_rule-16]: items ai-trader:do_rule:d4a109df99bc213e; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 14437-14455
[^item-do_rule-17]: items ai-trader:do_rule:b173f7f04ef6d490; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 14437-14455
[^item-do_rule-18]: items ai-trader:do_rule:730d603838463e76; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 13496-13500
[^item-do_rule-19]: items ai-trader:do_rule:d4f0a145bce74a9c; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4721-4725
[^item-do_rule-20]: items ai-trader:do_rule:bf1345a3296fe7e2; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3776-3780
[^item-dont_rule-1]: items ai-trader:dont_rule:09dd786c755b21a0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 541-544; 019d837d-d249-71c3-9637-b8d6992ce805 lines 547-547; 019d837d-d249-71c3-9637-b8d6992ce805 lines 548-549
[^item-dont_rule-2]: items ai-trader:dont_rule:7fd1f5bbc57d9d09; 019d837d-d249-71c3-9637-b8d6992ce805 lines 541-544; 019d837d-d249-71c3-9637-b8d6992ce805 lines 547-547; 019d837d-d249-71c3-9637-b8d6992ce805 lines 548-549
[^item-dont_rule-3]: items ai-trader:dont_rule:57550fb1323418c8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 293-293; 019d837d-d249-71c3-9637-b8d6992ce805 lines 294-295
[^item-dont_rule-4]: items ai-trader:dont_rule:c7563973406421c5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 293-293; 019d837d-d249-71c3-9637-b8d6992ce805 lines 294-295
[^item-dont_rule-5]: items ai-trader:dont_rule:1114cc8c0313b329; 019d837d-d249-71c3-9637-b8d6992ce805 lines 293-293; 019d837d-d249-71c3-9637-b8d6992ce805 lines 294-295
[^item-dont_rule-6]: items ai-trader:dont_rule:ef84f6a9706f12f4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 280-286
[^item-dont_rule-7]: items ai-trader:dont_rule:601ea401fe43453b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13534-13540
[^item-dont_rule-8]: items ai-trader:dont_rule:7b8dbf3af6db53ad; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13411-13417; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13418-13421
[^item-dont_rule-9]: items ai-trader:dont_rule:3c2f32081864ded4; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13411-13417
[^item-dont_rule-10]: items ai-trader:dont_rule:d3804be2aec281b4; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 3478-3503
[^item-dont_rule-11]: items ai-trader:dont_rule:9ec91b07ab56d6a7; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2175-2178; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2180-2180; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 2181-2183
[^item-dont_rule-12]: items ai-trader:dont_rule:e1f10927d8ee1d47; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1145-1148; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1150-1150; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1151-1153
[^item-dont_rule-13]: items ai-trader:dont_rule:b2157bb3dff58a2d; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1145-1148; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1150-1150; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1151-1153
[^item-dont_rule-14]: items ai-trader:dont_rule:fc1866f8b4e6f70e; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 873-876
[^item-dont_rule-15]: items ai-trader:dont_rule:695fc558c7cea7b5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 9313-9316
[^item-dont_rule-16]: items ai-trader:dont_rule:f62ebf8d3e3c10c2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3842-3845; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3847-3847; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3848-3850
[^item-dont_rule-17]: items ai-trader:dont_rule:d1a7777a459b794b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1067-1081
[^item-dont_rule-18]: items ai-trader:dont_rule:bfebad599ee920c9; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1014-1045
[^item-dont_rule-19]: items ai-trader:dont_rule:5c5bc5c99d41ec6f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 695-705
[^item-dont_rule-20]: items ai-trader:dont_rule:a21504461df8d873; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 690-690
[^item-dont_rule-21]: items ai-trader:dont_rule:2730f99a7feebdcb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 371-371
[^item-dont_rule-22]: items ai-trader:dont_rule:2b247594b8de3e52; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 18131-18135
[^item-dont_rule-23]: items ai-trader:dont_rule:9b8d9f29441359d1; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 17530-17536; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 17537-17540
[^item-dont_rule-24]: items ai-trader:dont_rule:f7de72f655cbb897; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 17175-17179
[^item-dont_rule-25]: items ai-trader:dont_rule:3e02d84742b0a34b; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 17083-17087
