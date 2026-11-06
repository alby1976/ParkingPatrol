"""Pure, privacy-conscious normalization for DATA120 observation data.

Input must already contain pseudonymous vehicle IDs. No Google API, network,
secrets, model predictions, or parking enforcement logic belongs here.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

import pandas as pd

TIME_ZONE = "America/Edmonton"
CHECK_COLUMNS = ("check_id", "area_id", "check_at", "check_complete")
SIGHTING_COLUMNS = ("vehicle_id", "check_id", "area_id", "observed_at")
FORBIDDEN = frozenset(
    {"plate", "license_plate", "licence_plate", "plate_number", "raw_plate",
     "driver_name", "customer_name", "password", "api_key"}
)


@dataclass(frozen=True)
class CleanResult:
    """Cleaned tables and non-identifying diagnostics (no source values)."""

    checks: pd.DataFrame
    sightings: pd.DataFrame
    issues: pd.DataFrame


def _clean_text(value: object) -> str | None:
    if pd.isna(value):
        return None
    value = re.sub(r"\\s+", " ", str(value)).strip().upper()
    return value or None


def _parse_time(value: object) -> pd.Timestamp | pd.NaT:
    """Parse datetime into Edmonton time, rejecting ambiguous local times."""
    try:
        if pd.isna(value) or str(value).strip() == "":
            return pd.NaT
        ts = pd.Timestamp(value)
        if pd.isna(ts):
            return pd.NaT
        if ts.tzinfo is None:
            return ts.tz_localize(TIME_ZONE, ambiguous="raise", nonexistent="raise")
        return ts.tz_convert(TIME_ZONE)
    except Exception:  # pandas may raise timezone-library-specific DST exceptions.
        return pd.NaT


def _parse_complete(value: object) -> bool | None:
    if pd.isna(value):
        return None
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "yes", "y", "1", "complete", "completed"}:
        return True
    if normalized in {"false", "no", "n", "0", "incomplete", "partial"}:
        return False
    return None


def _source_frame(frame: pd.DataFrame, required: tuple[str, ...], name: str) -> pd.DataFrame:
    if not isinstance(frame, pd.DataFrame):
        raise TypeError(f"{name} must be a pandas DataFrame")
    columns = {str(column).strip().lower() for column in frame.columns}
    if columns & FORBIDDEN:
        raise ValueError("Raw identifiers or credentials are not permitted in the cleaning input")
    if frame.columns.duplicated().any():
        raise ValueError(f"{name} contains duplicate column names")
    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise ValueError(f"{name} missing columns: {', '.join(missing)}")
    # Discard unknown columns to prevent accidental retention of private data.
    return frame.loc[:, list(required)].reset_index(drop=True).copy()


def normalize_observations(checks: pd.DataFrame, sightings: pd.DataFrame) -> CleanResult:
    """Normalize check and sighting tables without inventing parking durations.

    Args:
        checks: One row per check/area; includes empty or incomplete checks.
        sightings: Pseudonymous vehicle/check/area observations only.

    Returns:
        CleanResult with sanitized tables and issue descriptions/row positions.
        Invalid rows are excluded from cleaned output and listed in issues.
    """
    check_data = _source_frame(checks, CHECK_COLUMNS, "checks")
    sight_data = _source_frame(sightings, SIGHTING_COLUMNS, "sightings")
    diagnostics: list[dict[str, object]] = []

    def note(table: str, pos: int, reason: str) -> None:
        diagnostics.append({"table": table, "row_index": pos, "issue": reason})

    valid_checks: list[dict[str, object]] = []
    for pos, row in check_data.iterrows():
        ident = _clean_text(row["check_id"])
        area = _clean_text(row["area_id"])
        at = _parse_time(row["check_at"])
        complete = _parse_complete(row["check_complete"])
        if ident is None or area is None or pd.isna(at) or complete is None:
            note("checks", pos, "missing_or_invalid_required_field")
            continue
        valid_checks.append({
            "check_id": ident, "area_id": area, "check_at": at,
            "check_complete": complete, "_row_index": pos,
        })

    check_output = pd.DataFrame(valid_checks)
    if check_output.empty:
        check_output = pd.DataFrame(columns=[*CHECK_COLUMNS, "_row_index"])
    # If the same check/area disagrees about time or completeness, quarantine
    # all matching rows rather than arbitrarily keeping one interpretation.
    retained: list[dict[str, object]] = []
    for _, group in check_output.groupby(["check_id", "area_id"], sort=False):
        if len(group[["check_at", "check_complete"]].drop_duplicates()) > 1:
            for pos in group["_row_index"]:
                note("checks", int(pos), "conflicting_duplicate_check")
        else:
            retained.append(group.iloc[0].to_dict())
            for pos in group["_row_index"].iloc[1:]:
                note("checks", int(pos), "duplicate_check")
    check_output = pd.DataFrame(retained, columns=[*CHECK_COLUMNS, "_row_index"])
    if not check_output.empty:
        # A check ID should not describe multiple areas in this normalized schema.
        collision = check_output["check_id"].duplicated(keep=False)
        if collision.any():
            for pos in check_output.loc[collision, "_row_index"]:
                note("checks", int(pos), "check_id_used_for_multiple_areas")
            check_output = check_output.loc[~collision].copy()

    valid_keys = set(zip(check_output["check_id"], check_output["area_id"]))
    valid_sights: list[dict[str, object]] = []
    seen: set[tuple[str, str, str]] = set()
    for pos, row in sight_data.iterrows():
        ident = _clean_text(row["vehicle_id"])
        check_id = _clean_text(row["check_id"])
        area = _clean_text(row["area_id"])
        observed_at = _parse_time(row["observed_at"])
        if not ident or not check_id or not area or pd.isna(observed_at):
            note("sightings", pos, "missing_or_invalid_required_field")
            continue
        if (check_id, area) not in valid_keys:
            note("sightings", pos, "unknown_or_invalid_check")
            continue
        key = (ident, check_id, area)
        if key in seen:
            note("sightings", pos, "duplicate_vehicle_in_check")
            continue
        seen.add(key)
        valid_sights.append({
            "vehicle_id": ident, "check_id": check_id,
            "area_id": area, "observed_at": observed_at,
        })

    cleaned_checks = check_output.reindex(columns=list(CHECK_COLUMNS)).reset_index(drop=True)
    cleaned_sights = pd.DataFrame(valid_sights, columns=list(SIGHTING_COLUMNS))
    issues = pd.DataFrame(diagnostics, columns=["table", "row_index", "issue"])
    return CleanResult(cleaned_checks, cleaned_sights, issues)
