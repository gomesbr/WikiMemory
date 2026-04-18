---
title: "AI Trader - Code Map"
page_id: "projects/ai-trader/code-map"
domain: "ai-trader"
bucket: "code-map"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:07:10.937925Z
source_count: 74
claim_count: 5
tags:
  - wikimemory
  - project
  - ai-trader
  - bucket
  - code-map
---
# AI Trader - Code Map

Navigation: [[projects/ai-trader/index|AI Trader]] | [[projects/ai-trader/communication-preferences|AI Trader - Communication Preferences]] | [[projects/ai-trader/workflow-rules|AI Trader - Workflow Rules]] | [[projects/ai-trader/architecture|AI Trader - Architecture]] | [[projects/ai-trader/current-state|AI Trader - Current State]] | [[projects/ai-trader/tasks|AI Trader - Tasks]] | [[projects/ai-trader/outcomes|AI Trader - Outcomes]] | [[projects/ai-trader/failures|AI Trader - Failures]] | [[projects/ai-trader/decisions|AI Trader - Decisions]] | [[projects/ai-trader/next-steps|AI Trader - Next Steps]] | [[projects/ai-trader/open-questions|AI Trader - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- A skill is defined as a set of local instructions stored in a `SKILL.md` file. [latent: project_identity_and_scope] [confidence: strong][^claim-1]
- The source of truth for the skin is located at `CodexClaw/src/ui/skin.ts`. [latent: codebase_map_abstractions] [confidence: strong][^claim-2]
- Session/report persistence is handled in `db.ts` and `reports.ts`. [latent: codebase_map_abstractions] [confidence: strong][^claim-3]
- The full report is saved to a specific path in the store directory. [latent: current_state_synthesis] [confidence: strong][^claim-4]

## Code Location
- Various files are referenced for session filtering and settings management. [latent: codebase_map_abstractions] [confidence: strong][^claim-5]

### Canonical Items
- A skill is a set of local instructions to follow that is stored in a `SKILL.md` file. [confidence: explicit] [recurrence: 62][^item-code_location-1]
- (file: C:/Users/Fabio/.codex/skills/.system/skill-creator/SKILL.md) [confidence: explicit] [recurrence: 61][^item-code_location-2]
- (file: C:/Users/Fabio/.codex/skills/.system/skill-installer/SKILL.md) [confidence: explicit] [recurrence: 61][^item-code_location-3]
- src/trading/scheduler.ts [confidence: explicit] [recurrence: 39][^item-code_location-4]
- src/agents/runner.ts [confidence: explicit] [recurrence: 39][^item-code_location-5]
- - Source of truth skin lives at `CodexClaw/src/ui/skin.ts`. [confidence: explicit] [recurrence: 17][^item-code_location-6]
- - Session/report persistence in [db.ts](C:/Users/Fabio/Cursor AI projects/Projects/CodexClaw/src/db.ts) and [reports.ts](C:/Users/Fabio/Cursor AI projects/Projects/CodexClaw/src/reports.ts) [confidence: explicit] [recurrence: 4][^item-code_location-7]
- - research.md: CodexClaw/personas/research.md [confidence: explicit] [recurrence: 3][^item-code_location-8]
- - Scheduler filtering before send/run: [scheduler.ts](C:/Users/Fabio/Cursor AI projects/Projects/CodexClaw/src/trading/scheduler.ts:38), [scheduler.ts](C:/Users/Fabio/Cursor AI projects/Projects/CodexClaw/src/trading/scheduler.ts:56), [scheduler.ts](C:/User... [confidence: explicit] [recurrence: 3][^item-code_location-9]
- - `libs/common/src/settings.ts` [confidence: explicit] [recurrence: 3][^item-code_location-10]
- Full report saved to: store/reports/2026-03-01T20-09-09-238Z_8041307210_strategist.md [confidence: explicit] [recurrence: 3][^item-code_location-11]
- - [index.ts](/C:/Users/Fabio/Cursor%20AI%20projects/Projects/AITrader/apps/approval_ui/src/index.ts:34) (`TradeCardView`) [confidence: explicit] [recurrence: 3][^item-code_location-12]
- ## Active file: AITrader/sql/migrations/003_swing_workflow.sql [confidence: explicit] [recurrence: 2][^item-code_location-13]
- - index.html: AITrader/apps/approval_ui/src/public/index.html [confidence: explicit] [recurrence: 2][^item-code_location-14]
- - README.md: AITrader/README.md [confidence: explicit] [recurrence: 2][^item-code_location-15]
- `sql/migrations/README.md` [confidence: explicit] [recurrence: 2][^item-code_location-16]
- - non-coder = `gpt-5`, coder = `gpt-5.3-codex` defaults: [src/config.ts](C:/Users/Fabio/Cursor AI projects/Projects/CodexClaw/src/config.ts:21) [confidence: explicit] [recurrence: 2][^item-code_location-17]
- - [README.md](C:/Users/Fabio/Cursor AI projects/Projects/CodexClaw/README.md) [confidence: explicit] [recurrence: 2][^item-code_location-18]
- - Agent runner + model split in [runner.ts](C:/Users/Fabio/Cursor AI projects/Projects/CodexClaw/src/agents/runner.ts) [confidence: explicit] [recurrence: 2][^item-code_location-19]
- You currently have `AGENTS.md` plus agent persona files in `personas/`. [confidence: explicit] [recurrence: 2][^item-code_location-20]
- - `docs/api_endpoints.md` [confidence: explicit] [recurrence: 2][^item-code_location-21]
- - `libs/common/src/config.ts` [confidence: explicit] [recurrence: 2][^item-code_location-22]
- - 2026-03-01T20-09-09-238Z_8041307210_strategist.md: CodexClaw/store/reports/2026-03-01T20-09-09-238Z_8041307210_strategist.md [confidence: explicit] [recurrence: 2][^item-code_location-23]
- - [package.json](C:/Users/Fabio/Cursor AI projects/Projects/CodexClaw/package.json) [confidence: explicit] [recurrence: 2][^item-code_location-24]
- - `libs/common/src/incidents.ts` [confidence: explicit] [recurrence: 2][^item-code_location-25]
- - Webhook ingest (IP allowlist, idempotent hash, queue enqueue) in `apps/ingest_service/src/index.ts`. [confidence: explicit] [recurrence: 2][^item-code_location-26]
- - `libs/common/src/types.ts` [confidence: explicit] [recurrence: 2][^item-code_location-27]
- > tsx src/index.ts [confidence: explicit] [recurrence: 2][^item-code_location-28]
- - SKILL.md: CodexClaw/contracts/aitrader-agent-ops/SKILL.md [confidence: explicit] [recurrence: 2][^item-code_location-29]
- - open_brain_runbook.md: CodexClaw/docs/operations/open_brain_runbook.md [confidence: explicit] [recurrence: 2][^item-code_location-30]
- - [SPEC.md](C:/Users/Fabio/Cursor AI projects/Projects/CodexClaw/docs/SPEC.md) [confidence: explicit] [recurrence: 2][^item-code_location-31]
- Personas load every run from [`personas/<agent>.md`](C:/Users/Fabio/Cursor AI projects/Projects/CodexClaw/personas/strategist.md) etc. [confidence: explicit] [recurrence: 2][^item-code_location-32]
- - [config.ts](C:/Users/Fabio/Cursor AI projects/Projects/CodexClaw/src/config.ts) [confidence: explicit] [recurrence: 2][^item-code_location-33]
- - Approval/control APIs for setup decisions, runtime settings, risk policy, kill switch, strategy config, account automation, trust recovery, manual cycle runs ([approval_ui/src/index.ts:724](C:/Users/Fabio/Cursor AI projects/Projects/AITrader/apps/approval... [confidence: explicit] [recurrence: 2][^item-code_location-34]
- - Patch attempt on [index.ts](/C:/Users/Fabio/Cursor%20AI%20projects/Projects/AITrader/libs/marketdata/src/index.ts) was rejected by policy. [confidence: explicit] [recurrence: 2][^item-code_location-35]
- ## Active file: CodexClaw/store/reports/x_fx/2017662163540971756.md [confidence: explicit] [recurrence: 2][^item-code_location-36]
- - 2017662163540971756.json: CodexClaw/store/reports/x_full/2017662163540971756.json [confidence: explicit] [recurrence: 2][^item-code_location-37]
- - [scheduler.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/CodexClaw/src/trading/scheduler.ts:66) [confidence: explicit] [recurrence: 2][^item-code_location-38]
- - [ui_layout_fit.test.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/CodexClaw/src/tests/ui_layout_fit.test.ts:11) [confidence: explicit] [recurrence: 2][^item-code_location-39]
- I’m creating `docs/HANDOFF_2026-03-02.md` with current status, verified test state, active blockers, and a copy-paste resume prompt for the next chat. [confidence: explicit] [recurrence: 2][^item-code_location-40]
- - 2026-03-02T03-25-23-740Z_report-test-chat_strategist.md: CodexClaw/store/reports/2026-03-02T03-25-23-740Z_report-test-chat_strategist.md [confidence: explicit] [recurrence: 2][^item-code_location-41]
- - [src/tests/codex_runner_args.test.ts](C:\Users\Fabio\Cursor AI projects\Projects\CodexClaw\src\tests\codex_runner_args.test.ts) [confidence: explicit] [recurrence: 2][^item-code_location-42]
- - `src/tests/bot_routing_guard.test.ts` [confidence: explicit] [recurrence: 2][^item-code_location-43]
- - Daily/timestamp branch cadence + reuse logic in [src/git_policy.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/CodexClaw/src/git_policy.ts:6). [confidence: explicit] [recurrence: 2][^item-code_location-44]
- - Test added for “reuse same daily branch” in [src/tests/git_policy.test.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/CodexClaw/src/tests/git_policy.test.ts:72). [confidence: explicit] [recurrence: 2][^item-code_location-45]
- - Existing migration `sql/migrations/019_one_open_intent_per_setup.sql` stays in place (unique partial index). [confidence: explicit] [recurrence: 2][^item-code_location-46]
- - Performance/backtest: `libs/performance_engine/src/index.ts`, `libs/backtest/src/index.ts` [confidence: explicit] [recurrence: 2][^item-code_location-47]
- - SetupSpec/scoring: `libs/signals/src/index.ts` [confidence: explicit] [recurrence: 2][^item-code_location-48]
- - Wash-sale engine (strict symbol + contract, taxable only): `libs/wash_sale_engine/src/index.ts` [confidence: explicit] [recurrence: 2][^item-code_location-49]
- - `libs/marketdata/src/index.ts` [confidence: explicit] [recurrence: 2][^item-code_location-50]
- - `AITrader/docs/conversation_transcript.md` [confidence: explicit] [recurrence: 2][^item-code_location-51]
- - [Handoff Doc](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/CodexClaw/docs/HANDOFF_2026-03-02.md) [confidence: explicit] [recurrence: 2][^item-code_location-52]
- - Contains only `[remote "origin"]` with URL `https://github.com/gomesbr/AITrader.git` [confidence: explicit] [recurrence: 2][^item-code_location-53]
- - [app.js](/C:/Users/Fabio/Cursor%20AI%20projects/Projects/AITrader/apps/approval_ui/src/public/app.js:1833) (`renderTradeCardLayout`) [confidence: explicit] [recurrence: 2][^item-code_location-54]
- 2) Do you want us to read the transcript at C:\Users\Fabio\Cursor... [confidence: explicit] [recurrence: 2][^item-code_location-55]
- - [src/reports.ts](C:/Users/Fabio/Cursor AI projects/Projects/CodexClaw/src/reports.ts) [confidence: explicit] [recurrence: 2][^item-code_location-56]
- - README.md: AITrader/sql/migrations/README.md [confidence: explicit] [recurrence: 1][^item-code_location-57]
- - `apps/approval_ui/src/public/styles.css` [confidence: explicit] [recurrence: 1][^item-code_location-58]
- - [db.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/CodexClaw/src/db.ts:232) [confidence: explicit] [recurrence: 1][^item-code_location-59]
- - Unified tracked mutation wrapper in [task_tracker.ts](/c:/Users/Fabio/Cursor%20AI%20projects/Projects/CodexClaw/src/task_tracker.ts:1) [confidence: explicit] [recurrence: 1][^item-code_location-60]

## Sources
[^claim-1]: items ai-trader:code_location:83d54b094551d701; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4
[^claim-2]: items ai-trader:code_location:64d4bfd4aeb7cc4f; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-3]: items ai-trader:code_location:40805bd5839e51a0; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1839-1845; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2478-2484; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2592-2596
[^claim-4]: items ai-trader:code_location:eb30e3cf9e676d2c; 019cab4e-ab00-7e31-b50f-faff8205252f lines 5-5; 019cab4e-ab00-7e31-b50f-faff8205252f lines 6-9; 019cab4e-ab00-7e31-b50f-faff8205252f lines 112-115
[^claim-5]: items ai-trader:code_location:42192b8d3c857be0, ai-trader:code_location:14adb4d46ac10b20; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 334-334; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 335-337; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 450-450; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3614-3644; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3645-3648; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 5232-5241
[^item-code_location-1]: items ai-trader:code_location:83d54b094551d701; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4
[^item-code_location-2]: items ai-trader:code_location:a6ed6e22c239d7eb; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-code_location-3]: items ai-trader:code_location:d8c39ff74733f2be; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-code_location-4]: items ai-trader:code_location:a3c4f48c3de544d0; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 7-7; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 8-10; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 322-347
[^item-code_location-5]: items ai-trader:code_location:fc5d247a837a912a; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 7-7; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 8-10; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 322-347
[^item-code_location-6]: items ai-trader:code_location:64d4bfd4aeb7cc4f; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-code_location-7]: items ai-trader:code_location:40805bd5839e51a0; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1839-1845; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2478-2484; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2592-2596
[^item-code_location-8]: items ai-trader:code_location:c80f1b8c1a6f29eb; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 352-370; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 843-857; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 945-971
[^item-code_location-9]: items ai-trader:code_location:42192b8d3c857be0; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 334-334; 019caf9f-c9e4-7d33-9635-28feaa5b3b4a lines 335-337; 019cb0ef-a044-7090-9627-7f2d616c46f2 lines 450-450
[^item-code_location-10]: items ai-trader:code_location:14adb4d46ac10b20; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3614-3644; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3645-3648; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 5232-5241
[^item-code_location-11]: items ai-trader:code_location:eb30e3cf9e676d2c; 019cab4e-ab00-7e31-b50f-faff8205252f lines 5-5; 019cab4e-ab00-7e31-b50f-faff8205252f lines 6-9; 019cab4e-ab00-7e31-b50f-faff8205252f lines 112-115
[^item-code_location-12]: items ai-trader:code_location:949cf5a01835fdae; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 587-589; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 587-589; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 587-589
[^item-code_location-13]: items ai-trader:code_location:0f0ad12b56a326a2; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2238-2265; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2238-2265; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2319-2323
[^item-code_location-14]: items ai-trader:code_location:89db379cc88bc560; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2835-2854; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2855-2878; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2958-2968
[^item-code_location-15]: items ai-trader:code_location:2bf1734824c7e8f9; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1711-1711; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1712-1714; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1722-1726
[^item-code_location-16]: items ai-trader:code_location:8c6f6dd3fb16aa24; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2233-2233; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2234-2237; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2802-2830
[^item-code_location-17]: items ai-trader:code_location:2df97dc3c977c70b; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1131-1140; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1141-1144; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1383-1387
[^item-code_location-18]: items ai-trader:code_location:9d9601af81a29dd2; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 322-347; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 348-351; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1679-1683
[^item-code_location-19]: items ai-trader:code_location:275ad6eb4f2eb744; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1839-1845; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2685-2691; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 3223-3229
[^item-code_location-20]: items ai-trader:code_location:8e8022362f90cf70; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1699-1705; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1924-1924; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1925-1928
[^item-code_location-21]: items ai-trader:code_location:fa1f7444f7685afb; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1075-1079; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2233-2233; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2234-2237
[^item-code_location-22]: items ai-trader:code_location:209141c96c0ca5cf; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1075-1079; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2233-2233; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 2234-2237
[^item-code_location-23]: items ai-trader:code_location:0960c82b9b1ba78d; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 16086-16090; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 16432-16436; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 16510-16514
[^item-code_location-24]: items ai-trader:code_location:ec7eb3b6c547d942; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 322-347; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 348-351; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2592-2596
[^item-code_location-25]: items ai-trader:code_location:6d1fb6795a5ef0e4; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1075-1079; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3614-3644; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 3645-3648
[^item-code_location-26]: items ai-trader:code_location:fe48e341c30e16be; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 888-888; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 889-900; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1717-1721
[^item-code_location-27]: items ai-trader:code_location:4dca2071a5ae986e; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1606-1626; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1627-1630; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 8770-8782
[^item-code_location-28]: items ai-trader:code_location:26eeab925981c5f1; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4258-4258; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4258-4258; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 4259-4280
[^item-code_location-29]: items ai-trader:code_location:dc1230017828d87e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11044-11061; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11115-11125; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11126-11142
[^item-code_location-30]: items ai-trader:code_location:5e757e8990aa8684; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11376-11384; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 11686-11700; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 12760-12770
[^item-code_location-31]: items ai-trader:code_location:780231532a1ed04b; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2468-2468; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2469-2472; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 3410-3412
[^item-code_location-32]: items ai-trader:code_location:534f3530aa24ead6; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2478-2484; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 3410-3412; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 3413-3416
[^item-code_location-33]: items ai-trader:code_location:828c021a04e16068; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 2685-2691; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 3223-3229; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 3115-3115
[^item-code_location-34]: items ai-trader:code_location:b1b8e6f0b340ed7e; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 1065-1065; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 1065-1065; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 1065-1065
[^item-code_location-35]: items ai-trader:code_location:9f292af5ef2c42c6; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 632-632; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 632-632; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 633-635
[^item-code_location-36]: items ai-trader:code_location:d66ab08274e8cf55; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 19577-19593; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 19577-19593; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5-24
[^item-code_location-37]: items ai-trader:code_location:8f4833cdd13a656d; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 19577-19593; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5-24; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 695-705
[^item-code_location-38]: items ai-trader:code_location:c88de48904cbeade; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 4294-4296; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 4297-4300; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 4550-4550
[^item-code_location-39]: items ai-trader:code_location:c216f3ed826ae286; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 16005-16009; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 16081-16085; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 16503-16509
[^item-code_location-40]: items ai-trader:code_location:aa8bf2c2dad7121f; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 19594-19610; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 19611-19611; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 1225-1228
[^item-code_location-41]: items ai-trader:code_location:38777335312b0895; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 16938-16942; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 17088-17092; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 17132-17149
[^item-code_location-42]: items ai-trader:code_location:f52077df548d152e; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 18313-18318; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 690-690; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 691-694
[^item-code_location-43]: items ai-trader:code_location:3453e191329ec3c8; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 150-152; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 153-155; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 690-690
[^item-code_location-44]: items ai-trader:code_location:f7974ea08d73cb7c; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 3396-3402; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 16629-16646; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 16917-16923
[^item-code_location-45]: items ai-trader:code_location:72a5a61ccedf0b57; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 3396-3402; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 16917-16923; 019caca3-cd0b-73b0-99f0-1ef6221f7cae lines 150-152
[^item-code_location-46]: items ai-trader:code_location:9de5b2fe8e9903ea; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 14168-14177; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 14178-14181; 019caaa7-2fe4-7a72-9693-6b998656746e lines 769-769
[^item-code_location-47]: items ai-trader:code_location:be3885a5d74c20e2; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 888-888; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 889-900; 019caaa7-2fe4-7a72-9693-6b998656746e lines 769-769
[^item-code_location-48]: items ai-trader:code_location:c454a8a0e42a4ae9; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 888-888; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 889-900; 019caaa7-2fe4-7a72-9693-6b998656746e lines 769-769
[^item-code_location-49]: items ai-trader:code_location:6d2dcf9a70ee4212; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 888-888; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 889-900; 019caaa7-2fe4-7a72-9693-6b998656746e lines 769-769
[^item-code_location-50]: items ai-trader:code_location:785c1b31b539b3e2; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1606-1626; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1627-1630; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 461-463
[^item-code_location-51]: items ai-trader:code_location:536a3fda417132a8; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 17632-17636; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 17637-17653; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 17721-17738
[^item-code_location-52]: items ai-trader:code_location:51744e5bfe498efc; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 19617-19623; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 5-24
[^item-code_location-53]: items ai-trader:code_location:78ae2e20f558c202; 019cb148-7e62-79a3-af96-9f74a1edaa78 lines 237-237; 019cb148-7e62-79a3-af96-9f74a1edaa78 lines 238-241; 019cb166-459d-7a01-a948-70994c21d327 lines 35-58
[^item-code_location-54]: items ai-trader:code_location:84cf160f82936cc2; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 587-589; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 590-593; 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0 lines 1053-1053
[^item-code_location-55]: items ai-trader:code_location:6beeddbe90909271; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-code_location-56]: items ai-trader:code_location:66585b0b0beb8af1; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 1679-1683; 019ca18a-3473-7743-a7c0-50d4922dea5d lines 3-4
[^item-code_location-57]: items ai-trader:code_location:d32e0c937ab0471c; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1711-1711; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1712-1714; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1722-1726
[^item-code_location-58]: items ai-trader:code_location:7cdca2d32fe78bfd; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1075-1079; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1606-1626; 019c687b-3d0d-71c0-8929-9128cbf24060 lines 1627-1630
[^item-code_location-59]: items ai-trader:code_location:4d957b4c953e9c43; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 4294-4296; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 4294-4296; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 4294-4296
[^item-code_location-60]: items ai-trader:code_location:160fd5738361cffa; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 4550-4550; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 4551-4554; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 18096-18109
