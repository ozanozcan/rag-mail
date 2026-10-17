"""Block commits that could leak the owner's mail.

Fails if any checked file is a mail/corpus/credential file, or contains an email
address outside the reserved example domains. Real data lives in ~/.rag-mail/, never here.

Usage: check_no_private_data.py [--staged]   (default: all tracked files)
"""

import re
import subprocess
import sys
from pathlib import Path

BLOCKED_SUFFIXES = {".eml", ".mbox", ".jsonl", ".msg", ".pickle", ".sqlite", ".db"}
BLOCKED_NAMES = re.compile(r"(token|credentials|client_secret)[^/]*\.json$", re.I)
EMAIL = re.compile(r"[\w.+-]+@([\w-]+\.)+[a-z]{2,}", re.I)
# RFC 2606 reserved domains plus GitHub noreply addresses.
ALLOWED_DOMAINS = re.compile(r"@(([\w-]+\.)*example\.(com|org|net)|users\.noreply\.github\.com)$", re.I)


def files(staged: bool) -> list[str]:
    cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"] if staged else ["git", "ls-files"]
    return [f for f in subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.splitlines() if f]


def problems(path: str) -> list[str]:
    p = Path(path)
    if p.suffix.lower() in BLOCKED_SUFFIXES:
        return [f"{path}: mail/corpus file type {p.suffix}"]
    if BLOCKED_NAMES.search(p.name):
        return [f"{path}: credential file"]
    try:
        text = p.read_text(errors="ignore")
    except (FileNotFoundError, IsADirectoryError):
        return []
    return [
        f"{path}:{text.count(chr(10), 0, m.start()) + 1}: email address {m.group(0)!r}"
        for m in EMAIL.finditer(text)
        if not ALLOWED_DOMAINS.search(m.group(0))
    ]


def main() -> int:
    found = [msg for f in files("--staged" in sys.argv) for msg in problems(f)]
    for msg in found:
        print("BLOCKED", msg, file=sys.stderr)
    if found:
        print("Private data guard: use @example.com in fixtures; real data belongs in ~/.rag-mail/.", file=sys.stderr)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
