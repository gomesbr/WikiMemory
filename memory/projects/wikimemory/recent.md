---
type: recent-context
project: wikimemory
updated: 2026-04-20T01:19:51.521355Z
tags: [project/wikimemory, recent]
---

# Wikimemory - Recent Context - April 18 2026

## CURRENT FOCUS

- Current implementation includes memory-first generation/lint/refresh paths and compact bootstrap generation, with phased commands and state/audit artifacts active in the repository.

## ACTIVE DECISIONS

_No selected items from this evidence._

## IN PROGRESS

_No selected items from this evidence._

## FAILED / AVOID

- Actively growing logs can race during normalization/discovery; correctness should rely on on-handle observed bounds, skip unstable sources when needed, and preserve committed last-good state on anomalies.

## BACKLOG

- Improve project association/routing so evidence maps to correct project slugs instead of generic buckets and avoids cross-project leakage.
- Improve recent-memory quality with decay/windowing/active-context selection and stronger filtering of low-signal scaffold replies.
- Move memory thresholds/heuristics (stale windows, caps, rule patterns, trivial-message filters) from code into configurable policy.
- Add bootstrap renderers beyond Codex (e.g., Claude and generic targets).
- Integrate scheduler/cadence support for the memory-refresh path.

## OPEN QUESTIONS

_No selected items from this evidence._
