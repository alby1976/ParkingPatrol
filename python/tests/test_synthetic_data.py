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
                   {"one_check_probability": -0.2}, {"incomplete_probability": 2},
                   {"third_check_probability": -0.1}, {"third_check_probability": 1.5}):
        with pytest.raises(ValueError):
            SyntheticConfig(**kwargs)


def test_realistic_first_inspection_is_complete():
    """Require the first performed round to match clinic practice."""
    config = SyntheticConfig(days=10, seed=120)
    result = generate_synthetic_data(config)

    checks = result.checks.copy()
    checks["day"] = checks["check_at"].dt.date

    # Every performed inspection must be complete.
    assert checks["check_complete"].all()

    # Find the first inspection of each day.
    first_checks = (
        checks.sort_values("check_at")
        .groupby("day")
        .first()
    )

    # The first round must occur between 10:15 and 10:30.
    for checked_at in first_checks["check_at"]:
        minutes = checked_at.hour * 60 + checked_at.minute

        assert 10 * 60 + 15 <= minutes <= 10 * 60 + 30


def test_three_completed_inspections_can_be_generated():
    """Support three completed inspections on a simulated day."""
    config = SyntheticConfig(
        days=5,
        seed=120,
        one_check_probability=0.0,
        third_check_probability=1.0,
    )

    result = generate_synthetic_data(config)
    checks = result.checks.copy()
    checks["day"] = checks["check_at"].dt.date

    counts = checks.groupby("day").size()

    assert counts.eq(3).all()
    assert checks["check_complete"].all()

    for day, group in checks.groupby("day"):
        times = sorted(
            timestamp.strftime("%H:%M")
            for timestamp in group["check_at"]
        )

        assert "12:30" in times
        assert "15:30" in times


def test_third_inspection_can_occur_without_second():
    """Allow an afternoon round when the midday round is skipped."""
    config = SyntheticConfig(
        days=5,
        seed=120,
        one_check_probability=1.0,
        third_check_probability=1.0,
    )

    result = generate_synthetic_data(config)
    checks = result.checks.copy()
    checks["day"] = checks["check_at"].dt.date

    for _, group in checks.groupby("day"):
        times = sorted(
            timestamp.strftime("%H:%M")
            for timestamp in group["check_at"]
        )

        assert len(times) == 2
        assert "12:30" not in times
        assert "15:30" in times
        assert checks.loc[group.index, "check_complete"].all()


def test_cli_supports_optional_third_inspection(tmp_path, monkeypatch):
    """Allow the CLI to generate three completed rounds per day."""
    from synthetic_data import main

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "synthetic_data.py",
            "--days", "2",
            "--seed", "120",
            "--one-check-probability", "0",
            "--third-check-probability", "1",
            "--output", str(tmp_path),
        ],
    )

    main()

    checks = pd.read_csv(tmp_path / "synthetic_checks.csv")

    assert len(checks) == 6
    assert checks["check_complete"].all()
