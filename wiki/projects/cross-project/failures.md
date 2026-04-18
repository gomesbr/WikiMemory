---
title: "Cross-Project - Failures"
page_id: "projects/cross-project/failures"
domain: "cross-project"
bucket: "failures"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:11:05.278213Z
source_count: 2
claim_count: 6
tags:
  - wikimemory
  - cross-project
  - cross-project
  - bucket
  - failures
---
# Cross-Project - Failures

Navigation: [[projects/cross-project/index|Cross-Project]] | [[projects/cross-project/communication-preferences|Cross-Project - Communication Preferences]] | [[projects/cross-project/workflow-rules|Cross-Project - Workflow Rules]] | [[projects/cross-project/architecture|Cross-Project - Architecture]] | [[projects/cross-project/code-map|Cross-Project - Code Map]] | [[projects/cross-project/current-state|Cross-Project - Current State]] | [[projects/cross-project/tasks|Cross-Project - Tasks]] | [[projects/cross-project/outcomes|Cross-Project - Outcomes]] | [[projects/cross-project/decisions|Cross-Project - Decisions]] | [[projects/cross-project/next-steps|Cross-Project - Next Steps]] | [[projects/cross-project/open-questions|Cross-Project - Open Questions]]
Related Domains: [[projects/ai-scientist/index|AI Scientist]], [[projects/ai-trader/index|AI Trader]], [[projects/open-brain/index|Open Brain]]

## Summary
- Patches have been applied to address real-data failure modes, and regression tests have been added to prevent future occurrences. [latent: implicit_dos_and_donts] [confidence: strong][^claim-1]
- The live error count has shown a downward trend, indicating that the fixes implemented are effective. [latent: current_state_synthesis] [confidence: strong][^claim-2]
- Audit errors identified are real but do not indicate broken pointers, suggesting that the system is functioning as intended despite the errors. [latent: current_state_synthesis] [confidence: strong][^claim-3]

## Failure
- A historical failure has been recorded, indicating a recurring issue within the project. [latent: recurring_failure_patterns] [confidence: strong][^claim-4]
- The live suite encountered a real-data extraction failure, prompting a reproduction of the pipeline stage for analysis. [latent: current_state_synthesis] [confidence: strong][^claim-5]
- The remaining audit errors are identified as false contradictions, which need further investigation. [latent: partially_explicit_open_questions] [confidence: strong][^claim-6]

### Canonical Items
- failure [confidence: strong] [status: historical] [recurrence: 2][^item-failure-1]
- I’ve patched the real-data failure mode and added a regression test. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-2]
- I’ve got the exact live failure cluster now. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-3]
- The live error count is still dropping, which means the fix path is right. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-4]
- The remaining audit errors are still false contradictions, now from `next_step` and a generic `current_state` pronoun key. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-5]
- The live audit errors dropped sharply, so I’m inspecting the remaining ones now instead of widening the suppression. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-6]
- The audit errors are real but not pointing to broken pointers [confidence: strong] [status: historical] [recurrence: 1][^item-failure-7]
- if anything else shows up, it should be a true real-data issue, not a synthetic-contract mismatch. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-8]
- The live failure is a real-data edge: superseded conflicting observations were correctly kept, but validation still demanded a conflict notice for them. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-9]
- extractionerror [confidence: strong] [status: historical] [recurrence: 1][^item-failure-10]
- The live suite hit a real-data extraction failure, so I’m reproducing just that pipeline stage now and printing the fatal summary. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-11]
- I’m running the Phase 2 and extraction slices first so I can catch schema or hydration issues before I spend time on the live sample run. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-12]
- - asserts no phase failures [confidence: strong] [status: historical] [recurrence: 1][^item-failure-13]
- - treat broken raw refs as `error` [confidence: strong] [status: historical] [recurrence: 1][^item-failure-14]
- - Added lock handling, partial-failure recording, scoped refresh propagation, and aggregated refresh reporting [confidence: strong] [status: historical] [recurrence: 1][^item-failure-15]
- One remaining failure is just the failure-injection test not actually reaching `classify` after the no-op skip fix. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-16]
- fatal_error_summary [confidence: strong] [status: historical] [recurrence: 1][^item-failure-17]
- last_error [confidence: strong] [status: historical] [recurrence: 1][^item-failure-18]
- The refresh tests surfaced three concrete issues: lock-path behavior, no-op scope skipping, and scoped downstream invalidation. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-19]
- The focused suite found a couple of wiring bugs in refresh itself, not the design: wrong discovery constant name and a missing JSONL helper import. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-20]
- I’m running the focused suite now to catch orchestration issues before I touch docs or the broader test pass. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-21]
- That’ll give us coverage on no-op skipping, scoped fan-out, invalidation, locking, and partial-failure recording. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-22]
- - active fresh lock causes immediate failure [confidence: strong] [status: historical] [recurrence: 1][^item-failure-23]
- - audit errors -> refresh returns nonzero and records failed-at-audit [confidence: strong] [status: historical] [recurrence: 1][^item-failure-24]
- - error count [confidence: strong] [status: historical] [recurrence: 1][^item-failure-25]
- - Failure handling: [confidence: strong] [status: historical] [recurrence: 1][^item-failure-26]
- - failure phase [confidence: strong] [status: historical] [recurrence: 1][^item-failure-27]
- - Failure policy: [confidence: strong] [status: historical] [recurrence: 1][^item-failure-28]
- - fatal error summary [confidence: strong] [status: historical] [recurrence: 1][^item-failure-29]
- - if `audit` completes with `error_finding_count > 0`, refresh returns nonzero and records the run as failed-at-audit [confidence: strong] [status: historical] [recurrence: 1][^item-failure-30]
- - include total warning/error counts from bootstrap/audit [confidence: strong] [status: historical] [recurrence: 1][^item-failure-31]
- - injected phase failure stops the chain [confidence: strong] [status: historical] [recurrence: 1][^item-failure-32]
- - stop on the first fatal phase failure [confidence: strong] [status: historical] [recurrence: 1][^item-failure-33]
- - success/failure [confidence: strong] [status: historical] [recurrence: 1][^item-failure-34]
- - the run stops on the first fatal phase failure [confidence: strong] [status: historical] [recurrence: 1][^item-failure-35]
- - the top-level refresh report records the last completed phase and the failure point [confidence: strong] [status: historical] [recurrence: 1][^item-failure-36]
- best-effort cleanup on failure [confidence: strong] [status: historical] [recurrence: 1][^item-failure-37]
- I’m adding a focused test matrix now for stale warnings, contradictions, provenance/drift errors, and scoped audit refresh so we can validate the stage before touching docs. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-38]
- I’m patching the staging bug and adding a focused bootstrap test suite against the existing sample pipeline. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-39]
- I’ve patched the two noisy failure modes. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-40]
- Priority issues now: [confidence: strong] [status: historical] [recurrence: 1][^item-failure-41]
- I found the wiki failure path. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-42]
- I’m doing a tight compile check before I add the wiki tests so we catch any structural issues in the new module first, then I’ll use the tests to harden the behavior around citations, manifests, and incremental rebuilds. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-43]
- Recurring failure / friction patterns [confidence: strong] [status: historical] [recurrence: 1][^item-failure-44]
- I’m writing the extractor around the same staged-commit pattern as the earlier phases, including domain rebuilds, so Phase 5 stays safe on partial failures instead of leaving source and aggregate knowledge out of sync. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-45]
- - supports sample-scoped `source_id` runs, taxonomy-version full backfills, tombstones, and atomic rollback on failure [confidence: strong] [status: historical] [recurrence: 1][^item-failure-46]
- I’m adding the Phase 4 tests now around the actual trust boundaries: deterministic labeling, mixed-signal behavior, taxonomy-change backfills, sample scoping, and failure-safe rollback. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-47]
- I’m writing the classifier around the same state-machine shape as the earlier phases so taxonomy changes, sample runs, tombstones, and failures all behave consistently instead of becoming special cases later. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-48]
- * extract decisions, failures, next steps, open questions [confidence: strong] [status: historical] [recurrence: 1][^item-failure-49]
- * recurring issues [confidence: strong] [status: historical] [recurrence: 1][^item-failure-50]
- * review recurring issues [confidence: strong] [status: historical] [recurrence: 1][^item-failure-51]
- A mixed session can be broken into coherent blocks that humans would agree mostly belong together. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-52]
- I’m checking the API logs now before I hand this back, so we don’t leave the `Network` refresh in a broken state. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-53]
- I’ll verify the server startup + auth middleware path isn’t failing silently by checking route/middleware configuration and then patching the small edge case that most likely causes repeated login failures. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-54]
- The root request from PowerShell failed mid-handshake, so I’ll use curl to verify the served HTML and JS route directly. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-55]
- The domain bug is reduced [confidence: strong] [status: historical] [recurrence: 1][^item-failure-56]
- the remaining WhatsApp failure class is now clearly ownership/target/context misframing. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-57]
- I’m patching that specific layer in `v2_experiments.ts`, then I’ll validate with targeted batches and keep the loop running instead of stopping at the first failed attempt. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-58]
- I’m resuming from the current human-WhatsApp ownership/voice failure cluster in `v2_experiments.ts`, patching that layer first, then I’ll rerun a short miner batch and verify the rejection mix shifts. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-59]
- I’m patching only those in `src/v2_experiments.ts`, then I’ll run a short batch and check whether the rejection mix shifts from ownership/actor-scope failures to real thin-anchor failures. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-60]

## Sources
[^claim-1]: items cross-project:failure:2f76b3bc12a22361; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4174-4187
[^claim-2]: items cross-project:failure:db3a807aeec2001c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4097-4105
[^claim-3]: items cross-project:failure:7d02e203fc15df0f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4059-4069
[^claim-4]: items cross-project:failure:777317f7c316ff37; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 17458-17459; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^claim-5]: items cross-project:failure:74f34437522a7ed2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3981-3996
[^claim-6]: items cross-project:failure:ef7be2d319112b63; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4085-4095
[^item-failure-1]: items cross-project:failure:777317f7c316ff37; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 17458-17459; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-failure-2]: items cross-project:failure:2f76b3bc12a22361; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4174-4187
[^item-failure-3]: items cross-project:failure:3f6bfac82d1e20a8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4135-4143
[^item-failure-4]: items cross-project:failure:db3a807aeec2001c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4097-4105
[^item-failure-5]: items cross-project:failure:ef7be2d319112b63; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4085-4095
[^item-failure-6]: items cross-project:failure:788479fe3057e9b3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4071-4079
[^item-failure-7]: items cross-project:failure:7d02e203fc15df0f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4059-4069
[^item-failure-8]: items cross-project:failure:e597e3f9939c0a27; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4019-4037
[^item-failure-9]: items cross-project:failure:d324f8dc78e64a6d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4019-4037
[^item-failure-10]: items cross-project:failure:eb30cf0b817c09d8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4002-4009
[^item-failure-11]: items cross-project:failure:74f34437522a7ed2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3981-3996
[^item-failure-12]: items cross-project:failure:194a43b9b482aaa3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3919-3930
[^item-failure-13]: items cross-project:failure:674d8d7006c4b798; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-failure-14]: items cross-project:failure:e7441b597b90802d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3617-3620; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3623-3623; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3624-3625
[^item-failure-15]: items cross-project:failure:4d8aa293ab3d2c7c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3432-3437
[^item-failure-16]: items cross-project:failure:6732aeb9b4a84079; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3394-3401
[^item-failure-17]: items cross-project:failure:2ab7d52e29a016eb; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3380-3385
[^item-failure-18]: items cross-project:failure:35261f38054b5b28; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3380-3385
[^item-failure-19]: items cross-project:failure:03fe1d7c7fda5cd3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3319-3327
[^item-failure-20]: items cross-project:failure:57946b696a25f85c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3288-3311
[^item-failure-21]: items cross-project:failure:5dd5dbab2e3b4947; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3278-3286
[^item-failure-22]: items cross-project:failure:fa43d76c8335f0ec; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3271-3272
[^item-failure-23]: items cross-project:failure:f3883d59377a99c5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-24]: items cross-project:failure:2aa78d872fa42ebe; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-25]: items cross-project:failure:b459553bf880bd1a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-26]: items cross-project:failure:11a0e68990de9e2d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-27]: items cross-project:failure:925ff16a46d1d5c0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-28]: items cross-project:failure:8eaacb829128e682; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-29]: items cross-project:failure:f530d82d9c377070; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-30]: items cross-project:failure:5a07365676f1b01b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-31]: items cross-project:failure:544b57ed2b41d78c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-32]: items cross-project:failure:c9e35ca98be90366; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-33]: items cross-project:failure:a06ffff971ad91e5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-34]: items cross-project:failure:186d7c27969936f9; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-35]: items cross-project:failure:bed10c116f5ea73d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-36]: items cross-project:failure:fc812ea77c741960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-37]: items cross-project:failure:6afb908e50d66403; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-failure-38]: items cross-project:failure:71b3ba81a7067f63; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3100-3101
[^item-failure-39]: items cross-project:failure:f74b4168ab8648a2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2831-2847
[^item-failure-40]: items cross-project:failure:c414dedb7503c0f1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2447-2458
[^item-failure-41]: items cross-project:failure:9a85e3a86fcfec2a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2391-2399
[^item-failure-42]: items cross-project:failure:c622a866ceb5d0fe; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2352-2360
[^item-failure-43]: items cross-project:failure:cc6ba13c6ce12269; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1448-1469
[^item-failure-44]: items cross-project:failure:cc96443ae115e4e2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-failure-45]: items cross-project:failure:8e6145cf17fdcda6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1024-1028
[^item-failure-46]: items cross-project:failure:691cbc31cb89bb1d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 930-940; 019d837d-d249-71c3-9637-b8d6992ce805 lines 941-945
[^item-failure-47]: items cross-project:failure:dda4bfd9f297f3e6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 889-911
[^item-failure-48]: items cross-project:failure:29b6b3bc3ac6b605; 019d837d-d249-71c3-9637-b8d6992ce805 lines 842-843
[^item-failure-49]: items cross-project:failure:d510f67407fa1057; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-failure-50]: items cross-project:failure:5582190607fbf29b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-failure-51]: items cross-project:failure:f5a62eeae78b42c8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-failure-52]: items cross-project:failure:b754725febb63997; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-failure-53]: items cross-project:failure:8d0d90228e6ec068; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72632-72645
[^item-failure-54]: items cross-project:failure:b82c2faab8de486f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 70470-70474
[^item-failure-55]: items cross-project:failure:f7cf8eb0f6308a1c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 69359-69377
[^item-failure-56]: items cross-project:failure:07bfc4413227c087; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 62852-62864
[^item-failure-57]: items cross-project:failure:d031fd694820d91a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 62212-62226
[^item-failure-58]: items cross-project:failure:ad7f2362d46463ae; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 62122-62128
[^item-failure-59]: items cross-project:failure:e4afc5e13185a432; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 62016-62022
[^item-failure-60]: items cross-project:failure:99120fedd0ef0287; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 62002-62014
