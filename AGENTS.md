# SessionMemory

<!-- SESSIONMEMORY:START -->
# 🧠 Agent Memory Index

Generated SessionMemory entry map for Codex. Keep user-written content outside the managed block.

## Startup behavior

- The first line of the first real reply must explicitly reassure the user that the needed memory is already loaded here.
- Use this exact first line: `Your workspace memory is already loaded here.`
- Start new chats with a calm direct opener, but do not mention internal memory artifacts such as consumer-profile, rules files, or page names in the first message.
- Phrase the opener in the user's style using `./memory/global/user-rules.md` and `./memory/global/consumer-profile.md`.
- Ask whether the user wants to continue an existing project or start a new one before loading project-specific work.
- If the user says work happened in another chat, offer a copy/paste handoff prompt that asks only for the missing newer context.
- Treat backlog and saved open threads as options only. Never assume the next task or start work until the user chooses a direction.

## Read On Startup

1. Global rules:
   -> `./memory/global/user-rules.md`
   -> `./memory/global/consumer-profile.md`
   -> `./memory/_meta/consumer_style.json`
   -> `./memory/global/memory-freshness.md`
   -> `./memory/global/memory-health.md`
   -> `./memory/global/memory-change-log.md`
   -> `./memory/global/active-exceptions.md`

2. Do not load any project-specific pages until the user picks a project.

3. After project selection, load:
   -> `./memory/projects/<selected-project>/project.md`
   -> `./memory/projects/<selected-project>/recent.md`
   -> `./memory/projects/<selected-project>/continuations.md`
   -> `./memory/projects/<selected-project>/rules.md`
   -> `./memory/projects/<selected-project>/lessons.md`

4. Never load daily conversation pages by default:
   -> `./memory/daily-conversations/YYYY-MM-DD.md`
   -> Only read them if the user explicitly asks for a daily conversation history page or a specific date.

## Instructions

- Treat directive pages as rules to follow.
- Treat preference pages as style and workflow adaptation guidance.
- Treat descriptive pages as context, not authorization to act.
- Treat guidance pages as heuristics unless current user instructions or directives override them.
- Keep the bootstrap tiny and load linked memory files for detail.
<!-- SESSIONMEMORY:END -->
