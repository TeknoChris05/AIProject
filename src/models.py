from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List


class Event(BaseModel):
    ts: datetime
    source: str = "linux"
    host: Optional[str] = None
    program: Optional[str] = None
    pid: Optional[int] = None

    event_type: str
    severity: str = "info"  # info|low|medium|high

    user: Optional[str] = None
    src_ip: Optional[str] = None

    message: str
    raw: str
    fields: Dict[str, Any] = Field(default_factory=dict)


class Finding(BaseModel):
    rule_id: str
    title: str
    severity: str  # low|medium|high
    summary: str
    evidence: List[Event]
    tags: List[str] = Field(default_factory=list)


class Report(BaseModel):
    title: str
    generated_at: datetime

    time_range_start: Optional[datetime] = None
    time_range_end: Optional[datetime] = None

    executive_summary: str
    key_findings: List[Finding]
    timeline: List[Event]
    recommended_actions: List[str]
    notes: List[str] = Field(default_factory=list)