from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from .discovery import DiscoveryError, atomic_write_text, utc_now
from .product_config import ProductConfig, load_product_config, normalize_weekday


class SchedulerPlanError(DiscoveryError):
    """Fatal scheduler planning error."""


@dataclass(frozen=True)
class SchedulerPlanReport:
    generated_at: str
    latest_log_update_at: str | None
    last_refresh_at: str | None
    last_lint_at: str | None
    ingest_due: bool
    lint_due: bool
    within_schedule_window: bool
    refresh_command: str
    activation_script_path: str

    def to_dict(self) -> dict[str, object]:
        return {
            "generated_at": self.generated_at,
            "latest_log_update_at": self.latest_log_update_at,
            "last_refresh_at": self.last_refresh_at,
            "last_lint_at": self.last_lint_at,
            "ingest_due": self.ingest_due,
            "lint_due": self.lint_due,
            "within_schedule_window": self.within_schedule_window,
            "refresh_command": self.refresh_command,
            "activation_script_path": self.activation_script_path,
        }


@dataclass(frozen=True)
class SchedulerPlanResult:
    report: SchedulerPlanReport
    plan_path: Path
    activation_script_path: Path


def run_scheduler_plan(
    *,
    product_config_path: Path | str,
    state_dir: Path | str,
    scripts_dir: Path | str,
) -> SchedulerPlanResult:
    product_config_path = Path(product_config_path)
    state_dir = Path(state_dir)
    scripts_dir = Path(scripts_dir)
    config = load_product_config(product_config_path)

    registry = load_json(state_dir / "source_registry.json")
    latest_log_update_at = latest_active_log_update(registry)
    last_refresh_at = last_refresh_checkpoint_finished_at(
        state_dir / "memory_refresh_state.json",
        state_dir / "memory_refresh_runs.jsonl",
    )
    last_lint_at = latest_successful_finished_at(state_dir / "memory_lint_runs.jsonl")
    now_local = datetime.now().astimezone()
    within_schedule_window = in_schedule_window(now_local, config)
    ingest_due = schedule_due(
        latest_log_update_at=latest_log_update_at,
        last_run_at=last_refresh_at,
        interval_hours=config.scheduler.ingest_interval_hours,
        require_source_update=config.scheduler.require_log_update_for_ingest,
        now_local=now_local,
        config=config,
    )
    lint_due = schedule_due(
        latest_log_update_at=latest_log_update_at,
        last_run_at=last_lint_at,
        interval_hours=config.scheduler.lint_interval_hours,
        require_source_update=False,
        now_local=now_local,
        config=config,
    )
    refresh_command = build_refresh_command(config)
    activation_script_path = scripts_dir / "install-windows-task.generated.ps1"
    write_activation_script(activation_script_path, config, refresh_command)
    plan_path = state_dir / "scheduler_plan.json"
    report = SchedulerPlanReport(
        generated_at=utc_now(),
        latest_log_update_at=latest_log_update_at,
        last_refresh_at=last_refresh_at,
        last_lint_at=last_lint_at,
        ingest_due=ingest_due,
        lint_due=lint_due,
        within_schedule_window=within_schedule_window,
        refresh_command=refresh_command,
        activation_script_path=str(activation_script_path),
    )
    atomic_write_text(plan_path, json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n")
    return SchedulerPlanResult(report=report, plan_path=plan_path, activation_script_path=activation_script_path)


def build_refresh_command(config: ProductConfig) -> str:
    command = (
        "python -m sessionmemory memory-refresh"
        f" --consumer-profile-extraction-model {config.scheduler.consumer_profile_extraction_model}"
        f" --consumer-profile-merge-model {config.scheduler.consumer_profile_merge_model}"
        f" --consumer-profile-window-max-chars {config.scheduler.consumer_profile_window_max_chars}"
    )
    if config.scheduler.lint_autofix_enabled:
        command += " --lint-fix"
        command += f" --lint-fix-rounds {config.scheduler.lint_autofix_max_rounds}"
    return command


def write_activation_script(path: Path, config: ProductConfig, refresh_command: str) -> None:
    weekdays = ", ".join(config.scheduler.allowed_weekdays)
    content = "\n".join(
        [
            "param(",
            '    [string]$TaskName = "SessionMemoryRefresh",',
            '    [string]$ProjectRoot = (Resolve-Path ".").Path,',
            '    [string]$PythonExe = "python"',
            ")",
            "",
            "# Prepared only. Review this file before running it to activate the scheduler.",
            f"# Allowed weekdays: {weekdays}",
            f"# Local run time: {config.scheduler.run_hour_local:02d}:{config.scheduler.run_minute_local:02d}",
            f"# Refresh command: {refresh_command}",
            "",
            "$action = New-ScheduledTaskAction `",
            "    -Execute $PythonExe `",
            f'    -Argument "-m sessionmemory memory-refresh --consumer-profile-extraction-model {config.scheduler.consumer_profile_extraction_model} --consumer-profile-merge-model {config.scheduler.consumer_profile_merge_model} --consumer-profile-window-max-chars {config.scheduler.consumer_profile_window_max_chars}{" --lint-fix --lint-fix-rounds " + str(config.scheduler.lint_autofix_max_rounds) if config.scheduler.lint_autofix_enabled else ""}" `',
            "    -WorkingDirectory $ProjectRoot",
            "",
            "$trigger = New-ScheduledTaskTrigger `",
            "    -Weekly `",
            f"    -DaysOfWeek {','.join(day.title() for day in config.scheduler.allowed_weekdays)} `",
            f"    -At ([datetime]::Today.AddHours({config.scheduler.run_hour_local}).AddMinutes({config.scheduler.run_minute_local}))",
            "",
            "$settings = New-ScheduledTaskSettingsSet `",
            "    -AllowStartIfOnBatteries `",
            "    -DontStopIfGoingOnBatteries `",
            "    -MultipleInstances IgnoreNew",
            "",
            "# Register-ScheduledTask `",
            "#     -TaskName $TaskName `",
            "#     -Action $action `",
            "#     -Trigger $trigger `",
            "#     -Settings $settings `",
            '#     -Description "Run SessionMemory memory refresh based on prepared scheduler policy."',
            "",
            '# Write-Host "Prepared scheduler activation script. Uncomment Register-ScheduledTask when you want to activate it."',
            "",
        ]
    )
    atomic_write_text(path, content)


def schedule_due(
    *,
    latest_log_update_at: str | None,
    last_run_at: str | None,
    interval_hours: int,
    require_source_update: bool,
    now_local: datetime,
    config: ProductConfig,
) -> bool:
    if not in_schedule_window(now_local, config):
        return False
    if require_source_update and latest_log_update_at:
        if not last_run_at:
            return True
        if parse_iso(latest_log_update_at) <= parse_iso(last_run_at):
            return False
    if not last_run_at:
        return True
    return now_local.astimezone(parse_iso(last_run_at).tzinfo) >= parse_iso(last_run_at) + timedelta(hours=interval_hours)


def in_schedule_window(now_local: datetime, config: ProductConfig) -> bool:
    weekday = normalize_weekday(now_local.strftime("%A"))
    if weekday not in config.scheduler.allowed_weekdays:
        return False
    scheduled_minutes = config.scheduler.run_hour_local * 60 + config.scheduler.run_minute_local
    current_minutes = now_local.hour * 60 + now_local.minute
    return current_minutes >= scheduled_minutes


def latest_active_log_update(payload: dict[str, object]) -> str | None:
    latest = ""
    for record in payload.get("sources", []):
        if not isinstance(record, dict):
            continue
        if str(record.get("status") or "") == "tombstoned":
            continue
        mtime_utc = str(record.get("mtime_utc") or "")
        if mtime_utc and mtime_utc > latest:
            latest = mtime_utc
    return latest or None


def latest_successful_finished_at(path: Path) -> str | None:
    if not path.exists():
        return None
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if not payload.get("success"):
            continue
        finished_at = str(payload.get("finished_at") or "")
        if finished_at > latest:
            latest = finished_at
    return latest or None


def last_successful_refresh_finished_at(state_path: Path, run_log_path: Path) -> str | None:
    state_payload = load_json(state_path)
    state_value = str(state_payload.get("last_successful_refresh_finished_at") or "")
    if state_value:
        return state_value
    return latest_successful_finished_at(run_log_path)


def last_refresh_checkpoint_finished_at(state_path: Path, run_log_path: Path) -> str | None:
    state_payload = load_json(state_path)
    attempted_value = str(state_payload.get("last_attempted_refresh_finished_at") or "")
    if attempted_value:
        return attempted_value
    successful_value = str(state_payload.get("last_successful_refresh_finished_at") or "")
    if successful_value:
        return successful_value
    latest = ""
    if run_log_path.exists():
        for line in run_log_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            payload = json.loads(line)
            finished_at = str(payload.get("finished_at") or "")
            if finished_at > latest:
                latest = finished_at
    return latest or None


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
