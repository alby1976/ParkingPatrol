"""Build the DATA120 ParkingPatrol presentation.

Create an editable PowerPoint presentation from the approved outline
and public-safe, synthetic-data comparison chart.

Design Pattern:
    None. This module is a presentation-generation utility.

Pattern Rationale:
    A small, self-contained utility keeps presentation formatting
    separate from parking-data cleaning and anomaly detection.

Typical Usage:
    Run from the python directory:
        python reports/build_presentation.py
"""

import re
from pathlib import Path
from typing import Any

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt

REPORTS_DIR = Path(__file__).resolve().parent

OUTLINE_PATH = REPORTS_DIR / "PRESENTATION_OUTLINE.md"
CHART_PATH = REPORTS_DIR / "model_comparison.png"
OUTPUT_PATH = REPORTS_DIR / "ParkingPatrol_DATA120.pptx"


def create_presentation() -> Presentation:
    """Create a widescreen presentation with standard page dimensions.

    Returns:
        A new, empty 16:9 PowerPoint presentation.
    """
    presentation = Presentation()

    presentation.slide_width = Inches(13.333)
    presentation.slide_height = Inches(7.5)

    return presentation


def add_slide(presentation: Presentation, title: str):
    """Add a consistently formatted slide.

    Args:
        presentation: PowerPoint presentation to modify.
        title: Heading displayed at the top of the slide.

    Returns:
        The newly created PowerPoint slide.
    """
    slide = presentation.slides.add_slide(
        presentation.slide_layouts[6]
    )

    title_box = slide.shapes.add_textbox(
        Inches(0.7), Inches(0.35),
        Inches(11.9), Inches(0.8)
    )

    title_frame = title_box.text_frame
    title_frame.word_wrap = True

    paragraph = title_frame.paragraphs[0]
    paragraph.text = title
    paragraph.font.name = "Aptos Display"
    paragraph.font.size = Pt(28)
    paragraph.font.bold = True
    paragraph.font.color.rgb = RGBColor(30, 55, 85)

    return slide


def add_bullets(
        slide,
        bullet_points: list[str],
        left: float = 0.9,
        top: float = 1.5,
        width: float = 11.4,
        height: float = 5.2,
) -> None:
    """Add bullet points inside a configurable slide area.

    Args:
        slide: PowerPoint slide receiving the text.
        bullet_points: Statements to display.
        left: Left position in inches.
        top: Top position in inches.
        width: Text box width in inches.
        height: Text box height in inches.
    """
    text_box = slide.shapes.add_textbox(
        Inches(left),
        Inches(top),
        Inches(width),
        Inches(height),
    )

    text_frame = text_box.text_frame
    text_frame.word_wrap = True

    for index, bullet in enumerate(bullet_points):
        paragraph = (
            text_frame.paragraphs[0]
            if index == 0
            else text_frame.add_paragraph()
        )

        paragraph.text = f"• {bullet}"
        paragraph.font.name = "Aptos"
        paragraph.font.size = Pt(22)
        paragraph.font.color.rgb = RGBColor(45, 55, 72)
        paragraph.space_after = Pt(16)


def build_slide_1(presentation: Presentation) -> None:
    """Add the ParkingPatrol introduction slide.

    Args:
        presentation: Presentation receiving the slide.
    """
    slide = add_slide(
        presentation,
        "ParkingPatrol: Detecting Unusual Parking Patterns",
    )

    add_bullets(
        slide,
        [
            "38-space customer-only parking lot",
            "Staff inspect vehicles once or twice daily",
            "Repeated sightings may reveal unusual patterns",
            "Compare a simple rule with unsupervised ML",
            "Observations alone cannot prove a violation",
        ],
    )


def build_slide_2(presentation: Presentation) -> None:
    """Explain how ParkingPatrol collects vehicle observations.

    Args:
        presentation: Presentation receiving the slide.
    """
    slide = add_slide(
        presentation,
        "How ParkingPatrol Collects Data",
    )

    add_bullets(
        slide,
        [
            "38 customer-only parking spaces",
            "Staff usually inspect twice daily, sometimes once",
            "Google Forms records observed vehicles and timestamps",
            "Google Sheets stores the inspection records",
            "Arrival and departure times are not recorded",
            "Python analyzes observation patterns, not violations",
        ],
    )


def parse_outline(path: Path) -> list[dict[str, object] | None]:
    """Extract slide titles and bullet points from Markdown.

    Args:
        path: Path to a UTF-8 Markdown presentation outline.

    Returns:
        A list of dictionaries containing slide titles and bullets.
    """
    slides: list[dict[str, Any] | None] = []
    current_slide: dict[str, Any] | None = None
    current_section = None

    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()

        if text.startswith(("# Slide ", "## Slide ")):
            title = text.split("—", maxsplit=1)[-1].strip()

            current_slide = {
                "title": title,
                "bullets": [],
                "images": [],
                "highlights": [],
                "source_dir": path.parent,
            }
            slides.append(current_slide)


        elif text.startswith("- ") and current_slide is not None:
            bullet = text[2:]
            current_slide["bullets"].append(bullet)

            if current_section == "Presentation Highlights":
                current_slide["highlights"].append(bullet)

        elif text.startswith("### ") and current_slide is not None:
            current_section = text[4:].strip()

        elif (
                text.startswith("![")
                and "](" in text
                and text.endswith(")")
                and current_slide is not None
        ):
            alt, image_path = text[2:-1].split("](", maxsplit=1)

            current_slide["images"].append(
                {
                    "alt": alt,
                    "path": image_path,
                }
            )
    return slides


def add_slide_image(
        slide,
        image_path: Path,
        left_inches: float | None = None,
        top_inches: float | None = None,
        max_width_inches: float = 11.3,
        max_height_inches: float = 5.5,
) -> None:
    """Fit an image inside a slide without distorting it.

    Args:
        slide: PowerPoint slide receiving the image.
        image_path: Path to an existing image file.

    Raises:
        FileNotFoundError: If the image does not exist.
    """
    if not image_path.is_file():
        raise FileNotFoundError(
            f"Presentation image not found: {image_path}"
        )

    from PIL import Image

    with Image.open(image_path) as image:
        image_width, image_height = image.size

    # Reserve space at the top for the slide title.

    max_width = Inches(max_width_inches)
    max_height = Inches(max_height_inches)

    # Scale uniformly so neither dimension exceeds its limit.
    scale = min(
        max_width / image_width,
        max_height / image_height,
    )

    picture_width = int(image_width * scale)
    picture_height = int(image_height * scale)

    # Centre the image in the available area.

    slide_width = Inches(13.333)

    left = (
        int((slide_width - picture_width) / 2)
        if left_inches is None
        else Inches(left_inches)
    )

    top = (
        Inches(1.5) + int((max_height - picture_height) / 2)
        if top_inches is None
        else Inches(top_inches)
    )

    slide.shapes.add_picture(
        str(image_path),
        left,
        top,
        width=picture_width,
        height=picture_height,
    )


def build_model_comparison_slide(slide, highlights: list[str]) -> None:
    """Build an editable visual comparison of parking detection methods.

    Args:
        slide: Existing PowerPoint slide with its title already added.
        highlights: Model findings extracted from the Markdown outline.

    Notes:
        Flags are anomaly signals, not confirmed parking violations.
        LOF is deliberately marked as unscored when the safeguard applies.
    """

    def add_text(text, x, y, w, h, size=16, bold=False,
                 color=(30, 55, 85)):
        shape = slide.shapes.add_textbox(
            Inches(x), Inches(y), Inches(w), Inches(h)
        )
        frame = shape.text_frame
        frame.word_wrap = True
        frame.margin_left = Inches(0.05)
        frame.margin_top = Inches(0.03)

        p = frame.paragraphs[0]
        p.text = str(text)
        p.font.name = "Aptos"
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = RGBColor(*color)
        return shape

    def rectangle(x, y, w, h, color):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*color)
        shape.line.fill.background()
        return shape

    def get_count(keyword):
        for line in highlights:
            if keyword.lower() in line.lower():
                match = re.search(r"\b(\d+)\s+flagged\b", line, re.I)
                if match:
                    return int(match.group(1))
        return None

    rule_count = get_count("Two-check rule")
    forest_count = get_count("Isolation Forest")

    add_text(
        "Flag counts (not accuracy)",
        0.8, 1.25, 10, 0.4, size=18, bold=True
    )

    cards = [
        ("TWO-CHECK RULE", rule_count, (34, 105, 155)),
        ("ISOLATION FOREST", forest_count, (36, 140, 115)),
        ("LOCAL OUTLIER FACTOR", None, (105, 115, 135)),
    ]

    for i, (name, count, color) in enumerate(cards):
        x = 0.8 + i * 4.2

        rectangle(x, 1.85, 3.9, 1.65, (238, 243, 249))

        add_text(name, x + 0.2, 2.05, 3.5, 0.35,
                 size=13, bold=True, color=color)

        value = str(count) if count is not None else "Not scored"

        add_text(
            value, x + 0.2, 2.48, 3.5, 0.65,
            size=28 if count is not None else 20,
            bold=True
        )

    maximum = max(
        (count for count in (rule_count, forest_count)
         if count is not None),
        default=0
    )

    for index, (name, count, color) in enumerate(cards[:2]):
        y = 3.9 + index * 0.65

        add_text(name, 0.8, y, 3.0, 0.35, size=13)

        rectangle(3.9, y, 7.4, 0.27, (225, 231, 237))

        if maximum > 0 and count is not None and count > 0:
            rectangle(
                3.9, y,
                7.4 * count / maximum,
                0.27, color
            )

        add_text(
            str(count) if count is not None else "N/A",
            11.5, y - 0.05, 0.9, 0.4, size=15, bold=True
        )

    add_text(
        "LOF: Scoring withheld because duplicate feature patterns "
        "exceeded the configured neighborhood size.",
        0.8, 5.3, 11.8, 0.55, size=14
    )

    rectangle(0.8, 6.0, 11.8, 0.85, (232, 240, 248))

    add_text(
        "KEY TAKEAWAY",
        1.05, 6.08, 2.5, 0.3,
        size=13, bold=True
    )

    add_text(
        "Synthetic data only. Flags are not accuracy measures "
        "or confirmed violations; human verification is required.",
        1.05, 6.38, 11.1, 0.37,
        size=12
    )


def build_slides(
        presentation: Presentation,
        slide_data: list[dict[str, object]],
) -> None:
    """Create slides from Markdown with separate text and image areas.

    Args:
        presentation: Presentation receiving the slides.
        slide_data: Parsed Markdown slide information.
    """
    for item in slide_data:
        slide = add_slide(presentation, item["title"])

        # Use the specialized layout for the model comparison slide.
        if item["title"].strip().lower() == "model comparison and findings":
            add_speaker_notes(slide, item.get("bullets", []))
            build_model_comparison_slide(
                slide,
                item.get("highlights", []) or item.get("bullets", []),
            )
            continue

        bullets = item.get("bullets", [])
        images = item.get("images", [])

        # Preserve the complete outline in PowerPoint speaker notes.
        add_speaker_notes(slide, bullets)

        # Prefer explicitly selected presentation highlights.
        # Fall back to the first four bullets for older outlines.
        highlights = item.get("highlights", [])
        visible_bullets = (
            highlights[:4] if highlights else bullets[:4]
        )

        if images:
            # Use a side-by-side layout when images are present.
            if bullets:
                add_bullets(
                    slide,
                    visible_bullets,
                    left=0.7,
                    top=1.5,
                    width=5.0,
                    height=5.2,
                )

            for image_info in images:
                image_path = (
                        Path(item["source_dir"]) / image_info["path"]
                )

                add_slide_image(
                    slide,
                    image_path,
                    left_inches=6.0,
                    top_inches=1.7,
                    max_width_inches=6.5,
                    max_height_inches=4.8,
                )

        elif bullets:
            # Text-only slides use the original full-width layout.
            add_bullets(slide, visible_bullets)


def add_speaker_notes(slide, bullet_points: list[str]) -> None:
    """Preserve all original bullet points in PowerPoint speaker notes.

    Args:
        slide: PowerPoint slide receiving the notes.
        bullet_points: Complete bullet list from the Markdown outline.
    """
    notes_frame = slide.notes_slide.notes_text_frame

    notes_frame.text = "\n".join(bullet_points)


def main() -> None:
    """Generate a PowerPoint presentation from the Markdown outline."""
    slide_data = parse_outline(OUTLINE_PATH)

    presentation = create_presentation()
    build_slides(presentation, slide_data)

    presentation.save(OUTPUT_PATH)

    print(f"Slides generated: {len(presentation.slides)}")
    print(f"PowerPoint saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
