---
type: project-memory
project: ai-trader
updated: 2026-04-19T13:07:41.077730Z
tags: [project/ai-trader, memory]
---

# 🧠 Ai Trader - Project Memory

## PURPOSE

- Build a fully autonomous deterministic trading system.
- Deterministic autonomous trading system scaffold with TrendSpider webhook ingest, DB-backed job queue, SetupSpec builder + scoring, Options selection engine, Approval / auto execution flow, Chart snapshots attached to each trade card trigger, IBKR execution adapter, Tax reserve + wash sale protection.
- The agent told me it does not have dire file system access.

## CORE COMPONENTS

- the trading system includes a swing-cycle workflow with a morning plan, entry windows, end-of-day review/report, and a daily backtest pass.
- This system orchestrates multiple specialist agents using Codex CLI as the reasoning engine.

## CURRENT ARCHITECTURE

_None currently extracted._

## DESIGN PRINCIPLES

_None currently extracted._

## KEY CONSTRAINTS

- Assume a single-user deployment and optimize the memory system for the owner and their coding agents.
- cards only go to card history page after an approve/reject decision was made.
- global kill switch blocks trading.
- taxable only: strict wash-sale blocks by symbol and by contract for 31 days.
- trading disabled when trust score reaches 0.

## OPEN PROBLEMS

_None currently extracted._

## RELATED

- [[Ai Trader Recent]]
- [[Ai Trader Rules]]
- [[Global User Rules]]
