---
type: project-memory
project: codexclaw
updated: 2026-04-19T04:35:36.095048Z
tags: [project/codexclaw, memory]
---

# 🧠 Codexclaw - Project Memory

## PURPOSE

- Decisions locked: - Style: **Mission Control-inspired hybrid** (not a clone) - Navigation: **Left rail + content** - Priority modules: **Board, Projects, Memory, Docs** - Ops/Config location: **System tab** - `Future` tab: **Remove now** - Delivery: **Two phases** Video-derived module relevance (from.
- I've requested this (image, last msg from me) and the system got an error which is stored here: store/reports/2026-03-01T18-37-21-777Z_8041307210_strategist.md Can you investigate and fix it please.
- Treat the project as a quant-research-oriented agent system.

## CORE COMPONENTS

- the project appears to organize work around multiple agent roles, including strategist, research, execution, coder, and persona-oriented components, with references to chat and agent source files.
- the project references local memory storage components, including AGENTS.md, SOUL.md, IDENTITY.md, USER.md, and SQLite memory tables, as part of its agent setup.

## CURRENT ARCHITECTURE

- the intended memory backend is PostgreSQL with pgvector as the source of truth, with both MCP and REST interfaces exposed.
- the project appears to have an established multi-agent setup centered on strategist, research, execution, and coder roles.
- the project includes a quant research agent role as part of the agent lineup.
- the project instructions reference CodexClaw Pro Agents and point to agent-related source files under src/agent.ts, src/agents/runner.ts, and src/bot.ts.
- the repository includes CodexClaw agent instructions and local memory storage references, including SQLite tables for memory chunks and memory facts.
- the strategist is intended to be the primary conversational agent, routing natural-language requests to the other agents and combining researcher output into trade ideas.

## DESIGN PRINCIPLES

_None currently extracted._

## KEY CONSTRAINTS

- for CodexClaw UI work, reuse the project’s designated skin source of truth rather than inventing a new visual system.
- run pwd command and then reply only with the exact working directory path from command output.
- storage cost is expected to be the main expense driver for this system.
- this is what I want to know before we talk about implementation: 1) Why use slack is input source only.
- treat CodexClaw as an advisory-only trading system: it may suggest closes or adjustments, but it must not place trades directly.
- treat remote project board sync rate-limit warnings as non-blocking for core tracker behavior; do not surface them as if the main system is failing.

## OPEN PROBLEMS

- one question, how can I enforce the agent to open only one branch and make all the changes in it, instead of opening multiple branches every time I ask for something.

## RELATED

- [[Codexclaw Recent]]
- [[Codexclaw Rules]]
- [[Global User Rules]]
