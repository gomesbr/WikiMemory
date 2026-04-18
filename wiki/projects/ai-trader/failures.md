---
title: "AI Trader - Failures"
page_id: "projects/ai-trader/failures"
domain: "ai-trader"
bucket: "failures"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:07:37.633520Z
source_count: 74
claim_count: 7
tags:
  - wikimemory
  - project
  - ai-trader
  - bucket
  - failures
---
# AI Trader - Failures

Navigation: [[projects/ai-trader/index|AI Trader]] | [[projects/ai-trader/communication-preferences|AI Trader - Communication Preferences]] | [[projects/ai-trader/workflow-rules|AI Trader - Workflow Rules]] | [[projects/ai-trader/architecture|AI Trader - Architecture]] | [[projects/ai-trader/code-map|AI Trader - Code Map]] | [[projects/ai-trader/current-state|AI Trader - Current State]] | [[projects/ai-trader/tasks|AI Trader - Tasks]] | [[projects/ai-trader/outcomes|AI Trader - Outcomes]] | [[projects/ai-trader/decisions|AI Trader - Decisions]] | [[projects/ai-trader/next-steps|AI Trader - Next Steps]] | [[projects/ai-trader/open-questions|AI Trader - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- If a skill can't be applied cleanly, state the issue, pick the next-best approach, and continue. [latent: implicit_dos_and_donts] [confidence: strong][^claim-1]
- If something fails, report root cause, fix rationale, and evidence that the failure cannot recur via the same path. [latent: implicit_dos_and_donts] [confidence: strong][^claim-2]
- Use first-principles debugging: identify root cause and implement durable fixes with regression coverage instead of quick local patches. [latent: implicit_dos_and_donts] [confidence: strong][^claim-3]
- Define the failure precisely. [latent: implicit_dos_and_donts] [confidence: strong][^claim-4]

## Failure
- Use this doctrine whenever addressing failures, instability, or repeated operational friction. [latent: implicit_dos_and_donts] [confidence: strong][^claim-5]
- Do not ask user to "grant access" for those paths unless a command has already failed with a concrete filesystem/permission error. [latent: implicit_dos_and_donts] [confidence: strong][^claim-6]
- Do not claim filesystem/policy/approval blockers unless you include exact command + error evidence from this run. [latent: implicit_dos_and_donts] [confidence: strong][^claim-7]

### Canonical Items
- - Safety and fallback: If a skill can't be applied cleanly (missing files, unclear instructions), state the issue, pick the next-best approach, and continue. [confidence: strong] [status: historical] [recurrence: 61][^item-failure-1]
- - If something fails, report root cause, fix rationale, and evidence that the failure cannot recur via the same path. [confidence: strong] [status: historical] [recurrence: 17][^item-failure-2]
- - Use first-principles debugging: identify root cause and implement durable fixes with regression coverage instead of quick local patches. [confidence: strong] [status: historical] [recurrence: 17][^item-failure-3]
- Define the failure precisely: [confidence: strong] [status: historical] [recurrence: 17][^item-failure-4]
- Failure Playbook [confidence: strong] [status: historical] [recurrence: 17][^item-failure-5]
- Use this doctrine whenever addressing failures, instability, or repeated operational friction. [confidence: strong] [status: historical] [recurrence: 17][^item-failure-6]
- - Test/build failures not caused by this change. [confidence: strong] [status: historical] [recurrence: 10][^item-failure-7]
- do not ask user to "grant access" for those paths unless a command has already failed with a concrete filesystem/permission error. [confidence: strong] [status: historical] [recurrence: 8][^item-failure-8]
- error [confidence: strong] [status: historical] [recurrence: 6][^item-failure-9]
- - Do not claim filesystem/policy/approval blockers unless you include exact command + error evidence from this run. [confidence: strong] [status: historical] [recurrence: 6][^item-failure-10]
- - Escalate: missing access/tool/runtime blockers with exact error and minimum fix. [confidence: strong] [status: historical] [recurrence: 3][^item-failure-11]
- failed [confidence: strong] [status: historical] [recurrence: 2][^item-failure-12]
- {"pass":true|false,"confidence":"high|medium|low","issues":["..."],"requiredFixes":["..."],"approvedSummary":"..."} [confidence: strong] [status: historical] [recurrence: 2][^item-failure-13]
- error_text [confidence: strong] [status: historical] [recurrence: 2][^item-failure-14]
- apply_patch failed with 'writing outside of the project [confidence: strong] [status: historical] [recurrence: 2][^item-failure-15]
- debug [confidence: strong] [status: historical] [recurrence: 2][^item-failure-16]
- - [2026-02-28T23:19:23.834Z] (user) Ah, the issue is because the folder ‘cursor ai projects’ have spaces in the name. [confidence: strong] [status: historical] [recurrence: 2][^item-failure-17]
- I’m starting the real full-corpus load now and I’ll handle it phase by phase, fixing only root-cause issues if they show up and stopping only on completion or the 10GB derived-data cap. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-18]
- - fix real issues when they appeared [confidence: strong] [status: historical] [recurrence: 1][^item-failure-19]
- - I fixed that by making the failure metric **corpus-based and stable across reruns** [confidence: strong] [status: historical] [recurrence: 1][^item-failure-20]
- - Issues I hit while implementing: [confidence: strong] [status: historical] [recurrence: 1][^item-failure-21]
- - the repeated-failure stop test initially failed because the full-load gate trusted the latest incremental report too much [confidence: strong] [status: historical] [recurrence: 1][^item-failure-22]
- - The new runner executes phases `discover -> normalize -> segment -> classify -> extract -> wiki -> bootstrap -> audit`, measures derived-disk growth after every phase, enforces the `10 GB` cap, writes machine-readable issue bundles, and stops on repair-ne... [confidence: strong] [status: historical] [recurrence: 1][^item-failure-23]
- I found the second gap in the retry logic: the first-run metric was inflated by mixing live run notices with persisted stats, so the second identical failure looked like an “improvement.” I’m making the metric fully corpus-based. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-24]
- They’ll cover the happy path, a real gate failure, the derived-space stop, and the repeated non-improving stop without needing the real corpus. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-25]
- I’m running the fixed real-data sample suite now to verify the pointer-first migration and the last audit errors on live traces. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-26]
- I’ve isolated the failures to orchestration logic, not the lower phases. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-27]
- - It supports scoped reruns by `--source-id`, atomic snapshot replacement, and nonzero exit only when `error` findings exist [confidence: strong] [status: historical] [recurrence: 1][^item-failure-28]
- I found one state-snapshot issue while reviewing the new module: full audit runs should replace prior target state, not carry stale keys forward. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-29]
- - `error` if two or more `active` items with `confidence in {explicit,strong}` conflict in the same domain/subject [confidence: strong] [status: historical] [recurrence: 1][^item-failure-30]
- - `info` severity exists in the schema but v1 mainly emits `warning` and `error`. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-31]
- - `severity = info | warning | error` [confidence: strong] [status: historical] [recurrence: 1][^item-failure-32]
- - any error finding -> nonzero exit [confidence: strong] [status: historical] [recurrence: 1][^item-failure-33]
- - bootstrap bullet missing `supporting_item_keys`, unresolved `supporting_claim_ids`, or references to unknown current inputs -> `error` [confidence: strong] [status: historical] [recurrence: 1][^item-failure-34]
- - bootstrap bullet references removed wiki claim id -> `error` [confidence: strong] [status: historical] [recurrence: 1][^item-failure-35]
- - bootstrap bullet with unknown supporting claim id -> error [confidence: strong] [status: historical] [recurrence: 1][^item-failure-36]
- - bootstrap includes claim whose supporting items no longer exist -> error [confidence: strong] [status: historical] [recurrence: 1][^item-failure-37]
- - bootstrap includes wiki claim whose supporting extracted items no longer all exist -> `error` [confidence: strong] [status: historical] [recurrence: 1][^item-failure-38]
- - every `error` finding must correspond to a concrete broken reference, missing provenance, or hard contradiction [confidence: strong] [status: historical] [recurrence: 1][^item-failure-39]
- - Exit behavior is gateable: warnings still succeed, but any `error` finding makes the command return nonzero. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-40]
- - extracted item missing `provenance_refs` -> `error` [confidence: strong] [status: historical] [recurrence: 1][^item-failure-41]
- - extracted item with empty provenance -> error [confidence: strong] [status: historical] [recurrence: 1][^item-failure-42]
- - failed run preserves last committed audit snapshot [confidence: strong] [status: historical] [recurrence: 1][^item-failure-43]
- - superseded older temporal item should not produce a contradiction error [confidence: strong] [status: historical] [recurrence: 1][^item-failure-44]
- - wiki claim missing `supporting_item_ids` or unresolved provenance in manifest -> `error` [confidence: strong] [status: historical] [recurrence: 1][^item-failure-45]
- - wiki claim with unknown supporting item id -> error [confidence: strong] [status: historical] [recurrence: 1][^item-failure-46]
- - no `error` audits on sample [confidence: strong] [status: historical] [recurrence: 1][^item-failure-47]
- - severity buckets: `info | warning | error` [confidence: strong] [status: historical] [recurrence: 1][^item-failure-48]
- The real issue is `skipped_weak_inference` volume from instruction-heavy text, not classification anymore. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-49]
- I’ve isolated the likely failure mode to the last-mile context inheritance on the persisted sample. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-50]
- I’m debugging that override path directly instead of guessing, because those last seven should be mechanically explainable. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-51]
- I’ve pinpointed the extractor’s broader failure mode: it’s mining raw tool outputs and reasoning traces as if they were stable knowledge. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-52]
- The classification change is structural rather than just a keyword tweak: it will preserve project intent through low-signal reasoning/tool segments, which is the broader failure mode the live sample exposed. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-53]
- I’m locking in regression coverage for the exact failure mode I’m fixing: `AITrader`/finance-plan traces that fragment across neighboring segments, plus code-location false positives from prose like `e.g.`. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-54]
- The deeper issue isn’t just missing keywords. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-55]
- - The BOM fix generalizes a real Windows failure mode instead of leaving it as a temp-script workaround. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-56]
- I’m doing one last direct smoke check with a BOM-encoded config file so we know the exact real Windows failure I hit is actually resolved, not just theoretically patched. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-57]
- I’m rerunning the full suite once so we keep the repo stable, then I’ll summarize the real-data findings separately from the code fix, because the live sample exposed some quality issues we shouldn’t blur together. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-58]
- That way the real issue we hit is fixed at the right layer for all config/state JSON readers, not papered over in one temporary script. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-59]
- The real-data run surfaced one concrete engineering issue worth fixing immediately: config JSON with a Windows BOM can break the pipeline even though the content is valid. [confidence: strong] [status: historical] [recurrence: 1][^item-failure-60]

## Sources
[^claim-1]: items ai-trader:failure:76e5e17677e712b8; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-2]: items ai-trader:failure:a76937d9d8b94f87; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-3]: items ai-trader:failure:ededa0e1faee62c8; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-4]: items ai-trader:failure:5bb61cdc048083ce; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-5]: items ai-trader:failure:8db9a768aa0881c4; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-6]: items ai-trader:failure:e3d2716ff513d19e; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 5-5; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 6-8; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 16-16
[^claim-7]: items ai-trader:failure:8df64abb07b96d09; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 206-206; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 207-209; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 288-288
[^item-failure-1]: items ai-trader:failure:76e5e17677e712b8; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-failure-2]: items ai-trader:failure:a76937d9d8b94f87; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-failure-3]: items ai-trader:failure:ededa0e1faee62c8; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-failure-4]: items ai-trader:failure:5bb61cdc048083ce; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-failure-5]: items ai-trader:failure:3d2140abbf5fd24d; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-failure-6]: items ai-trader:failure:8db9a768aa0881c4; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-failure-7]: items ai-trader:failure:8d8a7022f189c5ed; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-failure-8]: items ai-trader:failure:e3d2716ff513d19e; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 5-5; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 6-8; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 16-16
[^item-failure-9]: items ai-trader:failure:2698ffb8e53f01a1; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 6288-6296; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 9520-9526; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 11300-11312
[^item-failure-10]: items ai-trader:failure:8df64abb07b96d09; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 206-206; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 207-209; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 288-288
[^item-failure-11]: items ai-trader:failure:08a087ed03ca9814; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 5-5; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 6-9; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 1058-1058
[^item-failure-12]: items ai-trader:failure:83d10efbd9f0cf34; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 9866-9875; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 13541-13548; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11686-11700
[^item-failure-13]: items ai-trader:failure:c225cad7d205bf19; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 5-5; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 6-8; 019caf95-fa0a-7900-9097-6dbda1513ef0 lines 16-16
[^item-failure-14]: items ai-trader:failure:2f7e99e3871e9b6c; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 13703-13710; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 13925-13932; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 10348-10348
[^item-failure-15]: items ai-trader:failure:0f8c02a4fa62fd45; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 213-213; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 214-217; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 206-206
[^item-failure-16]: items ai-trader:failure:54bd1bbbc68814f0; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 4884-4890; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 235-247
[^item-failure-17]: items ai-trader:failure:9aa48595c0e77ab4; 019ca705-c215-7221-8e6a-d28b922add82 lines 88-88; 019ca705-c215-7221-8e6a-d28b922add82 lines 89-92; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 5-5
[^item-failure-18]: items ai-trader:failure:fee8dcd0be9077ea; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4524-4540
[^item-failure-19]: items ai-trader:failure:64384a00234ee335; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4511-4519
[^item-failure-20]: items ai-trader:failure:44dd415094027db3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4505-4505; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4506-4510
[^item-failure-21]: items ai-trader:failure:629504bf30404b53; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4505-4505; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4506-4510
[^item-failure-22]: items ai-trader:failure:03e7dabc337ad927; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4505-4505; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4506-4510
[^item-failure-23]: items ai-trader:failure:9bd6274afa3d845a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4462-4467
[^item-failure-24]: items ai-trader:failure:b5f6fab699c3819c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4435-4449
[^item-failure-25]: items ai-trader:failure:e74fbaa80b43cdcc; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4404-4405
[^item-failure-26]: items ai-trader:failure:f8e4533610b71dd1; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4189-4201
[^item-failure-27]: items ai-trader:failure:d2b4aeab44721da6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3337-3347
[^item-failure-28]: items ai-trader:failure:83073df78724c767; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3132-3137
[^item-failure-29]: items ai-trader:failure:30368c218e162ce6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3083-3094
[^item-failure-30]: items ai-trader:failure:7d1e8ba9ff5a8184; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-31]: items ai-trader:failure:08e2893b75840ac3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-32]: items ai-trader:failure:b8dc9f364f3cfebe; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-33]: items ai-trader:failure:02afd522b99ef887; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-34]: items ai-trader:failure:ed6716a8db92d66f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-35]: items ai-trader:failure:bf457ff2f23f1e97; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-36]: items ai-trader:failure:f1175f7023623b53; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-37]: items ai-trader:failure:a82b05e46b68fbbb; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-38]: items ai-trader:failure:a2b95d0567464a9c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-39]: items ai-trader:failure:107751b4d61ea681; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-40]: items ai-trader:failure:cba9d78aa521a3ad; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-41]: items ai-trader:failure:f7530100e18c3c7b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-42]: items ai-trader:failure:0fccc3a0cf69f29a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-43]: items ai-trader:failure:15336d2218baf11d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-44]: items ai-trader:failure:10a15a974f98f1f9; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-45]: items ai-trader:failure:3211974d42f9257f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-46]: items ai-trader:failure:271aab058f8bffd3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2953-2956; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2960-2960; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2961-2962
[^item-failure-47]: items ai-trader:failure:2e22dfbafd911eea; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2922-2926
[^item-failure-48]: items ai-trader:failure:81533a3ca9f9eadf; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2922-2926
[^item-failure-49]: items ai-trader:failure:8d00a5e2dced2b99; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2494-2502
[^item-failure-50]: items ai-trader:failure:89c2d327ce8cb35a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2120-2128
[^item-failure-51]: items ai-trader:failure:c8c211ae5f5cc938; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2065-2070
[^item-failure-52]: items ai-trader:failure:0cb0015f596bf013; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2024-2034
[^item-failure-53]: items ai-trader:failure:560f13dbed23db18; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1904-1913
[^item-failure-54]: items ai-trader:failure:e502a5af7882b23c; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1894-1902
[^item-failure-55]: items ai-trader:failure:b4a20c4086072ef2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1858-1863
[^item-failure-56]: items ai-trader:failure:9d0713419a47ed4e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1824-1824; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1825-1828
[^item-failure-57]: items ai-trader:failure:5e20aeb842ff6d60; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1817-1823
[^item-failure-58]: items ai-trader:failure:2fb7d11804f24a0b; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1810-1815
[^item-failure-59]: items ai-trader:failure:3cdbd93d3b8ccb21; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1803-1808
[^item-failure-60]: items ai-trader:failure:2e52837849dd8f17; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1777-1785
