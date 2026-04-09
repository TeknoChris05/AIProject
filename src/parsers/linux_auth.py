from __future__ import annotations
import re
from datetime import datetime
from dateutil import parser as dtparser
from typing import Iterable, List, Optional
from ..models import Event

# Examples we handle:
# Mar  2 09:12:34 hostname sshd[1234]: Failed password for invalid user admin from 1.2.3.4 port 5555 ssh2
# Mar  2 09:13:10 hostname sshd[1234]: Accepted password for chris from 1.2.3.4 port 5555 ssh2
# Mar  2 09:14:01 hostname sudo:    chris : TTY=pts/0 ; PWD=/home/chris ; USER=root ; COMMAND=/bin/bash

AUTH_RE = re.compile(
    r"^(?P<ts>\w{3}\s+\d+\s+\d+:\d+:\d+)\s+"
    r"(?P<host>\S+)\s+"
    r"(?P<program>[a-zA-Z0-9_\-/]+)"
    r"(?:\[(?P<pid>\d+)\])?:\s+"
    r"(?P<msg>.*)$"
)

IP_RE = re.compile(r"\b(?P<ip>(?:\d{1,3}\.){3}\d{1,3})\b")

FAILED_SSH_RE = re.compile(r"Failed password for (invalid user )?(?P<user>\S+)")
ACCEPTED_SSH_RE = re.compile(r"Accepted (password|publickey) for (?P<user>\S+)")
SUDO_RE = re.compile(r"sudo:\s+(?P<user>\S+)\s*:\s+.*COMMAND=(?P<cmd>.+)$")
NEWUSER_RE = re.compile(r"(new user|useradd)\b", re.IGNORECASE)


def _parse_ts(ts_prefix: str, year_hint: Optional[int] = None) -> datetime:
    # syslog/auth logs omit year; dateutil fills current year; we allow hint override.
    dt = dtparser.parse(ts_prefix, fuzzy=True)
    if year_hint is not None:
        dt = dt.replace(year=year_hint)
    return dt


def parse_auth_lines(lines: Iterable[str], source: str = "auth.log") -> List[Event]:
    events: List[Event] = []
    for raw in lines:
        raw = raw.rstrip("\n")
        m = AUTH_RE.match(raw)
        if not m:
            continue

        ts = _parse_ts(m.group("ts"))
        host = m.group("host")
        program = m.group("program")
        pid = m.group("pid")
        msg = m.group("msg")

        pid_int = int(pid) if pid else None
        ip_match = IP_RE.search(msg)
        src_ip = ip_match.group("ip") if ip_match else None

        event_type = "auth.other"
        severity = "info"
        user = None
        fields = {}

        if "Failed password" in msg:
            event_type = "ssh.failed_login"
            severity = "low"
            fm = FAILED_SSH_RE.search(msg)
            if fm:
                user = fm.group("user")
        elif "Accepted" in msg and "sshd" in program:
            event_type = "ssh.success_login"
            severity = "medium"
            am = ACCEPTED_SSH_RE.search(msg)
            if am:
                user = am.group("user")
        elif msg.startswith("sudo:"):
            event_type = "sudo.command"
            severity = "medium"
            sm = SUDO_RE.search(msg)
            if sm:
                user = sm.group("user")
                fields["command"] = sm.group("cmd")
        elif NEWUSER_RE.search(msg):
            event_type = "account.change"
            severity = "high"

        events.append(
            Event(
                ts=ts,
                source=source,
                host=host,
                program=program,
                pid=pid_int,
                event_type=event_type,
                severity=severity,
                user=user,
                src_ip=src_ip,
                message=msg,
                raw=raw,
                fields=fields,
            )
        )
    return events