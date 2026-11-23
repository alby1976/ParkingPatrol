"""Synthetic fixture tests, without production or identifiable parking data."""
from datetime import time
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

    assert list(output.checks.columns) == [
        "check_id",
        "area_id",
        "check_at",
        "check_complete",
        "duration_minutes",
        "inspection_reason",
        "complaint_at",
    ]
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


def test_vehicle_observations_within_thirty_minutes():
    """Vehicle observations occur within 30 minutes of inspection start."""
    config = SyntheticConfig(days=10, seed=120)
    result = generate_synthetic_data(config)

    sightings = result.sightings.merge(
        result.checks[["check_id", "check_at"]],
        on="check_id",
        validate="many_to_one",
    )

    elapsed = sightings["observed_at"] - sightings["check_at"]

    assert (elapsed >= pd.Timedelta(0)).all()
    assert (elapsed <= pd.Timedelta(minutes=30)).all()

    # The generator must record each inspection's duration.
    assert "duration_minutes" in result.checks.columns

    durations = result.checks["duration_minutes"]

    assert durations.between(1, 30).all()
    assert 12 <= durations.mean() <= 18

    # No vehicle observation may occur after its inspection finishes.
    sightings = result.sightings.merge(
        result.checks[["check_id", "check_at", "duration_minutes"]],
        on="check_id",
        validate="many_to_one",
    )

    elapsed = (
        sightings["observed_at"] - sightings["check_at"]
    ).dt.total_seconds() / 60

    assert (elapsed <= sightings["duration_minutes"]).all()


def test_occasional_long_inspections():
    """Long inspections can occur without exceeding 30 minutes."""
    config = SyntheticConfig(
        days=365,
        seed=120,
    )

    result = generate_synthetic_data(config)
    durations = result.checks["duration_minutes"]

    assert durations.between(1, 30).all()
    assert 12 <= durations.mean() <= 18

    # Some inspections should take longer than 20 minutes.
    assert (durations > 20).any()


def test_customer_complaint_always_triggers_inspection():
    """Every simulated complaint creates one additional complete inspection."""
    config = SyntheticConfig(
        days=5,
        seed=120,
        one_check_probability=1.0,
        third_check_probability=0.0,
        complaint_probability=1.0,
    )

    result = generate_synthetic_data(config)
    checks = result.checks.copy()
    checks["day"] = checks["check_at"].dt.date

    # One morning inspection plus one complaint inspection daily.
    assert checks.groupby("day").size().eq(2).all()

    assert "inspection_reason" in checks.columns

    for _, group in checks.groupby("day"):
        assert set(group["inspection_reason"]) == {
            "routine",
            "customer_complaint",
        }
        assert group["check_complete"].all()


def test_complaint_inspections_occur_at_variable_times():
    """Every complaint is recorded, including those handled by routine rounds."""
    config = SyntheticConfig(
        days=30,
        seed=120,
        one_check_probability=1.0,
        third_check_probability=0.0,
        complaint_probability=1.0,
    )

    result = generate_synthetic_data(config)
    checks = result.checks.copy()

    # Exactly one simulated complaint occurs on each of 30 days.
    complaints = checks.loc[checks["complaint_at"].notna()].copy()

    assert len(complaints) == 30

    # Complaint times should vary, not always be 2:00 PM.
    times = complaints["complaint_at"].dt.strftime("%H:%M")
    assert times.nunique() > 1

    # Provisional simulation window: 9:00 AM through 4:59 PM.
    assert complaints["complaint_at"].dt.hour.between(9, 16).all()

    # Every complaint must be associated with a completed inspection.
    assert complaints["check_complete"].all()


def test_inspection_rounds_do_not_overlap():
    """An inspection must finish before the next one starts."""
    config = SyntheticConfig(
        days=365,
        seed=120,
        one_check_probability=0.0,
        third_check_probability=1.0,
        complaint_probability=1.0,
    )

    result = generate_synthetic_data(config)
    checks = result.checks.copy()
    checks["day"] = checks["check_at"].dt.date

    for _, group in checks.groupby("day"):
        group = group.sort_values("check_at")

        finish_times = (
            group["check_at"]
            + pd.to_timedelta(group["duration_minutes"], unit="m")
        )

        next_starts = group["check_at"].shift(-1)

        # Every inspection must finish before the next begins.
        assert (
            finish_times.iloc[:-1].to_numpy()
            <= next_starts.iloc[:-1].to_numpy()
        ).all()



def test_complaint_during_active_inspection_reuses_that_inspection():
    """A complaint during an inspection reuses that inspection."""
    from synthetic_data import find_active_inspection

    start = pd.Timestamp("2026-11-09 10:15", tz="America/Edmonton")

    checks = [
        {
            "check_id": "CHK_001_1",
            "check_at": start,
            "duration_minutes": 20,
            "inspection_reason": "routine",
        }
    ]

    # Customer complains 10 minutes into the inspection.
    complaint_at = start + pd.Timedelta(minutes=10)

    existing = find_active_inspection(checks, complaint_at)

    # Use the current inspection; do not require another.
    assert existing is checks[0]
    assert existing["inspection_reason"] == "routine"

    # A complaint after the inspection ends has no active round.
    later_complaint = start + pd.Timedelta(minutes=25)
    assert find_active_inspection(checks, later_complaint) is None


def test_generator_reuses_active_inspection_for_complaint(monkeypatch):
    """A complaint during a morning inspection creates no extra round."""
    import synthetic_data

    # Force the morning inspection to start at 10:15 AM.
    monkeypatch.setattr(
        synthetic_data,
        "generate_morning_time",
        lambda rng: time(10, 15),
        raising=False,
    )

    # Force the customer complaint to occur at 10:20 AM.
    monkeypatch.setattr(
        synthetic_data,
        "generate_complaint_time",
        lambda rng: time(10, 20),
        raising=False,
    )

    config = SyntheticConfig(
        days=1,
        seed=120,
        one_check_probability=1.0,
        third_check_probability=0.0,
        complaint_probability=1.0,
    )

    result = generate_synthetic_data(config)
    checks = result.checks

    # The morning inspection should satisfy the complaint.
    assert len(checks) == 1
    assert checks.iloc[0]["inspection_reason"] == "routine"

    # The complaint time must be retained separately.
    assert "complaint_at" in checks.columns
    assert pd.notna(checks.iloc[0]["complaint_at"])


def test_delayed_complaint_preserves_original_timestamp(monkeypatch):
    """A complaint received before an inspection retains its original time."""
    import synthetic_data

    # Complaint occurs five minutes before the midday routine inspection.
    monkeypatch.setattr(
        synthetic_data,
        "generate_complaint_time",
        lambda rng: time(12, 25),
    )

    config = SyntheticConfig(
        days=1,
        seed=120,
        one_check_probability=0.0,
        third_check_probability=0.0,
        complaint_probability=1.0,
    )

    result = generate_synthetic_data(config)

    complaints = result.checks.loc[
        result.checks["complaint_at"].notna()
    ]

    assert len(complaints) == 1

    complaint = complaints.iloc[0]

    # Preserve the actual customer complaint time.
    assert complaint["complaint_at"].strftime("%H:%M") == "12:25"

    # An inspection must not begin before the complaint occurs.
    assert complaint["check_at"] >= complaint["complaint_at"]

    # The complaint should be satisfied by an inspection that starts
    # at or after 12:25, without fabricating another complaint.
    assert complaint["check_complete"]


def test_complaint_before_routine_inspection_starts_promptly(monkeypatch):
    """A complaint outside an active round starts an inspection promptly."""
    import synthetic_data

    monkeypatch.setattr(
        synthetic_data,
        "generate_complaint_time",
        lambda rng: time(12, 25),
    )

    config = SyntheticConfig(
        days=1,
        seed=120,
        one_check_probability=0.0,
        third_check_probability=0.0,
        complaint_probability=1.0,
    )

    result = generate_synthetic_data(config)
    checks = result.checks.sort_values("check_at")

    complaints = checks.loc[
        checks["inspection_reason"] == "customer_complaint"
    ]

    assert len(complaints) == 1

    complaint = complaints.iloc[0]

    assert complaint["complaint_at"].strftime("%H:%M") == "12:25"
    assert complaint["check_at"].strftime("%H:%M") == "12:25"

    # Both the complaint and the routine inspection remain represented.
    assert len(checks) == 3

    # Inspections must not overlap.
    finish_times = (
        checks["check_at"]
        + pd.to_timedelta(checks["duration_minutes"], unit="m")
    )
    next_starts = checks["check_at"].shift(-1)

    assert (
        finish_times.iloc[:-1].to_numpy()
        <= next_starts.iloc[:-1].to_numpy()
    ).all()


def test_reused_complaint_does_not_skip_inspection_ids(monkeypatch):
    """Reusing an inspection must not create gaps in check IDs."""
    import synthetic_data

    monkeypatch.setattr(
        synthetic_data,
        "generate_morning_time",
        lambda rng: time(10, 15),
    )

    monkeypatch.setattr(
        synthetic_data,
        "generate_complaint_time",
        lambda rng: time(10, 20),
    )

    config = SyntheticConfig(
        days=1,
        seed=120,
        one_check_probability=0.0,
        third_check_probability=0.0,
        complaint_probability=1.0,
    )

    result = generate_synthetic_data(config)

    checks = result.checks.sort_values("check_at")

    assert len(checks) == 2

    assert checks["check_id"].tolist() == [
        "CHK_001_1",
        "CHK_001_2",
    ]

    assert checks["check_id"].is_unique


def test_cli_supports_complaint_probability(tmp_path, monkeypatch):
    """Allow complaint frequency to be configured through the CLI."""
    from synthetic_data import main

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "synthetic_data.py",
            "--days", "2",
            "--seed", "120",
            "--one-check-probability", "1",
            "--third-check-probability", "0",
            "--complaint-probability", "1",
            "--output", str(tmp_path),
        ],
    )

    main()

    checks = pd.read_csv(tmp_path / "synthetic_checks.csv")

    assert "complaint_at" in checks.columns
    assert checks["complaint_at"].notna().sum() == 2
