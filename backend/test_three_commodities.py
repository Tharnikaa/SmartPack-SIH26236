import sys
import json
sys.path.insert(0, 'backend')

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

commodities_test_inputs = [
    {
        "food_name": "Carrot",
        "food_category": "Fruit & Vegetable products",
        "moisture_level": 88.0,
        "fat_oil_sensitivity": "Low",
        "ph": 6.0,
        "respiration_activity": "Moderate",  # Kader: 10-20 mg CO2/kg/hr at 5C
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
        "respiration_activity": "Low",  # Kader: 5-10 mg CO2/kg/hr at 0-5C
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
        "respiration_activity": "Low",  # Kader: 5-10 mg CO2/kg/hr at 5C
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

comparison_rows = []

print("="*80)
print("SMARTPACK: THREE-COMMODITY AUDIT TEST (CARROT, APPLE, POTATO)")
print("="*80)

for inp in commodities_test_inputs:
    print(f"\n" + "-"*80)
    print(f"ANALYZING: {inp['food_name']} ({inp['food_category']})")
    print("-"*80)
    
    res = client.post("/api/analyze", json=inp)
    assert res.status_code == 200, f"Failed for {inp['food_name']}: {res.text}"
    data = res.json()
    
    reqs = data.get("requirements", {})
    recs = data.get("recommendations", [])
    debug = data.get("debug", {})
    funnel = debug.get("candidate_funnel", {})
    resp_prof = reqs.get("respiration_profile") or {}
    
    print(f"Moisture: {inp['moisture_level']}% | pH: {inp['ph']} | Fat/Oil: {inp['fat_oil_sensitivity']}")
    print(f"Respiration: {resp_prof.get('respiration_class', 'N/A')} (lookup: {resp_prof.get('canonical_commodity', 'N/A')}, rate: {resp_prof.get('rate_min')}-{resp_prof.get('rate_max')} {resp_prof.get('rate_unit')} @ {resp_prof.get('temperature_c')}C)")
    print(f"Temperature: {inp['storage_temperature_c']}C | RH: {inp['relative_humidity_pct']}% | Shelf Life: {inp['desired_shelf_life_days']} days | MAP: {inp['map_required']}")
    print(f"Calculated Target OTR: {reqs.get('target_otr_cc_m2_day')} | Target WVTR: {reqs.get('target_wvtr_g_m2_day')} | Gas Req: {reqs.get('map_gas_requirement', {}).get('level')}")
    
    print(f"\nCandidate Funnel:")
    print(f"  FSSAI Candidates Generated: {funnel.get('initial_generated')}")
    print(f"  Rejected by Hard Constraints: {funnel.get('rejected_count')}")
    print(f"  Surviving Candidates Scored: {funnel.get('after_hard_constraint_filtering')}")
    
    print(f"\nTop 3 Recommended Packaging:")
    for r in recs:
        factors = {f['factor']: round(f['score'], 2) for f in r.get("contributing_factors", [])}
        print(f"  Rank #{r['rank']}: {r['material']}")
        print(f"    Type: {r['packaging_type']} | Score: {r['suitability_score']}")
        print(f"    Scores: ML={factors.get('ML Suitability Model')} | Barrier={factors.get('Barrier Protection')} | Compat={factors.get('Compatibility & Safety')} | ShelfLife={factors.get('Shelf-Life Preservation')} | Mech={factors.get('Mechanical Robustness')} | Sust={factors.get('Sustainability')}")
        print(f"    OTR: {r['barrier_properties']['otr']} ({r['barrier_properties']['data_status']}) | WVTR: {r['barrier_properties']['wvtr']}")
        print(f"    Evidence: {r.get('evidence_points', [])[:3]}")

    top1 = recs[0] if recs else None
    top1_name = f"{top1['material']} ({top1['packaging_type']})" if top1 else "None"
    top1_score = top1['suitability_score'] if top1 else 0.0
    
    comparison_rows.append({
        "Commodity": inp["food_name"],
        "Respiration": resp_prof.get("respiration_class", inp["respiration_activity"]),
        "MAP": inp["map_required"],
        "Candidate Count": funnel.get("after_hard_constraint_filtering"),
        "Top 1": top1_name,
        "Score": top1_score
    })

print("\n" + "="*80)
print("FINAL COMPARISON SUMMARY TABLE")
print("="*80)
header = f"{'Commodity':<12} | {'Respiration':<12} | {'MAP':<6} | {'Candidates':<10} | {'Score':<6} | {'Top 1 Packaging'}"
print(header)
print("-" * len(header) + "-"*40)
for row in comparison_rows:
    print(f"{row['Commodity']:<12} | {row['Respiration']:<12} | {row['MAP']:<6} | {row['Candidate Count']:<10} | {row['Score']:<6} | {row['Top 1']}")
print("="*80)
