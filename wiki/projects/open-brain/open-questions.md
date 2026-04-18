---
title: "Open Brain - Open Questions"
page_id: "projects/open-brain/open-questions"
domain: "open-brain"
bucket: "open-questions"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:09:19.292528Z
source_count: 3
claim_count: 5
tags:
  - wikimemory
  - project
  - open-brain
  - bucket
  - open-questions
---
# Open Brain - Open Questions

Navigation: [[projects/open-brain/index|Open Brain]] | [[projects/open-brain/communication-preferences|Open Brain - Communication Preferences]] | [[projects/open-brain/workflow-rules|Open Brain - Workflow Rules]] | [[projects/open-brain/architecture|Open Brain - Architecture]] | [[projects/open-brain/code-map|Open Brain - Code Map]] | [[projects/open-brain/current-state|Open Brain - Current State]] | [[projects/open-brain/tasks|Open Brain - Tasks]] | [[projects/open-brain/outcomes|Open Brain - Outcomes]] | [[projects/open-brain/failures|Open Brain - Failures]] | [[projects/open-brain/decisions|Open Brain - Decisions]] | [[projects/open-brain/next-steps|Open Brain - Next Steps]]
Related Domains: [[global/index|Global]]

## Summary
- The focus of these questions includes generalization of changes and linking evidence to context. [latent: partially_explicit_open_questions] [confidence: strong][^claim-1]
- Questions also address the implications of extracted items for future phases of the project. [latent: partially_explicit_open_questions] [confidence: strong][^claim-2]
- There is a need to clarify the handling of contradictory extracted items. [latent: partially_explicit_open_questions] [confidence: strong][^claim-3]

## Open Question
- Active open questions include how changes generalize beyond immediate examples. [latent: partially_explicit_open_questions] [confidence: strong][^claim-4]
- The project should focus on solving the class of problems rather than just specific examples. [latent: partially_explicit_open_questions] [confidence: strong][^claim-5]

### Canonical Items
- should [confidence: strong] [status: active] [recurrence: 2][^item-open_question-1]
- Why: [confidence: strong] [status: active] [recurrence: 2][^item-open_question-2]
- - Explain how the change generalizes beyond the immediate example. [confidence: strong] [status: active] [recurrence: 2][^item-open_question-3]
- - Show how evidence links to actors, timestamps, and context. [confidence: strong] [status: active] [recurrence: 2][^item-open_question-4]
- - Solve the class of problem, not just the exact example shown. [confidence: strong] [status: active] [recurrence: 2][^item-open_question-5]
- What changed: [confidence: strong] [status: active] [recurrence: 2][^item-open_question-6]
- - Phase 8 should be `python -m wikimemory audit` [confidence: strong] [status: active] [recurrence: 1][^item-open_question-7]
- I’m checking the current repo shape around Phase 6 outputs so the Phase 7 plan fits what’s already implemented. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-8]
- - `cross-project` and `unclassified` are valid extraction domains, but weak/unusable content should usually be skipped rather than turned into noisy items. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-9]
- - Obsidian support starts here only as stable target metadata: extracted items should carry `target_namespace` and `target_page_key` so Phase 6 can map them cleanly into Obsidian-friendly wiki pages. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-10]
- For contradictory extracted items, should Phase 5: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-11]
- For Phase 5, the main implication is that extracted items should carry stable domain/item identifiers and future page-target hints cleanly enough that wiki synthesis can map them into Obsidian pages later. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-12]
- Should Phase 5 use this fixed v1 item taxonomy? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-13]
- Should temporal items like `current_state`, `next_step`, `outcome`, and `failure` carry a lifecycle marker such as: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-14]
- To support future Obsidian wiki generation, should each extracted item also carry a lightweight future target hint like: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-15]
- When repeated items are merged, should the merged item keep: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-16]
- Let me know when I should activate plan mode [confidence: strong] [status: active] [recurrence: 1][^item-open_question-17]
- When they come, I should be able to add them (maybe some config with project name, or keywords, not sure) in some config and the process should do a full run to all files (past and present) under the root to find references of those, and track them after in... [confidence: strong] [status: active] [recurrence: 1][^item-open_question-18]
- - Absolute path should live only in local config/runtime state [confidence: strong] [status: active] [recurrence: 1][^item-open_question-19]
- - But it should define and persist the state model needed for resumable downstream processing [confidence: strong] [status: active] [recurrence: 1][^item-open_question-20]
- - Phase 1 should not implement downstream parsing/resume behavior [confidence: strong] [status: active] [recurrence: 1][^item-open_question-21]
- - Public/internal reference format should be `source_root_alias + relative_path + session_id` [confidence: strong] [status: active] [recurrence: 1][^item-open_question-22]
- For actively growing files, should the system process only fully completed lines and leave any partial trailing line untouched until the next run? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-23]
- For scheduled automation, what run cadence do you expect roughly: every few minutes, hourly, or daily? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-24]
- I was asking whether provenance/manifests should expose raw absolute paths like `C:\Users\Fabio\...`, or whether they should use an internal stable reference. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-25]
- If the same `session_id` appears in two locations with different content, should the system stop and report immediately? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-26]
- Should Phase 1 include all sessions under the root, including this new `memory-system` project’s own future sessions, or do you want include/exclude rules from day one? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-27]
- So the Phase 1 endpoint should be: [confidence: strong] [status: active] [recurrence: 1][^item-open_question-28]
- I’m grounding Phase 1 in the actual source tree now so we can remove guesswork around discovery, append behavior, and what positional anchors later phases will need. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-29]
- 15-Final product should be automated scheduled runs only [confidence: strong] [status: active] [recurrence: 1][^item-open_question-30]
- 17-Whatever makes more sense to help future phases [confidence: strong] [status: active] [recurrence: 1][^item-open_question-31]
- 7-It should not, but if it does, treat as same data, so no duplicates [confidence: strong] [status: active] [recurrence: 1][^item-open_question-32]
- What can change in the future in where the main folder sits. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-33]
- Define how humans review the wiki, how agents consume bootstrap memory, and how approvals/refresh cycles work in practice. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-34]
- For very large files, how far should Phase 1 go on checkpointing? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-35]
- How much validation should Phase 1 perform before later parsing exists? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-36]
- I need to know whether file-level status is enough, or whether we should already reserve byte/line-level resume anchors for downstream streaming. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-37]
- If a file is moved or renamed but content is the same, should it remain the same logical source for provenance purposes, or should path define identity? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-38]
- If a previously known external file disappears, should the system keep a tombstone/history record, mark it unavailable, or treat it as removed from the active source set? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-39]
- If yes, how do you want “safe to process” defined: explicit closed files only, age-based stability, or append-aware tracking? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-40]
- What do you want the exact success endpoint of Phase 1 to be: “all sources discovered and statused,” or “all sources discovered, statused, and ready for resumable streamed downstream processing”? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-41]
- What exactly should Phase 1 include and exclude? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-42]
- What file shapes count as source logs initially? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-43]
- What is the minimum provenance anchor that Phase 1 must establish for later phases: file identity only, or file identity plus reserved positional anchors for downstream event ranges? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-44]
- What matters more for initial source fingerprinting: speed, certainty, or portability? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-45]
- What source locations must be supported at launch? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-46]
- When Phase 1 hits unreadable, partial, or corrupted files, should the run continue with flags, stop immediately, or quarantine those sources for manual review? [confidence: strong] [status: active] [recurrence: 1][^item-open_question-47]
- - `how: 40` (`21.1%`) [confidence: strong] [status: active] [recurrence: 1][^item-open_question-48]
- - `what: 27` (`14.2%`) [confidence: strong] [status: active] [recurrence: 1][^item-open_question-49]
- - `what` can no longer stay inflated just because the minimizer is using stale thresholds [confidence: strong] [status: active] [recurrence: 1][^item-open_question-50]
- - `why: 31` (`16.3%`) [confidence: strong] [status: active] [recurrence: 1][^item-open_question-51]
- I’m rebuilding the service so the new pruning rule is what the running app uses going forward, not just the one-off repair I ran directly. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-52]
- We’re at the target state now: 190 active cases, every phase gap closed, and every stem at or above 10% with `what` down to 14.2%. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-53]
- The minimizer patch is in, but I caught one more detail: in this exact state, removing extra `what` questions is part of the solution too, so I’m widening the plateau-removal rule to allow that safely instead of only trimming secondary stems. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-54]
- I’m fixing that at the pruning layer first, because that should get us to a smaller, balanced pool without generating more review work. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-55]
- whatquestionsharemax [confidence: strong] [status: active] [recurrence: 1][^item-open_question-56]
- I’m doing one last targeted augmentation against those stems, then I’ll prune back any excess `what` so the pool stays minimal instead of growing for no reason. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-57]
- The new share-based gaps are showing exactly what we need: we’re close, but still short on `who / when / where / why`. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-58]
- I’m relaxing the prune rule so it can keep removing safe excess `what` cases even when the penalty only drops after several removals. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-59]
- The last blocker is mathematical: with a share cap, removing one `what` case often doesn’t lower the penalty immediately because both the numerator and denominator move together. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-60]
- I’m loosening that to allow gradual improvement, which is exactly what we need for a large `what` overage. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-61]
- The only thing left is excess `what`. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-62]
- That should make the next augmentation batch produce actor-focused questions more often instead of defaulting back to descriptive `what` forms. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-63]
- The first controlled batch helped `when/why`, but `who` is still the main gap and `where` is still short. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-64]
- That should let us raise the missing `who/when/where/why` counts in smaller controlled steps. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-65]
- I’m running a targeted positive refill next so we add only the missing stem types, then I’ll prune back the excess `what` inventory. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-66]
- The stricter targets are active now, and the pool is correctly showing the real imbalance: it’s short on `who/when/where/why` and heavily over on `what`. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-67]
- The idea is simple: once the pool is gap-free, we greedily stale the most removable cases—starting with excess `what`—but only if the projected pool remains fully compliant after each removal. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-68]
- question_stem_what [confidence: strong] [status: active] [recurrence: 1][^item-open_question-69]
- whatquestiongap [confidence: strong] [status: active] [recurrence: 1][^item-open_question-70]
- Then I’ll add a minimal-pool pruning pass that removes excess `what` cases only when the projected pool still stays fully gap-free. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-71]
- I’m checking the current stem-target plumbing first, then I’ll finish the rebalance logic and prune excess `what` cases without reopening any phase gaps. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-72]
- I’m moving the stem target from “light diversity pressure” to a hard floor now: 10% of the certification slice for each `what/who/how/when/where/why`, plus a lower `what` dominance cap so we can actually call the pool balanced. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-73]
- I’ve confirmed the current pool is still too `what`-heavy for your use case, and the existing rule is too soft. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-74]
- I’m tightening the stem rule to a real 10% floor for `what/who/how/when/where/why`, then I’ll shrink the active pool down to the smallest gap-free set instead of letting review inventory keep growing. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-75]
- But 61% of what is still not considered balanced to me. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-76]
- Remove cases if necessary (preferably the 'what' cases since there is inbalance there'). [confidence: strong] [status: active] [recurrence: 1][^item-open_question-77]
- Set a minimum of 10% per stem type for what, who, how, when, where and why. [confidence: strong] [status: active] [recurrence: 1][^item-open_question-78]
- - `how: 35` (`13.0%`) [confidence: strong] [status: active] [recurrence: 1][^item-open_question-79]
- - `what: 165` (`61.1%`) [confidence: strong] [status: active] [recurrence: 1][^item-open_question-80]

## Sources
[^claim-1]: items open-brain:open_question:92bc866d058a855d, open-brain:open_question:130d625e58d39f19, open-brain:open_question:b514769aa9a3ea08; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-2]: items open-brain:open_question:6053ddf7a9339635, open-brain:open_question:24e115fe8f24c8a4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^claim-3]: items open-brain:open_question:6053ddf7a9339635; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^claim-4]: items open-brain:open_question:92bc866d058a855d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^claim-5]: items open-brain:open_question:b514769aa9a3ea08; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-open_question-1]: items open-brain:open_question:cf8bf799b7e5fe90; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 34340-34344; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 36087-36087; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 36088-36091
[^item-open_question-2]: items open-brain:open_question:ff4950c23e2f1c40; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 42868-42868; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 42869-42873; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43321-43326
[^item-open_question-3]: items open-brain:open_question:92bc866d058a855d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-open_question-4]: items open-brain:open_question:130d625e58d39f19; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-open_question-5]: items open-brain:open_question:b514769aa9a3ea08; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44561-44562; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57250-57251
[^item-open_question-6]: items open-brain:open_question:bbb3d6d51857ecc3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5307-5311; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 37227-37232; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 39147-39147
[^item-open_question-7]: items open-brain:open_question:4bc9254901f4346f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2922-2926
[^item-open_question-8]: items open-brain:open_question:d516a4306333ace4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2599-2607
[^item-open_question-9]: items open-brain:open_question:bba0007c177855d4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-open_question-10]: items open-brain:open_question:bc4f5305ee74c0ee; 019d837d-d249-71c3-9637-b8d6992ce805 lines 988-991; 019d837d-d249-71c3-9637-b8d6992ce805 lines 994-994; 019d837d-d249-71c3-9637-b8d6992ce805 lines 995-996
[^item-open_question-11]: items open-brain:open_question:6053ddf7a9339635; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-open_question-12]: items open-brain:open_question:24e115fe8f24c8a4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-open_question-13]: items open-brain:open_question:944dacdfaf30ec04; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-open_question-14]: items open-brain:open_question:2c6ca5acc6df51c5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-open_question-15]: items open-brain:open_question:67dd80bb6b97b412; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-open_question-16]: items open-brain:open_question:ea72b1353d807019; 019d837d-d249-71c3-9637-b8d6992ce805 lines 977-980
[^item-open_question-17]: items open-brain:open_question:e2010293c68eed29; 019d837d-d249-71c3-9637-b8d6992ce805 lines 95-97
[^item-open_question-18]: items open-brain:open_question:c13665602d453bba; 019d837d-d249-71c3-9637-b8d6992ce805 lines 95-97
[^item-open_question-19]: items open-brain:open_question:21f92cecb1f30314; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-open_question-20]: items open-brain:open_question:216e5123967ffc33; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-open_question-21]: items open-brain:open_question:4160c761186f9daf; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-open_question-22]: items open-brain:open_question:8edb85ab6fcad66e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-open_question-23]: items open-brain:open_question:01f02daf45069e34; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-open_question-24]: items open-brain:open_question:83b352edbe962b6e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-open_question-25]: items open-brain:open_question:2ffea93795ecadf5; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-open_question-26]: items open-brain:open_question:43e3f87a251c451d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-open_question-27]: items open-brain:open_question:ba6ca879d8204c85; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-open_question-28]: items open-brain:open_question:54946f8def2a2748; 019d837d-d249-71c3-9637-b8d6992ce805 lines 89-89; 019d837d-d249-71c3-9637-b8d6992ce805 lines 90-94
[^item-open_question-29]: items open-brain:open_question:11afd7e08f96c8b8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 23-31
[^item-open_question-30]: items open-brain:open_question:f36d38d8936949f2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 19-21
[^item-open_question-31]: items open-brain:open_question:7521e9e3656c08ca; 019d837d-d249-71c3-9637-b8d6992ce805 lines 19-21
[^item-open_question-32]: items open-brain:open_question:eb8c5d9699d14ffc; 019d837d-d249-71c3-9637-b8d6992ce805 lines 19-21
[^item-open_question-33]: items open-brain:open_question:15e5731b34031711; 019d837d-d249-71c3-9637-b8d6992ce805 lines 19-21
[^item-open_question-34]: items open-brain:open_question:def0a2460c177160; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-35]: items open-brain:open_question:fc836087cad781a8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-36]: items open-brain:open_question:29926b2a00a9324e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-37]: items open-brain:open_question:3bc4f45f241a1462; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-38]: items open-brain:open_question:23fc5f17d145ca63; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-39]: items open-brain:open_question:a831db2a0a85d5fc; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-40]: items open-brain:open_question:bfcfe43732bca206; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-41]: items open-brain:open_question:b94217520da21312; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-42]: items open-brain:open_question:e23abe50d6986dae; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-43]: items open-brain:open_question:c59a710f09583d8d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-44]: items open-brain:open_question:bf4d9aeecd16ba73; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-45]: items open-brain:open_question:c4f37a57a787cfad; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-46]: items open-brain:open_question:1bbb774b18145235; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-47]: items open-brain:open_question:8ab3a415b848c3ec; 019d837d-d249-71c3-9637-b8d6992ce805 lines 13-13; 019d837d-d249-71c3-9637-b8d6992ce805 lines 14-18
[^item-open_question-48]: items open-brain:open_question:97a821eb308c1c8a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88082-88085
[^item-open_question-49]: items open-brain:open_question:a46182d51fbc6204; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88082-88085
[^item-open_question-50]: items open-brain:open_question:b21a06f61a510777; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88082-88085
[^item-open_question-51]: items open-brain:open_question:024c14ad6092d53e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88082-88085
[^item-open_question-52]: items open-brain:open_question:104f769052edf8e9; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88072-88080
[^item-open_question-53]: items open-brain:open_question:197431dc3f3aa573; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88072-88080
[^item-open_question-54]: items open-brain:open_question:ef42b64d3b563692; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88046-88052
[^item-open_question-55]: items open-brain:open_question:f416d0cb0996f451; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88038-88044
[^item-open_question-56]: items open-brain:open_question:b18ab6de4002aece; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 88021-88028
[^item-open_question-57]: items open-brain:open_question:7d61c22a017eb32e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87955-87961
[^item-open_question-58]: items open-brain:open_question:349d3c84a7909248; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87955-87961
[^item-open_question-59]: items open-brain:open_question:c286ea928b6551bb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87909-87915
[^item-open_question-60]: items open-brain:open_question:ca217e5b2b59e521; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87909-87915
[^item-open_question-61]: items open-brain:open_question:6e6030019be73405; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87889-87895
[^item-open_question-62]: items open-brain:open_question:698a53594a38b972; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87875-87881
[^item-open_question-63]: items open-brain:open_question:2f61e944c93eaff1; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87829-87835
[^item-open_question-64]: items open-brain:open_question:647e586c9f335c4e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87813-87819
[^item-open_question-65]: items open-brain:open_question:301ab7147b19f5af; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87799-87805
[^item-open_question-66]: items open-brain:open_question:261e64d4693665fe; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87781-87787
[^item-open_question-67]: items open-brain:open_question:92675538b21e3608; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87781-87787
[^item-open_question-68]: items open-brain:open_question:4bcc49346a73602d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87745-87746
[^item-open_question-69]: items open-brain:open_question:dc36a7c89bedb6d5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87640-87645
[^item-open_question-70]: items open-brain:open_question:8515d83cb3e2136f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87640-87645
[^item-open_question-71]: items open-brain:open_question:8cac3ab8be4d7703; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87603-87611
[^item-open_question-72]: items open-brain:open_question:142993cbbcea7931; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87593-87601
[^item-open_question-73]: items open-brain:open_question:389b489c424f05b3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87581-87591
[^item-open_question-74]: items open-brain:open_question:98a77927d6d1c505; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87563-87569
[^item-open_question-75]: items open-brain:open_question:0e6110bacfe6bb30; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87552-87561
[^item-open_question-76]: items open-brain:open_question:f804271c8071c8ed; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87547-87550
[^item-open_question-77]: items open-brain:open_question:4ae03dfccb970f9f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87547-87550
[^item-open_question-78]: items open-brain:open_question:dc8e98f8e71eb0e5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87547-87550
[^item-open_question-79]: items open-brain:open_question:066584328c0ebaec; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87539-87543
[^item-open_question-80]: items open-brain:open_question:7dbfe85460c6f46f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 87539-87543
