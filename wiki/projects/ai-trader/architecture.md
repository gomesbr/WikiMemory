---
title: "AI Trader - Architecture"
page_id: "projects/ai-trader/architecture"
domain: "ai-trader"
bucket: "architecture"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:07:05.212124Z
source_count: 60
claim_count: 6
tags:
  - wikimemory
  - project
  - ai-trader
  - bucket
  - architecture
---
# AI Trader - Architecture

Navigation: [[projects/ai-trader/index|AI Trader]] | [[projects/ai-trader/communication-preferences|AI Trader - Communication Preferences]] | [[projects/ai-trader/workflow-rules|AI Trader - Workflow Rules]] | [[projects/ai-trader/code-map|AI Trader - Code Map]] | [[projects/ai-trader/current-state|AI Trader - Current State]] | [[projects/ai-trader/tasks|AI Trader - Tasks]] | [[projects/ai-trader/outcomes|AI Trader - Outcomes]] | [[projects/ai-trader/failures|AI Trader - Failures]] | [[projects/ai-trader/decisions|AI Trader - Decisions]] | [[projects/ai-trader/next-steps|AI Trader - Next Steps]] | [[projects/ai-trader/open-questions|AI Trader - Open Questions]]
Related Domains: [[global/index|Global]]

## Summary
- The architecture of the AI Trader project is based on a multi-agent architecture. [latent: project_identity_and_scope] [confidence: strong][^claim-1]
- The runtime components are critical to the functionality of the AI Trader system. [latent: architecture_synthesis] [confidence: strong][^claim-2]
- Constraint architecture must include Must / Must Not / Prefer / Escalate guidelines. [latent: architecture_synthesis] [confidence: strong][^claim-3]

## Architecture Note
- The architecture note emphasizes the importance of a multi-agent architecture. [latent: project_identity_and_scope] [confidence: strong][^claim-4]
- Runtime components are a fundamental aspect of the architecture. [latent: architecture_synthesis] [confidence: strong][^claim-5]
- The architecture must adhere to specific constraints including Must / Must Not / Prefer / Escalate. [latent: architecture_synthesis] [confidence: strong][^claim-6]

### Canonical Items
- ## Multi-Agent Architecture [confidence: strong] [recurrence: 36][^item-architecture_note-1]
- ## Runtime Components [confidence: strong] [recurrence: 36][^item-architecture_note-2]
- - Constraint Architecture must include Must / Must Not / Prefer / Escalate. [confidence: strong] [recurrence: 17][^item-architecture_note-3]
- - For other repos/apps, mirror this same token set and component style (colors, grid backdrop, panel/chip styling, typography) so all apps keep one consistent look and feel. [confidence: strong] [recurrence: 17][^item-architecture_note-4]
- ## constraint-architecture (C:\Users\Fabio\Cursor AI projects\Projects\CodexClaw\skills\constraint-architecture\SKILL.md) [confidence: strong] [recurrence: 15][^item-architecture_note-5]
- - Build passes for touched components. [confidence: strong] [recurrence: 10][^item-architecture_note-6]
- architecture [confidence: strong] [recurrence: 2][^item-architecture_note-7]
- - Root cause: commands like “git …” and PowerShell pipelines (“… | Select-Object …”) are rejected before execution. [confidence: strong] [recurrence: 2][^item-architecture_note-8]
- I’m proceeding through the full deterministic pipeline first and will only stop if that or the disk cap actually blocks the run. [confidence: strong] [recurrence: 1][^item-architecture_note-9]
- I’m running the full local suite now to make sure the new full-load layer didn’t regress the existing pipeline. [confidence: strong] [recurrence: 1][^item-architecture_note-10]
- I’m doing one final full test sweep so the pointer-first migration is clean across the rest of the pipeline too. [confidence: strong] [recurrence: 1][^item-architecture_note-11]
- - Phases `1-9` built the product pipeline [confidence: strong] [recurrence: 1][^item-architecture_note-12]
- The stubborn part is now even narrower: five reasoning/search segments that the override resolver can classify in isolation but still aren’t being rewritten in the pipeline output, so I’m reproducing that exact function path against the real persisted list... [confidence: strong] [recurrence: 1][^item-architecture_note-13]
- - So the pipeline now survives real data better, but the next real capability gap is quality hardening for classification/extraction before trusting wiki output. [confidence: strong] [recurrence: 1][^item-architecture_note-14]
- The real-data run surfaced one concrete engineering issue worth fixing immediately: config JSON with a Windows BOM can break the pipeline even though the content is valid. [confidence: strong] [recurrence: 1][^item-architecture_note-15]
- I’m doing one last end-to-end check on the wiki command itself against that same real sample so we can separate “real-data pipeline works” from “live synthesis is blocked by environment.” [confidence: strong] [recurrence: 1][^item-architecture_note-16]
- The real pipeline is producing actual classified segments and extracted items now. [confidence: strong] [recurrence: 1][^item-architecture_note-17]
- The first run hiccup was just PowerShell syntax, not the pipeline itself. [confidence: strong] [recurrence: 1][^item-architecture_note-18]
- I’m running the real pipeline stages against that file now and then I’ll inspect the extracted outputs, not just whether the commands returned zero. [confidence: strong] [recurrence: 1][^item-architecture_note-19]
- I’m running the actual pipeline against your real Codex sessions on a small sample now, and I’ll report exactly what passed and where any real-data issue shows up. [confidence: strong] [recurrence: 1][^item-architecture_note-20]
- I’m still doing the important part right now: a real-data end-to-end smoke test through extraction on a copied sample of your actual session logs, so we validate the pipeline against real traces instead of fabricated inputs. [confidence: strong] [recurrence: 1][^item-architecture_note-21]
- - durable pages like `workflow-rules`, `communication-preferences`, `architecture`, `decisions` grouped by recurrence/support, not just recency [confidence: strong] [recurrence: 1][^item-architecture_note-22]
- `durable items` like preferences, rules, decisions, architecture notes [confidence: strong] [recurrence: 1][^item-architecture_note-23]
- Reason: true “complete/fully processed” belongs to downstream pipeline state, not discovery/indexing. [confidence: strong] [recurrence: 1][^item-architecture_note-24]
- Then I’ll turn that into a decision-complete refactor plan instead of a generic architecture essay. [confidence: strong] [recurrence: 1][^item-architecture_note-25]
- The new auto-review pipeline is live. [confidence: strong] [recurrence: 1][^item-architecture_note-26]
- - 20% component exploit/recombination runs [confidence: strong] [recurrence: 1][^item-architecture_note-27]
- - feed confirmed hypotheses into component recombination scoring [confidence: strong] [recurrence: 1][^item-architecture_note-28]
- component [confidence: strong] [recurrence: 1][^item-architecture_note-29]
- If you want, I’ll now publish the final consolidated plan with this hypothesis layer merged into the previous componentized plan as the official v1.3 blueprint. [confidence: strong] [recurrence: 1][^item-architecture_note-30]
- It complements component recombination directly, it does not compete with it. [confidence: strong] [recurrence: 1][^item-architecture_note-31]
- Next candidate generation using confirmed hypotheses + component performance [confidence: strong] [recurrence: 1][^item-architecture_note-32]
- I’ll add a concrete first-principles checklist (theme-first, class-of-problem, minimal architecture, no one-off complexity) to both `AGENTS.md` files you actively use: workspace root and `CodexClaw/AGENTS.md`. [confidence: strong] [recurrence: 1][^item-architecture_note-33]
- - keep `gpt-5.3-codex` for merges, architecture changes, and bugfixing across files. [confidence: strong] [recurrence: 1][^item-architecture_note-34]
- I’ll research concrete speed-up patterns from primary sources (OpenAI + pgvector/Postgres docs) and map them to your pipeline with a no-quality-loss design. [confidence: strong] [recurrence: 1][^item-architecture_note-35]
- I’m now pulling pgvector/Postgres best-practice sources so we can speed the full pipeline end-to-end, not just API calls. [confidence: strong] [recurrence: 1][^item-architecture_note-36]
- **Holistic Quality Architecture** [confidence: strong] [recurrence: 1][^item-architecture_note-37]
- Add agent-only promotion pipeline: [confidence: strong] [recurrence: 1][^item-architecture_note-38]
- - “Components detected: 401k, Roth, Robinhood [confidence: strong] [recurrence: 1][^item-architecture_note-39]
- - [architecture.md](/c:/Users/Fabio/Cursor AI projects/Projects/AITrader/docs/architecture.md) [confidence: strong] [recurrence: 1][^item-architecture_note-40]

## Sources
[^claim-1]: items ai-trader:architecture_note:e47dd819dd28e612; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-2]: items ai-trader:architecture_note:ee70e96a7701b57e; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-3]: items ai-trader:architecture_note:292489bfa18f9c2c; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^claim-4]: items ai-trader:architecture_note:e47dd819dd28e612; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-5]: items ai-trader:architecture_note:ee70e96a7701b57e; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^claim-6]: items ai-trader:architecture_note:292489bfa18f9c2c; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-architecture_note-1]: items ai-trader:architecture_note:e47dd819dd28e612; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-architecture_note-2]: items ai-trader:architecture_note:ee70e96a7701b57e; 019c9cff-0337-77e0-9ba6-a4f6dc75a92e lines 3-4; 019c9d00-0d81-7b52-a1a9-84f7d4b05066 lines 3-4; 019c9d4c-657e-7d71-a062-4d77a75d3786 lines 3-4
[^item-architecture_note-3]: items ai-trader:architecture_note:292489bfa18f9c2c; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-architecture_note-4]: items ai-trader:architecture_note:d0908719f9f4f947; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-architecture_note-5]: items ai-trader:architecture_note:4709e352d9a4e845; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca705-c215-7221-8e6a-d28b922add82 lines 54-54
[^item-architecture_note-6]: items ai-trader:architecture_note:8f9d0c4fdc82ae01; 019ca705-c215-7221-8e6a-d28b922add82 lines 5-5; 019ca705-c215-7221-8e6a-d28b922add82 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-architecture_note-7]: items ai-trader:architecture_note:d122884e061c87d0; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 5315-5322; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 10406-10407; 019c9ca4-ac1c-76e2-b883-017d68d982a1 lines 17238-17239
[^item-architecture_note-8]: items ai-trader:architecture_note:d9e0e9c48fc83773; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 5-5; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 6-9; 019ca766-5bc5-78d1-aa87-19b2cfd3b1a5 lines 19-19
[^item-architecture_note-9]: items ai-trader:architecture_note:5dbfe4e2ed284d1d; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4524-4540
[^item-architecture_note-10]: items ai-trader:architecture_note:b5946a5379e5bcf6; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4450-4460
[^item-architecture_note-11]: items ai-trader:architecture_note:b29cbfa9233f2632; 019d837d-d249-71c3-9637-b8d6992ce805 lines 4189-4201
[^item-architecture_note-12]: items ai-trader:architecture_note:f00ab7ab911ba168; 019d837d-d249-71c3-9637-b8d6992ce805 lines 3452-3457
[^item-architecture_note-13]: items ai-trader:architecture_note:334cff6921e1a748; 019d837d-d249-71c3-9637-b8d6992ce805 lines 2179-2187
[^item-architecture_note-14]: items ai-trader:architecture_note:2ab7354b7697d49a; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1824-1824; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1825-1828
[^item-architecture_note-15]: items ai-trader:architecture_note:ddf72dcd63f44097; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1777-1785
[^item-architecture_note-16]: items ai-trader:architecture_note:2aeaa6668f4bc2bf; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1729-1744
[^item-architecture_note-17]: items ai-trader:architecture_note:efc82a1773aafc4e; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1729-1744
[^item-architecture_note-18]: items ai-trader:architecture_note:e29c037dfc116b54; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1685-1696
[^item-architecture_note-19]: items ai-trader:architecture_note:9e9e88e45d3d9c6f; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1668-1678; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1679-1683
[^item-architecture_note-20]: items ai-trader:architecture_note:67208a3151d69cdd; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1610-1624
[^item-architecture_note-21]: items ai-trader:architecture_note:9e0991cf011c1930; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1610-1624
[^item-architecture_note-22]: items ai-trader:architecture_note:9774501cea6a0dea; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1290-1290; 019d837d-d249-71c3-9637-b8d6992ce805 lines 1291-1295
[^item-architecture_note-23]: items ai-trader:architecture_note:214da3feff2365c3; 019d837d-d249-71c3-9637-b8d6992ce805 lines 963-963; 019d837d-d249-71c3-9637-b8d6992ce805 lines 964-968
[^item-architecture_note-24]: items ai-trader:architecture_note:ce46b1066f057322; 019d837d-d249-71c3-9637-b8d6992ce805 lines 99-103
[^item-architecture_note-25]: items ai-trader:architecture_note:13a527d404be9db1; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 57229-57239
[^item-architecture_note-26]: items ai-trader:architecture_note:785a4adcd494fc66; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 43588-43595
[^item-architecture_note-27]: items ai-trader:architecture_note:d1d07ac1224c3616; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31394-31394
[^item-architecture_note-28]: items ai-trader:architecture_note:d3d8a3bf70f8c44e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31394-31394
[^item-architecture_note-29]: items ai-trader:architecture_note:00c6379ef16d53a0; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31394-31394
[^item-architecture_note-30]: items ai-trader:architecture_note:b48d9198b0b482d7; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31394-31394
[^item-architecture_note-31]: items ai-trader:architecture_note:9b4e3c6d9f849510; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31394-31394
[^item-architecture_note-32]: items ai-trader:architecture_note:53d1c52847a950d7; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31394-31394
[^item-architecture_note-33]: items ai-trader:architecture_note:f9012fbf11027b70; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 20613-20622
[^item-architecture_note-34]: items ai-trader:architecture_note:c77498365b0676c4; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 17273-17277
[^item-architecture_note-35]: items ai-trader:architecture_note:f0aaa872088f26f9; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 15967-16016
[^item-architecture_note-36]: items ai-trader:architecture_note:79b897643d427e69; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 15967-16016
[^item-architecture_note-37]: items ai-trader:architecture_note:c69bfb48495b2723; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13534-13540; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13541-13544
[^item-architecture_note-38]: items ai-trader:architecture_note:45dbeb8e41b8e1cc; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13534-13540; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13541-13544
[^item-architecture_note-39]: items ai-trader:architecture_note:f936b80aa46e7f18; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 13432-13438
[^item-architecture_note-40]: items ai-trader:architecture_note:cc35bf86ae2e0b81; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 3115-3115; 019cbacf-74e5-7411-a1ab-6595d49c26a2 lines 3116-3119
