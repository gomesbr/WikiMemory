# Example Source Log

This folder contains one real input session log copied from the external Codex corpus as a representative source-data example.

File:

- `source-logs/representative-session.jsonl`

Why this sample was chosen:

- it is small enough to keep in the repo comfortably
- it includes the `session_meta` opening record
- it includes normal user and assistant message flow
- it includes reasoning records
- it includes `function_call` and `function_call_output` events
- it includes policy-blocked tool outputs as well as successful tool outputs
- it shows the actual top-level JSONL event structure that WikiMemory ingests

What GPT should learn from it:

- each line is one JSON object
- the outer record has fields like `timestamp`, `type`, and `payload`
- `type` changes across session lifecycle records such as `session_meta`, `response_item`, `event_msg`, and `turn_context`
- the semantic detail usually lives inside `payload`
- `payload.type` is important and can represent messages, reasoning, tool calls, tool outputs, token counts, task state changes, and more
- a single session log mixes system/developer/user context, tool activity, reasoning summaries, commentary updates, and final answers

This is only an example input file, not a complete corpus sample. It is meant to help another model understand the raw source format and event variety without needing access to the full external session store.
