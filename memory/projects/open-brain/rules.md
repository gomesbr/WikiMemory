---
type: project-rules
project: open-brain
updated: 2026-04-20T01:19:51.513054Z
tags: [project/open-brain, rules]
---

# Open Brain - Project Rules

## ALWAYS DO

- Production-quality data must use real OpenAI embeddings with no mock fallback; if provider quota/credit blocks runs, stop and report rather than silently degrading.
- Quality-first policy: do not trade extraction/reasoning quality for speed; apply universal quality gating so low-confidence artifacts are not promoted to trusted/published outputs.
- Inter-agent communication must be JSON-only with structured contracts.

## NEVER DO

- Avoid case-specific or domain-hardcoded prompt hacks; use generic capability-first retrieval/reasoning strategies and natural relative-time phrasing unless fixed dates are explicitly needed.

## CONDITIONAL RULES

- Benchmark/test cases and scoring must be grounded in real DB evidence with provenance (no synthetic expected answers), and stale cases should be regenerated when source evidence changes.
- Evaluation governance remains strict: certification/critical quality targets are ~99% class, with early-stop logic when 99% is no longer achievable; ambiguity debt is treated as a hard winner-governance risk.
- Respect scope/approval boundaries: do analysis-only when requested, avoid off-scope changes, confirm target screen/area after scope confusion, and during live review sessions avoid extra code changes unless asked.
- For approved bottleneck-fixing phases, run autonomous iterative loops (identify bottleneck → implement narrow fix → validate → repeat) without pausing at checkpoints.

## SCOPE NOTES

- Applies only to `open-brain` unless a rule explicitly says otherwise.
