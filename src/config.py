from __future__ import annotations
from pydantic import BaseModel


class PipelineConfig(BaseModel):
    max_lines: int = 200_000

    # Timeline
    timeline_limit: int = 200

    # Brute force (SSH failed logins)
    brute_force_fail_threshold: int = 8
    brute_force_window_minutes: int = 10

    # Syslog parsing (optional)
    include_syslog: bool = False
class Settings:
    FAILED_LOGIN_THRESHOLD = 5
    SUSPICIOUS_IPS = [
        "192.168.1.100",
        "10.0.0.66"
    ]

    MODEL_RISK_THRESHOLD = 0.7

    DEFAULT_INPUT_FILE = "data/incidents.json"
    DEFAULT_OUTPUT_FILE = "output/report.json"


settings = Settings()
