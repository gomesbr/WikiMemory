---
type: project-memory
project: open-brain
updated: 2026-04-21T05:01:53.135380Z
tags: [project/open-brain, memory]
---

# Open Brain - Project Memory

## PURPOSE

- OpenBrain is a local-first personal memory intelligence system (Postgres + pgvector, REST + MCP) that ingests multi-source history (notably WhatsApp/ChatGPT/Grok/CodexClaw), supports Ask + Network experiences, and runs benchmark/calibration workflows to improve retrieval and reasoning quality over real corpus evidence.
- OpenBrain work focuses on improving case-generation/review calibration quality (especially human WhatsApp-derived cases) and hardening cleanup+refill loops to maintain a no-gap pending/reviewable pool.

## CORE COMPONENTS

- Runtime configuration uses `runtime_settings` plus shared loader `libs/common/src/settings.ts`; ingest, execution, worker, and incidents logic read DB-backed settings dynamically.
- Primary implementation surfaces include `src/v2_ask.ts`, `src/v2_search.ts`, `src/v2_mesh.ts`, `src/v2_experiments.ts`, `src/v2_network.ts`, `src/server.ts`, and `src/ui.ts`; scripts under `src/scripts/` drive imports, re-embed/reextract, benchmark, strategy loop, and network/actor backfills.
- Core logic is centered in `src/v2_experiments.ts` with whole-corpus family-first mining and monitor orchestration (`generated/strategy_program/monitor_whole_corpus_family_backfill.ps1`), plus logs under `generated/strategy_program/*backfill*.log`; outcomes surface through existing experiment/readiness/overview payloads.

## CURRENT ARCHITECTURE

- Intended V2 data flow is canonical-first: ingest into `memory_items` -> canonicalize into `canonical_messages` -> embed canonicalized text -> build derived/aggregate artifacts; retrieval should be canonical-first.
- Persistent memory pipeline stores markdown turns at `store/memory/<chat>/YYYY-MM-DD.md` and indexes chunks in SQLite (`memory_chunks`, `memory_fts`) for retrieval into prompts.

## DIRECTORY TREE

`cd C:\Users\Fabio\Cursor AI projects\Projects\OpenBrain; tree /F /A`

```text
OpenBrain/
|-- backups/
|   `-- openbrain_20260304_010732.sql
|-- generated/
|   |-- actor_pronoun_review/
|   |   |-- actor_prefix_noise_merge_preview.json
|   |   |-- low_confidence_actor_pronouns.csv
|   |   |-- low_confidence_actor_pronouns.json
|   |   |-- low_confidence_actor_pronouns_review_sheet.csv
|   |   |-- low_confidence_actor_pronouns_review_sheet.overwritten_backup.csv
|   |   |-- they_actor_pronouns.csv
|   |   |-- they_actor_pronouns.json
|   |   |-- they_actor_pronouns_review_sheet.csv
|   |   |-- they_actor_pronouns_review_sheet.overwritten_backup.csv
|   |   |-- they_actor_pronouns_review_sheet_round2.csv
|   |   |-- they_actor_pronouns_review_sheet_round2.pre_refresh_backup.csv
|   |   `-- they_actor_pronouns_review_sheet_round3.csv
|   |-- actor_pronoun_review_refresh_tmp/
|   |   |-- low_confidence_actor_pronouns.csv
|   |   |-- low_confidence_actor_pronouns.json
|   |   |-- they_actor_pronouns.csv
|   |   `-- they_actor_pronouns.json
|   |-- actor_pronoun_review_round3_tmp/
|   |   |-- low_confidence_actor_pronouns.csv
|   |   |-- low_confidence_actor_pronouns.json
|   |   |-- they_actor_pronouns.csv
|   |   `-- they_actor_pronouns.json
|   |-- actor_review/
|   |   |-- actor_delete_ids_user.txt
|   |   |-- actor_merge_candidates.csv
|   |   |-- actor_samples.json
|   |   |-- actor_suspicious.csv
|   |   |-- actors_before_replay.csv
|   |   |-- actors_full.csv
|   |   |-- new_actors_after_replay.csv
|   |   |-- not_suspicious_ids_user.txt
|   |   |-- replay_memory_targets.tsv
|   |   |-- tmp_delete_group_like.txt
|   |   `-- tmp_merge_empty.tsv
|   |-- chat_transcripts/
|   |   |-- openbrain_chat_transcript_2026-03-02_to_2026-03-08_utf8.md
|   |   |-- openbrain_chat_transcript_2026-03-02_to_2026-03-08_utf8.txt
|   |   `-- openbrain_chat_transcript_2026-03-08_to_2026-03-14_utf8.md
|   |-- emoji/
|   |   |-- README.md
|   |   |-- whatsapp_emoji_catalog_all.csv
|   |   `-- whatsapp_emoji_catalog_all.json
|   |-- strategy_program/
|   |   |-- backfill_unique_families.err.log
|   |   |-- backfill_unique_families.log
|   |   |-- backfill_unique_families.ts
|   |   |-- benchmark_authoring_call_times.jsonl
|   |   |-- cpu_guard.log
|   |   |-- cpu_guard.ps1
|   |   |-- cpu_guard.stderr.log
|   |   |-- cpu_guard.stdout.log
|   |   |-- engineering_backlog.md
|   |   |-- loop_2efee43d-c2a8-48a6-aeb4-cb947357c6ac.err.log
|   |   |-- loop_2efee43d-c2a8-48a6-aeb4-cb947357c6ac.log
|   |   |-- loop_b922379a-73be-44a8-891e-d635c9ed1ab0.err.log
|   |   |-- loop_b922379a-73be-44a8-891e-d635c9ed1ab0.log
|   |   |-- loop_cc438d69-e2d4-45f7-a85a-d492ef3ef4f1.err.log
|   |   |-- loop_cc438d69-e2d4-45f7-a85a-d492ef3ef4f1.log
|   |   |-- loop_f4759905-d02c-49cc-8b25-debeed5b6737.err.log
|   |   |-- loop_f4759905-d02c-49cc-8b25-debeed5b6737.log
|   |   |-- monitor_launch.stderr.log
|   |   |-- monitor_launch.stdout.log
|   |   |-- monitor_process_stderr.log
|   |   |-- monitor_process_stdout.log
|   |   |-- monitor_runner_stderr.log
|   |   |-- monitor_runner_stdout.log
|   |   |-- monitor_whole_corpus_family_backfill.ps1
|   |   |-- pending_ai_refresh.log
|   |   |-- reseed_taxonomy_v2.log
|   |   |-- reset_reseed_stderr.log
|   |   |-- reset_reseed_stdout.log
|   |   |-- smoke_server_4311.err.log
|   |   |-- smoke_server_4311.out.log
|   |   |-- sms_state_2efee43d-c2a8-48a6-aeb4-cb947357c6ac.json
|   |   |-- sms_state_b922379a-73be-44a8-891e-d635c9ed1ab0.json
|   |   |-- sms_state_cc438d69-e2d4-45f7-a85a-d492ef3ef4f1.json
|   |   |-- sms_watch_2efee43d-c2a8-48a6-aeb4-cb947357c6ac.err.log
|   |   |-- sms_watch_2efee43d-c2a8-48a6-aeb4-cb947357c6ac.log
|   |   |-- sms_watch_b922379a-73be-44a8-891e-d635c9ed1ab0.err.log
|   |   |-- sms_watch_b922379a-73be-44a8-891e-d635c9ed1ab0.log
|   |   |-- sms_watch_b922379a-73be-44a8-891e-d635c9ed1ab0.stdout.log
|   |   |-- sms_watch_cc438d69-e2d4-45f7-a85a-d492ef3ef4f1.err.log
|   |   |-- sms_watch_cc438d69-e2d4-45f7-a85a-d492ef3ef4f1.log
|   |   |-- sms_watch_fatal.log
|   |   |-- start_sms_watch.ps1
|   |   |-- strategy_knowledge.jsonl
|   |   |-- whole_corpus_backfill.log
|   |   |-- whole_corpus_family_backfill.log
|   |   |-- whole_corpus_family_backfill_blocklist.json
|   |   |-- whole_corpus_family_backfill_cursor.json
|   |   |-- whole_corpus_family_backfill_monitor.log
|   |   |-- whole_corpus_family_backfill_rejections.jsonl
|   |   |-- whole_corpus_family_backfill_runner.stderr.log
|   |   |-- whole_corpus_family_backfill_runner.stdout.log
|   |   `-- whole_corpus_family_backfill_runner.ts
|   |-- test_candidates/
|   |   |-- type_domain_found_dbsignals.csv
|   |   |-- type_domain_found_dbsignals_v2.csv
|   |   |-- type_domain_matrix.csv
|   |   |-- type_domain_matrix_dbsignals.csv
|   |   |-- type_domain_matrix_dbsignals_v2.csv
|   |   |-- type_domain_missing.csv
|   |   |-- type_domain_missing_dbsignals.csv
|   |   `-- type_domain_missing_dbsignals_v2.csv
|   |-- dq_audit_20260305_173341.json
|   |-- dq_audit_20260305_180156.json
|   |-- dq_audit_latest.json
|   |-- tmp_ui_script_check.js
|   |-- v2_bootstrap_then_rebuild.log
|   |-- v2_bootstrap_then_rebuild_test.log
|   `-- video_9d5bzxVsocw_transcript.txt
|-- sql/
|   `-- 001_init.sql
|-- src/
|   |-- importers/
|   |   |-- chatgpt.ts
|   |   |-- codexclaw.ts
|   |   |-- grok.ts
|   |   `-- whatsapp.ts
|   |-- scripts/
|   |   |-- backup.ps1
|   |   |-- backup.sh
|   |   |-- common.ts
|   |   |-- dq_audit.ts
|   |   |-- dq_repair_full.ts
|   |   |-- generate_emoji_catalog.ts
|   |   |-- import_chatgpt.ts
|   |   |-- import_codexclaw.ts
|   |   |-- import_grok.ts
|   |   |-- import_whatsapp.ts
|   |   |-- metadata_queue_autoswitch.ps1
|   |   |-- metadata_queue_fill.ts
|   |   |-- metadata_queue_progress.ts
|   |   |-- metadata_queue_run_sequence.ps1
|   |   |-- metadata_queue_worker.ts
|   |   |-- openbrain_restart_all.ps1
|   |   |-- reembed_all.ts
|   |   |-- reembed_failed_mock_rows.ts
|   |   |-- reextract_metadata.ts
|   |   |-- refresh_corpus_semantics.ts
|   |   |-- replay_missing_whatsapp.ts
|   |   |-- restore.ps1
|   |   |-- restore.sh
|   |   |-- sanity_check_dates.ts
|   |   |-- v2_actor_prefix_noise_merge.ts
|   |   |-- v2_actor_pronoun_review_apply.ts
|   |   |-- v2_actor_pronoun_review_export.ts
|   |   |-- v2_actor_pronouns_backfill.ts
|   |   |-- v2_actor_review_apply.ts
|   |   |-- v2_actor_review_export.ts
|   |   |-- v2_bench_generate.ts
|   |   |-- v2_bench_run.ts
|   |   |-- v2_bench_signal.ts
|   |   |-- v2_benchmark_second_pass_cleanup.ts
|   |   |-- v2_bootstrap_then_rebuild.ps1
|   |   |-- v2_calibration.ts
|   |   |-- v2_experiment_reset_reseed.ts
|   |   |-- v2_network_backfill.ts
|   |   |-- v2_quality_bootstrap.ts
|   |   |-- v2_strategy_loop.ts
|   |   |-- v2_strategy_report.ts
|   |   |-- v2_strategy_sms_watch.ts
|   |   |-- v2_strategy_start.ts
|   |   |-- v2_strategy_step.ts
|   |   |-- wait_reembed_then_rebuild.ps1
|   |   `-- watch_reembed.ps1
|   |-- tests/
|   |   |-- chatgpt_importer.test.ts
|   |   |-- codexclaw_importer.test.ts
|   |   |-- domain_inference.test.ts
|   |   |-- finance_intent.test.ts
|   |   |-- grok_importer.test.ts
|   |   |-- network_graph.test.ts
|   |   |-- privacy.test.ts
|   |   |-- query_time.test.ts
|   |   |-- scripts_common.test.ts
|   |   |-- semantic_text.test.ts
|   |   |-- timestamp_normalization.test.ts
|   |   `-- whatsapp_importer.test.ts
|   |-- auth.ts
|   |-- brain.ts
|   |-- config.ts
|   |-- db.ts
|   |-- domain_inference.ts
|   |-- embedding_provider.ts
|   |-- finance_intent.ts
|   |-- mcp_http.ts
|   |-- metadata_provider.ts
|   |-- notify_sms.ts
|   |-- privacy.ts
|   |-- query_time.ts
|   |-- schema.ts
|   |-- sdk.ts
|   |-- semantic_text.ts
|   |-- server.ts
|   |-- session.ts
|   |-- time.ts
|   |-- types.ts
|   |-- ui.ts
|   |-- v2_ask.ts
|   |-- v2_benchmarks.ts
|   |-- v2_capabilities.ts
|   |-- v2_experiments.ts
|   |-- v2_mesh.ts
|   |-- v2_network.ts
|   |-- v2_pipeline.ts
|   |-- v2_protocol.ts
|   |-- v2_quality.ts
|   |-- v2_runtime.ts
|   |-- v2_search.ts
|   |-- v2_services.ts
|   `-- v2_types.ts
|-- _tmp_inline_script.js
|-- _tmp_login_page.html
|-- docker-compose.yml
|-- Dockerfile
|-- package-lock.json
|-- package.json
|-- PHASE2_EXECUTION_CHECKLIST.md
|-- README.md
|-- reprocess_tables.err.log
|-- reprocess_tables.out.log
|-- run_reprocess_tables.ps1
`-- tsconfig.json
```

## KEY CONSTRAINTS

- Benchmark/test cases and expected answers must be grounded in real DB/published evidence with provenance; synthetic expected answers are not allowed.
- Prioritize quality over speed; avoid lower-quality shortcuts, and minimize repeated full re-ingests by preferring in-place corrective passes plus a final remediation pass.
- Enforce CPU safety: avoid sustained 100% utilization; if high CPU persists per guard policy, throttle services stepwise and stop loop at minimum caps with logging.
- Scope improvements and generation to the whole published corpus/dataset rather than narrow domain-only/refill-only patches.
- Maintain diversity across source/conversation types and prioritize human conversations (WhatsApp individual/group) over assistant-centric threads.
- When ambiguity is detected, ask exactly one short, specific, open-ended clarification question and stop before final answering.
- Avoid overbuilding domain-specific permanent tables; keep most interpretation logic in the agent loop with bounded context/thread reads and strong indexing.
- Prevent cross-project instruction contamination; OpenBrain runtime prompt/config scope must be isolated so unrelated methodology updates do not alter project agents.

## OPEN PROBLEMS

- Recurring risk: actor-resolution drift in WhatsApp/legacy imports (missing actor IDs/metadata/parser issues/Unicode artifacts) can produce wrong speaker labels and incorrect summaries.

## BACKLOG

1. Implement cross-project agent access to OpenBrain via REST + MCP + shared SDK with service identities, scoped permissions, namespace isolation, policy enforcement, and audit logging.
2. Evolve People/Network toward a broader user-centered relationship graph with categorized connection types and richer context.
3. Phase 2: build persistent Network investigation workspace with conversational follow-ups, contextual reference resolution, and coordinated answer + scene + evidence updates.
4. Run second-pass retagging to correct wrong domain/lens labels after whole-dataset generation.
5. Improve `domain_inference.ts` (and related classifier logic) then run full corpus semantic refresh/canonical sync to reduce stale row labeling and improve discovery accuracy.
6. Fix concrete-cue extraction/tokenization for non-ASCII text (e.g., Spanish/Portuguese) so grounding/oracle checks retain salient words and do not incorrectly reject valid human WhatsApp threads.

## RELATED

- [[projects/open-brain/recent|Open Brain Recent]]
- [[projects/open-brain/rules|Open Brain Rules]]
- [[global/user-rules|Global User Rules]]
