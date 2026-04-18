---
title: "Cross-Project - Open Questions"
page_id: "projects/cross-project/open-questions"
domain: "cross-project"
bucket: "open-questions"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:11:30.342164Z
source_count: 2
claim_count: 4
tags:
  - wikimemory
  - cross-project
  - cross-project
  - bucket
  - open-questions
---
# Cross-Project - Open Questions

Navigation: [[projects/cross-project/index|Cross-Project]] | [[projects/cross-project/communication-preferences|Cross-Project - Communication Preferences]] | [[projects/cross-project/workflow-rules|Cross-Project - Workflow Rules]] | [[projects/cross-project/architecture|Cross-Project - Architecture]] | [[projects/cross-project/code-map|Cross-Project - Code Map]] | [[projects/cross-project/current-state|Cross-Project - Current State]] | [[projects/cross-project/tasks|Cross-Project - Tasks]] | [[projects/cross-project/outcomes|Cross-Project - Outcomes]] | [[projects/cross-project/failures|Cross-Project - Failures]] | [[projects/cross-project/decisions|Cross-Project - Decisions]] | [[projects/cross-project/next-steps|Cross-Project - Next Steps]]
Related Domains: [[projects/ai-scientist/index|AI Scientist]], [[projects/ai-trader/index|AI Trader]], [[projects/open-brain/index|Open Brain]]

## Summary
- The main remaining plan decisions involve quality gates, API-backed phases, and the aggressiveness of the autonomous retry loop. [latent: partially_explicit_open_questions] [confidence: strong][^claim-1]
- Current efforts include grounding in the existing pipeline and ensuring the full-run loop plan aligns with repository capabilities. [latent: partially_explicit_open_questions] [confidence: strong][^claim-2]
- There are ongoing tests to verify the effectiveness of changes made to the audit process and data handling. [latent: partially_explicit_open_questions] [confidence: strong][^claim-3]

## Open Question
- Decisions regarding the implementation of regression tests and their impact on data integrity are under consideration. [latent: partially_explicit_open_questions] [confidence: strong][^claim-4]

### Canonical Items
- **Why** [confidence: strong] [status: active] [recurrence: 2][^item-open_question-1]
- What changed [confidence: strong] [status: active] [recurrence: 2][^item-open_question-2]
- should [confidence: strong] [status: active] [recurrence: 2][^item-open_question-3]
- The main remaining plan decisions are about quality gates, API-backed phases, and how aggressive the autonomous retry loop should be. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-4]
- I’m grounding in the current pipeline and rollout hooks first so the full-run loop plan matches what the repo can already do and where it needs orchestration logic. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-5]
- I’m adding a narrow regression test so the live-data fix stays locked: repeated `next_step` items on the same file/path should warn, not fail the audit. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-6]
- this should tell us whether the remaining audit collisions are actually gone on live data. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-7]
- I’m rerunning the real sample suite again to verify the audit noise drops the way it should on actual data. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-8]
- This should be the last real-data cleanup pass. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-9]
- if anything else shows up, it should be a true real-data issue, not a synthetic-contract mismatch. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-10]
- One regression showed up in segmentation: the guardrail split test is now seeing a semantic split instead of the prior size-forced split. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-11]
- - Coverage should include: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-12]
- - downstream phases should bump only if their persisted artifact shape changes, otherwise rely on upstream invalidation via last-run/state dependencies [confidence: strong] [status: active] [recurrence: 1][^item-open_question-13]
- I’m running the targeted refresh tests first, then I’ll patch only what breaks. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-14]
- I’m checking the remaining version constants and manifest/state helpers now so `refresh` can fingerprint exactly what each phase already treats as output-shaping. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-15]
- Next focus should be Phase 5 hardening. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-16]
- What should you focus on next? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-17]
- What about phase 5, was everything ok there? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-18]
- The classification helper logic already knows how to relabel most of those low-signal segments, so I’m tracing why that override is not making it into the persisted output. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-19]
- One small usability gap showed up in the docs: the wiki phase now has a real OpenAI runtime dependency, so I’m adding the env var note before I wrap. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-20]
- Phase 6 should render from an internal page model into a pluggable output format. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-21]
- What is Obsidian-specific and should stay isolated: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-22]
- What remains valid as-is: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-23]
- Examples: short intros, section summaries, and “what this means” explanations that make the wiki navigable instead of a raw item dump. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-24]
- Examples: what changed from an earlier assumption, what replaced it, and why. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-25]
- Examples: what is currently built, what is sample-only, what is still pending, what design direction is currently winning. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-26]
- Examples: what Open Brain really is, what AI Scientist really is, how they differ, what AI Trader focuses on, what is in-scope vs out-of-scope. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-27]
- Examples: what the likely next implementation or validation action is, when it is implied by the work history rather than explicitly stated as “next step”. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-28]
- Latent knowledge should mean: knowledge that is not stated cleanly in one extracted item, but is inferable from repeated evidence across segments, sessions, time, or projects. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-29]
- What should not be LLM-owned: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-30]
- I’m grounding Phase 5 against the current outputs first, because knowledge extraction should consume the real classified segment shape we now have, not an older design sketch. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-31]
- I’m doing a quick syntax and structure pass now before I wire the CLI and tests, so any contract drift shows up early instead of after the full pipeline is connected. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-32]
- Current repo state: the Phase 3 code is in place, but there are no persisted `normalized/` or `segmented/` artifacts checked into this repo right now, so I’m assuming we should keep the same sample-first workflow for Phase 4. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-33]
- How should unknown or weakly supported segments behave? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-34]
- If a segment is mostly project-specific but also contains global preferences or workflow rules, should it be: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-35]
- Should every classification include an explanation payload listing the matched signals, such as keywords, path hints, repo hints, topic hints, and explicit mentions? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-36]
- Should Phase 4 classify only `segments`, not whole sessions or individual events? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-37]
- Should project taxonomy live in config from this phase onward, so future projects can be added and old classified segments can be re-run against the updated taxonomy? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-38]
- What classification strategy do you want for Phase 4? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-39]
- What confidence format do you want? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-40]
- What label model should each segment carry? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-41]
- What output shape do you want? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-42]
- When both `Open Brain` and `AI Scientist` appear in one segment, should `cross-project` be used only when no single dominant project clearly wins? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-43]
- I’m grounding Phase 4 against the actual Phase 3 outputs first, because classification should key off the segment artifacts we now have rather than the earlier design sketch. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-44]
- Example: keep a tool-call chain together when `call_id`, `turn_id`, or response linkage shows continuity, even if there are intervening low-signal events. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-45]
- How should we treat low-signal operational events like `task_started`, `task_complete`, token/accounting events, and similar runtime markers? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-46]
- I’m starting Phase 3 at the real boundary between Phase 2 and segmentation, so we keep the next plan grounded in what the system actually produces today. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-47]
- Should a segment be allowed to span multiple turns if the topic/workstream is still clearly continuous? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-48]
- Should explicit linkage win over superficial boundaries? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-49]
- Should Phase 3 stop at: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-50]
- Should Phase 3 support running on a selected sample set of normalized sources for now, instead of assuming the whole normalized corpus exists? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-51]
- Should the primary unit for segmentation be the normalized event stream, not inferred chat messages or raw JSON lines? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-52]
- What artifact shape do you want for Phase 3 output? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-53]
- I’m grounding Phase 3 against the actual Phase 2 outputs first, because segmentation depends on what normalized artifacts we truly have available, not just the design doc. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-54]
- ## Conceptual entities the system should understand [confidence: strong] [status: active] [recurrence: 1][^item-open_question-55]
- ## Why segmentation matters [confidence: strong] [status: active] [recurrence: 1][^item-open_question-56]
- * file movement/renaming should not break provenance if possible [confidence: strong] [status: active] [recurrence: 1][^item-open_question-57]
- * how to detect partial processing checkpoints? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-58]
- * how to fingerprint files efficiently? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-59]
- * how to support resume after interruption? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-60]
- * How will stale or contradicted knowledge be handled? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-61]
- * the system should support streaming/chunked processing [confidence: strong] [status: active] [recurrence: 1][^item-open_question-62]
- * what belongs in compact bootstrap memory [confidence: strong] [status: active] [recurrence: 1][^item-open_question-63]
- * What belongs in global vs project memory? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-64]
- * what belongs in rich wiki pages [confidence: strong] [status: active] [recurrence: 1][^item-open_question-65]
- * What is a segment? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-66]
- * What is a session? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-67]
- * What is allowed into bootstrap? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-68]
- * What is the minimum provenance unit? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-69]
- * what metadata is stored for each source file? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-70]
- * What must stay only in wiki? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-71]
- Define how humans and agents will actually consume the artifacts. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-72]
- Each phase should include ONLY: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-73]
- Extraction should dedupe aggressively and merge repeated patterns. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-74]
- Incremental design should be present from the start, even if first implementation is semi-manual. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-75]
- It should be a curated, structured abstraction layer. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-76]
- Need explicit rules for what may enter bootstrap memory. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-77]
- Normalization should preserve at least: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-78]
- Segmentation rules should prefer: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-79]
- Segmentation should avoid: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-80]

## Sources
[^claim-1]: items cross-project:open_question:582c09182ac2bee1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4290-4302
[^claim-2]: items cross-project:open_question:b4283cb4f3ced252; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4251-4262
[^claim-3]: items cross-project:open_question:f092f8482b256f0a, cross-project:open_question:60095ff2866d462d, cross-project:open_question:be6843f58139c3c6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4161-4173; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4097-4105; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4071-4079
[^claim-4]: items cross-project:open_question:f092f8482b256f0a, cross-project:open_question:7c37375977b04a7b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4161-4173; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4071-4079
[^item-open_question-1]: items cross-project:open_question:ff4950c23e2f1c40; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 42889-42894; 019d837d-d249-71c3-9637-b8d6992ce805 lines 739-742; 019d837d-d249-71c3-9637-b8d6992ce805 lines 930-940
[^item-open_question-2]: items cross-project:open_question:bbb3d6d51857ecc3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43702-43709; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 54465-54470; 019d837d-d249-71c3-9637-b8d6992ce805 lines 739-742
[^item-open_question-3]: items cross-project:open_question:cf8bf799b7e5fe90; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 52016-52017; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-open_question-4]: items cross-project:open_question:582c09182ac2bee1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4290-4302
[^item-open_question-5]: items cross-project:open_question:b4283cb4f3ced252; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4251-4262
[^item-open_question-6]: items cross-project:open_question:f092f8482b256f0a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4161-4173
[^item-open_question-7]: items cross-project:open_question:60095ff2866d462d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4097-4105
[^item-open_question-8]: items cross-project:open_question:be6843f58139c3c6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4071-4079
[^item-open_question-9]: items cross-project:open_question:7c37375977b04a7b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4071-4079
[^item-open_question-10]: items cross-project:open_question:ad11022e0ca19564; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4019-4037
[^item-open_question-11]: items cross-project:open_question:816ced29baf27b72; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3939-3947
[^item-open_question-12]: items cross-project:open_question:7414395f17a486ce; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-open_question-13]: items cross-project:open_question:e2ae2b8ddb9cb639; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-open_question-14]: items cross-project:open_question:2f2d9d75cda1f8b6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3312-3317
[^item-open_question-15]: items cross-project:open_question:95381c6764b81329; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3212-3223
[^item-open_question-16]: items cross-project:open_question:1512b7978f8068e1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2391-2399
[^item-open_question-17]: items cross-project:open_question:99b96d7221f4392e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2391-2399
[^item-open_question-18]: items cross-project:open_question:e6a5f19072b0383e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2382-2390
[^item-open_question-19]: items cross-project:open_question:e7b1df78c102832a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2087-2095
[^item-open_question-20]: items cross-project:open_question:f22645db9ea917a1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1593-1600
[^item-open_question-21]: items cross-project:open_question:36f50e36ad686871; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1340-1347
[^item-open_question-22]: items cross-project:open_question:45e116d04c10a831; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1340-1347
[^item-open_question-23]: items cross-project:open_question:aee49e6b3fb95eaf; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1340-1347
[^item-open_question-24]: items cross-project:open_question:412eb0143173f84d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-open_question-25]: items cross-project:open_question:be649fa15116fc9d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-open_question-26]: items cross-project:open_question:1610b757af0b5326; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-open_question-27]: items cross-project:open_question:dcfda2d16d6b7fcd; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-open_question-28]: items cross-project:open_question:f7f52f508124fe47; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-open_question-29]: items cross-project:open_question:a8feeeaacc140716; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-open_question-30]: items cross-project:open_question:f4dae66a5350d447; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-open_question-31]: items cross-project:open_question:f24d808f0c4bc182; 019d837d-d249-71c3-9637-b8d6992ce805 lines 950-961
[^item-open_question-32]: items cross-project:open_question:bcce28bd467d3ccb; 019d837d-d249-71c3-9637-b8d6992ce805 lines 873-881
[^item-open_question-33]: items cross-project:open_question:f245478a17c1cf3b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-open_question-34]: items cross-project:open_question:2ce69a821a3ea2c6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-open_question-35]: items cross-project:open_question:9f005435f824b977; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-open_question-36]: items cross-project:open_question:f960d38444cb0440; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-open_question-37]: items cross-project:open_question:a4762f99988ba944; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-open_question-38]: items cross-project:open_question:b01aac7150385f56; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-open_question-39]: items cross-project:open_question:4266c5df8417fd66; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-open_question-40]: items cross-project:open_question:c36d71afebd59e59; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-open_question-41]: items cross-project:open_question:7bac4f33e2696a98; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-open_question-42]: items cross-project:open_question:636ebe34b568e406; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-open_question-43]: items cross-project:open_question:fd6741fddb57ca25; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-open_question-44]: items cross-project:open_question:02b6ccb78ceb7f31; 019d837d-d249-71c3-9637-b8d6992ce805 lines 749-760
[^item-open_question-45]: items cross-project:open_question:d80b73aa122a503f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 516-517
[^item-open_question-46]: items cross-project:open_question:75038dffc52df406; 019d837d-d249-71c3-9637-b8d6992ce805 lines 516-517
[^item-open_question-47]: items cross-project:open_question:baa6edfae5c0a80d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 499-515; 019d837d-d249-71c3-9637-b8d6992ce805 lines 516-517
[^item-open_question-48]: items cross-project:open_question:c77849ced190ec1e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 516-517
[^item-open_question-49]: items cross-project:open_question:d44aed8a1545025f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 516-517
[^item-open_question-50]: items cross-project:open_question:b99304d0dd6d8f3a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 516-517
[^item-open_question-51]: items cross-project:open_question:bac43dd7e8197cb1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 516-517
[^item-open_question-52]: items cross-project:open_question:baac306adc447670; 019d837d-d249-71c3-9637-b8d6992ce805 lines 516-517
[^item-open_question-53]: items cross-project:open_question:24e5d1a4111d2fa1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 516-517
[^item-open_question-54]: items cross-project:open_question:50c34933953781cf; 019d837d-d249-71c3-9637-b8d6992ce805 lines 499-515
[^item-open_question-55]: items cross-project:open_question:01cc0bd73d463837; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-56]: items cross-project:open_question:e760a1fa0443e53d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-57]: items cross-project:open_question:a95f5bad5eb1d07c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-58]: items cross-project:open_question:0f9b1869ca9046c7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-59]: items cross-project:open_question:7bdae6df76405364; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-60]: items cross-project:open_question:e159c66187baf223; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-61]: items cross-project:open_question:26e6f0849fcc2b93; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-62]: items cross-project:open_question:c584a2fdd8c5fd86; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-63]: items cross-project:open_question:17250a6263dd1ff1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-64]: items cross-project:open_question:906e8b59acbc1d66; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-65]: items cross-project:open_question:8c4c4c53ef7843dc; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-66]: items cross-project:open_question:c45c8eaa2bbc9842; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-67]: items cross-project:open_question:0f0dd42d3f190c6f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-68]: items cross-project:open_question:9bd39051e822b95f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-69]: items cross-project:open_question:ce2723034b61a8c7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-70]: items cross-project:open_question:ebd41007465f5d92; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-71]: items cross-project:open_question:de923c24529efa72; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-72]: items cross-project:open_question:f3b6ad5f570c052a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-73]: items cross-project:open_question:f8d3a3f74438e46b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-74]: items cross-project:open_question:c34dee2a99088f69; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-75]: items cross-project:open_question:6d40b3c46f5b4545; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-76]: items cross-project:open_question:bc72eff77bc18829; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-77]: items cross-project:open_question:e4ed2189d7fa1c9e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-78]: items cross-project:open_question:7e476ac520563c17; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-79]: items cross-project:open_question:d91681862b2c68cd; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-open_question-80]: items cross-project:open_question:1c7ae9918c9d0122; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
