---
type: project-memory
project: open-brain
updated: 2026-04-19T04:21:45.658216Z
tags: [project/open-brain, memory]
---

# 🧠 Open Brain - Project Memory

## PURPOSE

- Project context: OpenBrain is a local-first memory service built around Postgres with pgvector, a REST API, a remote MCP endpoint, and bulk import pipelines for multiple chat sources.
- Project context: WhatsApp history is a core data source because the user wants the system to support deep personal analysis and self-modeling.
- Design the system to handle future expansion into additional personal-data domains and analysis lenses.

## CORE COMPONENTS

- Project context: It correctly integrates grounded benchmarks, component recombination, and hypothesis-driven experimentation.
- Project context: The intended pipeline is: ingest raw files, normalize the data, embed the normalized content, then build aggregation tables from that normalized layer.
- Respect this constraint: the WhatsApp import pipeline should accept a zip containing per-chat zip files and continue processing that nested structure.
- Use this architecture context: benchmark authoring pipeline Implement...
- Use this architecture context: support cross-project access so agents from other projects can query OpenBrain as a shared intelligence service.
- Use this architecture context: the strategy decomposition should use five core components, but the design should remain extensible rather than fixed to exactly five.

## CURRENT ARCHITECTURE

- Use this architecture context: open Brain is intended to replace CodexClaw’s local memory reads and writes through a provider layer, with Postgres plus pgvector as the source of truth and both REST and MCP interfaces exposed.
- Use this architecture context: this is a **UI architecture + information design** upgrade, not a backend product-domain expansion.
- Use this architecture context: a formal hypothesis layer should be added to the loop because it strengthens both the system design and the paper narrative.
- Use this architecture context: actor-name cleanup should rely on the project's standard deduplication and normalization routines rather than raw actor lists.
- Use this architecture context: add an evaluation step after each strategy finishes to determine whether the failure was caused by infrastructure or by strategy logic.
- Use this architecture context: after that, I want you to check if the architecture we have today for OpenBrain would support your queries (derived from the user queries).

## DESIGN PRINCIPLES

- Prefer fixing authoring failures by falling back to deterministic draft generation instead of returning nothing.
- When generation fails, produce a deterministic draft instead of returning nothing; treat those drafts as synthetic placeholders, not real data.

## KEY CONSTRAINTS

- Respect this constraint: no_queued_strategies - This is a problem because during research between groups, no strategies will be running max_steps_reached - I have not requested any max steps, but if you need a number, add a number that can only be reached after a.
- Respect this constraint: only issue I found was ""c887b01d-501f-4ec5-94e7-3f7030c275a1","Ella's Besties"," is a whatsapp group name, so it has to be remove from actor list.
- Assume a single-user deployment and optimize the memory system for the owner and their coding agents.
- Respect this constraint: avoid duplicate cases in the generated set; duplicates were observed and should be filtered out before finalizing output.
- Respect this constraint: avoid exposing the working directory path or similar sensitive command output in the UI or logs when running shell commands.
- Respect this constraint: before making changes, resolve outstanding infrastructure and schema drift issues, and restart the interface only after the system is brought up to date.

## OPEN PROBLEMS

- Project context: Hahahaha, look at what you are doing: "role: "system", content: "You are AnswerSynthesisAgent for OpenBrain.
- Project context: The user wants a large-scale evaluation exercise: generate many plausible questions across the provided taxonomy and lenses, infer the answer style the user would prefer, and assess whether the current OpenBrain architecture can support each case.
- Project context: Yeah, but one clarification: every time i say restart open brain or clean up ans restart or somthing that has to do with kill all proccesses and restart open brain i mean this: openbrain as a whole is its all infra/scafolding, that accounts for all processes that need to be in place for the system to run properly, like cpu_guard and sms sent, etc.
- Use this architecture context: expose OpenBrain to external project agents through structured JSON interfaces rather than ad hoc text protocols.
- Use this architecture context: i ran this as a coverage exercise conceptually with your taxonomy+lenses as a grid: 36 taxonomy domains 10 analysis lenses 10 question variants per lens/domain Total hypothetical set: ~3,600 question scenarios Then I mapped each scenario to: required data artifacts, expected answer style (based on your “good answer” examples), current OpenBrain support level, architecture gaps.

## RELATED

- [[Open Brain Recent]]
- [[Open Brain Rules]]
- [[Global User Rules]]
