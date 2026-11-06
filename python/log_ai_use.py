#!/usr/bin/env python3
"""Track DATA120 AI use and a two-step human review/acceptance gate.

This is a cooperative workflow; it cannot authenticate a human or prevent
assistants that ignore AGENTS.md from taking actions.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from zoneinfo import ZoneInfo

LOG = Path(__file__).resolve().parent / "docs" / "ai" / "AI_USE_LOG.md"
HISTORY = "## Assistance history"
NEXT = "## Copy this row for each future use"
GATE = "## AI material reading and acceptance register"
GATE_END = "## Draft disclosure wording"
ZONE = ZoneInfo("America/Edmonton")


def now() -> str:
    """Return local timestamp with a real UTC offset and seconds."""
    return datetime.now(ZONE).isoformat(timespec="seconds")


def clean(value: str) -> str:
    """Make a single Markdown table cell, without private data."""
    return " ".join(value.replace("|", "\\|").split()).strip()


def read_log() -> str:
    text = LOG.read_text(encoding="utf-8")
    if not all(m in text for m in (HISTORY, NEXT, GATE, GATE_END)):
        raise ValueError("AI_USE_LOG.md format not recognized; review manually.")
    return text


def gate_rows(text: str) -> list[list[str]]:
    block = text.split(GATE, 1)[1].split(GATE_END, 1)[0]
    rows = []
    for line in block.splitlines():
        if line.startswith("| ") and not line.startswith("| ---"):
            cells = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(cells) == 7 and cells[0] != "Entry ID":
                rows.append(cells)
    return rows


def replace_row(text: str, entry_id: str, cells: list[str]) -> str:
    lines = text.splitlines(keepends=True)
    inside = False
    for index, line in enumerate(lines):
        if line.startswith(GATE):
            inside = True
        elif line.startswith(GATE_END):
            inside = False
        if inside and line.startswith("| " + entry_id + " |"):
            lines[index] = "| " + " | ".join(cells) + " |\n"
            return "".join(lines)
    raise ValueError("Entry not found in acceptance register: " + entry_id)


def check(text: str) -> None:
    blocked = [r for r in gate_rows(text) if r[1] != "Accepted"]
    if blocked:
        raise SystemExit(
            "BLOCKED: material awaiting human reading/acceptance or revision: "
            + ", ".join(r[0] + " (" + r[1] + ")" for r in blocked)
        )
    print("CLEAR: all registered AI material explicitly accepted.")


def add(args: argparse.Namespace) -> None:
    text = read_log()
    check(text)  # Do not start a new material step while a previous one is pending.
    ident = uuid4().hex[:12]
    logged_at = now()
    history_row = "| " + " | ".join(
        clean(x) for x in (
            logged_at[:10], args.tool, args.activity,
            "Reading and acceptance pending (" + ident + ")",
            "Citation/disclosure pending",
        )
    ) + " |\n"
    before, after = text.split(NEXT, 1)
    text = before.rstrip() + "\n" + history_row + "\n" + NEXT + after
    register_row = "| " + " | ".join(
        clean(x) for x in (
            ident, "Pending reading", logged_at,
            "—", "—", args.activity, "—",
        )
    ) + " |\n"
    before, after = text.split(GATE_END, 1)
    text = before.rstrip() + "\n" + register_row + "\n" + GATE_END + after
    LOG.write_text(text, encoding="utf-8")
    print("CREATED:", ident, "— stop and present this material to the student.")


def confirm(args: argparse.Namespace) -> None:
    text = read_log()
    matches = [r for r in gate_rows(text) if r[0] == args.id]
    if len(matches) != 1:
        raise SystemExit("Unknown or duplicate entry ID.")
    r = matches[0]
    if args.action == "read":
        if r[1] != "Pending reading":
            raise SystemExit("Reading already recorded or entry not awaiting reading.")
        r[1] = "Read; awaiting decision"
        r[3] = now()
        r[6] = clean(args.note or "Student explicitly confirmed reading")
    elif args.action == "accept":
        if r[1] != "Read; awaiting decision":
            raise SystemExit("Reading must be explicitly confirmed before acceptance.")
        r[1] = "Accepted"
        r[4] = now()
        r[6] = clean(args.note or "Student explicitly accepted the material")
    elif args.action == "reject":
        if r[1] != "Read; awaiting decision":
            raise SystemExit("Reading must be confirmed before requesting changes.")
        r[1] = "Revision requested"
        r[4] = now()
        r[6] = clean(args.note or "Student requested revision")
    elif args.action == "revise":
        if r[1] != "Revision requested":
            raise SystemExit("Only rejected material can be resubmitted for reading.")
        r[1] = "Pending reading"
        r[3] = "—"
        r[4] = "—"
        r[6] = clean(args.note or "Revised material submitted for renewed review")
    LOG.write_text(replace_row(text, args.id, r), encoding="utf-8")
    print(args.action.upper(), args.id, "recorded at", now())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    create = sub.add_parser("add", help="Log AI contribution and request human review")
    create.add_argument("--tool", required=True)
    create.add_argument("--activity", required=True)
    sub.add_parser("check", help="Fail if any material is awaiting acceptance")
    for action in ("read", "accept", "reject", "revise"):
        p = sub.add_parser(action)
        p.add_argument("--id", required=True, help="Existing log entry ID")
        p.add_argument("--note", default="")
    args = parser.parse_args()
    if args.action == "add":
        add(args)
    elif args.action == "check":
        check(read_log())
    else:
        # Only run after the student explicitly confirms the named decision.
        confirm(args)


if __name__ == "__main__":
    main()
