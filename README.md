# WikiMemory

WikiMemory is a file-based memory pipeline for external Codex session logs.

Its job is to turn raw `.jsonl` session traces into:

- structured normalized events
- segmented conversational/work units
- deterministic domain classification
- extracted knowledge items
- synthesized wiki pages
- compact bootstrap memory for future agents
- audit findings over the entire memory layer

The project is designed to preserve provenance, stay incremental, and keep the raw source logs outside the repo. The raw logs remain the source of truth. Everything inside this repository is a derived artifact, control file, config, test, or generated knowledge output.

## Why This Exists

Codex session logs contain a large amount of useful information, but they are difficult to reuse directly:

- they are append-only raw traces
- they mix user intent, agent reasoning, tool calls, code work, status chatter, and planning
- they are not organized by project/domain knowledge
- they are too large and noisy to load directly into future sessions

WikiMemory solves that by building a layered pipeline:

1. discover the raw sessions
2. normalize them into a stable internal representation
3. segment them into meaningful spans
4. classify those spans into domains
5. extract durable and temporal knowledge
6. synthesize a human-readable wiki
7. compress the best subset into startup/bootstrap memory
8. audit the outputs for contradictions, drift, provenance gaps, and quality issues
9. orchestrate incremental refreshes
10. support controlled full-corpus loading with gates and disk-budget limits

## Design Principles

- Raw logs are the source of truth.
- Derived artifacts are disposable and rebuildable.
- Provenance is mandatory.
- Incremental operation matters.
- Deterministic structure comes before LLM synthesis.
- LLM use is bounded and evidence-backed, not freeform.
- Knowledge should be compressed progressively, not copied blindly.
- Fixes should generalize across the corpus, not overfit one sample.

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
- `ai-trader`
- `open-brain`
- `ai-scientist`
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

1. Configure `config/source_roots.json` or set `WIKIMEMORY_CODEX_SESSIONS_ROOT`
2. Set `OPENAI_API_KEY`
3. Run:

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
- `projects/ai-trader/`
- `projects/open-brain/`
- `projects/ai-scientist/`
- `projects/cross-project/`

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

WikiMemory is a multi-phase memory pipeline for external Codex session logs. It discovers raw `.jsonl` sessions without copying them into the repo, normalizes them into pointer-based canonical events, segments them into work units, classifies those units into domains such as global, ai-trader, open-brain, ai-scientist, and cross-project, extracts structured durable and temporal knowledge with provenance, synthesizes an Obsidian-compatible wiki using bounded OpenAI-backed summaries over deterministic evidence, compresses the highest-signal subset into bootstrap memory for future agents, audits the outputs for contradictions/drift/quality issues, and supports both incremental daily refreshes and strict full-corpus runs with disk-budget and phase gates.

And the shortest explanation is:

WikiMemory turns raw Codex logs into a provenance-backed wiki and startup memory layer through deterministic preprocessing plus bounded LLM synthesis.
