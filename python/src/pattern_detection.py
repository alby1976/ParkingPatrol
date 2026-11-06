"""Experimental anomaly signals from previously cleaned, pseudonymous checks.

No Google access, direct enforcement or inference of actual parking duration.
"""
from __future__ import annotations
from datetime import timedelta
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ("same_day_distinct_checks", "distinct_days_30d",
            "area_completed_checks_day", "observed_fraction_day",
            "distinct_areas_day", "check_hour_span")
PRIVATE = {"plate", "license_plate", "licence_plate", "plate_number",
           "raw_plate", "driver_name", "customer_name", "password", "api_key"}


def _check(frame: pd.DataFrame, required: tuple[str, ...]) -> None:
    """Require expected fields, without retaining source secrets."""
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame")
    if {str(c).lower() for c in frame.columns} & PRIVATE:
        raise ValueError("Input contains private raw identifier columns")
    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise ValueError("Missing fields: " + ", ".join(missing))


def build_vehicle_day_features(checks: pd.DataFrame, sightings: pd.DataFrame) -> pd.DataFrame:
    """Count distinct observed rounds per Edmonton day and recent observation days.

    Both inputs must come from the cleaning boundary and contain pseudonymous
    vehicle identifiers. Same-day events are distinct check IDs, not separate
    arrivals or confirmed parking visits. Incomplete checks may contribute
    positive sightings but never establish absence.
    """
    _check(checks, ("check_id", "area_id", "check_at", "check_complete"))
    _check(sightings, ("vehicle_id", "check_id", "area_id", "observed_at"))
    output_cols = ["vehicle_id", "day", *FEATURES]
    if checks.empty or sightings.empty:
        return pd.DataFrame(columns=output_cols)
    c = checks[["check_id", "area_id", "check_at", "check_complete"]].copy()
    if c.duplicated(["check_id", "area_id"]).any():
        raise ValueError("Duplicate area-check keys; clean checks first")
    c["check_at"] = pd.to_datetime(c["check_at"], utc=True).dt.tz_convert("America/Edmonton")
    c["day"] = c["check_at"].dt.date.astype(str)
    c["hour"] = c["check_at"].dt.hour + c["check_at"].dt.minute / 60
    s = sightings[["vehicle_id", "check_id", "area_id", "observed_at"]].copy()
    observed = s.merge(c, on=["check_id", "area_id"], how="inner",
                       validate="many_to_one").drop_duplicates(
                           ["vehicle_id", "check_id", "area_id"])
    if observed.empty:
        return pd.DataFrame(columns=output_cols)
    complete = (c.loc[c["check_complete"] == True]
                .groupby(["day", "area_id"])["check_id"].nunique()
                .rename("opportunities"))
    area = (observed.groupby(["vehicle_id", "day", "area_id"])
            .agg(seen_complete=("check_complete", "sum")).join(complete))
    area["opportunities"] = area["opportunities"].fillna(0)
    coverage = area.groupby(level=["vehicle_id", "day"]).agg(
        completed=("opportunities", "sum"), seen=("seen_complete", "sum"))
    perday = observed.groupby(["vehicle_id", "day"]).agg(
        same_day_distinct_checks=("check_id", "nunique"),
        distinct_areas_day=("area_id", "nunique"),
        first_hour=("hour", "min"), last_hour=("hour", "max")).join(coverage)
    perday["area_completed_checks_day"] = perday["completed"]
    perday["observed_fraction_day"] = (
        perday["seen"] / perday["completed"].replace(0, np.nan))
    perday["check_hour_span"] = perday["last_hour"] - perday["first_hour"]
    result = perday.reset_index()
    dates_by_vehicle = {
        vehicle: sorted(pd.to_datetime(group["day"]).dt.date.unique())
        for vehicle, group in result.groupby("vehicle_id")
    }
    def recent_days(row: pd.Series) -> int:
        day = pd.Timestamp(row["day"]).date()
        start = day - timedelta(days=29)
        return sum(start <= d <= day for d in dates_by_vehicle[row["vehicle_id"]])
    result["distinct_days_30d"] = result.apply(recent_days, axis=1)
    return result[output_cols].reset_index(drop=True)


def mark_repeat_check_suspicious(features: pd.DataFrame) -> pd.DataFrame:
    """Label review priority for two or more distinct checks in one day."""
    _check(features, ("same_day_distinct_checks",))
    out = features.copy()
    out["rule_suspicious"] = out["same_day_distinct_checks"] >= 2
    return out


def score_anomalies(features: pd.DataFrame, *, min_samples: int = 20,
                    contamination: float = 0.10, random_state: int = 42) -> pd.DataFrame:
    """Explore unusual patterns with IsolationForest; NOT misconduct probabilities.

    Scores are relative to this fitted dataset. For prospective work, fit
    only on past data and score later observations without future leakage.
    """
    if min_samples < 5 or not (0 < contamination <= 0.5):
        raise ValueError("Invalid anomaly model configuration")
    _check(features, FEATURES)
    out = features.copy()
    out["anomaly_score"] = np.nan
    out["anomaly_suspicious"] = False
    out["model_status"] = "insufficient_samples"
    if len(out) < min_samples:
        return out
    matrix = out[list(FEATURES)].astype(float)
    eligible = matrix.notna().all(axis=1) & np.isfinite(matrix).all(axis=1)
    if eligible.sum() < min_samples:
        out["model_status"] = "insufficient_coverage"
        return out
    valid = matrix.loc[eligible]
    if valid.nunique().max() <= 1:
        out["model_status"] = "no_feature_variation"
        return out
    model = make_pipeline(StandardScaler(), IsolationForest(
        contamination=contamination, n_estimators=100, random_state=random_state))
    model.fit(valid)
    out.loc[eligible, "anomaly_score"] = -model.decision_function(valid)
    out.loc[eligible, "anomaly_suspicious"] = model.predict(valid) == -1
    out.loc[eligible, "model_status"] = "scored"
    out.loc[~eligible, "model_status"] = "insufficient_coverage"
    return out


def combine_review_signals(frame: pd.DataFrame) -> pd.DataFrame:
    """Keep the rule and ML explanations separate for staff review."""
    _check(frame, ("rule_suspicious", "anomaly_suspicious"))
    out = frame.copy()
    rule = out["rule_suspicious"].fillna(False).astype(bool)
    ml = out["anomaly_suspicious"].fillna(False).astype(bool)
    out["suspicious"] = rule | ml
    out["flag_source"] = np.select(
        [rule & ml, rule, ml], ["rule+anomaly", "rule", "anomaly"], default="none")
    return out
