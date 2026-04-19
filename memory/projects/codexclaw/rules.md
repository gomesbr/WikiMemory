---
type: project-rules
project: codexclaw
updated: 2026-04-19T04:35:36.122248Z
tags: [project/codexclaw, rules]
---

# ⚙️ Codexclaw - Project Rules

## ALWAYS DO

_None currently extracted._

## NEVER DO

_None currently extracted._

## CONDITIONAL RULES

- add periodic check-ins or heartbeats so agents are reminded to review the tracker for unfinished assignments after idle periods or restarts.
- the user prefers a free-form conversational agent rather than rigid scripted replies.
- only the coder agent should use Codex; the other agents should use GPT-5.
- When the user asks for repository changes, commit and push without asking again unless credentials or conflicts block the action.
- limit the coder to opening at most one branch per day so review and merge work can be batched into a single daily approval cycle.
- after approval, the coder should merge pull requests automatically without requiring extra user involvement.
- add a tracker for coder work that shows backlog, in progress, blocked, and completed states in a simple visual board.
- persist the user's chat identifier so they do not need to re-enter it each time the app opens.
- keep the visual theme location discoverable for the coder agent so the user does not need to repeat where the shared skin lives.
- the strategist should interview the user to clarify vague requests before turning them into requirements.
- all agents should be able to create and manage tracker items when they discover extra work beyond the original plan.
- allow every agent to create and update its own tracker tasks, not just the strategist, so agents can handle extra work that emerges during execution.

## PROMOTED RULES (EXPLICIT)

- 21 explicit rule(s) are listed above by behavior bucket.

## INFERRED RULES

_None currently extracted._

## SCOPE NOTES

- Applies only to this project.

## RELATED

- [[Codexclaw Recent]]
- [[Codexclaw Rules]]
