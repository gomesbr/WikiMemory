from __future__ import annotations

from dataclasses import dataclass

GLOBAL_SCOPE = "global"
PROJECT_SCOPE = "project"


@dataclass(frozen=True)
class MemoryFileDefinition:
    key: str
    scope: str
    relative_path_template: str
    purpose: str
    optional: bool = False
    decays: bool = False

    def render_relative_path(self, project_slug: str | None = None) -> str:
        if "{project}" in self.relative_path_template:
            if not project_slug:
                raise ValueError(f"project_slug required for memory file {self.key}")
            return self.relative_path_template.format(project=project_slug)
        return self.relative_path_template


MEMORY_FILE_DEFINITIONS = {
    "global_user_rules": MemoryFileDefinition(
        key="global_user_rules",
        scope=GLOBAL_SCOPE,
        relative_path_template="memory/global/user-rules.md",
        purpose="Durable cross-project user rules and preferences.",
    ),
    "project_summary": MemoryFileDefinition(
        key="project_summary",
        scope=PROJECT_SCOPE,
        relative_path_template="memory/projects/{project}/project.md",
        purpose="Stable project identity, goals, and durable context.",
    ),
    "project_recent": MemoryFileDefinition(
        key="project_recent",
        scope=PROJECT_SCOPE,
        relative_path_template="memory/projects/{project}/recent.md",
        purpose="Fluid recent context that should roll forward over time.",
        decays=True,
    ),
    "project_rules": MemoryFileDefinition(
        key="project_rules",
        scope=PROJECT_SCOPE,
        relative_path_template="memory/projects/{project}/rules.md",
        purpose="Project-scoped durable rules and constraints.",
    ),
    "project_lessons": MemoryFileDefinition(
        key="project_lessons",
        scope=PROJECT_SCOPE,
        relative_path_template="memory/projects/{project}/lessons.md",
        purpose="High-signal lessons learned worth preserving.",
        optional=True,
    ),
}


MEMORY_CLASS_TO_FILE_KEY = {
    "global_user_rules": "global_user_rules",
    "project_rules": "project_rules",
    "stable_project_summary": "project_summary",
    "recent_project_state": "project_recent",
    "project_lessons": "project_lessons",
}


PROMOTION_STATES = (
    "candidate",
    "repeated",
    "durable",
    "explicit",
)
