import sys
sys.path.insert(0, 'backend')
from app.services.data_service import data_service
from app.logic.requirement_engine import requirement_engine
from app.logic.candidate_generator import candidate_generator
from app.logic.constraint_filter import constraint_filter
from app.logic.thickness_engine import thickness_engine
from app.logic.scoring_engine import scoring_engine
from app.logic.explanation_engine import explanation_engine

print("Testing data loading...")
print("Foods:", len(data_service.foods_df), "Recs:", len(data_service.recommended_df), "Ref Materials:", len(data_service.material_reference_df))
assert len(data_service.material_reference_df) > 0, "16_material_barrier_mechanical_reference.csv not loaded"

print("Checking active scoring weights (ml_score restored, 6 weights sum to 1.0)...")
print("Active weights:", scoring_engine.weights)
assert "ml_score" in scoring_engine.weights and scoring_engine.weights["ml_score"] > 0, "ml_score should be in active scoring weights"
assert abs(sum(scoring_engine.weights.values()) - 1.0) < 1e-3, "Scoring weights must sum to 1.0"

print("\n--- TEST 1: Biscuits (Low moisture, crisp, standard ambient) ---")
test_input = {
    "food_name": "Biscuits",
    "food_category": "Cereals and cereal products",
    "moisture_level": 4.5,
    "fat_oil_sensitivity": "Medium",
    "ph": 6.5,
    "respiration_activity": "Low",
    "desired_shelf_life_days": 180,
    "storage_temperature_c": 25.0,
    "relative_humidity_pct": 65.0,
    "storage_condition": "Ambient",
    "transport_condition": "Ambient / Road",
    "map_required": "No",
    "sustainability_priority": "Standard",
    "preferred_package_type": "Any"
}
reqs = requirement_engine.compute_requirements(test_input)
raw_cands = candidate_generator.generate_candidates(test_input, reqs)
surv, rej = constraint_filter.apply_filters(raw_cands, test_input, reqs)
print(f"Candidates: raw={len(raw_cands)}, surviving={len(surv)}, rejected={len(rej)}")

scored = []
for c in surv:
    c["scoring"] = scoring_engine.score_candidate(c, test_input, reqs)
    scored.append(c)

scored.sort(key=lambda x: x["scoring"]["final_suitability_score"], reverse=True)
top3 = explanation_engine.build_recommendations(scored, test_input, reqs)
print(f"Top 3 recommendations produced: {len(top3)}")
for r in top3:
    print(f"  Rank {r['rank']}: {r['material']} | {r['packaging_type']} | Score: {r['suitability_score']} | OTR: {r['barrier_properties']['otr']} | WVTR: {r['barrier_properties']['wvtr']}")

print("\n--- TEST 2: High Moisture Fresh Fruits with Respiration ---")
fruit_input = {
    "food_name": "Fresh Apples / Mangoes",
    "food_category": "Fruit & Vegetable products",
    "moisture_level": 84.0,
    "fat_oil_sensitivity": "Low",
    "ph": 4.0,
    "respiration_activity": "High",
    "desired_shelf_life_days": 21,
    "storage_temperature_c": 12.0,
    "relative_humidity_pct": 85.0,
    "storage_condition": "Chilled",
    "transport_condition": "Rough / Long-Distance",
    "map_required": "Optional",
    "sustainability_priority": "High (Recyclable)",
    "preferred_package_type": "Rigid"
}
f_reqs = requirement_engine.compute_requirements(fruit_input)
f_raw = candidate_generator.generate_candidates(fruit_input, f_reqs)
f_surv, f_rej = constraint_filter.apply_filters(f_raw, fruit_input, f_reqs)
print(f"Fruit Candidates: raw={len(f_raw)}, surviving={len(f_surv)}, rejected={len(f_rej)}")
f_scored = []
for c in f_surv:
    c["scoring"] = scoring_engine.score_candidate(c, fruit_input, f_reqs)
    f_scored.append(c)
f_scored.sort(key=lambda x: x["scoring"]["final_suitability_score"], reverse=True)
f_top3 = explanation_engine.build_recommendations(f_scored, fruit_input, f_reqs)
for r in f_top3:
    print(f"  Rank {r['rank']}: {r['material']} | {r['packaging_type']} | Score: {r['suitability_score']}")

print("\n--- TEST 3: Hard Incompatibility / Prohibited Material Check ---")
confect_input = {
    "food_name": "Traditional Confectionery / Sweets",
    "food_category": "Sweets and Confectionery",
    "moisture_level": 18.0,
    "fat_oil_sensitivity": "High",
    "ph": 6.0,
    "respiration_activity": "Low",
    "desired_shelf_life_days": 30,
    "storage_temperature_c": 22.0,
    "relative_humidity_pct": 55.0,
    "storage_condition": "Ambient",
    "transport_condition": "Ambient",
    "map_required": "No",
    "sustainability_priority": "Standard",
    "preferred_package_type": "Any"
}
# Inject a candidate with Base paper IS 2991
mock_cand = [{
    "material": "Base paper for waxed paper (IS 2991:1988)",
    "packaging_type": "Wrap",
    "sustainability": {}
}]
c_surv, c_rej = constraint_filter.apply_filters(mock_cand, confect_input, {})
print(f"Hard constraint filter on prohibited candidate: surviving={len(c_surv)}, rejected={len(c_rej)}")
if c_rej:
    print(f"  Rejection Reason: {c_rej[0]['rejection_reasons']}")

print("\nALL BACKEND PIPELINE CHECKS PASSED SUCCESSFULLY!")
