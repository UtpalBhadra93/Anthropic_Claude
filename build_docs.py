"""
build_docs.py
─────────────
Generates the full technical documentation PDF for NovaTel AI Agent.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, ListFlowable, ListItem,
    Preformatted
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
import datetime

# ── Colour Palette ────────────────────────────────────────────────────────
DEEP_BLUE     = colors.HexColor("#0D1B2A")
BRAND_BLUE    = colors.HexColor("#1565C0")
LIGHT_BLUE    = colors.HexColor("#1E88E5")
ACCENT_CYAN   = colors.HexColor("#00ACC1")
LIGHT_BG      = colors.HexColor("#F0F4F8")
CODE_BG       = colors.HexColor("#1E1E2E")
CODE_FG       = colors.HexColor("#CDD6F4")
ACCENT_GREEN  = colors.HexColor("#2E7D32")
ACCENT_ORANGE = colors.HexColor("#E65100")
ACCENT_RED    = colors.HexColor("#B71C1C")
MUTED_GREY    = colors.HexColor("#546E7A")
WHITE         = colors.white
BORDER_GREY   = colors.HexColor("#CFD8DC")
SECTION_LINE  = colors.HexColor("#90CAF9")

PAGE_W, PAGE_H = A4
MARGIN = 2.2 * cm


# ── Custom Page Template ──────────────────────────────────────────────────
class DocTemplate(SimpleDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=MARGIN,
            rightMargin=MARGIN,
            topMargin=2.8 * cm,
            bottomMargin=2.5 * cm,
            title="NovaTel AI Agent — Technical Documentation",
            author="Anthropic / AWS Bedrock",
        )
        self.page_number = 0

    def handle_pageBegin(self):
        self.page_number += 1
        super().handle_pageBegin()

    def build(self, flowables):
        super().build(flowables, onFirstPage=self._first_page, onLaterPages=self._later_pages)

    @staticmethod
    def _header_footer(c: canvas.Canvas, doc, show_header=True):
        c.saveState()
        w, h = A4

        # ── Header bar ──
        if show_header:
            c.setFillColor(DEEP_BLUE)
            c.rect(0, h - 1.8 * cm, w, 1.8 * cm, fill=1, stroke=0)
            c.setFillColor(ACCENT_CYAN)
            c.rect(0, h - 1.8 * cm, 0.6 * cm, 1.8 * cm, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(WHITE)
            c.drawString(1.0 * cm, h - 1.1 * cm, "NovaTel AI Agent")
            c.setFont("Helvetica", 8)
            c.setFillColor(colors.HexColor("#90CAF9"))
            c.drawRightString(w - 1.5 * cm, h - 1.1 * cm, "Technical Documentation  |  v1.0.0")

        # ── Footer bar ──
        c.setFillColor(LIGHT_BG)
        c.rect(0, 0, w, 1.8 * cm, fill=1, stroke=0)
        c.setStrokeColor(BRAND_BLUE)
        c.setLineWidth(0.4)
        c.line(MARGIN, 1.8 * cm, w - MARGIN, 1.8 * cm)

        c.setFont("Helvetica", 7.5)
        c.setFillColor(MUTED_GREY)
        c.drawString(MARGIN, 0.8 * cm, "Powered by Claude on AWS Bedrock  ·  NovaTel Telecom AI")
        c.drawRightString(w - MARGIN, 0.8 * cm, f"Page {doc.page}")
        c.restoreState()

    @classmethod
    def _first_page(cls, c, doc):
        cls._header_footer(c, doc, show_header=False)

    @classmethod
    def _later_pages(cls, c, doc):
        cls._header_footer(c, doc, show_header=True)

1.0
# ── Styles ────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    def s(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        "cover_title": s("cover_title",
            fontName="Helvetica-Bold", fontSize=38,
            textColor=WHITE, leading=46, alignment=TA_LEFT),

        "cover_sub": s("cover_sub",
            fontName="Helvetica", fontSize=16,
            textColor=colors.HexColor("#90CAF9"), leading=22, alignment=TA_LEFT),

        "cover_meta": s("cover_meta",
            fontName="Helvetica", fontSize=10,
            textColor=colors.HexColor("#B0BEC5"), leading=14, alignment=TA_LEFT),

        "h1": s("h1",
            fontName="Helvetica-Bold", fontSize=20,
            textColor=DEEP_BLUE, leading=26, spaceBefore=22, spaceAfter=8),

        "h2": s("h2",
            fontName="Helvetica-Bold", fontSize=14,
            textColor=BRAND_BLUE, leading=20, spaceBefore=16, spaceAfter=6),

        "h3": s("h3",
            fontName="Helvetica-Bold", fontSize=11,
            textColor=ACCENT_CYAN, leading=16, spaceBefore=12, spaceAfter=4),

        "body": s("body",
            fontName="Helvetica", fontSize=9.5,
            textColor=DEEP_BLUE, leading=15, alignment=TA_JUSTIFY,
            spaceBefore=4, spaceAfter=4),

        "body_sm": s("body_sm",
            fontName="Helvetica", fontSize=8.5,
            textColor=DEEP_BLUE, leading=13, spaceBefore=2, spaceAfter=2),

        "code": s("code",
            fontName="Courier", fontSize=8,
            textColor=CODE_FG, backColor=CODE_BG,
            leading=12, leftIndent=8, rightIndent=8,
            spaceBefore=6, spaceAfter=6),

        "code_inline": s("code_inline",
            fontName="Courier-Bold", fontSize=8.5,
            textColor=BRAND_BLUE, leading=13),

        "caption": s("caption",
            fontName="Helvetica-Oblique", fontSize=8,
            textColor=MUTED_GREY, leading=12,
            alignment=TA_CENTER, spaceBefore=2, spaceAfter=8),

        "note": s("note",
            fontName="Helvetica", fontSize=8.5,
            textColor=colors.HexColor("#1B5E20"),
            backColor=colors.HexColor("#E8F5E9"),
            leading=13, leftIndent=10, rightIndent=10,
            spaceBefore=6, spaceAfter=6, borderPad=6),

        "warning": s("warning",
            fontName="Helvetica", fontSize=8.5,
            textColor=colors.HexColor("#7F3B00"),
            backColor=colors.HexColor("#FFF3E0"),
            leading=13, leftIndent=10, rightIndent=10,
            spaceBefore=6, spaceAfter=6),

        "toc_h1": s("toc_h1",
            fontName="Helvetica-Bold", fontSize=10,
            textColor=BRAND_BLUE, leading=16, leftIndent=0, spaceBefore=4),

        "toc_h2": s("toc_h2",
            fontName="Helvetica", fontSize=9,
            textColor=DEEP_BLUE, leading=14, leftIndent=12),

        "pill": s("pill",
            fontName="Helvetica-Bold", fontSize=7.5,
            textColor=WHITE, leading=10, alignment=TA_CENTER),

        "list_item": s("list_item",
            fontName="Helvetica", fontSize=9.5,
            textColor=DEEP_BLUE, leading=14,
            leftIndent=12, spaceBefore=2, spaceAfter=2),
    }


S = make_styles()
CONTENT_W = PAGE_W - 2 * MARGIN


# ── Reusable Components ───────────────────────────────────────────────────
def hline(color=SECTION_LINE, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceAfter=6, spaceBefore=6)

def spacer(h=0.3):
    return Spacer(1, h * cm)

def section_header(title, icon=""):
    return KeepTogether([
        hline(BRAND_BLUE, 1.5),
        Paragraph(f"{icon}  {title}" if icon else title, S["h1"]),
        hline(SECTION_LINE, 0.4),
    ])

def sub_header(title):
    return Paragraph(title, S["h2"])

def sub_sub_header(title):
    return Paragraph(title, S["h3"])

def body(text):
    return Paragraph(text, S["body"])

def note_box(text):
    return Paragraph(f"<b>&#x2139;</b>  {text}", S["note"])

def warning_box(text):
    return Paragraph(f"<b>&#x26A0;</b>  {text}", S["warning"])

def code_block(text):
    return Preformatted(text, S["code"])

def bullet_list(items):
    return ListFlowable(
        [ListItem(Paragraph(i, S["list_item"]), leftIndent=20, bulletColor=BRAND_BLUE) for i in items],
        bulletType="bullet", start="•", leftIndent=12
    )

def make_table(data, col_widths, header_bg=BRAND_BLUE, stripe=True):
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        ("TOPPADDING", (0, 0), (-1, 0), 7),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 8.5),
        ("ALIGN", (0, 1), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 1), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER_GREY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [WHITE, colors.HexColor("#F8FAFC")] if stripe else [WHITE]),
    ]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


# ══════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════════════════════════════════════════
def cover_page():
    story = []

    # Full-bleed cover simulation with a tall table
    cover_data = [[""]]
    cover_table = Table(cover_data, colWidths=[CONTENT_W], rowHeights=[10.5 * cm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DEEP_BLUE),
        ("LINEBELOW", (0, 0), (-1, -1), 4, ACCENT_CYAN),
    ]))
    story.append(spacer(0.2))
    story.append(cover_table)

    # Overlay content manually via a follow-up block
    header_content = [
        [Paragraph("NovaTel AI Agent", S["cover_title"])],
        [Paragraph("Technical Documentation", S["cover_sub"])],
        [spacer(0.25)],
        [Paragraph("Agentic Telecom Support Platform  ·  Claude on AWS Bedrock", S["cover_meta"])],
        [Paragraph(f"Version 1.0.0  ·  {datetime.date.today().strftime('%B %Y')}", S["cover_meta"])],
    ]
    overlay = Table(header_content, colWidths=[CONTENT_W])
    overlay.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DEEP_BLUE),
        ("TOPPADDING", (0, 0), (0, 0), 18),
        ("BOTTOMPADDING", (0, -1), (0, -1), 20),
        ("LEFTPADDING", (0, 0), (-1, -1), 22),
        ("RIGHTPADDING", (0, 0), (-1, -1), 22),
        ("LINEBELOW", (0, -1), (-1, -1), 3, ACCENT_CYAN),
    ]))
    # Replace the spacer table with the overlay
    story[-1] = overlay

    story.append(spacer(0.6))

    # Feature badges row
    badge_data = [[
        Paragraph("AGENTIC CHAT", S["pill"]),
        Paragraph("TOOL USE", S["pill"]),
        Paragraph("RAG PIPELINE", S["pill"]),
        Paragraph("KAFKA EVENTS", S["pill"]),
        Paragraph("REST API", S["pill"]),
    ]]
    badge_colors = [BRAND_BLUE, ACCENT_CYAN, ACCENT_GREEN, ACCENT_ORANGE, MUTED_GREY]
    badge_widths = [CONTENT_W / 5] * 5
    badge_table = Table(badge_data, colWidths=badge_widths)
    badge_table.setStyle(TableStyle([
        ("BACKGROUND", (i, 0), (i, 0), badge_colors[i]) for i in range(5)
    ] + [
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BORDERPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(badge_table)
    story.append(spacer(0.7))

    # Abstract
    abstract_data = [[Paragraph(
        "This document provides complete technical documentation for the <b>NovaTel AI Agent</b> — "
        "a production-ready, agentic customer support platform built on <b>Claude 3.5 Sonnet</b> "
        "via <b>AWS Bedrock</b>. It covers system architecture, the four integrated tools, "
        "the RAG knowledge pipeline, Kafka event streaming, REST API reference, testing strategy, "
        "and deployment instructions. The implementation follows patterns taught in the "
        "<i>Anthropic Claude in Amazon Bedrock</i> course.",
        S["body"]
    )]]
    abstract_table = Table(abstract_data, colWidths=[CONTENT_W])
    abstract_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("LINEAFTER", (0, 0), (0, -1), 3, ACCENT_CYAN),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(abstract_table)
    story.append(spacer(0.5))

    # Meta info grid
    meta = [
        ["Project", "NovaTel AI Agent"],
        ["Version", "1.0.0"],
        ["AI Model", "Claude 3.5 Sonnet (anthropic.claude-3-5-sonnet-20241022-v2:0)"],
        ["Platform", "AWS Bedrock Converse API"],
        ["Language", "Python 3.11+"],
        ["Framework", "FastAPI  ·  Pydantic  ·  structlog"],
        ["Date", datetime.date.today().strftime("%d %B %Y")],
    ]
    meta_table = Table(
        [[Paragraph(f"<b>{k}</b>", S["body_sm"]), Paragraph(v, S["body_sm"])] for k, v in meta],
        colWidths=[4 * cm, CONTENT_W - 4 * cm]
    )
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, BORDER_GREY),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, LIGHT_BG]),
    ]))
    story.append(meta_table)
    story.append(PageBreak())
    return story


# ══════════════════════════════════════════════════════════════════════════
# TABLE OF CONTENTS
# ══════════════════════════════════════════════════════════════════════════
def table_of_contents():
    story = [section_header("Table of Contents"), spacer(0.3)]

    toc_entries = [
        ("1", "System Overview", [
            ("1.1", "Introduction & Goals"),
            ("1.2", "Technology Stack"),
            ("1.3", "Key Features"),
        ]),
        ("2", "Architecture", [
            ("2.1", "High-Level Architecture"),
            ("2.2", "Project Structure"),
            ("2.3", "Component Interactions"),
        ]),
        ("3", "Configuration & Setup", [
            ("3.1", "Environment Variables (.env)"),
            ("3.2", "Installation"),
            ("3.3", "Running the Application"),
        ]),
        ("4", "The Four Tools", [
            ("4.1", "Tool 1: Kafka Event Publisher"),
            ("4.2", "Tool 2: Account Lookup"),
            ("4.3", "Tool 3: Network Diagnostics"),
            ("4.4", "Tool 4: Plan Management"),
        ]),
        ("5", "Agentic Chat Loop", [
            ("5.1", "How the Agent Works"),
            ("5.2", "System Prompt Design"),
            ("5.3", "Session Management"),
            ("5.4", "Tool Orchestration Flow"),
        ]),
        ("6", "RAG Pipeline", [
            ("6.1", "Knowledge Base"),
            ("6.2", "Chunking Strategy"),
            ("6.3", "Hybrid Retrieval (BM25 + TF-IDF + RRF)"),
        ]),
        ("7", "Kafka Integration", [
            ("7.1", "Event Architecture"),
            ("7.2", "Topics & Event Types"),
            ("7.3", "Graceful Degradation"),
        ]),
        ("8", "REST API Reference", [
            ("8.1", "Endpoints Overview"),
            ("8.2", "Chat Endpoints"),
            ("8.3", "Account, Network & Plan Endpoints"),
        ]),
        ("9", "Testing", [
            ("9.1", "Test Strategy"),
            ("9.2", "Test Coverage"),
            ("9.3", "Running Tests"),
        ]),
        ("10", "Deployment", [
            ("10.1", "Docker Compose"),
            ("10.2", "Production Checklist"),
        ]),
    ]

    for num, title, subs in toc_entries:
        row_data = [[
            Paragraph(f"<b>{num}</b>", S["toc_h1"]),
            Paragraph(f"<b>{title}</b>", S["toc_h1"]),
        ]]
        t = Table(row_data, colWidths=[1.2 * cm, CONTENT_W - 1.2 * cm])
        t.setStyle(TableStyle([
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LINEBELOW", (0, 0), (-1, 0), 0.3, colors.HexColor("#BBDEFB")),
        ]))
        story.append(t)
        for s_num, s_title in subs:
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{s_num}&nbsp;&nbsp;{s_title}", S["toc_h2"]))
        story.append(spacer(0.1))

    story.append(PageBreak())
    return story


# ══════════════════════════════════════════════════════════════════════════
# SECTION 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════
def section_overview():
    story = [section_header("1.  System Overview")]

    story += [
        sub_header("1.1  Introduction & Goals"),
        body(
            "The <b>NovaTel AI Agent</b> is an intelligent, agentic customer support platform "
            "for a fictitious telecommunications company — NovaTel. The system is built around "
            "<b>Anthropic Claude 3.5 Sonnet</b> accessed via the <b>AWS Bedrock Converse API</b>, "
            "and implements the complete agentic architecture pattern taught in the "
            "<i>Anthropic Claude in Amazon Bedrock</i> course."
        ),
        body(
            "The agent — named <b>Aria</b> — can hold multi-turn customer support conversations, "
            "autonomously call tools to look up account data, diagnose network issues, manage "
            "service plans, and stream all customer interaction events to Apache Kafka for downstream "
            "processing and analytics."
        ),
        spacer(0.2),
        sub_header("1.2  Technology Stack"),
    ]

    stack_data = [
        ["Layer", "Technology", "Purpose"],
        ["AI Model", "Claude 3.5 Sonnet\n(AWS Bedrock)", "Core language model for reasoning & NLU"],
        ["API Access", "AWS Bedrock Converse API", "Multi-turn chat, tool use, streaming"],
        ["Application", "Python 3.11 + FastAPI", "REST API server with SSE streaming"],
        ["Configuration", "Pydantic-Settings + .env", "Type-safe environment configuration"],
        ["Event Bus", "Apache Kafka", "Async event publishing for all interactions"],
        ["Knowledge Base", "BM25 + TF-IDF (RAG)", "Hybrid retrieval over telecom KB docs"],
        ["Logging", "structlog", "Structured JSON logging in production"],
        ["Testing", "pytest + httpx + moto", "Unit, integration & mock-AWS tests"],
        ["Container", "Docker + docker-compose", "Reproducible deployment with Kafka"],
    ]
    story.append(make_table(stack_data,
        [3.2 * cm, 4.5 * cm, CONTENT_W - 7.7 * cm]))
    story.append(spacer(0.3))
    story.append(sub_header("1.3  Key Features"))

    feat_data = [
        ["Feature", "Description", "Status"],
        ["Agentic Chat Loop", "Multi-turn, multi-tool conversation with Claude", "Implemented"],
        ["Tool Use (4 tools)", "JSON-Schema tools dispatched automatically by Claude", "Implemented"],
        ["Kafka Integration", "Event publishing with graceful degradation", "Implemented"],
        ["RAG Pipeline", "BM25 + TF-IDF hybrid retrieval with RRF scoring", "Implemented"],
        ["Streaming Responses", "Server-Sent Events (SSE) token streaming", "Implemented"],
        ["Session Management", "Stateful multi-turn sessions with history", "Implemented"],
        ["REST API", "10 FastAPI endpoints with OpenAPI docs", "Implemented"],
        ["Test Suite", "5 test files, ~55 tests, 70%+ coverage target", "Implemented"],
        ["Docker Deployment", "Kafka + Kafka UI + Agent via docker-compose", "Implemented"],
        ["Retry Logic", "Exponential back-off via tenacity for Bedrock", "Implemented"],
    ]
    story.append(make_table(feat_data,
        [4.5 * cm, CONTENT_W - 7.5 * cm, 3.0 * cm]))
    story.append(PageBreak())
    return story


# ══════════════════════════════════════════════════════════════════════════
# SECTION 2 — ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════
def section_architecture():
    story = [section_header("2.  Architecture")]

    story += [
        sub_header("2.1  High-Level Architecture"),
        body(
            "The application follows a layered architecture with clear separation between "
            "the API layer, the agent orchestration layer, individual tool implementations, "
            "and the knowledge retrieval system."
        ),
        spacer(0.2),
    ]

    # Architecture diagram (drawn as a styled table)
    arch = [
        [Paragraph("<b>CLIENT</b>", S["pill"]),
         Paragraph("HTTP/SSE requests", S["body_sm"])],
        ["", Paragraph("▼", S["body_sm"])],
        [Paragraph("<b>FastAPI REST API</b>", S["pill"]),
         Paragraph("/api/v1/* endpoints · OpenAPI docs", S["body_sm"])],
        ["", Paragraph("▼", S["body_sm"])],
        [Paragraph("<b>TelecomAgent (Aria)</b>", S["pill"]),
         Paragraph("Agentic loop · Session mgmt · Prompt engineering", S["body_sm"])],
        ["", Paragraph("▼  ▼  ▼  ▼", S["body_sm"])],
    ]
    arch_t = Table(arch, colWidths=[4.5*cm, CONTENT_W - 4.5*cm])
    arch_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), BRAND_BLUE),
        ("BACKGROUND", (0, 2), (0, 2), ACCENT_CYAN),
        ("BACKGROUND", (0, 4), (0, 4), DEEP_BLUE),
        ("TEXTCOLOR", (0, 0), (0, 0), WHITE),
        ("TEXTCOLOR", (0, 2), (0, 2), WHITE),
        ("TEXTCOLOR", (0, 4), (0, 4), WHITE),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (1, 0), (1, -1), 10),
    ]))
    story.append(arch_t)

    # Tools row
    tools_data = [[
        Paragraph("<b>Kafka\nPublish</b>", S["pill"]),
        Paragraph("<b>Account\nLookup</b>", S["pill"]),
        Paragraph("<b>Network\nDiag.</b>", S["pill"]),
        Paragraph("<b>Plan\nMgmt</b>", S["pill"]),
    ]]
    tool_colors = [ACCENT_ORANGE, BRAND_BLUE, ACCENT_GREEN, MUTED_GREY]
    tw = CONTENT_W / 4
    tools_t = Table(tools_data, colWidths=[tw, tw, tw, tw])
    tools_t.setStyle(TableStyle([
        ("BACKGROUND", (i, 0), (i, 0), tool_colors[i]) for i in range(4)
    ] + [
        ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(tools_t)
    story.append(spacer(0.1))

    # Infrastructure row
    infra_data = [[
        Paragraph("<b>AWS Bedrock\n(Claude 3.5)</b>", S["pill"]),
        Paragraph("<b>Apache\nKafka</b>", S["pill"]),
        Paragraph("<b>RAG\nRetriever</b>", S["pill"]),
    ]]
    infra_colors = [BRAND_BLUE, ACCENT_ORANGE, ACCENT_CYAN]
    iw = CONTENT_W / 3
    infra_t = Table(infra_data, colWidths=[iw, iw, iw])
    infra_t.setStyle(TableStyle([
        ("BACKGROUND", (i, 0), (i, 0), infra_colors[i]) for i in range(3)
    ] + [
        ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(infra_t)
    story.append(Paragraph("Figure 1: High-level system architecture", S["caption"]))
    story.append(spacer(0.3))

    story.append(sub_header("2.2  Project Structure"))
    story.append(code_block(
"""telecom-ai-agent/
├── .env / .env.example         # Environment variables & API keys
├── main.py                     # Application entry point (uvicorn)
├── Dockerfile + docker-compose.yml
├── requirements.txt + pyproject.toml
│
├── src/
│   ├── config.py               # Pydantic-Settings (.env loader)
│   ├── logger.py               # structlog (JSON/console)
│   ├── agent/
│   │   ├── claude_client.py    # AWS Bedrock Converse API wrapper
│   │   ├── agent.py            # TelecomAgent — agentic loop
│   │   └── tools.py            # JSON-Schema tool definitions (4 tools)
│   ├── tools/
│   │   ├── __init__.py         # execute_tool() dispatcher
│   │   ├── kafka_tool.py       # ① Kafka publish / consume
│   │   ├── account_tool.py     # ② Customer account lookup
│   │   ├── network_tool.py     # ③ Network status & outages
│   │   └── plan_tool.py        # ④ Plan listing & changes
│   ├── rag/
│   │   ├── knowledge_base.py   # 5 NovaTel KB articles
│   │   └── retriever.py        # Hybrid BM25+TF-IDF+RRF retriever
│   └── api/
│       ├── app.py              # FastAPI factory + CORS middleware
│       └── routes.py           # 10 REST endpoints + SSE streaming
│
└── tests/
    ├── conftest.py             # Mock Bedrock fixtures
    ├── test_tools.py           # ~25 tool tests
    ├── test_agent.py           # Agentic loop tests
    ├── test_rag.py             # RAG pipeline tests
    ├── test_api.py             # FastAPI integration tests
    └── test_config.py          # Config loading tests"""))

    story.append(spacer(0.3))
    story.append(sub_header("2.3  Component Interactions"))
    body_text = (
        "When a user sends a message, it flows through the following sequence: "
        "(1) The FastAPI route handler receives the HTTP request and resolves or creates a chat session. "
        "(2) The <b>TelecomAgent</b> appends the user message to session history and calls "
        "<b>ClaudeBedrockClient.converse()</b> with the full message history, system prompt, and tool schemas. "
        "(3) Claude analyses the request. If it needs data, it returns a <code>tool_use</code> stop reason "
        "with a tool name and input arguments. "
        "(4) The <b>execute_tool()</b> dispatcher calls the appropriate Python function and returns the result. "
        "(5) The tool result is appended to history as a <code>toolResult</code> message, and the loop repeats. "
        "(6) When Claude has sufficient context, it returns an <code>end_turn</code> response. "
        "(7) The agent publishes a <code>SUPPORT_INTERACTION_COMPLETED</code> event to Kafka before "
        "returning the final text to the API caller."
    )
    story.append(body(body_text))
    story.append(PageBreak())
    return story


# ══════════════════════════════════════════════════════════════════════════
# SECTION 3 — CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════
def section_config():
    story = [section_header("3.  Configuration & Setup")]

    story += [
        sub_header("3.1  Environment Variables (.env)"),
        body(
            "All configuration is managed through a <code>.env</code> file loaded by "
            "<b>Pydantic-Settings</b>. Copy <code>.env.example</code> to <code>.env</code> "
            "and populate the required values. The file is excluded from version control via "
            "<code>.gitignore</code>."
        ),
        spacer(0.15),
    ]

    env_data = [
        ["Variable", "Required", "Default", "Description"],
        ["AWS_ACCESS_KEY_ID", "Yes*", "—", "AWS IAM access key"],
        ["AWS_SECRET_ACCESS_KEY", "Yes*", "—", "AWS IAM secret key"],
        ["AWS_REGION", "Yes", "us-east-1", "AWS region for Bedrock"],
        ["BEDROCK_MODEL_ID", "No", "claude-3-5-sonnet-\n20241022-v2:0", "Claude model identifier"],
        ["ANTHROPIC_API_KEY", "No", "—", "Direct Anthropic API (fallback/testing)"],
        ["KAFKA_BOOTSTRAP_SERVERS", "No", "localhost:9092", "Kafka broker address(es)"],
        ["KAFKA_TOPIC_EVENTS", "No", "telecom.customer.events", "Customer events topic"],
        ["KAFKA_TOPIC_ALERTS", "No", "telecom.network.alerts", "Network alerts topic"],
        ["KAFKA_CONSUMER_GROUP", "No", "telecom-ai-agent", "Kafka consumer group ID"],
        ["APP_ENV", "No", "development", "Environment: development/production"],
        ["APP_PORT", "No", "8000", "HTTP server port"],
        ["LOG_LEVEL", "No", "INFO", "Logging level"],
        ["API_SECRET_KEY", "Yes", "—", "Secret for API security"],
        ["ALLOWED_ORIGINS", "No", "http://localhost:3000", "CORS allowed origins (comma-sep)"],
    ]
    story.append(make_table(env_data,
        [5.2 * cm, 1.8 * cm, 3.5 * cm, CONTENT_W - 10.5 * cm]))
    story.append(Paragraph("* Use IAM roles in production instead of static credentials.", S["caption"]))

    story += [
        spacer(0.3),
        sub_header("3.2  Installation"),
        code_block(
"""# 1. Clone the repository
git clone https://github.com/your-org/telecom-ai-agent.git
cd telecom-ai-agent

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\\Scripts\\activate.bat      # Windows

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, API_SECRET_KEY

# 5. (Optional) Start Kafka with Docker
docker-compose up kafka kafka-ui -d"""),

        spacer(0.2),
        sub_header("3.3  Running the Application"),
        code_block(
"""# Development mode (hot-reload)
python main.py

# Or directly with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Full stack with Docker Compose
docker-compose up --build

# Endpoints
# API:       http://localhost:8000
# Docs:      http://localhost:8000/docs (Swagger UI)
# Kafka UI:  http://localhost:8080"""),

        note_box(
            "Enable Claude model access in AWS Bedrock console before first run: "
            "AWS Console → Amazon Bedrock → Model access → Request access for Claude 3.5 Sonnet."
        ),
        PageBreak(),
    ]
    return story


# ══════════════════════════════════════════════════════════════════════════
# SECTION 4 — THE FOUR TOOLS
# ══════════════════════════════════════════════════════════════════════════
def section_tools():
    story = [section_header("4.  The Four Tools")]

    story.append(body(
        "Claude interacts with the application through four <b>JSON-Schema defined tools</b>. "
        "These are passed to the Bedrock Converse API on every turn. When Claude determines "
        "it needs external data, it emits a <code>tool_use</code> block; the agent calls "
        "<code>execute_tool()</code> and returns the result as a <code>toolResult</code> message."
    ))
    story.append(spacer(0.2))

    # ── Tool 1: Kafka ──────────────────────────────────────────────────────
    story.append(KeepTogether([
        sub_header("4.1  Tool 1: kafka_publish_event  🔴"),
        body("Publishes a structured event envelope to a Kafka topic."),
    ]))

    story.append(make_table(
        [["Parameter", "Type", "Required", "Description"],
         ["topic", "string (enum)", "Yes", "Target topic: customer.events / network.alerts / billing.events"],
         ["event_type", "string", "Yes", "Event label, e.g. SUPPORT_TICKET_CREATED"],
         ["payload", "object", "Yes", "Free-form JSON payload for the event"],
         ["customer_id", "string", "No", "Customer ID to tag the event"],
        ],
        [3.5*cm, 2.8*cm, 2.0*cm, CONTENT_W - 8.3*cm]))

    story.append(spacer(0.1))
    story.append(code_block(
"""# Event envelope published to Kafka
{
  "event_id":    "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "event_type":  "SUPPORT_INTERACTION_COMPLETED",
  "source":      "novotel-ai-agent",
  "timestamp":   "2025-02-25T14:30:00Z",
  "customer_id": "CUST-10001",
  "payload": {
    "session_id": "...",
    "tool_calls": 2,
    "message_count": 6
  }
}"""))
    story.append(note_box(
        "Graceful degradation: if Kafka is unavailable, the event is logged locally "
        "and a degraded=true flag is returned. The agent continues without interruption."
    ))
    story.append(spacer(0.2))

    # ── Tool 2: Account ────────────────────────────────────────────────────
    story.append(KeepTogether([
        sub_header("4.2  Tool 2: get_account_info  👤"),
        body("Retrieves a NovaTel customer account — plan, billing status, usage, and services."),
    ]))
    story.append(make_table(
        [["Parameter", "Type", "Required", "Description"],
         ["customer_id", "string", "Either/Or", "Customer account ID (CUST-XXXXX)"],
         ["phone_number", "string", "Either/Or", "Phone number in E.164 format (+15551234567)"],
         ["include_usage", "boolean", "No", "Include data/call/SMS usage stats (default: true)"],
        ],
        [3.5*cm, 2.5*cm, 2.2*cm, CONTENT_W - 8.2*cm]))
    story.append(spacer(0.2))

    # ── Tool 3: Network ────────────────────────────────────────────────────
    story.append(KeepTogether([
        sub_header("4.3  Tool 3: check_network_status  📡"),
        body("Returns real-time network health for a given area, including active incidents and signal quality."),
    ]))
    story.append(make_table(
        [["Parameter", "Type", "Required", "Description"],
         ["zip_code", "string", "Either/Or", "5-digit US ZIP code"],
         ["customer_id", "string", "Either/Or", "Auto-resolves ZIP from account address"],
         ["service_type", "enum", "No", "mobile / home_internet / business / all (default)"],
        ],
        [3.5*cm, 2.5*cm, 2.2*cm, CONTENT_W - 8.2*cm]))

    story.append(spacer(0.1))
    story.append(make_table(
        [["Severity", "overall_status", "Meaning"],
         ["—", "operational", "No incidents — all services normal"],
         ["low", "degraded", "Minor issues, no major impact"],
         ["medium", "partial_outage", "Some services affected"],
         ["high", "major_outage", "Significant outage impacting many customers"],
        ],
        [3*cm, 3.5*cm, CONTENT_W - 6.5*cm]))
    story.append(spacer(0.2))

    # ── Tool 4: Plan ───────────────────────────────────────────────────────
    story.append(KeepTogether([
        sub_header("4.4  Tool 4: manage_plan  📋"),
        body("Lists NovaTel plans or processes a plan change for a customer."),
    ]))
    story.append(make_table(
        [["Action", "Required Params", "Description"],
         ["list_plans", "—", "Returns all 4 plans with pricing and features"],
         ["get_plan_details", "plan_id", "Returns full details for a specific plan"],
         ["change_plan", "customer_id, plan_id", "Processes plan upgrade or downgrade"],
        ],
        [3.8*cm, 4.2*cm, CONTENT_W - 8*cm]))
    story.append(spacer(0.15))
    story.append(make_table(
        [["Plan ID", "Name", "Price/mo", "Data", "Hotspot", "Category"],
         ["PLAN-BASIC-5G", "Basic 5G", "$35", "5 GB", "—", "Consumer"],
         ["PLAN-STANDARD-5G", "Standard 5G", "$55", "20 GB", "10 GB", "Consumer"],
         ["PLAN-UNLIMITED-PRO", "Unlimited Pro", "$75", "Unlimited", "50 GB", "Consumer"],
         ["PLAN-BUSINESS-ELITE", "Business Elite", "$150", "Unlimited", "100 GB", "Business"],
        ],
        [3.8*cm, 3.2*cm, 1.8*cm, 2.0*cm, 2.0*cm, CONTENT_W - 12.8*cm]))
    story.append(PageBreak())
    return story


# ══════════════════════════════════════════════════════════════════════════
# SECTION 5 — AGENTIC CHAT
# ══════════════════════════════════════════════════════════════════════════
def section_agent():
    story = [section_header("5.  Agentic Chat Loop")]

    story += [
        sub_header("5.1  How the Agent Works"),
        body(
            "The <b>TelecomAgent</b> implements the standard Anthropic agentic loop pattern. "
            "It maintains a <b>ChatSession</b> object holding the full conversation history "
            "and iterates until Claude returns a final <code>end_turn</code> response or the "
            "maximum iteration limit is reached."
        ),
        spacer(0.2),
    ]

    # Flow diagram as table
    flow_data = [
        [Paragraph("<b>Step</b>", S["body_sm"]),
         Paragraph("<b>Action</b>", S["body_sm"]),
         Paragraph("<b>stop_reason</b>", S["body_sm"])],
        ["1", "User message appended to session history", "—"],
        ["2", "ClaudeBedrockClient.converse() called\nwith messages + tools", "—"],
        ["3a", "Claude decides to call a tool", "tool_use"],
        ["4", "execute_tool() dispatched → result returned", "—"],
        ["5", "Tool result appended as toolResult message", "—"],
        ["6", "Return to step 2 (loop continues)", "—"],
        ["3b", "Claude has enough context → final text reply", "end_turn"],
        ["7", "Kafka SUPPORT_INTERACTION_COMPLETED event published", "—"],
        ["8", "Final text returned to API caller", "—"],
    ]
    flow_t = Table(flow_data,
        colWidths=[1.5*cm, CONTENT_W - 4.5*cm, 3.0*cm], repeatRows=1)
    flow_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DEEP_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER_GREY),
        ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#E3F2FD")),
        ("BACKGROUND", (0, 7), (-1, 7), colors.HexColor("#E8F5E9")),
        ("BACKGROUND", (0, 6), (-1, 6), colors.HexColor("#FFF3E0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(flow_t)
    story.append(spacer(0.3))

    story += [
        sub_header("5.2  System Prompt Design"),
        body(
            "The system prompt defines <b>Aria</b>'s persona, capabilities, and operating rules. "
            "It follows Anthropic best practices: role definition first, then behavioral guidelines, "
            "then tool usage instructions."
        ),
        code_block(
"""You are Aria, the intelligent virtual assistant for NovaTel — a leading
telecommunications company.

Your role is to help customers with:
• Account enquiries (billing, usage, payments)
• Plan changes (upgrades, downgrades, comparisons)
• Network issues (outages, signal quality, troubleshooting)
• General telecom support

Guidelines:
- Always look up the customer's account before discussing billing or plan changes.
- If there is a network outage affecting the customer, proactively mention it.
- After resolving an issue, publish a Kafka event to log the interaction.
- Use tools in sequence: account info → network check → plan action → Kafka event.

Today's date: {today}"""),

        spacer(0.2),
        sub_header("5.3  Session Management"),
        body(
            "Each chat session is represented by a <b>ChatSession</b> dataclass containing "
            "a UUID session ID, optional customer ID, cumulative message history, and a "
            "tool call counter. Sessions are stored in an in-memory dictionary keyed by "
            "session ID and survive across multiple HTTP requests within the same server process."
        ),

        spacer(0.2),
        sub_header("5.4  Tool Orchestration Flow"),
        body(
            "Claude autonomously decides which tools to call and in what order, based on the "
            "system prompt guidelines. A typical account enquiry follows this sequence:"
        ),
        bullet_list([
            "<b>get_account_info</b> — Claude calls this first to verify the customer and their plan",
            "<b>check_network_status</b> — if the customer mentions connectivity issues",
            "<b>manage_plan</b> — if a plan change is requested (after confirming current plan)",
            "<b>kafka_publish_event</b> — always called at the end to log the interaction",
        ]),
        PageBreak(),
    ]
    return story


# ══════════════════════════════════════════════════════════════════════════
# SECTION 6 — RAG
# ══════════════════════════════════════════════════════════════════════════
def section_rag():
    story = [section_header("6.  RAG Pipeline")]

    story += [
        sub_header("6.1  Knowledge Base"),
        body(
            "The NovaTel knowledge base contains five curated articles covering the most common "
            "customer support topics. Each document has a document ID, title, full text, and "
            "a set of semantic tags used for filtering."
        ),
        spacer(0.1),
    ]

    kb_data = [
        ["Doc ID", "Title", "Topics"],
        ["KB-001", "NovaTel Billing FAQ", "billing, payment, invoice, dispute"],
        ["KB-002", "Plans Overview", "plans, pricing, features, 5G"],
        ["KB-003", "Network Troubleshooting Guide", "network, signal, troubleshooting, internet"],
        ["KB-004", "Number Porting", "porting, number transfer, activation"],
        ["KB-005", "International Roaming", "roaming, international, travel, data passes"],
    ]
    story.append(make_table(kb_data, [2.5*cm, 5*cm, CONTENT_W - 7.5*cm]))
    story.append(spacer(0.3))

    story += [
        sub_header("6.2  Chunking Strategy"),
        body(
            "Documents are split into overlapping text chunks to ensure context continuity "
            "across chunk boundaries. The chunking parameters are configurable via environment "
            "variables:"
        ),
    ]
    story.append(make_table(
        [["Parameter", "Default", "Description"],
         ["CHUNK_SIZE", "512 tokens", "Maximum words per chunk"],
         ["CHUNK_OVERLAP", "50 tokens", "Overlap between consecutive chunks"],
         ["TOP_K_RESULTS", "5", "Number of chunks returned per query"],
        ],
        [3.5*cm, 2.5*cm, CONTENT_W - 6*cm]))

    story += [
        spacer(0.3),
        sub_header("6.3  Hybrid Retrieval (BM25 + TF-IDF + RRF)"),
        body(
            "The retriever combines two complementary ranking algorithms using "
            "<b>Reciprocal Rank Fusion (RRF)</b> to produce a single ranked result set:"
        ),
        bullet_list([
            "<b>BM25 (Okapi BM25)</b>: Sparse keyword-based retrieval. Excellent for exact term matches "
            "and domain-specific vocabulary like plan names and error codes.",
            "<b>TF-IDF cosine similarity</b>: Dense vector similarity capturing semantic overlap "
            "beyond exact keywords. Handles synonyms and paraphrased queries.",
            "<b>Reciprocal Rank Fusion (RRF)</b>: Combines both rank lists using the formula "
            "score = Σ 1/(k + rank), where k=60. RRF is robust and requires no score normalisation.",
        ]),
        spacer(0.1),
        code_block(
"""# RRF scoring formula (k=60)
rrf_score[i] = 1/(60 + bm25_rank[i] + 1) + 1/(60 + tfidf_rank[i] + 1)

# Example for query: "billing payment autopay"
# BM25 top result:  KB-001 (Billing FAQ)  → rank 0
# TF-IDF top result: KB-001               → rank 0
# Combined RRF:      score = 0.016 + 0.016 = 0.032  ← highest score"""),
        PageBreak(),
    ]
    return story


# ══════════════════════════════════════════════════════════════════════════
# SECTION 7 — KAFKA
# ══════════════════════════════════════════════════════════════════════════
def section_kafka():
    story = [section_header("7.  Kafka Integration")]

    story += [
        sub_header("7.1  Event Architecture"),
        body(
            "NovaTel uses Apache Kafka as its event backbone. The AI agent publishes events "
            "for every significant customer interaction, enabling downstream systems to build "
            "analytics dashboards, trigger billing workflows, escalate support tickets, and "
            "monitor network health in real time."
        ),
        spacer(0.2),
        sub_header("7.2  Topics & Event Types"),
    ]

    topics_data = [
        ["Topic", "Event Types", "Consumers"],
        ["telecom.customer.events",
         "SUPPORT_INTERACTION_COMPLETED\nPLAN_CHANGE_REQUESTED\nACCOUNT_LOOKUP",
         "Analytics, CRM, Audit log"],
        ["telecom.network.alerts",
         "NETWORK_OUTAGE_DETECTED\nMAINTENANCE_SCHEDULED\nSIGNAL_DEGRADED",
         "NOC dashboard, PagerDuty"],
        ["telecom.billing.events",
         "PAYMENT_DUE\nPAYMENT_OVERDUE\nPLAN_CHANGED",
         "Billing system, email service"],
    ]
    story.append(make_table(topics_data, [5*cm, 5.5*cm, CONTENT_W - 10.5*cm]))
    story.append(spacer(0.2))

    story += [
        sub_header("7.3  Graceful Degradation"),
        body(
            "The Kafka publisher is designed to never block the agent. If the Kafka broker "
            "is unavailable (e.g., in development or during broker restart), the tool:"
        ),
        bullet_list([
            "Catches the <code>NoBrokersAvailable</code> exception",
            "Logs the event locally via structlog with a warning level",
            "Returns <code>{ \"success\": true, \"degraded\": true }</code>",
            "The agent continues processing — the customer experience is unaffected",
        ]),
        code_block(
"""# Graceful degradation response
{
  "success": true,
  "degraded": true,
  "event_id": "f47ac10b-...",
  "topic": "telecom.customer.events",
  "message": "Kafka unavailable – event logged locally."
}"""),
        warning_box(
            "In production, ensure Kafka health monitoring and alerting is configured. "
            "Degraded mode means events are NOT persisted — fix broker connectivity promptly."
        ),
        PageBreak(),
    ]
    return story


# ══════════════════════════════════════════════════════════════════════════
# SECTION 8 — API REFERENCE
# ══════════════════════════════════════════════════════════════════════════
def section_api():
    story = [section_header("8.  REST API Reference")]

    story += [
        body(
            "The REST API is built with <b>FastAPI</b> and exposes ten endpoints. "
            "Interactive Swagger UI documentation is available at <code>http://localhost:8000/docs</code>. "
            "All endpoints are prefixed with <code>/api/v1</code>."
        ),
        spacer(0.2),
        sub_header("8.1  Endpoints Overview"),
    ]

    endpoints_data = [
        ["Method", "Path", "Description", "Auth"],
        ["GET", "/health", "Service health check", "No"],
        ["POST", "/chat", "Agentic chat (stateful, multi-turn)", "No"],
        ["POST", "/chat/stream", "Streaming chat — SSE token stream", "No"],
        ["POST", "/rag/search", "Search knowledge base (BM25+TF-IDF)", "No"],
        ["GET", "/tools", "List available Claude tools", "No"],
        ["GET", "/account/{id}", "Get customer account details", "No"],
        ["GET", "/network/status", "Check network status and outages", "No"],
        ["GET", "/plans", "List all service plans", "No"],
        ["POST", "/plans/change", "Change customer service plan", "No"],
        ["POST", "/kafka/publish", "Manually publish a Kafka event", "No"],
    ]
    story.append(make_table(endpoints_data, [1.8*cm, 4.2*cm, CONTENT_W - 8*cm, 2*cm]))
    story.append(spacer(0.3))

    story += [
        sub_header("8.2  Chat Endpoints"),
        sub_sub_header("POST /api/v1/chat — Agentic Chat"),
        body("Send a message to the NovaTel AI agent. Maintains session state across calls."),
        spacer(0.1),
        code_block(
"""# Request
POST /api/v1/chat
{
  "message": "I want to upgrade my plan",
  "session_id": "optional-uuid-for-continuity",
  "customer_id": "CUST-10001"
}

# Response
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "I've looked up your account. You're currently on Unlimited Pro...",
  "tool_calls": 2,
  "message_count": 6,
  "timestamp": "2025-02-25T14:30:00Z"
}"""),

        spacer(0.15),
        sub_sub_header("POST /api/v1/chat/stream — Streaming Chat (SSE)"),
        body(
            "Returns a <b>Server-Sent Events</b> stream. Each event contains a text token. "
            "Useful for real-time streaming UIs."
        ),
        code_block(
"""# Response stream
data: Hello
data: ! I
data:  can help you
data:  with that.
data: [DONE]"""),

        spacer(0.3),
        sub_header("8.3  Account, Network & Plan Endpoints"),
        code_block(
"""# Get account
GET /api/v1/account/CUST-10001?include_usage=true
→ { customer_id, name, plan_id, billing_status, data_usage_gb, ... }

# Network status
GET /api/v1/network/status?zip_code=78701
GET /api/v1/network/status?customer_id=CUST-10001
→ { overall_status, signal_quality, active_incidents, incident_count }

# List plans
GET /api/v1/plans
→ { plans: [...], total: 4 }

# Change plan
POST /api/v1/plans/change
{ "customer_id": "CUST-10001", "plan_id": "PLAN-STANDARD-5G" }
→ { success, direction, old_plan, new_plan, confirmation_number }

# Publish Kafka event
POST /api/v1/kafka/publish
{ "topic": "telecom.customer.events", "event_type": "TEST", "payload": {} }
→ { success, event_id, topic, partition, offset }"""),
        PageBreak(),
    ]
    return story


# ══════════════════════════════════════════════════════════════════════════
# SECTION 9 — TESTING
# ══════════════════════════════════════════════════════════════════════════
def section_testing():
    story = [section_header("9.  Testing")]

    story += [
        sub_header("9.1  Test Strategy"),
        body(
            "The test suite follows the <b>Arrange-Act-Assert</b> pattern throughout. "
            "AWS Bedrock calls are mocked using <code>unittest.mock</code> — no real AWS "
            "credentials are needed to run the tests. Kafka is also mocked, allowing tests "
            "to run in CI environments without any external services."
        ),
        spacer(0.2),
        sub_header("9.2  Test Coverage"),
    ]

    cov_data = [
        ["Test File", "Scope", "Key Tests", "Approx. Count"],
        ["test_tools.py", "All 4 tools + dispatcher",
         "Account lookup by ID/phone, network outage detection,\nplan upgrade/downgrade, Kafka mock producer",
         "~25 tests"],
        ["test_agent.py", "Agentic loop + Claude client",
         "Simple chat, tool call + response, max iteration guard,\nmessage history accumulation",
         "~12 tests"],
        ["test_rag.py", "RAG retriever pipeline",
         "Index build, BM25 retrieval, TF-IDF scoring, RRF ranking,\nchunking, context formatting",
         "~13 tests"],
        ["test_api.py", "FastAPI integration",
         "All 10 endpoints, session persistence, request validation,\n400/404/422 error handling",
         "~15 tests"],
        ["test_config.py", "Configuration loading",
         "Settings from env, origins list, lru_cache singleton,\nproduction flag",
         "~5 tests"],
    ]
    story.append(make_table(cov_data,
        [3.5*cm, 3.5*cm, CONTENT_W - 9.5*cm, 2.5*cm]))
    story.append(spacer(0.2))

    story += [
        note_box("Coverage target: 70%+ enforced by --cov-fail-under=70 in pyproject.toml."),
        spacer(0.2),
        sub_header("9.3  Running Tests"),
        code_block(
"""# Run full test suite with coverage
pytest

# Run only tool tests
pytest tests/test_tools.py -v

# Run only agent tests
pytest tests/test_agent.py -v

# Skip coverage (faster)
pytest --no-cov -v

# Run a single test
pytest tests/test_tools.py::TestKafkaTool::test_publish_with_mock_producer -v

# View HTML coverage report
pytest && open htmlcov/index.html"""),
        spacer(0.2),
        code_block(
"""# Expected output (abbreviated)
tests/test_config.py::TestSettings::test_settings_load             PASSED
tests/test_tools.py::TestAccountTool::test_lookup_by_customer_id   PASSED
tests/test_tools.py::TestKafkaTool::test_publish_with_mock_producer PASSED
tests/test_rag.py::TestRetriever::test_retrieve_billing_query       PASSED
tests/test_api.py::TestChatEndpoints::test_chat_basic              PASSED
...
===== 55 passed in 3.12s =====  Coverage: 74%"""),
        PageBreak(),
    ]
    return story


# ══════════════════════════════════════════════════════════════════════════
# SECTION 10 — DEPLOYMENT
# ══════════════════════════════════════════════════════════════════════════
def section_deployment():
    story = [section_header("10.  Deployment")]

    story += [
        sub_header("10.1  Docker Compose"),
        body(
            "The <code>docker-compose.yml</code> defines three services: Kafka (KRaft mode, "
            "no ZooKeeper), Kafka UI for monitoring, and the NovaTel AI Agent application. "
            "The agent service waits for Kafka to be healthy before starting."
        ),
        code_block(
"""# Start all services
docker-compose up --build -d

# Check logs
docker-compose logs -f agent

# Kafka UI
http://localhost:8080

# Stop all
docker-compose down

# Services and ports:
#   kafka      → localhost:9092
#   kafka-ui   → localhost:8080
#   agent      → localhost:8000"""),

        spacer(0.3),
        sub_header("10.2  Production Checklist"),
        spacer(0.1),
    ]

    checklist_data = [
        ["#", "Item", "Notes"],
        ["1", "Replace static AWS credentials with IAM roles",
         "Attach IAM role to EC2/ECS/Lambda — no keys in .env"],
        ["2", "Set APP_ENV=production in .env",
         "Switches to JSON logging, disables hot-reload"],
        ["3", "Set a strong API_SECRET_KEY",
         "Generate with: python -c \"import secrets; print(secrets.token_hex(32))\""],
        ["4", "Configure ALLOWED_ORIGINS",
         "Set to your frontend domain(s) only"],
        ["5", "Enable HTTPS",
         "Use nginx reverse proxy or AWS ALB with SSL termination"],
        ["6", "Configure Kafka with authentication",
         "Enable SASL/SCRAM or mTLS for Kafka in production"],
        ["7", "Set up log aggregation",
         "Ship structlog JSON to CloudWatch, Datadog, or ELK stack"],
        ["8", "Configure health check monitoring",
         "Monitor GET /api/v1/health endpoint in your observability platform"],
        ["9", "Set Bedrock throttling alerts",
         "Monitor ThrottlingException metrics in CloudWatch"],
        ["10", "Run pytest in CI/CD pipeline",
         "Enforce pytest --cov-fail-under=70 in GitHub Actions / CodePipeline"],
    ]
    story.append(make_table(checklist_data, [0.8*cm, 5.5*cm, CONTENT_W - 6.3*cm]))
    story.append(spacer(0.3))

    story += [
        warning_box(
            "Never commit your .env file to source control. The .gitignore includes it, "
            "but always verify with: git check-ignore -v .env before pushing."
        ),
        spacer(0.3),
        hline(BRAND_BLUE, 1),
        spacer(0.2),
        Paragraph(
            "End of Documentation  ·  NovaTel AI Agent v1.0.0",
            ParagraphStyle("footer_end",
                fontName="Helvetica", fontSize=9,
                textColor=MUTED_GREY, alignment=TA_CENTER)
        ),
        Paragraph(
            f"Generated {datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')}  "
            "·  Powered by Claude 3.5 Sonnet on AWS Bedrock",
            ParagraphStyle("footer_end2",
                fontName="Helvetica", fontSize=8,
                textColor=MUTED_GREY, alignment=TA_CENTER)
        ),
    ]
    return story


# ══════════════════════════════════════════════════════════════════════════
# MAIN BUILD FUNCTION
# ══════════════════════════════════════════════════════════════════════════
def build():
    out = "/home/utpalbhadra/NovaTel_AI_Agent_Documentation.pdf"
    doc = DocTemplate(out)

    story = []
    story += cover_page()
    story += table_of_contents()
    story += section_overview()
    story += section_architecture()
    story += section_config()
    story += section_tools()
    story += section_agent()
    story += section_rag()
    story += section_kafka()
    story += section_api()
    story += section_testing()
    story += section_deployment()

    doc.build(story)
    print(f"PDF created: {out}")
    return out


if __name__ == "__main__":
    build()
