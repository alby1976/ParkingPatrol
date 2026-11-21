# DATA120 results and presentation

This folder contains public-safe reporting artifacts built from fictional
synthetic observations and the student-reviewed eight-slide outline.

## Existing comparison outputs

- `PRESENTATION_OUTLINE.md`: accepted presentation structure and findings.
- `model_comparison_chart.py`: reproducible synthetic comparison chart generator.
- `model_comparison.png`: committed presentation chart generated from fictional data.
- `PROJECT_SUMMARY.md`: one-page project summary.

From the `python/` directory, regenerate the chart with:

```powershell
python reports/model_comparison_chart.py
```

## PowerPoint preparation

The planned eight-slide PowerPoint generator will use `python-pptx`.
Install all Python requirements using `python -m pip install -r requirements.txt`
from the `python/` directory. The `pyproject.toml` metadata reads the same
requirements file; there is no separate dependency list.

```powershell
python -c "import pptx; print(pptx.__version__)"
```

The student has verified `python-pptx 1.0.2` locally. **No PowerPoint deck or
generator has been created or tested yet.**

Synthetic demo findings: 315 fictional vehicle-day rows; two-check rule
flagged 133; Isolation Forest flagged 32; LOF was **not scored** on all 315
due to duplicate-feature safeguards. These are review signals, not validated
parking violations or model accuracy.

Do not commit confidential real-data exports, raw licence plates, secret
credentials or copyrighted third-party slides/images. Cite sources and
permitted GAI assistance according to the instructor's assignment rules.
