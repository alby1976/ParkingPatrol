#!/usr/bin/env python3
"""Append a transparent, non-sensitive DATA120 AI-use entry to AI_USE_LOG.md."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

LOG_PATH = Path(__file__).resolve().parent / "AI_USE_LOG.md"
HEADER = "## Assistance history"
NEXT_HEADER = "## Copy this row for each future use"


def cell(value: str) -> str:
    """Safely put plain text into a Markdown table cell."""
    return " ".join(value.replace("|", "\\|").split()).strip()


def add_entry(tool: str, activity: str, verification: str, citation: str) -> None:
    """Append an AI-use row without deleting previous entries."""
    if not tool.strip() or not activity.strip():
        raise ValueError("Tool and activity must not be empty.")
    original = LOG_PATH.read_text(encoding="utf-8")
    if HEADER not in original or NEXT_HEADER not in original:
        raise ValueError("Log layout was modified; manual review required.")
    today = datetime.now(ZoneInfo("America/Edmonton")).date().isoformat()
    row = "| " + " | ".join(
        cell(field) for field in (today, tool, activity, verification, citation)
    ) + " |\n"
    before, after = original.split(NEXT_HEADER, maxsplit=1)
    LOG_PATH.write_text(
        before.rstrip() + "\n" + row + "\n" + NEXT_HEADER + after,
        encoding="utf-8",
    )


def main() -> None:
    """Run the append-only logger with explicitly supplied disclosure details."""
    parser = argparse.ArgumentParser(
        description="Record an AI-assisted DATA120 task in python/AI_USE_LOG.md."
    )
    parser.add_argument("--tool", required=True, help="AI tool and model, if known")
    parser.add_argument("--activity", required=True, help="What AI actually assisted with")
    parser.add_argument(
        "--verification",
        default="Student verification pending",
        help="Actual student review, or pending status",
    )
    parser.add_argument(
        "--citation", default="Citation/disclosure pending",
        help="Submission citation or appendix reference, if known",
    )
    args = parser.parse_args()
    add_entry(args.tool, args.activity, args.verification, args.citation)
    print("Added a new entry to python/AI_USE_LOG.md; review before publishing.")


if __name__ == "__main__":
    main()
