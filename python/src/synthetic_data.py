"""Generate fictional parking checks and sightings for DATA120 analysis.

The synthetic records contain no real licence plates or offender labels.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
import random
from zoneinfo import ZoneInfo

import pandas as pd

EDMONTON = ZoneInfo("America/Edmonton")


@dataclass(frozen=True)
class SyntheticConfig:
    """Configuration for a fictional lot with no more than 38 spaces."""

    days: int = 10
    capacity: int = 38
    occupancy_rate: float = 0.65
    one_check_probability: float = 0.25
    incomplete_probability: float = 0.05
    seed: int = 120
    start_date: date = date(2026, 11, 1)

    def __post_init__(self) -> None:
        if not isinstance(self.days, int) or isinstance(self.days, bool) or self.days < 1:
            raise ValueError("days must be a positive integer")
        if not isinstance(self.capacity, int) or not 1 <= self.capacity <= 38:
            raise ValueError("capacity must be between 1 and 38")
        for name in ("occupancy_rate", "one_check_probability", "incomplete_probability"):
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
        n_checks = 1 if rng.random() < config.one_check_probability else 2
        previous_vehicles: list[str] = []
        for round_number in range(n_checks):
            check_id = f"CHK_{day_index + 1:03d}_{round_number + 1}"
            at_time = time(9, 0) if round_number == 0 else time(15, 0)
            checked_at = datetime.combine(current, at_time, tzinfo=EDMONTON)
            complete = rng.random() >= config.incomplete_probability
            check_rows.append({
                "check_id": check_id, "area_id": "LOT_A",
                "check_at": checked_at, "check_complete": complete,
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
                    "observed_at": checked_at + timedelta(minutes=rng.randrange(20)),
                })

    checks = pd.DataFrame(
        check_rows, columns=["check_id", "area_id", "check_at", "check_complete"]
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
    parser.add_argument("--occupancy-rate", type=float, default=0.65)
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parents[1] / "generated"
    )
    args = parser.parse_args()
    data = generate_synthetic_data(SyntheticConfig(
        days=args.days, seed=args.seed,
        one_check_probability=args.one_check_probability,
        occupancy_rate=args.occupancy_rate,
    ))
    args.output.mkdir(parents=True, exist_ok=True)
    data.checks.to_csv(args.output / "synthetic_checks.csv", index=False)
    data.sightings.to_csv(args.output / "synthetic_sightings.csv", index=False)
    print(f"Synthetic: {len(data.checks)} checks, {len(data.sightings)} sightings")
    print(f"Written to {args.output} (generated exports are ignored by Git)")


if __name__ == "__main__":
    main()
