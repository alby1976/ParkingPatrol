"""Synthetic tests: same-day rule and exploratory anomaly detector."""
import sys
from pathlib import Path
import pandas as pd
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pattern_detection import (build_vehicle_day_features,
    mark_repeat_check_suspicious, score_anomalies, combine_review_signals)


def records():
    checks = pd.DataFrame([
        ("C1", "A", pd.Timestamp("2026-10-15T08:00:00-06:00"), True),
        ("C2", "A", pd.Timestamp("2026-10-15T12:00:00-06:00"), True),
        ("C3", "A", pd.Timestamp("2026-10-15T17:00:00-06:00"), False),
        ("C4", "A", pd.Timestamp("2026-10-16T09:00:00-06:00"), True),
        ("C5", "B", pd.Timestamp("2026-10-15T15:00:00-06:00"), True),
    ], columns=["check_id", "area_id", "check_at", "check_complete"])
    sightings = pd.DataFrame([
        ("SYN_A", "C1", "A", pd.Timestamp("2026-10-15T08:01:00-06:00")),
        ("SYN_A", "C1", "A", pd.Timestamp("2026-10-15T08:01:00-06:00")),
        ("SYN_A", "C2", "A", pd.Timestamp("2026-10-15T12:01:00-06:00")),
        ("SYN_A", "C4", "A", pd.Timestamp("2026-10-16T09:01:00-06:00")),
        ("SYN_B", "C3", "A", pd.Timestamp("2026-10-15T17:01:00-06:00")),
        ("SYN_C", "C5", "B", pd.Timestamp("2026-10-15T15:01:00-06:00")),
    ], columns=["vehicle_id", "check_id", "area_id", "observed_at"])
    return checks, sightings


def test_no_completed_checks_keeps_coverage_unknown():
    """Do not infer coverage from an incomplete inspection."""
    checks, sightings = records()
    checks["check_complete"] = False

    features = build_vehicle_day_features(checks, sightings)
    vehicle = features.query("vehicle_id == 'SYN_B'").iloc[0]

    assert vehicle["same_day_distinct_checks"] == 1
    assert vehicle["area_completed_checks_day"] == 0
    assert pd.isna(vehicle["observed_fraction_day"])


def test_two_distinct_checks_flag_suspicious():
    c, s = records()
    out = mark_repeat_check_suspicious(build_vehicle_day_features(c, s))
    a = out.query("vehicle_id == 'SYN_A' and day == '2026-10-15'").iloc[0]
    assert a["same_day_distinct_checks"] == 2
    assert bool(a["rule_suspicious"])
    assert not bool(out.query("vehicle_id == 'SYN_B'")["rule_suspicious"].iloc[0])


def test_duplicate_not_a_second_event_and_day_is_local():
    c, s = records()
    out = build_vehicle_day_features(c, s)
    assert out.query("vehicle_id == 'SYN_A' and day == '2026-10-15'").iloc[0]["same_day_distinct_checks"] == 2
    assert set(out["day"]) == {"2026-10-15", "2026-10-16"}


def test_incomplete_check_not_automatically_an_absence():
    c, s = records()
    a = build_vehicle_day_features(c, s).query(
        "vehicle_id == 'SYN_A' and day == '2026-10-15'").iloc[0]
    assert a["area_completed_checks_day"] == 2
    assert a["observed_fraction_day"] == 1.0
    assert "duration" not in a.index


def test_two_distinct_areas_count_distinct_events():
    c, s = records()
    s.loc[len(s)] = ("SYN_C", "C2", "A", pd.Timestamp("2026-10-15T12:03:00-06:00"))
    out = mark_repeat_check_suspicious(build_vehicle_day_features(c, s))
    assert bool(out.query("vehicle_id == 'SYN_C'")["rule_suspicious"].iloc[0])


def test_invalid_link_is_excluded_and_raw_plates_rejected():
    c, s = records()
    s.loc[len(s)] = ("SYN_D", "UNKNOWN", "A", pd.Timestamp("2026-10-15T14:00:00-06:00"))
    assert "SYN_D" not in set(build_vehicle_day_features(c, s)["vehicle_id"])
    s["license_plate"] = ""
    with pytest.raises(ValueError, match="private"):
        build_vehicle_day_features(c, s)


def test_small_samples_do_not_get_anomaly_labels():
    c, s = records()
    scored = score_anomalies(build_vehicle_day_features(c, s), min_samples=20)
    assert scored["anomaly_suspicious"].eq(False).all()
    assert scored["anomaly_score"].isna().all()
    assert scored["model_status"].eq("insufficient_samples").all()



def test_lof_small_samples_do_not_get_anomaly_labels():
    """Skip LOF scoring when too few observations are available."""
    from pattern_detection import score_lof_anomalies

    checks, sightings = records()
    features = build_vehicle_day_features(checks, sightings)

    scored = score_lof_anomalies(features, min_samples=20)

    assert scored["lof_suspicious"].eq(False).all()
    assert scored["lof_score"].isna().all()
    assert scored["lof_status"].eq("insufficient_samples").all()



def test_lof_skips_heavily_duplicated_features():
    """Avoid unreliable LOF scores for identical feature vectors."""
    from pattern_detection import score_lof_anomalies

    rows = [{
        "vehicle_id": f"SYN_{i}",
        "day": "2026-10-15",
        "same_day_distinct_checks": 1,
        "distinct_days_30d": 1,
        "area_completed_checks_day": 2,
        "observed_fraction_day": 0.5,
        "distinct_areas_day": 1,
        "check_hour_span": 0.0,
    } for i in range(40)]

    features = pd.DataFrame(rows)
    scored = score_lof_anomalies(features, min_samples=20)

    assert scored["lof_status"].eq("no_feature_variation").all()
    assert scored["lof_score"].isna().all()
    assert not scored["lof_suspicious"].any()



def test_lof_rejects_mixed_duplicate_neighborhoods():
    """Skip LOF when duplicate groups overwhelm the neighborhood."""
    from pattern_detection import score_lof_anomalies

    rows = [{
        "vehicle_id": f"SYN_{i}",
        "day": "2026-10-15",
        "same_day_distinct_checks": 1,
        "distinct_days_30d": 1,
        "area_completed_checks_day": 2,
        "observed_fraction_day": 0.5,
        "distinct_areas_day": 1,
        "check_hour_span": 0.0,
    } for i in range(40)]

    for i in range(30, 40):
        rows[i]["distinct_days_30d"] = i - 28

    scored = score_lof_anomalies(
        pd.DataFrame(rows), min_samples=20
    )

    assert scored["lof_status"].eq("duplicate_neighborhood").all()
    assert scored["lof_score"].isna().all()
    assert not scored["lof_suspicious"].any()


def test_lof_scores_eligible_synthetic_features():
    """Score suitable synthetic observations using LOF."""
    from pattern_detection import score_lof_anomalies

    rows = [{
        "vehicle_id": f"SYN_{i}",
        "day": "2026-10-15",
        "same_day_distinct_checks": 1 + (i % 3),
        "distinct_days_30d": 1 + (i % 7),
        "area_completed_checks_day": 3,
        "observed_fraction_day": (1 + (i % 3)) / 3,
        "distinct_areas_day": 1,
        "check_hour_span": float(i % 5),
    } for i in range(40)]

    features = pd.DataFrame(rows)
    scored = score_lof_anomalies(features, min_samples=20)

    assert scored["lof_status"].eq("scored").all()
    assert scored["lof_score"].notna().all()
    assert scored["lof_suspicious"].dtype == bool


def test_unsupervised_model_yields_separate_nonprobabilistic_signal():
    rows = [{
        "vehicle_id": f"SYN_{i}", "day": "2026-10-15",
        "same_day_distinct_checks": 1, "distinct_days_30d": 1,
        "area_completed_checks_day": 3, "observed_fraction_day": 1 / 3,
        "distinct_areas_day": 1, "check_hour_span": 0.0,
    } for i in range(40)]
    rows[0].update(same_day_distinct_checks=7, distinct_days_30d=12,
        area_completed_checks_day=8, observed_fraction_day=0.875,
        distinct_areas_day=3, check_hour_span=10.0)
    scored = score_anomalies(pd.DataFrame(rows), min_samples=20, contamination=0.05)
    assert scored["model_status"].eq("scored").all()
    assert scored["anomaly_suspicious"].any()
    assert "probability_of_violation" not in scored.columns
    combined = combine_review_signals(mark_repeat_check_suspicious(scored))
    assert combined["suspicious"].any()
    assert set(combined["flag_source"]).issubset(
        {"none", "rule", "anomaly", "rule+anomaly"})


def test_compare_three_methods_preserves_unscored_status():
    """Keep three review methods separate when data is insufficient."""
    from pattern_detection import compare_review_methods

    checks, sightings = records()
    features = build_vehicle_day_features(checks, sightings)

    result = compare_review_methods(features)

    assert "rule_suspicious" in result.columns
    assert "anomaly_suspicious" in result.columns
    assert "lof_suspicious" in result.columns

    assert result["model_status"].eq("insufficient_samples").all()
    assert result["lof_status"].eq("insufficient_samples").all()
    assert result["lof_score"].isna().all()

    assert result["rule_suspicious"].any()
    assert not result["lof_suspicious"].any()


def test_invalid_model_configuration_rejected():
    c, s = records()
    frame = build_vehicle_day_features(c, s)
    with pytest.raises(ValueError):
        score_anomalies(frame, min_samples=1)
    with pytest.raises(ValueError):
        score_anomalies(frame, contamination=0.9)
