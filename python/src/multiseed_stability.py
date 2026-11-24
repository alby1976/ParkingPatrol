"""Evaluate synthetic parking observations across random seeds.

Generate reproducible synthetic observations and compare review methods
without reading private data or writing output files.

Design Pattern:
    None. This module orchestrates existing functions.

Pattern Rationale:
    Reuses the synthetic generator and detection methods without
    duplicating their implementation.

Typical Usage:
    Call evaluate_multiple_seeds() from tests or analysis scripts.
"""

from collections.abc import Sequence

import pandas as pd

from synthetic_data import SyntheticConfig, generate_synthetic_data
from pattern_detection import (
    build_vehicle_day_features,
    compare_review_methods,
)


def evaluate_multiple_seeds(seeds: Sequence[int]) -> pd.DataFrame:
    """Evaluate the three detection methods for each random seed.

    Args:
        seeds: Random seeds for reproducible synthetic experiments.

    Returns:
        One summary row per seed, preserving input order.
    """
    rows = []

    for seed in seeds:
        data = generate_synthetic_data(
            SyntheticConfig(
                days=10,
                seed=seed,
                one_check_probability=0.25,
                third_check_probability=0.25,
                complaint_probability=0.25,
                occupancy_rate=0.65,
            )
        )

        features = build_vehicle_day_features(
            data.checks,
            data.sightings,
        )
        results = compare_review_methods(features)

        rows.append(
            {
                "seed": seed,
                "checks": len(data.checks),
                "sightings": len(data.sightings),
                "vehicle_days": len(results),
                "rule_flags": int(results["rule_suspicious"].sum()),
                "if_flags": int(results["anomaly_suspicious"].sum()),

                "lof_flags": int(results["lof_suspicious"].sum()),
                "lof_scored": int(
                    (results["lof_status"] == "scored").sum()
                ),
                "lof_status": (
                    results["lof_status"].iloc[0]
                    if results["lof_status"].nunique() == 1
                    else "mixed"
                ),
            }
        )

    return pd.DataFrame(rows)
