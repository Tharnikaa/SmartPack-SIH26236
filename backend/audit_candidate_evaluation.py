"""
Audit Candidate Evaluation Script
Demonstrates commodity x packaging x storage x shelf-life x requirements evaluation
for Carrot, Apple, and Potato across at least 3 candidates each.
"""

import sys
import json
sys.path.insert(0, 'backend')

from app.services.data_service import data_service
data_service.load_all_datasets()

from app.logic.requirement_engine import requirement_engine
from app.logic.candidate_generator import CandidateGenerator
from app.logic.constraint_filter import constraint_filter
from app.logic.scoring_engine import scoring_engine
from app.logic.explanation_engine import explanation_engine
from app.ml.preprocessing import feature_pipeline

test_cases = [
    {
        "food_name": "Carrot",
        "food_category": "Fruit & Vegetable products",
        "moisture_level": 88.0,
        "fat_oil_sensitivity": "Low",
        "ph": 6.0,
        "respiration_activity": "Moderate",
        "desired_shelf_life_days": 28,
        "storage_temperature_c": 5.0,
        "relative_humidity_pct": 95.0,
        "storage_condition": "Chilled",
        "transport_condition": "Ambient / Road",
        "map_required": "No",
        "sustainability_priority": "Standard",
        "preferred_package_type": "Any"
    },
    {
        "food_name": "Apple",
        "food_category": "Fruit & Vegetable products",
        "moisture_level": 84.0,
        "fat_oil_sensitivity": "Low",
        "ph": 3.8,
        "respiration_activity": "Low",
        "desired_shelf_life_days": 90,
        "storage_temperature_c": 2.0,
        "relative_humidity_pct": 90.0,
        "storage_condition": "Chilled",
        "transport_condition": "Rough / Long-Distance",
        "map_required": "Optional",
        "sustainability_priority": "High (Recyclable)",
        "preferred_package_type": "Any"
    },
    {
        "food_name": "Potato",
        "food_category": "Fruit & Vegetable products",
        "moisture_level": 79.0,
        "fat_oil_sensitivity": "Low",
        "ph": 5.8,
        "respiration_activity": "Low",
        "desired_shelf_life_days": 120,
        "storage_temperature_c": 10.0,
        "relative_humidity_pct": 85.0,
        "storage_condition": "Ambient",
        "transport_condition": "Ambient / Road",
        "map_required": "No",
        "sustainability_priority": "Standard",
        "preferred_package_type": "Any"
    }
]

cg = CandidateGenerator()
feat_names = feature_pipeline.feature_names

print("=" * 100)
print("SMARTPACK: CANDIDATE-SPECIFIC MULTI-CRITERIA EVALUATION AUDIT")
print("Commodity x Packaging x Storage x Shelf-Life x Requirements")
print("=" * 100)

all_results = []

for case in test_cases:
    commodity_name = case["food_name"]
    print(f"\n{'#' * 100}")
    print(f"COMMODITY: {commodity_name.upper()} | Moisture: {case['moisture_level']}% | Respiration: {case['respiration_activity']} | Target Shelf Life: {case['desired_shelf_life_days']} days @ {case['storage_temperature_c']}°C")
    print(f"{'#' * 100}")

    reqs = requirement_engine.compute_requirements(case)
    candidates = cg.generate_candidates(case, reqs)
    surviving, rejected = constraint_filter.apply_filters(candidates, case, reqs)

    print(f"\nFunnel Summary: {len(candidates)} generated | {len(rejected)} rejected by hard filters | {len(surviving)} surviving candidates")

    # Score surviving candidates
    scored = []
    for cand in surviving:
        s_res = scoring_engine.score_candidate(cand, case, reqs)
        scored.append({**cand, "scoring": s_res})

    scored.sort(key=lambda x: x["scoring"]["final_suitability_score"], reverse=True)

    # Detailed audit logging for at least 3 candidates
    for idx, cand in enumerate(scored[:4]):
        s = cand["scoring"]
        breakdown = s["score_breakdown"]
        raw_feats = feature_pipeline.extract_features(case, reqs, cand)

        # Respiration compatibility factor
        resp_compat_val = raw_feats[feat_names.index("respiration_compatibility")]

        print(f"\n{'-' * 80}")
        print(f"Candidate #{idx + 1}: {cand['material']}")
        print(f"Packaging Type: {cand['packaging_type']}")
        print(f"Primary Packaging: {cand.get('primary_packaging')}")
        print(f"Secondary Packaging: {cand.get('secondary_packaging')}")
        print(f"Hard-Filter Status: PASSED (SURVIVED)")
        print(f"\n[ML Input Feature Vector] (23 dimensions):")
        for fname, fval in zip(feat_names, raw_feats):
            print(f"    {fname:28}: {fval}")

        print(f"\n[Multi-Criteria & ML Evaluation Scores]:")
        print(f"    ML Suitability Score       : {breakdown['ml_score'] * 100:.1f} / 100 (ML={breakdown['ml_score']:.4f})")
        print(f"    Barrier Score              : {breakdown['barrier_score'] * 100:.1f} / 100 (Score={breakdown['barrier_score']:.3f})")
        print(f"    Compatibility Score        : {breakdown['compatibility_score'] * 100:.1f} / 100 (Score={breakdown['compatibility_score']:.3f})")
        print(f"    Shelf-Life Score           : {breakdown['shelf_life_score'] * 100:.1f} / 100 (Score={breakdown['shelf_life_score']:.3f})")
        print(f"    Mechanical Score           : {breakdown['mechanical_score'] * 100:.1f} / 100 (Score={breakdown['mechanical_score']:.3f})")
        print(f"    Sustainability Score       : {breakdown['sustainability_score'] * 100:.1f} / 100 (Score={breakdown['sustainability_score']:.3f})")
        print(f"    Respiration Compatibility  : {resp_compat_val:.2f} / 1.00")
        print(f"    FINAL DERIVED SCORE        : {s['final_suitability_score']:.1f} / 100")
        print(f"    Mechanical Units Checked   : Tensile={cand['mechanical_properties'].get('tensile_strength')} | Burst={cand['mechanical_properties'].get('burst_strength')}")
        print(f"    Shelf-Life DB Checked      : Expected DB={cand.get('expected_shelf_life')}")

        all_results.append({
            "commodity": commodity_name,
            "candidate": cand["material"],
            "packaging_type": cand["packaging_type"],
            "primary_packaging": cand.get("primary_packaging"),
            "secondary_packaging": cand.get("secondary_packaging"),
            "ml_score": round(breakdown["ml_score"] * 100, 1),
            "barrier_score": round(breakdown["barrier_score"] * 100, 1),
            "compatibility_score": round(breakdown["compatibility_score"] * 100, 1),
            "shelf_life_score": round(breakdown["shelf_life_score"] * 100, 1),
            "mechanical_score": round(breakdown["mechanical_score"] * 100, 1),
            "sustainability_score": round(breakdown["sustainability_score"] * 100, 1),
            "respiration_compatibility": round(resp_compat_val, 2),
            "hard_filter_status": "PASSED",
            "final_score": s["final_suitability_score"]
        })

print("\n" + "=" * 115)
print("SYNTHESIS TABLE: ALL COMMODITIES & CANDIDATE PACKAGING OPTIONS")
print("=" * 115)
header = f"{'Commodity':<8} | {'Candidate Packaging':<32} | {'ML':<5} | {'Bar':<5} | {'Comp':<5} | {'SL':<5} | {'Mech':<5} | {'Sust':<5} | {'Resp':<5} | {'Final':<5}"
print(header)
print("-" * len(header))
for r in all_results:
    print(f"{r['commodity']:<8} | {r['candidate'][:32]:<32} | {r['ml_score']:<5} | {r['barrier_score']:<5} | {r['compatibility_score']:<5} | {r['shelf_life_score']:<5} | {r['mechanical_score']:<5} | {r['sustainability_score']:<5} | {r['respiration_compatibility']:<5} | {r['final_score']:<5}")
print("=" * 115)
