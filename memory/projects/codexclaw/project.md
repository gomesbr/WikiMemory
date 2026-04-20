---
type: project-memory
project: codexclaw
updated: 2026-04-20T01:19:51.494261Z
tags: [project/codexclaw, memory]
---

# Codexclaw - Project Memory

## PURPOSE

- CodexClaw Pro is a multi-agent trading operations orchestrator (Telegram/Node + optional Ops UI) where strategist-led workflows coordinate research, execution-risk monitoring, and coder development; it is advisory-only and must never execute trades directly.

## CORE COMPONENTS

- Core orchestration is role-separated: strategist is the user-facing orchestrator/final synthesis voice; research provides analysis/trade ideas; execution provides monitoring and risk guidance; coder performs software implementation. Personas are defined in dedicated files and per chat_id+agent state is persisted.

## CURRENT ARCHITECTURE

- Current architecture supports mixed providers: strategist/research/execution can run via OpenAI Responses API (GPT-5) while coder runs via Codex CLI; a CLI-only alternative for non-coder roles remains under consideration.
- CodexClaw includes an all-agent AI Tracker (Kanban + APIs), persistent memory/profile layers, skills loading from SKILL.md under skills/, and large-report archiving to store/reports with SQLite indexing; user replies should surface concise highlights plus report location metadata.

## DIRECTORY TREE

`cd C:\Users\Fabio\Cursor AI projects\Projects\CodexClaw; tree /F /A`

```text
CodexClaw/
|-- .github/
|   |-- ISSUE_TEMPLATE/
|   |   |-- bug_report.yml
|   |   |-- config.yml
|   |   `-- feature_request.yml
|   |-- workflows/
|   |   `-- ci.yml
|   |-- CODEOWNERS
|   |-- dependabot.yml
|   `-- pull_request_template.md
|-- artifacts/
|   `-- ai_trader_branch_inventory/
|       |-- branches.json
|       |-- delivery_task_completed.txt
|       `-- provenance.txt
|-- contracts/
|   `-- aitrader-agent-ops/
|       |-- assets/
|       |   `-- schemas/
|       |       |-- candidate_output.json
|       |       `-- trade_card_create_payload.json
|       |-- references/
|       |   |-- api_contracts.md
|       |   |-- daily_runbook.md
|       |   `-- prompt_catalog.md
|       |-- contracts.lock.json
|       `-- SKILL.md
|-- docs/
|   |-- operations/
|   |   |-- open_brain_cutover.md
|   |   |-- open_brain_runbook.md
|   |   `-- runbook.md
|   |-- CODEXCLAW_EPICS_TICKETS_PLAN.md
|   |-- GITHUB_SETUP.md
|   |-- HANDOFF_2026-03-02.md
|   `-- SPEC.md
|-- personas/
|   |-- coder.md
|   |-- execution.md
|   |-- research.md
|   `-- strategist.md
|-- skills/
|   |-- aitrader-coder-ops/
|   |   |-- references/
|   |   |   `-- checklist.md
|   |   `-- SKILL.md
|   |-- aitrader-execution-ops/
|   |   |-- references/
|   |   |   `-- recommendations.md
|   |   `-- SKILL.md
|   |-- aitrader-research-ops/
|   |   |-- references/
|   |   |   `-- schema.md
|   |   `-- SKILL.md
|   |-- aitrader-strategist-ops/
|   |   |-- references/
|   |   |   `-- workflow.md
|   |   `-- SKILL.md
|   |-- coder-windows-runtime/
|   |   `-- SKILL.md
|   |-- constraint-architecture/
|   |   `-- SKILL.md
|   |-- decomposition-planner/
|   |   `-- SKILL.md
|   |-- default-research/
|   |   `-- SKILL.md
|   |-- eval-design/
|   |   `-- SKILL.md
|   |-- intent-capture/
|   |   `-- SKILL.md
|   |-- root-cause-autonomy/
|   |   `-- SKILL.md
|   |-- spec-pack/
|   |   `-- SKILL.md
|   `-- strategist-routing-contract/
|       `-- SKILL.md
|-- src/
|   |-- agents/
|   |   `-- runner.ts
|   |-- scripts/
|   |   |-- contracts/
|   |   |   `-- sync_aitrader_contracts.ts
|   |   |-- ops/
|   |   |   |-- aitrader_precutover_readiness.ts
|   |   |   |-- scheduler_toggle.ts
|   |   |   `-- verify_scheduler_skip.ts
|   |   `-- import_reports_memory.ts
|   |-- tests/
|   |   |-- agent_inbox_worker.test.ts
|   |   |-- agent_task_claims.test.ts
|   |   |-- aitrader_agent_client.test.ts
|   |   |-- blocker_reason_required.test.ts
|   |   |-- bot_routing_guard.test.ts
|   |   |-- chat_story_state.test.ts
|   |   |-- close_guard.test.ts
|   |   |-- coder_runtime_retry.test.ts
|   |   |-- codex_runner_args.test.ts
|   |   |-- config_store.test.ts
|   |   |-- core_skills.test.ts
|   |   |-- evaluation.test.ts
|   |   |-- git_policy.test.ts
|   |   |-- impact_policy.test.ts
|   |   |-- intake_gate.test.ts
|   |   |-- intent.test.ts
|   |   |-- mcp.test.ts
|   |   |-- memory.test.ts
|   |   |-- pr_automation.test.ts
|   |   |-- profiles.test.ts
|   |   |-- providers.test.ts
|   |   |-- quality_gate.test.ts
|   |   |-- report_importer.test.ts
|   |   |-- reports.test.ts
|   |   |-- routing_contract.test.ts
|   |   |-- runner_prompt_transport.test.ts
|   |   |-- scheduler.test.ts
|   |   |-- semantic_dedupe.test.ts
|   |   |-- session_epoch.test.ts
|   |   |-- skills.test.ts
|   |   |-- spec_pack.test.ts
|   |   |-- specialist_ownership.test.ts
|   |   |-- story_board.test.ts
|   |   |-- story_tasks.test.ts
|   |   |-- subagents.test.ts
|   |   |-- task_ac_results.test.ts
|   |   |-- task_directives.test.ts
|   |   |-- task_impact.test.ts
|   |   |-- ui_docs_api.test.ts
|   |   |-- ui_expand_collapse.test.ts
|   |   |-- ui_layout_fit.test.ts
|   |   |-- user_output_filter.test.ts
|   |   `-- windows_preflight.test.ts
|   |-- trading/
|   |   `-- scheduler.ts
|   |-- ui/
|   |   |-- config_store.ts
|   |   |-- server.ts
|   |   `-- skin.ts
|   |-- agent.ts
|   |-- agent_inbox_worker.ts
|   |-- aitrader_agent_client.ts
|   |-- bot.ts
|   |-- config.ts
|   |-- db.ts
|   |-- evaluation.ts
|   |-- git_policy.ts
|   |-- github_project_sync.ts
|   |-- impact_policy.ts
|   |-- index.ts
|   |-- intent.ts
|   |-- logger.ts
|   |-- mcp.ts
|   |-- memory.ts
|   |-- memory_openbrain.ts
|   |-- memory_provider.ts
|   |-- openai.ts
|   |-- pr_automation.ts
|   |-- profiles.ts
|   |-- providers.ts
|   |-- report_importer.ts
|   |-- reports.ts
|   |-- skills.ts
|   |-- spec_pack.ts
|   |-- story_tasks.ts
|   |-- subagents.ts
|   |-- task_directives.ts
|   |-- task_tracker.ts
|   `-- telegram.ts
|-- store/
|   |-- logs/
|   |   `-- dev.log
|   |-- memory/
|   |   |-- 8041307210/
|   |   |   |-- 2026-02-28.md
|   |   |   |-- 2026-03-01.md
|   |   |   |-- 2026-03-02.md
|   |   |   |-- 2026-03-03.md
|   |   |   `-- 2026-03-04.md
|   |   `-- memory-test-chat/
|   |       |-- 2026-02-27.md
|   |       |-- 2026-02-28.md
|   |       |-- 2026-03-01.md
|   |       |-- 2026-03-02.md
|   |       |-- 2026-03-03.md
|   |       |-- 2026-03-04.md
|   |       `-- 2026-03-05.md
|   |-- reports/
|   |   |-- x_full/
|   |   |   |-- 2017662163540971756.json
|   |   |   |-- 2019894389099892746.json
|   |   |   |-- 2020279547745226803.json
|   |   |   |-- 2020633743401345158.json
|   |   |   |-- 2020704611640705485.json
|   |   |   |-- 2021740954244550839.json
|   |   |   |-- 2021957085043232890.json
|   |   |   |-- 2022055604333031886.json
|   |   |   |-- 2022406652897698010.json
|   |   |   |-- 2023894165164335364.json
|   |   |   |-- 2023990222027915746.json
|   |   |   |-- 2025302022749389282.json
|   |   |   `-- 2025920521871716562.json
|   |   |-- x_fx/
|   |   |   |-- 2017662163540971756.json
|   |   |   |-- 2017662163540971756.md
|   |   |   |-- 2019894389099892746.jpg
|   |   |   |-- 2019894389099892746.json
|   |   |   |-- 2020279547745226803.json
|   |   |   |-- 2020633743401345158.jpg
|   |   |   |-- 2020633743401345158.json
|   |   |   |-- 2020704611640705485.json
|   |   |   |-- 2021740954244550839.json
|   |   |   |-- 2021957085043232890.json
|   |   |   |-- 2021957085043232890.md
|   |   |   |-- 2022055604333031886.jpg
|   |   |   |-- 2022055604333031886.json
|   |   |   |-- 2022406652897698010.json
|   |   |   |-- 2023894165164335364.json
|   |   |   |-- 2023990222027915746.json
|   |   |   |-- 2025302022749389282.json
|   |   |   |-- 2025302022749389282.md
|   |   |   |-- 2025920521871716562.json
|   |   |   `-- 2025920521871716562.md
|   |   |-- 2026-02-27T21-43-35-151Z_123456_strategist.md
|   |   |-- 2026-02-27T23-20-37-855Z_8041307210_strategist.md
|   |   |-- 2026-02-27T23-30-13-771Z_8041307210_strategist.md
|   |   |-- 2026-02-27T23-38-35-995Z_8041307210_strategist.md
|   |   |-- 2026-02-27T23-59-33-093Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T00-01-54-439Z_8041307210_strategist.md
|   |   |-- 2026-02-28T00-02-18-918Z_8041307210_strategist.md
|   |   |-- 2026-02-28T00-10-02-716Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T00-36-50-688Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T00-42-21-799Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T00-50-47-424Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T01-16-12-504Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T01-17-50-037Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T01-26-49-802Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T01-27-20-942Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T01-35-34-520Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T01-38-05-437Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T01-42-13-110Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T02-23-25-087Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T03-01-09-958Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T03-22-52-687Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T03-32-31-688Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T03-49-46-496Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T04-13-37-602Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T04-15-01-218Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T04-23-24-166Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T04-29-03-388Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T04-37-53-789Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T05-00-06-348Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T05-09-46-082Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T05-23-22-740Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T05-25-53-704Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T05-40-35-958Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T05-46-39-343Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T05-50-33-141Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T05-55-46-526Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T06-09-18-457Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T06-21-00-166Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T06-26-43-505Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T06-32-25-987Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T06-50-32-608Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T07-10-11-880Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T07-20-33-818Z_8041307210_strategist.md
|   |   |-- 2026-02-28T07-28-15-245Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T14-45-59-166Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T14-47-49-356Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T14-49-31-249Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T20-29-04-775Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T20-41-30-040Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T20-47-35-299Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T20-56-08-934Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T20-57-49-974Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T21-09-16-097Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T21-30-43-018Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T21-40-48-017Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T21-46-25-999Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T21-55-34-348Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T22-10-19-316Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T22-11-48-417Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T22-14-09-057Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T22-31-59-671Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T22-59-41-287Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T23-03-43-637Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T23-04-55-594Z_report-test-chat_strategist.md
|   |   |-- 2026-02-28T23-19-23-568Z_8041307210_strategist.md
|   |   |-- 2026-02-28T23-47-01-427Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T00-29-56-896Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T01-22-46-615Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T02-18-04-654Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T02-32-55-448Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T03-04-22-215Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T03-34-07-616Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T03-34-49-155Z_8041307210_strategist.md
|   |   |-- 2026-03-01T03-40-03-759Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T04-14-13-577Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T06-34-41-024Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T07-40-49-296Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T07-46-21-275Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T08-44-22-196Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T08-47-21-613Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T09-04-07-291Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T09-06-00-058Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T09-08-54-387Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T13-40-02-351Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T13-52-04-159Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T17-04-11-769Z_github_sync_audit.json
|   |   |-- 2026-03-01T17-52-46-739Z_github_sync_audit.json
|   |   |-- 2026-03-01T18-37-21-777Z_8041307210_strategist.md
|   |   |-- 2026-03-01T18-43-28-920Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T18-51-47-013Z_github_sync_audit.json
|   |   |-- 2026-03-01T18-55-25-391Z_github_sync_audit.json
|   |   |-- 2026-03-01T19-29-40-648Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T20-09-09-238Z_8041307210_strategist.md
|   |   |-- 2026-03-01T21-16-33-266Z_report-test-chat_strategist.md
|   |   |-- 2026-03-01T21-29-57-226Z_report-test-chat_strategist.md
|   |   |-- 2026-03-02T03-25-23-740Z_report-test-chat_strategist.md
|   |   |-- 2026-03-02T15-15-36-360Z_report-test-chat_strategist.md
|   |   |-- 2026-03-02T16-51-39-135Z_report-test-chat_strategist.md
|   |   |-- 2026-03-02T16-59-53-444Z_report-test-chat_strategist.md
|   |   |-- 2026-03-02T22-40-17-797Z_report-test-chat_strategist.md
|   |   |-- 2026-03-02T22-51-23-407Z_report-test-chat_strategist.md
|   |   |-- 2026-03-02T23-06-37-994Z_report-test-chat_strategist.md
|   |   |-- 2026-03-03T00-08-08-371Z_report-test-chat_strategist.md
|   |   |-- 2026-03-03T00-32-48-989Z_report-test-chat_strategist.md
|   |   |-- 2026-03-03T00-45-19-110Z_report-test-chat_strategist.md
|   |   |-- 2026-03-03T00-46-09-252Z_report-test-chat_strategist.md
|   |   |-- 2026-03-03T01-26-46-737Z_8041307210_strategist.md
|   |   |-- 2026-03-03T01-45-53-997Z_report-test-chat_strategist.md
|   |   |-- 2026-03-03T03-02-58-473Z_report-test-chat_strategist.md
|   |   |-- 2026-03-03T03-05-59-820Z_report-test-chat_strategist.md
|   |   |-- 2026-03-03T04-03-54-837Z_report-test-chat_strategist.md
|   |   |-- 2026-03-03T06-19-32-181Z_report-test-chat_strategist.md
|   |   |-- 2026-03-03T06-33-10-625Z_report-test-chat_strategist.md
|   |   |-- 2026-03-04T23-36-59-746Z_report-test-chat_strategist.md
|   |   |-- 2026-03-04T23-39-05-155Z_report-test-chat_strategist.md
|   |   |-- 2026-03-05T04-03-39-479Z_report-test-chat_strategist.md
|   |   |-- 2026-03-05T04-04-46-126Z_report-test-chat_strategist.md
|   |   |-- 2026-03-05T04-10-08-404Z_report-test-chat_strategist.md
|   |   |-- 2026-03-05T04-14-34-254Z_report-test-chat_strategist.md
|   |   |-- article_2025654698590748672.html
|   |   |-- fetch_fx.js
|   |   |-- fetch_x_full.js
|   |   |-- fetch_x_links.js
|   |   |-- x_links_raw.json
|   |   `-- x_main.js
|   |-- workspaces/
|   |   |-- 8041307210/
|   |   |   |-- _intent/
|   |   |   |   `-- NORTH_STAR.md
|   |   |   |-- coder/
|   |   |   |   |-- AGENTS.md
|   |   |   |   |-- IDENTITY.md
|   |   |   |   |-- SOUL.md
|   |   |   |   `-- USER.md
|   |   |   |-- execution/
|   |   |   |   |-- AGENTS.md
|   |   |   |   |-- IDENTITY.md
|   |   |   |   |-- SOUL.md
|   |   |   |   `-- USER.md
|   |   |   |-- research/
|   |   |   |   |-- AGENTS.md
|   |   |   |   |-- IDENTITY.md
|   |   |   |   |-- SOUL.md
|   |   |   |   `-- USER.md
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- retry-probe-chat/
|   |   |   |-- _intent/
|   |   |   |   `-- NORTH_STAR.md
|   |   |   `-- coder/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772236701602/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772236731955/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772236772766/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772237402397/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772239010200/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772239341323/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772239846934/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772241372043/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772241469575/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772242009338/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772242040489/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772242534042/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772242684980/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772242932651/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772245404621/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772247669447/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772248972212/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772249551224/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772250586003/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772252017128/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772252100686/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772252603694/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772252942925/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772253473328/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772254805906/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772255385626/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772256202297/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772256353209/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772257235430/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772257598868/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772257832648/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772258146008/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772258957951/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772259659608/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772260002968/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772260345501/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772261432129/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772262611227/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772263694785/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772289958701/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772290068892/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772290170783/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772310544234/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772311289574/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772311654806/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772312168453/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772312269480/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772312955584/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772314242416/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772314847493/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772315185496/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772315733856/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772316618845/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772316707951/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772316848577/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772317919173/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772319580792/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772319823175/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772319895114/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772322420873/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772324996409/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772328166053/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772331484135/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772332374956/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772334261686/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772336047128/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772336403260/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772338453084/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772346880430/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772350848791/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772351180788/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772354661683/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772354841009/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772355846785/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772355959535/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772356133858/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772372401835/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772373123696/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772390608409/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772393380124/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772399792735/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772400596701/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772421923229/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772464535617/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772470298284/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772470792412/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772491217027/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772491882652/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772492797116/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772496487433/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772497968269/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772498718383/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772498768457/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772502353157/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772506977715/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772507158980/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772510634005/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772518771435/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772519589896/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772667418743/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772667544268/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772683418505/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772683485265/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   |-- test-chat-1772683807439/
|   |   |   `-- strategist/
|   |   |       |-- AGENTS.md
|   |   |       |-- IDENTITY.md
|   |   |       |-- SOUL.md
|   |   |       `-- USER.md
|   |   `-- test-chat-1772684073343/
|   |       `-- strategist/
|   |           |-- AGENTS.md
|   |           |-- IDENTITY.md
|   |           |-- SOUL.md
|   |           `-- USER.md
|   |-- _ui_snapshot.html
|   |-- db.sqlite
|   |-- db.sqlite-shm
|   `-- db.sqlite-wal
|-- AGENTS.md
|-- CONTRIBUTING.md
|-- mcp.config.json
|-- memory.md
|-- package-lock.json
|-- package.json
|-- README.md
|-- SECURITY.md
|-- skills.md
|-- tmp_codex_write_probe_danger_1772496002.txt
|-- tmp_codex_write_probe_dfa_1772496114.txt
|-- tmp_manual_write_probe.txt
|-- tmp_runner_retry_probe_1772496515824.txt
|-- tmp_storyboard_0.jpg
|-- tmp_ui_script.js
`-- tsconfig.json
```

## KEY CONSTRAINTS

_No selected items from this evidence._

## OPEN PROBLEMS

_No selected items from this evidence._

## BACKLOG

1. Complete unresolved runbook+scheduler package: finalize runbook sections, add idempotent scheduler toggle/verification path, add scheduler gating tests, and provide full build/test/runtime evidence on feature branch.
2. Execute Mission Control Phase 2 UI polish (paint/fetch ordering, summary call caching, keyboard navigation refinements) to improve current UX quality.
3. Document TRACKER_TASKS/TACKER_UPDATES directive usage in README/AGENTS so contributors and agents can reliably use agent-created follow-up tasks.
4. Produce a Mission Control-style Command Center redesign plan that includes only workspace-relevant modules/options and excludes irrelevant areas (e.g., calendar).

## RELATED

- [[projects/codexclaw/recent|Codexclaw Recent]]
- [[projects/codexclaw/rules|Codexclaw Rules]]
- [[global/user-rules|Global User Rules]]
