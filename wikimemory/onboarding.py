from __future__ import annotations

import json
import os
from dataclasses import dataclass
from dataclasses import replace
from pathlib import Path

from .adapters import BOOTSTRAP_RENDERERS, MARKDOWN_RENDERERS
from .discovery import ensure_directory
from .product_config import ProductConfig, default_product_config, detect_operating_system


@dataclass(frozen=True)
class OnboardingQuestion:
    question_id: str
    prompt: str
    detected_value: str | None
    recommended_option: str
    options: tuple[dict[str, str], ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "question_id": self.question_id,
            "prompt": self.prompt,
            "detected_value": self.detected_value,
            "recommended_option": self.recommended_option,
            "options": [dict(option) for option in self.options],
        }


@dataclass(frozen=True)
class OnboardingReport:
    project_root: str
    detected: dict[str, object]
    recommended_product_config: dict[str, object]
    questions: tuple[OnboardingQuestion, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "project_root": self.project_root,
            "detected": self.detected,
            "recommended_product_config": self.recommended_product_config,
            "questions": [question.to_dict() for question in self.questions],
        }


def run_onboarding(project_root: Path | str, config_path: Path | str | None = None) -> OnboardingReport:
    project_root = Path(project_root).resolve()
    detected = detect_environment(project_root)
    draft_config = default_product_config(project_root)
    if detected["likely_markdown_mode"] == "plain_markdown":
        draft_config = replace_markdown_mode(draft_config, "plain_markdown")
    if detected["likely_bootstrap_renderer"] != draft_config.agent_platform.bootstrap_renderer:
        draft_config = replace_bootstrap_renderer(
            draft_config,
            str(detected["likely_bootstrap_renderer"]),
            str(detected["likely_bootstrap_target_path"]),
        )

    if config_path is not None:
        write_product_config(Path(config_path), draft_config)

    questions = build_onboarding_questions(detected)
    return OnboardingReport(
        project_root=str(project_root),
        detected=detected,
        recommended_product_config=draft_config.to_dict(),
        questions=questions,
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
    elif "CLAUDE.md" in bootstrap_candidates:
        likely_bootstrap_renderer = "claude_md"
        likely_bootstrap_target_path = "CLAUDE.md"
    else:
        likely_bootstrap_renderer = "codex_agents_md"
        likely_bootstrap_target_path = "AGENTS.md"

    if (project_root / ".cursor").exists():
        likely_editor = "cursor"
    elif (project_root / ".vscode").exists():
        likely_editor = "vscode"
    else:
        likely_editor = "unknown"

    log_root = os.environ.get("WIKIMEMORY_CODEX_SESSIONS_ROOT", "").strip() or str(Path.home() / ".codex" / "sessions")
    existing_configs = sorted(str(path.relative_to(project_root)).replace("\\", "/") for path in (project_root / "config").glob("*.json")) if (project_root / "config").exists() else []

    return {
        "operating_system": os_name,
        "project_root": str(project_root),
        "likely_editor": likely_editor,
        "likely_markdown_mode": likely_markdown_mode,
        "likely_bootstrap_renderer": likely_bootstrap_renderer,
        "likely_bootstrap_target_path": likely_bootstrap_target_path,
        "likely_log_root": log_root,
        "existing_bootstrap_files": bootstrap_candidates,
        "existing_config_files": existing_configs,
    }


def build_onboarding_questions(detected: dict[str, object]) -> tuple[OnboardingQuestion, ...]:
    markdown_default = "A" if detected["likely_markdown_mode"] == "obsidian_markdown" else "B"
    bootstrap_default = {
        "codex_agents_md": "A",
        "claude_md": "B",
    }.get(str(detected["likely_bootstrap_renderer"]), "C")
    editor_default = "A" if detected["likely_editor"] == "cursor" else "C"

    return (
        OnboardingQuestion(
            question_id="markdown_mode",
            prompt="Confirm markdown output mode.",
            detected_value=str(detected["likely_markdown_mode"]),
            recommended_option=markdown_default,
            options=(
                {"key": "A", "label": "Obsidian markdown", "description": "Frontmatter, tags, and wikilinks enabled."},
                {"key": "B", "label": "Plain markdown", "description": "Portable markdown without Obsidian syntax."},
                {"key": "C", "label": "Keep both later", "description": "Use one now, but preserve renderer portability."},
            ),
        ),
        OnboardingQuestion(
            question_id="bootstrap_target",
            prompt="Confirm bootstrap target file strategy.",
            detected_value=str(detected["likely_bootstrap_target_path"]),
            recommended_option=bootstrap_default,
            options=(
                {"key": "A", "label": "AGENTS.md", "description": "Codex-oriented bootstrap target."},
                {"key": "B", "label": "CLAUDE.md", "description": "Claude-oriented bootstrap target."},
                {"key": "C", "label": "Generic first", "description": "Keep a neutral bootstrap artifact as primary."},
            ),
        ),
        OnboardingQuestion(
            question_id="editor",
            prompt="Confirm detected editor/workflow environment.",
            detected_value=str(detected["likely_editor"]),
            recommended_option=editor_default,
            options=(
                {"key": "A", "label": "Cursor/Codex", "description": "Optimize defaults for Cursor plus Codex workflows."},
                {"key": "B", "label": "Claude workflow", "description": "Optimize defaults for Claude-oriented bootstrap usage."},
                {"key": "C", "label": "Generic", "description": "Keep environment-neutral defaults."},
            ),
        ),
        OnboardingQuestion(
            question_id="log_root",
            prompt="Confirm session log root.",
            detected_value=str(detected["likely_log_root"]),
            recommended_option="A",
            options=(
                {"key": "A", "label": "Use detected", "description": "Use the detected Codex session-log location."},
                {"key": "B", "label": "Configure manually", "description": "Set a custom log root in product/source config."},
                {"key": "C", "label": "Adapter later", "description": "Keep config extensible for another log format."},
            ),
        ),
        OnboardingQuestion(
            question_id="project_routing",
            prompt="Confirm unresolved-project routing policy.",
            detected_value=None,
            recommended_option="A",
            options=(
                {"key": "A", "label": "LLM for unresolved", "description": "Use deterministic aliases first, then LLM only for generic project buckets."},
                {"key": "B", "label": "Deterministic only", "description": "Never call a provider during project association."},
                {"key": "C", "label": "Ask before routing", "description": "Keep unresolved records until reviewed."},
            ),
        ),
        OnboardingQuestion(
            question_id="promotion_policy",
            prompt="Confirm inferred-rule promotion policy.",
            detected_value=None,
            recommended_option="A",
            options=(
                {"key": "A", "label": "Confirm inferred", "description": "Explicit user promotions become durable; inferred repeated rules stay reviewable."},
                {"key": "B", "label": "Auto-promote repeated", "description": "Repeated inferred rules can become durable automatically."},
                {"key": "C", "label": "Project-only auto", "description": "Auto-promote repeated project rules, but not global rules."},
            ),
        ),
    )


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
    return replace(
        config,
        agent_platform=type(config.agent_platform)(
            platform=config.agent_platform.platform,
            bootstrap_renderer=renderer_id,
            bootstrap_target_path=target_path,
        ),
    )


def write_product_config(config_path: Path, config: ProductConfig) -> None:
    ensure_directory(config_path.parent)
    config_path.write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")
