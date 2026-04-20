---
type: project-rules
project: wikimemory
updated: 2026-04-20T01:19:51.524797Z
tags: [project/wikimemory, rules]
---

# Wikimemory - Project Rules

## ALWAYS DO

- Raw logs must remain external and immutable source-of-truth; processing must support incremental/streaming behavior for large append-only files and preserve non-chat event structures rather than flattening to simple prompt/response.
- Maintain Obsidian compatibility (wikilinks/frontmatter/stable pages) while keeping the internal page model tool-agnostic; Obsidian is a rendering target, not canonical storage format.
- Real-data validation is required alongside unit/mocked tests; use representative samples and env-gated live-corpus runs where needed.
- LLM synthesis is allowed only in bounded, evidence-backed form: deterministic structure remains primary, and synthesized claims must cite supporting extracted provenance without inventing facts.
- Generated wiki/memory outputs are deterministic rewrites; manual edits inside generated files are not preserved.

## NEVER DO

- Do not promote one-off instructions, progress/status chatter, or transient commands as durable rules; extraction and rendering must distinguish durable policy from session-local scaffolding.

## CONDITIONAL RULES

_No selected items from this evidence._

## SCOPE NOTES

- Applies only to `wikimemory` unless a rule explicitly says otherwise.
