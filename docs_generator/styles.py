"""
Styling definitions, color palette, and canvas management for SmartPack Documentation.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    Paragraph, Table, TableStyle
)
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 38
USABLE_WIDTH = PAGE_WIDTH - 2 * MARGIN

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and stamp exact total page counts ('Page X of Y')
    along with running header and footer on all pages except the cover.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Suppress running header and footer on cover page
        if self._pageNumber > 1:
            # Running Header
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(colors.HexColor("#1E3A8A")) # Deep Navy
            self.drawString(MARGIN, PAGE_HEIGHT - 28, "SMARTPACK (SIH 26236): TECHNICAL & ARCHITECTURAL DOCUMENTATION")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 28, "AI-ASSISTED FOOD PACKAGING SYSTEM")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(MARGIN, PAGE_HEIGHT - 34, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 34)
            
            # Running Footer
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(MARGIN, 22, "CONFIDENTIAL & PROPRIETARY  |  SIH EVALUATION & TECHNICAL AUDIT DOSSIER")
            page_str = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(PAGE_WIDTH - MARGIN, 22, page_str)
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(MARGIN, 30, PAGE_WIDTH - MARGIN, 30)

        self.restoreState()


def get_smartpack_styles():
    styles = getSampleStyleSheet()
    
    # Custom light theme palette
    c_primary = colors.HexColor("#1E3A8A")   # Deep Navy 900
    c_brand = colors.HexColor("#2563EB")     # Cobalt Blue 600
    c_accent = colors.HexColor("#4F46E5")    # Indigo 600
    c_secondary = colors.HexColor("#0D9488") # Teal 700
    c_dark = colors.HexColor("#0F172A")      # Slate 900
    c_body = colors.HexColor("#334155")      # Slate 700
    c_muted = colors.HexColor("#64748B")     # Slate 500
    
    styles.add(ParagraphStyle(
        'CoverSuper',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_brand,
        alignment=1,
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=c_primary,
        alignment=1,
        spaceAfter=8
    ))
    
    styles.add(ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        alignment=1,
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        'CoverDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_body,
        alignment=1,
        spaceAfter=20
    ))

    styles.add(ParagraphStyle(
        'CoverMetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=c_primary
    ))

    styles.add(ParagraphStyle(
        'CoverMetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark
    ))

    styles.add(ParagraphStyle(
        'SecHeading',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=17,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'SubSecHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=c_accent,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'SubSubSecHeading',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=12,
        textColor=c_dark,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        textColor=c_body,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        'BodyCustomBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11.2,
        textColor=c_dark,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=11.0,
        textColor=c_body,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.white,
        alignment=0
    ))

    styles.add(ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=9.0,
        textColor=c_dark
    ))

    styles.add(ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.0,
        leading=9.0,
        textColor=c_primary
    ))

    styles.add(ParagraphStyle(
        'TableCellMono',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8.5,
        textColor=c_dark
    ))

    styles.add(ParagraphStyle(
        'CalloutTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=10.5,
        textColor=c_dark,
        spaceAfter=2
    ))

    styles.add(ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.2,
        textColor=c_body
    ))

    styles.add(ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=8.8,
        textColor=colors.HexColor("#0F172A")
    ))

    return styles


def create_callout(title, text, style_type="note", styles=None):
    bg_map = {
        "note": (colors.HexColor("#F0F7FF"), colors.HexColor("#2563EB")),
        "tip": (colors.HexColor("#ECFDF5"), colors.HexColor("#059669")),
        "warning": (colors.HexColor("#FFFBEB"), colors.HexColor("#D97706")),
        "caution": (colors.HexColor("#FEF2F2"), colors.HexColor("#DC2626")),
        "statute": (colors.HexColor("#F5F3FF"), colors.HexColor("#7C3AED")),
    }
    bg_color, border_color = bg_map.get(style_type, bg_map["note"])

    p_title = Paragraph(f"<b>{title}</b>", styles['CalloutTitle'])
    p_text = Paragraph(text, styles['CalloutText'])
    
    table = Table([[p_title], [p_text]], colWidths=[USABLE_WIDTH])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('BOX', (0, 0), (-1, -1), 0.75, border_color),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return table
