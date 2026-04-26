

<!-- WIKIMEMORY:START -->
# 🧠 Agent Memory Index

Generated WikiMemory entry map for Codex. Keep user-written content outside the managed block.

## Startup behavior

- Start new chats with a calm direct opener, but do not mention internal memory artifacts such as consumer-profile, rules files, or page names in the first message.
- Phrase the opener in the user's style using ./memory/global/user-rules.md and ./memory/global/consumer-profile.md.
- The first message must state exactly how old the latest durable workspace memory is using both relative time and absolute time.
- Use wording like: `Latest durable workspace memory update: about <relative-age> ago (<absolute-time>).`
- Ask whether the user wants to continue an existing project or start a new one before loading project-specific work.
- Mention that if work happened in another chat after that timestamp, you can provide a copy/paste prompt to pull only the missing newer context into this chat.
- If asked for that handoff prompt, write it as a prompt addressed to the other chat, not to the user here.
- The handoff prompt must be copy/paste ready with no brackets, no placeholders, and no fields for the user to fill in manually.
- The handoff prompt must ask the other chat to summarize only what changed after the latest durable memory timestamp for this workspace.
- If the user selects a project, send a follow-up summary of that project's direction, backlog, preferences, recent context, and lessons.
- Treat backlog and open threads as options only; never assume the next task or start work until the user chooses a direction.
- Interpret page roles explicitly: directive = follow, preference = adapt tone/work style to, descriptive = use for context, guidance = use as heuristic guidance unless contradicted by directives or the user.
- If the user asks to do something that conflicts with saved rules, name the conflicting page/rule and ask whether it is a one-off exception or a memory change.
- For durable rule changes, ask the user to confirm with a single line starting with `Memory command:` such as `Memory command: add global rule: ...`, `Memory command: add project rule: ...`, `Memory command: replace rule: "old" -> "new"`, or `Memory command: remove rule: "..."`.

## Freshness

- Latest durable refresh: 2026-04-19T02:18:21.416824Z.
- Relative age: 7 days.
- Layer status: memory=fresh, profile=fresh, bootstrap=fresh.
- Detailed freshness page: ./memory/global/memory-freshness.md

## Read on startup:

1. Global rules:
   -> ./memory/global/user-rules.md
   -> ./memory/global/consumer-profile.md
   -> ./memory/_meta/consumer_style.json
   -> ./memory/global/memory-freshness.md
   -> ./memory/global/memory-health.md
   -> ./memory/global/memory-change-log.md
   -> ./memory/global/active-exceptions.md

2. Do not load any project-specific pages until the consumer picks a project.

Available projects:
   - aitrader
   - codexclaw
   - wikimemory

Project routing rule:
- If the consumer refers to a project indirectly, approximately, or by description instead of exact name, map it to the closest matching available project before loading project pages.
- Ask one short clarification only if multiple projects are plausible or the match is weak.

## After project selection, load in order:

1. Project memory:
   -> ./memory/projects/<selected-project>/project.md

2. Recent context (highest priority):
   -> ./memory/projects/<selected-project>/recent.md
   -> ./memory/projects/<selected-project>/continuations.md

3. Project rules:
   -> ./memory/projects/<selected-project>/rules.md

4. Project lessons:
   -> ./memory/projects/<selected-project>/lessons.md

## Instructions

- Treat these files as source of truth.
- user-rules.md and project rules.md contain directive agent behavior; follow them.
- consumer-profile.md contains inferred preferences; mirror style and workflow without presenting them as hard rules.
- project.md and recent.md provide state/context; summarize them, but do not treat them as authorization to act.
- lessons.md contains reusable heuristics; apply them when relevant, but let directives and current user requests win.
- consumer_style.json is a compiled style config; use it to keep bootstrap phrasing and follow-up tone aligned with the consumer.
- Prefer recent.md for current direction after the consumer picks a project.
- Do not infer durable rules from one-off instructions.
- Do not auto-resume saved backlog items without explicit confirmation from the consumer.
- Consumer-confirmed `Memory command:` lines are authoritative memory edits and should be preserved as explicit overrides.
- Keep this bootstrap tiny; load linked memory files for detail.
<!-- WIKIMEMORY:END -->
