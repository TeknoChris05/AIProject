from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from .config import PipelineConfig
from .models import Event, Report, Finding
from .parsers.linux_auth import parse_auth_lines
from .io_utils import read_text_lines
from .rules import rule_bruteforce, rule_sudo_suspicious, rule_account_changes
from .reporting import build_executive_summary, recommended_actions


def run_pipeline(
    auth_log_path: str,
    cfg: Optional[PipelineConfig] = None,
) -> Report:
    cfg = cfg or PipelineConfig()

    # Read log file
    lines = read_text_lines(auth_log_path, max_lines=cfg.max_events)

    # Parse events
    events: List[Event] = parse_auth_lines(lines, source=auth_log_path)

    # Sort events
    events_sorted = sorted(events, key=lambda e: e.ts)

    start = events_sorted[0].ts if events_sorted else None
    end = events_sorted[-1].ts if events_sorted else None

    # Run detection rules
    findings: List[Finding] = []
    findings += [r.finding for r in rule_bruteforce(events, cfg)]
    findings += [r.finding for r in rule_sudo_suspicious(events)]
    findings += [r.finding for r in rule_account_changes(events)]

    # Build timeline
    suspicious = [e for e in events_sorted if e.severity in ("medium", "high")]
    timeline = suspicious[-cfg.timeline_limit:] if suspicious else events_sorted[-cfg.timeline_limit:]

    # Build report
    report = Report(
        title="IncidentLens: Linux Incident Triage Report",
        generated_at=datetime.now(),
        time_range_start=start,
        time_range_end=end,
        executive_summary=build_executive_summary(findings, start, end),
        key_findings=sorted(
            findings,
            key=lambda f: {"high": 0, "medium": 1, "low": 2}.get(f.severity, 3),
        ),
        timeline=timeline,
        recommended_actions=recommended_actions(findings),
        notes=[
            "MVP uses parsing + heuristic detection. Extend with networking logs or AI later.",
        ],
    )

    return report