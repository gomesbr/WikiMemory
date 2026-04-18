---
title: "Global - Code Map"
page_id: "global/code-map"
domain: "global"
bucket: "code-map"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:06:37.202528Z
source_count: 27
claim_count: 6
tags:
  - wikimemory
  - global
  - global
  - bucket
  - code-map
---
# Global - Code Map

Navigation: [[global/index|Global]] | [[global/communication-preferences|Global - Communication Preferences]] | [[global/workflow-rules|Global - Workflow Rules]] | [[global/architecture|Global - Architecture]] | [[global/current-state|Global - Current State]] | [[global/tasks|Global - Tasks]] | [[global/outcomes|Global - Outcomes]] | [[global/failures|Global - Failures]] | [[global/decisions|Global - Decisions]] | [[global/next-steps|Global - Next Steps]] | [[global/open-questions|Global - Open Questions]]

## Summary
- Skills are defined as sets of local instructions stored in SKILL.md files. [latent: project_identity_and_scope] [confidence: strong][^claim-1]
- The project includes various source files that handle different functionalities such as memory capture, persistence, and UI operations. [latent: architecture_synthesis] [confidence: strong][^claim-2]
- The skills and their management are integral to the functionality of the Codex CLI and its associated tools. [latent: project_identity_and_scope] [confidence: strong][^claim-3]

## Code Location
- The file structure includes directories for skills, UI, and various source files that manage different aspects of the application. [latent: codebase_map_abstractions] [confidence: strong][^claim-4]
- Each skill is represented by a SKILL.md file located in specific directories for organization and access. [latent: codebase_map_abstractions] [confidence: strong][^claim-5]
- The source files are categorized by their functionality, such as memory management, database interactions, and server operations. [latent: architecture_synthesis] [confidence: strong][^claim-6]

### Canonical Items
- # AGENTS.md instructions for c:\Users\Fabio\Cursor AI projects\Projects [confidence: explicit] [recurrence: 25][^item-code_location-1]
- (file: C:/Users/Fabio/.codex/skills/.system/skill-creator/SKILL.md) [confidence: explicit] [recurrence: 25][^item-code_location-2]
- (file: C:/Users/Fabio/.codex/skills/.system/skill-installer/SKILL.md) [confidence: explicit] [recurrence: 25][^item-code_location-3]
- A skill is a set of local instructions to follow that is stored in a `SKILL.md` file. [confidence: explicit] [recurrence: 25][^item-code_location-4]
- strategist routes to it in `src/bot.ts`. [confidence: explicit] [recurrence: 18][^item-code_location-5]
- - `src/ui/server.ts`: local operations dashboard [confidence: explicit] [recurrence: 18][^item-code_location-6]
- - `src/agent.ts`: Codex CLI subprocess + JSONL parser [confidence: explicit] [recurrence: 17][^item-code_location-7]
- - `src/db.ts`: persistence layer [confidence: explicit] [recurrence: 17][^item-code_location-8]
- - `src/mcp.ts`: MCP server/tool integration + allowlist [confidence: explicit] [recurrence: 17][^item-code_location-9]
- - `src/memory.ts`: memory capture + retrieval [confidence: explicit] [recurrence: 17][^item-code_location-10]
- - `src/profiles.ts`: workspace profile management [confidence: explicit] [recurrence: 17][^item-code_location-11]
- - `src/providers.ts`: non-coder provider abstraction and fallback chain [confidence: explicit] [recurrence: 17][^item-code_location-12]
- - `src/skills.ts`: skill discovery/matching/context builder [confidence: explicit] [recurrence: 17][^item-code_location-13]
- - `src/subagents.ts`: subagent queue, execution, worker loop [confidence: explicit] [recurrence: 17][^item-code_location-14]
- - `src/trading/scheduler.ts`: cron automation [confidence: explicit] [recurrence: 17][^item-code_location-15]
- - `src/agent_inbox_worker.ts`: heartbeat/checkpoint worker for assigned agent tasks [confidence: explicit] [recurrence: 16][^item-code_location-16]
- - North-star intent is persisted per chat in `store/workspaces/<chat_id>/_intent/NORTH_STAR.md`. [confidence: explicit] [recurrence: 16][^item-code_location-17]
- - `audits/full_load_notices.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-18]
- - `config/full_load_config.json` [confidence: explicit] [recurrence: 1][^item-code_location-19]
- - `state/full_load_runs.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-20]
- - `state/full_load_state.json` [confidence: explicit] [recurrence: 1][^item-code_location-21]
- - `audits/refresh_notices.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-22]
- - `state/refresh_runs.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-23]
- - `state/refresh_state.json` [confidence: explicit] [recurrence: 1][^item-code_location-24]
- - Add `config/refresh_config.json` [confidence: explicit] [recurrence: 1][^item-code_location-25]
- - `audits/bootstrap_notices.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-26]
- - `bootstrap/global.md` [confidence: explicit] [recurrence: 1][^item-code_location-27]
- - `bootstrap/projects/cross-project.md` [confidence: explicit] [recurrence: 1][^item-code_location-28]
- - `config/bootstrap_config.json` [confidence: explicit] [recurrence: 1][^item-code_location-29]
- - `state/bootstrap_runs.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-30]
- - `state/bootstrap_state.json` [confidence: explicit] [recurrence: 1][^item-code_location-31]
- - `state/wiki_state.json` [confidence: explicit] [recurrence: 1][^item-code_location-32]
- - `audits/wiki_notices.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-33]
- - `state/wiki_runs.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-34]
- - `audits/classification_notices.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-35]
- - `classified/sources/<source_id>/segments.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-36]
- - `classified/sources/<source_id>/stats.json` [confidence: explicit] [recurrence: 1][^item-code_location-37]
- - `config/classification_taxonomy.json` [confidence: explicit] [recurrence: 1][^item-code_location-38]
- - `state/classification_runs.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-39]
- - `state/classification_state.json` [confidence: explicit] [recurrence: 1][^item-code_location-40]
- - `schema/normalization_catalog.json` [confidence: explicit] [recurrence: 1][^item-code_location-41]
- - `state/normalization_runs.jsonl` [confidence: explicit] [recurrence: 1][^item-code_location-42]
- - `state/normalization_state.json` [confidence: explicit] [recurrence: 1][^item-code_location-43]
- - Preserve compaction-related entries, including outer `compacted` events and `event_msg.payload.type = context_compacted`, as first-class normalized events. [confidence: explicit] [recurrence: 1][^item-code_location-44]
- - Stage updated `normalization_state.json`, `normalization_runs.jsonl`, and `normalization_notices.jsonl` in temp files too. [confidence: explicit] [recurrence: 1][^item-code_location-45]
- Next I’ll extract concrete responsibilities from `AGENTS.md`, persona files, and the scheduler so the roadmap is role-specific instead of generic. [confidence: explicit] [recurrence: 1][^item-code_location-46]
- First I’ll read `skill-creator` guidance plus `CodexClaw/AGENTS.md`, `skills.md`, personas, and `scheduler.ts` so the plan matches your current agent architecture and daily flow. [confidence: explicit] [recurrence: 1][^item-code_location-47]
- - 2017662163540971756.json: CodexClaw/store/reports/x_full/2017662163540971756.json [confidence: explicit] [recurrence: 1][^item-code_location-48]
- - 2017662163540971756.md: CodexClaw/store/reports/x_fx/2017662163540971756.md [confidence: explicit] [recurrence: 1][^item-code_location-49]
- - 2026-03-01T20-09-09-238Z_8041307210_strategist.md: CodexClaw/store/reports/2026-03-01T20-09-09-238Z_8041307210_strategist.md [confidence: explicit] [recurrence: 1][^item-code_location-50]
- - `docs/HANDOFF_2026-03-02.md` [confidence: explicit] [recurrence: 1][^item-code_location-51]
- - `docs/operations/runbook.md` [confidence: explicit] [recurrence: 1][^item-code_location-52]
- - HANDOFF_2026-03-02.md: CodexClaw/docs/HANDOFF_2026-03-02.md [confidence: explicit] [recurrence: 1][^item-code_location-53]
- - runbook.md: CodexClaw/docs/operations/runbook.md [confidence: explicit] [recurrence: 1][^item-code_location-54]
- Style update in `src/ui/skin.ts`: [confidence: explicit] [recurrence: 1][^item-code_location-55]
- Create file tmp_codex_write_probe_dfa_1772496114.txt with exact content 'probe-ok' and then reply only: done [confidence: explicit] [recurrence: 1][^item-code_location-56]
- Create file tmp_codex_write_probe_danger_1772496002.txt with exact content 'probe-ok' and then reply only: done [confidence: explicit] [recurrence: 1][^item-code_location-57]
- Create file tmp_codex_write_probe_a_1772495983.txt with exact content 'probe-ok' and then reply only: done [confidence: explicit] [recurrence: 1][^item-code_location-58]
- Create file tmp_codex_write_probe_1772495949.txt with exact content 'probe-ok' and then reply only: done [confidence: explicit] [recurrence: 1][^item-code_location-59]
- - 2026-03-02T03-25-23-740Z_report-test-chat_strategist.md: CodexClaw/store/reports/2026-03-02T03-25-23-740Z_report-test-chat_strategist.md [confidence: explicit] [recurrence: 1][^item-code_location-60]

## Sources
[^claim-1]: items global:code_location:83d54b094551d701; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6
[^claim-2]: items global:code_location:489eae885e08005e, global:code_location:dd13b90cd4f4215b, global:code_location:485bd3284eb0f042, global:code_location:ec2a00127b6a0f20, global:code_location:2364936d1ae3b63a; 019c9f4b-8acd-70d1-bd77-e2356d46b6f2 lines 91-91; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^claim-3]: items global:code_location:f1518f27e3459bba, global:code_location:e994e7b931ef707b; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^claim-4]: items global:code_location:cc1a8819596b5bd9, global:code_location:a6ed6e22c239d7eb, global:code_location:d8c39ff74733f2be, global:code_location:dd13b90cd4f4215b, global:code_location:f1518f27e3459bba; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2-4; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2-4; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 18171-18178; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2-4; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 18171-18178; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^claim-5]: items global:code_location:83d54b094551d701; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6
[^claim-6]: items global:code_location:489eae885e08005e, global:code_location:485bd3284eb0f042, global:code_location:ec2a00127b6a0f20, global:code_location:2364936d1ae3b63a; 019c9f4b-8acd-70d1-bd77-e2356d46b6f2 lines 91-91; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-1]: items global:code_location:cc1a8819596b5bd9; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2-4
[^item-code_location-2]: items global:code_location:a6ed6e22c239d7eb; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2-4; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 18171-18178
[^item-code_location-3]: items global:code_location:d8c39ff74733f2be; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2-4; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 18171-18178
[^item-code_location-4]: items global:code_location:83d54b094551d701; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3-6
[^item-code_location-5]: items global:code_location:489eae885e08005e; 019c9f4b-8acd-70d1-bd77-e2356d46b6f2 lines 91-91; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4
[^item-code_location-6]: items global:code_location:dd13b90cd4f4215b; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-7]: items global:code_location:f1518f27e3459bba; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-8]: items global:code_location:e994e7b931ef707b; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-9]: items global:code_location:16e4a8dbe1bb2ff6; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-10]: items global:code_location:485bd3284eb0f042; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-11]: items global:code_location:ec2a00127b6a0f20; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-12]: items global:code_location:2364936d1ae3b63a; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-13]: items global:code_location:cad7fdc904c9feed; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-14]: items global:code_location:a35dfb44fc7863f2; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-15]: items global:code_location:a3c4f48c3de544d0; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-16]: items global:code_location:b4d0b7f95487f1f2; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-17]: items global:code_location:bdb78c6a0f288030; 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5 lines 3-3; 019ca6fa-7ec5-7f71-ab37-96eb69672b2c lines 3-4; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 3-4
[^item-code_location-18]: items global:code_location:392e59078aa7eabd; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4327-4330; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4333-4333; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4334-4335
[^item-code_location-19]: items global:code_location:15aaef59d294d4fa; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4327-4330; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4333-4333; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4334-4335
[^item-code_location-20]: items global:code_location:811ce1633191482a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4327-4330; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4333-4333; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4334-4335
[^item-code_location-21]: items global:code_location:96d0ad14fba42aa4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4327-4330; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4333-4333; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4334-4335
[^item-code_location-22]: items global:code_location:4ed8e63d033fb75d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3142-3146
[^item-code_location-23]: items global:code_location:10663f90e4db1027; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3142-3146
[^item-code_location-24]: items global:code_location:1ac0b20787bf6100; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3142-3146
[^item-code_location-25]: items global:code_location:254b04cc22c49f58; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3142-3146
[^item-code_location-26]: items global:code_location:f0bbd79dc7b8f7aa; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2609-2609; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2610-2613
[^item-code_location-27]: items global:code_location:dc908d6889f9a66f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2609-2609; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2610-2613
[^item-code_location-28]: items global:code_location:8bcc8a498df92b8d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2609-2609; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2610-2613
[^item-code_location-29]: items global:code_location:3946fbcccf6e45ae; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2609-2609; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2610-2613
[^item-code_location-30]: items global:code_location:e07b4cd725ebc7a0; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2609-2609; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2610-2613
[^item-code_location-31]: items global:code_location:11882286c3ccbff2; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2609-2609; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2610-2613
[^item-code_location-32]: items global:code_location:e5dbbe3eace00141; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1377-1380; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1383-1383; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1384-1385
[^item-code_location-33]: items global:code_location:37eb6cd467ea8167; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1377-1380; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1377-1380; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1383-1383
[^item-code_location-34]: items global:code_location:d51ebe4de739e677; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1377-1380; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1383-1383; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1384-1385
[^item-code_location-35]: items global:code_location:2c7c9c76b6d2758d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 799-802; 019d837d-d249-71c3-9637-b8d6992ce805 lines 805-805; 019d837d-d249-71c3-9637-b8d6992ce805 lines 806-807
[^item-code_location-36]: items global:code_location:bca5f51206431ed6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 799-802; 019d837d-d249-71c3-9637-b8d6992ce805 lines 805-805; 019d837d-d249-71c3-9637-b8d6992ce805 lines 806-807
[^item-code_location-37]: items global:code_location:2951c44156e0ac4d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 799-802; 019d837d-d249-71c3-9637-b8d6992ce805 lines 805-805; 019d837d-d249-71c3-9637-b8d6992ce805 lines 806-807
[^item-code_location-38]: items global:code_location:9a05af1d5e35b3ab; 019d837d-d249-71c3-9637-b8d6992ce805 lines 799-802; 019d837d-d249-71c3-9637-b8d6992ce805 lines 799-802; 019d837d-d249-71c3-9637-b8d6992ce805 lines 805-805
[^item-code_location-39]: items global:code_location:3fb1af7a67bed036; 019d837d-d249-71c3-9637-b8d6992ce805 lines 799-802; 019d837d-d249-71c3-9637-b8d6992ce805 lines 805-805; 019d837d-d249-71c3-9637-b8d6992ce805 lines 806-807
[^item-code_location-40]: items global:code_location:82ae0783956f4f29; 019d837d-d249-71c3-9637-b8d6992ce805 lines 799-802; 019d837d-d249-71c3-9637-b8d6992ce805 lines 805-805; 019d837d-d249-71c3-9637-b8d6992ce805 lines 806-807
[^item-code_location-41]: items global:code_location:0aca7d36b40d25f4; 019d837d-d249-71c3-9637-b8d6992ce805 lines 287-290
[^item-code_location-42]: items global:code_location:93338d9dce4cc9d9; 019d837d-d249-71c3-9637-b8d6992ce805 lines 287-290
[^item-code_location-43]: items global:code_location:4a53d2b2f483e58e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 287-290
[^item-code_location-44]: items global:code_location:6851eb6868af1334; 019d837d-d249-71c3-9637-b8d6992ce805 lines 287-290
[^item-code_location-45]: items global:code_location:de7f7221cd87c14e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 287-290
[^item-code_location-46]: items global:code_location:8e8022362f90cf70; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1827-1839
[^item-code_location-47]: items global:code_location:209a0f4eb42df9b8; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 1818-1824
[^item-code_location-48]: items global:code_location:8f4833cdd13a656d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1046-1054; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1230-1230
[^item-code_location-49]: items global:code_location:d66ab08274e8cf55; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1046-1054; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1230-1230
[^item-code_location-50]: items global:code_location:0960c82b9b1ba78d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1046-1054; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1230-1230
[^item-code_location-51]: items global:code_location:aa8bf2c2dad7121f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1230-1230
[^item-code_location-52]: items global:code_location:d945ffe2c4290b84; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1230-1230
[^item-code_location-53]: items global:code_location:058580cf60ed97d3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1046-1054; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1230-1230
[^item-code_location-54]: items global:code_location:91643a6197db1c2c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1046-1054; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1230-1230
[^item-code_location-55]: items global:code_location:e75295cfe893a223; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1230-1230
[^item-code_location-56]: items global:code_location:9e1222bf6bbde341; 019cb100-5540-7371-8eb5-a89bab51137b lines 5-18
[^item-code_location-57]: items global:code_location:e7500c35cb3a937a; 019cb0fe-a160-7362-85e0-720ad035cf30 lines 5-18
[^item-code_location-58]: items global:code_location:0cc53d4703fcb33e; 019cb0fe-5561-75f0-803f-0525f796830d lines 5-17
[^item-code_location-59]: items global:code_location:8165ab8957903379; 019cb0fd-cf4c-7520-baf2-de448646fff2 lines 5-17
[^item-code_location-60]: items global:code_location:38777335312b0895; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 18171-18178
