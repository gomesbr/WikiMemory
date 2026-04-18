---
title: "Open Brain - Next Steps"
page_id: "projects/open-brain/next-steps"
domain: "open-brain"
bucket: "next-steps"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:09:13.191911Z
source_count: 3
claim_count: 7
tags:
  - wikimemory
  - project
  - open-brain
  - bucket
  - next-steps
---
# Open Brain - Next Steps

Navigation: [[projects/open-brain/index|Open Brain]] | [[projects/open-brain/communication-preferences|Open Brain - Communication Preferences]] | [[projects/open-brain/workflow-rules|Open Brain - Workflow Rules]] | [[projects/open-brain/architecture|Open Brain - Architecture]] | [[projects/open-brain/code-map|Open Brain - Code Map]] | [[projects/open-brain/current-state|Open Brain - Current State]] | [[projects/open-brain/tasks|Open Brain - Tasks]] | [[projects/open-brain/outcomes|Open Brain - Outcomes]] | [[projects/open-brain/failures|Open Brain - Failures]] | [[projects/open-brain/decisions|Open Brain - Decisions]] | [[projects/open-brain/open-questions|Open Brain - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- The next steps involve making minimal runtime fixes and running focused tests to catch remaining issues. [latent: implicit_next_steps] [confidence: strong][^claim-1]
- Temporal items will be organized in the order of active, historical, and superseded, sorted by last seen. [latent: implicit_next_steps] [confidence: strong][^claim-2]
- Introducing an LLM in Phase 5 will enhance recall on implicit knowledge, aiding in extracting decisions and architecture notes. [latent: implicit_next_steps] [confidence: strong][^claim-3]
- Grounding Phase 2 in the current state and real trace structure will precede asking normalization decisions that affect design. [latent: implicit_next_steps] [confidence: strong][^claim-4]

## Next Step
- The next step includes refining Phase 1 after receiving answers and producing a detailed plan. [latent: implicit_next_steps] [confidence: strong][^claim-5]
- Checking the current pool state and tightening the stem-generation path is planned to prevent lagging. [latent: implicit_next_steps] [confidence: strong][^claim-6]
- A targeted augmentation against stems will be performed, followed by pruning excess to maintain a minimal pool. [latent: implicit_next_steps] [confidence: strong][^claim-7]

### Canonical Items
- I’m making the minimal runtime fix and then I’ll run the focused Phase 7 suite to catch any remaining issues. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-1]
- - temporal items: `active > historical > superseded`, then last_seen desc [confidence: strong] [status: active] [recurrence: 1][^item-next_step-2]
- Introducing an LLM in Phase 5 now would mainly buy you better recall on messy, implicit knowledge: it can pull out decisions, preferences, next steps, and architecture notes even when they’re phrased indirectly or spread across a segment. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-3]
- I’m grounding Phase 2 in the current `WikiMemory` state and the real trace structure first, then I’ll ask only the normalization decisions that still materially affect the design. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-4]
- I’ll wait for your answers, then I’ll refine Phase 1 and only after that produce the detailed Phase 1 plan. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-5]
- I’m checking the current pool state and then I’ll tighten the stem-generation path so `who` and `where` stop lagging while we keep the pool minimal and gap-free. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-6]
- I’m doing one last targeted augmentation against those stems, then I’ll prune back any excess `what` so the pool stays minimal instead of growing for no reason. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-7]
- I’m switching the stem gaps to enforce a real 10% share floor against the active pool size, then I’ll do one last targeted refill/prune cycle. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-8]
- I’m doing one more targeted batch focused on those stems, then I’ll switch to pruning so we end at the smallest balanced pool instead of just accumulating more cases. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-9]
- I’m running a targeted positive refill next so we add only the missing stem types, then I’ll prune back the excess `what` inventory. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-10]
- I’m running a quick compile check now, then I’ll do a real rebalance pass on the active experiment and only stop when the pool is both stem-balanced and gap-free. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-11]
- I’m patching two things together: stricter stem targets and a final “minimal balanced pool” pass after refill, so we don’t fix the mix and then immediately drift back to an oversized queue. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-12]
- I’m wiring the stricter 10% floors into the actual gap engine, then I’ll run a targeted rebalance so we end up with the smallest pool that still satisfies every phase. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-13]
- Then I’ll add a minimal-pool pruning pass that removes excess `what` cases only when the projected pool still stays fully gap-free. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-14]
- I’m checking the current stem-target plumbing first, then I’ll finish the rebalance logic and prune excess `what` cases without reopening any phase gaps. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-15]
- I’m moving the stem target to an absolute 10%-of-certification-floor minimum and then I’ll prune the excess inventory down toward the smallest reviewable set that still stays gap-free. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-16]
- I’m tightening the stem rule to a real 10% floor for `what/who/how/when/where/why`, then I’ll shrink the active pool down to the smallest gap-free set instead of letting review inventory keep growing. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-17]
- I’m running a build so the code-side rule change is fully compiled too, then I’ll give you the final distribution and gap state. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-18]
- I’m fixing that now, then I’ll rerun the targeted augmentation. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-19]
- I’ve strengthened the seed selection and prompt so the writer sees cases that can actually support `who/when/where/why`. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-20]
- I’m running a typecheck now before I touch the live pool, then I’ll do a controlled rebalance and verify both the stem mix and the gap state. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-21]
- Next I’m adding stem-aware targets and then I’ll run a controlled rebalance so we improve the pool without reopening the benchmark gaps. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-22]
- I’m wiring question-stem counts into projected coverage and gap math first, then I’ll make generation/refill respect those gaps. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-23]
- I’m adding question-shape diversity as a real pool rule and then I’ll rebalance the active pool against it while keeping the benchmark gaps closed. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-24]
- I’m checking the authoring path now to add stem diversity as a first-class pool rule, then I’ll rebalance the active pool against that new rule while preserving the phase thresholds. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-25]
- I’m adding question-shape diversity as a real pool rule, not a one-off rebalance, then I’ll rebalance the active pool and verify it stays gap-free. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-26]
- I’m doing a final build so the fix is on disk in the runtime artifacts too, then I’ll wrap with the exact end state. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-27]
- I’m stopping those orphaned cleanup workers first, then I’ll do a controlled recovery in smaller steps so we get to a stable no-gap state instead of fighting a moving target. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-28]
- I’m validating that, then I’ll rerun cleanup/refill and keep it targeted until the gap snapshot is fully clean. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-29]
- I’m tightening that selection logic first, then I’ll rerun cleanup/refill and stop only when the snapshot is clean. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-30]
- I’m fixing the refill at the pool-balance layer so it can’t reintroduce assistant-heavy stale cases, then I’ll rerun cleanup/refill until the active gap snapshot is clean. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-31]
- I’m stopping that stray loop and then doing one controlled human-recovery refill pass so we end on a stable, trustworthy state. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-32]
- I’m loosening that floor during human recovery so the loop can stale enough assistant-heavy cases first, then refill back to a healthy mix. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-33]
- I’m running the full cleanup + refill cycle now, then I’ll verify the end-state snapshot instead of stopping at “the function works.” [confidence: strong] [status: active] [recurrence: 1][^item-next_step-34]
- I’m giving the authoring calls a realistic timeout budget now and then I’ll rerun the refill. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-35]
- I’m running a quick validation next, then I’ll rerun cleanup and check whether the pool closes all gaps. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-36]
- Next I’m tightening the human-seed refill path and then I’ll rerun cleanup + refill until the pool comes back with no gaps. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-37]
- I’m fixing that model-call layer and then wiring it into human-gap refill so we can close the pool with the right kinds of cases instead of just spinning. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-38]
- If we don’t fix that root filter, we’ll keep cleaning good junk out and then failing to bring back the right kinds of cases. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-39]
- First I’m checking the current refill/reactivation paths around human-share and clarify recovery so we can fix the mechanism and then rerun cleanup end-to-end. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-40]
- I’m filling the clarify shortage first, then I’ll push the human/topology recovery in longer-running batches without the broken assistant-heavy path. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-41]
- I’m switching it to targeted stale reactivation plus human-only positive generation, then I’ll rerun the full cleanup from the current experiment state. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-42]
- I’m tightening that generation path now and then I’ll rerun cleanup until the pool closes cleanly. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-43]
- We need both pieces working together: reactivate the good human stale cases and generate additional human cases, then only trim nonhuman cases once we’re safely above the stage minimum. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-44]
- Next I’m rerunning the retroactive cleanup on the same experiment with the new refill loop and then I’ll compare the final gap state against the thresholds to confirm whether the pending pool is actually clean and complete. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-45]
- I’m running a typecheck first, then I’ll execute the cleanup again on the experiment and inspect the final gap state directly. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-46]
- I’ve got the patch shape: keep the cleanup pruning/repair as-is, then replace the one-shot weak refill with an iterative, gap-aware recovery loop that uses the stronger positive backfill path and keeps going until the penalty actually drops to zero or we st... [confidence: strong] [status: active] [recurrence: 1][^item-next_step-47]
- I have the exact failure path now: cleanup calls clarify refill first, then a broad positive refill that does not sufficiently preserve the post-cleanup clarify/human topology constraints. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-48]
- I’m fixing the refill path at the loop level and then rerunning the retroactive cleanup end-to-end until the pending pool is back to a no-gap state. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-49]
- I’m using that instead of improvising a one-off call, then I’ll compare the pending/reviewable state before and after. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-50]
- The API route is session-protected and the first DB role guess was wrong, so I’m checking the local compose config for the correct database credentials and then I’ll run the cleanup directly against the latest experiment. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-51]
- I found the cleanup function, but it isn’t exposed as an API route, so I’m going to invoke it directly against the latest experiment and then verify the before/after queue state from the experiment payloads. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-52]
- I’m checking the cleanup entrypoint and the current experiment target first, then I’ll run the retroactive cleanup and verify whether the pending queue quality actually improved. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-53]
- I’m finishing the integration points now: wiring the authoring-loop state into the existing experiment payloads, then tightening the retroactive repair/refill path so the old pending inventory is repaired with the same stricter logic we use for new cases. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-54]
- I’m picking this back up at the authoring-loop layer and wiring the remaining pieces in the same holistic path: writer/evaluator routing, batch ledger/state, then retroactive repair and targeted refill. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-55]
- I’m continuing at the authoring-loop layer now: schema/types first, then I’ll wire contracts, trust, and the new writer/evaluator path through the existing case-generation flow so this lands holistically rather than as one-off fixes. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-56]
- The good news is the codebase already has most of the refill machinery we need, so I can connect the hardened authoring gate to retroactive cleanup and then reuse the existing gap-aware refill instead of adding another generator path. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-57]
- Next I’m wiring the authoring-specific types/state and then the writer/evaluator path. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-58]
- I’m implementing the authoring-loop hardening at the loop-control and authoring layers first: schema/config/types, then the batch contract/ledger path, then the writer/evaluator routing and retroactive cleanup hooks. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-59]
- I’m now wiring those pieces together so the authoring loop records contracts/trust and then routes cleanup-created shortages back through the existing gap-aware refill flow. [confidence: strong] [status: active] [recurrence: 1][^item-next_step-60]

## Sources
[^claim-1]: items open-brain:next_step:41b6953d3dcac215; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2857-2870
[^claim-2]: items open-brain:next_step:a63ecd7934ba397f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^claim-3]: items open-brain:next_step:799ee148372a62de; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^claim-4]: items open-brain:next_step:a56309f501ad4be0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 246-257
[^claim-5]: items open-brain:next_step:3130e45447ac2895; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^claim-6]: items open-brain:next_step:c3b5ae0111098d33; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88004-88012
[^claim-7]: items open-brain:next_step:e08d7d3e1fd13589; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87955-87961
[^item-next_step-1]: items open-brain:next_step:41b6953d3dcac215; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2857-2870
[^item-next_step-2]: items open-brain:next_step:a63ecd7934ba397f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-next_step-3]: items open-brain:next_step:799ee148372a62de; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-next_step-4]: items open-brain:next_step:a56309f501ad4be0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 246-257
[^item-next_step-5]: items open-brain:next_step:3130e45447ac2895; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-next_step-6]: items open-brain:next_step:c3b5ae0111098d33; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88004-88012
[^item-next_step-7]: items open-brain:next_step:e08d7d3e1fd13589; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87955-87961
[^item-next_step-8]: items open-brain:next_step:e416d338189bf857; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87935-87941
[^item-next_step-9]: items open-brain:next_step:505b423144c110f2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87867-87873
[^item-next_step-10]: items open-brain:next_step:d9ac0a211887a4a0; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87781-87787
[^item-next_step-11]: items open-brain:next_step:dcad495d22f74349; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87765-87771
[^item-next_step-12]: items open-brain:next_step:69ee490bb9edc601; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87693-87694
[^item-next_step-13]: items open-brain:next_step:b90b5733d7cee978; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87613-87621
[^item-next_step-14]: items open-brain:next_step:39a4c6f6acabb7ea; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87603-87611
[^item-next_step-15]: items open-brain:next_step:3ca152ad333920a2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87593-87601
[^item-next_step-16]: items open-brain:next_step:fbe1b9e3ff68af44; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87563-87569
[^item-next_step-17]: items open-brain:next_step:e4dfe08d7432329e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87552-87561
[^item-next_step-18]: items open-brain:next_step:d2bd382deaa0eb65; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87523-87529
[^item-next_step-19]: items open-brain:next_step:d3faff5493bfef74; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87416-87422
[^item-next_step-20]: items open-brain:next_step:ac11c1ffbfd4d7ae; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87408-87414
[^item-next_step-21]: items open-brain:next_step:cff587c8f80c1ae6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87269-87275
[^item-next_step-22]: items open-brain:next_step:d23114fd8c25eba2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87077-87087
[^item-next_step-23]: items open-brain:next_step:d1355d583f5792ff; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87065-87075
[^item-next_step-24]: items open-brain:next_step:3473c216606a7313; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87055-87063
[^item-next_step-25]: items open-brain:next_step:279f483649731e05; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87031-87039
[^item-next_step-26]: items open-brain:next_step:996792c89fc47507; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87021-87029
[^item-next_step-27]: items open-brain:next_step:4cca8ee7a46686bc; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86972-86980
[^item-next_step-28]: items open-brain:next_step:8d998ebff0283f5f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86836-86844
[^item-next_step-29]: items open-brain:next_step:08370def455d0e84; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86786-86794
[^item-next_step-30]: items open-brain:next_step:18356f6c9b4c3610; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86716-86726
[^item-next_step-31]: items open-brain:next_step:f7fd6724b9610265; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86699-86714
[^item-next_step-32]: items open-brain:next_step:83f5e97433cbdd32; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86638-86646
[^item-next_step-33]: items open-brain:next_step:fc85cdae3c93341d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86591-86602
[^item-next_step-34]: items open-brain:next_step:18357c57c93a4527; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86581-86589
[^item-next_step-35]: items open-brain:next_step:22ce579317f47f9d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86525-86531
[^item-next_step-36]: items open-brain:next_step:e90424389150da82; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86433-86441
[^item-next_step-37]: items open-brain:next_step:6f7f7476f8c006cd; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86355-86365
[^item-next_step-38]: items open-brain:next_step:263ea8d56018bfa1; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86241-86249
[^item-next_step-39]: items open-brain:next_step:0c94f0e091ff73a1; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86141-86152
[^item-next_step-40]: items open-brain:next_step:00372a3bdb5dccff; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86079-86085
[^item-next_step-41]: items open-brain:next_step:1d28ac9948cc559e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86038-86044
[^item-next_step-42]: items open-brain:next_step:c4b09e7439823a86; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85957-85968
[^item-next_step-43]: items open-brain:next_step:7d41b46e9064a80c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85784-85790
[^item-next_step-44]: items open-brain:next_step:ad8f8849bdd51eb2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85753-85761
[^item-next_step-45]: items open-brain:next_step:717753830363506e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85666-85672
[^item-next_step-46]: items open-brain:next_step:a994eca118923f02; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85656-85664
[^item-next_step-47]: items open-brain:next_step:039765c54aa42568; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85642-85643
[^item-next_step-48]: items open-brain:next_step:fbb60477ce6c3576; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85576-85584
[^item-next_step-49]: items open-brain:next_step:d7da04860fc1506e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85536-85542
[^item-next_step-50]: items open-brain:next_step:e9f90c98726b82a9; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85493-85501
[^item-next_step-51]: items open-brain:next_step:4b90a9ef834df4ed; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85483-85491
[^item-next_step-52]: items open-brain:next_step:60f56e3a4861337e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85471-85481
[^item-next_step-53]: items open-brain:next_step:d131e1737ec3f413; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85459-85469
[^item-next_step-54]: items open-brain:next_step:398ea8ed113f2f8d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85031-85041
[^item-next_step-55]: items open-brain:next_step:71cc71f854f72c44; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84722-84736
[^item-next_step-56]: items open-brain:next_step:1167b55132047d6b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84500-84508
[^item-next_step-57]: items open-brain:next_step:a5c333b0f8abb098; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84397-84405
[^item-next_step-58]: items open-brain:next_step:b186ade32bee034e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84375-84385
[^item-next_step-59]: items open-brain:next_step:999df792d047d577; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84345-84351
[^item-next_step-60]: items open-brain:next_step:6d5eb2919deb0b41; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84240-84252
