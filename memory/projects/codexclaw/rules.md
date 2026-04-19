---
type: project-rules
project: codexclaw
updated: 2026-04-19T04:21:45.647759Z
tags: [project/codexclaw, rules]
---

# ⚙️ Codexclaw - Project Rules

## ALWAYS DO

- No always-do rules selected yet.

## NEVER DO

- No never-do rules selected yet.

## CONDITIONAL RULES

- Follow this operating rule: add a tracker for coder work that shows backlog, in progress, blocked, and completed states in a simple visual board.
- Follow this operating rule: add periodic check-ins or heartbeats so agents are reminded to review the tracker for unfinished assignments after idle periods or restarts.
- Follow this operating rule: after approval, the coder should merge pull requests automatically without requiring extra user involvement.
- Follow this operating rule: all agents should be able to create and manage tracker items when they discover extra work beyond the original plan.
- Follow this operating rule: allow every agent to create and update its own tracker tasks, not just the strategist, so agents can handle extra work that emerges during execution.
- Follow this operating rule: apply the CodexClaw UI skin standard by default and reuse the shared source-of-truth skin for CodexClaw UI work.
- Follow this operating rule: configure branch protection and agent behavior so the coding agent follows the repository rules automatically.
- Follow this operating rule: default to acting as a senior software engineer for dashboard and platform work, with emphasis on reliability, observability, and developer workflow improvements.
- Follow this operating rule: default to completing work as one tracker item; only break it into additional stories or follow-up tasks when the scope clearly requires it.
- Follow this operating rule: default to solving assigned work as one tracker item, and only split into extra stories when the scope clearly requires it.
- Follow this operating rule: follow the CodexClaw Pro Agents instructions in the repository's AGENTS.md file for this workspace.
- Follow this operating rule: follow the senior-engineer operating style for CodexClaw work: maintain dashboards and platform code, improve reliability and observability, support developer workflows, and provide implementation plans or code-level guidance for build tasks.
- Follow this operating rule: for CodexClaw UI work, follow the shared visual standard referenced by the project instructions so interface changes stay consistent across apps.
- Follow this operating rule: for this project, prioritize solutions and architecture quality from the team, not just isolated task completion.
- Follow this operating rule: keep a consistent visual language across CodexClaw apps when making UI changes.
- Follow this operating rule: keep the visual theme location discoverable for the coder agent so the user does not need to repeat where the shared skin lives.
- Follow this operating rule: limit the coder to opening at most one branch per day so review and merge work can be batched into a single daily approval cycle.
- Follow this operating rule: only the coder agent should use Codex; the other agents should use GPT-5.
- Follow this operating rule: persist the user's chat identifier so they do not need to re-enter it each time the app opens.
- Follow this operating rule: prefer completing the assigned work as one tracker item; only break it into extra stories or follow-up tasks when there is a clear need.
- Follow this operating rule: prefer finishing the assigned work as one tracker item by default; only split into extra stories or follow-up tasks when there is a clear need.
- Follow this operating rule: prefer implementation plans or code-level guidance for build tasks, and keep UI language consistent across applications.
- Follow this operating rule: provide a lightweight place to store large analysis outputs, and surface only a concise summary plus a pointer to the full result location.
- Follow this operating rule: show every status lane even when it has no items, so the board layout remains visible and predictable.
- Follow this operating rule: the CodexClaw workspace includes agent-specific instructions and memory storage files, plus SQLite-backed memory tables; follow the repository’s agent docs when operating in this project.
- Follow this operating rule: the agent should route requests to the researcher when the user asks for research-oriented help instead of staying in a generic response mode.
- Follow this operating rule: the assigned implementing agent should own each task through its phases until completion, while the strategist stays available for user-facing coordination and delegates routine work to coder and researcher unless the work is truly strategic.
- Follow this operating rule: the layout should split the main task area and the specialist area evenly across the screen, with separate vertical scrolling inside each section.
- Follow this operating rule: the memory system should support bulk importing large amounts of prompt history from multiple AI tools, not just Slack as an input source.
- Follow this operating rule: the page should combine tracker, configuration, and future tools into a single command-center style entry point.
- Follow this operating rule: the project should expose memory and skills files for agents so they can load persistent guidance and role-specific behavior after restart.
- Follow this operating rule: the project should include a mission-control scheduler view that groups scheduled jobs by project and shows each job’s name, cadence, purpose, and other helpful metadata.
- Follow this operating rule: the strategist role is explicitly emphasized in the project instructions and appears repeatedly, so planning-oriented behavior should be prioritized when operating in this repo.
- Follow this operating rule: the strategist should interview the user to clarify vague requests before turning them into requirements.
- Follow this operating rule: the tracker should be the shared system of record, and tasks or user stories should be split so the coder can take them one at a time.
- Follow this operating rule: the user does not want separate scrollbars for every vertical list; they want exactly two scrollbars total, one for the agent task section and one for the specialist section.
- Follow this operating rule: the user prefers a free-form conversational agent rather than rigid scripted replies.
- Follow this operating rule: the user wants a way to import conversation logs from ChatGPT and Grok into the memory system.
- Follow this operating rule: the user wants all identified epics for codexclaw implemented, but the agent should first verify whether any requested work is already present to avoid duplicating features.
- Follow this operating rule: the user wants the UI cards to stay compact so the full details are revealed only when clicked.
- Follow this operating rule: the user wants the agent to keep working on a single long-lived branch per project across multiple requests, rather than creating a new branch each time, and only open a PR when they explicitly authorize review and merge.
- Follow this operating rule: track every interaction that turns into work for any agent so the user has full visibility into all agent tasks.
- Follow this operating rule: treat the Chief Strategist role as the active persona when the conversation or instructions explicitly assign it.
- Follow this operating rule: treat the CodexClaw agent as a senior software engineer focused on dashboards, platform code, reliability, observability, and developer workflows; provide implementation plans or code-level guidance for build tasks.
- Follow this operating rule: treat the CodexClaw workspace as a multi-role setup with strategist, research, execution, and coder personas; keep supporting docs and memory data under the project’s store/memory area and SQLite memory tables.
- Follow this operating rule: treat the CodexClaw workspace as a senior-engineer environment: prioritize reliability, observability, and developer workflow improvements; provide implementation plans or code-level guidance for build tasks; keep UI language consistent across apps; and prefer durable root-cause fixes with regression coverage over temporary patches.
- Follow this operating rule: treat the researcher, execution, strategist, and coder agents as part of the same review pipeline, with background filtering so only approved ideas move forward.
- Follow this operating rule: treat the user as a senior software engineer for CodexClaw work: focus on dashboards, platform code, reliability, observability, and developer workflow improvements.
- Follow this operating rule: use a lightweight background process to screen agent outputs for mistakes, contradictions, and weak reasoning, since the user cares about preventing costly errors rather than reading full discussion traces.
- Follow this operating rule: use a risk classification step to separate high-risk from low-risk items before review or execution.
- Follow this operating rule: use a tracker as the central place for agent work visibility, with statuses such as backlog, in progress, blocked/pending, and done.
- Follow this operating rule: use first-principles debugging: find the underlying cause, implement a lasting fix, and add regression coverage instead of applying a narrow local workaround.
- Follow this operating rule: use root-cause analysis and durable fixes with regression coverage instead of narrow local patches.
- Follow this operating rule: use root-cause analysis and durable fixes, and include regression coverage instead of applying a narrow local patch.
- Follow this operating rule: use the Chief Strategist role when operating in this project context.
- Follow this operating rule: use the CodexClaw agent roles defined in the project instructions: strategist, research, and execution personas are expected, with coding handled through the specified agent implementation path.
- Follow this operating rule: use the repository’s AGENTS.md guidance as the active operating contract for CodexClaw work in this workspace.
- Follow this operating rule: use the shared UI skin as the default visual source of truth for CodexClaw UI work, and keep the design language consistent across apps.
- Follow this operating rule: when an agent marks a task blocked, it must include the blocker reason and immediately notify the strategist so the strategist can escalate to the user if needed.
- Follow this operating rule: when asked to build or change something, provide implementation plans or code-level guidance rather than only high-level advice.
- Follow this operating rule: when asked to proceed, implement the agreed plan rather than only discussing it.
- Follow this operating rule: when handling a task, keep it as one tracker item by default; only split into extra stories or follow-up tasks when there is a clear need.
- Follow this operating rule: when the user asks for a simple conversational reply, answer in a single friendly sentence and avoid formal structure.
- When the user asks for repository changes, commit and push without asking again unless credentials or conflicts block the action.
- When the user asks for repository changes, commit and push without asking again unless credentials or conflicts block the action.
- When the user asks for repository changes, commit and push without asking again unless credentials or conflicts block the action.

## PROMOTED RULES (EXPLICIT)

- 21 explicit rule(s) are listed above by behavior bucket.

## INFERRED RULES

- Follow this operating rule: apply the CodexClaw UI skin standard by default and reuse the shared source-of-truth skin for CodexClaw UI work. (confidence: strong; source_count: 21)
- Follow this operating rule: configure branch protection and agent behavior so the coding agent follows the repository rules automatically. (confidence: medium; source_count: 2)
- Follow this operating rule: default to acting as a senior software engineer for dashboard and platform work, with emphasis on reliability, observability, and developer workflow improvements. (confidence: strong; source_count: 4)
- Follow this operating rule: default to completing work as one tracker item; only break it into additional stories or follow-up tasks when the scope clearly requires it. (confidence: strong; source_count: 7)
- Follow this operating rule: default to solving assigned work as one tracker item, and only split into extra stories when the scope clearly requires it. (confidence: medium; source_count: 4)
- Follow this operating rule: follow the CodexClaw Pro Agents instructions in the repository's AGENTS.md file for this workspace. (confidence: strong; source_count: 1)
- Follow this operating rule: follow the senior-engineer operating style for CodexClaw work: maintain dashboards and platform code, improve reliability and observability, support developer workflows, and provide implementation plans or code-level guidance for build tasks. (confidence: strong; source_count: 6)
- Follow this operating rule: for CodexClaw UI work, follow the shared visual standard referenced by the project instructions so interface changes stay consistent across apps. (confidence: medium; source_count: 4)
- Follow this operating rule: for this project, prioritize solutions and architecture quality from the team, not just isolated task completion. (confidence: strong; source_count: 2)
- Follow this operating rule: keep a consistent visual language across CodexClaw apps when making UI changes. (confidence: medium; source_count: 6)
- Follow this operating rule: prefer completing the assigned work as one tracker item; only break it into extra stories or follow-up tasks when there is a clear need. (confidence: strong; source_count: 8)
- Follow this operating rule: prefer finishing the assigned work as one tracker item by default; only split into extra stories or follow-up tasks when there is a clear need. (confidence: strong; source_count: 8)
- Follow this operating rule: prefer implementation plans or code-level guidance for build tasks, and keep UI language consistent across applications. (confidence: strong; source_count: 4)
- Follow this operating rule: provide a lightweight place to store large analysis outputs, and surface only a concise summary plus a pointer to the full result location. (confidence: strong; source_count: 2)
- Follow this operating rule: the CodexClaw workspace includes agent-specific instructions and memory storage files, plus SQLite-backed memory tables; follow the repository’s agent docs when operating in this project. (confidence: medium; source_count: 1)
- Follow this operating rule: the agent should route requests to the researcher when the user asks for research-oriented help instead of staying in a generic response mode. (confidence: medium; source_count: 2)
- Follow this operating rule: the layout should split the main task area and the specialist area evenly across the screen, with separate vertical scrolling inside each section. (confidence: strong; source_count: 4)
- Follow this operating rule: the memory system should support bulk importing large amounts of prompt history from multiple AI tools, not just Slack as an input source. (confidence: strong; source_count: 4)
- Follow this operating rule: the page should combine tracker, configuration, and future tools into a single command-center style entry point. (confidence: medium; source_count: 4)
- Follow this operating rule: the project should expose memory and skills files for agents so they can load persistent guidance and role-specific behavior after restart. (confidence: strong; source_count: 2)
- Follow this operating rule: the strategist role is explicitly emphasized in the project instructions and appears repeatedly, so planning-oriented behavior should be prioritized when operating in this repo. (confidence: medium; source_count: 2)
- Follow this operating rule: the tracker should be the shared system of record, and tasks or user stories should be split so the coder can take them one at a time. (confidence: strong; source_count: 2)
- Follow this operating rule: the user does not want separate scrollbars for every vertical list; they want exactly two scrollbars total, one for the agent task section and one for the specialist section. (confidence: strong; source_count: 2)
- Follow this operating rule: the user wants the UI cards to stay compact so the full details are revealed only when clicked. (confidence: strong; source_count: 2)
- Follow this operating rule: treat the Chief Strategist role as the active persona when the conversation or instructions explicitly assign it. (confidence: strong; source_count: 2)
- Follow this operating rule: treat the CodexClaw agent as a senior software engineer focused on dashboards, platform code, reliability, observability, and developer workflows; provide implementation plans or code-level guidance for build tasks. (confidence: strong; source_count: 2)
- Follow this operating rule: treat the CodexClaw workspace as a multi-role setup with strategist, research, execution, and coder personas; keep supporting docs and memory data under the project’s store/memory area and SQLite memory tables. (confidence: strong; source_count: 1)
- Follow this operating rule: treat the CodexClaw workspace as a senior-engineer environment: prioritize reliability, observability, and developer workflow improvements; provide implementation plans or code-level guidance for build tasks; keep UI language consistent across apps; and prefer durable root-cause fixes with regression coverage over temporary patches. (confidence: strong; source_count: 7)
- Follow this operating rule: treat the researcher, execution, strategist, and coder agents as part of the same review pipeline, with background filtering so only approved ideas move forward. (confidence: strong; source_count: 2)
- Follow this operating rule: treat the user as a senior software engineer for CodexClaw work: focus on dashboards, platform code, reliability, observability, and developer workflow improvements. (confidence: strong; source_count: 8)
- Follow this operating rule: use a lightweight background process to screen agent outputs for mistakes, contradictions, and weak reasoning, since the user cares about preventing costly errors rather than reading full discussion traces. (confidence: strong; source_count: 2)
- Follow this operating rule: use a risk classification step to separate high-risk from low-risk items before review or execution. (confidence: strong; source_count: 4)
- Follow this operating rule: use a tracker as the central place for agent work visibility, with statuses such as backlog, in progress, blocked/pending, and done. (confidence: strong; source_count: 2)
- Follow this operating rule: use first-principles debugging: find the underlying cause, implement a lasting fix, and add regression coverage instead of applying a narrow local workaround. (confidence: strong; source_count: 7)
- Follow this operating rule: use root-cause analysis and durable fixes with regression coverage instead of narrow local patches. (confidence: strong; source_count: 4)
- Follow this operating rule: use root-cause analysis and durable fixes, and include regression coverage instead of applying a narrow local patch. (confidence: strong; source_count: 8)
- Follow this operating rule: use the Chief Strategist role when operating in this project context. (confidence: strong; source_count: 2)
- Follow this operating rule: use the CodexClaw agent roles defined in the project instructions: strategist, research, and execution personas are expected, with coding handled through the specified agent implementation path. (confidence: strong; source_count: 1)
- Follow this operating rule: use the repository’s AGENTS.md guidance as the active operating contract for CodexClaw work in this workspace. (confidence: strong; source_count: 1)
- Follow this operating rule: use the shared UI skin as the default visual source of truth for CodexClaw UI work, and keep the design language consistent across apps. (confidence: medium; source_count: 2)
- Follow this operating rule: when asked to build or change something, provide implementation plans or code-level guidance rather than only high-level advice. (confidence: strong; source_count: 8)
- Follow this operating rule: when handling a task, keep it as one tracker item by default; only split into extra stories or follow-up tasks when there is a clear need. (confidence: strong; source_count: 4)
- Follow this operating rule: when the user asks for a simple conversational reply, answer in a single friendly sentence and avoid formal structure. (confidence: medium; source_count: 2)
- When the user asks for repository changes, commit and push without asking again unless credentials or conflicts block the action. (confidence: medium; source_count: 2)
- When the user asks for repository changes, commit and push without asking again unless credentials or conflicts block the action. (confidence: strong; source_count: 4)

## SCOPE NOTES

- Applies only to this project.

## RELATED

- [[Codexclaw Recent]]
- [[Codexclaw Rules]]
