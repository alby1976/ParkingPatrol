"""Tests for reproducible multi-seed parking evaluation.

Design Pattern:
    None. These are focused pytest tests.

Pattern Rationale:
    Tests verify the evaluation contract independently.

Typical Usage:
    Run with pytest before implementing the evaluator.
"""

import pandas as pd

from multiseed_stability import evaluate_multiple_seeds


def test_evaluates_all_five_seeds():
    """Return one evaluation result for every requested seed."""
    seeds = [120, 121, 122, 123, 124]

    results = evaluate_multiple_seeds(seeds)

    assert len(results) == 5
    assert results["seed"].tolist() == seeds


def test_multiseed_results_are_reproducible():
    """Identical seed lists must produce identical evaluation summaries."""
    seeds = [120, 121, 122, 123, 124]

    first = evaluate_multiple_seeds(seeds)
    second = evaluate_multiple_seeds(seeds)

    pd.testing.assert_frame_equal(first, second)


def test_multiseed_flag_counts_are_valid():
    """Review flag counts must not exceed the number of vehicle-days."""
    results = evaluate_multiple_seeds([120, 121, 122, 123, 124])

    assert (results["vehicle_days"] > 0).all()

    for column in ["rule_flags", "if_flags", "lof_flags", "lof_scored"]:
        assert (results[column] >= 0).all()
        assert (results[column] <= results["vehicle_days"]).all()

    # LOF cannot flag more records than it successfully scored.
    assert (results["lof_flags"] <= results["lof_scored"]).all()


def test_multiseed_reports_lof_status():
    """Report why LOF could not score synthetic vehicle-day records."""
    results = evaluate_multiple_seeds([120, 121, 122, 123, 124])

    assert "lof_status" in results.columns

    # Every seed should report its LOF outcome.
    assert results["lof_status"].notna().all()

    # For these five scenarios, duplicated feature neighbourhoods
    # prevent LOF scoring.
    assert (
        results["lof_status"] == "duplicate_neighborhood"
    ).all()

    assert (results["lof_scored"] == 0).all()
