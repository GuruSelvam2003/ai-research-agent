from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime


def export_to_pdf(topic: str, summaries: list, analysis: str, filename: str = None):
    """
    Generate a professional PDF research brief.
    
    Args:
        topic: Research topic string
        summaries: List of dicts with keys: title, published, url, summary
        analysis: String containing themes/gaps analysis
        filename: Output filename (auto-generated if None)
    """
    if filename is None:
        filename = topic.replace(" ", "_") + "_research_brief.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch
    )

    # ── Styles ────────────────────────────────────────────
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=24,
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold"
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#555555"),
        spaceAfter=4,
        alignment=TA_CENTER
    )

    section_header_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading1"],
        fontSize=14,
        textColor=colors.HexColor("#1a1a2e"),
        spaceBefore=16,
        spaceAfter=6,
        fontName="Helvetica-Bold",
        borderPad=4
    )

    paper_title_style = ParagraphStyle(
        "PaperTitle",
        parent=styles["Heading2"],
        fontSize=12,
        textColor=colors.HexColor("#16213e"),
        spaceBefore=12,
        spaceAfter=4,
        fontName="Helvetica-Bold"
    )

    meta_style = ParagraphStyle(
        "Meta",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#777777"),
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#333333"),
        spaceAfter=8,
        leading=15
    )

    analysis_style = ParagraphStyle(
        "Analysis",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#222222"),
        spaceAfter=6,
        leading=16,
        leftIndent=8
    )

    # ── Build Content ─────────────────────────────────────
    story = []

    # Header banner using a table
    header_data = [[
        Paragraph("🔬 AI Research Brief", title_style)
    ]]
    header_table = Table(header_data, colWidths=[6.5 * inch])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1a1a2e")),
        ("ROUNDEDCORNERS", [8]),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
    ]))

    # Override title color for dark background
    title_style.textColor = colors.white
    story.append(header_table)
    story.append(Spacer(1, 0.2 * inch))

    # Topic and date
    story.append(Paragraph(f"Topic: {topic}", ParagraphStyle(
        "TopicStyle",
        parent=styles["Normal"],
        fontSize=13,
        textColor=colors.HexColor("#1a1a2e"),
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        spaceAfter=4
    )))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y')} · {len(summaries)} papers analyzed",
        subtitle_style
    ))
    story.append(Spacer(1, 0.15 * inch))
    story.append(HRFlowable(width="100%", thickness=1.5,
                 color=colors.HexColor("#1a1a2e"), spaceAfter=12))

    # ── Papers Section ────────────────────────────────────
    story.append(Paragraph("📄 Papers Analyzed", section_header_style))
    story.append(HRFlowable(width="100%", thickness=0.5,
                 color=colors.HexColor("#cccccc"), spaceAfter=8))

    for i, s in enumerate(summaries):
        # Paper number badge + title
        story.append(Paragraph(
            f"<b>[{i+1}]</b> {s['title']}", paper_title_style
        ))
        story.append(Paragraph(
            f"Published: {s['published']}  |  URL: {s['url']}", meta_style
        ))

        # Summary box
        summary_data = [[Paragraph(s['summary'], body_style)]]
        summary_table = Table(summary_data, colWidths=[6.3 * inch])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f4f6fb")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#c0c8e0")),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.08 * inch))

    # ── Analysis Section ──────────────────────────────────
    story.append(Spacer(1, 0.1 * inch))
    story.append(HRFlowable(width="100%", thickness=1.5,
                 color=colors.HexColor("#1a1a2e"), spaceAfter=8))
    story.append(Paragraph("🧠 Research Analysis", section_header_style))
    story.append(HRFlowable(width="100%", thickness=0.5,
                 color=colors.HexColor("#cccccc"), spaceAfter=8))

    # Split analysis into paragraphs
    for para in analysis.split("\n"):
        para = para.strip()
        if not para:
            story.append(Spacer(1, 0.05 * inch))
            continue
        if para.startswith("**") or para[0].isdigit():
            story.append(Paragraph(f"<b>{para.replace('**','')}</b>", analysis_style))
        else:
            story.append(Paragraph(para, analysis_style))

    # ── Footer ────────────────────────────────────────────
    story.append(Spacer(1, 0.3 * inch))
    story.append(HRFlowable(width="100%", thickness=0.5,
                 color=colors.HexColor("#cccccc"), spaceAfter=6))
    story.append(Paragraph(
        "Generated by AI Research Agent · Built with LLaMA 3.2 + ArXiv API",
        ParagraphStyle("Footer", parent=styles["Normal"],
                      fontSize=8, textColor=colors.HexColor("#aaaaaa"),
                      alignment=TA_CENTER)
    ))

    # ── Build PDF ─────────────────────────────────────────
    doc.build(story)
    print(f"✅ PDF saved to {filename}")
    return filename
