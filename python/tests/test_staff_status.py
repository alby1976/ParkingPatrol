"""Test fictional staff classifications separately from verified review outcomes.

Design Pattern:
    None.

Pattern Rationale:
    Direct synthetic fixtures make the validation rules easy to inspect.

Typical Usage:
    Run with pytest inside the DATA120 Python 3.13 environment.
"""

import pandas as pd
import pytest

from staff_status import normalize_staff_reports


def test_explicit_categories_do_not_create_verified_findings():
    """Accept three categorical reports without setting an enforcement status."""
    source = pd.DataFrame([
        {"vehicle_id": " SYN_0001 ", "staff_status": "Unknown",
         "reported_at": "2026-11-12T09:30:00-07:00"},
        {"vehicle_id": "SYN_0002", "staff_status": "Suspicious",
         "reported_at": "2026-11-12T09:32:00-07:00"},
        {"vehicle_id": "SYN_0003", "staff_status": "Violator",
         "reported_at": "2026-11-12T09:33:00-07:00"},
    ])
    original = source.copy(deep=True)
    result = normalize_staff_reports(source)
    assert result["staff_status"].tolist() == ["unknown", "suspicious", "violator"]
    assert result["vehicle_id"].iloc[0] == "SYN_0001"
    assert "blacklisted" not in result.columns
    assert "verified_outcome" not in result.columns
    pd.testing.assert_frame_equal(source, original)


def test_missing_or_invalid_fields_fail_closed():
    """Disallow implicit defaults, blank IDs and unsupported categories."""
    base = pd.DataFrame([{
        "vehicle_id": "SYN_0001",
        "staff_status": "Unknown",
        "reported_at": "2026-11-12T09:30:00-07:00",
    }])
    for name, value in (
        ("staff_status", None), ("staff_status", ""),
        ("staff_status", "Confirmed"), ("vehicle_id", ""),
        ("vehicle_id", "ABC123"),
        ("reported_at", "bad")
    ):
        frame = base.copy()
        frame.loc[0, name] = value
        with pytest.raises(ValueError):
            normalize_staff_reports(frame)


def test_rejects_raw_plate_columns():
    """Refuse to ingest identifiable plate fields into the Python project."""
    source = pd.DataFrame([{
        "vehicle_id": "SYN_0001",
        "staff_status": "Unknown",
        "reported_at": "2026-11-12T09:30:00-07:00",
        "Plate": "ABC123",
    }])
    with pytest.raises(ValueError, match="raw"):
        normalize_staff_reports(source)


def test_requires_explicit_timezone_offset():
    """Reject timestamp strings with no UTC offset."""
    source = pd.DataFrame([{
        "vehicle_id": "SYN_0001",
        "staff_status": "Unknown",
        "reported_at": "2026-11-12 09:30",
    }])
    with pytest.raises(ValueError):
        normalize_staff_reports(source)
