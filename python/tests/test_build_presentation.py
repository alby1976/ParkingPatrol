
"""Test the Markdown-driven presentation generator.

Design Pattern:
    None. These are focused unit tests.

Pattern Rationale:
    Tests verify the parser independently of PowerPoint creation.

Typical Usage:
    Run with pytest from the python directory.
"""

from pathlib import Path
import sys

REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
sys.path.insert(0, str(REPORTS_DIR))

from build_presentation import parse_outline


def test_parse_outline_reads_slide_titles_and_bullets(tmp_path):
    """Read multiple slides from a fictional Markdown outline."""
    outline = tmp_path / "outline.md"

    outline.write_text(
        "# Slide 1 — Introduction\n"
        "## The Problem\n"
        "- 38 parking spaces\n"
        "- Manual inspections\n"
        "\n"
        "## Slide 2 — Data Collection\n"
        "- Google Forms\n"
        "- Google Sheets\n",
        encoding="utf-8",
    )

    slides = parse_outline(outline)

    assert len(slides) == 2

    assert slides[0]["title"] == "Introduction"
    assert slides[0]["bullets"] == [
        "38 parking spaces",
        "Manual inspections",
    ]

    assert slides[1]["title"] == "Data Collection"
    assert slides[1]["bullets"] == [
        "Google Forms",
        "Google Sheets",
    ]


def test_parse_outline_preserves_chart_reference(tmp_path):
    """Preserve a Markdown chart reference for PowerPoint rendering."""
    outline = tmp_path / "outline.md"

    outline.write_text(
        "## Slide 7 — Model Comparison\n"
        "- Synthetic results only\n"
        "![Synthetic model comparison](model_comparison.png)\n",
        encoding="utf-8",
    )

    slides = parse_outline(outline)

    assert len(slides) == 1
    assert slides[0]["images"] == [
        {
            "alt": "Synthetic model comparison",
            "path": "model_comparison.png",
        }
    ]


def test_add_slide_image(tmp_path):
    """Insert a fictional chart image into a PowerPoint slide."""
    from PIL import Image

    from build_presentation import add_slide_image, create_presentation

    image_path = tmp_path / "fictional_chart.png"
    Image.new("RGB", (800, 450), "white").save(image_path)

    presentation = create_presentation()
    slide = presentation.slides.add_slide(
        presentation.slide_layouts[6]
    )

    add_slide_image(slide, image_path)

    assert len(slide.shapes) == 1
    assert slide.shapes[0].shape_type == 13


def test_tall_image_fits_within_slide(tmp_path):
    """Keep a tall image inside the slide's available space."""
    from PIL import Image

    from build_presentation import add_slide_image, create_presentation

    image_path = tmp_path / "tall_chart.png"
    Image.new("RGB", (300, 1200), "white").save(image_path)

    presentation = create_presentation()
    slide = presentation.slides.add_slide(
        presentation.slide_layouts[6]
    )

    add_slide_image(slide, image_path)

    picture = slide.shapes[0]

    assert picture.left >= 0
    assert picture.top >= 0
    assert picture.left + picture.width <= presentation.slide_width
    assert picture.top + picture.height <= presentation.slide_height


def test_build_slides_from_markdown(tmp_path):
    """Generate PowerPoint slides from a fictional Markdown outline."""
    from build_presentation import (
        build_slides,
        create_presentation,
        parse_outline,
    )

    outline = tmp_path / "outline.md"
    outline.write_text(
        "# Slide 1 — Introduction\n"
        "- First observation\n"
        "\n"
        "## Slide 2 — Findings\n"
        "- Second observation\n",
        encoding="utf-8",
    )

    slide_data = parse_outline(outline)
    presentation = create_presentation()

    build_slides(presentation, slide_data)

    assert len(presentation.slides) == 2
    assert "Introduction" in presentation.slides[0].shapes[0].text
    assert "Findings" in presentation.slides[1].shapes[0].text


def test_build_slides_from_markdown(tmp_path):
    """Generate PowerPoint slides from a fictional Markdown outline."""
    from build_presentation import (
        build_slides,
        create_presentation,
        parse_outline,
    )

    outline = tmp_path / "outline.md"
    outline.write_text(
        "# Slide 1 — Introduction\n"
        "- First observation\n"
        "\n"
        "## Slide 2 — Findings\n"
        "- Second observation\n",
        encoding="utf-8",
    )

    slide_data = parse_outline(outline)
    presentation = create_presentation()

    build_slides(presentation, slide_data)

    assert len(presentation.slides) == 2
    assert "Introduction" in presentation.slides[0].shapes[0].text
    assert "Findings" in presentation.slides[1].shapes[0].text


def test_build_slides_inserts_markdown_image(tmp_path):
    """Insert an image referenced by a fictional Markdown slide."""
    from PIL import Image
    from pptx.enum.shapes import MSO_SHAPE_TYPE

    from build_presentation import (
        build_slides,
        create_presentation,
        parse_outline,
    )

    image_path = tmp_path / "chart.png"
    Image.new("RGB", (800, 450), "white").save(image_path)

    outline = tmp_path / "outline.md"
    outline.write_text(
        "## Slide 7 — Model Comparison\n"
        "- Fictional observations only\n"
        "![Comparison chart](chart.png)\n",
        encoding="utf-8",
    )

    presentation = create_presentation()
    slide_data = parse_outline(outline)

    build_slides(presentation, slide_data)

    pictures = [
        shape
        for shape in presentation.slides[0].shapes
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE
    ]

    assert len(pictures) == 1


def test_slide_text_does_not_overlap_chart(tmp_path):
    """Keep slide text and a Markdown chart in separate areas."""
    from PIL import Image
    from pptx.enum.shapes import MSO_SHAPE_TYPE

    from build_presentation import (
        build_slides,
        create_presentation,
        parse_outline,
    )

    Image.new("RGB", (800, 450), "white").save(
        tmp_path / "chart.png"
    )

    outline = tmp_path / "outline.md"
    outline.write_text(
        "## Slide 7 — Model Comparison\n"
        "- Rule flagged 133 fictional observations\n"
        "- Isolation Forest flagged 32\n"
        "![Comparison chart](chart.png)\n",
        encoding="utf-8",
    )

    presentation = create_presentation()
    build_slides(presentation, parse_outline(outline))

    slide = presentation.slides[0]
    pictures = [
        shape for shape in slide.shapes
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE
    ]
    text_boxes = [
        shape for shape in slide.shapes
        if shape.has_text_frame
        and "Rule flagged" in shape.text
    ]

    assert len(pictures) == 1
    assert len(text_boxes) == 1

    picture = pictures[0]
    text_box = text_boxes[0]

    separated_horizontally = (
        text_box.left + text_box.width <= picture.left
        or picture.left + picture.width <= text_box.left
    )
    separated_vertically = (
        text_box.top + text_box.height <= picture.top
        or picture.top + picture.height <= text_box.top
    )

    assert separated_horizontally or separated_vertically


def test_long_slide_limits_visible_bullets():
    """Keep dense outline content from overflowing a slide."""
    from build_presentation import build_slides, create_presentation

    bullets = [f"Fictional research point {i}" for i in range(18)]

    presentation = create_presentation()
    build_slides(
        presentation,
        [{"title": "Conclusions", "bullets": bullets, "images": []}],
    )

    slide = presentation.slides[0]
    body_boxes = [
        shape
        for shape in slide.shapes
        if shape.has_text_frame and "Fictional research point" in shape.text
    ]

    assert len(body_boxes) == 1

    displayed = body_boxes[0].text
    assert displayed.count("Fictional research point") <= 4

    notes = slide.notes_slide.notes_text_frame.text

    assert "Fictional research point 0" in notes
    assert "Fictional research point 17" in notes


def test_parse_outline_selects_presentation_highlights(tmp_path):
    """Select explicit highlights without losing supporting details."""
    from build_presentation import parse_outline

    outline = tmp_path / "outline.md"
    outline.write_text(
        "## Slide 7 — Model Comparison\n"
        "### Presentation Highlights\n"
        "- Rule: 133 flagged\n"
        "- Isolation Forest: 32 flagged\n"
        "- LOF: Not scored\n"
        "- Synthetic data only\n"
        "\n"
        "### Supporting Details\n"
        "- Only 23 distinct feature patterns\n"
        "- Results do not establish real-world accuracy\n",
        encoding="utf-8",
    )

    slides = parse_outline(outline)

    assert len(slides) == 1

    assert slides[0]["highlights"] == [
        "Rule: 133 flagged",
        "Isolation Forest: 32 flagged",
        "LOF: Not scored",
        "Synthetic data only",
    ]

    assert len(slides[0]["bullets"]) == 6


def test_build_slides_displays_explicit_highlights():
    """Display selected highlights rather than the first outline bullets."""
    from build_presentation import build_slides, create_presentation

    presentation = create_presentation()

    build_slides(
        presentation,
        [
            {
                "title": "Model Comparison",
                "bullets": [
                    "Background detail one",
                    "Background detail two",
                    "Rule: 133 flagged",
                    "LOF: Not scored",
                ],
                "highlights": [
                    "Rule: 133 flagged",
                    "LOF: Not scored",
                ],
                "images": [],
            }
        ],
    )

    slide = presentation.slides[0]
    visible_text = "\n".join(
        shape.text for shape in slide.shapes if shape.has_text_frame
    )
    notes_text = slide.notes_slide.notes_text_frame.text

    assert "Rule: 133 flagged" in visible_text
    assert "LOF: Not scored" in visible_text
    assert "Background detail one" not in visible_text

    assert "Background detail one" in notes_text
    assert "Background detail two" in notes_text
