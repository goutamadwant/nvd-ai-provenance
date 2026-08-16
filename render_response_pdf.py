#!/usr/bin/env python3
"""Render the NIST response Markdown as a polished, searchable PDF."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#176B87")
TEAL = colors.HexColor("#218380")
TEXT = colors.HexColor("#202A33")
MUTED = colors.HexColor("#5E6A73")
LINE = colors.HexColor("#D7E0E6")


def inline_markup(value: str) -> str:
    escaped = html.escape(value.strip())
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"`(.+?)`", r'<font name="Courier">\1</font>', escaped)
    escaped = re.sub(
        r"(?<![\"'=])(https?://[^\s<]+)",
        lambda match: f'<link href="{match.group(1)}" color="#176B87">{match.group(1)}</link>',
        escaped,
    )
    return escaped


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "DocumentTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=25,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=18,
        ),
        "h2": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13.5,
            leading=17,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=7,
        ),
        "h3": ParagraphStyle(
            "Subsection",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=BLUE,
            spaceBefore=10,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.25,
            leading=13.2,
            textColor=TEXT,
            alignment=TA_LEFT,
            spaceAfter=7,
        ),
        "meta": ParagraphStyle(
            "Metadata",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.25,
            leading=13,
            textColor=MUTED,
            leftIndent=10,
            borderColor=LINE,
            borderWidth=0,
            borderPadding=2,
            spaceAfter=2,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.1,
            leading=12.8,
            textColor=TEXT,
            leftIndent=15,
            firstLineIndent=-8,
            bulletIndent=3,
            spaceAfter=4,
        ),
        "number": ParagraphStyle(
            "Number",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.1,
            leading=12.8,
            textColor=TEXT,
            leftIndent=18,
            firstLineIndent=-13,
            spaceAfter=4,
        ),
        "reference": ParagraphStyle(
            "Reference",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            textColor=MUTED,
            leftIndent=14,
            firstLineIndent=-10,
            spaceAfter=4,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
    }


def parse_markdown(markdown: str) -> list[object]:
    style = styles()
    story: list[object] = []
    paragraph: list[str] = []
    list_item: list[str] = []
    list_bullet = ""
    list_kind = ""
    in_references = False

    def flush() -> None:
        nonlocal list_bullet, list_kind
        if paragraph:
            story.append(Paragraph(inline_markup(" ".join(paragraph)), style["body"]))
            paragraph.clear()
        if list_item:
            target_style = style["reference"] if in_references else style[list_kind]
            prefix = "&#8226;" if list_kind == "bullet" else f"<b>{list_bullet}</b>"
            story.append(
                Paragraph(
                    f"{prefix}&nbsp;&nbsp;{inline_markup(' '.join(list_item))}",
                    target_style,
                )
            )
            list_item.clear()
            list_bullet = ""
            list_kind = ""

    for raw in markdown.splitlines():
        line = raw.rstrip()
        if not line:
            flush()
            continue
        if line.startswith("# "):
            flush()
            story.append(Spacer(1, 0.08 * inch))
            story.append(Paragraph(inline_markup(line[2:]), style["title"]))
            continue
        if line.startswith("## "):
            flush()
            title = line[3:]
            in_references = title == "References"
            story.append(Paragraph(inline_markup(title), style["h2"]))
            continue
        if line.startswith("### "):
            flush()
            story.append(Paragraph(inline_markup(line[4:]), style["h3"]))
            continue
        if line.startswith(
            (
                "**Federal Register document:**",
                "**Docket:**",
                "**Submitted by:**",
                "**Capacity:**",
                "**Date prepared:**",
            )
        ):
            flush()
            story.append(Paragraph(inline_markup(line), style["meta"]))
            continue
        if line.startswith("- "):
            flush()
            list_item.append(line[2:])
            list_bullet = "-"
            list_kind = "bullet"
            continue
        numbered = re.match(r"^(\d+)\.\s+(.*)$", line)
        if numbered:
            flush()
            list_item.append(numbered.group(2))
            list_bullet = f"{numbered.group(1)}."
            list_kind = "number"
            continue
        if list_item:
            list_item.append(line.strip())
            continue
        paragraph.append(line.strip())
    flush()
    return story


def draw_page(canvas: object, document: SimpleDocTemplate) -> None:
    canvas.saveState()
    width, height = letter
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(0.72 * inch, height - 0.55 * inch, width - 0.72 * inch, height - 0.55 * inch)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(NAVY)
    canvas.drawString(0.72 * inch, height - 0.43 * inch, "NIST-2026-0100 | NVD AI Modernization")
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - 0.72 * inch, height - 0.43 * inch, "Goutam Adwant")
    canvas.line(0.72 * inch, 0.52 * inch, width - 0.72 * inch, 0.52 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(width / 2, 0.34 * inch, f"Page {document.page}")
    canvas.restoreState()


def render(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(destination),
        pagesize=letter,
        rightMargin=0.78 * inch,
        leftMargin=0.78 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.68 * inch,
        title="Assertion-Level Provenance and Verifiable AI Enrichment for a Modernized NVD",
        author="Goutam Adwant",
        subject="Response to NIST RFI 2026-16371, docket NIST-2026-0100",
        creator="Standards Radar VEPP response package",
    )
    story = parse_markdown(source.read_text(encoding="utf-8"))
    document.build(story, onFirstPage=draw_page, onLaterPages=draw_page)


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {Path(sys.argv[0]).name} INPUT.md OUTPUT.pdf", file=sys.stderr)
        return 2
    render(Path(sys.argv[1]), Path(sys.argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
