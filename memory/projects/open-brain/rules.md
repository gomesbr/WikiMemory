---
type: project-rules
project: open-brain
updated: 2026-04-19T04:21:45.668183Z
tags: [project/open-brain, rules]
---

# ⚙️ Open Brain - Project Rules

## ALWAYS DO

- No always-do rules selected yet.

## NEVER DO

- No never-do rules selected yet.

## CONDITIONAL RULES

- Follow this operating rule: a second-pass cleanup is still expected later, even after the main generation loop has been running for a while.
- Follow this operating rule: a strategy group should continue through all queued strategies even if one succeeds before the last one finishes.
- Follow this operating rule: add a dashboard section for pre-loop user answers so calibration can be completed inside the interface instead of requiring terminal interaction.
- Follow this operating rule: add a progress-percentage column to the source breakdown view so each source shows completion alongside totals and pending counts.
- Follow this operating rule: add a routine that keeps the relevant repositories or working copies clean and up to date on a daily basis.
- Follow this operating rule: add a sanitizer before ingestion to strip or escape JSON-reserved characters that can break downstream processing.
- Follow this operating rule: add pagination to the support matrix so the user can browse all domains.
- Follow this operating rule: adopt an intent-engineered ask flow, make ambiguity governance explicit before locking benchmarks, and enforce strict winner selection rules in the benchmark pipeline.
- Follow this operating rule: after fixing the requested issue, remove the completed item from the backlog.
- Follow this operating rule: after implementing changes, the loop should run without requiring further user input.
- Follow this operating rule: aim for a corpus where most mined cases come from human-to-human conversations rather than assistant-only threads.
- Follow this operating rule: ambiguous benchmark items should be routed to a clarification step instead of being scored as pass or fail when the ambiguity is genuine.
- Follow this operating rule: apply the actor cleanup heuristics consistently: discard entries that are only a phone number, discard WhatsApp group chat names, and remove tilde characters from names.
- Follow this operating rule: before broad reruns, systematically repair cases that have inline notes, quoted issue markers, or obvious defects, then rerun until they satisfy the comments.
- Follow this operating rule: before ingestion, run data-quality reasoning to catch misclassification and noise issues across the dataset, not only in the graph layer.
- Follow this operating rule: build an evolution monitoring module that tracks strategy evolution live at the experiment level and ties it to the pre-loop calibration workflow.
- Follow this operating rule: for 'it' and 'you' actor cases, present the entries directly in chat instead of exporting them to a file.
- Follow this operating rule: for CodexClaw Mission Control, follow the approved clean redesign direction: hybrid rail plus top navigation, main content with a side panel, calm minimal visual tone, and apply it across all modules in phase 1.
- Follow this operating rule: for agent debug views, use separate swim lanes per agent and show directional arrows for message flow, including vertical sequencing within a lane and cross-lane handoffs.
- Follow this operating rule: for judge calibration, the data owner can review sample question-answer pairs and confirm whether the generated answer matches the database-backed truth.
- Follow this operating rule: for the 'they' actor set, create a separate review CSV so the user can inspect it manually.
- Follow this operating rule: for the AITrader effort, keep agent automation centered on repeatable prompts and skills, and expose a reliable API path for the agent to read market data and create trade cards.
- Follow this operating rule: for the CodexClaw roadmap, keep strategist as the only Phase 1 writer to AITrader; other agents should remain outside that write path in Phase 1.
- Follow this operating rule: for unresolved raw records, prefer tracking them explicitly rather than forcing a full re-ingest unless the source data cannot be recovered another way.
- Follow this operating rule: if source files are available, attempt recovery and re-ingestion from those originals before treating records as permanently unrecoverable.
- Follow this operating rule: improve ingestion so structural content such as tables is detected in raw input and reformatted for indexing without changing meaning.
- Follow this operating rule: in the support matrix, sort cards by evidence count descending, but keep cards from the same domain grouped near each other.
- Follow this operating rule: keep test generation grounded in real facts, but produce multiple wording variants across a clarity spectrum for each fact.
- Follow this operating rule: keep the already reviewed yes cases and only a small, useful subset of no cases for training; remove the rest and replenish the queue so the final mix still meets the desired yes-rate threshold.
- Follow this operating rule: keep the taxonomy strict to the defined 36 domains, but review legacy labels to decide whether any should become first-class domains instead of being deleted as noise.
- Follow this operating rule: keep traversing the dataset until completion, continuing to solve blockers while the run is active.
- Follow this operating rule: monitor the pipeline on a short recurring cadence and, when progress stalls, inspect dropped cases to determine whether they are valid before making code changes and resuming the run.
- Follow this operating rule: no process in the system should be using the raw actor list.
- Follow this operating rule: open Brain should support bulk and recurring ingestion from ChatGPT, Grok, WhatsApp, and existing CodexClaw history.
- Follow this operating rule: openBrain’s quick-start flow is Windows-oriented and begins with copying the example environment file before starting the service.
- Follow this operating rule: pause concurrent writers before cleanup or replay work, then restart them afterward to avoid corruption or inconsistent results.
- Follow this operating rule: prefer published, high-quality artifacts as the basis for graph building, insights, and answers.
- Follow this operating rule: prioritize diverse case sources, especially conversations involving people, individuals, and group chats, rather than over-relying on assistant-centric WhatsApp examples.
- Follow this operating rule: prioritize improving the agent on the existing dataset before relying on any normalized or re-embedded data path.
- Follow this operating rule: pronoun attribution should be applied across all actors in the database, not just a subset.
- Follow this operating rule: provide a debug view for Ask that shows the full information flow across orchestrator and agents, including intermediate outputs and a visible loading indicator while requests are processing.
- Follow this operating rule: provide a review workflow where the user can approve or reject candidate new domains, candidate new lenses, and proposed merges or splits of existing domains.
- Follow this operating rule: remove OpenRouter references from the codebase; the project should no longer use OpenRouter, and there should be no fallback to OpenAI API.
- Follow this operating rule: remove WhatsApp group chats from the actor list when they appear in review outputs.
- Follow this operating rule: run the metadata and facet gap discovery across the full published corpus, including actors, groups, dates, thread titles, and source-system coverage.
- Follow this operating rule: the Evolution page should use a more descriptive experiment selector and present it as a dropdown listing all available experiments.
- Follow this operating rule: the Network screen should replace the older People Network variant as the primary implementation target.
- Follow this operating rule: the People area should evolve into a relationship graph centered on the user, showing all connected data categories and types.
- Follow this operating rule: the agent only needs to know OpenBrain capabilities and how to use them to retrieve the requested data; extra domain-specific assumptions are unnecessary.
- Follow this operating rule: the agent should infer user intent from the question itself and translate that intent into retrieval subqueries against OpenBrain without relying on special hint codes.
- Follow this operating rule: the app should keep iterating on the phase-gap loop, with emphasis on filling missing coverage across all phases rather than stopping early.
- Follow this operating rule: the batch generation should continue across the full published corpus, not only the narrow refill-failure subset.
- Follow this operating rule: the case-generation process should not be narrowed to only a few proven domains; it should continue using the full dataset so the system can surface broader coverage.
- Follow this operating rule: the loop should be able to restart from the first strategy after changes, and the orchestrator should monitor health and recover from unexpected stops.
- Follow this operating rule: the messaging integration work is being done in Node.js using Twilio.
- Follow this operating rule: the readiness UI needs a cleaner card-based layout for phase information, arranged side by side and easier to scan.
- Follow this operating rule: the strategy program should be implemented as a grounded, componentized, hypothesis-driven optimizer upgrade that preserves provenance and supports autonomous continuous looping.
- Follow this operating rule: the support matrix should not render as one long horizontal string; reorganize it into a clearer layout, including moving the section under benchmark freshness if that improves readability.
- Follow this operating rule: the user is testing prompt changes by comparing model answers against a reference response and wants iteration until the outputs are closely aligned.
- Follow this operating rule: the user is tuning processing throughput in small increments and expects the agent to apply the requested rate changes, then observe whether CPU and completion behavior match.
- Follow this operating rule: the user wants a comprehensive emoji translation strategy for WhatsApp across iPhone and Android, including context-sensitive meaning resolution.
- Follow this operating rule: the user wants a verdict filter so they can focus on yes or no cases separately.
- Follow this operating rule: the user wants long-running work to continue in the background while the conversation moves on to other topics, rather than blocking on a single task.
- Follow this operating rule: the user wants taxonomy coverage checked against the current database when preparing a new version, but not on every run, and wants a way to handle future domain growth.
- Follow this operating rule: the user wants the Evolution module implemented in OpenBrain UI, combining live experiment monitoring, pre-loop calibration in the UI, and strict lock/start governance.
- Follow this operating rule: the user wants the agent to keep checking whether the workload is actually progressing, especially when the visible rate or CPU usage does not match expectations.
- Follow this operating rule: the user wants the code updated to diversify clarified-required questions, avoid repeating near-duplicate prompts, and delete items that fail revalidation so deprecated questions do not remain in the system.
- Follow this operating rule: the user wants the thinking methodology about first-principles, theme-based problem solving added to the agent guidance so future responses follow that approach.
- Follow this operating rule: treat actor linkage as a row-level contract: each message record should carry its own actor and conversation identifiers, plus timestamp, text, reply linkage, and source metadata.
- Follow this operating rule: treat canonicalization as a normalization step before embedding; do not conflate it with re-embedding the same data.
- Follow this operating rule: treat names with obvious noise markers or non-name patterns as suspicious review candidates, but remove entries from that list when the user confirms they are not suspicious.
- Follow this operating rule: treat repeated case-generation failures as a signal to inspect the authoring pipeline broadly, not just the critical queue, and prune both reviewed and unreviewed duplicates.
- Follow this operating rule: treat the benchmark set as a way to expose gaps in the platform, not as a test of existing production data alone.
- Follow this operating rule: treat the requested Mission Control look as both a style and layout goal: keep it simple, clean, and easy to scan, not just visually similar.
- Follow this operating rule: use JSON as the required format for agent-to-agent communication to keep interactions structured and machine-readable.
- Follow this operating rule: use SMS notifications for key loop events: strategy failure, strategy success, all strategies in a group failing, and the start of research for a new group.
- Follow this operating rule: use a benchmark-driven coverage workflow to generate hypothetical user questions from the taxonomy and analysis lenses, then map each question to expected answer quality and required platform support.
- Follow this operating rule: use a pull request as the merge path to main for this codebase, rather than merging directly.
- Follow this operating rule: use keyword matches only as entry points; always expand into surrounding context and reply chains before drawing conclusions.
- Follow this operating rule: use phone numbers from WhatsApp data when available to help confirm actor identity and review name matches.
- Follow this operating rule: when a question is too ambiguous to answer reliably, the system should ask the owner for confirmation during the creation or validation phase before locking it in.
- Follow this operating rule: when asked to make a change, implement it directly rather than only adding it to the backlog.
- Follow this operating rule: when generating review CSVs for ambiguous actors, use a simple three-column format with no extra quoting in the editable third column.
- Follow this operating rule: when replaying data, surface any newly created actors for user review so they can confirm whether each is genuinely new, should be merged, or should be removed.
- Follow this operating rule: when reporting strategies, present them in chronological order from oldest to newest rather than newest first.
- Follow this operating rule: when reviewing documentation, check for duplicated or conflicting descriptions of skills, roles, responsibilities, and personas across markdown files.
- Follow this operating rule: when reviewing the 'they' dataset, normalize actor names by stripping any leading tilde and extra leading whitespace before matching or merging.
- Follow this operating rule: when selecting retrieval candidates, prioritize groups where the user is most active with other people, since those are likely to generate more questions.
- Follow this operating rule: when the user asks for visual fixes, prioritize correcting layout issues shown in screenshots before moving on to the next task.
- Follow this operating rule: when the user reports failed rows, the agent should reset or reprocess those failures rather than treating them as terminal.
- Keep responses concise by default and avoid unnecessary process narration when token budget matters.
- Keep responses concise by default and avoid unnecessary process narration when token budget matters.
- Keep responses concise by default and avoid unnecessary process narration when token budget matters.
- No fallback should exist as answers have to be evidence based.

## PROMOTED RULES (EXPLICIT)

- 48 explicit rule(s) are listed above by behavior bucket.

## INFERRED RULES

- Follow this operating rule: a second-pass cleanup is still expected later, even after the main generation loop has been running for a while. (confidence: strong; source_count: 2)
- Follow this operating rule: add a progress-percentage column to the source breakdown view so each source shows completion alongside totals and pending counts. (confidence: strong; source_count: 4)
- Follow this operating rule: ambiguous benchmark items should be routed to a clarification step instead of being scored as pass or fail when the ambiguity is genuine. (confidence: strong; source_count: 5)
- Follow this operating rule: before ingestion, run data-quality reasoning to catch misclassification and noise issues across the dataset, not only in the graph layer. (confidence: strong; source_count: 4)
- Follow this operating rule: for 'it' and 'you' actor cases, present the entries directly in chat instead of exporting them to a file. (confidence: medium; source_count: 2)
- Follow this operating rule: for the 'they' actor set, create a separate review CSV so the user can inspect it manually. (confidence: strong; source_count: 2)
- Follow this operating rule: for the AITrader effort, keep agent automation centered on repeatable prompts and skills, and expose a reliable API path for the agent to read market data and create trade cards. (confidence: medium; source_count: 3)
- Follow this operating rule: for the CodexClaw roadmap, keep strategist as the only Phase 1 writer to AITrader; other agents should remain outside that write path in Phase 1. (confidence: medium; source_count: 2)
- Follow this operating rule: for unresolved raw records, prefer tracking them explicitly rather than forcing a full re-ingest unless the source data cannot be recovered another way. (confidence: strong; source_count: 2)
- Follow this operating rule: if source files are available, attempt recovery and re-ingestion from those originals before treating records as permanently unrecoverable. (confidence: strong; source_count: 4)
- Follow this operating rule: improve ingestion so structural content such as tables is detected in raw input and reformatted for indexing without changing meaning. (confidence: strong; source_count: 2)
- Follow this operating rule: keep test generation grounded in real facts, but produce multiple wording variants across a clarity spectrum for each fact. (confidence: medium; source_count: 2)
- Follow this operating rule: keep the taxonomy strict to the defined 36 domains, but review legacy labels to decide whether any should become first-class domains instead of being deleted as noise. (confidence: strong; source_count: 2)
- Follow this operating rule: no process in the system should be using the raw actor list. (confidence: medium; source_count: 1)
- Follow this operating rule: openBrain’s quick-start flow is Windows-oriented and begins with copying the example environment file before starting the service. (confidence: medium; source_count: 1)
- Follow this operating rule: pause concurrent writers before cleanup or replay work, then restart them afterward to avoid corruption or inconsistent results. (confidence: strong; source_count: 2)
- Follow this operating rule: prefer published, high-quality artifacts as the basis for graph building, insights, and answers. (confidence: medium; source_count: 2)
- Follow this operating rule: prioritize diverse case sources, especially conversations involving people, individuals, and group chats, rather than over-relying on assistant-centric WhatsApp examples. (confidence: strong; source_count: 2)
- Follow this operating rule: pronoun attribution should be applied across all actors in the database, not just a subset. (confidence: strong; source_count: 2)
- Follow this operating rule: remove WhatsApp group chats from the actor list when they appear in review outputs. (confidence: strong; source_count: 2)
- Follow this operating rule: the agent only needs to know OpenBrain capabilities and how to use them to retrieve the requested data; extra domain-specific assumptions are unnecessary. (confidence: strong; source_count: 2)
- Follow this operating rule: the agent should infer user intent from the question itself and translate that intent into retrieval subqueries against OpenBrain without relying on special hint codes. (confidence: strong; source_count: 2)
- Follow this operating rule: the app should keep iterating on the phase-gap loop, with emphasis on filling missing coverage across all phases rather than stopping early. (confidence: strong; source_count: 2)
- Follow this operating rule: the readiness UI needs a cleaner card-based layout for phase information, arranged side by side and easier to scan. (confidence: strong; source_count: 2)
- Follow this operating rule: the support matrix should not render as one long horizontal string; reorganize it into a clearer layout, including moving the section under benchmark freshness if that improves readability. (confidence: strong; source_count: 4)
- Follow this operating rule: the user is testing prompt changes by comparing model answers against a reference response and wants iteration until the outputs are closely aligned. (confidence: medium; source_count: 2)
- Follow this operating rule: the user is tuning processing throughput in small increments and expects the agent to apply the requested rate changes, then observe whether CPU and completion behavior match. (confidence: strong; source_count: 3)
- Follow this operating rule: the user wants long-running work to continue in the background while the conversation moves on to other topics, rather than blocking on a single task. (confidence: medium; source_count: 2)
- Follow this operating rule: the user wants the agent to keep checking whether the workload is actually progressing, especially when the visible rate or CPU usage does not match expectations. (confidence: strong; source_count: 3)
- Follow this operating rule: treat actor linkage as a row-level contract: each message record should carry its own actor and conversation identifiers, plus timestamp, text, reply linkage, and source metadata. (confidence: strong; source_count: 4)
- Follow this operating rule: treat canonicalization as a normalization step before embedding; do not conflate it with re-embedding the same data. (confidence: medium; source_count: 2)
- Follow this operating rule: treat names with obvious noise markers or non-name patterns as suspicious review candidates, but remove entries from that list when the user confirms they are not suspicious. (confidence: strong; source_count: 8)
- Follow this operating rule: treat repeated case-generation failures as a signal to inspect the authoring pipeline broadly, not just the critical queue, and prune both reviewed and unreviewed duplicates. (confidence: strong; source_count: 2)
- Follow this operating rule: treat the benchmark set as a way to expose gaps in the platform, not as a test of existing production data alone. (confidence: strong; source_count: 2)
- Follow this operating rule: treat the requested Mission Control look as both a style and layout goal: keep it simple, clean, and easy to scan, not just visually similar. (confidence: medium; source_count: 2)
- Follow this operating rule: use a benchmark-driven coverage workflow to generate hypothetical user questions from the taxonomy and analysis lenses, then map each question to expected answer quality and required platform support. (confidence: strong; source_count: 2)
- Follow this operating rule: use a pull request as the merge path to main for this codebase, rather than merging directly. (confidence: medium; source_count: 2)
- Follow this operating rule: use keyword matches only as entry points; always expand into surrounding context and reply chains before drawing conclusions. (confidence: strong; source_count: 4)
- Follow this operating rule: use phone numbers from WhatsApp data when available to help confirm actor identity and review name matches. (confidence: medium; source_count: 4)
- Follow this operating rule: when generating review CSVs for ambiguous actors, use a simple three-column format with no extra quoting in the editable third column. (confidence: strong; source_count: 4)
- Follow this operating rule: when reviewing documentation, check for duplicated or conflicting descriptions of skills, roles, responsibilities, and personas across markdown files. (confidence: medium; source_count: 2)
- Follow this operating rule: when reviewing the 'they' dataset, normalize actor names by stripping any leading tilde and extra leading whitespace before matching or merging. (confidence: strong; source_count: 2)
- Follow this operating rule: when the user reports failed rows, the agent should reset or reprocess those failures rather than treating them as terminal. (confidence: strong; source_count: 2)
- Keep responses concise by default and avoid unnecessary process narration when token budget matters. (confidence: strong; source_count: 2)
- Keep responses concise by default and avoid unnecessary process narration when token budget matters. (confidence: strong; source_count: 2)
- No fallback should exist as answers have to be evidence based. (confidence: medium; source_count: 1)

## SCOPE NOTES

- Applies only to this project.

## RELATED

- [[Open Brain Recent]]
- [[Open Brain Rules]]
