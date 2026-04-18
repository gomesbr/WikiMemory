---
title: "Open Brain - Workflow Rules"
page_id: "projects/open-brain/workflow-rules"
domain: "open-brain"
bucket: "workflow-rules"
page_type: "bucket_page"
renderer: "obsidian_markdown"
generated_at: 2026-04-13T19:33:05.505557Z
source_count: 1
claim_count: 9
tags:
  - wikimemory
  - project
  - open-brain
  - bucket
  - workflow-rules
---
# Open Brain - Workflow Rules

Navigation: [[projects/open-brain/index|Open Brain]] | [[projects/open-brain/communication-preferences|Open Brain - Communication Preferences]] | [[projects/open-brain/architecture|Open Brain - Architecture]] | [[projects/open-brain/code-map|Open Brain - Code Map]] | [[projects/open-brain/current-state|Open Brain - Current State]] | [[projects/open-brain/tasks|Open Brain - Tasks]] | [[projects/open-brain/outcomes|Open Brain - Outcomes]] | [[projects/open-brain/failures|Open Brain - Failures]] | [[projects/open-brain/decisions|Open Brain - Decisions]] | [[projects/open-brain/next-steps|Open Brain - Next Steps]] | [[projects/open-brain/open-questions|Open Brain - Open Questions]]

## Summary
- The workflow rules for the Open Brain project include specific do's and don'ts to ensure data quality and project efficiency. [latent: workflow_norms] [confidence: strong][^claim-1]
- Key do's include ensuring visibility of labels and checking for duplicates in data. [latent: workflow_norms] [confidence: strong][^claim-2]
- The rules are designed to maintain the integrity of the data and streamline the workflow process. [latent: workflow_norms] [confidence: strong][^claim-3]

## Do Rule
- Take your time, think step by step, make sure no more data quality gaps exist in any table. [latent: workflow_norms] [confidence: strong][^claim-4]
- Labels should always be visible to ensure clarity in data representation. [latent: workflow_norms] [confidence: strong][^claim-5]
- Make sure there are no duplicates in the data to maintain its integrity. [latent: workflow_norms] [confidence: strong][^claim-6]

### Canonical Items
- Take your time, think step by step, make sure no more data quality gaps exists in any table. [confidence: strong] [recurrence: 1][^item-do_rule-1]
- labels always visible [confidence: strong] [recurrence: 1][^item-do_rule-2]
- root and category labels always visible [confidence: strong] [recurrence: 1][^item-do_rule-3]
- Another consideration, underlying data might change after graph is saved, so we either save graph as historical so graph will always look the same independent of data changes, or we show the graph with current data. [confidence: strong] [recurrence: 1][^item-do_rule-4]
- Next I’m checking the runner and why progress is sparse to make sure we’re actually favoring the phase gates you listed. [confidence: strong] [recurrence: 1][^item-do_rule-5]
- Make sure there are no duplicates. [confidence: strong] [recurrence: 1][^item-do_rule-6]
- The temporal split exposed a real bug: some new temporal subfamilies were ending up with `0` viable anchor rows after anchor scoring, and the scheduler assumed `anchorRows[0]` always exists. [confidence: strong] [recurrence: 1][^item-do_rule-7]
- By the way, if those 2 names are different actors, they are both me, so make sure to merge them. [confidence: strong] [recurrence: 1][^item-do_rule-8]
- Make sure cases are being diverse and are being picked up from all types of sources and conversations. [confidence: strong] [recurrence: 1][^item-do_rule-9]
- Check the quality of the new samples from time to time to make sure garbage is not being inserted. [confidence: strong] [recurrence: 1][^item-do_rule-10]
- That is the second time that this happens, always when context window compaction is happening [confidence: strong] [recurrence: 1][^item-do_rule-11]
- Also make sure the deduped actors (many into 1 id) don't lose reference to their messages (aka any other table where the merged id is now referring to the new id) [confidence: strong] [recurrence: 1][^item-do_rule-12]
- Make sure that this is what is happening. [confidence: strong] [recurrence: 1][^item-do_rule-13]
- Lets say you think we need 80% or YES, so make sure the final count (reviewed + new) meet that percentage. [confidence: strong] [recurrence: 1][^item-do_rule-14]
- The questions ALWAYS need to come from MY point of view OR the AGENTS point of view [confidence: strong] [recurrence: 1][^item-do_rule-15]
- always build a semantic frame first [confidence: strong] [recurrence: 1][^item-do_rule-16]
- make sure the question can actually recover the evidence [confidence: strong] [recurrence: 1][^item-do_rule-17]
- make sure 'all systems' are health and runnig [confidence: strong] [recurrence: 1][^item-do_rule-18]
- make sure these models behave in aligned ways. [confidence: strong] [recurrence: 1][^item-do_rule-19]
- generated strategies always contain 5 valid components. [confidence: strong] [recurrence: 1][^item-do_rule-20]
- Make sure only one session is running. [confidence: strong] [recurrence: 1][^item-do_rule-21]
- Also, you should be the orchestator and monitor here, so make sure the loop is heathy and running and try to act proactively on any improvement and/or system failure. [confidence: strong] [recurrence: 1][^item-do_rule-22]
- If you want, I can also add a `stop_reason` field persisted into DB each time the loop exits, so this is always auditable. [confidence: strong] [recurrence: 1][^item-do_rule-23]
- When compacting context data from this window, always bring the full plan (we are about to create that in a sec). [confidence: strong] [recurrence: 1][^item-do_rule-24]
- Always consider initial questions will have more details. [confidence: strong] [recurrence: 1][^item-do_rule-25]

## Dont Rule
- Do not add a new UI module in this phase to avoid complications. [latent: workflow_norms] [confidence: strong][^claim-7]
- Never keep a weak higher-order case just to preserve counts, as it can lead to data quality issues. [latent: workflow_norms] [confidence: strong][^claim-8]
- The system should reject summaries that do not materially cover the substantive evidence to ensure relevance. [latent: workflow_norms] [confidence: strong][^claim-9]

### Canonical Items
- If we don’t fix that root filter, we’ll keep cleaning good junk out and then failing to bring back the right kinds of cases. [confidence: strong] [recurrence: 1][^item-dont_rule-1]
- The remaining gap is coming from supply shape, not cleanup correctness: we don’t have enough good human cases in stale inventory, so cleanup is depending on whole-corpus human generation and that path is still rejecting too much. [confidence: strong] [recurrence: 1][^item-dont_rule-2]
- That gives us the retroactive “don’t make me review this junk again” behavior without turning cleanup into a giant new subsystem. [confidence: strong] [recurrence: 1][^item-dont_rule-3]
- Do not add a new UI module in this phase. [confidence: strong] [recurrence: 1][^item-dont_rule-4]
- Keep cheaper deterministic screening for obvious rejects and anchor sufficiency, but do not let deterministic paraphrase logic remain the final answer-construction layer. [confidence: strong] [recurrence: 1][^item-dont_rule-5]
- Never keep a weak higher-order case just to preserve counts. [confidence: strong] [recurrence: 1][^item-dont_rule-6]
- Do not only fix future cases. [confidence: strong] [recurrence: 1][^item-dont_rule-7]
- Do not introduce a separate experiment-loop API family [confidence: strong] [recurrence: 1][^item-dont_rule-8]
- `Do not copy Anthropic’s context-reset-heavy 4.5 harness` [confidence: strong] [recurrence: 1][^item-dont_rule-9]
- `Do not make everything multi-agent` [confidence: strong] [recurrence: 1][^item-dont_rule-10]
- don’t rely on self-evaluation alone [confidence: strong] [recurrence: 1][^item-dont_rule-11]
- The system should reject summaries that do not materially cover the substantive evidence. [confidence: strong] [recurrence: 1][^item-dont_rule-12]
- another issue, response reference evidence but I don't see evidence in the evidence section. [confidence: strong] [recurrence: 1][^item-dont_rule-13]
- do not hardcode phone numbers or tokens [confidence: strong] [recurrence: 1][^item-dont_rule-14]
- repeated audit rows are now prevented by indexes, so the same tables do not rot again on reruns [confidence: strong] [recurrence: 1][^item-dont_rule-15]
- That meant the login handler never attached, so the form behaved like a plain submit and left you on the login page after password entry. [confidence: strong] [recurrence: 1][^item-dont_rule-16]
- The page script has a browser-side syntax error again, which means the login handler never fully boots and the form falls back to a plain submit. [confidence: strong] [recurrence: 1][^item-dont_rule-17]
- Do not add photo handling in v1. [confidence: strong] [recurrence: 1][^item-dont_rule-18]
- Do not change the fundamental saved-view / snapshot behavior in this pass. [confidence: strong] [recurrence: 1][^item-dont_rule-19]
- Do not redesign saved-view/snapshot APIs in this pass. [confidence: strong] [recurrence: 1][^item-dont_rule-20]
- Existing published relationship data should be reused where valid, but person nodes must resolve to canonical actor ids whenever possible. [confidence: strong] [recurrence: 1][^item-dont_rule-21]
- Then relationship/fact rows should point into canonical actor ids whenever possible. [confidence: strong] [recurrence: 1][^item-dont_rule-22]
- You asked for the workspace instructions in the root `AGENTS.md` to govern responses, and they override the behavior you don’t want. [confidence: strong] [recurrence: 1][^item-dont_rule-23]
- Don't need short updates either. [confidence: strong] [recurrence: 1][^item-dont_rule-24]
- Good catch: the running app is still serving the old login handler, so your browser never got the fix. [confidence: strong] [recurrence: 1][^item-dont_rule-25]

## Sources
[^claim-1]: items open-brain:do_rule:69a19cdb86283b51, open-brain:do_rule:59f5885236a507f3, open-brain:do_rule:a15785727dbe4069, open-brain:do_rule:11b33353a351a242; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 73732-73735; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72445-72448; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72451-72451; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72452-72453; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72445-72448; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72451-72451; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72452-72453; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71673-71674
[^claim-2]: items open-brain:do_rule:59f5885236a507f3, open-brain:do_rule:3047087da1a03326, open-brain:do_rule:01be76f65111dc85; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72445-72448; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72451-72451; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72452-72453; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 64789-64792; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 54471-54474
[^claim-3]: items open-brain:do_rule:69a19cdb86283b51, open-brain:dont_rule:b3c5b1269df003e2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 73732-73735; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86141-86152
[^claim-4]: items open-brain:do_rule:69a19cdb86283b51; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 73732-73735
[^claim-5]: items open-brain:do_rule:59f5885236a507f3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72445-72448; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72451-72451; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72452-72453
[^claim-6]: items open-brain:do_rule:3047087da1a03326; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 64789-64792
[^claim-7]: items open-brain:dont_rule:4e93ef3675605b2b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84001-84004; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84007-84007; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84008-84010
[^claim-8]: items open-brain:dont_rule:a33cea7cbb5a8965; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84001-84004; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84007-84007; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84008-84010
[^claim-9]: items open-brain:dont_rule:24a726992652ddfb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82667-82667; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82668-82673
[^item-do_rule-1]: items open-brain:do_rule:69a19cdb86283b51; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 73732-73735
[^item-do_rule-2]: items open-brain:do_rule:59f5885236a507f3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72445-72448; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72451-72451; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72452-72453
[^item-do_rule-3]: items open-brain:do_rule:a15785727dbe4069; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72445-72448; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72451-72451; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72452-72453
[^item-do_rule-4]: items open-brain:do_rule:11b33353a351a242; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71673-71674
[^item-do_rule-5]: items open-brain:do_rule:6cacdf8eb775d2e8; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 68260-68268
[^item-do_rule-6]: items open-brain:do_rule:3047087da1a03326; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 64789-64792
[^item-do_rule-7]: items open-brain:do_rule:4d25a9cbc8cd90e3; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 61932-61938
[^item-do_rule-8]: items open-brain:do_rule:be0fe03e58abde47; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 59491-59494
[^item-do_rule-9]: items open-brain:do_rule:01be76f65111dc85; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 54471-54474
[^item-do_rule-10]: items open-brain:do_rule:b8608af00666260f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 52959-52967
[^item-do_rule-11]: items open-brain:do_rule:08ab5854e1700a2b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 52106-52109
[^item-do_rule-12]: items open-brain:do_rule:139f06900cd69f4d; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 51408-51411
[^item-do_rule-13]: items open-brain:do_rule:0c1ce872c4726ab7; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 51408-51411
[^item-do_rule-14]: items open-brain:do_rule:604c6140371eece6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 44093-44096
[^item-do_rule-15]: items open-brain:do_rule:d4b272d7c6b830e7; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 38672-38673
[^item-do_rule-16]: items open-brain:do_rule:112a129865d78a5a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 37816-37817
[^item-do_rule-17]: items open-brain:do_rule:0670658434ba4b95; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 37601-37601; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 37602-37606
[^item-do_rule-18]: items open-brain:do_rule:00bb2c97fbe64e06; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 35762-35766
[^item-do_rule-19]: items open-brain:do_rule:05f1879e2f23d508; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 33107-33107; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 33108-33111
[^item-do_rule-20]: items open-brain:do_rule:3cf326c2c6d03b49; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 31363-31366
[^item-do_rule-21]: items open-brain:do_rule:d27720927b5baa7f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 30834-30838
[^item-do_rule-22]: items open-brain:do_rule:e0bdaed04ba17a00; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 28909-28913
[^item-do_rule-23]: items open-brain:do_rule:514ce5706a87ee71; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 28650-28656
[^item-do_rule-24]: items open-brain:do_rule:3a7b2572335ce863; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26606-26610
[^item-do_rule-25]: items open-brain:do_rule:83c09e43800c8730; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 26359-26363
[^item-dont_rule-1]: items open-brain:dont_rule:b3c5b1269df003e2; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 86141-86152
[^item-dont_rule-2]: items open-brain:dont_rule:84552e87048eb43f; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85820-85828
[^item-dont_rule-3]: items open-brain:dont_rule:29d7b2e0cd37f2da; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 85253-85264
[^item-dont_rule-4]: items open-brain:dont_rule:4e93ef3675605b2b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84001-84004; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84007-84007; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84008-84010
[^item-dont_rule-5]: items open-brain:dont_rule:ca7dd746d9ffa981; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84001-84004; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84007-84007; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84008-84010
[^item-dont_rule-6]: items open-brain:dont_rule:a33cea7cbb5a8965; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84001-84004; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84007-84007; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 84008-84010
[^item-dont_rule-7]: items open-brain:dont_rule:85241900171e02b6; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 83960-83960; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 83961-83964
[^item-dont_rule-8]: items open-brain:dont_rule:1138821b90167c54; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82837-82840; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82843-82843; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82844-82846
[^item-dont_rule-9]: items open-brain:dont_rule:0be362689bc5090c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82715-82715; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82716-82720
[^item-dont_rule-10]: items open-brain:dont_rule:53879e25ecc4d041; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82715-82715; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82716-82720
[^item-dont_rule-11]: items open-brain:dont_rule:66117a36e1851050; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82715-82715; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82716-82720
[^item-dont_rule-12]: items open-brain:dont_rule:24a726992652ddfb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82667-82667; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 82668-82673
[^item-dont_rule-13]: items open-brain:dont_rule:fe6aafd0ceb9b16a; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 79053-79056
[^item-dont_rule-14]: items open-brain:dont_rule:0c14d13136b21afb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 78650-78655
[^item-dont_rule-15]: items open-brain:dont_rule:9428492932dc90aa; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 75564-75564; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 75565-75568
[^item-dont_rule-16]: items open-brain:dont_rule:be50d7a54d74c97e; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72765-72770
[^item-dont_rule-17]: items open-brain:dont_rule:b3ee278cf3fb78ea; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72705-72711
[^item-dont_rule-18]: items open-brain:dont_rule:c4811e9673f6bb62; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72445-72448; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72451-72451; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72452-72453
[^item-dont_rule-19]: items open-brain:dont_rule:440b90989d8d6fbb; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72445-72448; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72451-72451; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72452-72453
[^item-dont_rule-20]: items open-brain:dont_rule:f4a8ef621e74d886; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72445-72448; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72451-72451; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 72452-72453
[^item-dont_rule-21]: items open-brain:dont_rule:929954e3ff4fb224; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71698-71701; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71704-71704; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71705-71706
[^item-dont_rule-22]: items open-brain:dont_rule:4c18872da6c72cbc; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71650-71650; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71651-71655
[^item-dont_rule-23]: items open-brain:dont_rule:492ff9b3c2abca3c; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71334-71339
[^item-dont_rule-24]: items open-brain:dont_rule:33dc05523d36848b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 71331-71332
[^item-dont_rule-25]: items open-brain:dont_rule:a9ab9690c524307b; 019cb0f9-2d39-7850-a9e1-11263a5a8783 lines 69153-69161
