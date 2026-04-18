---
title: "Open Brain - Code Map"
page_id: "projects/open-brain/code-map"
domain: "open-brain"
bucket: "code-map"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:08:35.480905Z
source_count: 4
claim_count: 3
tags:
  - wikimemory
  - project
  - open-brain
  - bucket
  - code-map
---
# Open Brain - Code Map

Navigation: [[projects/open-brain/index|Open Brain]] | [[projects/open-brain/communication-preferences|Open Brain - Communication Preferences]] | [[projects/open-brain/workflow-rules|Open Brain - Workflow Rules]] | [[projects/open-brain/architecture|Open Brain - Architecture]] | [[projects/open-brain/current-state|Open Brain - Current State]] | [[projects/open-brain/tasks|Open Brain - Tasks]] | [[projects/open-brain/outcomes|Open Brain - Outcomes]] | [[projects/open-brain/failures|Open Brain - Failures]] | [[projects/open-brain/decisions|Open Brain - Decisions]] | [[projects/open-brain/next-steps|Open Brain - Next Steps]] | [[projects/open-brain/open-questions|Open Brain - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- The project utilizes a skill system defined in SKILL.md files. [latent: project_identity_and_scope] [confidence: strong][^claim-1]
- Active files and logs are maintained for tracking the project's development. [latent: current_state_synthesis] [confidence: strong][^claim-2]
- The project includes modules for real-data case generation and strategy execution. [latent: architecture_synthesis] [confidence: strong][^claim-3]

## Code Location
- No synthesized section summary yet.

### Canonical Items
- - loop_2efee43d-c2a8-48a6-aeb4-cb947357c6ac.log: OpenBrain/generated/strategy_program/loop_2efee43d-c2a8-48a6-aeb4-cb947357c6ac.log [confidence: explicit] [recurrence: 2][^item-code_location-1]
- - sms_state_2efee43d-c2a8-48a6-aeb4-cb947357c6ac.json: OpenBrain/generated/strategy_program/sms_state_2efee43d-c2a8-48a6-aeb4-cb947357c6ac.json [confidence: explicit] [recurrence: 2][^item-code_location-2]
- - `OpenBrain/README.md` [confidence: explicit] [recurrence: 2][^item-code_location-3]
- - prod-grok-backend.json: c:\Users\Fabio\AppData\Local\Temp\e2ddf759-eba7-489f-8946-d78e822532bd_6496f4fc-d714-437a-bcbc-a845241a02b7.zip.2bd\ttl\30d\export_data\0ddfd3a1-9485-4b4a-b5a8-ebd1be61b56b\prod-grok-backend.json [confidence: explicit] [recurrence: 2][^item-code_location-4]
- - Loop log: `OpenBrain/generated/strategy_program/loop_b922379a-73be-44a8-891e-d635c9ed1ab0.log` [confidence: explicit] [recurrence: 2][^item-code_location-5]
- - [src/v2_types.ts](c:/Users/Fabio/Cursor AI projects/Projects/OpenBrain/src/v2_types.ts) [confidence: explicit] [recurrence: 1][^item-code_location-6]
- ## Active file: OpenBrain/generated/chat_transcripts/openbrain_chat_transcript_2026-03-02_to_2026-03-08_utf8.md [confidence: explicit] [recurrence: 1][^item-code_location-7]
- I’m now adding the new experiment engine module (`v2_experiments.ts`) with real-data case generation, strategy catalog execution, per-case scoring/failure buckets, leaderboard, and winner decisioning. [confidence: explicit] [recurrence: 1][^item-code_location-8]
- - [src/ui.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/ui.ts) [confidence: explicit] [recurrence: 1][^item-code_location-9]
- (file: C:/Users/Fabio/.codex/skills/.system/skill-creator/SKILL.md) [confidence: explicit] [recurrence: 1][^item-code_location-10]
- (file: C:/Users/Fabio/.codex/skills/.system/skill-installer/SKILL.md) [confidence: explicit] [recurrence: 1][^item-code_location-11]
- A skill is a set of local instructions to follow that is stored in a `SKILL.md` file. [confidence: explicit] [recurrence: 1][^item-code_location-12]
- - `src/server.ts` (REST API) [confidence: explicit] [recurrence: 1][^item-code_location-13]
- - dq_audit_latest.json: OpenBrain/generated/dq_audit_latest.json [confidence: explicit] [recurrence: 1][^item-code_location-14]
- - [package.json](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/package.json) [confidence: explicit] [recurrence: 1][^item-code_location-15]
- - `CodexClaw/docs/operations/open_brain_runbook.md` [confidence: explicit] [recurrence: 1][^item-code_location-16]
- - runbook.md: CodexClaw/docs/operations/runbook.md [confidence: explicit] [recurrence: 1][^item-code_location-17]
- - [src/config.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/config.ts) [confidence: explicit] [recurrence: 1][^item-code_location-18]
- npm run v2:bench:signal -- --mode=profile --set=signal_140 --chat=personal.main --min-score=0.28 --min-rows=20 [confidence: explicit] [recurrence: 1][^item-code_location-19]
- - metadata_provider.ts: OpenBrain/src/metadata_provider.ts [confidence: explicit] [recurrence: 1][^item-code_location-20]
- - Agent mesh dispatcher (controller/specialists/adjudicator flow) in [v2_mesh.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/v2_mesh.ts:181). [confidence: explicit] [recurrence: 1][^item-code_location-21]
- - V2 ask loop with bounded refinement, sufficiency/contradiction checks, answer contract, evidence linking in [v2_ask.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/v2_ask.ts:150). [confidence: explicit] [recurrence: 1][^item-code_location-22]
- https://arxiv.org/abs/2104.08663 [confidence: explicit] [recurrence: 1][^item-code_location-23]
- - REST API in [server.ts](\/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/server.ts) [confidence: explicit] [recurrence: 1][^item-code_location-24]
- - DB + dedupe + vector search in [db.ts](\/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/db.ts) [confidence: explicit] [recurrence: 1][^item-code_location-25]
- - __init__.py: WikiMemory/wikimemory/__init__.py [confidence: explicit] [recurrence: 1][^item-code_location-26]
- - __main__.py: WikiMemory/wikimemory/__main__.py [confidence: explicit] [recurrence: 1][^item-code_location-27]
- - pyproject.toml: WikiMemory/pyproject.toml [confidence: explicit] [recurrence: 1][^item-code_location-28]
- - Updated [.gitignore](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/.gitignore) and [README.md](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/WikiMemory/README.md) for the new `segmented/` artifacts and command. [confidence: explicit] [recurrence: 1][^item-code_location-29]
- - Added [tests/test_normalization.py](</c:/Users/Fabio/Cursor AI projects/Projects/WikiMemory/tests/test_normalization.py>) covering: [confidence: explicit] [recurrence: 1][^item-code_location-30]
- - cli.py: WikiMemory/wikimemory/cli.py [confidence: explicit] [recurrence: 1][^item-code_location-31]
- - Added a new backend network layer in [src/v2_network.ts](C:\Users\Fabio\Cursor AI projects\Projects\OpenBrain\src\v2_network.ts). [confidence: explicit] [recurrence: 1][^item-code_location-32]
- - [generated/strategy_program/whole_corpus_family_backfill_runner.ts](C:\Users\Fabio\Cursor AI projects\Projects\OpenBrain\generated\strategy_program\whole_corpus_family_backfill_runner.ts) [confidence: explicit] [recurrence: 1][^item-code_location-33]
- - `sql/001_init.sql` [confidence: explicit] [recurrence: 1][^item-code_location-34]
- - CPU guard log: `generated/strategy_program/cpu_guard.log` [confidence: explicit] [recurrence: 1][^item-code_location-35]
- I confirmed there’s no persistent `AGENTS.md` in `OpenBrain`, so I’m adding one now with a hard rule: solve classes of problems generically (intent -> subqueries -> evidence sufficiency), never ad-hoc single-question hints. [confidence: explicit] [recurrence: 1][^item-code_location-36]
- - [src/session.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/session.ts) [confidence: explicit] [recurrence: 1][^item-code_location-37]
- - [whole_corpus_family_backfill_cursor.json](c:\Users\Fabio\Cursor%20AI%20projects\Projects\OpenBrain\generated\strategy_program\whole_corpus_family_backfill_cursor.json) [confidence: explicit] [recurrence: 1][^item-code_location-38]
- - openbrain_chat_transcript_2026-03-08_to_2026-03-14_utf8.md: OpenBrain/generated/chat_transcripts/openbrain_chat_transcript_2026-03-08_to_2026-03-14_utf8.md [confidence: explicit] [recurrence: 1][^item-code_location-39]
- - [ui.ts](c:\Users\Fabio\Cursor%20AI%20projects\Projects\OpenBrain\src\ui.ts) [confidence: explicit] [recurrence: 1][^item-code_location-40]
- - low_confidence_actor_pronouns.csv: OpenBrain/generated/actor_pronoun_review/low_confidence_actor_pronouns.csv [confidence: explicit] [recurrence: 1][^item-code_location-41]
- - RAGChecker (fine-grained diagnostic metrics): https://arxiv.org/abs/2408.08067 [confidence: explicit] [recurrence: 1][^item-code_location-42]
- I’m rewiring `server.ts` in one pass: route segmentation (API-key memory endpoints vs session-auth brain endpoints), login/logout/session, privacy mode endpoints, brain query/profile/graph/timeline/insights/jobs APIs, plus app HTML serving and worker/migrat... [confidence: explicit] [recurrence: 1][^item-code_location-43]
- `generated/test_candidates/type_domain_found_dbsignals_v2.csv` [confidence: explicit] [recurrence: 1][^item-code_location-44]
- I fixed it in [v2_experiments.ts](c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/v2_experiments.ts): [confidence: explicit] [recurrence: 1][^item-code_location-45]
- - CRAG paper: https://arxiv.org/abs/2401.15884 [confidence: explicit] [recurrence: 1][^item-code_location-46]
- - HyDE paper: https://arxiv.org/abs/2212.10496 [confidence: explicit] [recurrence: 1][^item-code_location-47]
- - [v2_types.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/v2_types.ts) [confidence: explicit] [recurrence: 1][^item-code_location-48]
- - type_domain_found_dbsignals.csv: OpenBrain/generated/test_candidates/type_domain_found_dbsignals.csv [confidence: explicit] [recurrence: 1][^item-code_location-49]
- - type_domain_found_dbsignals_v2.csv: OpenBrain/generated/test_candidates/type_domain_found_dbsignals_v2.csv [confidence: explicit] [recurrence: 1][^item-code_location-50]
- - type_domain_missing_dbsignals_v2.csv: OpenBrain/generated/test_candidates/type_domain_missing_dbsignals_v2.csv [confidence: explicit] [recurrence: 1][^item-code_location-51]
- - type_domain_matrix_dbsignals.csv: OpenBrain/generated/test_candidates/type_domain_matrix_dbsignals.csv [confidence: explicit] [recurrence: 1][^item-code_location-52]
- - [package.json](c:/Users/Fabio/Cursor AI projects/Projects/OpenBrain/package.json) [confidence: explicit] [recurrence: 1][^item-code_location-53]
- - [actor_suspicious.csv](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/generated/actor_review/actor_suspicious.csv) [confidence: explicit] [recurrence: 1][^item-code_location-54]
- - Universal quality evaluate/adjudicate/metrics/bootstrap in [v2_quality.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/v2_quality.ts:82). [confidence: explicit] [recurrence: 1][^item-code_location-55]
- - [ui.ts](c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/ui.ts) [confidence: explicit] [recurrence: 1][^item-code_location-56]
- - Docs in [README.md](\/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/README.md) [confidence: explicit] [recurrence: 1][^item-code_location-57]
- - New V2 schema/tables (canonical/silver, candidates, quarantine, quality ledger, answer traceability, benchmark, service auth/audit) in [schema.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/schema.ts:225). [confidence: explicit] [recurrence: 1][^item-code_location-58]
- - Published fact/graph search endpoints in [v2_search.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/v2_search.ts:3). [confidence: explicit] [recurrence: 1][^item-code_location-59]
- - Shared TS SDK for other projects/agents in [sdk.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/OpenBrain/src/sdk.ts:35). [confidence: explicit] [recurrence: 1][^item-code_location-60]

## Sources
[^claim-1]: items open-brain:code_location:a6ed6e22c239d7eb, open-brain:code_location:d8c39ff74733f2be, open-brain:code_location:83d54b094551d701; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5452-5453; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6794-6795; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5452-5453; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6794-6795; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5452-5453; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5452-5453; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5452-5453
[^claim-2]: items open-brain:code_location:7af6834d76468263, open-brain:code_location:71c8030c83edac1f; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 19624-19635; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 27539-27545; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 28657-28661; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 30995-30995; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 30995-30995; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 30996-30999
[^claim-3]: items open-brain:code_location:d6a1e081a3e33dca; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26891-26894; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 37377-37383; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 37681-37689
[^item-code_location-1]: items open-brain:code_location:af8cb931889cd951; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 19624-19635; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 29414-29418; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 29552-29556
[^item-code_location-2]: items open-brain:code_location:cef2a1f9a4bb06fa; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 19624-19635; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 29414-29418; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 29552-29556
[^item-code_location-3]: items open-brain:code_location:d060ec75a30f0654; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3842-3845; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3847-3847; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3848-3850
[^item-code_location-4]: items open-brain:code_location:daded0f9d0f83394; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5090-5102; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5173-5181; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5182-5194
[^item-code_location-5]: items open-brain:code_location:7af6834d76468263; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 19624-19635; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 27539-27545; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 28657-28661
[^item-code_location-6]: items open-brain:code_location:0be20f4588875dcc; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 27443-27443; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 27444-27447; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 32670-32670
[^item-code_location-7]: items open-brain:code_location:71c8030c83edac1f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 30995-30995; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 30995-30995; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 30996-30999
[^item-code_location-8]: items open-brain:code_location:d6a1e081a3e33dca; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26891-26894; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 37377-37383; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 37681-37689
[^item-code_location-9]: items open-brain:code_location:c34fc78a1fd196dd; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6259-6275; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6276-6279; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 7271-7280
[^item-code_location-10]: items open-brain:code_location:a6ed6e22c239d7eb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5452-5453; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6794-6795; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711
[^item-code_location-11]: items open-brain:code_location:d8c39ff74733f2be; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5452-5453; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6794-6795; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43710-43711
[^item-code_location-12]: items open-brain:code_location:83d54b094551d701; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5452-5453; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5452-5453; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5452-5453
[^item-code_location-13]: items open-brain:code_location:fd5f8efbf5952ac2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3842-3845; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3847-3847; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3848-3850
[^item-code_location-14]: items open-brain:code_location:518025d66a5b7b22; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22747-22751; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22769-22773; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22869-22873
[^item-code_location-15]: items open-brain:code_location:fe62bdda4acec25f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6259-6275; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6276-6279; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11970-11993
[^item-code_location-16]: items open-brain:code_location:5e757e8990aa8684; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3842-3845; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3847-3847; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3848-3850
[^item-code_location-17]: items open-brain:code_location:91643a6197db1c2c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3455-3464; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3652-3669; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3724-3737
[^item-code_location-18]: items open-brain:code_location:2df97dc3c977c70b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6259-6275; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6276-6279; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 10366-10381
[^item-code_location-19]: items open-brain:code_location:9847b24b55490e78; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 15169-15169; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 15170-15173; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 18146-18155
[^item-code_location-20]: items open-brain:code_location:dd8c05baf70d3f1d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 39179-39181; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 39203-39206; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 39246-39247
[^item-code_location-21]: items open-brain:code_location:49efcfead49c5f4a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14196-14196; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14197-14200; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 19709-19715
[^item-code_location-22]: items open-brain:code_location:25f9d5f0ad3ef4d8; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14196-14196; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14197-14200; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 19709-19715
[^item-code_location-23]: items open-brain:code_location:9ad7118c4dedbf01; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20901-20901; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31340-31340; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31341-31344
[^item-code_location-24]: items open-brain:code_location:b4e6ac2ed270852b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4968-4968; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4969-4972; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14196-14196
[^item-code_location-25]: items open-brain:code_location:aee9c7321c8c34cb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4968-4968; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4969-4972; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6602-6608
[^item-code_location-26]: items open-brain:code_location:8c481b50a94924b0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 242-244; 019d837d-d249-71c3-9637-b8d6992ce805 lines 276-278; 019d837d-d249-71c3-9637-b8d6992ce805 lines 293-293
[^item-code_location-27]: items open-brain:code_location:b1cacae7301fc217; 019d837d-d249-71c3-9637-b8d6992ce805 lines 242-244; 019d837d-d249-71c3-9637-b8d6992ce805 lines 276-278; 019d837d-d249-71c3-9637-b8d6992ce805 lines 293-293
[^item-code_location-28]: items open-brain:code_location:601211f367c2be60; 019d837d-d249-71c3-9637-b8d6992ce805 lines 242-244; 019d837d-d249-71c3-9637-b8d6992ce805 lines 276-278; 019d837d-d249-71c3-9637-b8d6992ce805 lines 293-293
[^item-code_location-29]: items open-brain:code_location:a2bd2812fa4d4408; 019d837d-d249-71c3-9637-b8d6992ce805 lines 728-738; 019d837d-d249-71c3-9637-b8d6992ce805 lines 739-742; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1593-1600
[^item-code_location-30]: items open-brain:code_location:203d2bcd5f9c08b9; 019d837d-d249-71c3-9637-b8d6992ce805 lines 468-468; 019d837d-d249-71c3-9637-b8d6992ce805 lines 469-472; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4230-4230
[^item-code_location-31]: items open-brain:code_location:7987fd3c76928b94; 019d837d-d249-71c3-9637-b8d6992ce805 lines 242-244; 019d837d-d249-71c3-9637-b8d6992ce805 lines 276-278; 019d837d-d249-71c3-9637-b8d6992ce805 lines 293-293
[^item-code_location-32]: items open-brain:code_location:ea923144f532357f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72082-72086; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72087-72091; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72372-72377
[^item-code_location-33]: items open-brain:code_location:8d8361927b4b8e96; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71575-71575; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71576-71580; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 76586-76591
[^item-code_location-34]: items open-brain:code_location:e9e40616586e35b7; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3842-3845; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3847-3847; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 3848-3850
[^item-code_location-35]: items open-brain:code_location:49092fc90e416b45; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 28312-28318; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71575-71575; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71576-71580
[^item-code_location-36]: items open-brain:code_location:8e8022362f90cf70; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 19042-19053; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20855-20858; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71268-71283
[^item-code_location-37]: items open-brain:code_location:c36b55600c6cb829; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6259-6275; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6276-6279; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 70561-70570
[^item-code_location-38]: items open-brain:code_location:f92c75534c911210; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 65742-65747; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 68491-68496; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 68530-68535
[^item-code_location-39]: items open-brain:code_location:32f670d120407975; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 65541-65544; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 65578-65581; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 65748-65751
[^item-code_location-40]: items open-brain:code_location:41819e46ae85c964; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 45641-45641; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 45642-45646; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57774-57779
[^item-code_location-41]: items open-brain:code_location:eff55c78440ec495; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 51285-51288; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 51308-51311; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 51327-51330
[^item-code_location-42]: items open-brain:code_location:7536531b05748886; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 33067-33067; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 33068-33071; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44580-44580
[^item-code_location-43]: items open-brain:code_location:15508d16103c5460; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5897-5900; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 39851-39862
[^item-code_location-44]: items open-brain:code_location:fa1bc65365cb1e99; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26677-26680; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26701-26704; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26706-26706
[^item-code_location-45]: items open-brain:code_location:ffa12946862931fd; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 28872-28876; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 28872-28876; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 28872-28876
[^item-code_location-46]: items open-brain:code_location:763c831f20d0b4f5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26039-26042; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 32321-32326; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 32327-32330
[^item-code_location-47]: items open-brain:code_location:c9e3459b8af228cc; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26039-26042; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31340-31340; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31341-31344
[^item-code_location-48]: items open-brain:code_location:bca3664925c75fec; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22212-22212; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22213-22216; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 30278-30282
[^item-code_location-49]: items open-brain:code_location:010b6b464c86edf7; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26546-26550; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26606-26610; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 28657-28661
[^item-code_location-50]: items open-brain:code_location:ec21e98cd05b07d0; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26619-26623; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26681-26685; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26693-26697
[^item-code_location-51]: items open-brain:code_location:aa978a8554adb840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26619-26623; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26681-26685; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26693-26697
[^item-code_location-52]: items open-brain:code_location:f92eb3d39c8b1a47; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26546-26550; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26606-26610; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26619-26623
[^item-code_location-53]: items open-brain:code_location:6f1b72afa1173f97; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 8404-8408; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 9137-9141; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 9260-9273
[^item-code_location-54]: items open-brain:code_location:9330f6c13fbf8483; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22322-22326; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22400-22404; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22762-22768
[^item-code_location-55]: items open-brain:code_location:f38a73b1afefdd82; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14196-14196; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14197-14200; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22222-22228
[^item-code_location-56]: items open-brain:code_location:fc725ad60b00cd91; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 7474-7474; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 7475-7478; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 19927-19931
[^item-code_location-57]: items open-brain:code_location:a84f8199b25ab384; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4968-4968; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 4969-4972; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 6259-6275
[^item-code_location-58]: items open-brain:code_location:405e6c120acf62d5; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14196-14196; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14197-14200; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 16328-16328
[^item-code_location-59]: items open-brain:code_location:d16732dd1a3ca3ea; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14196-14196; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14197-14200; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22212-22212
[^item-code_location-60]: items open-brain:code_location:52e57ad7e47ca6ae; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14196-14196; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 14197-14200; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 22212-22212
