#!/usr/bin/env python3
"""GUID range of this mod and a local replay of the anno-mods/GuidRanges registration.

    python tools/guidrange.py check  <GuidRanges clone>   # overlap / safe-range check against the registry table
    python tools/guidrange.py apply  <GuidRanges clone>   # add our row on a local branch and commit it (no push)

The registry is a markdown table in 117/guids.md. A pull request adds one row to the
"Public GUID Ranges" table, sorted by start ID.
"""
import re
import subprocess
import sys
from pathlib import Path

USER = "taskr"
RANGE_START = 2_110_000_000
RANGE_END = 2_110_000_999
SAFE_START, SAFE_END = 1_337_471_142, 2_147_483_647
FIRST_FOLDER_GUID = RANGE_START  # folder categories use RANGE_START+0 .. ; texts use the same GUIDs as LineIds
TABLE_FILE = Path("117") / "guids.md"
ROW_RE = re.compile(r"^\|\s*(?P<user>[^|]+?)\s*\|\s*(?P<start>[\d.]+)\s*\|\s*(?P<end>[\d.]*)\s*\|")


def fmt(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def parse_int(s: str):
    s = s.strip().replace(".", "")
    return int(s) if s.isdigit() else None


def our_row() -> str:
    return f"| {USER:<15} | {fmt(RANGE_START):>13} | {fmt(RANGE_END):>13} |"


def read_ranges(text: str):
    out = []
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        a, b = parse_int(m["start"]), parse_int(m["end"])
        if a is not None and b is not None:
            out.append((m["user"].strip("*_ "), a, b))
    return out


def check(text: str):
    problems = []
    if not (SAFE_START <= RANGE_START <= RANGE_END <= SAFE_END):
        problems.append("range is outside the safe range")
    if RANGE_END - RANGE_START + 1 > 100_000:
        problems.append("more than 100.000 GUIDs needs one entry per 100.000")
    for user, a, b in read_ranges(text):
        if user == USER:
            continue
        if RANGE_START <= b and a <= RANGE_END:
            problems.append(f"overlaps {user} ({fmt(a)} - {fmt(b)})")
    return problems


def apply(repo: Path):
    f = repo / TABLE_FILE
    text = f.read_text(encoding="utf-8")
    problems = check(text)
    if problems:
        raise SystemExit("not applied: " + "; ".join(problems))
    lines = text.splitlines()
    insert_at = None
    in_public = False
    for i, line in enumerate(lines):
        if line.startswith("## Public GUID Ranges"):
            in_public = True
        m = ROW_RE.match(line)
        if in_public and m:
            a = parse_int(m["start"])
            if a is not None and a > RANGE_START and "range start" not in m["user"]:
                insert_at = i
                break
    if insert_at is None:
        raise SystemExit("no insertion point found")
    lines.insert(insert_at, our_row())
    f.write_text("\n".join(lines) + "\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "checkout", "-b", f"add-{USER}-range"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", str(TABLE_FILE)], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", f"Add GUID range for {USER}"], check=True)
    print(subprocess.run(["git", "-C", str(repo), "show", "--stat", "--format=%s", "HEAD"], capture_output=True, text=True).stdout)
    print(subprocess.run(["git", "-C", str(repo), "diff", "HEAD~1", "HEAD", "-U1"], capture_output=True, text=True).stdout)


def main(argv):
    if len(argv) != 3 or argv[1] not in ("check", "apply"):
        raise SystemExit(__doc__)
    repo = Path(argv[2])
    text = (repo / TABLE_FILE).read_text(encoding="utf-8")
    if argv[1] == "check":
        problems = check(text)
        print(f"{USER}: {fmt(RANGE_START)} - {fmt(RANGE_END)}")
        print("row:", our_row())
        print("OK, no overlap" if not problems else "PROBLEMS: " + "; ".join(problems))
        raise SystemExit(1 if problems else 0)
    apply(repo)


if __name__ == "__main__":
    main(sys.argv)
