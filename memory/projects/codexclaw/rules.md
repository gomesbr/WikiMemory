---
type: project-rules
project: codexclaw
updated: 2026-04-19T13:07:41.438395Z
tags: [project/codexclaw, rules]
---

# ⚙️ Codexclaw - Project Rules

## ALWAYS DO

_None currently extracted._

## NEVER DO

- Do not force a fixed number of backlog stories; let the strategist create as many items as needed from the underlying code requirements.

## CONDITIONAL RULES

- When developing a new Codexclaw version that is not yet in production use, do not preserve backward compatibility with the previous version by default. Treat the new version as a clean system unless the user explicitly asks for migration or compatibility support.
- the primary chat agent should behave as a natural-language strategist that routes requests to the other agents, rather than replying with rigid scripted text. It should gather researcher output and use it to form trade ideas. Only the coder should use Codex; the other agents should use GPT-5.
- When the user asks for repository changes, commit and push without asking again unless credentials or conflicts block the action.
- after the user approves pull requests, the coder should merge them automatically without requiring extra user intervention.
- all agents should be allowed to create and update tracker tasks when they discover extra work, while the strategist remains the primary delegator.
- add periodic check-ins or heartbeat reminders so agents revisit the tracker for unfinished assignments after idle time or interruptions such as restarts.
- the main interface should be a single command-center page that brings together the tracker, configuration, and future tools in one place.
- keep task creation granular so a simple request does not explode into many separate tracker items.
- if the current chat becomes too slow or heavy, continue in a new chat while preserving context rather than restarting the task.
- the command center redesign should follow the Mission Control-inspired plan: left navigation rail, content area, and priority modules centered on Board, Projects, Memory, and Docs, with Ops/Config moved under System and the Future tab removed.
- the CodexClaw chat experience should avoid overly mechanical responses and preserve free-form conversation behavior.
- the bot should route user requests to the researcher agent when appropriate instead of answering everything directly from the main chat path.

## PROMOTED RULES (EXPLICIT)

- 40 explicit rule(s) are listed above by behavior bucket.

## INFERRED RULES

_None currently extracted._

## SCOPE NOTES

- Applies only to this project.

## RELATED

- [[Codexclaw Recent]]
- [[Codexclaw Rules]]
