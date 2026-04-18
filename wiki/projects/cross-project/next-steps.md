---
title: "Cross-Project - Next Steps"
page_id: "projects/cross-project/next-steps"
domain: "cross-project"
bucket: "next-steps"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:11:23.778881Z
source_count: 2
claim_count: 7
tags:
  - wikimemory
  - cross-project
  - cross-project
  - bucket
  - next-steps
---
# Cross-Project - Next Steps

Navigation: [[projects/cross-project/index|Cross-Project]] | [[projects/cross-project/communication-preferences|Cross-Project - Communication Preferences]] | [[projects/cross-project/workflow-rules|Cross-Project - Workflow Rules]] | [[projects/cross-project/architecture|Cross-Project - Architecture]] | [[projects/cross-project/code-map|Cross-Project - Code Map]] | [[projects/cross-project/current-state|Cross-Project - Current State]] | [[projects/cross-project/tasks|Cross-Project - Tasks]] | [[projects/cross-project/outcomes|Cross-Project - Outcomes]] | [[projects/cross-project/failures|Cross-Project - Failures]] | [[projects/cross-project/decisions|Cross-Project - Decisions]] | [[projects/cross-project/open-questions|Cross-Project - Open Questions]]
Related Domains: [[projects/ai-scientist/index|AI Scientist]], [[projects/ai-trader/index|AI Trader]], [[projects/open-brain/index|Open Brain]]

## Summary
- The next steps involve running focused extraction and audit tests, followed by the env-gated live sample suite. [latent: implicit_next_steps] [confidence: strong][^claim-1]
- Patching the contradiction policy at the audit layer and rerunning tests is a priority. [latent: implicit_next_steps] [confidence: strong][^claim-2]
- Isolating the remaining live-data gap and tightening the contradiction policy are key actions moving forward. [latent: implicit_next_steps] [confidence: strong][^claim-3]
- The extraction tests will be updated to use the temp source-roots config and include a regression test. [latent: implicit_next_steps] [confidence: strong][^claim-4]

## Next Step
- The next step is to bump the Phase 2 schema and move into new tests, including the real-data suite. [latent: implicit_next_steps] [confidence: strong][^claim-5]
- Wiring the resolver and validating the live sample set through the pipeline is planned next. [latent: implicit_next_steps] [confidence: strong][^claim-6]
- Editing the resolver and threading the optional lazy-hydration path through classification and extraction is a priority. [latent: implicit_next_steps] [confidence: strong][^claim-7]

### Canonical Items
- I’m running the focused extraction/audit tests first, then the env-gated live sample suite. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-1]
- I’m patching the contradiction policy at the audit layer and the last generic subject-key fallback, then I’ll rerun the targeted and live tests. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-2]
- I’ve isolated the remaining live-data gap in Phase 8 and I’m tightening the contradiction policy plus the last generic subject-key cases, then I’ll rerun the live sample suite. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-3]
- I’m making the extraction tests use the temp source-roots config end to end, then adding one regression where the signal exists only past the bounded Phase 2 text cutoff. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-4]
- I’m bumping the Phase 2 schema and then moving straight into the new tests, including the real-data suite. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-5]
- next step is wiring the resolver and the new pointer-first artifact shape, then I’ll validate the live sample set through the pipeline. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-6]
- I’m editing the resolver and Phase 2 first, then I’ll thread the optional lazy-hydration path through classification/extraction and finish with tests. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-7]
- I’m running the targeted refresh tests first, then I’ll patch only what breaks. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-8]
- I’m adding `refresh.py` now, then I’ll wire the CLI and build a focused orchestration test matrix around real phase calls with fake LLMs. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-9]
- - if `classify` is full, then `extract/wiki/bootstrap/audit` are also full [confidence: strong] [status: active] [recurrence: 1][^item-next_step-10]
- - if `wiki` is full, then `bootstrap/audit` are also full [confidence: strong] [status: active] [recurrence: 1][^item-next_step-11]
- I’m wiring tests and the last repo updates, then I’ll validate the bootstrap pipeline end-to-end locally. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-12]
- I’m adding the new module and config now, then I’ll hook the CLI/tests after the core pipeline is in place. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-13]
- I’m checking the latest run’s notice mix and then I’ll cap the noisy categories at segment level. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-14]
- - then rerun Phase 6 on the same sample and inspect wiki quality again [confidence: strong] [status: active] [recurrence: 1][^item-next_step-15]
- I’m patching the page packet so synthesized claims can only reference item keys that are actually present in the rendered page sections, then I’ll rerun the same real sample. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-16]
- I’m fixing that and then adding a focused `test_wiki.py` file that exercises the full discovery→wiki path with mocked synthesis. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-17]
- Phase 6 is partially scaffolded, and I’m tightening it by adding the wiki test coverage and then validating the full pipeline end to end. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-18]
- I’m doing a tight compile check before I add the wiki tests so we catch any structural issues in the new module first, then I’ll use the tests to harden the behavior around citations, manifests, and incremental rebuilds. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-19]
- After that I’ll run the new wiki tests first, then the full suite so we catch any integration gaps without widening the blast radius too early. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-20]
- I’m moving into the code edits next with the smallest viable slice first: the core wiki module and CLI wiring, then the markdown/manifests, then the tests. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-21]
- - then have a renderer, where v1 renderer is `markdown+obsidian` [confidence: strong] [status: active] [recurrence: 1][^item-next_step-22]
- Examples: the actual settled decision when it was discussed across multiple turns, refined, challenged, then accepted. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-23]
- Examples: what the likely next implementation or validation action is, when it is implied by the work history rather than explicitly stated as “next step”. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-24]
- Implicit next steps [confidence: strong] [status: active] [recurrence: 1][^item-next_step-25]
- I’m moving that file into the repo now, then I’ll continue with the CLI/tests there. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-26]
- I’m wiring the command surface and repo metadata now, then I’ll add tests to shake out the edge cases before we consider the phase done. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-27]
- The main change is a new extractor module that mirrors the earlier phase patterns, then I’ll wire the CLI and add focused tests around the tricky parts like domain merging, weak-signal skips, and conflict handling. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-28]
- I’m adding the discovery engine next, including Windows shared-read handling and the atomic state promotion path, then I’ll back it with integration-style tests. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-29]
- The shape is clear now, so I’m creating the new repo and then I’ll wire the discovery engine, state format, and tests around the real append-aware behavior we verified. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-30]
- I’m mapping the project at phase level first, then I’ll stay strictly inside Phase 1 and surface the decisions we need before any detailed plan exists. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-31]
- * extract decisions, failures, next steps, open questions [confidence: strong] [status: active] [recurrence: 1][^item-next_step-32]
- * next step [confidence: strong] [status: active] [recurrence: 1][^item-next_step-33]
- ONLY THEN we move to Phase 2. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-34]
- Then start PHASE 1 CLARIFICATION by asking questions [confidence: strong] [status: active] [recurrence: 1][^item-next_step-35]
- I’m validating the frontend login flow directly from the served HTML/JS to find where it returns to `showLogin` unexpectedly and then patch only that path. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-36]
- I’ll verify the server startup + auth middleware path isn’t failing silently by checking route/middleware configuration and then patching the small edge case that most likely causes repeated login failures. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-37]
- I’ll recheck the API health/login endpoint path and container startup state now, then apply only the minimal backend fix if it regressed. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-38]
- I’ll quickly validate with simple curl calls again and then, if needed, patch the login UX. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-39]
- I’ll re-run with more time and then check service status and verify the running JS directly inside the container. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-40]
- I’ll verify what the running app is actually serving, then force a full rebuild/deploy so the browser uses the patched login handler and confirm the old handler is gone from the served bundle. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-41]
- I’m going to: 1) improve the preloop phase cards layout in `renderPreloopReadiness(...)`, 2) make top/bottom pending queue counts use the same active non-stale definition, then 4) run `npm run typecheck && npm test`, and 5) restart the loop focusing on phas... [confidence: strong] [status: active] [recurrence: 1][^item-next_step-42]
- I’m validating and then rerunning the short batch again. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-43]
- First I’m checking the exact rejection path and the current miner state, then I’ll patch that layer, validate, and rerun the batch. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-44]
- I’m tightening the authoring prompt and adding a dedicated fallback builder for other-human-to-user directives, then I’ll test on a short batch. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-45]
- I’m patching that at the authoring prompt and critique layer, then I’ll rerun another batch. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-46]
- Then I’ll rerun the same short batch and compare the rejection slice. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-47]
- I’m patching that specific layer in `v2_experiments.ts`, then I’ll validate with targeted batches and keep the loop running instead of stopping at the first failed attempt. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-48]
- I’m resuming from the current human-WhatsApp ownership/voice failure cluster in `v2_experiments.ts`, patching that layer first, then I’ll rerun a short miner batch and verify the rejection mix shifts. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-49]
- I’m resuming exactly at the post-ownership patch point in `v2_experiments.ts`: rerun the short whole-corpus batch, inspect whether the WhatsApp human-thread ownership failures dropped, and only then decide whether the long monitor should restart. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-50]
- Then I’ll rerun the same short batch once more. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-51]
- I’m resuming on the narrow path we already scoped: validate the latest `v2_experiments.ts` patch, then either keep the miner running or fix the next real bottleneck and rerun. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-52]
- I’m validating and then rerunning the same short batch again. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-53]
- First I’m reopening the current code and applying the patch in small verified hunks, then I’ll run typecheck/tests and a targeted batch before restarting the miner. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-54]
- I’m patching those two functions directly, then I’ll run targeted checks on `Unnati`, `Santiago`, `Priya Amex`, and `Taylor Kella` before I restart the loop. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-55]
- The change is: author from family/context first, then assign domain/lens from the authored case, so valid evidence no longer dies under nonsense domain attribution. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-56]
- I’m validating and then forcing one more batch so the active pool rebalances under the new floor before the monitor resumes. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-57]
- I’m checking the live benchmark mix first, then I’ll prune assistant-heavy active cases down to the floor we actually need and start the whole-corpus miner under the new human-first scheduler. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-58]
- I’m finishing the runtime facet/reasoning metadata, then wiring facet coverage into benchmark readiness and the Evolution UI before running validation. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-59]
- only then assign domain + lens as evaluation metadata [confidence: strong] [status: active] [recurrence: 1][^item-next_step-60]

## Sources
[^claim-1]: items cross-project:next_step:7b15bcf4cb30341c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4174-4187
[^claim-2]: items cross-project:next_step:ed011072cf9a1d4e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4135-4143
[^claim-3]: items cross-project:next_step:ace7704649375e33; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4125-4133
[^claim-4]: items cross-project:next_step:aaf215ec64057e44; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3908-3918
[^claim-5]: items cross-project:next_step:fd749a7b97f1308c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3868-3876
[^claim-6]: items cross-project:next_step:b665c01ab1ca1150; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3758-3759
[^claim-7]: items cross-project:next_step:5e4d4b48646168bd; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3722-3733
[^item-next_step-1]: items cross-project:next_step:7b15bcf4cb30341c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4174-4187
[^item-next_step-2]: items cross-project:next_step:ed011072cf9a1d4e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4135-4143
[^item-next_step-3]: items cross-project:next_step:ace7704649375e33; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4125-4133
[^item-next_step-4]: items cross-project:next_step:aaf215ec64057e44; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3908-3918
[^item-next_step-5]: items cross-project:next_step:fd749a7b97f1308c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3868-3876
[^item-next_step-6]: items cross-project:next_step:b665c01ab1ca1150; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3758-3759
[^item-next_step-7]: items cross-project:next_step:5e4d4b48646168bd; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3722-3733
[^item-next_step-8]: items cross-project:next_step:52c09f4efddeef83; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3312-3317
[^item-next_step-9]: items cross-project:next_step:6ce8f88565d33862; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3225-3226
[^item-next_step-10]: items cross-project:next_step:a26ea384eec66172; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-next_step-11]: items cross-project:next_step:0a4dae9c518f2125; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-next_step-12]: items cross-project:next_step:54a1dc718f4b9ff3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2763-2777
[^item-next_step-13]: items cross-project:next_step:23f889c5dd101e6a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2702-2703
[^item-next_step-14]: items cross-project:next_step:6054e1229c60b6e1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2521-2529
[^item-next_step-15]: items cross-project:next_step:20af297c91f5fe3a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2391-2399
[^item-next_step-16]: items cross-project:next_step:b779012aee3b82cc; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2352-2360
[^item-next_step-17]: items cross-project:next_step:8ee6577fa2fffc48; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1552-1558
[^item-next_step-18]: items cross-project:next_step:a77d578a408e5942; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1489-1500
[^item-next_step-19]: items cross-project:next_step:b4ece750952a6940; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1448-1469
[^item-next_step-20]: items cross-project:next_step:782eb799ca55a854; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1438-1443
[^item-next_step-21]: items cross-project:next_step:0e9ac52ef5a74f0a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1408-1409
[^item-next_step-22]: items cross-project:next_step:1a4a1d94d6e6d948; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1340-1347
[^item-next_step-23]: items cross-project:next_step:339abedea4749668; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-next_step-24]: items cross-project:next_step:736fb60bc8e96b77; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-next_step-25]: items cross-project:next_step:9f44f529794ae11c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1334-1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1335-1339
[^item-next_step-26]: items cross-project:next_step:cbfc54c4382c7f4e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1161-1176
[^item-next_step-27]: items cross-project:next_step:9afa3be675035f5f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1156-1157
[^item-next_step-28]: items cross-project:next_step:fad0ecfadd7bb316; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1116-1117
[^item-next_step-29]: items cross-project:next_step:4236edd458389781; 019d837d-d249-71c3-9637-b8d6992ce805 lines 161-162
[^item-next_step-30]: items cross-project:next_step:1e4210d112a98ae4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 135-148
[^item-next_step-31]: items cross-project:next_step:21a06d9fbebcc967; 019d837d-d249-71c3-9637-b8d6992ce805 lines 10-12
[^item-next_step-32]: items cross-project:next_step:86e424e2bf9a5de7; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-next_step-33]: items cross-project:next_step:bf104b20e5c2193e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-next_step-34]: items cross-project:next_step:baffbcdc89e18629; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-next_step-35]: items cross-project:next_step:cc3f08f5f29706c2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 6-6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 7-8
[^item-next_step-36]: items cross-project:next_step:474df899caf2d1b1; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 70912-70920
[^item-next_step-37]: items cross-project:next_step:341845f611343ad6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 70470-70474
[^item-next_step-38]: items cross-project:next_step:7c969c63a4ebc247; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 70213-70218
[^item-next_step-39]: items cross-project:next_step:6443429ac4805d3a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 69883-69904
[^item-next_step-40]: items cross-project:next_step:ea623e4c4d8f31b3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 69321-69352
[^item-next_step-41]: items cross-project:next_step:1f58818dd8f614d4; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 69269-69279
[^item-next_step-42]: items cross-project:next_step:bca52b89abb871a4; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 67962-67967
[^item-next_step-43]: items cross-project:next_step:bd3f8bdd2f1b7b08; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 63636-63648
[^item-next_step-44]: items cross-project:next_step:948cca22cfc26ee5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 63305-63311
[^item-next_step-45]: items cross-project:next_step:0139d4a89c3b7b67; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 62933-62943
[^item-next_step-46]: items cross-project:next_step:9e8ae9fdcbb656fb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 62852-62864
[^item-next_step-47]: items cross-project:next_step:b58d1f3ac3e5babe; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 62632-62644
[^item-next_step-48]: items cross-project:next_step:7a63c3645e353704; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 62122-62128
[^item-next_step-49]: items cross-project:next_step:ce5af5e8e9fc60e1; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 62016-62022
[^item-next_step-50]: items cross-project:next_step:9ed9568988fa962c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 61657-61663
[^item-next_step-51]: items cross-project:next_step:bc88b42b35d603ab; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 61638-61655
[^item-next_step-52]: items cross-project:next_step:28e1761e45a9c8af; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 61232-61238
[^item-next_step-53]: items cross-project:next_step:665b798225c900af; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 61218-61230
[^item-next_step-54]: items cross-project:next_step:71ce47f8174fabec; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 60629-60635
[^item-next_step-55]: items cross-project:next_step:1f4398983c72df47; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 60512-60524
[^item-next_step-56]: items cross-project:next_step:abd8e7494723c940; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 59182-59194
[^item-next_step-57]: items cross-project:next_step:1413f89017e1104a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 58740-58752
[^item-next_step-58]: items cross-project:next_step:5ad9e18650d064fc; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 58408-58424
[^item-next_step-59]: items cross-project:next_step:8791f353b94488a7; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57582-57588
[^item-next_step-60]: items cross-project:next_step:e4a88989fd6366f3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57242-57249
