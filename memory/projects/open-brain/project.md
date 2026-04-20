---
type: project-memory
project: open-brain
updated: 2026-04-20T01:19:51.506162Z
tags: [project/open-brain, memory]
---

# Open Brain - Project Memory

## PURPOSE

- OpenBrain is a local-first memory and reasoning platform on Postgres+pgvector with REST/MCP interfaces, focused on Ask-first grounded answers and benchmark/calibration-driven quality improvement over real user data; graph/network views are explanation and investigation surfaces layered on the same evidence-backed retrieval core.

## CORE COMPONENTS

- Core architecture is TypeScript/Node with Dockerized API+Postgres, pgvector-centered retrieval, importer pipelines (ChatGPT/Grok/WhatsApp/CodexClaw), V2 ask/mesh/search/experiments modules, and DB-backed long-running operational scripts/queues.

## CURRENT ARCHITECTURE

_No selected items from this evidence._

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

_No selected items from this evidence._

## OPEN PROBLEMS

_No selected items from this evidence._

## BACKLOG

1. Deferred Phase 2: build Network as a persistent multi-turn investigation workspace (scene memory, reference resolution, coordinated answer+scene updates, richer evidence tabs) after Phase 1 Ask→Graph contract work.
2. Network polish backlog: improve central stage visual/interaction quality (collisions, icon/label alignment, drilldown scaling, +N expansion interaction, consistent category/friend color semantics).
3. Backlog includes systematic case-quality cleanup work: remove malformed/duplicate/low-value items, improve summary/reviewer rationale quality, and apply holistic retroactive fixes when defect classes are discovered.
4. Investigate and document the People→Network data pipeline/source-of-truth details as groundwork for broader relationship graph evolution centered on the user entity.
5. Deferred experiment-loop enhancements: statistical early stopping/elimination, background research waves, richer scoreboard/history, and more complex multi-agent debate only if hybrid review underperforms.

## RELATED

- [[projects/open-brain/recent|Open Brain Recent]]
- [[projects/open-brain/rules|Open Brain Rules]]
- [[global/user-rules|Global User Rules]]
