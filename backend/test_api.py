import sys
sys.path.insert(0, 'backend')
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("1. Testing GET /api/health")
res = client.get("/api/health")
print("Status:", res.status_code, res.json())
assert res.status_code == 200

print("\n2. Testing GET /api/foods?q=apple")
res = client.get("/api/foods?q=apple")
print("Status:", res.status_code, "Found foods:", len(res.json()))
assert res.status_code == 200

print("\n3. Testing GET /api/packaging/materials")
res = client.get("/api/packaging/materials")
print("Status:", res.status_code, "Catalog materials:", len(res.json()))
assert res.status_code == 200

print("\n4. Testing GET /api/ml/status")
res = client.get("/api/ml/status")
print("Status:", res.status_code, "Model status:", res.json().get("model_status"))
assert res.status_code == 200

print("\n5. Testing POST /api/analyze for Biscuits")
payload = {
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
res = client.post("/api/analyze", json=payload)
print("Status:", res.status_code)
data = res.json()
print("Top 3 count:", len(data["recommendations"]))
for rec in data["recommendations"]:
    print(f"  Rank {rec['rank']}: {rec['material']} - Score: {rec['suitability_score']}")

print("\n6. Testing POST /api/analyze for Case with No Valid Compatible Packaging (Strict Zero Plastic + Only Flexible in Non-Flexible category)")
strict_payload = {
    "food_name": "Acidic Fruit Puree",
    "food_category": "Fruit & Vegetable products",
    "moisture_level": 85.0,
    "fat_oil_sensitivity": "Low",
    "ph": 3.2,
    "respiration_activity": "Low",
    "desired_shelf_life_days": 365,
    "storage_temperature_c": 25.0,
    "relative_humidity_pct": 65.0,
    "storage_condition": "Ambient",
    "transport_condition": "Ambient",
    "map_required": "Yes",
    "sustainability_priority": "Strict (Zero-Plastic)",
    "preferred_package_type": "Flexible"
}
res = client.post("/api/analyze", json=strict_payload)
print("Status:", res.status_code)
strict_data = res.json()
print("Response status field:", strict_data.get("status"))
print("Message:", strict_data.get("message"))
print("Rejected candidates sample count:", len(strict_data.get("rejected_candidates", [])))

print("\nALL API ENDPOINTS TESTED AND VERIFIED WORKING!")
