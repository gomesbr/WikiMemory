---
type: project-memory
project: codexclaw
updated: 2026-04-19T13:07:41.349626Z
tags: [project/codexclaw, memory]
---

# 🧠 Codexclaw - Project Memory

## PURPOSE

- Decisions locked: - Style: **Mission Control-inspired hybrid** (not a clone) - Navigation: **Left rail + content** - Priority modules: **Board, Projects, Memory, Docs** - Ops/Config location: **System tab** - `Future` tab: **Remove now** - Delivery: **Two phases** Video-derived module relevance (from.
- The CodexClaw role includes maintaining dashboards and platform code, improving reliability and observability, and giving implementation-level guidance for requested build tasks.

## CORE COMPONENTS

- use PostgreSQL with pgvector as the source of truth, and expose both MCP and REST interfaces for the memory system.
- codexClaw stores memory in SQLite tables named memory_chunks and memory_f, and related agent instructions reference AGENTS.md, SOUL.md, IDENTITY.md, USER.md, and store/memory/ as part of the working setup.
- the codebase references agent entry points in src/agent.ts, src/agents/runner.ts, and src/bot.ts; prioritize those files when tracing agent behavior or making changes to the agent pipeline.
- the CodexClaw agent setup references multiple roles and local instruction files, including AGENTS.md, SOUL.md, IDENTITY.md, USER.md, and memory storage under store/memory, with SQLite-backed memory tables.
- the project uses a quant research agent as one of its defined roles.
- the project’s agent setup references CodexClaw Pro Agents and ties the strategist, research, execution, coder, and persona components to the agent files under src/agent.ts, src/agents/runner.ts, and src/bot.ts.

## CURRENT ARCHITECTURE

- use the repository's multi-role agent setup, with strategist, research, execution, and coder responsibilities coordinated through the agent runtime files in the project.
- run pwd command and then reply only with the exact working directory path from command output.
- the near-term deployment target is Windows, with a move to a Mac Studio planned later; design storage and runtime assumptions accordingly.

## DESIGN PRINCIPLES

_None currently extracted._

## KEY CONSTRAINTS

- the working context for this project is a Windows machine using PowerShell in the CodexClaw repository path shown in the instructions.
- only focus on the menus and options that are useful here.
- only split into additional stories/follow-up tasks when clearly necessary.
- when remote repository access is needed, the user can provide the account details or authentication setup so the agent can continue repository and branch-protection work.

## OPEN PROBLEMS

_None currently extracted._

## RELATED

- [[Codexclaw Recent]]
- [[Codexclaw Rules]]
- [[Global User Rules]]
