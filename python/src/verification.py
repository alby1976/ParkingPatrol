"""Human verification records, separate from ML review signals and enforcement.

This module records a decision and *reported* manual actions. It never
issues a ticket, changes a Google Sheet, or dispatches an officer.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime

FINDINGS = frozenset({"confirmed_violation", "no_violation", "inconclusive"})
ACTIONS = frozenset({"ticket", "tag"})


@dataclass(frozen=True)
class ManualAction:
    """Staff-recorded on-site action; not an instruction to take action."""

    action: str
    staff_id: str
    action_ref: str
    action_at: datetime


@dataclass(frozen=True)
class ReviewOutcome:
    """Explicit human finding, supported by a private evidence reference."""

    vehicle_id: str
    status: str
    reviewer_id: str
    evidence_ref: str
    reviewed_at: datetime
    blacklisted: bool
    manual_actions: tuple[ManualAction, ...] = ()


def _required(value: str, name: str) -> str:
    """Require a nonblank opaque identifier; never print source values."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be supplied by a human")
    return value.strip()


def _timestamp(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Expected timezone-aware timestamp")
    return value


def record_review(
    *, vehicle_id: str, suspicious: bool, finding: str,
    reviewer_id: str, evidence_ref: str, reviewed_at: datetime
) -> ReviewOutcome:
    """Record a human finding; a suspicion alone never establishes violation.

    Args:
        vehicle_id: Already-pseudonymized identifier.
        suspicious: Existing rule/ML review signal.
        finding: Human decision: confirmed_violation/no_violation/inconclusive.
        reviewer_id: Opaque staff ID explicitly recording human verification.
        evidence_ref: Opaque reference to restricted independent evidence.
        reviewed_at: Time of actual human review, with timezone.

    Returns:
        An immutable record; blacklisted only for confirmed violations.

    Notes:
        This does not authorize or perform enforcement. Store the real review
        evidence and any required local authority checks outside public Git.
    """
    _required(vehicle_id, "vehicle_id")
    if not isinstance(suspicious, bool):
        raise ValueError("suspicious must be boolean")
    if finding not in FINDINGS:
        raise ValueError("Invalid human finding")
    _required(reviewer_id, "reviewer_id")
    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
        raise ValueError("A private evidence reference is required")
    return ReviewOutcome(
        vehicle_id=vehicle_id.strip(), status=finding,
        reviewer_id=reviewer_id.strip(), evidence_ref=evidence_ref.strip(),
        reviewed_at=_timestamp(reviewed_at),
        blacklisted=finding == "confirmed_violation",
    )


def record_manual_action(
    review: ReviewOutcome, *, action: str, staff_id: str,
    action_ref: str, action_at: datetime
) -> ReviewOutcome:
    """Record a separate staff-reported on-site ticket/tag after confirmation.

    Never sends instructions to patrol or creates a ticket/tag itself.
    """
    if not isinstance(review, ReviewOutcome) or review.status != "confirmed_violation":
        raise ValueError("Manual action record requires confirmed human violation")
    if action not in ACTIONS:
        raise ValueError("Unsupported manual action")
    _required(staff_id, "staff_id")
    _required(action_ref, "action_ref")
    detail = ManualAction(
        action=action, staff_id=staff_id.strip(), action_ref=action_ref.strip(),
        action_at=_timestamp(action_at),
    )
    return replace(review, manual_actions=(*review.manual_actions, detail))
