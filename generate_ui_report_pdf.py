import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
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
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Suppress running header on cover/first page
        if self._pageNumber > 1:
            self.drawString(54, 752, "SMARTPACK: COMPLETE UI/UX ARCHITECTURE & VISUALIZATION GUIDE")
            self.setFont("Helvetica", 8)
            self.drawRightString(letter[0] - 54, 752, "SIH Problem Statement 26236")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, 744, letter[0] - 54, 744)
            
        # Running footer with clean separation
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 34, "SMARTPACK FRONTEND SPECIFICATION  |  REACT 18 + TAILWIND CSS + FASTAPI")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 34, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 44, letter[0] - 54, 44)
        self.restoreState()

def build_ui_pdf(filename="docs/SmartPack_UI_Visual_Report.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Premium corporate palette
    c_primary = colors.HexColor("#1E3A8A")   # Navy 900
    c_brand = colors.HexColor("#4F46E5")     # Indigo 600
    c_secondary = colors.HexColor("#0D9488") # Teal 700
    c_dark = colors.HexColor("#0F172A")      # Slate 900
    c_muted = colors.HexColor("#475569")     # Slate 600
    c_card_bg = colors.HexColor("#F8FAFC")   # Slate 50
    c_border = colors.HexColor("#CBD5E1")    # Slate 300
    c_emerald = colors.HexColor("#059669")   # Emerald 600
    c_amber_bg = colors.HexColor("#FFFBEB")  # Amber 50
    c_amber_border = colors.HexColor("#F59E0B") # Amber 500
    c_wireframe_bg = colors.HexColor("#F1F5F9") # Slate 100

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=25,
        textColor=c_primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_muted,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=c_primary,
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9.8,
        leading=13.5,
        textColor=c_brand,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    tbl_header = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=c_dark
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=c_dark
    )

    wireframe_box_style = ParagraphStyle(
        'WfBox',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_dark,
        alignment=1 # Centered
    )

    wireframe_sub_style = ParagraphStyle(
        'WfSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.5,
        textColor=c_muted,
        alignment=1
    )

    story = []

    # ================= COVER / HEADER BLOCK =================
    story.append(Paragraph("SmartPack: User Interface & Visual Layout Report", title_style))
    story.append(Paragraph("A Comprehensive Guide to Visualizing the Entire Web Application Workflow<br/><b>SIH Problem Statement 26236: Smart Food-Packaging Recommendation System</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_brand, spaceBefore=0, spaceAfter=8))

    meta_table_data = [
        [Paragraph("<b>Target System:</b> SmartPack Web Application", tbl_cell), Paragraph("<b>Tech Stack:</b> React 18, TypeScript, Tailwind CSS, Lucide Icons", tbl_cell)],
        [Paragraph("<b>Design Philosophy:</b> Scientific Precision, High Contrast & Clean Cards", tbl_cell), Paragraph("<b>Color Palette:</b> Slate 50/900, Indigo 600, Teal 700, Emerald 600", tbl_cell)],
        [Paragraph("<b>Key Features:</b> Live Sliders, Real-Time Meters, Top-3 Cards, Comparison Table", tbl_cell), Paragraph("<b>Responsive Target:</b> Desktop (1280px+), Tablet, and Mobile Viewports", tbl_cell)]
    ]
    meta_table = Table(meta_table_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 0.8, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # ================= SECTION 1: GLOBAL VISUAL ARCHITECTURE =================
    story.append(Paragraph("1. Global UI Architecture & Spatial Layout", h1_style))
    story.append(Paragraph(
        "The SmartPack user interface is designed like a high-end food science workstation. It avoids cluttered enterprise forms by structuring the application into a top-to-bottom <b>analytical journey</b>: Global Header &rarr; Interactive Parameter Configuration &rarr; Food Vulnerability Requirement Meters &rarr; Top-3 Recommendation Cards &rarr; Material Comparison Matrix &rarr; Detailed Explanations.",
        body_style
    ))

    # Wireframe schematic table of the full page
    wf_data = [
        [Paragraph("<b>NAVBAR:</b> Logo | Tabs: [Analysis Pipeline] [FSSAI Catalog] [ML Model Card] | Health Status [Active 496 Foods] | [Dev Telemetry]", wireframe_box_style)],
        [Paragraph("<b>HERO BANNER:</b> SIH 26236 Working Prototype Badge &bull; Headline &bull; FSSAI / ICMR / BIS Badges", wireframe_box_style)],
        [Paragraph("<b>INPUT CONFIGURATION FORM:</b><br/>"
                   "• Col 1: Food Item & ICMR Auto-Fill &bull; Category Select &bull; Moisture % Slider &bull; Fat Sensitivity &bull; pH Slider<br/>"
                   "• Col 2: Desired Shelf-Life Chips (14d/30d/90d/180d/365d) &bull; Temp (°C) &bull; RH % &bull; Transport Rigor &bull; MAP Switch<br/>"
                   "• Action Bar: [Adjust Weights Modal] &bull; <b>[Analyze Compatible Packaging Button (Sparkles)]</b>", wireframe_sub_style)],
        [Paragraph("<b>CALCULATED REQUIREMENT METERS (Screen 3):</b><br/>"
                   "[Oxygen Barrier: HIGH (0.85)] &bull; [Moisture Barrier: HIGH (0.90)] &bull; [Mechanical: MEDIUM (0.50)] &bull; [Seal: HERMETIC]", wireframe_sub_style)],
        [Paragraph("<b>TOP-3 RECOMMENDATION CARDS (Screen 4):</b><br/>"
                   "Card 1: #1 Primary Recommendation (Score 88/100) | Card 2: #2 Alternative Option (82/100) | Card 3: #3 Alternative Option (78/100)", wireframe_box_style)],
        [Paragraph("<b>SIDE-BY-SIDE COMPARISON TABLE (Screen 5):</b><br/>"
                   "Direct Matrix comparing Option 1 vs Option 2 vs Option 3 across OTR, WVTR, Thickness, Strength, Seal, MAP, and Score", wireframe_sub_style)],
        [Paragraph("<b>FOOTER:</b> SmartPack SIH-26236 &bull; FSSAI Schedule IV &bull; BIS Standards &bull; ICMR IFCT 2017", wireframe_sub_style)]
    ]
    wf_table = Table(wf_data, colWidths=[504])
    wf_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_wireframe_bg),
        ('BOX', (0,0), (-1,-1), 1, c_brand),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(wf_table)
    story.append(Spacer(1, 10))

    # ================= SECTION 2: SCREEN-BY-SCREEN VISUAL BREAKDOWN =================
    story.append(Paragraph("2. Screen-by-Screen Detailed Visual Breakdown", h1_style))

    # SCREEN 1: NAVBAR
    story.append(Paragraph("Screen 1: Top Navigation Bar & System Health", h2_style))
    story.append(Paragraph(
        "• <b>Brand Title:</b> Gradient-embossed 'SmartPack' with a dynamic beaker/package icon.<br/>"
        "• <b>Navigation Segmented Tabs:</b> Three clickable pill-style tabs: <i>'Analysis Pipeline'</i>, <i>'FSSAI Packaging Catalog'</i>, and <i>'ML Model Card & Audit'</i>.<br/>"
        "• <b>Real-Time API Health Badge:</b> A live emerald pill indicator showing <code>'Operational (496 Foods Loaded)'</code> dynamically verified against the backend FastAPI <code>/api/health</code> endpoint.<br/>"
        "• <b>Developer Telemetry Button:</b> A slate icon button that triggers the slide-out audit drawer.",
        body_style
    ))

    # SCREEN 2: INPUT FORM
    story.append(Paragraph("Screen 2: Interactive Food Input Panel (`FoodInputForm.tsx`)", h2_style))
    story.append(Paragraph(
        "Organized in a dual-column card on a pure white background with subtle rounded borders (24px radius):<br/>"
        "• <b>ICMR Food Search Bar:</b> As the user types (e.g. 'Biscuit', 'Milk', 'Pickle'), an autocomplete dropdown surfaces real foods from the ICMR IFCT 2017 dataset. Selecting an item auto-populates its exact moisture % and fat classification.<br/>"
        "• <b>Biochemical Sliders:</b> Smooth interactive range sliders for <b>Moisture %</b> (0 to 100%) and <b>pH Level</b> (2.0 acidic to 10.0 alkaline, color-coded from ruby red to cyan).<br/>"
        "• <b>Quick-Select Shelf-Life Chips:</b> Tactile pill buttons for standard shelf lives (<code>14 Days</code>, <code>30 Days</code>, <code>90 Days</code>, <code>180 Days</code>, <code>1 Year</code>) plus an exact number input.<br/>"
        "• <b>Environmental & Logistics Dropdowns:</b> Storage condition (Ambient 25°C, Chilled 4°C, Frozen -18°C), Relative Humidity slider, and Transport condition (Ambient Road, Cold Chain, Rough / Long Distance).<br/>"
        "• <b>Primary Action Button:</b> A large indigo gradient button stating <i>'Analyze Compatible Packaging'</i> with glowing micro-animation and loading spinner.",
        body_style
    ))

    # SCREEN 3: REQUIREMENT METERS
    story.append(Paragraph("Screen 3: Calculated Biochemical Requirement Gauges (`RequirementMeters.tsx`)", h2_style))
    story.append(Paragraph(
        "Appears immediately after calculation to reveal the food's scientific degradation risks before showing materials:<br/>"
        "• <b>4 Dynamic Cards:</b> Oxygen Barrier Demand, Moisture Barrier Demand, Mechanical Protection Need, and Sealability Requirement.<br/>"
        "• <b>Visual Status Badges:</b> Color-coded badges (Rose = High Demand, Amber = Medium Demand, Slate = Standard Demand).<br/>"
        "• <b>Animated Progress Bars:</b> Filled according to calculated score (e.g. 0.85/1.0), showing exact scientific rationale below (e.g. <i>'Critical oxygen barrier required to prevent lipid peroxidation in high-fat formulation'</i>).<br/>"
        "• <b>Origin Tag:</b> Every meter is stamped with <code>CALCULATED REQUIREMENT</code> to ensure full transparency.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # SCREEN 4: TOP 3 CARDS
    story.append(Paragraph("Screen 4: Top-3 Packaging Recommendation Cards (`RecommendationCard.tsx`)", h2_style))
    story.append(Paragraph(
        "A responsive 3-column deck comparing the top candidates ranked by suitability:",
        body_style
    ))

    card_layout_data = [
        [
            Paragraph("<b>#1 Primary Recommendation</b><br/><font color='#059669'><b>Rank 1 (Top Pick)</b></font>", tbl_cell_bold),
            Paragraph("<b>#2 Alternative Option</b><br/><font color='#4F46E5'><b>Rank 2 (Runner Up)</b></font>", tbl_cell_bold),
            Paragraph("<b>#3 Alternative Option</b><br/><font color='#64748B'><b>Rank 3 (Economic/Eco)</b></font>", tbl_cell_bold)
        ],
        [
            Paragraph("<b>Glass bottle with metal caps</b><br/>Type: Rigid Container<br/>Score: <b>88.5 / 100</b>", tbl_cell),
            Paragraph("<b>Tin container (lacquered)</b><br/>Type: Rigid Container<br/>Score: <b>82.0 / 100</b>", tbl_cell),
            Paragraph("<b>Aluminium-foil laminated pouch</b><br/>Type: Flexible Pouch<br/>Score: <b>78.4 / 100</b>", tbl_cell)
        ],
        [
            Paragraph("• OTR: &asymp; 0.0 (Impermeable)<br/>• WVTR: &asymp; 0.0 (Impermeable)<br/>• Closure: Lug Cap / Crown<br/>• Coverage: 85% Verified", tbl_cell),
            Paragraph("• OTR: &asymp; 0.0 (Impermeable)<br/>• WVTR: &asymp; 0.0 (Impermeable)<br/>• Closure: Double Seam<br/>• Coverage: 80% Verified", tbl_cell),
            Paragraph("• OTR: &lt; 0.1 cc/m²/day<br/>• WVTR: &lt; 0.1 g/m²/24h<br/>• Closure: Heat-Seal Hermetic<br/>• Coverage: 65% Verified", tbl_cell)
        ],
        [
            Paragraph("<b>Badges:</b><br/>[DATABASE VALUE] [ML PREDICTION]", tbl_cell),
            Paragraph("<b>Badges:</b><br/>[DATABASE VALUE] [ML PREDICTION]", tbl_cell),
            Paragraph("<b>Badges:</b><br/>[DATABASE VALUE] [ML PREDICTION]", tbl_cell)
        ],
        [
            Paragraph("<b>CTA:</b> [Why This Packaging? &rarr;]", tbl_cell_bold),
            Paragraph("<b>CTA:</b> [Why This Packaging? &rarr;]", tbl_cell_bold),
            Paragraph("<b>CTA:</b> [Why This Packaging? &rarr;]", tbl_cell_bold)
        ]
    ]
    cl_table = Table(card_layout_data, colWidths=[168, 168, 168])
    cl_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(cl_table)
    story.append(Spacer(1, 10))

    # SCREEN 5: COMPARISON TABLE
    story.append(Paragraph("Screen 5: Side-by-Side Packaging Matrix (`ComparisonTable.tsx`)", h2_style))
    story.append(Paragraph(
        "Directly beneath the cards, a comprehensive comparison matrix presents a side-by-side engineering evaluation across all candidates: <b>Material Name</b>, <b>Packaging Type</b>, <b>OTR</b>, <b>WVTR</b>, <b>Thickness Spec</b>, <b>Mechanical Strength</b>, <b>Sealability Closure</b>, <b>Compatibility Status</b>, <b>MAP Suitability</b>, <b>Shelf-Life Protection</b>, <b>Sustainability Recyclability</b>, <b>Data Coverage %</b>, <b>ML Score</b>, and <b>Final Derived Score</b>. The top option is highlighted with an emerald badge, while cells with unmeasured properties show clean italicized notices.",
        body_style
    ))

    # SCREEN 6: WHY THIS MODAL
    story.append(Paragraph("Screen 6: 'Why This Packaging?' Deep-Dive Modal (`WhyPackagingModal.tsx`)", h2_style))
    story.append(Paragraph(
        "Clicking 'Why This Packaging?' on any card launches a focused modal dialog with three powerful sections:<br/>"
        "1. <b>Weighted Multi-Factor Breakdown:</b> Visual bars detailing the 6 components of the score (ML Suitability 30%, Barrier Fit 20%, Compatibility 15%, Shelf-Life 15%, Mechanical 10%, Sustainability 10%).<br/>"
        "2. <b>Statutory Citation Box:</b> Cites exact FSSAI Schedule IV document name, page number, and official regulatory classification.<br/>"
        "3. <b>Google Gemini AI Explanation Generator:</b> An interactive button that calls Gemini 1.5 Flash to synthesize a personalized, plain-English biochemical explanation explaining why this packaging protects the food against lipid rancidity and microbial decay.<br/>"
        "4. <b>Scientific Limitations & Warnings:</b> Discloses mandatory testing requirements (overall migration IS 9845 and accelerated shelf life testing).",
        body_style
    ))

    # SCREEN 7: DEVELOPER DRAWER
    story.append(Paragraph("Screen 7: Developer Telemetry & Audit Funnel Drawer (`DeveloperDrawer.tsx`)", h2_style))
    story.append(Paragraph(
        "A slide-over right panel designed for auditors, food scientists, and developers:<br/>"
        "• <b>Funnel Counter:</b> Displays Candidate Reduction Stats (e.g. <i>102 Initial Candidates &rarr; 45 Filtered by Hard Safety Rules &rarr; 3 Final Recommendations</i>).<br/>"
        "• <b>Rejection Audit:</b> Lists rejected materials and the exact statutory rule that triggered rejection (e.g. <i>'Rejected Bare Tinplate: FSSAI Acidic Corrosion Safety Rule (pH 3.8 &lt; 4.5 requires lacquered can per IS 5837)'</i>).<br/>"
        "• <b>Weights Configuration:</b> Displays the active mathematical weights loaded from <code>config/scoring_weights.json</code>.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # ================= SECTION 3: COLOR SYSTEM & DESIGN TOKENS =================
    story.append(Paragraph("3. Design System, Color Tokens & Typography", h1_style))
    story.append(Paragraph(
        "SmartPack follows a purpose-driven, accessible design token system implemented in Tailwind CSS:",
        body_style
    ))

    color_table_data = [
        [Paragraph("Token / Color Role", tbl_header), Paragraph("Hex / Tailwind Class", tbl_header), Paragraph("UI Usage & Semantic Meaning", tbl_header)],
        [Paragraph("Primary Brand", tbl_cell_bold), Paragraph("<code>#4F46E5</code> (indigo-600)", tbl_cell), Paragraph("Primary CTA buttons, active tabs, prominent badges, header accents.", tbl_cell)],
        [Paragraph("Success / High Fit", tbl_cell_bold), Paragraph("<code>#059669</code> (emerald-600)", tbl_cell), Paragraph("Top-rank badge, high suitability scores (80%+), operational health status.", tbl_cell)],
        [Paragraph("Warning / Caution", tbl_cell_bold), Paragraph("<code>#D97706</code> (amber-600)", tbl_cell), Paragraph("Medium barrier demands, data limitations notices, shelf-life caveats.", tbl_cell)],
        [Paragraph("Hazard / Rejection", tbl_cell_bold), Paragraph("<code>#DC2626</code> (rose-600)", tbl_cell), Paragraph("Hard constraint rejections, acidic corrosion warnings, missing input errors.", tbl_cell)],
        [Paragraph("Card & Panel Surfaces", tbl_cell_bold), Paragraph("<code>#FFFFFF</code> / <code>#F8FAFC</code>", tbl_cell), Paragraph("Clean white cards elevated over subtle slate-50 background with soft 1px borders.", tbl_cell)],
        [Paragraph("Typography", tbl_cell_bold), Paragraph("Inter / System Sans-serif", tbl_cell), Paragraph("Crisp tabular numbers, clean hierarchy (H1 32px, H2 20px, Body 14px, Badges 11px).", tbl_cell)]
    ]
    ct_table = Table(color_table_data, colWidths=[120, 130, 254])
    ct_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 0.8, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(ct_table)
    story.append(Spacer(1, 10))

    # ================= SECTION 4: USER INTERACTION FLOW =================
    story.append(Paragraph("4. End-to-End User Interaction Flow", h1_style))
    story.append(Paragraph(
        "<b>Step 1: Ingestion & Fast Setup</b><br/>"
        "The user selects or searches a food (e.g. <i>'Potato Chips'</i>). The form instantly loads nutritional baseline values (Moisture: 2%, Fat: 35%). The user adjusts the target shelf life to 180 days and storage to Ambient (25°C, 65% RH).<br/><br/>"
        "<b>Step 2: Triggering Analysis</b><br/>"
        "The user clicks <i>'Analyze Compatible Packaging'</i>. The button enters a smooth loading state while the FastAPI backend runs the 6-stage pipeline in under 150 milliseconds.<br/><br/>"
        "<b>Step 3: Immediate Vulnerability Feedback</b><br/>"
        "The page scrolls smoothly to the <b>Requirement Meters</b>. The user immediately visualizes that their high-fat, low-moisture chips demand <b>High Oxygen Barrier</b> (to prevent rancidity) and <b>High Moisture Barrier</b> (to prevent crispness loss).<br/><br/>"
        "<b>Step 4: Evaluating the Top-3 Recommendations</b><br/>"
        "The user compares the cards: Option 1 recommends a <i>Metallized Polyester / Polyethylene laminate pouch</i> with near-zero transmission rates. Option 2 offers a <i>Nitrogen-flushed composite can</i>. Option 3 presents a <i>Bio-based high-barrier pouch</i>.<br/><br/>"
        "<b>Step 5: Deep Explanation & AI Dialogue</b><br/>"
        "The user clicks <i>'Why This Packaging?'</i> on Option 1. The modal displays the mathematical score breakdown and generates a Gemini AI summary citing FSSAI Schedule IV regulatory compliance.<br/><br/>"
        "<b>Step 6: Audit & Export</b><br/>"
        "If desired, the user opens the Developer Telemetry Drawer to review rejected candidate logs, or refers to the generated PDF reports.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # ================= SIGN-OFF & CONCLUSION =================
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph(
        "<b>Summary for Stakeholders:</b> The SmartPack user interface transforms complex polymer engineering, biochemical degradation risks, and Indian FSSAI statutory regulations into an intuitive, responsive, and visually transparent dashboard that anyone can operate and understand within seconds.",
        ParagraphStyle('Conclusion', parent=body_style, fontName='Helvetica-Oblique', textColor=c_muted)
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"UI Report PDF generated successfully at {filename}")

if __name__ == "__main__":
    out = "docs/SmartPack_UI_Visual_Report.pdf"
    if len(sys.argv) > 1:
        out = sys.argv[1]
    build_ui_pdf(out)
