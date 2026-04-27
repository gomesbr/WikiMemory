from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AdapterDefinition:
    adapter_id: str
    adapter_kind: str
    description: str
    supports_incremental: bool
    config_keys: tuple[str, ...]


LOG_ADAPTERS = {
    "codex_jsonl": AdapterDefinition(
        adapter_id="codex_jsonl",
        adapter_kind="log_source",
        description="External Codex JSONL session logs with session_meta first-line identity.",
        supports_incremental=True,
        config_keys=("root_alias", "absolute_path", "include_glob"),
    ),
}


PROJECT_DELTA_ADAPTERS = {
    "git_worktree": AdapterDefinition(
        adapter_id="git_worktree",
        adapter_kind="project_delta_source",
        description="Git working tree plus commit/diff based project delta source.",
        supports_incremental=True,
        config_keys=("project_root", "include_untracked", "tracked_branches"),
    ),
}


MARKDOWN_RENDERERS = {
    "obsidian_markdown": AdapterDefinition(
        adapter_id="obsidian_markdown",
        adapter_kind="markdown_renderer",
        description="Markdown renderer with Obsidian wikilinks, frontmatter, and tags.",
        supports_incremental=True,
        config_keys=("frontmatter", "wikilinks", "tags", "callouts"),
    ),
    "plain_markdown": AdapterDefinition(
        adapter_id="plain_markdown",
        adapter_kind="markdown_renderer",
        description="Portable plain markdown renderer without Obsidian-specific syntax.",
        supports_incremental=True,
        config_keys=("frontmatter", "reference_links"),
    ),
}


BOOTSTRAP_RENDERERS = {
    "codex_agents_md": AdapterDefinition(
        adapter_id="codex_agents_md",
        adapter_kind="bootstrap_renderer",
        description="Generate a tiny AGENTS.md entry map for Codex workflows.",
        supports_incremental=True,
        config_keys=("target_path", "memory_links"),
    ),
    "claude_md": AdapterDefinition(
        adapter_id="claude_md",
        adapter_kind="bootstrap_renderer",
        description="Generate a tiny CLAUDE.md entry map for Claude workflows.",
        supports_incremental=True,
        config_keys=("target_path", "memory_links"),
    ),
    "generic_bootstrap_md": AdapterDefinition(
        adapter_id="generic_bootstrap_md",
        adapter_kind="bootstrap_renderer",
        description="Generate a neutral bootstrap markdown entry map.",
        supports_incremental=True,
        config_keys=("target_path", "memory_links"),
    ),
}
