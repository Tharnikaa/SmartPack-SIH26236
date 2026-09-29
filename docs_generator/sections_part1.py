"""
SmartPack Documentation - Part 1: Cover, Executive Summary, TOC, Sections 1 to 5.
"""

from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from docs_generator.styles import USABLE_WIDTH, create_callout

def build_cover_page(styles):
    elements = []
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("SMART INDIA HACKATHON (SIH) 2024 / 2026 TECHNICAL DOSSIER", styles['CoverSuper']))
    elements.append(Paragraph("SMARTPACK", styles['CoverTitle']))
    elements.append(Paragraph("AI-Assisted Intelligent Food Packaging Material Recommendation System", styles['CoverSubtitle']))
    elements.append(Paragraph("SIH Problem Statement 26236  |  Theme: Agriculture, FoodTech & Rural Development", styles['CoverDesc']))
    
    elements.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceAfter=25, spaceBefore=10))
    
    # Metadata Box
    meta_data = [
        [Paragraph("Project Title:", styles['CoverMetaLabel']), Paragraph("SmartPack: Intelligent Food Packaging Selection & Compliance Engine", styles['CoverMetaVal'])],
        [Paragraph("Problem Statement ID:", styles['CoverMetaLabel']), Paragraph("26236 (Ministry of Food Processing Industries / FSSAI Domain)", styles['CoverMetaVal'])],
        [Paragraph("Target Audience:", styles['CoverMetaLabel']), Paragraph("SIH Technical Jury, Food Processing MSMEs, Regulatory Auditors, Packaging Engineers", styles['CoverMetaVal'])],
        [Paragraph("System Architecture:", styles['CoverMetaLabel']), Paragraph("Hybrid Deterministic-Statutory & Machine Learning Assisted Multi-Criteria System", styles['CoverMetaVal'])],
        [Paragraph("Implementation Status:", styles['CoverMetaLabel']), Paragraph("Functional Engineering Prototype (FastAPI Backend + React 19 Frontend + Trained ML Bundle)", styles['CoverMetaVal'])],
        [Paragraph("Document Purpose:", styles['CoverMetaLabel']), Paragraph("Comprehensive Technical Specification, Pipeline Audit & Viva Defense Reference", styles['CoverMetaVal'])],
        [Paragraph("Date of Publication:", styles['CoverMetaLabel']), Paragraph("September 2026 (Production Release v2.0)", styles['CoverMetaVal'])],
        [Paragraph("Repository Corpus:", styles['CoverMetaLabel']), Paragraph("Tharnikaa / SmartPack-SIH26236", styles['CoverMetaVal'])],
    ]
    meta_table = Table(meta_data, colWidths=[140, USABLE_WIDTH - 140])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(meta_table)
    
    elements.append(Spacer(1, 40))
    
    statute_box = create_callout(
        "STATUTORY & SCIENTIFIC CITATION MANDATE",
        "This project adheres strictly to empirical ground-truth governance. In compliance with FSSAI (Packaging) Regulations 2018, "
        "Bureau of Indian Standards (BIS) specifications, and ICMR-NIN IFCT 2017 nutritional tables, SmartPack enforces zero-fabrication "
        "protocols. Unmeasured transmission rates are truthfully flagged as 'Data unavailable', and statutory safety rules function as non-negotiable "
        "hard filters before algorithmic multi-criteria scoring.",
        style_type="statute",
        styles=styles
    )
    elements.append(statute_box)
    
    elements.append(PageBreak())
    return elements


def build_executive_summary_and_toc(styles):
    elements = []
    
    elements.append(Paragraph("Executive Summary", styles['SecHeading']))
    elements.append(Paragraph(
        "Post-harvest food losses across India are estimated by the Ministry of Food Processing Industries (MoFPI) and ICAR to "
        "range between 15% and 30% annually, representing tens of thousands of crores in wasted agricultural output and food insecurity. "
        "A primary driver of this loss is sub-optimal, unscientific, or non-compliant packaging material selection. Food processors—particularly "
        "rural enterprises, farmer producer organizations (FPOs), and small and medium-sized enterprises (MSMEs)—frequently rely on informal "
        "trial-and-error, generic low-barrier polyethylene films, or outdated packaging methods that fail to preserve product freshness, "
        "induce rapid lipid peroxidation, cause premature desiccation, or violate national food-contact regulations.",
        styles['BodyCustom']
    ))
    elements.append(Paragraph(
        "<b>SmartPack</b> solves SIH Problem Statement 26236 by establishing an automated, scientific, AI-assisted decision-support system. "
        "Instead of treating packaging selection as an unstructured conversational chat or an unconstrained machine-learning black box, "
        "SmartPack couples <b>deterministic statutory interlocks</b> (FSSAI Schedule IV, IS 14534, IS 2991) with <b>physics-based preservation heuristics</b>, "
        "a <b>candidate-specific 23-feature Random Forest ML model</b>, a <b>multi-criteria scoring engine</b>, and a <b>strictly grounded generative AI "
        "(Google Gemini 2.5 Flash) explanation layer</b>. This documentation provides a transparent, exhaustive technical specification of the entire "
        "codebase, datasets, algorithms, and validation results.",
        styles['BodyCustom']
    ))
    
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Table of Contents", styles['SecHeading']))
    
    toc_data = [
        [Paragraph("<b>Sec</b>", styles['TableHead']), Paragraph("<b>Section Title</b>", styles['TableHead']), Paragraph("<b>Focus & Scope</b>", styles['TableHead'])],
        [Paragraph("1", styles['TableCellBold']), Paragraph("SIH 26236 Problem Statement Analysis", styles['TableCell']), Paragraph("Industry background, multi-physics barriers, failure of manual selection", styles['TableCell'])],
        [Paragraph("2", styles['TableCellBold']), Paragraph("SmartPack — Proposed Solution", styles['TableCell']), Paragraph("High-level system concept, inputs, 10-stage processing pipeline, outputs", styles['TableCell'])],
        [Paragraph("3", styles['TableCellBold']), Paragraph("Architectural Innovation & Hybrid Advantage", styles['TableCell']), Paragraph("Why hybrid AI outperforms pure LLMs and pure ML; hallucination prevention", styles['TableCell'])],
        [Paragraph("4", styles['TableCellBold']), Paragraph("Dataset Inventory & Data Engineering", styles['TableCell']), Paragraph("Comprehensive 16-dataset catalogue, source hierarchy (ICMR, FSSAI, BIS, ICAR)", styles['TableCell'])],
        [Paragraph("5", styles['TableCellBold']), Paragraph("Data Quality, Integrity & Limitations", styles['TableCell']), Paragraph("OTR/WVTR availability, missing field analysis, data transparency protocol", styles['TableCell'])],
        [Paragraph("6", styles['TableCellBold']), Paragraph("Machine Learning Architecture & Metrics", styles['TableCell']), Paragraph("Random Forest regressor & classifier, candidate-specific training, metrics", styles['TableCell'])],
        [Paragraph("7", styles['TableCellBold']), Paragraph("Feature Engineering Pipeline (23 Dimensions)", styles['TableCell']), Paragraph("Complete 23-feature vector, interaction features, feature importance ranking", styles['TableCell'])],
        [Paragraph("8", styles['TableCellBold']), Paragraph("Requirement Generation Engine", styles['TableCell']), Paragraph("Biochemical heuristics for oxygen, moisture, mechanical, seal, light requirements", styles['TableCell'])],
        [Paragraph("9", styles['TableCellBold']), Paragraph("Packaging Candidate Generation", styles['TableCell']), Paragraph("FSSAI Schedule IV candidate retrieval, polymer reference matching, thickness", styles['TableCell'])],
        [Paragraph("10", styles['TableCellBold']), Paragraph("Regulatory Hard Constraint Filter", styles['TableCell']), Paragraph("8 deterministic interlocks: recycled plastics ban, acid tinplate, produce interlock", styles['TableCell'])],
        [Paragraph("11", styles['TableCellBold']), Paragraph("Multi-Criteria Technical Scoring Engine", styles['TableCell']), Paragraph("6 criteria weights, composite formulation, critical barrier defect penalty", styles['TableCell'])],
        [Paragraph("12", styles['TableCellBold']), Paragraph("Top-3 Recommendation & Diversification", styles['TableCell']), Paragraph("Packaging family diversification logic, output cards, UI data contracts", styles['TableCell'])],
        [Paragraph("13", styles['TableCellBold']), Paragraph("LLM / Generative AI Explanation Layer", styles['TableCell']), Paragraph("Gemini 2.5 Flash narrative generation, strict grounding, prompt engineering", styles['TableCell'])],
        [Paragraph("14", styles['TableCellBold']), Paragraph("Deep Dive: Oxygen & Water Vapor Permeation", styles['TableCell']), Paragraph("OTR and WVTR physics, test conditions, units, literature reference baseline", styles['TableCell'])],
        [Paragraph("15", styles['TableCellBold']), Paragraph("Complete Technology Stack Specification", styles['TableCell']), Paragraph("Frontend, backend, ML libraries, data stores, deployment specifications", styles['TableCell'])],
        [Paragraph("16", styles['TableCellBold']), Paragraph("System Architecture & Data Flow", styles['TableCell']), Paragraph("Modular architecture diagram, component interactions, runtime boundaries", styles['TableCell'])],
        [Paragraph("17", styles['TableCellBold']), Paragraph("Complete Technical Pipeline Flowchart", styles['TableCell']), Paragraph("End-to-end execution flow, decision gates, error recovery paths", styles['TableCell'])],
        [Paragraph("18", styles['TableCellBold']), Paragraph("RESTful API Specifications & Data Contracts", styles['TableCell']), Paragraph("Endpoints table, POST /api/analyze request/response schemas, JSON payloads", styles['TableCell'])],
        [Paragraph("19", styles['TableCellBold']), Paragraph("Repository Codebase Structure", styles['TableCell']), Paragraph("File tree inspection, architectural responsibility of backend/frontend modules", styles['TableCell'])],
        [Paragraph("20", styles['TableCellBold']), Paragraph("Comprehensive Test Cases & Pipeline Audit", styles['TableCell']), Paragraph("8 realistic commodities (Carrot, Apple, Potato, Chips, Biscuits, Oil, Sauce, Fallback)", styles['TableCell'])],
        [Paragraph("21", styles['TableCellBold']), Paragraph("Current Known Issues & Engineering Solutions", styles['TableCell']), Paragraph("Resolution of candidate similarity via produce and snack physical interlocks", styles['TableCell'])],
        [Paragraph("22", styles['TableCellBold']), Paragraph("Security, Integrity & Error Handling", styles['TableCell']), Paragraph("Input validation, Pydantic type safety, exception handling, data isolation", styles['TableCell'])],
        [Paragraph("23", styles['TableCellBold']), Paragraph("Runtime Performance & Scalability", styles['TableCell']), Paragraph("Sub-50ms execution latency, memory footprint, production readiness", styles['TableCell'])],
        [Paragraph("24", styles['TableCellBold']), Paragraph("Sustainability, Circular Economy & EPR", styles['TableCell']), Paragraph("PWM Rules 2016, CPCB EPR categories, food-loss vs packaging carbon trade-offs", styles['TableCell'])],
        [Paragraph("25", styles['TableCellBold']), Paragraph("Transparent System Limitations", styles['TableCell']), Paragraph("Sparse empirical OTR data, synthetic ML training set, FSSAI category granularity", styles['TableCell'])],
        [Paragraph("26", styles['TableCellBold']), Paragraph("Future Engineering Roadmap", styles['TableCell']), Paragraph("Lab testing expansion, active MAP sensors, ASTM database, mobile deployment", styles['TableCell'])],
        [Paragraph("27", styles['TableCellBold']), Paragraph("Complete End-to-End Walkthrough Trace", styles['TableCell']), Paragraph("Step-by-step numerical pipeline execution for Potato Chips & Fresh Produce", styles['TableCell'])],
        [Paragraph("28", styles['TableCellBold']), Paragraph("Theoretical Synthesis: Why SmartPack is Hybrid AI", styles['TableCell']), Paragraph("Comparison: Rule-based vs Pure ML vs Pure LLM vs SmartPack Hybrid Engine", styles['TableCell'])],
        [Paragraph("29", styles['TableCellBold']), Paragraph("Hackathon Presentation & Viva Defense Guide", styles['TableCell']), Paragraph("Pitch summaries (30s, 1m, 3m), 5 jury talking points, 10 tough viva Q&As", styles['TableCell'])],
        [Paragraph("30", styles['TableCellBold']), Paragraph("Final Technical Positioning & Conclusion", styles['TableCell']), Paragraph("Auditable claims, engineering maturity statement, concluding perspective", styles['TableCell'])],
    ]
    toc_table = Table(toc_data, colWidths=[24, 180, USABLE_WIDTH - 204])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(toc_table)
    
    elements.append(PageBreak())
    return elements


def build_section_1_problem_statement(styles):
    elements = []
    elements.append(Paragraph("1. Understanding the SIH 26236 Problem Statement", styles['SecHeading']))
    elements.append(Paragraph(
        "Smart India Hackathon (SIH) Problem Statement <b>26236</b>, presented under the aegis of the Ministry of Food Processing "
        "Industries (MoFPI) and the Food Safety and Standards Authority of India (FSSAI), is titled: <i>'AI-Based Intelligent Food "
        "Packaging Material Recommendation System for Food Commodities'</i>. This problem addresses a profound technological and economic "
        "bottleneck across the agricultural post-harvest value chain.",
        styles['BodyCustom']
    ))
    
    elements.append(Paragraph("1.1 The Multi-Physics Complexity of Food Packaging", styles['SubSecHeading']))
    elements.append(Paragraph(
        "Packaging in the food industry is not merely passive containment or brand display; it is an active thermodynamic and "
        "biochemical barrier. Food spoilage occurs through distinct, concurrent biochemical degradation pathways that depend directly "
        "on the food's physical and compositional characteristics:",
        styles['BodyCustom']
    ))
    
    spoilage_points = [
        "<b>Moisture Migration:</b> Dry, crisp foods (biscuits, potato chips, extruded snacks, aw < 0.3) absorb atmospheric moisture, resulting in crispness loss and caking. Conversely, high-moisture foods (fresh cuts, bakery, meats) lose moisture through desiccation, causing weight loss, toughening, and visual shrinkage.",
        "<b>Oxygen-Induced Lipid Peroxidation:</b> High-fat commodities (nuts, fried snacks, dairy powders, edible oils) undergo free-radical auto-oxidation when exposed to atmospheric oxygen, generating rancid off-flavors (hexanal, aldehydes) and destroying fat-soluble vitamins (A, D, E).",
        "<b>Produce Respiration & Anaerobic Spoilage:</b> Fresh fruits and vegetables are living, respiring biological tissues. They consume oxygen (O2) and emit carbon dioxide (CO2) and water vapor. If sealed inside an impermeable container without ventilation, internal O2 rapidly depletes (<1-2%), triggering anaerobic fermentation, ethanol accumulation, and tissue rot.",
        "<b>Photo-Degradation:</b> Ambient ultraviolet and visible light induce photo-oxidation in fats and riboflavin degradation in milk. In tubers such as potatoes, light exposure stimulates chlorophyll synthesis ('greening') accompanied by the accumulation of toxic glycoalkaloids (solanine and chaconine).",
        "<b>Chemical & Acid Interaction:</b> High-acid foods (pickles, tomato sauces, fruit juices, pH < 4.5) actively corrode bare metals, causing tin dissolution, hydrogen swells, and off-flavors, requiring epoxy-phenolic internal lacquering.",
        "<b>Mechanical Logistics Rigor:</b> During transit across Indian roads, food packages experience vibration, compression, and impact forces that shatter brittle goods or puncture flexible pouches unless sufficient tensile strength and bursting strength are provided."
    ]
    for pt in spoilage_points:
        elements.append(Paragraph(f"• {pt}", styles['BulletCustom']))
        
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("1.2 The Failure of Manual Packaging Selection", styles['SubSecHeading']))
    elements.append(Paragraph(
        "Historically, packaging selection in Indian MSMEs has been dominated by fragmented manual processes. A food entrepreneur "
        "must navigate more than 15 Bureau of Indian Standards (BIS) product specifications, multiple schedules of the FSSAI Packaging Regulations, "
        "Central Pollution Control Board (CPCB) Extended Producer Responsibility (EPR) mandates, and complex polymer property tables. "
        "Human cognitive limits make it nearly impossible to evaluate 20+ interacting variables manually without error.",
        styles['BodyCustom']
    ))
    
    # Requirement Comparison Table
    elements.append(Paragraph("1.3 SIH Problem Statement Requirement vs. SmartPack Implementation", styles['SubSecHeading']))
    comp_data = [
        [Paragraph("<b>SIH 26236 Mandated Scope</b>", styles['TableHead']), Paragraph("<b>SmartPack Implemented Reality (v2.0)</b>", styles['TableHead']), Paragraph("<b>Status & Traceability</b>", styles['TableHead'])],
        [Paragraph("Accept commodity composition & storage conditions", styles['TableCell']), Paragraph("13 input fields (moisture, fat, pH, respiration, shelf life, temp, RH, MAP, etc.)", styles['TableCell']), Paragraph("FULLY IMPLEMENTED (FastAPI / React)", styles['TableCellBold'])],
        [Paragraph("Scientific requirement generation", styles['TableCell']), Paragraph("Automated physics-based barrier & physical requirement calculations", styles['TableCell']), Paragraph("FULLY IMPLEMENTED (requirement_engine.py)", styles['TableCellBold'])],
        [Paragraph("Statutory regulatory compliance checking", styles['TableCell']), Paragraph("8 hard safety constraints (IS 14534 recycled plastics ban, IS 2991, acid tinplate)", styles['TableCell']), Paragraph("FULLY IMPLEMENTED (constraint_filter.py)", styles['TableCellBold'])],
        [Paragraph("Fresh produce respiration handling", styles['TableCell']), Paragraph("Produce Respiration Interlock (bans airtight cans/bottles for respiring produce)", styles['TableCell']), Paragraph("FULLY IMPLEMENTED (constraint_filter.py)", styles['TableCellBold'])],
        [Paragraph("AI / Machine Learning suitability prediction", styles['TableCell']), Paragraph("Candidate-specific 23-feature Random Forest Regressor & Classifier", styles['TableCell']), Paragraph("FULLY IMPLEMENTED (train.py, predict.py)", styles['TableCellBold'])],
        [Paragraph("Transparent multi-criteria ranking", styles['TableCell']), Paragraph("6-factor weighted scoring (ML, Barrier, Compatibility, Shelf-life, Mech, Sust)", styles['TableCell']), Paragraph("FULLY IMPLEMENTED (scoring_engine.py)", styles['TableCellBold'])],
        [Paragraph("Empirical laboratory testing of new films", styles['TableCell']), Paragraph("Physical lab testing not executable in software prototype; referenced published lit", styles['TableCell']), Paragraph("PROPOSED / FUTURE SCOPE", styles['TableCell'])],
        [Paragraph("Real-time shelf-life sensor integration", styles['TableCell']), Paragraph("Smart sensor hardware integration outside digital recommendation scope", styles['TableCell']), Paragraph("PROPOSED / FUTURE SCOPE", styles['TableCell'])],
    ]
    t = Table(comp_data, colWidths=[160, 210, USABLE_WIDTH - 370])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t)
    
    elements.append(PageBreak())
    return elements


def build_section_2_proposed_solution(styles):
    elements = []
    elements.append(Paragraph("2. SmartPack — The Proposed Solution", styles['SecHeading']))
    elements.append(Paragraph(
        "SmartPack is an intelligent, multi-layered food packaging recommendation and regulatory verification engine. "
        "It acts as a digital packaging technologist for food processors, research institutions, and regulatory enforcement bodies. "
        "The system accepts food compositional characteristics, environmental storage conditions, and user commercial priorities, "
        "executing a transparent 10-stage evaluation pipeline to produce the Top 3 optimal packaging specifications.",
        styles['BodyCustom']
    ))
    
    elements.append(Paragraph("2.1 Pipeline Inputs, Processing & Outputs", styles['SubSecHeading']))
    
    pipe_data = [
        [Paragraph("<b>Pipeline Stage</b>", styles['TableHead']), Paragraph("<b>Detailed Technical Scope</b>", styles['TableHead']), Paragraph("<b>Source / Responsible Module</b>", styles['TableHead'])],
        [Paragraph("1. Input Intake", styles['TableCellBold']), Paragraph("Commodity name, category, moisture %, fat sensitivity (L/M/H), pH, respiration class, target shelf life (days), storage temp (°C), RH %, storage mode, transport rigor, MAP demand, sustainability priority, package format.", styles['TableCell']), Paragraph("AnalyzeRequest (Pydantic v2) / FoodInputForm.tsx", styles['TableCell'])],
        [Paragraph("2. Food Data Lookup", styles['TableCellBold']), Paragraph("Auto-populates nutritional baselines from ICMR-NIN IFCT 2017 (496 foods) and respiration profiles from post-harvest reference database.", styles['TableCell']), Paragraph("data_service.py / 01_food_dataset.csv", styles['TableCell'])],
        [Paragraph("3. Requirement Synthesis", styles['TableCellBold']), Paragraph("Computes quantitative (0-1) and qualitative barrier requirements for oxygen, moisture, mechanical strength, seal integrity, light protection, and gas exchange.", styles['TableCell']), Paragraph("requirement_engine.py / requirement_thresholds.json", styles['TableCell'])],
        [Paragraph("4. Candidate Retrieval", styles['TableCellBold']), Paragraph("Retrieves officially sanctioned packaging options mapped to the food category from FSSAI Schedule IV (102 rows) enriched with BIS specifications.", styles['TableCell']), Paragraph("candidate_generator.py / 14_recommended_packaging.csv", styles['TableCell'])],
        [Paragraph("5. Hard Regulatory Filter", styles['TableCellBold']), Paragraph("Applies 8 deterministic legal and physical safety interlocks. Drops candidates violating FSSAI, BIS, or biological safety mandates before any scoring.", styles['TableCell']), Paragraph("constraint_filter.py / 13_regulatory_rules.csv", styles['TableCell'])],
        [Paragraph("6. ML Feature Vector", styles['TableCellBold']), Paragraph("Constructs a standardized candidate-specific 23-dimensional feature vector combining commodity, storage, candidate packaging, and interaction terms.", styles['TableCell']), Paragraph("preprocessing.py (FeaturePipeline)", styles['TableCell'])],
        [Paragraph("7. ML Inference", styles['TableCellBold']), Paragraph("Random Forest Regressor predicts continuous suitability score (0-100); Random Forest Classifier validates binary acceptance.", styles['TableCell']), Paragraph("predict.py / packaging_suitability_model.pkl", styles['TableCell'])],
        [Paragraph("8. Multi-Criteria Scoring", styles['TableCellBold']), Paragraph("Computes composite score combining ML (25%), Barrier (25%), Compatibility (15%), Shelf Life (15%), Mechanical (10%), Sustainability (10%). Applies barrier defect penalty.", styles['TableCell']), Paragraph("scoring_engine.py / scoring_weights.json", styles['TableCell'])],
        [Paragraph("9. Family Diversification", styles['TableCellBold']), Paragraph("Filters surviving candidates across 7 distinct material families (glass, metal, carton, foil laminate, tray, flexible pouch, rigid plastic) to ensure genuine choice.", styles['TableCell']), Paragraph("explanation_engine.py (_get_family)", styles['TableCell'])],
        [Paragraph("10. Explanation Synthesis", styles['TableCellBold']), Paragraph("Formulates positive evidence points, statutory citations, scientific warnings, and optional fluent narrative synthesized by Google Gemini 2.5 Flash.", styles['TableCell']), Paragraph("explanation_engine.py & llm_service.py", styles['TableCell'])],
    ]
    t = Table(pipe_data, colWidths=[100, 260, USABLE_WIDTH - 360])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t)
    
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("2.2 Output Contract for Top 3 Recommendations", styles['SubSecHeading']))
    elements.append(Paragraph(
        "Each recommended packaging option is returned with a comprehensive technical payload: "
        "Rank (#1, #2, #3), Material Name, Packaging Format, Derived Suitability Score (0-100), "
        "ML Suitability Score, Measured or Literature OTR & WVTR with source citations, Barrier Classification, "
        "Shelf-Life Validation Status (Fully Validated vs. Additional Validation Required), Thickness Specification (microns/gauge), "
        "Mechanical Strength (Tensile/Burst), Sustainability & Recyclability status (CPCB/EPR Category), "
        "Itemized Positive Evidence Points, Scientific Caveats & Warnings, and Statutory Document Citations.",
        styles['BodyCustom']
    ))
    
    elements.append(PageBreak())
    return elements


def build_section_3_architectural_innovation(styles):
    elements = []
    elements.append(Paragraph("3. SmartPack Architectural Innovation", styles['SecHeading']))
    elements.append(Paragraph(
        "A central trap in modern AI development is the uncritical deployment of Large Language Models (LLMs) or black-box classifiers "
        "for domain-critical engineering problems. In food packaging, recommending an illegal, unhygienic, or physically incompatible material "
        "can lead to massive commercial recalls, botulinum/microbial food poisoning, or statutory criminal prosecution under the Food Safety "
        "and Standards Act, 2006. SmartPack's innovation lies in its <b>decoupled, hybrid architecture</b>.",
        styles['BodyCustom']
    ))
    
    elements.append(Paragraph("3.1 Why a Simple Chatbot / Pure LLM Fails in Food Packaging", styles['SubSecHeading']))
    elements.append(Paragraph(
        "When an end-user prompts a standard conversational LLM (e.g. GPT-4, standard Gemini, or Llama) with a query like "
        "<i>'Recommend a cheap plastic pouch for potato chips to last 6 months'</i>, the LLM hallucinates plausible-sounding but catastrophic advice:",
        styles['BodyCustom']
    ))
    
    flaws = [
        "<b>Hallucinated Barrier Values:</b> LLMs frequently fabricate exact numerical OTR and WVTR values (e.g. 'OTR of 0.5 cc/m2/day for standard LDPE'), confusing polymers, test conditions, and material structures. In reality, standard LDPE has an OTR near 8,000 cc/m2/day—a 16,000-fold discrepancy that would spoil chips in 48 hours.",
        "<b>Violation of Statutory Prohibitions:</b> LLMs unaware of Indian environmental and food safety statutes will blithely recommend 'recycled PET pouches' for snacks. Under FSSAI Regulation 4(4) and IS 14534:1998, recycled plastics are strictly prohibited for direct food contact.",
        "<b>Suffocation of Living Produce:</b> LLMs often recommend high-barrier vacuum pouches or airtight metal cans for fresh fruits or carrots to 'maximize shelf life'. This cuts off oxygen, inducing rapid anaerobic tissue breakdown and catastrophic spoilage.",
        "<b>Non-Deterministic Outputs:</b> The same prompt submitted twice may yield conflicting packaging materials, making the system legally unviable for commercial quality assurance or industrial compliance."
    ]
    for f in flaws:
        elements.append(Paragraph(f"• {f}", styles['BulletCustom']))
        
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("3.2 The SmartPack Hybrid Separation of Concerns", styles['SubSecHeading']))
    elements.append(Paragraph(
        "SmartPack completely separates the <b>Deterministic Decision Engine</b> from the <b>Generative Explanation Engine</b>. "
        "The recommendation decision is 100% computed by deterministic rule filters, statutory lookups, physics heuristics, and the "
        "Scikit-Learn Random Forest model. The LLM has zero authority to add, remove, or re-rank packaging options; it operates solely "
        "as an authoritative technical writer, translating pipeline evidence into an accessible scientific explanation.",
        styles['BodyCustom']
    ))
    
    arch_comp = [
        [Paragraph("<b>Architectural Layer</b>", styles['TableHead']), Paragraph("<b>Engine Technology</b>", styles['TableHead']), Paragraph("<b>Operational Function</b>", styles['TableHead']), Paragraph("<b>Hallucination Risk</b>", styles['TableHead'])],
        [Paragraph("1. Statutory Safety", styles['TableCellBold']), Paragraph("Deterministic Rule Filters (IS / FSSAI)", styles['TableCell']), Paragraph("Applies hard statutory bans (IS 14534 recycled plastics ban, IS 2991 wax paper ban, acid etching limits)", styles['TableCell']), Paragraph("0.0% (Zero Risk)", styles['TableCellBold'])],
        [Paragraph("2. Biological Preservation", styles['TableCellBold']), Paragraph("Produce Respiration Interlock Heuristics", styles['TableCell']), Paragraph("Enforces breathability for respiring produce; bans airtight hermetic containers for live horticultural produce", styles['TableCell']), Paragraph("0.0% (Zero Risk)", styles['TableCellBold'])],
        [Paragraph("3. Data Ground Truth", styles['TableCellBold']), Paragraph("Curated Relational CSV Tables", styles['TableCell']), Paragraph("Retrieves verified nutritional composition (ICMR) and approved packaging forms (FSSAI Schedule IV)", styles['TableCell']), Paragraph("0.0% (Zero Risk)", styles['TableCellBold'])],
        [Paragraph("4. Algorithmic Fit", styles['TableCellBold']), Paragraph("Candidate-Specific Random Forest (23 features)", styles['TableCell']), Paragraph("Provides non-linear suitability scoring signal trained on domain interactions", styles['TableCell']), Paragraph("Bounded by tabular feature vector", styles['TableCell'])],
        [Paragraph("5. Transparent Ranking", styles['TableCellBold']), Paragraph("Multi-Criteria Weighted Linear Combiner", styles['TableCell']), Paragraph("Integrates ML, Barrier, Compatibility, Shelf-life, Mechanical, and Sustainability scores with defect penalty", styles['TableCell']), Paragraph("0.0% (Deterministic Math)", styles['TableCellBold'])],
        [Paragraph("6. Natural Language", styles['TableCellBold']), Paragraph("Google Gemini 2.5 Flash (Contextual Prompting)", styles['TableCell']), Paragraph("Synthesizes fluent explanation using strictly provided pipeline evidence without altering rankings", styles['TableCell']), Paragraph("Strictly Grounded (Evidence Injection)", styles['TableCell'])],
    ]
    t_arch = Table(arch_comp, colWidths=[90, 130, 200, USABLE_WIDTH - 420])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_arch)
    
    elements.append(PageBreak())
    return elements


def build_section_4_dataset_engineering(styles):
    elements = []
    elements.append(Paragraph("4. Dataset Inventory & Data Engineering", styles['SecHeading']))
    elements.append(Paragraph(
        "A rigorous audit was conducted across all datasets present in the repository (`Claude-DataSet/` and `data/`). "
        "No columns, rows, or values were assumed or invented. The actual source files were parsed, profiled, and mapped "
        "into the backend architecture. Below is the complete catalog of all 16 datasets utilized across the system.",
        styles['BodyCustom']
    ))
    
    ds_data = [
        [Paragraph("<b>Dataset Filename</b>", styles['TableHead']), Paragraph("<b>Rows</b>", styles['TableHead']), Paragraph("<b>Cols</b>", styles['TableHead']), Paragraph("<b>Primary Source</b>", styles['TableHead']), Paragraph("<b>Core Contents & Usage in SmartPack</b>", styles['TableHead'])],
        [Paragraph("01_food_dataset.csv", styles['TableCellMono']), Paragraph("496", styles['TableCellBold']), Paragraph("28", styles['TableCell']), Paragraph("ICMR-NIN IFCT 2017", styles['TableCell']), Paragraph("Nutritional composition (moisture, protein, fat, fiber, ash, energy). Used for auto-completing food properties in input form.", styles['TableCell'])],
        [Paragraph("02_food_quality_dataset.csv", styles['TableCellMono']), Paragraph("1,506", styles['TableCellBold']), Paragraph("12", styles['TableCell']), Paragraph("AGMARK Compendia", styles['TableCell']), Paragraph("Quality grading specifications (organic/inorganic foreign matter, sizing, moisture limits) across food grains, pulses, spices.", styles['TableCell'])],
        [Paragraph("03_contamination_dataset.csv", styles['TableCellMono']), Paragraph("1,359", styles['TableCellBold']), Paragraph("11", styles['TableCell']), Paragraph("FSSAI Contaminants Regs", styles['TableCell']), Paragraph("Maximum permitted limits for heavy metals (lead, copper, arsenic, cadmium), mycotoxins, natural toxins across commodities.", styles['TableCell'])],
        [Paragraph("04_storage_dataset.csv", styles['TableCellMono']), Paragraph("8", styles['TableCellBold']), Paragraph("16", styles['TableCell']), Paragraph("ICAR / AGMARK / BIS", styles['TableCell']), Paragraph("Recommended cold storage temperatures, gas atmospheres, and duration benchmarks for chilled/frozen meats, fish, and produce.", styles['TableCell'])],
        [Paragraph("05_shelf_life_dataset.csv", styles['TableCellMono']), Paragraph("26", styles['TableCellBold']), Paragraph("18", styles['TableCell']), Paragraph("ICAR Post-Harvest AR", styles['TableCell']), Paragraph("Measured shelf-life benchmarks across fresh vs. treated/retort packaged foods (soy paneer, fish fingers, nut butters).", styles['TableCell'])],
        [Paragraph("06_packaging_material_dataset.csv", styles['TableCellMono']), Paragraph("26", styles['TableCellBold']), Paragraph("21", styles['TableCell']), Paragraph("FSSAI / BIS Handbook", styles['TableCell']), Paragraph("Catalog of packaging materials (PET, HDPE, LDPE, PP, Foil, Paperboard, Glass) with primary/secondary designations and recyclability.", styles['TableCell'])],
        [Paragraph("07_packaging_properties_dataset_Claude.csv", styles['TableCellMono']), Paragraph("85", styles['TableCellBold']), Paragraph("12", styles['TableCell']), Paragraph("BIS Standards (IS 10146+)", styles['TableCell']), Paragraph("Physical/mechanical specifications: burst index, tensile strength, tear index, pH, moisture content across paperboard & polymers.", styles['TableCell'])],
        [Paragraph("08_barrier_properties_dataset.csv", styles['TableCellMono']), Paragraph("2", styles['TableCellBold']), Paragraph("21", styles['TableCell']), Paragraph("BIS (IS 5012:1987)", styles['TableCell']), Paragraph("Water vapour transmission rate (WVTR) for coated cellulose film (30 g/m2/day creased, 15 uncreased). OTR unmeasured in raw extract.", styles['TableCell'])],
        [Paragraph("09_food_packaging_compatibility_MERGED.csv", styles['TableCellMono']), Paragraph("50", styles['TableCellBold']), Paragraph("18", styles['TableCell']), Paragraph("FSSAI / ICAR / BIS", styles['TableCell']), Paragraph("Compatibility pairs mapping food categories to packaging types, documenting lipid oxidation risks and migration concerns.", styles['TableCell'])],
        [Paragraph("10_packaging_shelf_life_dataset.csv", styles['TableCellMono']), Paragraph("17", styles['TableCellBold']), Paragraph("19", styles['TableCell']), Paragraph("ICAR-DARE Trials", styles['TableCell']), Paragraph("Empirical shelf-life extension records comparing unpackaged baselines with retort pouches, vacuum packs, and MAP films.", styles['TableCell'])],
        [Paragraph("11_sustainability_dataset.csv", styles['TableCellMono']), Paragraph("11", styles['TableCellBold']), Paragraph("16", styles['TableCell']), Paragraph("BIS / CPCB / MoEFCC", styles['TableCell']), Paragraph("Circularity profiles: recyclability, compostability, biodegradability, renewable resource origin, and waste management routes.", styles['TableCell'])],
        [Paragraph("12_recyclability_dataset.csv", styles['TableCellMono']), Paragraph("6", styles['TableCellBold']), Paragraph("13", styles['TableCell']), Paragraph("CPCB / PWM Rules 2016", styles['TableCell']), Paragraph("Categorization of plastics into EPR Categories I, II, III with recycling routes (mechanical recycling per IS 14534 vs. energy recovery).", styles['TableCell'])],
        [Paragraph("13_regulatory_rules.csv", styles['TableCellMono']), Paragraph("20", styles['TableCellBold']), Paragraph("16", styles['TableCell']), Paragraph("FSSAI / BIS Mandates", styles['TableCell']), Paragraph("Statutory prohibitions: recycled plastics ban (IS 14534), overall migration limit (60 mg/kg per IS 9845), heavy metal limits.", styles['TableCell'])],
        [Paragraph("14_recommended_packaging.csv", styles['TableCellMono']), Paragraph("102", styles['TableCellBold']), Paragraph("13", styles['TableCell']), Paragraph("FSSAI Schedule IV & ICAR", styles['TableCell']), Paragraph("Ground-truth mapping connecting 10 food categories to officially recommended packaging materials and forms.", styles['TableCell'])],
        [Paragraph("15_MASTER_ML_DATASET.csv", styles['TableCellMono']), Paragraph("17", styles['TableCellBold']), Paragraph("34", styles['TableCell']), Paragraph("ICAR Trial Extracts", styles['TableCell']), Paragraph("Experimental trials linking food, package, and shelf-life observations. Serves as biological ground-truth anchor.", styles['TableCell'])],
        [Paragraph("16_material_barrier_mechanical_reference.csv", styles['TableCellMono']), Paragraph("20", styles['TableCellBold']), Paragraph("17", styles['TableCell']), Paragraph("Standard Literature (Selke)", styles['TableCell']), Paragraph("Validated literature benchmarks for 20 polymer families (REF-01 to REF-20) providing published OTR, WVTR, and tensile values.", styles['TableCell'])],
    ]
    t_ds = Table(ds_data, colWidths=[120, 24, 22, 100, USABLE_WIDTH - 266])
    t_ds.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(t_ds)
    
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("4.2 Source Hierarchy & Institutional Authority", styles['SubSecHeading']))
    elements.append(Paragraph(
        "SmartPack structures its data sources according to a strict legal and scientific hierarchy: "
        "<b>1. Statutory Regulations (FSSAI / MoEFCC):</b> Mandatory legal limits under the Food Safety and Standards Act, 2006, and Plastic Waste Management Rules, 2016. "
        "<b>2. National Standardization (BIS):</b> Testing protocols and material purity standards (IS 10146 for PE, IS 10151 for PP, IS 9845 for migration, IS 14534 for recycling). "
        "<b>3. Agricultural & Nutritional Research (ICMR-NIN / ICAR):</b> Empirical food composition tables (IFCT 2017) and post-harvest storage trial reports. "
        "<b>4. Peer-Reviewed Packaging Literature (Robertson 2012, Selke 2004):</b> Standard baseline permeation constants for commercial polymers.",
        styles['BodyCustom']
    ))
    
    elements.append(PageBreak())
    return elements


def build_section_5_data_quality_and_limitations(styles):
    elements = []
    elements.append(Paragraph("5. Data Quality, Integrity & Limitations", styles['SecHeading']))
    elements.append(Paragraph(
        "A critical requirement for SIH evaluation is absolute technical honesty. Many hackathon projects claim to possess "
        "'complete laboratory measurements for all food materials'. SmartPack rejects this pretense. Real-world food science "
        "data is characterized by significant gaps, non-standardized test conditions, and missing parameters. "
        "SmartPack classifies every data attribute into one of five rigorous tiers.",
        styles['BodyCustom']
    ))
    
    elements.append(Paragraph("5.1 Data Availability Classification Matrix", styles['SubSecHeading']))
    
    qual_data = [
        [Paragraph("<b>Data Domain</b>", styles['TableHead']), Paragraph("<b>Classification</b>", styles['TableHead']), Paragraph("<b>Source Coverage Reality</b>", styles['TableHead']), Paragraph("<b>SmartPack Handling Protocol</b>", styles['TableHead'])],
        [Paragraph("Food Nutritional Composition", styles['TableCellBold']), Paragraph("AVAILABLE", styles['TableCellBold']), Paragraph("496 foods in 01_food_dataset.csv with exact moisture, fat, protein, fiber, ash from ICMR IFCT 2017.", styles['TableCell']), Paragraph("Direct numerical lookup; populates baseline moisture and fat sensitivity.", styles['TableCell'])],
        [Paragraph("Food pH & Water Activity (aw)", styles['TableCellBold']), Paragraph("PARTIALLY AVAILABLE", styles['TableCellBold']), Paragraph("100% missing from raw ICMR CSV. Derived from standard food category reference bounds.", styles['TableCell']), Paragraph("Defaults to category averages (e.g. 6.0 for cereals, 3.8 for fruits); user override permitted.", styles['TableCell'])],
        [Paragraph("Produce Respiration Rates", styles['TableCellBold']), Paragraph("AVAILABLE", styles['TableCellBold']), Paragraph("Post-harvest reference database maps horticultural produce to exact respiration classes and rates.", styles['TableCell']), Paragraph("Automatic lookup by food name (e.g. Carrot: Medium, Apple: Low, Broccoli: High).", styles['TableCell'])],
        [Paragraph("Packaging Tensile & Bursting", styles['TableCellBold']), Paragraph("AVAILABLE", styles['TableCellBold']), Paragraph("85 property specs in 07_packaging_properties_dataset_Claude.csv from BIS standards.", styles['TableCell']), Paragraph("Extracted into mechanical_properties; used for physical integrity scoring.", styles['TableCell'])],
        [Paragraph("Oxygen Transmission Rate (OTR)", styles['TableCellBold']), Paragraph("MISSING IN RAW / AVAILABLE IN REF", styles['TableCellBold']), Paragraph("100% missing across plastics in 08_barrier_properties_dataset.csv. Added via 16_material_barrier_mechanical_reference.csv.", styles['TableCell']), Paragraph("Displays published literature value with full citation; unmeasured marked as 'Data unavailable'.", styles['TableCell'])],
        [Paragraph("Water Vapor Trans. Rate (WVTR)", styles['TableCellBold']), Paragraph("PARTIALLY AVAILABLE", styles['TableCellBold']), Paragraph("Present for cellulose film in 08_barrier_properties_dataset.csv; polymer values mapped via reference table.", styles['TableCell']), Paragraph("Displays exact test conditions (38°C, 90% RH) when available; never fabricates fake numbers.", styles['TableCell'])],
        [Paragraph("Empirical Shelf Life (Trials)", styles['TableCellBold']), Paragraph("PARTIALLY AVAILABLE", styles['TableCellBold']), Paragraph("26 shelf-life rows in 05_shelf_life_dataset.csv and 17 in 10_packaging_shelf_life_dataset.csv.", styles['TableCell']), Paragraph("Accounts for validation mismatch: if target > benchmark, flags 'Additional validation required'.", styles['TableCell'])],
        [Paragraph("ML Training Labels", styles['TableCellBold']), Paragraph("SYNTHETIC / DOMAIN-GROUNDED", styles['TableCellBold']), Paragraph("600 rows generated from physics-based permeation, respiration, and FSSAI rules.", styles['TableCell']), Paragraph("Explicitly disclosed as prototype synthetic target; not claimed as lab experiments.", styles['TableCell'])],
    ]
    t_q = Table(qual_data, colWidths=[95, 95, 160, USABLE_WIDTH - 350])
    t_q.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_q)
    
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("5.2 Why OTR and WVTR Cannot Be Fabricated", styles['SubSecHeading']))
    elements.append(Paragraph(
        "Oxygen Transmission Rate (OTR) and Water Vapor Transmission Rate (WVTR) are **material performance properties**, "
        "not food composition attributes. They cannot be calculated via a regression formula from food moisture or pH. "
        "Permeation is governed by polymer morphology, crystallinity, orientation (e.g. BOPP vs. cast PP), co-extrusion layers, "
        "metallization optical density, aluminum foil pinhole integrity, plasticizer content, and film thickness gauge. "
        "Furthermore, transmission rates vary exponentially with temperature and relative humidity per the Arrhenius relationship. "
        "SmartPack enforces a strict **Zero-Fabrication Data Integrity Protocol**: when an exact empirical test value is absent from "
        "the database, the UI displays <i>'Data unavailable'</i> or references published peer-reviewed polymer ranges, "
        "ensuring the user is never misled into a false sense of barrier security.",
        styles['BodyCustom']
    ))
    
    callout = create_callout(
        "AUDIT PRINCIPLE: TRANSPARENT SHELF-LIFE VALIDATION",
        "If a food processor requests a 180-day shelf life for a snack, and FSSAI Schedule IV lists a laminate pouch with a 90-day "
        "validated benchmark, SmartPack does NOT pretend the packaging guarantees 180 days. Instead, the scoring engine discounts "
        "the shelf-life score, labels the status as 'ADDITIONAL VALIDATION REQUIRED', and generates an explicit warning: "
        "'Target shelf life (180 days) exceeds validated source benchmark (90 days). Additional real-time or accelerated shelf-life "
        "testing is required.'",
        style_type="warning",
        styles=styles
    )
    elements.append(callout)
    
    elements.append(PageBreak())
    return elements
