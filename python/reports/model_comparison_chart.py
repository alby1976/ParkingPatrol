
"""Generate a reproducible ParkingPatrol synthetic model comparison chart.

The chart compares the two-check rule, Isolation Forest, and LOF.
Unscored models are shown separately from models finding no anomalies.

Usage:
    python reports/model_comparison_chart.py
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from pattern_detection import (
    build_vehicle_day_features,
    compare_review_methods,
)


def load_synthetic_features() -> pd.DataFrame:
    """Load fictional observations and build vehicle-day features.

    Returns:
        DataFrame containing pseudonymous vehicle-day features.

    Raises:
        FileNotFoundError: If a synthetic CSV file is missing.
    """
    generated_dir = Path(__file__).resolve().parents[1] / "generated"

    checks = pd.read_csv(generated_dir / "synthetic_checks.csv")
    sightings = pd.read_csv(generated_dir / "synthetic_sightings.csv")

    return build_vehicle_day_features(checks, sightings)


def summarize_comparison(features: pd.DataFrame) -> dict[str, object]:
    """Summarize the three review methods using fictional observations.

    Args:
        features: Pseudonymous vehicle-day feature records.

    Returns:
        Counts for the rule and Isolation Forest, plus the LOF status.
    """
    results = compare_review_methods(features)

    lof_scored = results["lof_status"].eq("scored")

    return {
        "total_rows": len(results),
        "rule_flags": int(results["rule_suspicious"].sum()),
        "isolation_forest_flags": int(
            results["anomaly_suspicious"].sum()
        ),
        "lof_scored_rows": int(lof_scored.sum()),
        "lof_flags": int(
            (results["lof_suspicious"] & lof_scored).sum()
        ),
        "lof_status_counts": results["lof_status"].value_counts().to_dict(),
    }


def create_comparison_chart(summary: dict[str, object]) -> Path:
    """Create a chart comparing review signals on synthetic data.

    Args:
        summary: Results returned by summarize_comparison().

    Returns:
        Path to the saved PNG chart.
    """
    total = int(summary["total_rows"])
    scored = int(summary["lof_scored_rows"])

    methods = ["Two-check rule", "Isolation Forest", "LOF"]
    counts = [
        int(summary["rule_flags"]),
        int(summary["isolation_forest_flags"]),
        int(summary["lof_flags"]),
    ]

    fig, ax = plt.subplots(figsize=(10, 5.5))

    bars = ax.bar(methods, counts, color=["#4472C4", "#70AD47", "#A5A5A5"])

    for index, bar in enumerate(bars):
        height = bar.get_height()

        if index == 2 and scored != total:
            label = (
                "Not scored"
                if scored == 0
                else f"Partially scored ({scored}/{total})"
            )
        else:
            label = str(counts[index])

        ax.annotate(
            label,
            (bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=11,
        )

    if scored != total:
        bars[2].set_alpha(0.25)

    ax.set_ylim(0, max(counts + [1]) * 1.2)
    ax.set_ylabel("Flagged vehicle-day observations")
    ax.set_title("ParkingPatrol: Synthetic-data method comparison")
    ax.text(
        0.5,
        -0.19,
        f"Synthetic data only | {total} vehicle-day rows | "
        "Flags require human review",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
    )

    fig.tight_layout()

    output_path = Path(__file__).resolve().parent / "model_comparison.png"
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    return output_path


def main() -> None:
    """Generate the model comparison chart from synthetic observations."""
    features = load_synthetic_features()
    summary = summarize_comparison(features)
    output_path = create_comparison_chart(summary)

    print(f"Total vehicle-day rows: {summary['total_rows']}")
    print(f"Two-check rule flags: {summary['rule_flags']}")
    print(
        "Isolation Forest flags: "
        f"{summary['isolation_forest_flags']}"
    )
    print(f"LOF scored rows: {summary['lof_scored_rows']}")
    print(f"LOF status counts: {summary['lof_status_counts']}")
    print(f"Chart saved to: {output_path}")


if __name__ == "__main__":
    main()
