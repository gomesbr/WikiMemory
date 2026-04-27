# Consumer Working Profile

SessionMemory can eventually maintain a `consumer working profile` to help future agent sessions collaborate better with the same person.

This is intentionally **not** a psychology profile, diagnosis, or intelligence score.

The goal is practical:

- reduce repeated friction
- match explanation depth
- match autonomy level
- remember recurring goals
- remember domain strengths
- remember tool and workflow preferences

## What The Profile Is For

The profile should answer:

- How should the agent communicate with this consumer?
- What level of initiative does the consumer usually want?
- Which technical domains does the consumer seem strong in?
- Which projects and goals are currently active?
- Which persistent constraints should the agent remember?

It should not try to answer:

- What kind of person is this in a psychological sense?
- How intelligent are they?
- What private or sensitive traits do they have?

## Allowed Inference Categories

These are the categories SessionMemory should allow:

- `communication_preferences`
- `workflow_preferences`
- `technical_strengths`
- `active_domains`
- `current_goals`
- `persistent_constraints`
- `collaboration_style`
- `decision_preferences`
- `tool_preferences`

Examples:

- prefers concise status updates
- wants direct implementation rather than long planning
- strong in backend debugging
- works frequently on trading systems and memory tooling
- currently focused on better agent onboarding
- prefers conservative changes over broad refactors
- likes the agent to infer defaults before asking questions

## Disallowed Inference Categories

These should stay out of scope:

- IQ or intelligence scoring
- psychological diagnosis
- personality typing as fact
- mental-health inference
- medical inference
- religion
- political beliefs
- sexual orientation
- protected-class inference
- manipulative targeting

Even if a model thinks it can guess these, SessionMemory should not store them.

## Quality Rules

Every profile fact should follow these rules:

1. It must improve future collaboration.
2. It must be grounded in observable behavior or repeated requests.
3. It should use soft wording:
   - "appears to prefer"
   - "has repeatedly asked for"
   - "usually wants"
4. One-off comments should not become stable profile facts unless later evidence repeats or confirms them.
5. Each fact should carry evidence references.
6. The consumer should be able to review, correct, or remove it.

## Suggested Schema

The schema lives in:

- `schema/consumer_working_profile.schema.json`

Recommended top-level sections:

- `communication_preferences`
- `workflow_preferences`
- `technical_strengths`
- `active_domains`
- `current_goals`
- `persistent_constraints`
- `collaboration_style`
- `decision_preferences`
- `tool_preferences`

## Recommended Product Framing

The profile should be presented as:

- a working profile
- a collaboration profile
- a memory aid for future agent sessions

Not as:

- a personality model
- a psychology profile
- an intelligence rating

## Implementation Guidance

When this becomes part of the extraction pipeline:

1. Keep profile extraction separate from rules/recent/project memory.
2. Require evidence-backed, structured items.
3. Bias toward under-collection.
4. Add review and correction paths before treating profile items as durable.
5. Prefer explicit consumer statements over inferred conclusions.
