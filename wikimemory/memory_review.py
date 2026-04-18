from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .normalization import append_jsonl_text

STATE_SCHEMA_VERSION = 1
MEMORY_REVIEW_SCHEMA_VERSION = 1


class MemoryReviewError(DiscoveryError):
    """Fatal memory review error."""


@dataclass(frozen=True)
class MemoryReviewRunReport:
    run_id: str
    started_at: str
    finished_at: str
    pending_count: int
    approved_count: int
    rejected_count: int
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "pending_count": self.pending_count,
            "approved_count": self.approved_count,
            "rejected_count": self.rejected_count,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class MemoryReviewResult:
    report: MemoryReviewRunReport
    decisions_path: Path
    review_items_path: Path
    run_log_path: Path


def run_memory_review(
    *,
    memory_dir: Path | str,
    state_dir: Path | str,
    audits_dir: Path | str,
    approve: Iterable[str] | None = None,
    reject: Iterable[str] | None = None,
) -> MemoryReviewResult:
    memory_dir = Path(memory_dir)
    state_dir = Path(state_dir)
    audits_dir = Path(audits_dir)
    ensure_directory(state_dir)
    ensure_directory(audits_dir)

    run_id = f"memory-review-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()
    decisions_path = state_dir / "memory_review_decisions.json"
    run_log_path = state_dir / "memory_review_runs.jsonl"
    review_items_path = audits_dir / "memory_review_items.jsonl"
    previous_run_log = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""

    try:
        decisions_payload = load_decisions(decisions_path)
        decisions = dict(decisions_payload.get("decisions", {}))
        for item_id in approve or ():
            decisions[str(item_id)] = {"decision": "approved", "decided_at": utc_now(), "run_id": run_id}
        for item_id in reject or ():
            decisions[str(item_id)] = {"decision": "rejected", "decided_at": utc_now(), "run_id": run_id}

        review_items = load_review_items(memory_dir)
        pending_rows = []
        for item in review_items:
            item_id = str(item.get("item_id") or "")
            decision = str(decisions.get(item_id, {}).get("decision") or "pending")
            row = dict(item)
            row["review_decision"] = decision
            pending_rows.append(row)
        write_jsonl(review_items_path, pending_rows)

        approved_count = sum(1 for value in decisions.values() if value.get("decision") == "approved")
        rejected_count = sum(1 for value in decisions.values() if value.get("decision") == "rejected")
        pending_count = sum(1 for row in pending_rows if row.get("review_decision") == "pending")
        atomic_write_text(
            decisions_path,
            json.dumps(
                {
                    "schema_version": STATE_SCHEMA_VERSION,
                    "memory_review_schema_version": MEMORY_REVIEW_SCHEMA_VERSION,
                    "last_run_id": run_id,
                    "decisions": decisions,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
        )
        finished_at = utc_now()
        report = MemoryReviewRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=finished_at,
            pending_count=pending_count,
            approved_count=approved_count,
            rejected_count=rejected_count,
            success=True,
            fatal_error_summary=None,
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, report.to_dict()))
        return MemoryReviewResult(report, decisions_path, review_items_path, run_log_path)
    except Exception as exc:
        finished_at = utc_now()
        report = MemoryReviewRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=finished_at,
            pending_count=0,
            approved_count=0,
            rejected_count=0,
            success=False,
            fatal_error_summary=str(exc),
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, report.to_dict()))
        return MemoryReviewResult(report, decisions_path, review_items_path, run_log_path)


def load_review_items(memory_dir: Path) -> list[dict[str, object]]:
    path = memory_dir / "_meta" / "promotion_review.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_decisions(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"decisions": {}}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    atomic_write_text(
        path,
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows),
    )
