# Start Here For Agent

If you are the consumer's code agent, start the WikiMemory configuration flow from this file.

WikiMemory is a memory solution for coding agents. Its goal is to turn prior session logs into compact agent-facing memory so new sessions can remember:

- user preferences
- consumer working style
- project rules
- recent work
- decisions
- open questions

## What To Do First

1. Read `README.md`.
2. Run:

```powershell
python -m wikimemory onboard --json
```

3. Review the generated:

- `config/product_config.json`
- `config/agent_onboarding_brief.generated.md`

4. Infer as much as you can from the local environment before asking the consumer questions.
5. Show the consumer the inferred options first.
6. Ask only the unresolved questions you cannot verify safely from the repo, filesystem, env vars, or existing bootstrap files.
7. After confirmation, update config and bootstrap files to match the consumer workflow.

## Configuration Principle

Prefer agent-driven setup:

- inspect local environment first
- detect likely OS, editor, bootstrap target, and log paths
- detect nearby participating repos when possible
- infer sensible defaults
- ask concise confirmation questions only where ambiguity remains

## Main Config Files

- `config/product_config.json`
- `config/source_roots.json`
- `config/consumer_profile_policy.json`
- bootstrap target like `AGENTS.md` or `CLAUDE.md`

## Consumer Working Profile

WikiMemory may later maintain a `consumer working profile` so future sessions can collaborate better with the same person.

Use it only for work-relevant collaboration traits, such as:

- communication preferences
- workflow preferences
- technical strengths
- active domains
- current goals

Do not treat it as a psychology or intelligence profile.

See:

- `docs/consumer-profile.md`
- `schema/consumer_working_profile.schema.json`

## Important Constraint

Do not treat WikiMemory as generic note generation. The real product goal is reliable memory bootstrap for future agent sessions, based on previous session conversation logs.
