from pathlib import Path
from typing import List

def read_text_lines(path: str, max_lines: int = 200000) -> List[str]:
    p = Path(path)
    lines: List[str] = []
    with p.open("r", encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f):
            lines.append(line)
            if i + 1 >= max_lines:
                break
    return lines