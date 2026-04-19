---
type: project-memory
project: ai-trader
updated: 2026-04-19T04:21:45.619281Z
tags: [project/ai-trader, memory]
---

# 🧠 Ai Trader - Project Memory

## PURPOSE

- Project context: Build a fully autonomous deterministic trading system.
- Project context: Deterministic autonomous trading system scaffold with TrendSpider webhook ingest, DB-backed job queue, SetupSpec builder + scoring, Options selection engine, Approval / auto execution flow, Chart snapshots attached to each trade card trigger, IBKR execution adapter, Tax reserve + wash sale protection.
- Project context: Every time you make a change, think about the system as new.

## CORE COMPONENTS

- Project context: This system orchestrates multiple specialist agents using Codex CLI as the reasoning engine.
- Respect this constraint: the IBKR adapter should be implemented without requiring live IBKR accounts yet, so integration can proceed before credentials are available.
- Project context: The user profile indicates a senior software engineer background, which may justify concise, implementation-oriented technical communication.

## CURRENT ARCHITECTURE

- Use this architecture context: add a database link between one trade card and one or more alert IDs so backend agents can associate generated cards with source signals.
- Use this architecture context: build the trading system around a webhook-driven alert intake, queued processing, scoring, options selection, approval or auto-execution, broker execution, risk and tax handling, and performance tracking.
- Use this architecture context: if one alert fans out to multiple trade cards, or one card has multiple input alerts, the lineage graph should show all related nodes without becoming cluttered.
- Use this architecture context: keep the alert-ingress layer resilient by authenticating incoming alerts, deduplicating repeats, and placing events onto a queue instead of trading directly inside the webhook handler.
- Use this architecture context: keep the lineage graph aligned so summary sits with the intent level and closed positions appear after opened positions.
- Use this architecture context: keep the lineage section docked as a bottom bar when minimized, labeled Lineage, and do not show pin, expand, or close controls in that minimized state.

## DESIGN PRINCIPLES

- Use this architecture context: the system is designed as a deterministic autonomous trading scaffold with webhook ingestion, queued jobs, setup scoring, options selection, approval or auto-execution, broker execution, performance tracking, and a daily swing-cycle workflow.

## KEY CONSTRAINTS

- Assume a single-user deployment and optimize the memory system for the owner and their coding agents.
- Respect this constraint: the trading scaffold enforces hard safety limits: minimum reward-to-risk, risk-cap compliance, a global trading stop, trust-score-based shutdown, and wash-sale restrictions for taxable accounts only.
- For wash-sale management, preserve tax-window context around when positions should be closed, held, or reopened.
- Respect this constraint: allow nodes in the lineage graph to be repositioned, and prevent overlapping or overly spaced layouts when viewing lineage.
- Respect this constraint: audit the mocked lineage data thoroughly and fix missing or inconsistent cards before considering the screen complete.
- Respect this constraint: avoid adding event markers to the performance chart because they make the visualization feel crowded.

## OPEN PROBLEMS

- Use this architecture context: treat the lineage graph as a chronological chain of distinct trading events, including trade card, open intent, open order, open fill, position opened, close intent, close order, close fill, position closed, and tax lot when applicable.
- Respect this constraint: one trade card should only have one open intent.
- Respect this constraint: order intent section should show only order intents open, idependent of the date they were post there.

## RELATED

- [[Ai Trader Recent]]
- [[Ai Trader Rules]]
- [[Global User Rules]]
