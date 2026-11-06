"""Synthetic, test-first verification workflow tests. No real plate data."""
from datetime import datetime, timezone
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from verification import record_review, record_manual_action  # noqa: E402


WHEN = datetime(2026, 11, 5, 20, 0, tzinfo=timezone.utc)


def test_confirmed_violation_blacklists_only_after_explicit_human_review():
    outcome = record_review(
        vehicle_id="SYN_001", suspicious=True, finding="confirmed_violation",
        reviewer_id="STAFF_TEST", evidence_ref="PRIVATE_CASE_001", reviewed_at=WHEN
    )
    assert outcome.blacklisted is True
    assert outcome.status == "confirmed_violation"
    assert outcome.manual_actions == ()


@pytest.mark.parametrize("finding", ["no_violation", "inconclusive"])
def test_review_not_confirming_violation_does_not_blacklist(finding):
    outcome = record_review(
        vehicle_id="SYN_002", suspicious=True, finding=finding,
        reviewer_id="STAFF_TEST", evidence_ref="PRIVATE_CASE_002", reviewed_at=WHEN
    )
    assert outcome.blacklisted is False
    assert outcome.manual_actions == ()


def test_model_suspicion_cannot_automatically_blacklist():
    with pytest.raises(ValueError, match="human"):
        record_review(
            vehicle_id="SYN_003", suspicious=True, finding="confirmed_violation",
            reviewer_id="", evidence_ref="PRIVATE_CASE_003", reviewed_at=WHEN
        )


def test_no_evidence_cannot_confirm_violation():
    with pytest.raises(ValueError, match="evidence"):
        record_review(
            vehicle_id="SYN_004", suspicious=True, finding="confirmed_violation",
            reviewer_id="STAFF_TEST", evidence_ref="", reviewed_at=WHEN
        )


def test_manual_ticket_and_tag_are_separate_recorded_actions():
    review = record_review(
        vehicle_id="SYN_005", suspicious=True, finding="confirmed_violation",
        reviewer_id="STAFF_TEST", evidence_ref="PRIVATE_CASE_005", reviewed_at=WHEN
    )
    ticket = record_manual_action(
        review, action="ticket", staff_id="PATROL_TEST",
        action_ref="PRIVATE_TICKET_001", action_at=WHEN
    )
    tagged = record_manual_action(
        ticket, action="tag", staff_id="PATROL_TEST",
        action_ref="PRIVATE_TAG_001", action_at=WHEN
    )
    assert tagged.blacklisted is True
    assert tuple(a.action for a in tagged.manual_actions) == ("ticket", "tag")


def test_no_manual_enforcement_action_without_confirmed_violation():
    review = record_review(
        vehicle_id="SYN_006", suspicious=True, finding="inconclusive",
        reviewer_id="STAFF_TEST", evidence_ref="PRIVATE_CASE_006", reviewed_at=WHEN
    )
    with pytest.raises(ValueError, match="confirmed"):
        record_manual_action(
            review, action="ticket", staff_id="STAFF_TEST",
            action_ref="PRIVATE_TICKET_006", action_at=WHEN
        )


def test_manual_action_cannot_be_faked_by_ai():
    review = record_review(
        vehicle_id="SYN_007", suspicious=True, finding="confirmed_violation",
        reviewer_id="STAFF_TEST", evidence_ref="PRIVATE_CASE_007", reviewed_at=WHEN
    )
    with pytest.raises(ValueError, match="staff"):
        record_manual_action(
            review, action="tag", staff_id="",
            action_ref="PRIVATE_TAG_007", action_at=WHEN
        )


def test_reject_unknown_outcome_or_action():
    with pytest.raises(ValueError, match="finding"):
        record_review(
            vehicle_id="SYN_008", suspicious=True, finding="suspicious",
            reviewer_id="STAFF_TEST", evidence_ref="PRIVATE_CASE_008", reviewed_at=WHEN
        )
    review = record_review(
        vehicle_id="SYN_008", suspicious=True, finding="confirmed_violation",
        reviewer_id="STAFF_TEST", evidence_ref="PRIVATE_CASE_008", reviewed_at=WHEN
    )
    with pytest.raises(ValueError, match="action"):
        record_manual_action(
            review, action="automatic_tow", staff_id="STAFF_TEST",
            action_ref="PRIVATE_008", action_at=WHEN
        )
