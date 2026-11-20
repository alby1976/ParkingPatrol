
"""Tests for the synthetic model-comparison chart."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
_original_close = plt.close
REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
sys.path.insert(0, str(REPORTS_DIR))

from model_comparison_chart import create_comparison_chart


def test_chart_labels_unscored_lof(tmp_path, monkeypatch):
    """LOF must say 'Not scored', not report zero detections."""
    summary = {
        "total_rows": 315,
        "rule_flags": 133,
        "isolation_forest_flags": 32,
        "lof_scored_rows": 0,
        "lof_flags": 0,
    }

    monkeypatch.setattr(
        "model_comparison_chart.__file__",
        str(tmp_path / "model_comparison_chart.py"),
    )
    monkeypatch.setattr(plt, "close", lambda figure: None)

    try:
        output_path = create_comparison_chart(summary)

        assert output_path.exists()

        figure = plt.gcf()
        labels = [text.get_text() for text in figure.axes[0].texts]

        assert "Not scored" in labels
        assert "0" not in labels
    finally:
        _original_close(figure)
