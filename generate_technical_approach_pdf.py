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
            self.drawString(54, 752, "SMARTPACK: TECHNICAL ARCHITECTURE & METHODOLOGY SPECIFICATION")
            self.setFont("Helvetica", 8)
            self.drawRightString(letter[0] - 54, 752, "SIH Problem Statement 26236")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, 744, letter[0] - 54, 744)
            
        # Running footer with clean separation
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 34, "SMARTPACK DECISION-SUPPORT ENGINE  |  FSSAI & BIS ALIGNED PROTOCOL")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 34, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 44, letter[0] - 54, 44)
        self.restoreState()

def build_pdf(filename="docs/SmartPack_Technical_Approach.pdf"):
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

    # Harmonious corporate technical palette
    c_primary = colors.HexColor("#1E3A8A")   # Navy 900
    c_secondary = colors.HexColor("#0D9488") # Teal 700
    c_dark = colors.HexColor("#0F172A")      # Slate 900
    c_muted = colors.HexColor("#475569")     # Slate 600
    c_card_bg = colors.HexColor("#F8FAFC")   # Slate 50
    c_border = colors.HexColor("#CBD5E1")    # Slate 300
    c_amber_bg = colors.HexColor("#FFFBEB")  # Amber 50
    c_amber_border = colors.HexColor("#F59E0B") # Amber 500

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=c_muted,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
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

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#78350F")
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

    formula_style = ParagraphStyle(
        'FormulaText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=c_primary,
        alignment=1 # Centered
    )

    story = []

    # ================= COVER / TITLE BLOCK =================
    story.append(Paragraph("SmartPack: Technical Architecture Document", title_style))
    story.append(Paragraph("Comprehensive Architectural, Scientific, and Machine Learning Specification<br/><b>SIH Problem Statement 26236: Smart Food-Packaging Recommendation System</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=0, spaceAfter=8))

    meta_table_data = [
        [Paragraph("<b>Project:</b> SmartPack (FSSAI Aligned)", tbl_cell), Paragraph("<b>Version:</b> 1.0.0-Production Spec", tbl_cell)],
        [Paragraph("<b>Domain:</b> Food Biochemistry, Materials Science & AI", tbl_cell), Paragraph("<b>Regulatory Framework:</b> FSSAI Regs 2018 / BIS Standards", tbl_cell)],
        [Paragraph("<b>Core Engine:</b> Scikit-Learn Random Forest & FastAPI", tbl_cell), Paragraph("<b>System Role:</b> Scientific Decision-Support Tool", tbl_cell)]
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
    story.append(Spacer(1, 10))

    # ================= SECTION 1: EXECUTIVE SUMMARY =================
    story.append(Paragraph("1. Executive Summary & Problem Context", h1_style))
    story.append(Paragraph(
        "Selecting appropriate food packaging requires balancing biological deterioration mechanisms (lipid oxidation, moisture vapor migration, enzymatic action, microbial proliferation), physical handling stresses during Indian transit conditions, environmental EPR circularity, and mandatory statutory regulations under the <b>Food Safety and Standards (Packaging) Regulations, 2018</b>. Small and medium food processors frequently lack capital-intensive testing equipment, causing food waste through under-packaging or excessive packaging costs and non-recyclable multi-material waste through over-packaging.",
        body_style
    ))
    story.append(Paragraph(
        "<b>SmartPack</b> bridges this gap via an explainable, multi-layered algorithmic pipeline. It synthesizes food composition data (ICMR IFCT 2017 nutritional records), regulatory mandates (FSSAI Schedule IV packaging endorsements), Bureau of Indian Standards (BIS) specifications, and an audited <b>Random Forest Machine Learning model</b> into an objective, rank-ordered recommendation.",
        body_style
    ))

    # Regulatory Notice Box
    callout_data = [[
        Paragraph(
            "<b>STATUTORY NOTICE (Section 12 Compliance):</b> SmartPack functions strictly as an analytical decision-support system. It accelerates material pre-screening but does not replace mandatory laboratory migration testing (IS 9845) or real-time microbiological shelf-life challenge tests required for commercial certification.",
            callout_style
        )
    ]]
    callout_table = Table(callout_data, colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_amber_bg),
        ('BOX', (0,0), (-1,-1), 1, c_amber_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 10))

    # ================= SECTION 2: END-TO-END PIPELINE ARCHITECTURE =================
    story.append(Paragraph("2. System Architecture & Recommendation Pipeline", h1_style))
    story.append(Paragraph(
        "The recommendation pipeline executes as a rigorous 6-stage funnel ensuring safety rules are enforced prior to candidate scoring:",
        body_style
    ))

    pipeline_table_data = [
        [Paragraph("Stage", tbl_header), Paragraph("Component", tbl_header), Paragraph("Engineering & Algorithmic Function", tbl_header)],
        [
            Paragraph("<b>Stage 1</b>", tbl_cell_bold),
            Paragraph("Input Normalization", tbl_cell),
            Paragraph("Parses food moisture %, fat sensitivity index, product pH, desired shelf life (days), ambient/cold storage temp (°C), RH %, and transit rigor.", tbl_cell)
        ],
        [
            Paragraph("<b>Stage 2</b>", tbl_cell_bold),
            Paragraph("Requirement Engine", tbl_cell),
            Paragraph("Calculates dynamic vulnerability thresholds: Oxygen barrier score (lipid oxidation risk), Moisture barrier score (deliquescence/caking), Seal integrity level, and MAP gas barrier.", tbl_cell)
        ],
        [
            Paragraph("<b>Stage 3</b>", tbl_cell_bold),
            Paragraph("Candidate Retrieval", tbl_cell),
            Paragraph("Queries FSSAI Schedule IV mappings (<code>14_recommended_packaging.csv</code>) to retrieve regulatory-endorsed candidate packaging categories.", tbl_cell)
        ],
        [
            Paragraph("<b>Stage 4</b>", tbl_cell_bold),
            Paragraph("Hard Safety Interlock", tbl_cell),
            Paragraph("<b>Enforces Regulatory Constraints:</b> Rejects candidates violating safety mandates (e.g., bare reactive metals for acidic foods, recycled plastics in direct food contact without NOC).", tbl_cell)
        ],
        [
            Paragraph("<b>Stage 5</b>", tbl_cell_bold),
            Paragraph("Hybrid Scoring & ML", tbl_cell),
            Paragraph("Scores surviving candidates using an 18-feature Random Forest ML model (30% weight) combined with multi-criteria barrier, compatibility, shelf-life, and circularity formulas.", tbl_cell)
        ],
        [
            Paragraph("<b>Stage 6</b>", tbl_cell_bold),
            Paragraph("Explainability Engine", tbl_cell),
            Paragraph("Constructs transparent Top-3 recommendations with factor breakdowns, data origin badges ('DATABASE VALUE' vs 'DERIVED SCORE'), and LLM technical narratives.", tbl_cell)
        ]
    ]
    p_table = Table(pipeline_table_data, colWidths=[55, 125, 324])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 0.8, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(p_table)
    story.append(Spacer(1, 10))

    # ================= SECTION 3: MACHINE LEARNING SPECIFICATION =================
    story.append(Paragraph("3. Machine Learning Model Architecture & Performance", h1_style))
    story.append(Paragraph(
        "SmartPack deploys a dual-head Random Forest ensemble trained to generalize complex interactions between product nutritional vulnerabilities, transit hazards, and polymer barrier physics.",
        body_style
    ))
    story.append(Paragraph("• <b>Random Forest Regressor (100 estimators, max depth 8):</b> Predicts continuous suitability score S_ML in [0.0, 1.0].", bullet_style))
    story.append(Paragraph("• <b>Random Forest Classifier (100 estimators, max depth 8):</b> Predicts discrete suitability binary label (Class 1: Suitable, Class 0: Incompatible).", bullet_style))
    story.append(Paragraph("• <b>Dataset & Splitting:</b> 7,200 synthesized feature pairs derived from ICMR nutritional records and FSSAI packaging mappings with a 75/25 train/test split (5,400 training rows, 1,800 held-out test rows, random_state=42).", bullet_style))

    metrics_table_data = [
        [Paragraph("Regression Metric", tbl_header), Paragraph("Value", tbl_header), Paragraph("Classification Metric", tbl_header), Paragraph("Value", tbl_header)],
        [Paragraph("Mean Absolute Error (MAE)", tbl_cell), Paragraph("<b>0.0348</b> (~3.5%)", tbl_cell), Paragraph("Classification Accuracy", tbl_cell), Paragraph("<b>91.83%</b>", tbl_cell)],
        [Paragraph("Root Mean Squared Error (RMSE)", tbl_cell), Paragraph("<b>0.0448</b>", tbl_cell), Paragraph("Precision (Suitable Class)", tbl_cell), Paragraph("<b>85.86%</b>", tbl_cell)],
        [Paragraph("Coefficient of Determination (R²)", tbl_cell), Paragraph("<b>0.9187</b> (91.9%)", tbl_cell), Paragraph("Recall / Sensitivity", tbl_cell), Paragraph("<b>84.66%</b>", tbl_cell)],
        [Paragraph("Feature Space Dimension", tbl_cell), Paragraph("<b>18 Tabular Features</b>", tbl_cell), Paragraph("F1 Score", tbl_cell), Paragraph("<b>0.8526</b>", tbl_cell)]
    ]
    m_table = Table(metrics_table_data, colWidths=[150, 102, 150, 102])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('BOX', (0,0), (-1,-1), 0.8, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Audited Feature Importance Ranking:</b>", h2_style))
    story.append(Paragraph(
        "1. <b>Desired Shelf-Life Days (72.82%)</b>: Governs whether monolayer commodity films suffice or high-barrier foil/EVOH laminates are required.<br/>"
        "2. <b>Multilayer Laminate Structure (13.88%)</b>: Detects presence of metallized or barrier co-extrusion layers.<br/>"
        "3. <b>Glass / Metal Class (9.89%)</b>: Accounts for zero-permeation impermeable rigid substrate behavior.<br/>"
        "4. <b>Recyclability Indicator (1.60%)</b>: Incentivizes single-polymer and recyclable structures aligned with EPR targets.<br/>"
        "5. <b>Product Moisture & Storage Environment (1.81%)</b>: Evaluates water vapor pressure differential across package boundaries.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # ================= SECTION 4: PHYSICAL CONSTANTS VS ML MODEL =================
    story.append(Paragraph("4. Physical Properties vs. ML Disambiguation", h1_style))
    story.append(Paragraph(
        "A critical technical consideration is whether the ML model generates physical values such as <b>Oxygen Transmission Rate (OTR)</b>, <b>Water Vapor Transmission Rate (WVTR)</b>, <b>Film Thickness</b>, and <b>Mechanical Strength</b>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Architectural Decoupling:</b> Material transmission rates are empirical constants dictated by polymer morphology and Fickian permeation laws. Guessing these values with ML would introduce hallucination risk. Consequently, SmartPack separates deterministic physical values from algorithmic scoring:",
        body_style
    ))

    prop_table_data = [
        [Paragraph("Property", tbl_header), Paragraph("Data Paradigm", tbl_header), Paragraph("Source & Engineering Basis", tbl_header)],
        [
            Paragraph("<b>OTR</b> (Oxygen Transmission)", tbl_cell_bold),
            Paragraph("Database / Material Standard", tbl_cell),
            Paragraph("BIS handbook and polymer test data (ASTM D3985). Glass bottles and tin containers are impermeable (OTR ≈ 0.0 cc/m²/day).", tbl_cell)
        ],
        [
            Paragraph("<b>WVTR</b> (Water Vapor Transmission)", tbl_cell_bold),
            Paragraph("Database / Material Standard", tbl_cell),
            Paragraph("Empirical transmission (ASTM F1249 / IS 5012). Foil laminates (&lt;0.1 g/m²/24h) and tin/glass (0.0 g/m²/24h) offer near-absolute moisture barrier.", tbl_cell)
        ],
        [
            Paragraph("<b>Film Thickness / Gauge</b>", tbl_cell_bold),
            Paragraph("Statutory / BIS Standard", tbl_cell),
            Paragraph("Regulated under Plastic Waste Management Rules 2016 (minimum 50–75 microns) or BIS material specs (e.g. IS 2508).", tbl_cell)
        ],
        [
            Paragraph("<b>Sealability / Closure</b>", tbl_cell_bold),
            Paragraph("Requirement Engine Output", tbl_cell),
            Paragraph("Specifies closure geometry (Hermetic Lug Cap for glass, Double Seam for tin, Hermetic Heat-Seal for pouches).", tbl_cell)
        ],
        [
            Paragraph("<b>MAP Suitability</b>", tbl_cell_bold),
            Paragraph("Polymer Classification Rule", tbl_cell),
            Paragraph("Evaluates presence of gas-tight barrier layers (EVOH, aluminium foil, metallized PET, tin cans).", tbl_cell)
        ],
        [
            Paragraph("<b>Final Suitability Score</b>", tbl_cell_bold),
            Paragraph("<b>Trained ML Ensemble (0–100)</b>", tbl_cell),
            Paragraph("<b>Predictive Output:</b> Synthesizes all 18 physical, environmental, and regulatory dimensions into an objective ranking.", tbl_cell)
        ]
    ]
    pr_table = Table(prop_table_data, colWidths=[120, 130, 254])
    pr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 0.8, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(pr_table)
    story.append(Spacer(1, 10))

    # ================= SECTION 5: HYBRID SCORING FORMULA =================
    story.append(Paragraph("5. Hybrid Multi-Criteria Scoring Formulation", h1_style))
    story.append(Paragraph(
        "To ensure transparency and allow domain specialists to adjust weightings, recommendations are ranked via a linear combination of 6 weighted factors defined in <code>config/scoring_weights.json</code>:",
        body_style
    ))

    # Centered formula box
    f_data = [[Paragraph("<b>Final Score = (0.30 × S_ML) + (0.20 × S_barrier) + (0.15 × S_compat) + (0.15 × S_shelf) + (0.10 × S_mech) + (0.10 × S_sust)</b>", formula_style)]]
    f_table = Table(f_data, colWidths=[504])
    f_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(f_table)
    story.append(Spacer(1, 6))

    score_breakdown_data = [
        [Paragraph("Factor Name", tbl_header), Paragraph("Default Weight", tbl_header), Paragraph("Evaluation Basis", tbl_header)],
        [Paragraph("ML Model Score (S_ML)", tbl_cell_bold), Paragraph("<b>30%</b> (0.30)", tbl_cell), Paragraph("Random Forest regressor suitability output based on 18-dimensional feature vector.", tbl_cell)],
        [Paragraph("Barrier Fit Score (S_barrier)", tbl_cell_bold), Paragraph("<b>20%</b> (0.20)", tbl_cell), Paragraph("Degree to which material satisfies calculated oxygen and moisture barrier requirements.", tbl_cell)],
        [Paragraph("Compatibility Score (S_compat)", tbl_cell_bold), Paragraph("<b>15%</b> (0.15)", tbl_cell), Paragraph("Chemical inertness, acidity handling (IS 5837), and fat stress cracking resistance.", tbl_cell)],
        [Paragraph("Shelf-Life Protection (S_shelf)", tbl_cell_bold), Paragraph("<b>15%</b> (0.15)", tbl_cell), Paragraph("Historical protection horizon versus requested commercial shelf-life duration.", tbl_cell)],
        [Paragraph("Mechanical Robustness (S_mech)", tbl_cell_bold), Paragraph("<b>10%</b> (0.10)", tbl_cell), Paragraph("Crush and puncture resistance under specified transport conditions (rigid vs flexible).", tbl_cell)],
        [Paragraph("Circularity Score (S_sust)", tbl_cell_bold), Paragraph("<b>10%</b> (0.10)", tbl_cell), Paragraph("CPCB Extended Producer Responsibility (EPR) recyclability, mono-materiality, or compostability.", tbl_cell)]
    ]
    sb_table = Table(score_breakdown_data, colWidths=[140, 90, 274])
    sb_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('BOX', (0,0), (-1,-1), 0.8, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(sb_table)
    story.append(Spacer(1, 10))

    # ================= SECTION 6: REGULATORY SAFETY & INDIAN STANDARDS =================
    story.append(Paragraph("6. Regulatory Compliance & Hard Safety Rules", h1_style))
    story.append(Paragraph(
        "SmartPack enforces statutory Indian food packaging regulations as <b>uncompromising hard filters</b> that immediately eliminate non-compliant materials regardless of their ML score:",
        body_style
    ))
    story.append(Paragraph("• <b>FSSAI (Packaging) Regulations, 2018 (Regulation 4(4)):</b> Strict ban on printing ink migration to food contact surfaces, prohibition of newspaper wrapping, and restriction on recycled plastics in direct contact without CPCB/FSSAI clearance.", bullet_style))
    story.append(Paragraph("• <b>Acidic Food Corrosion Interlock (pH &lt; 4.5):</b> Canned acidic foods mandate internal food-grade epoxy/phenolic lacquering per <b>IS 5837</b>; bare reactive tinplate is rejected to avoid heavy metal migration.", bullet_style))
    story.append(Paragraph("• <b>Lipid Migration Barrier:</b> Direct unlined paper prohibited for high-fat formulations to prevent oil staining, environmental stress cracking, and rancidity.", bullet_style))
    story.append(Paragraph("• <b>BIS Polymeric Specifications:</b> Validation against Indian Standards including IS 10146 (PE), IS 10142 (PP), IS 10151 (PVC), and IS 12252 (PET).", bullet_style))
    story.append(Spacer(1, 8))

    # ================= SECTION 7: TECHNICAL DATA TRANSPARENCY =================
    story.append(Paragraph("7. Technical Data Transparency & Audit Trail", h1_style))
    story.append(Paragraph(
        "To maintain scientific integrity when standard public databases exhibit missing values, SmartPack implements strict transparency guardrails:",
        body_style
    ))
    story.append(Paragraph("1. <b>Explicit Data Origin Badging:</b> Every metric in the UI and API is labeled as either <b>DATABASE VALUE</b> (verified empirical or statutory record) or <b>DERIVED SCORE / CALCULATED REQUIREMENT</b> (model estimation).", body_style))
    story.append(Paragraph("2. <b>No Data Fabrication Rule:</b> Missing test numbers are displayed as <i>'Data unavailable in source database'</i> or <i>'≈ 0.0 (Impermeable)'</i> rather than hallucinated.", body_style))
    story.append(Paragraph("3. <b>Technical Data Coverage Index:</b> Each candidate displays a completeness score indicating how many physical properties were verified in primary standards.", body_style))
    story.append(Paragraph("4. <b>Audit Funnel Logging:</b> Complete execution traces track the initial candidate pool, candidates eliminated by hard constraint rules, and scoring weight applications.", body_style))
    story.append(Spacer(1, 10))

    # ================= SECTION 8: SOFTWARE STACK & DEPLOYMENT =================
    story.append(Paragraph("8. Software Implementation & Architecture Stack", h1_style))
    stack_data = [
        [Paragraph("Tier", tbl_header), Paragraph("Technology", tbl_header), Paragraph("Purpose & Key Libraries", tbl_header)],
        [Paragraph("Backend API", tbl_cell_bold), Paragraph("FastAPI (Python 3.11+)", tbl_cell), Paragraph("Asynchronous REST API, Pydantic validation schemas, CORS middleware.", tbl_cell)],
        [Paragraph("ML / Analytics", tbl_cell_bold), Paragraph("Scikit-Learn, Pandas, NumPy", tbl_cell), Paragraph("Random Forest ensemble, feature preprocessing pipeline, joblib serialization.", tbl_cell)],
        [Paragraph("LLM Integration", tbl_cell_bold), Paragraph("Google Gemini API (1.5 Flash)", tbl_cell), Paragraph("Context-aware natural language explanations and regulatory citations.", tbl_cell)],
        [Paragraph("Frontend UI", tbl_cell_bold), Paragraph("React 18, TypeScript, Tailwind", tbl_cell), Paragraph("Accessible, reactive interface with Lucide iconography and live scoring weights.", tbl_cell)],
        [Paragraph("Build & Deploy", tbl_cell_bold), Paragraph("Vite, Render YAML, Uvicorn", tbl_cell), Paragraph("Optimized single-command build, static asset serving, and cloud containerization.", tbl_cell)]
    ]
    st_table = Table(stack_data, colWidths=[90, 150, 264])
    st_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 0.8, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(st_table)
    story.append(Spacer(1, 10))

    # ================= SIGN-OFF & CONCLUSION =================
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph(
        "<b>Conclusion:</b> SmartPack successfully demonstrates that food packaging selection is most effectively addressed through a hybrid architecture combining statutory safety interlocks, physical material properties, and machine learning suitability scoring. This ensures that recommendations are both innovative and strictly compliant with Indian food safety standards.",
        ParagraphStyle('Conclusion', parent=body_style, fontName='Helvetica-Oblique', textColor=c_muted)
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at {filename}")

if __name__ == "__main__":
    out = "docs/SmartPack_Technical_Approach.pdf"
    if len(sys.argv) > 1:
        out = sys.argv[1]
    build_pdf(out)
