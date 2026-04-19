---
type: project-memory
project: codexclaw
updated: 2026-04-19T04:21:45.640467Z
tags: [project/codexclaw, memory]
---

# 🧠 Codexclaw - Project Memory

## PURPOSE

- Project context: Decisions locked: - Style: **Mission Control-inspired hybrid** (not a clone) - Navigation: **Left rail + content** - Priority modules: **Board, Projects, Memory, Docs** - Ops/Config location: **System tab** - `Future` tab: **Remove now** - Delivery: **Two phases** Video-derived module relevance (from.
- Project context: I've requested this (image, last msg from me) and the system got an error which is stored here: store/reports/2026-03-01T18-37-21-777Z_8041307210_strategist.md Can you investigate and fix it please.
- Project context: Treat the project as a quant-research-oriented agent system.

## CORE COMPONENTS

- Use this architecture context: the project appears to organize work around multiple agent roles, including strategist, research, execution, coder, and persona-oriented components, with references to chat and agent source files.
- Use this architecture context: the project references local memory storage components, including AGENTS.md, SOUL.md, IDENTITY.md, USER.md, and SQLite memory tables, as part of its agent setup.

## CURRENT ARCHITECTURE

- Use this architecture context: the intended memory backend is PostgreSQL with pgvector as the source of truth, with both MCP and REST interfaces exposed.
- Use this architecture context: i need to have good solutions/architecture provided by the team.
- Use this architecture context: the project appears to have an established multi-agent setup centered on strategist, research, execution, and coder roles.
- Use this architecture context: the project includes a quant research agent role as part of the agent lineup.
- Use this architecture context: the project instructions reference CodexClaw Pro Agents and point to agent-related source files under src/agent.ts, src/agents/runner.ts, and src/bot.ts.
- Use this architecture context: the repository includes CodexClaw agent instructions and local memory storage references, including SQLite tables for memory chunks and memory facts.

## DESIGN PRINCIPLES

- No stable design principles extracted yet.

## KEY CONSTRAINTS

- Respect this constraint: for CodexClaw UI work, reuse the project’s designated skin source of truth rather than inventing a new visual system.
- Respect this constraint: run pwd command and then reply only with the exact working directory path from command output.
- Respect this constraint: storage cost is expected to be the main expense driver for this system.
- Respect this constraint: this is what I want to know before we talk about implementation: 1) Why use slack is input source only.
- Respect this constraint: treat CodexClaw as an advisory-only trading system: it may suggest closes or adjustments, but it must not place trades directly.
- Respect this constraint: treat GitHub Project sync rate-limit warnings as non-blocking for core tracker behavior; do not surface them as if the main system is failing.

## OPEN PROBLEMS

- Respect this constraint: one question, how can I enforce the agent to open only one branch and make all the changes in it, instead of opening multiple branches every time I ask for something.

## RELATED

- [[Codexclaw Recent]]
- [[Codexclaw Rules]]
- [[Global User Rules]]
