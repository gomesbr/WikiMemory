---
title: "Cross-Project - Code Map"
page_id: "projects/cross-project/code-map"
domain: "cross-project"
bucket: "code-map"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:10:41.022983Z
source_count: 3
claim_count: 2
tags:
  - wikimemory
  - cross-project
  - cross-project
  - bucket
  - code-map
---
# Cross-Project - Code Map

Navigation: [[projects/cross-project/index|Cross-Project]] | [[projects/cross-project/communication-preferences|Cross-Project - Communication Preferences]] | [[projects/cross-project/workflow-rules|Cross-Project - Workflow Rules]] | [[projects/cross-project/architecture|Cross-Project - Architecture]] | [[projects/cross-project/current-state|Cross-Project - Current State]] | [[projects/cross-project/tasks|Cross-Project - Tasks]] | [[projects/cross-project/outcomes|Cross-Project - Outcomes]] | [[projects/cross-project/failures|Cross-Project - Failures]] | [[projects/cross-project/decisions|Cross-Project - Decisions]] | [[projects/cross-project/next-steps|Cross-Project - Next Steps]] | [[projects/cross-project/open-questions|Cross-Project - Open Questions]]
Related Domains: [[projects/ai-scientist/index|AI Scientist]], [[projects/ai-trader/index|AI Trader]], [[projects/open-brain/index|Open Brain]]

## Summary
- No synthesized summary yet.

## Code Location
- The code location section includes paths to various documentation files such as open_brain_runbook.md and runbook.md. [latent: codebase_map_abstractions] [confidence: strong][^claim-1]
- It lists persona documents like strategist.md and research.md as part of the CodexClaw project. [latent: project_identity_and_scope] [confidence: strong][^claim-2]

### Canonical Items
- - open_brain_runbook.md: CodexClaw/docs/operations/open_brain_runbook.md [confidence: explicit] [recurrence: 1][^item-code_location-1]
- - runbook.md: CodexClaw/docs/operations/runbook.md [confidence: explicit] [recurrence: 1][^item-code_location-2]
- - strategist.md: CodexClaw/personas/strategist.md [confidence: explicit] [recurrence: 1][^item-code_location-3]
- - research.md: CodexClaw/personas/research.md [confidence: explicit] [recurrence: 1][^item-code_location-4]
- + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetContentCommand [confidence: explicit] [recurrence: 1][^item-code_location-5]
- - prod-grok-backend.json: c:\Users\Fabio\AppData\Local\Temp\e2ddf759-eba7-489f-8946-d78e822532bd_6496f4fc-d714-437a-bcbc-a845241a02b7.zip.2bd\ttl\30d\export_data\0ddfd3a1-9485-4b4a-b5a8-ebd1be61b56b\prod-grok-backend.json [confidence: explicit] [recurrence: 1][^item-code_location-6]
- - `--config` default `config/refresh_config.json` [confidence: explicit] [recurrence: 1][^item-code_location-7]
- - `audits/refresh_notices.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-8]
- - `refresh` reads `state/source_registry.json` before and after discovery and derives `changed_source_ids` from any source with: [confidence: explicit] [recurrence: 1][^item-code_location-9]
- - `state/refresh_runs.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-10]
- - `state/refresh_state.json` [confidence: explicit] [recurrence: 1][^item-code_location-11]
- - `audits/wiki_notices.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-12]
- - `state/wiki_runs.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-13]
- - `state/wiki_state.json` [confidence: explicit] [recurrence: 1][^item-code_location-14]
- I’m fixing that and then adding a focused `test_wiki.py` file that exercises the full discovery→wiki path with mocked synthesis. [confidence: explicit] [recurrence: 1][^item-code_location-15]
- - `audits/extraction_notices.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-16]
- - `state/extraction_runs.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-17]
- - `state/extraction_state.json` [confidence: explicit] [recurrence: 1][^item-code_location-18]
- - Validation passed for the relevant scope: `python -m unittest tests.test_normalization tests.test_segmentation tests.test_classification -v` completed successfully. [confidence: explicit] [recurrence: 1][^item-code_location-19]
- - `audits/classification_notices.jsonl` for low-confidence / unclassified / conflicting cases [confidence: explicit] [recurrence: 1][^item-code_location-20]
- - `classified/sources/<source_id>/segments.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-21]
- - `classified/sources/<source_id>/stats.json` [confidence: explicit] [recurrence: 1][^item-code_location-22]
- - `state/classification_runs.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-23]
- - `state/segmentation_state.json` [confidence: explicit] [recurrence: 1][^item-code_location-24]
- - `state/segmentation_runs.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-25]
- `C:\Users\Fabio\.codex\sessions` [confidence: explicit] [recurrence: 1][^item-code_location-26]
- I’ll quickly verify current `/` response and local `dist/ui.js` contents from host and container match. [confidence: explicit] [recurrence: 1][^item-code_location-27]
- I’m resuming on the narrow path we already scoped: validate the latest `v2_experiments.ts` patch, then either keep the miner running or fix the next real bottleneck and rerun. [confidence: explicit] [recurrence: 1][^item-code_location-28]
- Implementing v1.9 in the scoped files only: `src/v2_types.ts`, `src/v2_ask.ts`, `src/v2_experiments.ts`, and `src/ui.ts`. [confidence: explicit] [recurrence: 1][^item-code_location-29]
- In `src/v2_ask.ts` and `src/v2_types.ts`: [confidence: explicit] [recurrence: 1][^item-code_location-30]
- (file: C:/Users/Fabio/.codex/skills/.system/skill-creator/SKILL.md) [confidence: explicit] [recurrence: 1][^item-code_location-31]
- (file: C:/Users/Fabio/.codex/skills/.system/skill-installer/SKILL.md) [confidence: explicit] [recurrence: 1][^item-code_location-32]
- A skill is a set of local instructions to follow that is stored in a `SKILL.md` file. [confidence: explicit] [recurrence: 1][^item-code_location-33]
- https://api.python.langchain.com/en/latest/langchain/retrievers/langchain.retrievers.parent_document_retriever.ParentDocumentRetriever.html [confidence: explicit] [recurrence: 1][^item-code_location-34]
- https://arxiv.org/abs/2104.08663 [confidence: explicit] [recurrence: 1][^item-code_location-35]
- https://arxiv.org/abs/2501.13956 [confidence: explicit] [recurrence: 1][^item-code_location-36]
- https://docs.ragas.io/en/v0.4.3/concepts/metrics/ [confidence: explicit] [recurrence: 1][^item-code_location-37]
- Add `src/structure_parser.ts` (deterministic parser + canonicalizer). [confidence: explicit] [recurrence: 1][^item-code_location-38]
- In `metadata_provider.ts`, if `content_kind=table`, skip strict model-only path and merge parser output + fallback metadata. [confidence: explicit] [recurrence: 1][^item-code_location-39]
- + CategoryInfo : ObjectNotFound: (C:\Users\Fabio\..._worker.err.log:String) [Get-Content], Ite [confidence: explicit] [recurrence: 1][^item-code_location-40]
- + CategoryInfo : ObjectNotFound: (C:\Users\Fabio\...ueue_worker.log:String) [Get-Content], Ite [confidence: explicit] [recurrence: 1][^item-code_location-41]
- + CategoryInfo : ObjectNotFound: (C:\Users\Fabio\...app_context.log:String) [Get-Content], ItemNotFoundException [confidence: explicit] [recurrence: 1][^item-code_location-42]
- I found a likely inconsistency in `docs/operations/runbook.md` around execution actions versus the new Phase 2 lane (`roll`/`adjust_stop`). [confidence: explicit] [recurrence: 1][^item-code_location-43]
- First I’ll inspect current `src/ui/server.ts` and `src/ui/skin.ts` structure, then patch shell/layout, add the new UI summary endpoints, and restyle all modules to the calm minimal system without breaking existing actions. [confidence: explicit] [recurrence: 1][^item-code_location-44]
- I also resolved the CodexClaw merge conflict before merging (in `src/db.ts`) and fixed a merge artifact in `src/config.ts` (duplicate `schedulerEnabled` key), then rebuilt successfully. [confidence: explicit] [recurrence: 1][^item-code_location-45]
- - Updated [daily_repo_sync.ps1](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/daily_repo_sync.ps1) [confidence: explicit] [recurrence: 1][^item-code_location-46]
- I’ll reopen `src/types.ts` raw and rewrite it cleanly in one pass so we keep type contracts consistent. [confidence: explicit] [recurrence: 1][^item-code_location-47]
- - open_brain_cutover.md: CodexClaw/docs/operations/open_brain_cutover.md [confidence: explicit] [recurrence: 1][^item-code_location-48]
- npm run import:whatsapp -- --input "D:\Fabio\Documents\AI\AI Brain\AI_Brain_Imports\whatsapp\whatsappdump.zip" --namespace personal.main --api-key "$key" [confidence: explicit] [recurrence: 1][^item-code_location-49]
- - 2026-03-03T01-26-46-737Z_8041307210_strategist.md: CodexClaw/store/reports/2026-03-03T01-26-46-737Z_8041307210_strategist.md [confidence: explicit] [recurrence: 1][^item-code_location-50]
- - HANDOFF_2026-03-02.md: CodexClaw/docs/HANDOFF_2026-03-02.md [confidence: explicit] [recurrence: 1][^item-code_location-51]
- - [openbrain.ts](\/c:/Users/Fabio/Cursor%20AI%20projects/Projects/AITrader/apps/approval_ui/src/openbrain.ts) [confidence: explicit] [recurrence: 1][^item-code_location-52]
- - `C:\Users\Fabio\Cursor AI projects\Projects\sync-logs\` [confidence: explicit] [recurrence: 1] [conflict][^item-code_location-53]
- - `lock_path = state/refresh.lock.json` [confidence: explicit] [recurrence: 1] [conflict][^item-code_location-54]
- - acquire `state/refresh.lock.json` before any phase [confidence: explicit] [recurrence: 1] [conflict][^item-code_location-55]
- - writes `classified/sources/<source_id>/segments.jsonl`, `classified/sources/<source_id>/stats.json`, `state/classification_state.json`, `state/classification_runs.jsonl`, and `audits/classification_notices.jsonl` [confidence: explicit] [recurrence: 1] [conflict][^item-code_location-56]
- - `state/classification_state.json` [confidence: explicit] [recurrence: 1] [conflict][^item-code_location-57]
- In `src/v2_experiments.ts`: [confidence: explicit] [recurrence: 1] [conflict][^item-code_location-58]
- I’m patching only the whole-corpus mining path in `src/v2_experiments.ts`. [confidence: explicit] [recurrence: 1] [conflict][^item-code_location-59]
- Get-Content : Cannot find path 'C:\Users\Fabio\Cursor AI projects\Projects\reembed_whatsapp_context.log' because it does not exist. [confidence: explicit] [recurrence: 1] [conflict][^item-code_location-60]

## Sources
[^claim-1]: items cross-project:code_location:5e757e8990aa8684, cross-project:code_location:91643a6197db1c2c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5607-5627; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5682-5688; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4973-4983; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11044-11061; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11115-11125
[^claim-2]: items cross-project:code_location:69c63c98d6895fc9, cross-project:code_location:c80f1b8c1a6f29eb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11044-11061; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11115-11125; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11126-11142; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11044-11061; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11115-11125; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11126-11142
[^item-code_location-1]: items cross-project:code_location:5e757e8990aa8684; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5607-5627; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5682-5688; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694
[^item-code_location-2]: items cross-project:code_location:91643a6197db1c2c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4973-4983; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11044-11061; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11115-11125
[^item-code_location-3]: items cross-project:code_location:69c63c98d6895fc9; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11044-11061; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11115-11125; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11126-11142
[^item-code_location-4]: items cross-project:code_location:c80f1b8c1a6f29eb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11044-11061; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11115-11125; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11126-11142
[^item-code_location-5]: items cross-project:code_location:a6525ef6f0ac019d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 12648-12664; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 16344-16358
[^item-code_location-6]: items cross-project:code_location:daded0f9d0f83394; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5607-5627; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5682-5688; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694
[^item-code_location-7]: items cross-project:code_location:254b04cc22c49f58; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192
[^item-code_location-8]: items cross-project:code_location:4ed8e63d033fb75d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-code_location-9]: items cross-project:code_location:86682338e4efe71f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-code_location-10]: items cross-project:code_location:10663f90e4db1027; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-code_location-11]: items cross-project:code_location:1ac0b20787bf6100; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-code_location-12]: items cross-project:code_location:37eb6cd467ea8167; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1593-1600; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1601-1605
[^item-code_location-13]: items cross-project:code_location:d51ebe4de739e677; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1593-1600; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1601-1605
[^item-code_location-14]: items cross-project:code_location:e5dbbe3eace00141; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1593-1600; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1601-1605
[^item-code_location-15]: items cross-project:code_location:84f7178ddc36c6af; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1552-1558
[^item-code_location-16]: items cross-project:code_location:ec5168978add80d0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1275-1280; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1281-1285
[^item-code_location-17]: items cross-project:code_location:36f8dbabe00d530e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1275-1280; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1281-1285
[^item-code_location-18]: items cross-project:code_location:7a04c66122af8115; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1275-1280; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1281-1285
[^item-code_location-19]: items cross-project:code_location:ea4112f3a17cc438; 019d837d-d249-71c3-9637-b8d6992ce805 lines 930-940; 019d837d-d249-71c3-9637-b8d6992ce805 lines 930-940; 019d837d-d249-71c3-9637-b8d6992ce805 lines 941-945
[^item-code_location-20]: items cross-project:code_location:2c7c9c76b6d2758d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-code_location-21]: items cross-project:code_location:bca5f51206431ed6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-code_location-22]: items cross-project:code_location:2951c44156e0ac4d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-code_location-23]: items cross-project:code_location:3fb1af7a67bed036; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-code_location-24]: items cross-project:code_location:e56473a31a39e1b6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 516-517; 019d837d-d249-71c3-9637-b8d6992ce805 lines 739-742
[^item-code_location-25]: items cross-project:code_location:83c74456a5c0e598; 019d837d-d249-71c3-9637-b8d6992ce805 lines 516-517
[^item-code_location-26]: items cross-project:code_location:204d87edab04d5d8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 489-494
[^item-code_location-27]: items cross-project:code_location:1b5429e249a0750a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 69359-69377
[^item-code_location-28]: items cross-project:code_location:d6a1e081a3e33dca; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 61232-61238
[^item-code_location-29]: items cross-project:code_location:5332c38feafbfe33; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57582-57588
[^item-code_location-30]: items cross-project:code_location:438d50336c140960; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57242-57249
[^item-code_location-31]: items cross-project:code_location:a6ed6e22c239d7eb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20910-20915
[^item-code_location-32]: items cross-project:code_location:d8c39ff74733f2be; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20910-20915
[^item-code_location-33]: items cross-project:code_location:83d54b094551d701; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20910-20915; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20910-20915; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20910-20915
[^item-code_location-34]: items cross-project:code_location:1b4f4a8439c6fbda; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20902-20909
[^item-code_location-35]: items cross-project:code_location:9ad7118c4dedbf01; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20902-20909
[^item-code_location-36]: items cross-project:code_location:6405b40263ce01b6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20902-20909
[^item-code_location-37]: items cross-project:code_location:df02548e91efcfd4; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20902-20909
[^item-code_location-38]: items cross-project:code_location:4ef6a3921c6fe72a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 17481-17487
[^item-code_location-39]: items cross-project:code_location:56b9d0a42a14dda0; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 17481-17487
[^item-code_location-40]: items cross-project:code_location:81d0cc11d4092e36; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 16344-16358
[^item-code_location-41]: items cross-project:code_location:5ffd00ac046aeb9e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 16344-16358
[^item-code_location-42]: items cross-project:code_location:ff2f64f2ba3c1285; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 12648-12664
[^item-code_location-43]: items cross-project:code_location:d945ffe2c4290b84; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 3267-3279
[^item-code_location-44]: items cross-project:code_location:93a6cb136c7f72b6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 9346-9357; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 10608-10609
[^item-code_location-45]: items cross-project:code_location:e994e7b931ef707b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 10436-10461
[^item-code_location-46]: items cross-project:code_location:e1ef761e983f00fe; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 10126-10152; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 10208-10225
[^item-code_location-47]: items cross-project:code_location:1d9fa8c8e17c821c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5787-5797
[^item-code_location-48]: items cross-project:code_location:ae123493369c03be; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5607-5627; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5682-5688; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5694-5694
[^item-code_location-49]: items cross-project:code_location:c48ab18af31f3227; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5441-5451
[^item-code_location-50]: items cross-project:code_location:0b2c4da1e45510a3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4973-4983
[^item-code_location-51]: items cross-project:code_location:058580cf60ed97d3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4973-4983
[^item-code_location-52]: items cross-project:code_location:3f3b4011c39c10e0; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4968-4968; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4969-4972
[^item-code_location-53]: items cross-project:code_location:cc1a8819596b5bd9; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 10126-10152; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 12648-12664; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 12648-12664
[^item-code_location-54]: items cross-project:code_location:62e324b41d571546; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192
[^item-code_location-55]: items cross-project:code_location:25998cf21416e34a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3186-3189; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3192-3192; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3193-3194
[^item-code_location-56]: items cross-project:code_location:33d4eeafa10ffbc8; 019d837d-d249-71c3-9637-b8d6992ce805 lines 930-940; 019d837d-d249-71c3-9637-b8d6992ce805 lines 941-945
[^item-code_location-57]: items cross-project:code_location:82ae0783956f4f29; 019d837d-d249-71c3-9637-b8d6992ce805 lines 762-762; 019d837d-d249-71c3-9637-b8d6992ce805 lines 763-766
[^item-code_location-58]: items cross-project:code_location:01e414c9abc7193b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57242-57249; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57242-57249; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 60945-60951
[^item-code_location-59]: items cross-project:code_location:84b41d873dba3c88; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 59182-59194; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 60526-60532; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 60629-60635
[^item-code_location-60]: items cross-project:code_location:a2ed6c83484e42d4; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 12648-12664
