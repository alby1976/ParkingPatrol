"""Normalize parking categories, including a historically confirmed ticket status.

Accept only pseudonymous vehicle identifiers from a restricted import
boundary. Historical Violator means a prior ticket exists according to authorized staff;
this function cannot check the underlying ticket record. Never modify
operational statuses, contact
AI services, or initiate enforcement.

Design Pattern:
    None.

Pattern Rationale:
    A pure, cohesive transformation validates a small research table
    without introducing adapter/service classes before a Sheets
    integration is approved.

Typical Usage:
    Pass approved, locally pseudonymized staff reports to
    normalize_staff_reports. Keep independently verified outcomes in
    the separate verification module.
"""

from __future__ import annotations

import re

import pandas as pd

STAFF_STATUSES = frozenset({"unknown", "suspicious", "violator"})
COLUMNS = ("vehicle_id", "staff_status", "reported_at")
OPAQUE_ID = re.compile(r"^(?:V[0-9A-F]{24}|SYN_[A-Z0-9_]+|DEMO_[A-Z0-9_]+)$")
FORBIDDEN = frozenset({
    "plate", "license_plate", "licence_plate", "plate_number", "raw_plate",
    "driver_name", "customer_name", "api_key", "password"
})


def normalize_staff_reports(reports: pd.DataFrame) -> pd.DataFrame:
    """Normalize labels without verifying private historical ticket evidence.

    Args:
        reports: A table with already-pseudonymized vehicle IDs, an explicitly
            selected staff status, and offset-aware report timestamps.

    Returns:
        Independent copy with lowercase statuses, normalized opaque vehicle
        IDs, and timestamps in America/Edmonton time.

    Raises:
        TypeError: Input is not a pandas DataFrame.
        ValueError: Required fields are missing, forbidden raw identifiers
            appear, staff statuses are invalid, or timestamps lack an offset.

    Note:
        A "violator" selection represents an authorized staff attestation
        that this vehicle received a ticket in the past, rather than a
        suspicion. The underlying ticket record must be confirmed through
        restricted operational records; this pure validator cannot check
        it. It does not establish a new violation, issue a ticket or tow,
        or serve as automatic model ground truth.
        Never join future status reports into historical ML feature rows.
    """
    if not isinstance(reports, pd.DataFrame):
        raise TypeError("reports must be a DataFrame")
    if reports.columns.duplicated().any():
        raise ValueError("Duplicate input columns")
    if {str(x).strip().lower() for x in reports.columns} & FORBIDDEN:
        raise ValueError("Reports must not contain raw plate or private fields")
    if set(COLUMNS) - set(reports.columns):
        raise ValueError("Missing required status-report fields")
    if set(reports.columns) != set(COLUMNS):
        raise ValueError("Unexpected status-report fields")

    out = reports.loc[:, list(COLUMNS)].copy(deep=True)
    ids = out["vehicle_id"].map(
        lambda x: x.strip().upper() if isinstance(x, str) else ""
    )
    if ids.eq("").any() or not ids.map(lambda x: bool(OPAQUE_ID.fullmatch(x))).all():
        raise ValueError("Missing or non-pseudonymous vehicle ID")
    out["vehicle_id"] = ids

    labels = out["staff_status"].map(
        lambda x: x.strip().lower() if isinstance(x, str) else ""
    )
    if not labels.isin(STAFF_STATUSES).all():
        raise ValueError("Missing or invalid staff status")
    out["staff_status"] = labels

    try:
        times = pd.to_datetime(out["reported_at"], utc=False, errors="raise")
        if times.dt.tz is None:
            raise ValueError("Report timestamps require a UTC offset")
        out["reported_at"] = times.dt.tz_convert("America/Edmonton")
    except (TypeError, AttributeError) as exc:
        raise ValueError("Report timestamps require matching explicit offsets") from exc
    except ValueError as exc:
        raise ValueError("Invalid or naive report timestamp") from exc
    return out.reset_index(drop=True)
