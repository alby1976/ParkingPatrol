"""Synthetic tests only: no licence plates, production exports, or Google APIs."""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cleaning import normalize_observations  # noqa: E402


def sample_checks():
    return pd.DataFrame([
        {"check_id": " round 1 ", "area_id": " east ", "check_at": "2026-01-15 09:30",
         "check_complete": "yes"},
        {"check_id": "round 2", "area_id": "east", "check_at": "2026-01-16 09:30",
         "check_complete": "no"},
        {"check_id": "round 3", "area_id": "east", "check_at": "2026-01-17 09:30",
         "check_complete": "yes"},
    ])


def sample_sightings():
    return pd.DataFrame([
        {"vehicle_id": " demo_001 ", "check_id": "round 1", "area_id": "EAST",
         "observed_at": "2026-01-15T09:31:00-07:00"},
        {"vehicle_id": "DEMO_001", "check_id": "ROUND 1", "area_id": "east",
         "observed_at": "2026-01-15 09:31"},
        {"vehicle_id": "demo_002", "check_id": "round 2", "area_id": "east",
         "observed_at": "2026-01-16 09:32"},
    ])


def test_normalizes_deduplicates_and_preserves_incomplete_and_empty_checks():
    result = normalize_observations(sample_checks(), sample_sightings())
    assert len(result.checks) == 3
    assert len(result.sightings) == 2
    assert result.sightings.iloc[0]["vehicle_id"] == "DEMO_001"
    assert result.checks["check_complete"].tolist() == [True, False, True]
    assert "duplicate_vehicle_in_check" in result.issues["issue"].tolist()
    assert str(result.sightings.iloc[0]["observed_at"].tzinfo) == "America/Edmonton"


def test_unknown_checks_are_quarantined_without_exposing_values():
    sightings = sample_sightings()
    sightings.loc[0, "check_id"] = "unknown"
    result = normalize_observations(sample_checks(), sightings)
    assert "unknown_or_invalid_check" in result.issues["issue"].tolist()
    assert "unknown" not in result.issues.to_string().lower()


def test_conflicting_duplicate_check_quarantines_corresponding_sightings():
    checks = pd.concat([sample_checks(), sample_checks().iloc[[0]]], ignore_index=True)
    checks.loc[3, "check_at"] = "2026-01-15 10:00"
    result = normalize_observations(checks, sample_sightings())
    assert "ROUND 1" not in result.checks["check_id"].tolist()
    assert "conflicting_duplicate_check" in result.issues["issue"].tolist()
    assert "unknown_or_invalid_check" in result.issues["issue"].tolist()


def test_ambiguous_local_dst_time_rejected():
    checks = sample_checks()
    checks.loc[0, "check_at"] = "2026-11-01 01:30"
    result = normalize_observations(checks, sample_sightings())
    assert "ROUND 1" not in result.checks["check_id"].tolist()
    assert "missing_or_invalid_required_field" in result.issues["issue"].tolist()


def test_prohibits_raw_plate_fields():
    sightings = sample_sightings()
    sightings["license_plate"] = ["", "", ""]
    with pytest.raises(ValueError, match="Raw identifiers"):
        normalize_observations(sample_checks(), sightings)


def test_input_dataframes_not_modified():
    checks = sample_checks()
    sightings = sample_sightings()
    checks_original = checks.copy(deep=True)
    sightings_original = sightings.copy(deep=True)
    normalize_observations(checks, sightings)
    pd.testing.assert_frame_equal(checks, checks_original)
    pd.testing.assert_frame_equal(sightings, sightings_original)
