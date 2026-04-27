# WikiMemory

Point your code agent to [START_HERE_FOR_AGENT.md](START_HERE_FOR_AGENT.md) to begin configuration.

WikiMemory is a file-based memory pipeline for agent session logs and related project context.

Its job is to turn raw session traces and project signals into:

- structured normalized events
- segmented conversational/work units
- deterministic domain classification
- extracted knowledge items
- optional consumer working-profile inputs for better future collaboration
- synthesized wiki pages
- compact bootstrap memory for future agents
- audit findings over the entire memory layer

The project is designed to preserve provenance, stay incremental, and keep the raw source logs outside the repo. The raw logs remain the source of truth. Everything inside this repository is a derived artifact, control file, config, test, or generated knowledge output.

## Why This Exists

Agent session logs contain a large amount of useful information, but they are difficult to reuse directly:

- they are append-only raw traces
- they mix user intent, agent reasoning, tool calls, code work, status chatter, and planning
- they are not organized by project/domain knowledge
- they are too large and noisy to load directly into future sessions

WikiMemory solves that by building a layered pipeline:

1. discover the raw sessions
2. normalize them into a stable internal representation
3. ingest normalized logs and project deltas into canonical evidence records
4. segment them into meaningful spans
5. classify those spans into domains
6. extract durable and temporal knowledge
7. synthesize a human-readable wiki
8. compress the best subset into startup/bootstrap memory
9. audit the outputs for contradictions, drift, provenance gaps, and quality issues
10. orchestrate incremental refreshes and controlled full-corpus loading

## Design Principles

- Raw logs are the source of truth.
- Derived artifacts are disposable and rebuildable.
- Provenance is mandatory.
- Incremental operation matters.
- Deterministic structure comes before LLM synthesis.
- LLM use is bounded and evidence-backed, not freeform.
- Knowledge should be compressed progressively, not copied blindly.
- Fixes should generalize across the corpus, not overfit one sample.
- Consumer profiling should stay behavior-oriented, evidence-backed, and non-sensitive.

## Consumer Working Profile

WikiMemory can support a `consumer working profile` to help future agent sessions collaborate better with the same consumer.

This should be limited to work-relevant traits such as:

- communication preferences
- workflow preferences
- technical strengths
- active domains
- current goals
- persistent constraints

It should not infer or store:

- IQ or intelligence scores
- psychological diagnosis
- mental-health inference
- protected-class traits
- other sensitive personal attributes

Reference files:

- `docs/consumer-profile.md`
- `schema/consumer_working_profile.schema.json`
- `config/consumer_profile_policy.json`

## Source Compatibility

WikiMemory is not limited to one vendor's chat product. It is designed to support multiple conversation-history sources through different adapter styles:

- `local_session_log_adapter`
- `chat_export_adapter`
- `api_event_capture_adapter`

The setup agent is expected to work on this configuration for the consumer. During onboarding it should inspect the local environment, infer the most likely source type, and configure the right ingestion path instead of expecting the consumer to map the storage model manually.

Compatibility matrix:

| Source | Local raw logs | Export available | Incremental-friendly | Best adapter type | Product fit |
| --- | --- | --- | --- | --- | --- |
| Codex CLI / local Codex workflows | Yes | Possible but not required | High | `local_session_log_adapter` | Strong |
| Claude Code | Yes | Possible | High | `local_session_log_adapter` | Strong |
| Cursor-style local agent workflows | Usually yes when backed by local session/event files | Sometimes | High | `local_session_log_adapter` | Strong |
| ChatGPT web / app | No stable local raw log contract | Yes | Medium | `chat_export_adapter` | Medium |
| Claude web / Claude Desktop | No stable append-only local raw log contract for this use case | Yes | Medium | `chat_export_adapter` | Medium |
| API-only custom agent apps | Only if the app records them | N/A unless the app adds export | High when instrumented | `api_event_capture_adapter` | Strong when instrumented |

Interpretation:

- `Strong`: best fit for continuous memory refresh because the source can be read incrementally and reprocessed deterministically.
- `Medium`: usable, but better for periodic imports or backfills than continuous local delta tracking.
- `Weak` would mean the product needs an additional logging layer before memory quality will be reliable.

Practical rule:

- if the platform stores full local conversations, WikiMemory can usually run incrementally
- if the platform only offers account export, WikiMemory can still work, but more like import/snapshot mode
- if the platform offers neither, the solution is to add API-side event capture at the app layer

## End-to-End Pipeline

### Phase 1: Discovery

Discovery scans one or more configured external roots for session log files and assigns stable logical identity using `session_meta.payload.id`.

It tracks:

- file path
- source identity
- file size and append checkpoints
- committed byte/line bounds
- tombstones for missing files
- duplicate/conflict conditions

This phase does not copy raw logs into the repo.

Writes:

- `state/source_registry.json`
- `state/discovery_runs.jsonl`

### Phase 2: Normalization

Normalization converts each raw event line into a stable canonical event record.

This project uses a pointer-first normalization design. It does not persist the full raw JSON event payload. Instead it stores:

- `source_id`
- `session_id`
- `event_id`
- `source_line_no`
- `source_byte_start`
- `source_byte_end`
- `timestamp`
- `outer_type`
- `payload_type`
- `canonical_kind`
- `role`
- references and ids extracted from the payload
- bounded `text_surfaces`
- `event_digest`
- `text_surface_truncated`

This keeps provenance exact while avoiding a full raw mirror in Phase 2. If a later phase truly needs more detail than the stored text surfaces provide, it can lazily hydrate the original event through the resolver.

Writes:

- `normalized/sources/<source_id>/session.json`
- `normalized/sources/<source_id>/events.jsonl`
- `normalized/sources/<source_id>/stats.json`
- `state/normalization_state.json`
- `state/normalization_runs.jsonl`
- `audits/normalization_notices.jsonl`

### Phase 3: Segmentation

Before segmentation, the redesigned product foundation can also build a canonical `evidence/` layer:

- log evidence from pointer-first normalized agent events
- project-delta evidence from Git working tree status and HEAD metadata
- actor/source/provenance fields that future memory-first extraction can consume

Project association is deterministic first:

- configured project roots and aliases are matched against session cwd, paths, open tabs, and event text
- unresolved generic workspace records fall back to `projects`
- optional `project_routing` can run a bounded OpenAI second pass only for those unresolved sources
- routing decisions are cached in `state/project_routing_state.json` so repeated refreshes stay incremental

Command:

```powershell
python -m wikimemory ingest
```

Writes:

- `evidence/logs/<source_id>.jsonl`
- `evidence/projects/<project>.jsonl`
- `state/ingest_state.json`
- `state/ingest_runs.jsonl`
- `audits/ingest_notices.jsonl`

The memory-first path can then generate compact operational memory directly from evidence:

```powershell
python -m wikimemory memory
```

Writes:

- `memory/global/user-rules.md`
- `memory/projects/<project>/project.md`
- `memory/projects/<project>/recent.md`
- `memory/projects/<project>/rules.md`
- `memory/projects/<project>/lessons.md` when high-signal lessons exist
- `memory/_meta/items.jsonl`
- `state/memory_state.json`
- `state/memory_runs.jsonl`
- `audits/memory_notices.jsonl`

The configured agent bootstrap file can then be generated from compact memory:

```powershell
python -m wikimemory agent-bootstrap
```

In the default configuration this writes a tiny bootstrap entry map, usually `AGENTS.md`, that points to the derived memory files instead of copying the whole memory layer into the bootstrap.

Bootstrap rendering is configurable:

- `codex_agents_md` writes Codex-oriented `AGENTS.md`
- `claude_md` writes Claude-oriented `CLAUDE.md`
- `generic_bootstrap_md` writes a neutral markdown entry map
- the bootstrap stays small in all modes and links to derived memory instead of inlining recent context

Compact memory outputs can be linted independently from the legacy wiki pipeline:

```powershell
python -m wikimemory memory-lint
```

This checks rule quality, scope, provenance, stale recent-state items, and whether the agent bootstrap stays an entry map instead of inlining noisy recent context.

The redesigned memory path also has a single end-to-end refresh command:

```powershell
python -m wikimemory memory-refresh
```

This runs discovery, normalization, evidence ingest, compact memory generation, agent bootstrap generation, and memory linting without invoking the legacy wiki/bootstrap synthesis path.

Review inferred durable-rule candidates:

```powershell
python -m wikimemory memory-review
python -m wikimemory memory-review --approve <item_id>
python -m wikimemory memory-review --reject <item_id>
```

Apply canonical item fixes and rerender pages before the final lint pass:

```powershell
python -m wikimemory memory-lint --fix --max-fix-rounds 2
```

Prepare scheduler artifacts without activating anything:

```powershell
python -m wikimemory scheduler-plan
powershell -ExecutionPolicy Bypass -File scripts/install-windows-task.ps1 -IntervalMinutes 60
```

`scheduler-plan` writes a dry-run plan to `state/scheduler_plan.json` and a commented activation script to `scripts/install-windows-task.generated.ps1`. Scheduler timing now lives in `config/product_config.json`, including weekdays, local run time, ingest interval, lint interval, log-update gating, and whether future scheduled lint runs should use autofix.

Adapter extension notes live in `docs/adapters.md`.

Segmentation groups normalized events into higher-level units that are more useful than raw line-by-line traces.

Typical segments correspond to:

- a focused task slice
- a plan/change/review loop
- a domain-consistent chunk of work
- a coherent question/answer or tool-heavy work span

Segmentation remains file-based and source-local.

Writes:

- `segmented/sources/<source_id>/session_flow.json`
- `segmented/sources/<source_id>/segments.jsonl`
- `segmented/sources/<source_id>/stats.json`
- `state/segmentation_state.json`
- `state/segmentation_runs.jsonl`

### Phase 4: Classification

Classification assigns each segment to a domain label.

Current supported primary labels:

- `global`
- `project-a`
- `project-b`
- `project-c`
- `cross-project`
- `unclassified`

Classification is deterministic and config-driven. It uses:

- segment content
- source path and repo hints
- session metadata
- classification taxonomy config
- contextual inheritance for low-signal chains

The classifier is conservative, but the current production goal is that meaningful content-bearing segments should not remain `unclassified`.

Writes:

- `classified/sources/<source_id>/segments.jsonl`
- `classified/sources/<source_id>/stats.json`
- `state/classification_state.json`
- `state/classification_runs.jsonl`
- `audits/classification_notices.jsonl`

### Phase 5: Extraction

Extraction turns classified segments into structured knowledge items.

This is where the system begins to distinguish between:

- durable knowledge
- temporal knowledge
- project-scoped knowledge
- global user/agent interaction rules
- code location hints
- failures, decisions, current state, tasks, and open questions

Current item taxonomy:

- durable:
  - `communication_preference`
  - `do_rule`
  - `dont_rule`
  - `workflow_rule`
  - `decision`
  - `architecture_note`
  - `code_location`
- temporal:
  - `current_state`
  - `task_request`
  - `outcome`
  - `failure`
  - `next_step`
  - `open_question`

Extraction is deterministic and conservative. It now also carries durability metadata so the wiki layer can distinguish:

- true durable policy
- one-off session instructions
- progress narration
- schema/header noise

Important extracted metadata includes:

- `primary_domain`
- `secondary_domains`
- `confidence`
- `normalized_signature`
- `subject_key`
- `temporal_status`
- `target_namespace`
- `target_page_key`
- `provenance_refs`
- `durability_class`
- `wiki_eligible`
- `promotion_blockers`
- `supporting_session_count`
- `supporting_day_count`

Writes:

- `extracted/sources/<source_id>/items.jsonl`
- `extracted/sources/<source_id>/stats.json`
- `extracted/domains/<domain>/items.jsonl`
- `state/extraction_state.json`
- `state/extraction_runs.jsonl`
- `audits/extraction_notices.jsonl`

### Phase 6: Wiki Synthesis

Wiki synthesis builds a human-facing wiki from extracted domain items.

This phase is hybrid:

- deterministic code owns page identity, page structure, ranking, budgets, navigation, and provenance rendering
- the LLM owns bounded summaries and latent synthesis

The wiki is rendered as markdown and is Obsidian-compatible, but the internal page model is intended to remain renderer-friendly rather than permanently tied to Obsidian syntax.

Wiki generation now includes quality controls such as:

- only `wiki_eligible` items may populate canonical sections
- empty bucket pages are suppressed
- empty domain indexes are suppressed
- empty `unclassified` namespace pages are suppressed
- per-bucket evidence budgets
- page-size caps
- summary validation against generic filler patterns

Writes:

- `wiki/global/...`
- `wiki/projects/<domain>/...`
- `wiki/_meta/pages/...`
- `state/wiki_state.json`
- `state/wiki_runs.jsonl`
- `audits/wiki_notices.jsonl`

### Phase 7: Bootstrap Memory

Bootstrap memory is the compact agent-start layer.

This is not a second wiki. It is a much smaller compressed memory artifact for future sessions and agents. It selects and compresses only the highest-signal information needed for alignment and startup context.

Bootstrap is also hybrid:

- deterministic evidence selection
- bounded LLM compression into short agent-facing bullets
- no new latent knowledge is introduced here

Writes:

- `bootstrap/global.md`
- `bootstrap/projects/<domain>.md`
- `bootstrap/_meta/...`
- `state/bootstrap_state.json`
- `state/bootstrap_runs.jsonl`
- `audits/bootstrap_notices.jsonl`

### Phase 8: Audit

Audit validates the memory outputs.

It is deterministic and manifest-first. It does not rely on re-parsing the rendered markdown as the source of truth when structured manifests already exist.

Audit families include:

- contradictions
- duplicates
- stale temporal items
- provenance gaps
- wiki/bootstrap drift
- wiki quality issues such as:
  - transient rule pollution
  - empty pages
  - oversized pages
  - schema noise
  - generic synthesized claims

Writes:

- `audits/contradictions.jsonl`
- `audits/duplicates.jsonl`
- `audits/stale_items.jsonl`
- `audits/provenance_gaps.jsonl`
- `audits/wiki_bootstrap_drift.jsonl`
- `audits/wiki_quality.jsonl`
- `state/audit_state.json`
- `state/audit_runs.jsonl`

### Phase 9: Refresh

Refresh is the daily orchestration command.

It runs the pipeline incrementally and lets each phase keep ownership of its own invalidation logic. It supports scoped downstream work when only some source ids changed.

Refresh manages:

- phased execution
- scoped or skipped downstream phases
- lock handling
- partial-success recording
- aggregated phase reporting

Writes:

- `state/refresh_state.json`
- `state/refresh_runs.jsonl`
- `audits/refresh_notices.jsonl`
- `state/refresh.lock.json` during active runs

### Phase 10: Full Load

Full load is the strict full-corpus runner.

Its job is to support a controlled full-dataset pass with:

- phase-by-phase gates
- derived-disk accounting
- stop conditions
- issue bundles
- retry/repair control

It is meant for operational corpus loading, not day-to-day use.

Writes:

- `state/full_load_state.json`
- `state/full_load_runs.jsonl`
- `audits/full_load_notices.jsonl`
- `audits/full_load_issues/<run_id>/<phase>/issue.json`

## Repository Structure

Top-level folders you will care about:

- `wikimemory/`
  - Python implementation for all phases
- `config/`
  - JSON configuration for source roots, taxonomy, extraction, wiki, bootstrap, audit, refresh, and full-load
- `examples/`
  - representative raw source-data example for explaining the input format
- `schema/`
  - normalization catalog and related schema assets
- `tests/`
  - unit, regression, integration, and env-gated live-corpus tests
- `state/`
  - phase state files and run logs
- `audits/`
  - machine-readable notices and audit findings
- `normalized/`
  - Phase 2 outputs
- `segmented/`
  - Phase 3 outputs
- `classified/`
  - Phase 4 outputs
- `extracted/`
  - Phase 5 outputs
- `wiki/`
  - Phase 6 rendered wiki plus structured page manifests
- `bootstrap/`
  - Phase 7 compact memory outputs

## Raw Data Model and Provenance

The project intentionally does not vend the raw corpus into this repository.

Instead:

- raw session logs stay in the configured external source roots
- discovery indexes them
- normalization stores exact byte-range provenance
- later phases refer back to normalized provenance
- the raw event resolver can hydrate an original raw event by reading the exact byte slice from the source file

This gives the project:

- lower disk usage than a full raw mirror
- exact traceability back to original session logs
- rebuildability
- stricter separation between raw source-of-truth and derived memory products

## Configuration

### Core Config Files

- `config/source_roots.json`
  - where discovery looks for raw logs
- `config/product_config.json`
  - unified product config for memory model, adapters, output mode, bootstrap target, scheduler, and policies
- `config/classification_taxonomy.json`
  - labels, keywords, aliases, repo/path hints, and scoring behavior for Phase 4
- `config/extraction_rules.json`
  - extraction rules, item taxonomy behavior, and page-target mapping for Phase 5
- `config/wiki_config.json`
  - wiki page map, budgets, caps, renderer settings, and OpenAI provider/model settings for Phase 6
- `config/bootstrap_config.json`
  - bootstrap budgets, section caps, provider settings, and selection rules for Phase 7
- `config/audit_config.json`
  - stale windows, quality gates, and deterministic audit rules for Phase 8
- `config/refresh_config.json`
  - incremental orchestration config for Phase 9
- `config/full_load_config.json`
  - full-corpus gating, retry policy, control samples, and disk budget for Phase 10

### Environment Variables

Raw session root:

- `WIKIMEMORY_CODEX_SESSIONS_ROOT`

OpenAI-backed phases:

- `OPENAI_API_KEY`
- optional `WIKIMEMORY_OPENAI_MODEL`
- optional `WIKIMEMORY_OPENAI_BASE_URL`

Testing:

- `WIKIMEMORY_RUN_LIVE_TESTS=1`

### Local `.env`

The CLI loads a project `.env` file automatically, so local development can keep API keys or overrides in:

- `.env`

That file is ignored by git.

## Commands

Main commands:

```powershell
python -m wikimemory discover
python -m wikimemory normalize
python -m wikimemory ingest
python -m wikimemory memory
python -m wikimemory agent-bootstrap
python -m wikimemory memory-lint
python -m wikimemory memory-refresh
python -m wikimemory segment
python -m wikimemory classify
python -m wikimemory extract
python -m wikimemory wiki
python -m wikimemory bootstrap
python -m wikimemory audit
python -m wikimemory refresh
python -m wikimemory full-load
```

Tests:

```powershell
python -m unittest discover -s tests -v
$env:WIKIMEMORY_RUN_LIVE_TESTS=1
python -m unittest tests.test_live_corpus -v
```

Most phase commands support standard path overrides and optional scoping by `--source-id` where applicable.

## Recommended Operating Modes

### First Setup

1. Point your code agent to `START_HERE_FOR_AGENT.md`
2. Or run:

```powershell
python -m wikimemory onboard
```

3. Configure `config/source_roots.json` or set `WIKIMEMORY_CODEX_SESSIONS_ROOT`
4. Set `OPENAI_API_KEY`
5. Run:

```powershell
python -m wikimemory refresh
```

### Daily Usage

For normal operation:

```powershell
python -m wikimemory refresh
```

### Full Corpus Pass

For a strict end-to-end gated run:

```powershell
python -m wikimemory full-load
```

### Focused Repair or Experiment Work

When iterating on one problem area, rerun only the later phases you changed. Example:

```powershell
python -m wikimemory extract
python -m wikimemory wiki
python -m wikimemory bootstrap
python -m wikimemory audit
```

## Wiki Output Model

The wiki is organized into:

- `global/`
- `projects/<project-a>/`
- `projects/<project-b>/`
- `projects/<project-c>/`
- `projects/<shared-or-cross-project>/`

Typical page buckets:

- `index.md`
- `communication-preferences.md`
- `workflow-rules.md`
- `architecture.md`
- `code-map.md`
- `current-state.md`
- `tasks.md`
- `outcomes.md`
- `failures.md`
- `decisions.md`
- `next-steps.md`
- `open-questions.md`

Every rendered page has a structured manifest under `wiki/_meta/pages/...`.

Those manifests are important because they capture:

- synthesized claims
- supporting extracted item ids
- provenance refs
- page metadata

The markdown is human-facing. The manifests are machine-facing.

## Example Raw Input

If you need to show another model what the source data looks like without exposing the full external corpus, use:

- `examples/source-logs/representative-session.jsonl`

That file is a real session log chosen because it is small but still demonstrates:

- the `session_meta` opening record
- user and assistant messages
- commentary updates
- reasoning records
- tool/function calls and outputs
- token-count and task lifecycle events

## Bootstrap Output Model

Bootstrap outputs are much smaller than the wiki and are designed to be used as startup memory.

Each bootstrap file is paired with a manifest that resolves:

- bullet ids
- supporting extracted item keys
- supporting wiki claim ids
- conflict markers when applicable

That lets the project keep bootstrap markdown compact while preserving exact evidence outside the body.

## LLM Usage Boundaries

This project is not “LLM everywhere.”

Deterministic phases:

- discovery
- normalization
- segmentation
- classification
- extraction
- audit
- refresh orchestration
- full-load orchestration

Hybrid phases:

- wiki synthesis
- bootstrap compression

LLM rules:

- the LLM never replaces provenance
- the LLM never owns the core source model
- the LLM receives bounded evidence packets
- the LLM must return structured output
- synthesized claims are validated
- generic filler is filtered

## Current Quality Controls

Notable controls that now exist:

- pointer-first normalization to avoid full raw duplication
- conservative deterministic extraction with durability metadata
- global-rule pollution suppression
- project-aware routing for rules/preferences
- empty wiki page suppression
- page budgets and size caps
- summary validation against generic filler
- audit checks for transient rule pollution and wiki quality
- incremental refresh logic
- full-load disk-budget enforcement

## Testing Strategy

The test suite includes:

- unit tests
- regression tests
- integration tests
- env-gated live-corpus tests

Live-corpus coverage exists because synthetic tests alone are not enough for this project. The pipeline must survive real session traces, real noise, and real scale.

The live-corpus suite uses:

- representative real source ids
- temporary output directories
- stubbed LLM calls where appropriate

This keeps live validation meaningful without turning tests into full production runs.

## What Makes This Project Different

This project is not just a log indexer and not just a summarizer.

It is a layered memory system that tries to preserve:

- exact provenance
- domain separation
- temporal vs durable distinctions
- deterministic intermediate artifacts
- bounded LLM synthesis
- operational rebuildability

That combination is the real product.

## Current Status

At the time this README was expanded, the project includes:

- Phases 1-10 implemented
- pointer-first Phase 2 migration completed
- full-corpus run completed successfully
- wiki quality remediation completed
- Obsidian-compatible wiki rendering
- GitHub-backed repo now set up

The system is usable end-to-end, but it should still be treated as an evolving memory pipeline rather than a frozen final product. The most likely future work areas are:

- better ranking and compaction of temporal knowledge
- richer contradiction handling
- better project relationship synthesis
- operational monitoring around scheduled refresh/full-load runs

## If You Need To Explain This Project To Another Model

A good one-paragraph explanation is:

WikiMemory is a multi-phase memory pipeline for agent session logs. It discovers raw session traces without copying them into the repo, normalizes them into pointer-based canonical events, segments them into work units, classifies those units into domains, extracts structured durable and temporal knowledge with provenance, synthesizes a readable memory layer using bounded LLM-backed summaries over deterministic evidence, compresses the highest-signal subset into bootstrap memory for future agent sessions, audits the outputs for contradictions, drift, and quality issues, and supports both incremental refreshes and strict full-corpus runs with phase gates.

And the shortest explanation is:

WikiMemory turns raw agent logs into a provenance-backed memory and startup layer through deterministic preprocessing plus bounded LLM synthesis.
