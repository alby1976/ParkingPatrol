"""Generate fictional parking checks and sightings for DATA120 analysis.

The synthetic records contain no real licence plates or offender labels.
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

EDMONTON = ZoneInfo("America/Edmonton")


def generate_morning_time(rng: random.Random) -> time:
    """Generate the start time of the morning inspection."""
    return time(10, rng.randint(15, 30))


def generate_complaint_time(rng: random.Random) -> time:
    """Generate a simulated customer complaint time."""
    return time(
        hour=rng.randint(9, 16),
        minute=rng.randint(0, 59),
    )


def find_active_inspection(
        checks: list[dict],
        complaint_at: datetime,
) -> dict | None:
    """Find an inspection underway when a customer complains.

    Args:
        checks: Inspection records containing check_at and duration_minutes.
        complaint_at: Time the customer complained.

    Returns:
        The active inspection record, or None if no inspection is active.
    """
    for check in checks:
        started_at = check["check_at"]
        finished_at = started_at + timedelta(
            minutes=check["duration_minutes"]
        )

        if started_at <= complaint_at < finished_at:
            return check

    return None


@dataclass(frozen=True)
class SyntheticConfig:
    """Configuration for a fictional lot with no more than 38 spaces."""

    days: int = 10
    capacity: int = 38
    occupancy_rate: float = 0.65
    one_check_probability: float = 0.25
    third_check_probability: float = 0.0
    complaint_probability: float = 0.0
    # Every performed inspection is complete under normal clinic practice.
    # A skipped inspection is not recorded as an incomplete inspection.
    incomplete_probability: float = 0.0
    seed: int = 120
    start_date: date = date(2026, 11, 1)

    def __post_init__(self) -> None:
        if not isinstance(self.days, int) or isinstance(self.days, bool) or self.days < 1:
            raise ValueError("days must be a positive integer")
        if not isinstance(self.capacity, int) or not 1 <= self.capacity <= 38:
            raise ValueError("capacity must be between 1 and 38")
        for name in (
                "occupancy_rate",
                "one_check_probability",
                "third_check_probability",
                "complaint_probability",
                "incomplete_probability"
        ):
            value = getattr(self, name)
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must be between zero and one")
        if not isinstance(self.start_date, date) or isinstance(self.start_date, datetime):
            raise ValueError("start_date must be a date")


@dataclass(frozen=True)
class SyntheticData:
    """Synthetic check and sighting tables in the normalized schema."""

    checks: pd.DataFrame
    sightings: pd.DataFrame


def generate_synthetic_data(config: SyntheticConfig = SyntheticConfig()) -> SyntheticData:
    """Produce reproducible fictional observation records, not violation labels.

    Args:
        config: User-selected generation parameters and random seed.

    Returns:
        SyntheticData with separate checks (including empty checks) and
        pseudonymous sightings with timezone-aware Edmonton timestamps.
    """
    rng = random.Random(config.seed)
    regular_pool = [f"SYN_{i:04d}" for i in range(1, max(9, config.capacity // 2) + 1)]
    casual_pool = [f"SYN_{i:04d}" for i in range(100, 100 + config.capacity * 8)]
    check_rows: list[dict] = []
    sight_rows: list[dict] = []
    for day_index in range(config.days):
        current = config.start_date + timedelta(days=day_index)
        # First inspection always takes place.
        round_times = [(generate_morning_time(rng), "routine")]

        # Second inspection may be skipped because of workload.
        if rng.random() >= config.one_check_probability:
            round_times.append((time(12, 30), "routine"))

        # Third inspection is optional and independent of the second.
        if rng.random() < config.third_check_probability:
            round_times.append((time(15, 30), "routine"))

        # Every simulated complaint triggers an additional inspection.
        if rng.random() < config.complaint_probability:
            complaint_time = generate_complaint_time(rng)
            round_times.append((complaint_time, "customer_complaint"))

        round_times.sort(key=lambda item: item[0])

        previous_vehicles: list[str] = []
        previous_end: datetime | None = None

        for at_time, inspection_reason in round_times:
            checked_at = datetime.combine(current, at_time, tzinfo=EDMONTON)

            # A complaint during an active inspection is handled by that round.
            if inspection_reason == "customer_complaint":
                active_check = find_active_inspection(check_rows, checked_at)

                if active_check is not None:
                    active_check["complaint_at"] = checked_at
                    continue

            round_number = sum(
                check["check_at"].date() == current
                for check in check_rows
            )
            check_id = f"CHK_{day_index + 1:03d}_{round_number + 1}"

            # Do not start another inspection while one is still underway.
            if previous_end is not None and checked_at < previous_end:
                checked_at = previous_end

            complete = rng.random() >= config.incomplete_probability

            # Most inspections take around 15 minutes.
            # Occasionally, a full inspection takes up to 30 minutes.
            # The 10% long-inspection rate is a simulation assumption.
            if rng.random() < 0.10:
                duration_minutes = rng.randint(21, 30)
            else:
                duration_minutes = rng.randint(10, 20)
            # Remember when this inspection finishes.
            previous_end = checked_at + timedelta(minutes=duration_minutes)

            check_rows.append({
                "check_id": check_id,
                "area_id": "LOT_A",
                "check_at": checked_at,
                "check_complete": complete,
                "duration_minutes": duration_minutes,
                "inspection_reason": inspection_reason,
                "complaint_at": (
                    checked_at if inspection_reason == "customer_complaint" else None
                ),
            })

            spots_seen = sum(
                rng.random() < config.occupancy_rate for _ in range(config.capacity)
            )
            if spots_seen == 0:
                previous_vehicles = []
                continue
            carry = []
            if round_number > 0:
                carry = [v for v in previous_vehicles if rng.random() < 0.62]
                carry = carry[:spots_seen]
            remaining = spots_seen - len(carry)
            regular_candidates = [v for v in regular_pool if v not in carry]
            casual_candidates = [v for v in casual_pool if v not in carry]
            regular_count = min(len(regular_candidates), remaining // 3)
            vehicles = (
                    carry
                    + rng.sample(regular_candidates, regular_count)
                    + rng.sample(casual_candidates, remaining - regular_count)
            )
            rng.shuffle(vehicles)
            previous_vehicles = vehicles
            for vehicle in vehicles:
                sight_rows.append({
                    "vehicle_id": vehicle, "check_id": check_id,
                    "area_id": "LOT_A",
                    "observed_at": checked_at + timedelta(
                        minutes=rng.randint(0, duration_minutes)
                    ),
                })

    checks = pd.DataFrame(
        check_rows,
        columns=[
            "check_id",
            "area_id",
            "check_at",
            "check_complete",
            "duration_minutes",
            "inspection_reason",
            "complaint_at",
        ],
    )
    sightings = pd.DataFrame(
        sight_rows, columns=["vehicle_id", "check_id", "area_id", "observed_at"]
    )
    checks["check_at"] = pd.to_datetime(checks["check_at"])
    if not sightings.empty:
        sightings["observed_at"] = pd.to_datetime(sightings["observed_at"])
    else:
        sightings["observed_at"] = pd.Series([], dtype=checks["check_at"].dtype)
    return SyntheticData(checks, sightings)


def main() -> None:
    """Export fictional CSVs to an ignored, local-only generated folder."""
    parser = argparse.ArgumentParser(description="Generate synthetic parking observations")
    parser.add_argument("--days", type=int, default=10)
    parser.add_argument("--seed", type=int, default=120)
    parser.add_argument("--one-check-probability", type=float, default=0.25)
    parser.add_argument(
        "--third-check-probability",
        type=float,
        default=0.0,
        help="Probability of an optional 3:30 PM inspection",
    )

    parser.add_argument(
        "--complaint-probability",
        type=float,
        default=0.0,
        help="Probability of one customer complaint per simulated day",
    )
    parser.add_argument("--occupancy-rate", type=float, default=0.65)
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parents[1] / "generated"
    )
    args = parser.parse_args()
    data = generate_synthetic_data(SyntheticConfig(
        days=args.days,
        seed=args.seed,
        one_check_probability=args.one_check_probability,
        third_check_probability=args.third_check_probability,
        complaint_probability=args.complaint_probability,
        occupancy_rate=args.occupancy_rate,
    ))
    args.output.mkdir(parents=True, exist_ok=True)
    data.checks.to_csv(args.output / "synthetic_checks.csv", index=False)
    data.sightings.to_csv(args.output / "synthetic_sightings.csv", index=False)
    print(f"Synthetic: {len(data.checks)} checks, {len(data.sightings)} sightings")
    print(f"Written to {args.output} (generated exports are ignored by Git)")


if __name__ == "__main__":
    main()
