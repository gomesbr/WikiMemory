---
title: "Open Brain - Failures"
page_id: "projects/open-brain/failures"
domain: "open-brain"
bucket: "failures"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:09:00.379524Z
source_count: 2
claim_count: 6
tags:
  - wikimemory
  - project
  - open-brain
  - bucket
  - failures
---
# Open Brain - Failures

Navigation: [[projects/open-brain/index|Open Brain]] | [[projects/open-brain/communication-preferences|Open Brain - Communication Preferences]] | [[projects/open-brain/workflow-rules|Open Brain - Workflow Rules]] | [[projects/open-brain/architecture|Open Brain - Architecture]] | [[projects/open-brain/code-map|Open Brain - Code Map]] | [[projects/open-brain/current-state|Open Brain - Current State]] | [[projects/open-brain/tasks|Open Brain - Tasks]] | [[projects/open-brain/outcomes|Open Brain - Outcomes]] | [[projects/open-brain/decisions|Open Brain - Decisions]] | [[projects/open-brain/next-steps|Open Brain - Next Steps]] | [[projects/open-brain/open-questions|Open Brain - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- Common failure patterns include issues with data linkage and specific graph nodes. [latent: recurring_failure_patterns] [confidence: strong][^claim-1]
- Identifying the broader failure mode is crucial for effective resolution. [latent: recurring_failure_patterns] [confidence: strong][^claim-2]
- Fixes should be implemented at the appropriate abstraction layer to prevent similar issues. [latent: implicit_dos_and_donts] [confidence: strong][^claim-3]

## Failure
- When fixing a bug, a minimal runtime fix should be made first, followed by running tests to catch remaining issues. [latent: implicit_next_steps] [confidence: strong][^claim-4]
- Project-scoped rules include current state, decisions, architecture notes, task requests, next steps, open questions, failures, and risks. [latent: project_identity_and_scope] [confidence: strong][^claim-5]
- Failures or invalid JSON must preserve the last committed bootstrap state to ensure stability. [latent: implicit_dos_and_donts] [confidence: strong][^claim-6]

### Canonical Items
- - Example pattern: "data linkage issue" vs "one bad graph node". [confidence: strong] [status: historical] [recurrence: 2][^item-failure-1]
- - Identify the broader failure mode. [confidence: strong] [status: historical] [recurrence: 2][^item-failure-2]
- - Implement the fix at the right abstraction layer so similar issues are also prevented. [confidence: strong] [status: historical] [recurrence: 2][^item-failure-3]
- - State the underlying class of failure, not the single symptom. [confidence: strong] [status: historical] [recurrence: 2][^item-failure-4]
- When fixing a bug: [confidence: strong] [status: historical] [recurrence: 2][^item-failure-5]
- I’m making the minimal runtime fix and then I’ll run the focused Phase 7 suite to catch any remaining issues. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-6]
- - `current_state`, `decision`, `architecture_note`, `task_request`, `next_step`, `open_question`, `failure`, project-scoped rules [confidence: strong] [status: historical] [recurrence: 1][^item-failure-7]
- - `project`: `identity=4`, `current_state=6`, `architecture=5`, `project_rules=4`, `tasks=5`, `next_steps=5`, `open_questions=4`, `failures_risks=4` [confidence: strong] [status: historical] [recurrence: 1][^item-failure-8]
- - failed synthesis or invalid JSON must preserve the last committed bootstrap state [confidence: strong] [status: historical] [recurrence: 1][^item-failure-9]
- - optionally `failure` when clearly global [confidence: strong] [status: historical] [recurrence: 1][^item-failure-10]
- - Fixed Phase 6 index-page synthesis/citation bug in [wikimemory/wiki.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/wikimemory/wiki.py) [confidence: strong] [status: historical] [recurrence: 1][^item-failure-11]
- - I also fixed a real Windows integration bug the smoke test exposed: BOM-encoded JSON config/state files are now accepted across the pipeline in [wikimemory/discovery.py](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/wikimemory/discovery.py),... [confidence: strong] [status: historical] [recurrence: 1][^item-failure-12]
- I found one mechanical issue while wiring things up: the first extractor patch landed one directory too high under the workspace root instead of inside `WikiMemory`. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-13]
- ## Incremental and Failure Behavior [confidence: strong] [status: historical] [recurrence: 1][^item-failure-14]
- - `decision`, `architecture_note`, `code_location`, `current_state`, `task_request`, `outcome`, `failure`, `next_step`, `open_question` default to the best non-global segment domain [confidence: strong] [status: historical] [recurrence: 1][^item-failure-15]
- - `failure` -> `failures` [confidence: strong] [status: historical] [recurrence: 1][^item-failure-16]
- - `outcome` and `failure` default to `historical` [confidence: strong] [status: historical] [recurrence: 1][^item-failure-17]
- - Fatal failures: [confidence: strong] [status: historical] [recurrence: 1][^item-failure-18]
- - validation failure after staging [confidence: strong] [status: historical] [recurrence: 1][^item-failure-19]
- `communication_preference`, `do_rule`, `dont_rule`, `workflow_rule`, `decision`, `architecture_note`, `code_location`, `current_state`, `task_request`, `outcome`, `failure`, `next_step`, `open_question` [confidence: strong] [status: historical] [recurrence: 1][^item-failure-20]
- Should temporal items like `current_state`, `next_step`, `outcome`, and `failure` carry a lifecycle marker such as: [confidence: strong] [status: historical] [recurrence: 1][^item-failure-21]
- - status tracked (`new`, `growing`, `stable`, `complete`, `tombstoned`, `error`, `duplicate`) [confidence: strong] [status: historical] [recurrence: 1][^item-failure-22]
- I’m testing whether that’s a formatting quirk, encoding issue, or genuinely non-standard JSONL. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-23]
- The quick type-count probe exposed something useful: these traces aren’t guaranteed to be trivially parseable line-by-line with a naive JSON reader, which is exactly the kind of Phase 1 boundary issue we want to catch early. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-24]
- - The broader failure was pool-balance logic drift: the system was treating the old static stem minimums as removable thresholds, so it kept too many excess cases and stayed skewed even after we introduced the new live `10%` rule. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-25]
- I found the main issue: the minimizer is still scoring removable stems against the old fixed floors, so it’s not aggressively shrinking the pool toward the new 10%-of-live-pool target. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-26]
- I’ve confirmed the live issue: the pool is only failing on `who` and `where`, and because the 10% rule is based on live pool size, the cleanest fix may be to prune excess cases rather than add more. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-27]
- The minimizer found the right issue: it was only willing to remove a case if one removal solved the entire imbalance in a single step. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-28]
- - The broader failure mode was question-shape imbalance: the pool could be “benchmark-gap free” while still being too dominated by `what` questions to train the kind of usage you actually care about. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-29]
- I hit a local scoping bug in the new seed-ranking path. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-30]
- - The broader issue is question-shape imbalance: the pool is still heavily dominated by `what` questions, with almost no `who/when/where/why`. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-31]
- - The broader failure mode was that refill was optimizing local supply counts while allowing the pool mix to regress globally. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-32]
- The current pool is exactly what we expected from the bug: total and clarify are fine, but human share is still below threshold. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-33]
- error [confidence: strong] [status: historical] [recurrence: 1][^item-failure-34]
- I found the refill math issue too: when human share was low, the rebalancer was still protecting the full final pool size, which made it mathematically impossible for refill to catch up. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-35]
- I’m using the `openai-docs` skill for this part because the remaining refill blocker is a GPT‑5.4 API request-shape issue, and I want to align the authoring calls with current official behavior before I rerun the loop. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-36]
- I found another important root issue: even with a better refill, the current target estimator can massively overstate how many human cases we need unless the pool is rebalanced hard first. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-37]
- I’m working on the refill failure as a loop-level issue, not just rerunning cleanup. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-38]
- I’m checking the official GPT‑5.4 usage pattern now so we fix the refill path on the right model contract instead of layering more retries on top of a broken call. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-39]
- I found another important refill blocker: the fast positive-augmentation path is currently broken at the model call level, which helps explain why the loop keeps falling back to slower underproductive recovery. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-40]
- I’m focusing on the refill failure as a loop-level capability gap, not a one-off batch issue. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-41]
- I’m filling the clarify shortage first, then I’ll push the human/topology recovery in longer-running batches without the broken assistant-heavy path. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-42]
- We fixed the destructive part of refill, but the remaining issue is supply: the human-case refill path is still too underproductive for the gaps cleanup creates. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-43]
- I’m checking the stale candidate inventory now so we can see whether the issue is “not enough good human cases exist” or “the selector still isn’t prioritizing them strongly enough.” [confidence: strong] [status: historical] [recurrence: 1][^item-failure-44]
- I caught one follow-on issue in the patch: the refill generator needs the stage minimum before it decides whether it’s allowed to rebalance. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-45]
- I found two concrete refill bugs, not just one: first, stale reactivation is too permissive when the pool has a human/topology gap [confidence: strong] [status: historical] [recurrence: 1][^item-failure-46]
- pairfailurecounts [confidence: strong] [status: historical] [recurrence: 1][^item-failure-47]
- I have the exact failure path now: cleanup calls clarify refill first, then a broad positive refill that does not sufficiently preserve the post-cleanup clarify/human topology constraints. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-48]
- I’ve confirmed the issue is exactly where we expected: cleanup is pruning correctly, but the refill path is still repopulating the pool with the wrong composition after cleanup. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-49]
- First I’m checking the current refill/cleanup flow and the relevant experiment code paths so we can correct the broader failure mode instead of patching one run. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-50]
- - Broader failure theme: the `repair/cleanup` side is working, but the `refill` side is still not restoring a review-ready pool. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-51]
- - Added per-batch authoring contracts, trust states, failure-bucket summaries, answer-shape types, and loop-state payloads. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-52]
- - The broader failure was that the case loop still had split logic: new authoring was getting smarter, but supplemental generation, retroactive cleanup, and loop-state tracking were still weaker and disconnected. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-53]
- I’m doing one last host-side check with `curl.exe` instead of PowerShell’s web client, because the PowerShell error looks transport-related rather than application-related. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-54]
- The API container isn’t logging an obvious failure, so I’m checking the root endpoint as a sanity test. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-55]
- That will tell us whether this is just a startup delay or a real runtime issue caused by the migration/build. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-56]
- The remaining issues were exactly the kind we want typecheck to catch: preserving verifier provenance when we override admission decisions, and making sure the blocker summary uses the canonical failure-bucket shape. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-57]
- Typecheck caught two real consistency issues: the repaired admission-decision override needs to preserve the verifier metadata, and my blocker summary call was using the wrong helper shape. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-58]
- I caught one consistency issue while wiring the cleanup pass: the authoring loop-state builder already owns everything it needs, so I’m removing the extra experiment object plumbing instead of expanding the shape unnecessarily. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-59]
- - Cluster excluded/pending-bad cases by failure family and process them in batches. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-60]

## Sources
[^claim-1]: items open-brain:failure:9d16f84343f86972; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-2]: items open-brain:failure:54f56486df5e778c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-3]: items open-brain:failure:6b056873095a1b28; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-4]: items open-brain:failure:5f739e22b2069040; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-5]: items open-brain:failure:b50a20e7b73ac10d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^claim-6]: items open-brain:failure:b1d10b0d14c70361; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-failure-1]: items open-brain:failure:9d16f84343f86972; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-failure-2]: items open-brain:failure:54f56486df5e778c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-failure-3]: items open-brain:failure:6b056873095a1b28; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-failure-4]: items open-brain:failure:48f36fed521cf39c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-failure-5]: items open-brain:failure:5f739e22b2069040; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-failure-6]: items open-brain:failure:7edbe4455b2e273e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2857-2870
[^item-failure-7]: items open-brain:failure:b50a20e7b73ac10d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-failure-8]: items open-brain:failure:3a224896ca58f686; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-failure-9]: items open-brain:failure:b1d10b0d14c70361; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-failure-10]: items open-brain:failure:278a20cb737f6b21; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2635-2638; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2641-2641; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2642-2643
[^item-failure-11]: items open-brain:failure:327aedf9e880af45; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2376-2381
[^item-failure-12]: items open-brain:failure:74e274a8c7bfe4b2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1824-1824; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1825-1828
[^item-failure-13]: items open-brain:failure:dbfd070a7a531331; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1161-1176
[^item-failure-14]: items open-brain:failure:d5ae25e265b1cd00; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-failure-15]: items open-brain:failure:b786024c4de3ea56; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-failure-16]: items open-brain:failure:9c140fb489cd8320; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-failure-17]: items open-brain:failure:df524005ad01a71b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-failure-18]: items open-brain:failure:736debf25ab643fd; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-failure-19]: items open-brain:failure:c0f94fd9c87244a4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-failure-20]: items open-brain:failure:3ca3c18b54e45dca; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-failure-21]: items open-brain:failure:506322626fafb057; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-failure-22]: items open-brain:failure:738c9cf6d0eaa126; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-failure-23]: items open-brain:failure:411d99e2de552360; 019d837d-d249-71c3-9637-b8d6992ce805 lines 43-51
[^item-failure-24]: items open-brain:failure:8bb0bea26097e2d5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 43-51
[^item-failure-25]: items open-brain:failure:3d2327e256668644; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88082-88085
[^item-failure-26]: items open-brain:failure:f154f38ed8f8dad2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88038-88044
[^item-failure-27]: items open-brain:failure:3b7306ab5af96b4a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88014-88020
[^item-failure-28]: items open-brain:failure:18d8225e5be630d6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87889-87895
[^item-failure-29]: items open-brain:failure:088b775d79ca5871; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87539-87543
[^item-failure-30]: items open-brain:failure:a5366a653335240e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87416-87422
[^item-failure-31]: items open-brain:failure:43432e83bb65e557; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87008-87013
[^item-failure-32]: items open-brain:failure:56d575897712ac0a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86988-86992
[^item-failure-33]: items open-brain:failure:833093c57f673b58; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86810-86816
[^item-failure-34]: items open-brain:failure:2698ffb8e53f01a1; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 12785-12793; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13659-13664; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13996-14018
[^item-failure-35]: items open-brain:failure:bea6ff7f4598e400; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86591-86602
[^item-failure-36]: items open-brain:failure:275303f712eeda23; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86469-86478
[^item-failure-37]: items open-brain:failure:ee52e382fef81114; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86399-86405
[^item-failure-38]: items open-brain:failure:f302961f95b7d4c2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86342-86353
[^item-failure-39]: items open-brain:failure:1960436f0110a7cd; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86259-86267
[^item-failure-40]: items open-brain:failure:81dc122f5fe10acc; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86233-86239
[^item-failure-41]: items open-brain:failure:24c7bf379aa5345f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86079-86085
[^item-failure-42]: items open-brain:failure:2d83c8efe5dcdbb1; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86038-86044
[^item-failure-43]: items open-brain:failure:91ed747d61170625; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85784-85790
[^item-failure-44]: items open-brain:failure:93479efca60b4a7e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85733-85741
[^item-failure-45]: items open-brain:failure:b942e7906eab158d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85705-85713
[^item-failure-46]: items open-brain:failure:8a3560c2dcd4638e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85604-85612
[^item-failure-47]: items open-brain:failure:8c8605fe0acefcf9; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 53134-53139; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85595-85602
[^item-failure-48]: items open-brain:failure:285399276166442f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85576-85584
[^item-failure-49]: items open-brain:failure:305d3c5106a7c879; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85554-85564
[^item-failure-50]: items open-brain:failure:e204cbf1aebe47e9; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85536-85542
[^item-failure-51]: items open-brain:failure:c5353440a455c0e0; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85525-85530
[^item-failure-52]: items open-brain:failure:08868a0beb70127f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85447-85447; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85448-85451
[^item-failure-53]: items open-brain:failure:c25fa68602343c03; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85447-85447; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85448-85451
[^item-failure-54]: items open-brain:failure:dd234067620d0ffd; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85419-85425
[^item-failure-55]: items open-brain:failure:f54ca0c59f321bc5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85383-85389
[^item-failure-56]: items open-brain:failure:6c2c19d590e17f7b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85375-85381
[^item-failure-57]: items open-brain:failure:e353f8f72a02e595; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85331-85339
[^item-failure-58]: items open-brain:failure:160eefa9da58b084; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85300-85312
[^item-failure-59]: items open-brain:failure:373084e9ce8595e0; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85195-85201
[^item-failure-60]: items open-brain:failure:8619064898375b2a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84001-84004; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84007-84007; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84008-84010
