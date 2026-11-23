"""Synthetic fixture tests, without production or identifiable parking data."""
from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from synthetic_data import SyntheticConfig, generate_synthetic_data


def test_reproducible_for_same_seed():
    config = SyntheticConfig(days=10, seed=120)
    first = generate_synthetic_data(config)
    second = generate_synthetic_data(config)
    pd.testing.assert_frame_equal(first.checks, second.checks)
    pd.testing.assert_frame_equal(first.sightings, second.sightings)


def test_capacity_and_one_or_two_checks_each_day():
    result = generate_synthetic_data(SyntheticConfig(days=35, capacity=38, seed=19))
    assert len(result.checks["check_at"].dt.date.unique()) == 35
    assert result.checks.groupby(result.checks["check_at"].dt.date).size().between(1, 2).all()
    counts = result.sightings.groupby("check_id").size()
    assert counts.le(38).all()
    assert result.checks["check_id"].is_unique


def test_schema_and_edmonton_times_and_join_keys():
    output = generate_synthetic_data(SyntheticConfig(days=10))
    assert list(output.checks.columns) == ["check_id", "area_id", "check_at", "check_complete"]
    assert list(output.sightings.columns) == ["vehicle_id", "check_id", "area_id", "observed_at"]
    assert str(output.checks["check_at"].dt.tz) == "America/Edmonton"
    assert str(output.sightings["observed_at"].dt.tz) == "America/Edmonton"
    assert set(output.sightings["check_id"]).issubset(set(output.checks["check_id"]))
    assert output.sightings["vehicle_id"].str.fullmatch(r"SYN_\d{4}").all()
    assert not output.sightings.duplicated(["vehicle_id", "check_id", "area_id"]).any()


def test_empty_completed_checks_are_retained():
    result = generate_synthetic_data(SyntheticConfig(
        days=14, capacity=8, occupancy_rate=0, incomplete_probability=0, seed=7))
    assert len(result.sightings) == 0
    assert len(result.checks) >= 14
    assert result.checks["check_complete"].all()


def test_recurring_vehicles_and_same_day_repeat_events_exist():
    result = generate_synthetic_data(SyntheticConfig(
        days=30, capacity=38, occupancy_rate=0.8, seed=7))
    join = result.sightings.merge(result.checks[["check_id", "check_at"]], on="check_id")
    perday = join.groupby(["vehicle_id", join["check_at"].dt.date])["check_id"].nunique()
    assert perday.ge(2).any()
    distinct_days = join.groupby("vehicle_id")["check_at"].apply(lambda s: s.dt.date.nunique())
    assert distinct_days.ge(3).any()


def test_invalid_configuration_is_rejected():
    for kwargs in ({"days": 0}, {"capacity": 0}, {"capacity": 39},
                   {"occupancy_rate": -0.1}, {"occupancy_rate": 1.1},
                   {"one_check_probability": -0.2}, {"incomplete_probability": 2}):
        with pytest.raises(ValueError):
            SyntheticConfig(**kwargs)
