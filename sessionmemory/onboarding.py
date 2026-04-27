from __future__ import annotations

import json
import os
from dataclasses import dataclass
from dataclasses import replace
from pathlib import Path

from .adapters import BOOTSTRAP_RENDERERS, LOG_ADAPTERS, MARKDOWN_RENDERERS
from .discovery import ensure_directory
from .product_config import ProductConfig, default_product_config, detect_operating_system


@dataclass(frozen=True)
class OnboardingOption:
    option_id: str
    label: str
    inferred_value: str | None
    confidence: str
    rationale: str
    configurable_in: str
    consumer_confirmation_needed: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "option_id": self.option_id,
            "label": self.label,
            "inferred_value": self.inferred_value,
            "confidence": self.confidence,
            "rationale": self.rationale,
            "configurable_in": self.configurable_in,
            "consumer_confirmation_needed": self.consumer_confirmation_needed,
        }


@dataclass(frozen=True)
class OnboardingQuestion:
    question_id: str
    prompt: str
    why_it_matters: str
    detected_value: str | None
    recommended_option: str
    options: tuple[dict[str, str], ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "question_id": self.question_id,
            "prompt": self.prompt,
            "why_it_matters": self.why_it_matters,
            "detected_value": self.detected_value,
            "recommended_option": self.recommended_option,
            "options": [dict(option) for option in self.options],
        }


@dataclass(frozen=True)
class OnboardingReport:
    project_root: str
    project_goal: str
    detected: dict[str, object]
    inferred_options: tuple[OnboardingOption, ...]
    recommended_product_config: dict[str, object]
    questions: tuple[OnboardingQuestion, ...]
    agent_entry_file: str
    generated_files: tuple[str, ...]
    next_steps: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "project_root": self.project_root,
            "project_goal": self.project_goal,
            "detected": self.detected,
            "inferred_options": [option.to_dict() for option in self.inferred_options],
            "recommended_product_config": self.recommended_product_config,
            "questions": [question.to_dict() for question in self.questions],
            "agent_entry_file": self.agent_entry_file,
            "generated_files": list(self.generated_files),
            "next_steps": list(self.next_steps),
        }


PROJECT_GOAL = (
    "SessionMemory is a memory layer for coding agents. It turns prior session logs into compact agent-facing "
    "memory so new sessions can remember user preferences, project rules, recent work, decisions, and open questions."
)


def run_onboarding(
    project_root: Path | str,
    config_path: Path | str | None = None,
    brief_path: Path | str | None = None,
) -> OnboardingReport:
    project_root = Path(project_root).resolve()
    detected = detect_environment(project_root)
    draft_config = default_product_config(project_root)
    draft_config = apply_detected_defaults(draft_config, detected)
    inferred_options = build_inferred_options(detected)
    questions = build_onboarding_questions(detected)

    generated_files: list[str] = []
    if config_path is not None:
        write_product_config(Path(config_path), draft_config)
        generated_files.append(str(Path(config_path)))
    if brief_path is not None:
        write_agent_onboarding_brief(Path(brief_path), project_root, detected, inferred_options, questions, draft_config)
        generated_files.append(str(Path(brief_path)))

    return OnboardingReport(
        project_root=str(project_root),
        project_goal=PROJECT_GOAL,
        detected=detected,
        inferred_options=inferred_options,
        recommended_product_config=draft_config.to_dict(),
        questions=questions,
        agent_entry_file="START_HERE_FOR_AGENT.md",
        generated_files=tuple(generated_files),
        next_steps=(
            "Read START_HERE_FOR_AGENT.md.",
            "Review the inferred options first and confirm the ones the environment strongly suggests.",
            "Ask the consumer only the unresolved questions that cannot be safely inferred.",
            "Then edit config/product_config.json, config/source_roots.json, and bootstrap targets to match the consumer workflow.",
        ),
    )


def detect_environment(project_root: Path) -> dict[str, object]:
    project_root = project_root.resolve()
    os_name = detect_operating_system()
    likely_markdown_mode = "obsidian_markdown" if (project_root / "wiki" / ".obsidian").exists() else "plain_markdown"

    bootstrap_candidates = []
    for path in ("AGENTS.md", "CLAUDE.md"):
        if (project_root / path).exists():
            bootstrap_candidates.append(path)
    if "AGENTS.md" in bootstrap_candidates:
        likely_bootstrap_renderer = "codex_agents_md"
        likely_bootstrap_target_path = "AGENTS.md"
        likely_agent_platform = "codex"
    elif "CLAUDE.md" in bootstrap_candidates:
        likely_bootstrap_renderer = "claude_md"
        likely_bootstrap_target_path = "CLAUDE.md"
        likely_agent_platform = "claude"
    else:
        likely_bootstrap_renderer = "codex_agents_md"
        likely_bootstrap_target_path = "AGENTS.md"
        likely_agent_platform = "generic"

    if (project_root / ".cursor").exists():
        likely_editor = "cursor"
    elif (project_root / ".vscode").exists():
        likely_editor = "vscode"
    elif (project_root / ".idea").exists():
        likely_editor = "jetbrains"
    else:
        likely_editor = "unknown"

    likely_log_root = (
        os.environ.get("SESSIONMEMORY_CODEX_SESSIONS_ROOT", "").strip()
        or os.environ.get("CODEX_SESSIONS_ROOT", "").strip()
        or str(Path.home() / ".codex" / "sessions")
    )
    likely_log_adapter = "codex_jsonl"
    existing_configs = sorted(
        str(path.relative_to(project_root)).replace("\\", "/")
        for path in (project_root / "config").glob("*.json")
    ) if (project_root / "config").exists() else []
    sibling_projects = detect_sibling_projects(project_root)
    available_llm_envs = {
        "OPENAI_API_KEY": bool(os.environ.get("OPENAI_API_KEY")),
        "SESSIONMEMORY_OPENAI_BASE_URL": bool(os.environ.get("SESSIONMEMORY_OPENAI_BASE_URL")),
        "SESSIONMEMORY_OPENAI_MODEL": bool(os.environ.get("SESSIONMEMORY_OPENAI_MODEL")),
    }

    return {
        "operating_system": os_name,
        "project_root": str(project_root),
        "likely_editor": likely_editor,
        "likely_agent_platform": likely_agent_platform,
        "likely_markdown_mode": likely_markdown_mode,
        "likely_bootstrap_renderer": likely_bootstrap_renderer,
        "likely_bootstrap_target_path": likely_bootstrap_target_path,
        "likely_log_root": likely_log_root,
        "likely_log_adapter": likely_log_adapter,
        "existing_bootstrap_files": bootstrap_candidates,
        "existing_config_files": existing_configs,
        "detected_sibling_projects": sibling_projects,
        "available_llm_envs": available_llm_envs,
    }


def apply_detected_defaults(config: ProductConfig, detected: dict[str, object]) -> ProductConfig:
    if detected["likely_markdown_mode"] == "plain_markdown":
        config = replace_markdown_mode(config, "plain_markdown")
    if detected["likely_bootstrap_renderer"] != config.agent_platform.bootstrap_renderer:
        config = replace_bootstrap_renderer(
            config,
            str(detected["likely_bootstrap_renderer"]),
            str(detected["likely_bootstrap_target_path"]),
        )
    config = replace(
        config,
        environment=type(config.environment)(
            operating_system=str(detected["operating_system"]),
            editor=str(detected["likely_editor"]),
            repo_root=str(detected["project_root"]),
        ),
        log_sources=(
            type(config.log_sources[0])(
                adapter=str(detected["likely_log_adapter"]),
                root_alias="agent_sessions",
                absolute_path=str(detected["likely_log_root"]),
                include_glob="**/*.jsonl",
            ),
        ),
    )
    return config


def build_inferred_options(detected: dict[str, object]) -> tuple[OnboardingOption, ...]:
    options = [
        OnboardingOption(
            option_id="operating_system",
            label="Host operating system",
            inferred_value=str(detected["operating_system"]),
            confidence="high",
            rationale="Detected directly from the current runtime platform.",
            configurable_in="config/product_config.json.environment.operating_system",
            consumer_confirmation_needed=False,
        ),
        OnboardingOption(
            option_id="editor",
            label="Primary editor/workspace",
            inferred_value=str(detected["likely_editor"]),
            confidence="medium" if detected["likely_editor"] != "unknown" else "low",
            rationale="Inferred from editor-specific folders in the repo.",
            configurable_in="config/product_config.json.environment.editor",
            consumer_confirmation_needed=True,
        ),
        OnboardingOption(
            option_id="agent_platform",
            label="Primary code-agent workflow",
            inferred_value=str(detected["likely_agent_platform"]),
            confidence="medium" if detected["existing_bootstrap_files"] else "low",
            rationale="Inferred from existing bootstrap files such as AGENTS.md or CLAUDE.md.",
            configurable_in="config/product_config.json.agent_platform",
            consumer_confirmation_needed=True,
        ),
        OnboardingOption(
            option_id="bootstrap_target",
            label="Bootstrap target file",
            inferred_value=str(detected["likely_bootstrap_target_path"]),
            confidence="medium" if detected["existing_bootstrap_files"] else "low",
            rationale="Inferred from existing bootstrap targets in the repo.",
            configurable_in="config/product_config.json.agent_platform.bootstrap_target_path",
            consumer_confirmation_needed=True,
        ),
        OnboardingOption(
            option_id="markdown_mode",
            label="Memory markdown dialect",
            inferred_value=str(detected["likely_markdown_mode"]),
            confidence="medium",
            rationale="Inferred from whether an Obsidian workspace already exists.",
            configurable_in="config/product_config.json.markdown_output",
            consumer_confirmation_needed=True,
        ),
        OnboardingOption(
            option_id="log_root",
            label="Primary session-log root",
            inferred_value=str(detected["likely_log_root"]),
            confidence="medium" if str(detected["likely_log_root"]) else "low",
            rationale="Inferred from environment variables first, then from the default Codex session location.",
            configurable_in="config/product_config.json.log_sources + config/source_roots.json",
            consumer_confirmation_needed=True,
        ),
        OnboardingOption(
            option_id="sibling_projects",
            label="Nearby project repositories",
            inferred_value=", ".join(str(item) for item in detected["detected_sibling_projects"]) or None,
            confidence="low",
            rationale="Nearby folders were scanned, but only the consumer can confirm which repos should participate in memory.",
            configurable_in="config/product_config.json.project_sources + project_aliases",
            consumer_confirmation_needed=True,
        ),
        OnboardingOption(
            option_id="llm_credentials",
            label="LLM provider availability",
            inferred_value="available" if detected["available_llm_envs"]["OPENAI_API_KEY"] else "missing",
            confidence="high",
            rationale="Based on current environment variables, not on provider reachability.",
            configurable_in="environment variables + config/product_config.json.*.provider",
            consumer_confirmation_needed=False,
        ),
    ]
    return tuple(options)


def build_onboarding_questions(detected: dict[str, object]) -> tuple[OnboardingQuestion, ...]:
    markdown_default = "A" if detected["likely_markdown_mode"] == "obsidian_markdown" else "B"
    bootstrap_default = {
        "codex_agents_md": "A",
        "claude_md": "B",
    }.get(str(detected["likely_bootstrap_renderer"]), "C")
    editor_default = "A" if detected["likely_editor"] == "cursor" else "C"
    agent_default = {"codex": "A", "claude": "B"}.get(str(detected["likely_agent_platform"]), "C")

    return (
        OnboardingQuestion(
            question_id="agent_platform",
            prompt="Which agent workflow should SessionMemory optimize for first?",
            why_it_matters="This chooses the bootstrap renderer, target file, and default startup flow for new agent sessions.",
            detected_value=str(detected["likely_agent_platform"]),
            recommended_option=agent_default,
            options=(
                {"key": "A", "label": "Codex", "description": "Use AGENTS.md and Codex-oriented bootstrap defaults."},
                {"key": "B", "label": "Claude", "description": "Use CLAUDE.md and Claude-oriented bootstrap defaults."},
                {"key": "C", "label": "Generic", "description": "Keep bootstrap neutral so multiple agents can share it."},
            ),
        ),
        OnboardingQuestion(
            question_id="markdown_mode",
            prompt="Confirm markdown output mode.",
            why_it_matters="This controls whether memory uses Obsidian-specific features like wikilinks and tags.",
            detected_value=str(detected["likely_markdown_mode"]),
            recommended_option=markdown_default,
            options=(
                {"key": "A", "label": "Obsidian markdown", "description": "Frontmatter, tags, and wikilinks enabled."},
                {"key": "B", "label": "Plain markdown", "description": "Portable markdown without Obsidian syntax."},
                {"key": "C", "label": "Portable first", "description": "Prefer plain markdown now, keep richer renderers possible later."},
            ),
        ),
        OnboardingQuestion(
            question_id="bootstrap_target",
            prompt="Confirm bootstrap target file strategy.",
            why_it_matters="This determines which file an agent should read first at the start of a fresh session.",
            detected_value=str(detected["likely_bootstrap_target_path"]),
            recommended_option=bootstrap_default,
            options=(
                {"key": "A", "label": "AGENTS.md", "description": "Codex-oriented bootstrap target."},
                {"key": "B", "label": "CLAUDE.md", "description": "Claude-oriented bootstrap target."},
                {"key": "C", "label": "Generic bootstrap", "description": "Keep a neutral bootstrap artifact as primary."},
            ),
        ),
        OnboardingQuestion(
            question_id="editor",
            prompt="Confirm detected editor/workflow environment.",
            why_it_matters="Editor conventions affect bootstrap placement, repo ergonomics, and what the agent can infer locally.",
            detected_value=str(detected["likely_editor"]),
            recommended_option=editor_default,
            options=(
                {"key": "A", "label": "Cursor", "description": "Optimize defaults for Cursor plus Codex workflows."},
                {"key": "B", "label": "VS Code", "description": "Optimize for a more editor-neutral repo setup."},
                {"key": "C", "label": "Other", "description": "Keep the setup generic and avoid editor-specific assumptions."},
            ),
        ),
        OnboardingQuestion(
            question_id="log_root",
            prompt="Which session-log source should SessionMemory ingest?",
            why_it_matters="The core product goal depends on reading past agent conversation logs from the right place.",
            detected_value=str(detected["likely_log_root"]),
            recommended_option="A",
            options=(
                {"key": "A", "label": "Use detected path", "description": "Start with the inferred Codex session-log location."},
                {"key": "B", "label": "Custom path", "description": "Point to another local log directory."},
                {"key": "C", "label": "Different adapter later", "description": "Keep the design open for another agent-log format."},
            ),
        ),
        OnboardingQuestion(
            question_id="participating_projects",
            prompt="Which repositories should be included in project memory and routing?",
            why_it_matters="This determines the project graph, alias resolution, and cross-project memory boundaries.",
            detected_value=", ".join(str(item) for item in detected["detected_sibling_projects"]) or None,
            recommended_option="A",
            options=(
                {"key": "A", "label": "Current repo only", "description": "Keep memory scoped to this repo for now."},
                {"key": "B", "label": "Current + siblings", "description": "Include nearby related repos for cross-project memory."},
                {"key": "C", "label": "Manual selection", "description": "Let the consumer specify exactly which repos participate."},
            ),
        ),
        OnboardingQuestion(
            question_id="promotion_policy",
            prompt="How cautious should durable memory promotion be?",
            why_it_matters="This controls when repeated conversation patterns become persistent user or project rules.",
            detected_value=None,
            recommended_option="A",
            options=(
                {"key": "A", "label": "Confirm inferred", "description": "Explicit user promotions persist; inferred rules stay reviewable."},
                {"key": "B", "label": "Auto-promote repeated", "description": "Repeated inferred rules can become durable automatically."},
                {"key": "C", "label": "Project-only auto", "description": "Auto-promote repeated project rules, but not global user rules."},
            ),
        ),
    )


def detect_sibling_projects(project_root: Path) -> list[str]:
    siblings: list[str] = []
    parent = project_root.parent
    if not parent.exists():
        return siblings
    for path in sorted(parent.iterdir()):
        if path == project_root or not path.is_dir():
            continue
        if (path / ".git").exists() or (path / "README.md").exists():
            siblings.append(path.name)
    return siblings[:12]


def replace_markdown_mode(config: ProductConfig, mode: str) -> ProductConfig:
    renderer = MARKDOWN_RENDERERS[mode]
    return replace(
        config,
        markdown_output=type(config.markdown_output)(
            mode=renderer.adapter_id,
            root_dir=config.markdown_output.root_dir,
            enable_frontmatter=config.markdown_output.enable_frontmatter,
            enable_tags=renderer.adapter_id == "obsidian_markdown",
            enable_wikilinks=renderer.adapter_id == "obsidian_markdown",
        ),
    )


def replace_bootstrap_renderer(config: ProductConfig, renderer_id: str, target_path: str) -> ProductConfig:
    if renderer_id not in BOOTSTRAP_RENDERERS:
        renderer_id = "generic_bootstrap_md"
    platform = "codex" if renderer_id == "codex_agents_md" else "claude" if renderer_id == "claude_md" else "generic"
    return replace(
        config,
        agent_platform=type(config.agent_platform)(
            platform=platform,
            bootstrap_renderer=renderer_id,
            bootstrap_target_path=target_path,
        ),
    )


def write_product_config(config_path: Path, config: ProductConfig) -> None:
    ensure_directory(config_path.parent)
    config_path.write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")


def write_agent_onboarding_brief(
    brief_path: Path,
    project_root: Path,
    detected: dict[str, object],
    inferred_options: tuple[OnboardingOption, ...],
    questions: tuple[OnboardingQuestion, ...],
    config: ProductConfig,
) -> None:
    ensure_directory(brief_path.parent)
    lines = [
        "# SessionMemory Agent Configuration Brief",
        "",
        PROJECT_GOAL,
        "",
        "## Agent Workflow",
        "",
        "1. Read this brief and the repository README.",
        "2. Start from the inferred options below and trust high-confidence detections unless the consumer overrides them.",
        "3. Ask the consumer only the unresolved questions that cannot be verified safely from local context.",
        "4. After confirmation, edit the product/source config files and any bootstrap target files needed for that workflow.",
        "",
        "## Inferred Options",
        "",
    ]
    for option in inferred_options:
        lines.append(
            f"- `{option.option_id}`: inferred=`{option.inferred_value or 'unknown'}`; confidence=`{option.confidence}`; "
            f"confirm=`{'yes' if option.consumer_confirmation_needed else 'no'}`; config=`{option.configurable_in}`"
        )
        lines.append(f"  - {option.rationale}")
    lines.extend(["", "## Questions For The Consumer", ""])
    for question in questions:
        lines.append(f"- `{question.question_id}`: {question.prompt}")
        lines.append(f"  - Why: {question.why_it_matters}")
        if question.detected_value:
            lines.append(f"  - Detected: `{question.detected_value}`")
        lines.append(f"  - Recommended: `{question.recommended_option}`")
    lines.extend(
        [
            "",
            "## Suggested Files To Edit",
            "",
            "- `config/product_config.json`",
            "- `config/source_roots.json`",
            f"- `{config.agent_platform.bootstrap_target_path}`",
            "",
            "## Detected Environment",
            "",
            "```json",
            json.dumps(detected, indent=2, sort_keys=True),
            "```",
            "",
        ]
    )
    brief_path.write_text("\n".join(lines), encoding="utf-8")
