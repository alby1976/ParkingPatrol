
"""Regression tests for the AI-use logging utility."""

from pathlib import Path

import log_ai_use


def test_logger_recognizes_current_log_headings(tmp_path, monkeypatch):
    """The logger must recognize the current AI-use log format."""
    log_content = (
        "## Assistance history\n\n"
        "## Copy this row for each future use\n\n"
        "## AI material reading and acceptance register\n\n"
        "## Project-specific GAI disclosure wording - "
        "verify instructor permission before submission\n"
    )

    log_file = tmp_path / "AI_USE_LOG.md"
    log_file.write_text(log_content, encoding="utf-8")

    monkeypatch.setattr(log_ai_use, "LOG", log_file)

    assert log_ai_use.read_log() == log_content


def test_new_history_entry_stays_inside_table(tmp_path, monkeypatch):
    """Insert new assistance entries inside the history table."""
    from types import SimpleNamespace

    content = (
        "## Assistance history\n\n"
        "| Date | Tool | Task | Review | Citation |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| 2026-11-24 | Existing | Old task | Accepted | Ref |\n\n"
        "## Proposed APA-style citations\n\n"
        "Citation information.\n\n"
        "## Copy this row for each future use\n\n"
        "## AI material reading and acceptance register\n\n"
        "## Project-specific GAI disclosure wording\n"
    )

    path = tmp_path / "AI_USE_LOG.md"
    path.write_text(content, encoding="utf-8")
    monkeypatch.setattr(log_ai_use, "LOG", path)

    log_ai_use.add(
        SimpleNamespace(tool="Test AI", activity="New task")
    )

    updated = path.read_text(encoding="utf-8")
    history = updated.split(
        "## Proposed APA-style citations", 1
    )[0]

    assert "| Test AI | New task |" in history

    # The activity must not appear as a stray row in the
    # citation and reference section.
    citation_section = updated.split(
        "## Proposed APA-style citations", 1
    )[1].split(
        "## AI material reading and acceptance register", 1
    )[0]

    assert "| Test AI | New task |" not in citation_section

    # The matching acceptance-register entry must still exist.
    register = updated.split(
        "## AI material reading and acceptance register", 1
    )[1]

    assert "New task" in register


def test_read_and_accept_update_both_tables(tmp_path, monkeypatch):
    """Reading and acceptance must update both log tables."""
    from types import SimpleNamespace

    entry_id = "test123"
    activity = "S20 test activity"

    content = (
        "## Assistance history\n\n"
        "| Date | Tool | Task | Review | Citation |\n"
        "| --- | --- | --- | --- | --- |\n"
        f"| 2026-11-24 | Test AI | {activity} | "
        f"Reading and acceptance pending ({entry_id}) | Pending |\n\n"
        "## Proposed APA-style citations\n\n"
        "## Copy this row for each future use\n\n"
        "## AI material reading and acceptance register\n\n"
        "| Entry ID | Status | Logged at | Read confirmed at | "
        "Decision at | Material / scope | Student response |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
        f"| {entry_id} | Pending reading | 2026-11-24 | - | - | "
        f"{activity} | - |\n\n"
        "## Project-specific GAI disclosure wording\n"
    )

    path = tmp_path / "AI_USE_LOG.md"
    path.write_text(content, encoding="utf-8")
    monkeypatch.setattr(log_ai_use, "LOG", path)

    log_ai_use.confirm(
        SimpleNamespace(
            action="read",
            id=entry_id,
            note="Student confirmed reading",
        )
    )

    after_read = path.read_text(encoding="utf-8")
    history = after_read.split(
        "## Proposed APA-style citations", 1
    )[0]

    assert f"Reading confirmed; awaiting acceptance ({entry_id})" in history

    log_ai_use.confirm(
        SimpleNamespace(
            action="accept",
            id=entry_id,
            note="Student accepted changes",
        )
    )

    after_accept = path.read_text(encoding="utf-8")
    history = after_accept.split(
        "## Proposed APA-style citations", 1
    )[0]

    assert f"Reading and acceptance confirmed ({entry_id})" in history
    assert f"Reading and acceptance pending ({entry_id})" not in history
    assert f"| {entry_id} | Accepted |" in after_accept


def test_new_ai_log_records_use_ascii(tmp_path, monkeypatch):
    """New AI-use records must contain ASCII-only characters."""
    from types import SimpleNamespace

    content = (
        "## Assistance history\n\n"
        "| Date | Tool | Task | Review | Citation |\n"
        "| --- | --- | --- | --- | --- |\n"
        "## Proposed APA-style citations\n\n"
        "## Copy this row for each future use\n\n"
        "## AI material reading and acceptance register\n\n"
        "| Entry ID | Status | Logged at | Read confirmed at | "
        "Decision at | Material / scope | Student response |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
        "## Project-specific GAI disclosure wording\n"
    )

    path = tmp_path / "AI_USE_LOG.md"
    path.write_text(content, encoding="utf-8")
    monkeypatch.setattr(log_ai_use, "LOG", path)

    log_ai_use.add(
        SimpleNamespace(tool="Test AI", activity="ASCII test")
    )

    result = path.read_text(encoding="utf-8")

    assert result.isascii()
    assert "Pending" in result
