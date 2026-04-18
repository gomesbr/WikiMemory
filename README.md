# WikiMemory

Phase 1-10 discovery, normalization, segmentation, classification, extraction, wiki synthesis, bootstrap memory generation, audit validation, incremental refresh orchestration, and full-corpus load control for external Codex session logs.

## What It Does

- discovers every `.jsonl` log under one or more configured external roots
- assigns stable logical identity from `session_meta.payload.id`
- stores only derived state in this repo
- keeps Phase 2 pointer-first by storing event byte ranges, bounded text surfaces, and canonical fields instead of a full raw-event mirror
- supports append-aware rescans for active files
- detects identical duplicates, tombstones missing files, and stops on conflicting anomalies

## Configuration

Edit [config/source_roots.json](config/source_roots.json) if you need additional roots or aliases.
Edit [config/classification_taxonomy.json](config/classification_taxonomy.json) to tune deterministic project/global classification rules.
Edit [config/extraction_rules.json](config/extraction_rules.json) to tune deterministic knowledge extraction rules and target page mappings.
Edit [config/wiki_config.json](config/wiki_config.json) to tune page layout, Obsidian rendering, and OpenAI-backed wiki synthesis.
Edit [config/bootstrap_config.json](config/bootstrap_config.json) to tune bootstrap budgets, section caps, and OpenAI-backed compression.
Edit [config/audit_config.json](config/audit_config.json) to tune stale-item windows and deterministic audit rules.
Edit [config/refresh_config.json](config/refresh_config.json) to tune the daily refresh orchestration inputs and lock settings.
Edit [config/full_load_config.json](config/full_load_config.json) to tune strict full-corpus phase gates, retry limits, live control-sample references, and derived-disk budget enforcement.

The default root uses an environment override with a local fallback:

- `WIKIMEMORY_CODEX_SESSIONS_ROOT`

If you move your sessions folder to another drive, update that environment variable and rerun discovery.

Wiki synthesis uses OpenAI-backed structured generation in Phase 6. Set:

- `OPENAI_API_KEY`
- optional `WIKIMEMORY_OPENAI_MODEL`
- optional `WIKIMEMORY_OPENAI_BASE_URL`

## Commands

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
python -m unittest discover -s tests -v
$env:WIKIMEMORY_RUN_LIVE_TESTS=1; python -m unittest tests.test_live_corpus -v
```

`python -m wikimemory discover` writes:

- `state/source_registry.json`
- `state/discovery_runs.jsonl`

`python -m wikimemory normalize` writes:

- `state/normalization_state.json`
- `state/normalization_runs.jsonl`
- `audits/normalization_notices.jsonl`
- `normalized/sources/<source_id>/session.json`
- `normalized/sources/<source_id>/events.jsonl`
- `normalized/sources/<source_id>/stats.json`

Phase 2 normalized events are provenance-first:

- keep `source_line_no`, `source_byte_start`, `source_byte_end`, `event_digest`, canonical fields, and bounded `text_surfaces`
- set `text_surface_truncated` when later phases may need lazy raw hydration
- do not persist `raw_event`

`python -m wikimemory segment` writes:

- `state/segmentation_state.json`
- `state/segmentation_runs.jsonl`
- `segmented/sources/<source_id>/session_flow.json`
- `segmented/sources/<source_id>/segments.jsonl`
- `segmented/sources/<source_id>/stats.json`

`python -m wikimemory classify` writes:

- `state/classification_state.json`
- `state/classification_runs.jsonl`
- `audits/classification_notices.jsonl`
- `classified/sources/<source_id>/segments.jsonl`
- `classified/sources/<source_id>/stats.json`

`python -m wikimemory extract` writes:

- `state/extraction_state.json`
- `state/extraction_runs.jsonl`
- `audits/extraction_notices.jsonl`
- `extracted/sources/<source_id>/items.jsonl`
- `extracted/sources/<source_id>/stats.json`
- `extracted/domains/<domain>/items.jsonl`

`python -m wikimemory wiki` writes:

- `state/wiki_state.json`
- `state/wiki_runs.jsonl`
- `audits/wiki_notices.jsonl`
- `wiki/global/...`
- `wiki/projects/<domain>/...`
- `wiki/_meta/pages/...`

`python -m wikimemory bootstrap` writes:

- `state/bootstrap_state.json`
- `state/bootstrap_runs.jsonl`
- `audits/bootstrap_notices.jsonl`
- `bootstrap/global.md`
- `bootstrap/projects/<domain>.md`
- `bootstrap/_meta/...`

`python -m wikimemory audit` writes:

- `state/audit_state.json`
- `state/audit_runs.jsonl`
- `audits/contradictions.jsonl`
- `audits/duplicates.jsonl`
- `audits/stale_items.jsonl`
- `audits/provenance_gaps.jsonl`
- `audits/wiki_bootstrap_drift.jsonl`

`python -m wikimemory refresh` writes:

- `state/refresh_state.json`
- `state/refresh_runs.jsonl`
- `audits/refresh_notices.jsonl`
- `state/refresh.lock.json` while a run is active

`python -m wikimemory full-load` writes:

- `state/full_load_state.json`
- `state/full_load_runs.jsonl`
- `audits/full_load_notices.jsonl`
- `audits/full_load_issues/<run_id>/<phase>/issue.json`
