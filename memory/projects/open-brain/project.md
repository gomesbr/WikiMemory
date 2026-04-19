---
type: project-memory
project: open-brain
updated: 2026-04-19T04:35:36.172824Z
tags: [project/open-brain, memory]
---

# 🧠 Open Brain - Project Memory

## PURPOSE

- OpenBrain is a local-first memory service built around Postgres with pgvector, a REST API, a remote MCP endpoint, and bulk import pipelines for multiple chat sources.
- WhatsApp history is a core data source because the user wants the system to support deep personal analysis and self-modeling.
- Design the system to handle future expansion into additional personal-data domains and analysis lenses.

## CORE COMPONENTS

- It correctly integrates grounded benchmarks, component recombination, and hypothesis-driven experimentation.
- The intended pipeline is: ingest raw files, normalize the data, embed the normalized content, then build aggregation tables from that normalized layer.
- the WhatsApp import pipeline should accept a zip containing per-chat zip files and continue processing that nested structure.
- support cross-project access so agents from other projects can query OpenBrain as a shared intelligence service.
- the strategy decomposition should use five core components, but the design should remain extensible rather than fixed to exactly five.
- **Intent-engineered Ask flow** (goal/constraints/escalation explicit in prompts and runtime decisions).

## CURRENT ARCHITECTURE

- this is a **UI architecture + information design** upgrade, not a backend product-domain expansion.
- a formal hypothesis layer should be added to the loop because it strengthens both the system design and the paper narrative.
- actor-name cleanup should rely on the project's standard deduplication and normalization routines rather than raw actor lists.
- add an evaluation step after each strategy finishes to determine whether the failure was caused by infrastructure or by strategy logic.
- after that, I want you to check if the architecture we have today for OpenBrain would support your queries (derived from the user queries).
- aggregation refresh may be runnable in parallel with embedding work if there is no dependency between the two stages.

## DESIGN PRINCIPLES

- Prefer fixing authoring failures by falling back to deterministic draft generation instead of returning nothing.
- When generation fails, produce a deterministic draft instead of returning nothing; treat those drafts as synthetic placeholders, not real data.

## KEY CONSTRAINTS

- no_queued_strategies - This is a problem because during research between groups, no strategies will be running max_steps_reached - I have not requested any max steps, but if you need a number, add a number that can only be reached after a.
- only issue I found was ""c887b01d-501f-4ec5-94e7-3f7030c275a1","Ella's Besties"," is a whatsapp group name, so it has to be remove from actor list.
- Assume a single-user deployment and optimize the memory system for the owner and their coding agents.
- avoid duplicate cases in the generated set; duplicates were observed and should be filtered out before finalizing output.
- avoid exposing the working directory path or similar sensitive command output in the UI or logs when running shell commands.
- before making changes, resolve outstanding infrastructure and schema drift issues, and restart the interface only after the system is brought up to date.

## OPEN PROBLEMS

- Hahahaha, look at what you are doing: "role: "system", content: "You are AnswerSynthesisAgent for OpenBrain.
- Prioritize a large-scale evaluation exercise: generate many plausible questions across the provided taxonomy and lenses, infer the answer style the user would prefer, and assess whether the current OpenBrain architecture can support each case.
- Yeah, but one clarification: every time i say restart open brain or clean up ans restart or somthing that has to do with kill all proccesses and restart open brain i mean this: openbrain as a whole is its all infra/scafolding, that accounts for all processes that need to be in place for the system to run properly, like cpu_guard and sms sent, etc.
- expose OpenBrain to external project agents through structured JSON interfaces rather than ad hoc text protocols.
- i ran this as a coverage exercise conceptually with your taxonomy+lenses as a grid: 36 taxonomy domains 10 analysis lenses 10 question variants per lens/domain Total hypothetical set: ~3,600 question scenarios Then I mapped each scenario to: required data artifacts, expected answer style (based on your “good answer” examples), current OpenBrain support level, architecture gaps.

## RELATED

- [[Open Brain Recent]]
- [[Open Brain Rules]]
- [[Global User Rules]]
