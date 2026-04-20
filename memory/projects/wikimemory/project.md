---
type: project-memory
project: wikimemory
updated: 2026-04-20T01:19:51.517367Z
tags: [project/wikimemory, memory]
---

# Wikimemory - Project Memory

## PURPOSE

- WikiMemory is a file-based, multi-phase memory pipeline that ingests external immutable Codex JSONL logs and produces compact, provenance-backed operational memory outputs (including memory/ artifacts, wiki pages, and bootstrap memory) for future coding agents with high signal and low token cost.

## CORE COMPONENTS

_No selected items from this evidence._

## CURRENT ARCHITECTURE

- The architecture is phased and manifest/state-driven: discovery -> normalization -> ingest/evidence -> segmentation -> classification -> extraction -> wiki synthesis -> bootstrap -> audit, with orchestration commands for refresh/full-load and per-phase state, notices, and rerun support.
- Normalization is pointer-first: store provenance pointers and bounded canonical text instead of raw_event mirrors, and use RawEventResolver for exact on-demand hydration when deeper raw context is required.

## DIRECTORY TREE

`cd C:\Users\Fabio\Cursor AI projects\Projects\WikiMemory; tree /F /A`

```text
WikiMemory/
|-- audits/
|   |-- full_load_issues/
|   |   `-- full-load-20260418T211436259835Z/
|   |       `-- bootstrap/
|   |           `-- issue.json
|   |-- agent_bootstrap_notices.jsonl
|   |-- bootstrap_notices.jsonl
|   |-- classification_notices.jsonl
|   |-- contradictions.jsonl
|   |-- duplicates.jsonl
|   |-- extraction_notices.jsonl
|   |-- full_load_notices.jsonl
|   |-- ingest_notices.jsonl
|   |-- memory_lint_findings.jsonl
|   |-- memory_notices.jsonl
|   |-- memory_review_items.jsonl
|   |-- normalization_notices.jsonl
|   |-- provenance_gaps.jsonl
|   |-- stale_items.jsonl
|   |-- wiki_bootstrap_drift.jsonl
|   |-- wiki_notices.jsonl
|   `-- wiki_quality.jsonl
|-- bootstrap/
|   |-- _meta/
|   |   |-- projects/
|   |   |   |-- ai-scientist.json
|   |   |   |-- ai-trader.json
|   |   |   |-- cross-project.json
|   |   |   `-- open-brain.json
|   |   `-- global.json
|   |-- projects/
|   |   |-- ai-scientist.md
|   |   |-- ai-trader.md
|   |   |-- cross-project.md
|   |   `-- open-brain.md
|   `-- global.md
|-- classified/
|   `-- sources/
|       |-- 019c687b-3d0d-71c0-8929-9128cbf24060/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9ca4-ac1c-76e2-b883-017d68d982a1/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9cff-0337-77e0-9ba6-a4f6dc75a92e/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d00-0d81-7b52-a1a9-84f7d4b05066/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d4c-657e-7d71-a062-4d77a75d3786/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d53-7494-7e83-8519-25d541393ee6/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d54-1089-7ad2-9f90-57be7710dcad/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d57-92b6-7382-a637-8c4251b63817/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d57-dec5-7f12-9b7a-20330759fbfd/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d58-ef98-7c71-b725-1f9074946181/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d5a-2434-77d2-b985-9f8045648610/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d5b-128f-7240-9aee-54b8ea2f59d7/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d5b-6fcd-7483-b5c6-2255c43b916d/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d5b-b1a6-7fc1-a6c4-c7c8abe77031/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d5b-e6cd-7db0-8980-b08248a4ba09/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d5c-55a5-7841-ab96-65ee521280b5/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d5d-6ca1-7763-9121-0be51be71a7b/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d5d-dc33-7ef2-b7cf-2e97f6231167/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d5e-15f7-7483-a5de-bac1f5d3e835/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d5e-3ea5-7503-a2c9-74d8f75a220b/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d5f-becf-7d83-9fb9-caa573e948b0/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d60-390c-7251-8e71-54bb184c5607/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d60-9b0d-71b0-be73-efa8033c9940/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d6a-1df2-7290-9e8a-1e3b28e2feb9/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d6b-6077-7c33-bb98-d1504ca0d6d4/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d6f-34ed-7dc1-a7cc-4209d931f215/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d7a-12c2-7fd1-8b96-7605c72fbbb9/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d81-8487-73e3-9a63-1fa7d23f7bad/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9d82-290f-7241-8d9e-f59b9f5e258b/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9f43-3a51-7052-ad49-94d4475d953a/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9f43-944f-7403-a8a0-8484dd96dfab/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9f44-cac1-7b13-9ce0-dfc4492316ba/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9f48-e770-78f0-b223-9600b20b6303/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9f49-ff0a-7e11-a8a3-c2bfe616580b/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9f4b-8acd-70d1-bd77-e2356d46b6f2/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9f56-e5d9-7d91-906a-cf263f2a4c84/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019c9f58-333b-7c52-a26d-bdc0709234c5/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca18a-3473-7743-a7c0-50d4922dea5d/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca2f8-b377-7703-acfb-1825c4c2f8b0/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca30c-78c3-7191-8deb-e42ed4b348ab/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca310-20e8-76f0-95aa-e213d3cb77cb/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca311-ed33-74d2-8f97-58ee853a1b59/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca320-9699-77b3-a669-546e27eb724e/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca5ea-9c32-7090-8985-3411f371f917/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca5f3-bf03-7fe0-9d95-760e31374dd0/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca5f9-374c-7d20-b8ad-9c8290adcde3/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca609-b3bb-73f3-aec5-c64a38059274/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca60d-f3c6-7f13-a9fc-bf9314e79b01/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca611-9dc1-7e00-9adb-b470f228ed85/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca617-1b99-7df1-ae0b-3a643924e117/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca617-3330-7b42-840a-81859188334e/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca61e-6ec1-7c91-aa53-1c61330da985/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca61e-8ac1-7503-a0f3-a553d43375fc/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca61e-a9a0-7a81-8663-461ed161f842/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca69a-b325-7540-84eb-61c29f4c1f7c/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca6fa-7ec5-7f71-ab37-96eb69672b2c/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca6fe-4e31-7b23-8705-b0e23f293d62/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca705-c215-7221-8e6a-d28b922add82/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca718-449c-73b1-b935-872a2422adf2/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca71b-c355-7731-9c8e-ff9f39e97ba3/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019ca78b-4fe3-73a3-9e4d-e077c637de74/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019caa7e-937d-7e72-95e8-631ca4b769b4/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019caaa7-2fe4-7a72-9693-6b998656746e/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cab13-b21e-76f3-9029-bcd0333cd3eb/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cab4e-ab00-7e31-b50f-faff8205252f/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019caca3-cd0b-73b0-99f0-1ef6221f7cae/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019caf95-fa0a-7900-9097-6dbda1513ef0/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019caf9f-c9e4-7d33-9635-28feaa5b3b4a/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cb0ef-a044-7090-9627-7f2d616c46f2/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cb0f9-2d39-7850-a9e1-11263a5a8783/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cb0fd-2d7f-7f81-9d7e-088d64565547/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cb0fd-cf4c-7520-baf2-de448646fff2/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cb0fe-5561-75f0-803f-0525f796830d/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cb0fe-a160-7362-85e0-720ad035cf30/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cb0ff-85d9-7cf1-8054-6fd4770fe9f2/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cb100-5540-7371-8eb5-a89bab51137b/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cb106-799e-7151-bf0b-76cd90d07e55/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cb148-7e62-79a3-af96-9f74a1edaa78/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cb162-d216-7f63-9eb0-f7c9cd446990/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cb166-459d-7a01-a948-70994c21d327/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cba69-7058-72e0-805d-180f5372e2bd/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       |-- 019cbacf-74e5-7411-a1ab-6595d49c26a2/
|       |   |-- segments.jsonl
|       |   `-- stats.json
|       `-- 019d837d-d249-71c3-9637-b8d6992ce805/
|           |-- segments.jsonl
|           `-- stats.json
|-- config/
|   |-- audit_config.json
|   |-- bootstrap_config.json
|   |-- classification_taxonomy.json
|   |-- extraction_rules.json
|   |-- full_load_config.json
|   |-- product_config.json
|   |-- refresh_config.json
|   |-- source_roots.json
|   `-- wiki_config.json
|-- docs/
|   `-- adapters.md
|-- evidence/
|   |-- logs/
|   |   |-- 019c687b-3d0d-71c0-8929-9128cbf24060.jsonl
|   |   |-- 019c9ca4-ac1c-76e2-b883-017d68d982a1.jsonl
|   |   |-- 019c9cff-0337-77e0-9ba6-a4f6dc75a92e.jsonl
|   |   |-- 019c9d00-0d81-7b52-a1a9-84f7d4b05066.jsonl
|   |   |-- 019c9d4c-657e-7d71-a062-4d77a75d3786.jsonl
|   |   |-- 019c9d53-7494-7e83-8519-25d541393ee6.jsonl
|   |   |-- 019c9d54-1089-7ad2-9f90-57be7710dcad.jsonl
|   |   |-- 019c9d57-92b6-7382-a637-8c4251b63817.jsonl
|   |   |-- 019c9d57-dec5-7f12-9b7a-20330759fbfd.jsonl
|   |   |-- 019c9d58-ef98-7c71-b725-1f9074946181.jsonl
|   |   |-- 019c9d5a-2434-77d2-b985-9f8045648610.jsonl
|   |   |-- 019c9d5b-128f-7240-9aee-54b8ea2f59d7.jsonl
|   |   |-- 019c9d5b-6fcd-7483-b5c6-2255c43b916d.jsonl
|   |   |-- 019c9d5b-b1a6-7fc1-a6c4-c7c8abe77031.jsonl
|   |   |-- 019c9d5b-e6cd-7db0-8980-b08248a4ba09.jsonl
|   |   |-- 019c9d5c-55a5-7841-ab96-65ee521280b5.jsonl
|   |   |-- 019c9d5d-6ca1-7763-9121-0be51be71a7b.jsonl
|   |   |-- 019c9d5d-dc33-7ef2-b7cf-2e97f6231167.jsonl
|   |   |-- 019c9d5e-15f7-7483-a5de-bac1f5d3e835.jsonl
|   |   |-- 019c9d5e-3ea5-7503-a2c9-74d8f75a220b.jsonl
|   |   |-- 019c9d5f-becf-7d83-9fb9-caa573e948b0.jsonl
|   |   |-- 019c9d60-390c-7251-8e71-54bb184c5607.jsonl
|   |   |-- 019c9d60-9b0d-71b0-be73-efa8033c9940.jsonl
|   |   |-- 019c9d6a-1df2-7290-9e8a-1e3b28e2feb9.jsonl
|   |   |-- 019c9d6b-6077-7c33-bb98-d1504ca0d6d4.jsonl
|   |   |-- 019c9d6f-34ed-7dc1-a7cc-4209d931f215.jsonl
|   |   |-- 019c9d7a-12c2-7fd1-8b96-7605c72fbbb9.jsonl
|   |   |-- 019c9d81-8487-73e3-9a63-1fa7d23f7bad.jsonl
|   |   |-- 019c9d82-290f-7241-8d9e-f59b9f5e258b.jsonl
|   |   |-- 019c9f43-3a51-7052-ad49-94d4475d953a.jsonl
|   |   |-- 019c9f43-944f-7403-a8a0-8484dd96dfab.jsonl
|   |   |-- 019c9f44-cac1-7b13-9ce0-dfc4492316ba.jsonl
|   |   |-- 019c9f48-e770-78f0-b223-9600b20b6303.jsonl
|   |   |-- 019c9f49-ff0a-7e11-a8a3-c2bfe616580b.jsonl
|   |   |-- 019c9f4b-8acd-70d1-bd77-e2356d46b6f2.jsonl
|   |   |-- 019c9f56-e5d9-7d91-906a-cf263f2a4c84.jsonl
|   |   |-- 019c9f58-333b-7c52-a26d-bdc0709234c5.jsonl
|   |   |-- 019ca18a-3473-7743-a7c0-50d4922dea5d.jsonl
|   |   |-- 019ca2f8-b377-7703-acfb-1825c4c2f8b0.jsonl
|   |   |-- 019ca30c-78c3-7191-8deb-e42ed4b348ab.jsonl
|   |   |-- 019ca310-20e8-76f0-95aa-e213d3cb77cb.jsonl
|   |   |-- 019ca311-ed33-74d2-8f97-58ee853a1b59.jsonl
|   |   |-- 019ca320-9699-77b3-a669-546e27eb724e.jsonl
|   |   |-- 019ca5ea-9c32-7090-8985-3411f371f917.jsonl
|   |   |-- 019ca5f3-bf03-7fe0-9d95-760e31374dd0.jsonl
|   |   |-- 019ca5f9-374c-7d20-b8ad-9c8290adcde3.jsonl
|   |   |-- 019ca609-b3bb-73f3-aec5-c64a38059274.jsonl
|   |   |-- 019ca60d-f3c6-7f13-a9fc-bf9314e79b01.jsonl
|   |   |-- 019ca611-9dc1-7e00-9adb-b470f228ed85.jsonl
|   |   |-- 019ca617-1b99-7df1-ae0b-3a643924e117.jsonl
|   |   |-- 019ca617-3330-7b42-840a-81859188334e.jsonl
|   |   |-- 019ca61e-6ec1-7c91-aa53-1c61330da985.jsonl
|   |   |-- 019ca61e-8ac1-7503-a0f3-a553d43375fc.jsonl
|   |   |-- 019ca61e-a9a0-7a81-8663-461ed161f842.jsonl
|   |   |-- 019ca69a-b325-7540-84eb-61c29f4c1f7c.jsonl
|   |   |-- 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5.jsonl
|   |   |-- 019ca6fa-7ec5-7f71-ab37-96eb69672b2c.jsonl
|   |   |-- 019ca6fe-4e31-7b23-8705-b0e23f293d62.jsonl
|   |   |-- 019ca705-c215-7221-8e6a-d28b922add82.jsonl
|   |   |-- 019ca718-449c-73b1-b935-872a2422adf2.jsonl
|   |   |-- 019ca71b-c355-7731-9c8e-ff9f39e97ba3.jsonl
|   |   |-- 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5.jsonl
|   |   |-- 019ca78b-4fe3-73a3-9e4d-e077c637de74.jsonl
|   |   |-- 019caa7e-937d-7e72-95e8-631ca4b769b4.jsonl
|   |   |-- 019caaa7-2fe4-7a72-9693-6b998656746e.jsonl
|   |   |-- 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0.jsonl
|   |   |-- 019cab13-b21e-76f3-9029-bcd0333cd3eb.jsonl
|   |   |-- 019cab4e-ab00-7e31-b50f-faff8205252f.jsonl
|   |   |-- 019caca3-cd0b-73b0-99f0-1ef6221f7cae.jsonl
|   |   |-- 019caf95-fa0a-7900-9097-6dbda1513ef0.jsonl
|   |   |-- 019caf9f-c9e4-7d33-9635-28feaa5b3b4a.jsonl
|   |   |-- 019cb0ef-a044-7090-9627-7f2d616c46f2.jsonl
|   |   |-- 019cb0f9-2d39-7850-a9e1-11263a5a8783.jsonl
|   |   |-- 019cb0fd-2d7f-7f81-9d7e-088d64565547.jsonl
|   |   |-- 019cb0fd-cf4c-7520-baf2-de448646fff2.jsonl
|   |   |-- 019cb0fe-5561-75f0-803f-0525f796830d.jsonl
|   |   |-- 019cb0fe-a160-7362-85e0-720ad035cf30.jsonl
|   |   |-- 019cb0ff-85d9-7cf1-8054-6fd4770fe9f2.jsonl
|   |   |-- 019cb100-5540-7371-8eb5-a89bab51137b.jsonl
|   |   |-- 019cb106-799e-7151-bf0b-76cd90d07e55.jsonl
|   |   |-- 019cb148-7e62-79a3-af96-9f74a1edaa78.jsonl
|   |   |-- 019cb162-d216-7f63-9eb0-f7c9cd446990.jsonl
|   |   |-- 019cb166-459d-7a01-a948-70994c21d327.jsonl
|   |   |-- 019cba69-7058-72e0-805d-180f5372e2bd.jsonl
|   |   |-- 019cbacf-74e5-7411-a1ab-6595d49c26a2.jsonl
|   |   `-- 019d837d-d249-71c3-9637-b8d6992ce805.jsonl
|   `-- projects/
|       |-- ai-trader.jsonl
|       |-- codexclaw.jsonl
|       |-- open-brain.jsonl
|       `-- wikimemory.jsonl
|-- examples/
|   |-- config/
|   |   `-- generic-log-adapter-template.json
|   |-- source-logs/
|   |   `-- representative-session.jsonl
|   `-- README.md
|-- experimental_exports/
|   `-- codex_chat_by_day/
|       |-- 2026-02-16-codex-chat.md
|       |-- 2026-02-17-codex-chat.md
|       |-- 2026-02-18-codex-chat.md
|       |-- 2026-02-21-codex-chat.md
|       |-- 2026-02-22-codex-chat.md
|       |-- 2026-02-23-codex-chat.md
|       |-- 2026-02-24-codex-chat.md
|       |-- 2026-02-25-codex-chat.md
|       |-- 2026-02-26-codex-chat.md
|       |-- 2026-02-27-codex-chat.md
|       |-- 2026-02-28-codex-chat.md
|       |-- 2026-03-01-codex-chat.md
|       |-- 2026-03-02-codex-chat.md
|       |-- 2026-03-03-codex-chat.md
|       |-- 2026-03-04-codex-chat.md
|       |-- 2026-03-05-codex-chat.md
|       |-- 2026-03-06-codex-chat.md
|       |-- 2026-03-07-codex-chat.md
|       |-- 2026-03-08-codex-chat.md
|       |-- 2026-03-09-codex-chat.md
|       |-- 2026-03-10-codex-chat.md
|       |-- 2026-03-11-codex-chat.md
|       |-- 2026-03-12-codex-chat.md
|       |-- 2026-03-13-codex-chat.md
|       |-- 2026-03-14-codex-chat.md
|       |-- 2026-03-15-codex-chat.md
|       |-- 2026-03-16-codex-chat.md
|       |-- 2026-03-17-codex-chat.md
|       |-- 2026-03-20-codex-chat.md
|       |-- 2026-03-21-codex-chat.md
|       |-- 2026-03-23-codex-chat.md
|       |-- 2026-03-24-codex-chat.md
|       |-- 2026-03-26-codex-chat.md
|       |-- 2026-03-27-codex-chat.md
|       |-- 2026-03-28-codex-chat.md
|       |-- 2026-04-12-codex-chat.md
|       |-- 2026-04-13-codex-chat.md
|       |-- 2026-04-14-codex-chat.md
|       |-- 2026-04-18-codex-chat.md
|       |-- 2026-04-19-codex-chat.md
|       `-- manifest.json
|-- extracted/
|   |-- domains/
|   |   |-- ai-scientist/
|   |   |   `-- items.jsonl
|   |   |-- ai-trader/
|   |   |   `-- items.jsonl
|   |   |-- cross-project/
|   |   |   `-- items.jsonl
|   |   |-- global/
|   |   |   `-- items.jsonl
|   |   `-- open-brain/
|   |       `-- items.jsonl
|   `-- sources/
|       |-- 019c687b-3d0d-71c0-8929-9128cbf24060/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9ca4-ac1c-76e2-b883-017d68d982a1/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9cff-0337-77e0-9ba6-a4f6dc75a92e/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d00-0d81-7b52-a1a9-84f7d4b05066/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d4c-657e-7d71-a062-4d77a75d3786/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d53-7494-7e83-8519-25d541393ee6/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d54-1089-7ad2-9f90-57be7710dcad/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d57-92b6-7382-a637-8c4251b63817/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d57-dec5-7f12-9b7a-20330759fbfd/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d58-ef98-7c71-b725-1f9074946181/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d5a-2434-77d2-b985-9f8045648610/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d5b-128f-7240-9aee-54b8ea2f59d7/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d5b-6fcd-7483-b5c6-2255c43b916d/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d5b-b1a6-7fc1-a6c4-c7c8abe77031/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d5b-e6cd-7db0-8980-b08248a4ba09/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d5c-55a5-7841-ab96-65ee521280b5/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d5d-6ca1-7763-9121-0be51be71a7b/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d5d-dc33-7ef2-b7cf-2e97f6231167/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d5e-15f7-7483-a5de-bac1f5d3e835/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d5e-3ea5-7503-a2c9-74d8f75a220b/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d5f-becf-7d83-9fb9-caa573e948b0/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d60-390c-7251-8e71-54bb184c5607/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d60-9b0d-71b0-be73-efa8033c9940/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d6a-1df2-7290-9e8a-1e3b28e2feb9/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d6b-6077-7c33-bb98-d1504ca0d6d4/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d6f-34ed-7dc1-a7cc-4209d931f215/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d7a-12c2-7fd1-8b96-7605c72fbbb9/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d81-8487-73e3-9a63-1fa7d23f7bad/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9d82-290f-7241-8d9e-f59b9f5e258b/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9f43-3a51-7052-ad49-94d4475d953a/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9f43-944f-7403-a8a0-8484dd96dfab/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9f44-cac1-7b13-9ce0-dfc4492316ba/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9f48-e770-78f0-b223-9600b20b6303/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9f49-ff0a-7e11-a8a3-c2bfe616580b/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9f4b-8acd-70d1-bd77-e2356d46b6f2/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9f56-e5d9-7d91-906a-cf263f2a4c84/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019c9f58-333b-7c52-a26d-bdc0709234c5/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca18a-3473-7743-a7c0-50d4922dea5d/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca2f8-b377-7703-acfb-1825c4c2f8b0/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca30c-78c3-7191-8deb-e42ed4b348ab/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca310-20e8-76f0-95aa-e213d3cb77cb/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca311-ed33-74d2-8f97-58ee853a1b59/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca320-9699-77b3-a669-546e27eb724e/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca5ea-9c32-7090-8985-3411f371f917/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca5f3-bf03-7fe0-9d95-760e31374dd0/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca5f9-374c-7d20-b8ad-9c8290adcde3/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca609-b3bb-73f3-aec5-c64a38059274/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca60d-f3c6-7f13-a9fc-bf9314e79b01/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca611-9dc1-7e00-9adb-b470f228ed85/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca617-1b99-7df1-ae0b-3a643924e117/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca617-3330-7b42-840a-81859188334e/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca61e-6ec1-7c91-aa53-1c61330da985/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca61e-8ac1-7503-a0f3-a553d43375fc/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca61e-a9a0-7a81-8663-461ed161f842/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca69a-b325-7540-84eb-61c29f4c1f7c/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca6fa-7ec5-7f71-ab37-96eb69672b2c/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca6fe-4e31-7b23-8705-b0e23f293d62/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca705-c215-7221-8e6a-d28b922add82/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca718-449c-73b1-b935-872a2422adf2/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca71b-c355-7731-9c8e-ff9f39e97ba3/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019ca78b-4fe3-73a3-9e4d-e077c637de74/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019caa7e-937d-7e72-95e8-631ca4b769b4/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019caaa7-2fe4-7a72-9693-6b998656746e/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cab13-b21e-76f3-9029-bcd0333cd3eb/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cab4e-ab00-7e31-b50f-faff8205252f/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019caca3-cd0b-73b0-99f0-1ef6221f7cae/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019caf95-fa0a-7900-9097-6dbda1513ef0/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019caf9f-c9e4-7d33-9635-28feaa5b3b4a/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cb0ef-a044-7090-9627-7f2d616c46f2/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cb0f9-2d39-7850-a9e1-11263a5a8783/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cb0fd-2d7f-7f81-9d7e-088d64565547/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cb0fd-cf4c-7520-baf2-de448646fff2/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cb0fe-5561-75f0-803f-0525f796830d/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cb0fe-a160-7362-85e0-720ad035cf30/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cb0ff-85d9-7cf1-8054-6fd4770fe9f2/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cb100-5540-7371-8eb5-a89bab51137b/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cb106-799e-7151-bf0b-76cd90d07e55/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cb148-7e62-79a3-af96-9f74a1edaa78/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cb162-d216-7f63-9eb0-f7c9cd446990/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cb166-459d-7a01-a948-70994c21d327/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cba69-7058-72e0-805d-180f5372e2bd/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       |-- 019cbacf-74e5-7411-a1ab-6595d49c26a2/
|       |   |-- items.jsonl
|       |   `-- stats.json
|       `-- 019d837d-d249-71c3-9637-b8d6992ce805/
|           |-- items.jsonl
|           `-- stats.json
|-- memory/
|   `-- _meta/
|       `-- daily/
|           |-- 2026-02-16.json
|           |-- 2026-02-17.json
|           |-- 2026-02-18.json
|           |-- 2026-02-21.json
|           |-- 2026-02-22.json
|           |-- 2026-02-23.json
|           |-- 2026-02-24.json
|           |-- 2026-02-25.json
|           |-- 2026-02-26.json
|           |-- 2026-02-27.json
|           |-- 2026-02-28.json
|           |-- 2026-03-01.json
|           |-- 2026-03-02.json
|           |-- 2026-03-03.json
|           |-- 2026-03-04.json
|           |-- 2026-03-05.json
|           |-- 2026-03-06.json
|           |-- 2026-03-07.json
|           |-- 2026-03-08.json
|           |-- 2026-03-09.json
|           |-- 2026-03-10.json
|           |-- 2026-03-11.json
|           |-- 2026-03-12.json
|           |-- 2026-03-13.json
|           |-- 2026-03-14.json
|           |-- 2026-03-15.json
|           |-- 2026-03-16.json
|           |-- 2026-03-17.json
|           |-- 2026-03-20.json
|           |-- 2026-03-21.json
|           |-- 2026-03-23.json
|           |-- 2026-03-24.json
|           |-- 2026-03-26.json
|           |-- 2026-03-27.json
|           |-- 2026-03-28.json
|           |-- 2026-04-12.json
|           |-- 2026-04-13.json
|           |-- 2026-04-14.json
|           |-- 2026-04-18.json
|           `-- 2026-04-19.json
|-- normalized/
|   `-- sources/
|       |-- 019c687b-3d0d-71c0-8929-9128cbf24060/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9ca4-ac1c-76e2-b883-017d68d982a1/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9cff-0337-77e0-9ba6-a4f6dc75a92e/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d00-0d81-7b52-a1a9-84f7d4b05066/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d4c-657e-7d71-a062-4d77a75d3786/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d53-7494-7e83-8519-25d541393ee6/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d54-1089-7ad2-9f90-57be7710dcad/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d57-92b6-7382-a637-8c4251b63817/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d57-dec5-7f12-9b7a-20330759fbfd/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d58-ef98-7c71-b725-1f9074946181/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d5a-2434-77d2-b985-9f8045648610/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d5b-128f-7240-9aee-54b8ea2f59d7/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d5b-6fcd-7483-b5c6-2255c43b916d/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d5b-b1a6-7fc1-a6c4-c7c8abe77031/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d5b-e6cd-7db0-8980-b08248a4ba09/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d5c-55a5-7841-ab96-65ee521280b5/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d5d-6ca1-7763-9121-0be51be71a7b/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d5d-dc33-7ef2-b7cf-2e97f6231167/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d5e-15f7-7483-a5de-bac1f5d3e835/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d5e-3ea5-7503-a2c9-74d8f75a220b/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d5f-becf-7d83-9fb9-caa573e948b0/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d60-390c-7251-8e71-54bb184c5607/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d60-9b0d-71b0-be73-efa8033c9940/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d6a-1df2-7290-9e8a-1e3b28e2feb9/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d6b-6077-7c33-bb98-d1504ca0d6d4/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d6f-34ed-7dc1-a7cc-4209d931f215/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d7a-12c2-7fd1-8b96-7605c72fbbb9/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d81-8487-73e3-9a63-1fa7d23f7bad/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9d82-290f-7241-8d9e-f59b9f5e258b/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9f43-3a51-7052-ad49-94d4475d953a/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9f43-944f-7403-a8a0-8484dd96dfab/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9f44-cac1-7b13-9ce0-dfc4492316ba/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9f48-e770-78f0-b223-9600b20b6303/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9f49-ff0a-7e11-a8a3-c2bfe616580b/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9f4b-8acd-70d1-bd77-e2356d46b6f2/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9f56-e5d9-7d91-906a-cf263f2a4c84/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019c9f58-333b-7c52-a26d-bdc0709234c5/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca18a-3473-7743-a7c0-50d4922dea5d/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca2f8-b377-7703-acfb-1825c4c2f8b0/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca30c-78c3-7191-8deb-e42ed4b348ab/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca310-20e8-76f0-95aa-e213d3cb77cb/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca311-ed33-74d2-8f97-58ee853a1b59/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca320-9699-77b3-a669-546e27eb724e/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca5ea-9c32-7090-8985-3411f371f917/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca5f3-bf03-7fe0-9d95-760e31374dd0/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca5f9-374c-7d20-b8ad-9c8290adcde3/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca609-b3bb-73f3-aec5-c64a38059274/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca60d-f3c6-7f13-a9fc-bf9314e79b01/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca611-9dc1-7e00-9adb-b470f228ed85/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca617-1b99-7df1-ae0b-3a643924e117/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca617-3330-7b42-840a-81859188334e/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca61e-6ec1-7c91-aa53-1c61330da985/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca61e-8ac1-7503-a0f3-a553d43375fc/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca61e-a9a0-7a81-8663-461ed161f842/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca69a-b325-7540-84eb-61c29f4c1f7c/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca6fa-7ec5-7f71-ab37-96eb69672b2c/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca6fe-4e31-7b23-8705-b0e23f293d62/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca705-c215-7221-8e6a-d28b922add82/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca718-449c-73b1-b935-872a2422adf2/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca71b-c355-7731-9c8e-ff9f39e97ba3/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019ca78b-4fe3-73a3-9e4d-e077c637de74/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019caa7e-937d-7e72-95e8-631ca4b769b4/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019caaa7-2fe4-7a72-9693-6b998656746e/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cab13-b21e-76f3-9029-bcd0333cd3eb/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cab4e-ab00-7e31-b50f-faff8205252f/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019caca3-cd0b-73b0-99f0-1ef6221f7cae/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019caf95-fa0a-7900-9097-6dbda1513ef0/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019caf9f-c9e4-7d33-9635-28feaa5b3b4a/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cb0ef-a044-7090-9627-7f2d616c46f2/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cb0f9-2d39-7850-a9e1-11263a5a8783/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cb0fd-2d7f-7f81-9d7e-088d64565547/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cb0fd-cf4c-7520-baf2-de448646fff2/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cb0fe-5561-75f0-803f-0525f796830d/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cb0fe-a160-7362-85e0-720ad035cf30/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cb0ff-85d9-7cf1-8054-6fd4770fe9f2/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cb100-5540-7371-8eb5-a89bab51137b/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cb106-799e-7151-bf0b-76cd90d07e55/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cb148-7e62-79a3-af96-9f74a1edaa78/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cb162-d216-7f63-9eb0-f7c9cd446990/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cb166-459d-7a01-a948-70994c21d327/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cba69-7058-72e0-805d-180f5372e2bd/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       |-- 019cbacf-74e5-7411-a1ab-6595d49c26a2/
|       |   |-- events.jsonl
|       |   |-- session.json
|       |   `-- stats.json
|       `-- 019d837d-d249-71c3-9637-b8d6992ce805/
|           |-- events.jsonl
|           |-- session.json
|           `-- stats.json
|-- schema/
|   `-- normalization_catalog.json
|-- scripts/
|   `-- install-windows-task.ps1
|-- segmented/
|   `-- sources/
|       |-- 019c687b-3d0d-71c0-8929-9128cbf24060/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9ca4-ac1c-76e2-b883-017d68d982a1/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9cff-0337-77e0-9ba6-a4f6dc75a92e/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d00-0d81-7b52-a1a9-84f7d4b05066/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d4c-657e-7d71-a062-4d77a75d3786/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d53-7494-7e83-8519-25d541393ee6/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d54-1089-7ad2-9f90-57be7710dcad/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d57-92b6-7382-a637-8c4251b63817/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d57-dec5-7f12-9b7a-20330759fbfd/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d58-ef98-7c71-b725-1f9074946181/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d5a-2434-77d2-b985-9f8045648610/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d5b-128f-7240-9aee-54b8ea2f59d7/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d5b-6fcd-7483-b5c6-2255c43b916d/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d5b-b1a6-7fc1-a6c4-c7c8abe77031/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d5b-e6cd-7db0-8980-b08248a4ba09/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d5c-55a5-7841-ab96-65ee521280b5/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d5d-6ca1-7763-9121-0be51be71a7b/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d5d-dc33-7ef2-b7cf-2e97f6231167/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d5e-15f7-7483-a5de-bac1f5d3e835/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d5e-3ea5-7503-a2c9-74d8f75a220b/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d5f-becf-7d83-9fb9-caa573e948b0/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d60-390c-7251-8e71-54bb184c5607/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d60-9b0d-71b0-be73-efa8033c9940/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d6a-1df2-7290-9e8a-1e3b28e2feb9/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d6b-6077-7c33-bb98-d1504ca0d6d4/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d6f-34ed-7dc1-a7cc-4209d931f215/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d7a-12c2-7fd1-8b96-7605c72fbbb9/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d81-8487-73e3-9a63-1fa7d23f7bad/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9d82-290f-7241-8d9e-f59b9f5e258b/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9f43-3a51-7052-ad49-94d4475d953a/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9f43-944f-7403-a8a0-8484dd96dfab/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9f44-cac1-7b13-9ce0-dfc4492316ba/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9f48-e770-78f0-b223-9600b20b6303/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9f49-ff0a-7e11-a8a3-c2bfe616580b/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9f4b-8acd-70d1-bd77-e2356d46b6f2/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9f56-e5d9-7d91-906a-cf263f2a4c84/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019c9f58-333b-7c52-a26d-bdc0709234c5/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca18a-3473-7743-a7c0-50d4922dea5d/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca2f8-b377-7703-acfb-1825c4c2f8b0/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca30c-78c3-7191-8deb-e42ed4b348ab/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca310-20e8-76f0-95aa-e213d3cb77cb/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca311-ed33-74d2-8f97-58ee853a1b59/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca320-9699-77b3-a669-546e27eb724e/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca5ea-9c32-7090-8985-3411f371f917/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca5f3-bf03-7fe0-9d95-760e31374dd0/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca5f9-374c-7d20-b8ad-9c8290adcde3/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca609-b3bb-73f3-aec5-c64a38059274/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca60d-f3c6-7f13-a9fc-bf9314e79b01/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca611-9dc1-7e00-9adb-b470f228ed85/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca617-1b99-7df1-ae0b-3a643924e117/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca617-3330-7b42-840a-81859188334e/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca61e-6ec1-7c91-aa53-1c61330da985/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca61e-8ac1-7503-a0f3-a553d43375fc/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca61e-a9a0-7a81-8663-461ed161f842/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca69a-b325-7540-84eb-61c29f4c1f7c/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca6a9-a7bc-7253-a18a-d77cd4a65aa5/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca6fa-7ec5-7f71-ab37-96eb69672b2c/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca6fe-4e31-7b23-8705-b0e23f293d62/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca705-c215-7221-8e6a-d28b922add82/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca718-449c-73b1-b935-872a2422adf2/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca71b-c355-7731-9c8e-ff9f39e97ba3/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019ca78b-4fe3-73a3-9e4d-e077c637de74/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019caa7e-937d-7e72-95e8-631ca4b769b4/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019caaa7-2fe4-7a72-9693-6b998656746e/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019caaf1-3a40-7082-ac18-8fe3f3eb0dd0/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cab13-b21e-76f3-9029-bcd0333cd3eb/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cab4e-ab00-7e31-b50f-faff8205252f/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019caca3-cd0b-73b0-99f0-1ef6221f7cae/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019caf95-fa0a-7900-9097-6dbda1513ef0/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019caf9f-c9e4-7d33-9635-28feaa5b3b4a/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cb0ef-a044-7090-9627-7f2d616c46f2/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cb0f9-2d39-7850-a9e1-11263a5a8783/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cb0fd-2d7f-7f81-9d7e-088d64565547/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cb0fd-cf4c-7520-baf2-de448646fff2/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cb0fe-5561-75f0-803f-0525f796830d/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cb0fe-a160-7362-85e0-720ad035cf30/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cb0ff-85d9-7cf1-8054-6fd4770fe9f2/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cb100-5540-7371-8eb5-a89bab51137b/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cb106-799e-7151-bf0b-76cd90d07e55/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cb148-7e62-79a3-af96-9f74a1edaa78/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cb162-d216-7f63-9eb0-f7c9cd446990/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cb166-459d-7a01-a948-70994c21d327/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cba69-7058-72e0-805d-180f5372e2bd/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       |-- 019cbacf-74e5-7411-a1ab-6595d49c26a2/
|       |   |-- segments.jsonl
|       |   |-- session_flow.json
|       |   `-- stats.json
|       `-- 019d837d-d249-71c3-9637-b8d6992ce805/
|           |-- segments.jsonl
|           |-- session_flow.json
|           `-- stats.json
|-- state/
|   |-- agent_bootstrap_runs.jsonl
|   |-- agent_bootstrap_state.json
|   |-- audit_runs.jsonl
|   |-- audit_state.json
|   |-- bootstrap_runs.jsonl
|   |-- bootstrap_state.json
|   |-- classification_runs.jsonl
|   |-- classification_state.json
|   |-- discovery_runs.jsonl
|   |-- extraction_runs.jsonl
|   |-- extraction_state.json
|   |-- full_load_runs.jsonl
|   |-- full_load_state.json
|   |-- ingest_runs.jsonl
|   |-- ingest_state.json
|   |-- memory_lint_runs.jsonl
|   |-- memory_lint_state.json
|   |-- memory_refresh_runs.jsonl
|   |-- memory_refresh_state.json
|   |-- memory_review_decisions.json
|   |-- memory_review_runs.jsonl
|   |-- memory_runs.jsonl
|   |-- memory_state.json
|   |-- memory_v2_runs.jsonl
|   |-- normalization_runs.jsonl
|   |-- normalization_state.json
|   |-- project_routing_runs.jsonl
|   |-- project_routing_state.json
|   |-- segmentation_runs.jsonl
|   |-- segmentation_state.json
|   |-- source_registry.json
|   |-- wiki_runs.jsonl
|   `-- wiki_state.json
|-- tests/
|   |-- fixtures/
|   |   `-- live_corpus_manifest.json
|   |-- test_agent_bootstrap.py
|   |-- test_audit.py
|   |-- test_bootstrap.py
|   |-- test_classification.py
|   |-- test_discovery.py
|   |-- test_extraction.py
|   |-- test_full_load.py
|   |-- test_ingest.py
|   |-- test_live_corpus.py
|   |-- test_memory_generation.py
|   |-- test_memory_lint.py
|   |-- test_memory_refresh.py
|   |-- test_memory_review.py
|   |-- test_memory_v2.py
|   |-- test_normalization.py
|   |-- test_onboarding.py
|   |-- test_product_config.py
|   |-- test_raw_event_resolver.py
|   |-- test_refresh.py
|   |-- test_segmentation.py
|   `-- test_wiki.py
|-- wikimemory/
|   |-- __init__.py
|   |-- __main__.py
|   |-- adapters.py
|   |-- agent_bootstrap.py
|   |-- audit.py
|   |-- bootstrap.py
|   |-- classification.py
|   |-- cli.py
|   |-- discovery.py
|   |-- env_loader.py
|   |-- extraction.py
|   |-- full_load.py
|   |-- ingest.py
|   |-- memory_extraction.py
|   |-- memory_generation.py
|   |-- memory_lint.py
|   |-- memory_model.py
|   |-- memory_refresh.py
|   |-- memory_review.py
|   |-- memory_v2.py
|   |-- normalization.py
|   |-- onboarding.py
|   |-- product_config.py
|   |-- project_routing.py
|   |-- raw_event_resolver.py
|   |-- refresh.py
|   |-- segmentation.py
|   `-- wiki.py
|-- AGENTS.md
|-- pyproject.toml
`-- README.md
```

## KEY CONSTRAINTS

_No selected items from this evidence._

## OPEN PROBLEMS

_No selected items from this evidence._

## BACKLOG

1. Add/maintain explicit notification and audit surfacing for previously unseen but valid outer event types or payload subtypes so schema drift drives parser upgrades without failing normalization.
2. Improve project association/routing so evidence maps to correct project slugs instead of generic buckets and avoids cross-project leakage.
3. Improve recent-memory quality with decay/windowing/active-context selection and stronger filtering of low-signal scaffold replies.
4. Move memory thresholds/heuristics (stale windows, caps, rule patterns, trivial-message filters) from code into configurable policy.
5. Add bootstrap renderers beyond Codex (e.g., Claude and generic targets).
6. Integrate scheduler/cadence support for the memory-refresh path.

## RELATED

- [[projects/wikimemory/recent|Wikimemory Recent]]
- [[projects/wikimemory/rules|Wikimemory Rules]]
- [[global/user-rules|Global User Rules]]
