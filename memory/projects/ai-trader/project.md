---
type: project-memory
project: ai-trader
updated: 2026-04-20T01:19:51.481153Z
tags: [project/ai-trader, memory]
---

# Ai Trader - Project Memory

## PURPOSE

- AITrader is a deterministic, high-trust swing-trading operations platform: it ingests TrendSpider alerts, builds/scorers setup specs, selects options, routes trades through approval-first or optional auto-execution, executes via broker adapter (mock-supported), and tracks risk/tax/wash-sale/performance/trust with replayability and auditability through a web console.

## CORE COMPONENTS

_No selected items from this evidence._

## CURRENT ARCHITECTURE

- Operational lifecycle follows a swing cycle: collect/score intraday triggers, prepare morning execution/closure plan, execute in configured windows, allow emergency exits, then run EOD review and reporting for next-day prep.
- Strategy management is per-account via Strategy Lab profile records; paper accounts may have multiple active strategies while Roth/taxable accounts are constrained to one active strategy.
- Approval UI exposes machine-facing `/agent/v1/*` endpoints with bearer-token auth and idempotency requirements for mutating operations.
- Architecture is a TypeScript pnpm-workspace monorepo with PostgreSQL and DB-backed queue patterns, organized into apps (ingest_service, worker, execution_service, approval_ui) plus shared libs (common, marketdata, signals, options/risk/tax/wash/performance engines, broker, charts, backtest) and SQL migrations enforcing lifecycle/risk invariants.

## DIRECTORY TREE

`cd C:\Users\Fabio\Cursor AI projects\Projects\AITrader; tree /F /A`

```text
AITrader/
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
|-- apps/
|   |-- approval_ui/
|   |   |-- src/
|   |   |   |-- public/
|   |   |   |   |-- app.js
|   |   |   |   |-- index.html
|   |   |   |   `-- styles.css
|   |   |   |-- agent_trade_card_service.ts
|   |   |   |-- index.ts
|   |   |   |-- lineage.ts
|   |   |   `-- openbrain.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   |-- execution_service/
|   |   |-- src/
|   |   |   `-- index.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   |-- ingest_service/
|   |   |-- src/
|   |   |   `-- index.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   `-- worker/
|       |-- src/
|       |   `-- index.ts
|       |-- package.json
|       `-- tsconfig.json
|-- config/
|   |-- incident_penalties_options.json
|   |-- options_constraints_aggressive_swing.json
|   |-- strategy_v1.json
|   `-- swing_risk_policy.json
|-- docs/
|   |-- reports/
|   |   `-- aitrader_branches/
|   |       |-- branches_list_origin.txt
|   |       |-- branches_report.md
|   |       `-- evidence.txt
|   |-- api_endpoints.md
|   |-- architecture.md
|   |-- conversation_transcript.md
|   |-- conversation_transcript_verbatim.md
|   |-- deployment_options.md
|   |-- GITHUB_SETUP.md
|   |-- IDEAS_PARKING_LOT_2026-03.md
|   |-- incident_trust_model.md
|   |-- strategy_v1_rationale.md
|   `-- swing_workflow.md
|-- libs/
|   |-- backtest/
|   |   |-- src/
|   |   |   `-- index.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   |-- broker_ibkr/
|   |   |-- src/
|   |   |   `-- index.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   |-- charts/
|   |   |-- src/
|   |   |   `-- index.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   |-- common/
|   |   |-- src/
|   |   |   |-- config.ts
|   |   |   |-- db.ts
|   |   |   |-- hashing.ts
|   |   |   |-- incidents.ts
|   |   |   |-- index.ts
|   |   |   |-- pg-shim.d.ts
|   |   |   |-- queue.ts
|   |   |   |-- safety.ts
|   |   |   |-- schemas.ts
|   |   |   |-- settings.ts
|   |   |   |-- time.ts
|   |   |   `-- types.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   |-- marketdata/
|   |   |-- src/
|   |   |   `-- index.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   |-- options_engine/
|   |   |-- src/
|   |   |   `-- index.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   |-- performance_engine/
|   |   |-- src/
|   |   |   `-- index.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   |-- risk_engine/
|   |   |-- src/
|   |   |   `-- index.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   |-- signals/
|   |   |-- src/
|   |   |   `-- index.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   |-- tax_engine/
|   |   |-- src/
|   |   |   `-- index.ts
|   |   |-- package.json
|   |   `-- tsconfig.json
|   `-- wash_sale_engine/
|       |-- src/
|       |   `-- index.ts
|       |-- package.json
|       `-- tsconfig.json
|-- skills/
|   `-- aitrader-agent-ops/
|       |-- assets/
|       |   `-- schemas/
|       |       |-- candidate_output.json
|       |       `-- trade_card_create_payload.json
|       |-- references/
|       |   |-- api_contracts.md
|       |   |-- daily_runbook.md
|       |   `-- prompt_catalog.md
|       |-- contracts.manifest.json
|       `-- SKILL.md
|-- sql/
|   |-- migrations/
|   |   |-- 001_init.sql
|   |   |-- 002_seed_example.sql
|   |   |-- 003_swing_workflow.sql
|   |   |-- 004_console_audit.sql
|   |   |-- 005_runtime_settings.sql
|   |   |-- 006_incident_penalty_custom.sql
|   |   |-- 007_invalid_kill_switch_category.sql
|   |   |-- 008_strategy_profiles.sql
|   |   |-- 009_seed_linked_scenario.sql
|   |   |-- 010_setup_alert_links.sql
|   |   |-- 011_seed_setup_alert_links.sql
|   |   |-- 012_lineage_seed_consistency.sql
|   |   |-- 013_lineage_backfill_full_audit.sql
|   |   |-- 014_align_mock_financial_values.sql
|   |   |-- 015_reconcile_lineage_lifecycle.sql
|   |   |-- 016_fix_lifecycle_integrity.sql
|   |   |-- 017_enforce_lifecycle_hard_rules.sql
|   |   |-- 018_position_amendments_and_roll_seed.sql
|   |   |-- 019_one_open_intent_per_setup.sql
|   |   |-- 020_prevent_reactivation_of_final_statuses.sql
|   |   |-- 021_lineage_full_audit_repair_and_second_roll.sql
|   |   |-- 022_cleanup_filled_orders_without_fills.sql
|   |   |-- 023_lineage_strict_intent_scope_and_cleanup.sql
|   |   |-- 024_rehydrate_missing_roll_open_intents.sql
|   |   |-- 025_hard_link_trade_lifecycle.sql
|   |   |-- 026_one_close_intent_per_setup.sql
|   |   |-- 027_seasonal_only_wash_policy.sql
|   |   |-- 028_agent_api_and_marketdata_foundation.sql
|   |   |-- 029_agent_execution_position_actions.sql
|   |   `-- README.md
|   `-- runbooks/
|       |-- pre_real_cutover_apply.sql
|       `-- pre_real_cutover_dry_run.sql
|-- tests/
|   |-- options_engine.test.ts
|   |-- package.json
|   |-- risk_engine.test.ts
|   |-- tax_wash_sale.test.ts
|   `-- tsconfig.json
|-- approval_ui.dev.log
|-- approval_ui.direct.log
|-- CONTRIBUTING.md
|-- docker-compose.yml
|-- package.json
|-- pnpm-lock.yaml
|-- pnpm-workspace.yaml
|-- README.md
|-- SECURITY.md
|-- start-approval.cmd
`-- tsconfig.base.json
```

## KEY CONSTRAINTS

_No selected items from this evidence._

## OPEN PROBLEMS

_No selected items from this evidence._

## BACKLOG

1. Ensure representative deterministic mock-data fallback across all console sections/subsections so layouts remain fully populated when live data is empty (real data takes precedence).
2. Implement real market-data ingestion (provider evaluation + integration), replacing current deterministic/mock-only flow for production use.
3. Add chart screenshot/preview with visible setup annotations to each trade card (not text-only metadata).

## RELATED

- [[projects/ai-trader/recent|Ai Trader Recent]]
- [[projects/ai-trader/rules|Ai Trader Rules]]
- [[global/user-rules|Global User Rules]]
