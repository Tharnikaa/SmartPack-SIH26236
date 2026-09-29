"""
Master Orchestrator to generate SmartPack_SIH26236_Complete_Technical_Documentation.pdf.
Imports all 5 modular sections and builds the complete, professional, publication-grade document.
"""

import os
import sys
import time
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate

from docs_generator.styles import (
    NumberedCanvas, get_smartpack_styles, MARGIN
)
from docs_generator.sections_part1 import (
    build_cover_page, build_executive_summary_and_toc,
    build_section_1_problem_statement, build_section_2_proposed_solution,
    build_section_3_architectural_innovation, build_section_4_dataset_engineering,
    build_section_5_data_quality_and_limitations
)
from docs_generator.sections_part2 import (
    build_section_6_machine_learning_pipeline, build_section_7_feature_engineering,
    build_section_8_requirement_engine, build_section_9_candidate_generation,
    build_section_10_regulatory_constraint_filter, build_section_11_scoring_engine,
    build_section_12_top3_recommendation_logic
)
from docs_generator.sections_part3 import (
    build_section_13_llm_explanation_layer, build_section_14_otr_and_wvtr_deep_dive,
    build_section_15_technology_stack, build_section_16_17_system_architecture_and_flows,
    build_section_18_api_specifications, build_section_19_codebase_structure
)
from docs_generator.sections_part4 import (
    build_section_20_test_cases, build_section_21_known_issues_and_resolution,
    build_section_22_23_security_and_performance, build_section_24_sustainability_and_epr,
    build_section_25_26_limitations_and_future_scope
)
from docs_generator.sections_part5 import (
    build_section_27_end_to_end_walkthrough, build_section_28_why_hybrid_ai,
    build_section_29_hackathon_presentation_and_viva, build_section_30_final_positioning
)

def generate_pdf(output_filename="SmartPack_SIH26236_Complete_Technical_Documentation.pdf"):
    start_time = time.time()
    print(f"Starting PDF generation: {output_filename}")
    
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=38,
        bottomMargin=38
    )

    styles = get_smartpack_styles()
    story = []

    print("Building Part 1: Cover, Executive Summary, TOC, Sections 1-5...")
    story.extend(build_cover_page(styles))
    story.extend(build_executive_summary_and_toc(styles))
    story.extend(build_section_1_problem_statement(styles))
    story.extend(build_section_2_proposed_solution(styles))
    story.extend(build_section_3_architectural_innovation(styles))
    story.extend(build_section_4_dataset_engineering(styles))
    story.extend(build_section_5_data_quality_and_limitations(styles))

    print("Building Part 2: Sections 6-12 (ML, Features, Requirements, Rules, Scoring, Top 3)...")
    story.extend(build_section_6_machine_learning_pipeline(styles))
    story.extend(build_section_7_feature_engineering(styles))
    story.extend(build_section_8_requirement_engine(styles))
    story.extend(build_section_9_candidate_generation(styles))
    story.extend(build_section_10_regulatory_constraint_filter(styles))
    story.extend(build_section_11_scoring_engine(styles))
    story.extend(build_section_12_top3_recommendation_logic(styles))

    print("Building Part 3: Sections 13-19 (LLM, OTR/WVTR, Tech Stack, Architecture, API, Codebase)...")
    story.extend(build_section_13_llm_explanation_layer(styles))
    story.extend(build_section_14_otr_and_wvtr_deep_dive(styles))
    story.extend(build_section_15_technology_stack(styles))
    story.extend(build_section_16_17_system_architecture_and_flows(styles))
    story.extend(build_section_18_api_specifications(styles))
    story.extend(build_section_19_codebase_structure(styles))

    print("Building Part 4: Sections 20-26 (Test Cases, Known Issues, Security, Sustainability, Roadmap)...")
    story.extend(build_section_20_test_cases(styles))
    story.extend(build_section_21_known_issues_and_resolution(styles))
    story.extend(build_section_22_23_security_and_performance(styles))
    story.extend(build_section_24_sustainability_and_epr(styles))
    story.extend(build_section_25_26_limitations_and_future_scope(styles))

    print("Building Part 5: Sections 27-30 (End-to-End Walkthrough, Hybrid AI, Viva Guide, Final Positioning)...")
    story.extend(build_section_27_end_to_end_walkthrough(styles))
    story.extend(build_section_28_why_hybrid_ai(styles))
    story.extend(build_section_29_hackathon_presentation_and_viva(styles))
    story.extend(build_section_30_final_positioning(styles))

    print(f"Total flowable elements assembled: {len(story)}")
    print("Compiling document via NumberedCanvas...")
    doc.build(story, canvasmaker=NumberedCanvas)

    elapsed = round(time.time() - start_time, 2)
    file_size_kb = round(os.path.getsize(output_filename) / 1024, 1)
    print(f"SUCCESS: PDF created at '{output_filename}' ({file_size_kb} KB) in {elapsed}s")

if __name__ == "__main__":
    generate_pdf()
