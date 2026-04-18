---
title: "Cross-Project - Decisions"
page_id: "projects/cross-project/decisions"
domain: "cross-project"
bucket: "decisions"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:11:15.669847Z
source_count: 2
claim_count: 5
tags:
  - wikimemory
  - cross-project
  - cross-project
  - bucket
  - decisions
---
# Cross-Project - Decisions

Navigation: [[projects/cross-project/index|Cross-Project]] | [[projects/cross-project/communication-preferences|Cross-Project - Communication Preferences]] | [[projects/cross-project/workflow-rules|Cross-Project - Workflow Rules]] | [[projects/cross-project/architecture|Cross-Project - Architecture]] | [[projects/cross-project/code-map|Cross-Project - Code Map]] | [[projects/cross-project/current-state|Cross-Project - Current State]] | [[projects/cross-project/tasks|Cross-Project - Tasks]] | [[projects/cross-project/outcomes|Cross-Project - Outcomes]] | [[projects/cross-project/failures|Cross-Project - Failures]] | [[projects/cross-project/next-steps|Cross-Project - Next Steps]] | [[projects/cross-project/open-questions|Cross-Project - Open Questions]]
Related Domains: [[projects/ai-scientist/index|AI Scientist]], [[projects/ai-trader/index|AI Trader]], [[projects/open-brain/index|Open Brain]]

## Summary
- Locked decisions are critical for project continuity. [latent: decision_synthesis] [confidence: strong][^claim-1]
- Tradeoff decisions are necessary for effective project management. [latent: decision_synthesis] [confidence: strong][^claim-2]

## Decision
- The main remaining plan decisions involve quality gates and API-backed phases. [latent: decision_synthesis] [confidence: strong][^claim-3]
- Decision lineage is tracked to ensure clarity in decision-making. [latent: decision_lineage] [confidence: strong][^claim-4]
- Decision synthesis includes examples of settled decisions discussed across multiple sessions. [latent: decision_synthesis] [confidence: strong][^claim-5]

### Canonical Items
- decision [confidence: explicit] [recurrence: 2][^item-decision-1]
- ## Locked Decisions [confidence: explicit] [recurrence: 1][^item-decision-2]
- `quality_decisions` [confidence: explicit] [recurrence: 1][^item-decision-3]
- I’ve got the tradeoff decisions. [confidence: explicit] [recurrence: 1][^item-decision-4]
- The main remaining plan decisions are about quality gates, API-backed phases, and how aggressive the autonomous retry loop should be. [confidence: explicit] [recurrence: 1][^item-decision-5]
- Decision lineage [confidence: explicit] [recurrence: 1][^item-decision-6]
- Decision synthesis [confidence: explicit] [recurrence: 1][^item-decision-7]
- Examples: the actual settled decision when it was discussed across multiple turns, refined, challenged, then accepted. [confidence: explicit] [recurrence: 1][^item-decision-8]
- Before I lock the Phase 4 plan, I need these decisions: [confidence: explicit] [recurrence: 1][^item-decision-9]
- Before I produce the Phase 3 plan, I need these decisions: [confidence: explicit] [recurrence: 1][^item-decision-10]
- I’m mapping the project at phase level first, then I’ll stay strictly inside Phase 1 and surface the decisions we need before any detailed plan exists. [confidence: explicit] [recurrence: 1][^item-decision-11]
- ## Cross-phase critical decisions [confidence: explicit] [recurrence: 1][^item-decision-12]
- * decisions [confidence: explicit] [recurrence: 1][^item-decision-13]
- * extract decisions, failures, next steps, open questions [confidence: explicit] [recurrence: 1][^item-decision-14]
- * inspect project state and decisions [confidence: explicit] [recurrence: 1][^item-decision-15]
- * Propose options when decisions are unclear [confidence: explicit] [recurrence: 1][^item-decision-16]
- A written design spec exists and is stable enough that implementation decisions are consistent. [confidence: explicit] [recurrence: 1][^item-decision-17]
- Also include recommended artifact structures, critical design tradeoffs, and a list of decisions that must be finalized before coding. [confidence: explicit] [recurrence: 1][^item-decision-18]
- I answer and help define assumptions and decisions [confidence: explicit] [recurrence: 1][^item-decision-19]
- Please produce a detailed implementation plan organized by phases, with clear goals, deliverables, dependencies, risks, and open design decisions for each phase. [confidence: explicit] [recurrence: 1][^item-decision-20]
- This is one of the most important design decisions in the whole plan. [confidence: explicit] [recurrence: 1][^item-decision-21]
- I need one scope decision to make the two-phase split implementation-safe. [confidence: explicit] [recurrence: 1][^item-decision-22]
- `risk_safety_decisions` [confidence: explicit] [recurrence: 1][^item-decision-23]
- Your reviewed clarify decisions are enough to learn the pattern now. [confidence: explicit] [recurrence: 1][^item-decision-24]
- I’m analyzing your owner decisions first to extract repeated failure modes and question-pattern duplication, then I’ll fix clarify generation at that layer, purge deprecated clarify cases, and regenerate a cleaner diverse batch. [confidence: explicit] [recurrence: 1][^item-decision-25]
- - only cases with `admissionDecision.admitted = true` [confidence: explicit] [recurrence: 1][^item-decision-26]
- - the main issue is that several `Yes` decisions approved cases where the **question/evidence are okay, but the lens is wrong** [confidence: explicit] [recurrence: 1][^item-decision-27]
- - your `No` decisions were mostly strong [confidence: explicit] [recurrence: 1][^item-decision-28]
- I’m pulling your first reviewed batch from the DB with the linked question, label, notes, and evidence so I can sanity-check the decisions instead of guessing from counts. [confidence: explicit] [recurrence: 1][^item-decision-29]
- ## Locked Product Decisions [confidence: explicit] [recurrence: 1][^item-decision-30]
- **Decision panel (right)** [confidence: explicit] [recurrence: 1][^item-decision-31]
- `PreloopDecisionPayload` [confidence: explicit] [recurrence: 1][^item-decision-32]
- Implement decision form + shortcut handlers. [confidence: explicit] [recurrence: 1][^item-decision-33]
- First I’ll validate the new reviewer code compiles cleanly, then I’ll restart the active strategy loop so each completed strategy gets an automatic intelligent review + retry-or-advance decision. [confidence: explicit] [recurrence: 1][^item-decision-34]
- `QualityDecision` [confidence: explicit] [recurrence: 1][^item-decision-35]
- Decision: `publish|hold|reject|retry`. [confidence: explicit] [recurrence: 1][^item-decision-36]
- Fields: `artifact_type, artifact_id, score, decision, reasons, decided_by, created_at`. [confidence: explicit] [recurrence: 1][^item-decision-37]
- Quality decisions are explicit and auditable. [confidence: explicit] [recurrence: 1][^item-decision-38]
- If you want, next I’ll produce a **full replacement plan** with these deltas merged into your current execution plan (decision-complete, implementation-ready). [confidence: explicit] [recurrence: 1][^item-decision-39]
- "decision": "promote|hold|reject|retry", [confidence: explicit] [recurrence: 1][^item-decision-40]
- - Add `quality_decisions` table capturing agent decisions with rationale and model/version. [confidence: explicit] [recurrence: 1][^item-decision-41]
- - Final promote/hold/reject decision for candidates and answers. [confidence: explicit] [recurrence: 1][^item-decision-42]
- Decision ledger: [confidence: explicit] [recurrence: 1][^item-decision-43]
- Quality correction source: agent-generated decisions first, user feedback secondary. [confidence: explicit] [recurrence: 1][^item-decision-44]
- Decision behavior: risk appetite, procrastination, impulsivity, follow-through. [confidence: explicit] [recurrence: 1][^item-decision-45]
- Publish/hold/reject decisions are auditable. [confidence: explicit] [recurrence: 1] [conflict][^item-decision-46]
- - publish/hold/reject decisions [confidence: explicit] [recurrence: 1] [conflict][^item-decision-47]

## Sources
[^claim-1]: items cross-project:decision:7d5e949ab4244662; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5689-5692; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5695-5697
[^claim-2]: items cross-project:decision:da941d97f2d64fc7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4303-4314
[^claim-3]: items cross-project:decision:de894151a975d8b3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4290-4302
[^claim-4]: items cross-project:decision:f41f233dbe359f54; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^claim-5]: items cross-project:decision:05741182e3f14af9; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-decision-1]: items cross-project:decision:ab4c3a9625ce2272; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 10349-10351; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57242-57249; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6
[^item-decision-2]: items cross-project:decision:7d5e949ab4244662; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5689-5692; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5695-5697
[^item-decision-3]: items cross-project:decision:9d38e8afad511a50; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13564-13567; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20924-20924; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20925-20928
[^item-decision-4]: items cross-project:decision:da941d97f2d64fc7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4303-4314
[^item-decision-5]: items cross-project:decision:de894151a975d8b3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4290-4302
[^item-decision-6]: items cross-project:decision:f41f233dbe359f54; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-decision-7]: items cross-project:decision:05741182e3f14af9; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-decision-8]: items cross-project:decision:a1a131a2896c1378; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-decision-9]: items cross-project:decision:79a37ee5ac471968; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-decision-10]: items cross-project:decision:83b7a247e2806c97; 019d837d-d249-71c3-9637-b8d6992ce805 lines 516-517
[^item-decision-11]: items cross-project:decision:9a7dc317bb15c529; 019d837d-d249-71c3-9637-b8d6992ce805 lines 10-12
[^item-decision-12]: items cross-project:decision:7ed8e4cc237c3de9; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-decision-13]: items cross-project:decision:95c6c1d9d5abaece; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-decision-14]: items cross-project:decision:b2171dc38d28dd76; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-decision-15]: items cross-project:decision:d8091a24695270e4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-decision-16]: items cross-project:decision:413d7499cde7468b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-decision-17]: items cross-project:decision:ab5f5ee9be48afe3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-decision-18]: items cross-project:decision:a4199b48c81fd8d8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-decision-19]: items cross-project:decision:9a8da05b3303bcc7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-decision-20]: items cross-project:decision:49e339e061e4e744; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-decision-21]: items cross-project:decision:7754830af1cdb3f1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-decision-22]: items cross-project:decision:784cf4e49b96e3bf; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 77276-77282
[^item-decision-23]: items cross-project:decision:19def17aba148afd; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 49264-49264
[^item-decision-24]: items cross-project:decision:fb41f490ec06517c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 46317-46331
[^item-decision-25]: items cross-project:decision:219ae2d44f43a1ab; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 46305-46315
[^item-decision-26]: items cross-project:decision:af73391256dceed2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43655-43659
[^item-decision-27]: items cross-project:decision:b3175de9e5e166a9; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43342-43342
[^item-decision-28]: items cross-project:decision:2c90be38f0575244; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43342-43342
[^item-decision-29]: items cross-project:decision:0fb52df0889bc827; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43332-43340
[^item-decision-30]: items cross-project:decision:a9e20e9e9158f9f6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 34450-34457
[^item-decision-31]: items cross-project:decision:0bca328494d4a69e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 34450-34457
[^item-decision-32]: items cross-project:decision:06b6af5419ae0c74; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 34450-34457
[^item-decision-33]: items cross-project:decision:532d3138b045b7b1; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 34450-34457
[^item-decision-34]: items cross-project:decision:7685a2c1353035e1; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 29927-29928
[^item-decision-35]: items cross-project:decision:21f4463e97cc9795; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20924-20924; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20925-20928
[^item-decision-36]: items cross-project:decision:3f696970f23be82b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20924-20924; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20925-20928
[^item-decision-37]: items cross-project:decision:3991dff5dca44986; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20924-20924; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20925-20928
[^item-decision-38]: items cross-project:decision:5acce3c243f1c29f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20924-20924; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20925-20928
[^item-decision-39]: items cross-project:decision:77c0248c7bd3962c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20902-20909
[^item-decision-40]: items cross-project:decision:cca1dbb6390c4792; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13564-13567
[^item-decision-41]: items cross-project:decision:e5fa68d1c7d04eb6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13564-13567
[^item-decision-42]: items cross-project:decision:baae128e2f4fc363; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13564-13567
[^item-decision-43]: items cross-project:decision:e8aa5c906ecec50b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13564-13567
[^item-decision-44]: items cross-project:decision:5bae4240b7ff1b77; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13564-13567
[^item-decision-45]: items cross-project:decision:781224f346e648b1; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13455-13455; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13456-13458
[^item-decision-46]: items cross-project:decision:a290fc7008cebd18; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20924-20924; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20925-20928
[^item-decision-47]: items cross-project:decision:e93c62d6630ca7e4; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13564-13567
