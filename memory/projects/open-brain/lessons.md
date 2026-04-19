---
type: lessons
project: open-brain
updated: 2026-04-19T04:21:45.670806Z
tags: [project/open-brain, lessons]
---

# 🧠 Open Brain - Lessons Learned

## MEMORY DESIGN

- Carry forward this lesson: before abandoning a strategy, try additional in-strategy and between-strategy improvements that could convert a failure into a success.
- Carry forward this lesson: canonicalization is being discussed as a preprocessing step distinct from re-embedding; do not assume it means rebuilding embeddings from scratch.
- Carry forward this lesson: do not overfit to a single edge case by adding a large extraction subsystem; instead, identify the broader theme and solve at the row/entity linkage level.
- Carry forward this lesson: for yes/no evaluation, treat evidence-backed answers as correct even when they differ from the user's expected wording or preference.
- Carry forward this lesson: if a generated list is accidentally overwritten, restore the recovered files before continuing with pronoun updates.
- Carry forward this lesson: if no data is returned, agent needs to investigate root cause and fix it so strategy can run again until test cases can return responses..
- Carry forward this lesson: if the current strategy stops producing useful results, pause, inspect the discarded items for bottlenecks, and adjust the logic based on whether the rejections are valid.
- Carry forward this lesson: many entries in the candidate set are WhatsApp group names; prefixing them with a distinguishing marker was used to separate them from person names.
- Carry forward this lesson: one more think helpful to add to that answer is a quick feedback question like, "is that right?" so I could reply with yes (which can be kept as datapoint to enhance confidence for next time) or "no, I actually have X" (so datapoint can be added for next time as well).
- Carry forward this lesson: prefer Docker Compose service commands when restarting the local stack; the plain service name may not exist outside the compose context.
- Carry forward this lesson: that is how you should think next time.
- Carry forward this lesson: the answer flow should include a brief confirmation prompt so the user can validate or correct the inferred result, and that feedback should be retained for future confidence updates.
- Carry forward this lesson: the strategy metadata should not reuse the same next-step hypothesis for every run; each strategy should carry a distinct, evidence-based adjustment derived from what happened before it.
- Carry forward this lesson: the user believes short or noisy phrases and emoji-bearing messages can still be valid search targets if they carry conversational meaning.
- Carry forward this lesson: the user needed beginner-friendly help setting secrets for Open Brain, so future guidance should assume low setup familiarity and explain steps plainly.
- Carry forward this lesson: the user wants evidence of failed case creation before accepting any narrowing strategy, and prefers the system to explain the underlying intelligence rather than rely on user-provided examples alone.
- Carry forward this lesson: time you run a command, don't show app pwd in the screen.
- Carry forward this lesson: when a stability fix collapses multiple source values into one representative field, preserve the original source information if it carries analytical value.
- Carry forward this lesson: when generating responses, preserve the correct speaker attribution and avoid blending paraphrase with copied source wording in a way that sounds unnatural.
- Carry forward this lesson: when ingestion fails on malformed records, inspect the underlying record content to determine why parsing or formatting broke.
- Carry forward this lesson: when reviewing actor classifications, prioritize correcting ambiguous entries and known false positives such as duplicates or group names.
- Carry forward this lesson: when reviewing shared videos or screenshots, prioritize honest critique and call out anything that does not help the plan; do not default to agreement.
- Carry forward this lesson: when summarizing named people, preserve who said or did what and include concrete details from the evidence instead of generic paraphrases.
- Carry forward this lesson: when the model uses the wrong speaker perspective but the underlying answer is otherwise correct, the feedback should target the pronoun/persona issue rather than the factual content.

## SYSTEM DESIGN

- Carry forward this lesson: do not overfit to a single edge case by adding a large extraction subsystem; instead, identify the broader theme and solve at the row/entity linkage level.
- Carry forward this lesson: if no data is returned, agent needs to investigate root cause and fix it so strategy can run again until test cases can return responses..
- Carry forward this lesson: the user wants evidence of failed case creation before accepting any narrowing strategy, and prefers the system to explain the underlying intelligence rather than rely on user-provided examples alone.

ONLY INCLUDE HIGH-SIGNAL CONTENT
