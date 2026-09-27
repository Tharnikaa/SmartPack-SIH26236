import json
import os
from typing import Dict, Any, Optional
from app.services.data_service import data_service

class RequirementEngine:
    def __init__(self, thresholds_path: str = "config/requirement_thresholds.json"):
        self.thresholds_path = thresholds_path
        self.thresholds = self._load_thresholds()

    def _load_thresholds(self) -> Dict[str, Any]:
        if os.path.exists(self.thresholds_path):
            try:
                with open(self.thresholds_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "moisture_thresholds": {"dry_max_pct": 12.0, "intermediate_max_pct": 50.0, "high_min_pct": 50.0},
            "ph_thresholds": {"high_acid_max": 4.5, "low_acid_min": 4.5},
            "shelf_life_factors": {"short_days": 14, "medium_days": 90, "long_days": 365}
        }

    def compute_requirements(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates scientific requirement estimates based on food properties and storage requirements.
        Adheres to transparency guidelines: all outputs are labelled 'Calculated requirement'.
        """
        food_name_raw = str(user_input.get("food_name", "")).strip()
        food_name = food_name_raw.lower()
        food_category = str(user_input.get("food_category", "")).lower()
        
        # Look up commodity-specific respiration profile from reference CSV
        resp_ref = data_service.lookup_respiration(food_name_raw, food_category)
        if resp_ref:
            respiration = resp_ref["respiration_class"].lower()
        else:
            respiration = str(user_input.get("respiration_activity", "Low")).lower()

        moisture = float(user_input.get("moisture_level", 15.0) or 15.0)
        fat_sensitivity = str(user_input.get("fat_oil_sensitivity", "Medium")).lower()
        ph = float(user_input.get("ph", 6.0) or 6.0)
        shelf_life_days = int(user_input.get("desired_shelf_life_days", 90) or 90)
        storage_temp = float(user_input.get("storage_temperature_c", 25.0) or 25.0)
        relative_humidity = float(user_input.get("relative_humidity_pct", 65.0) or 65.0)
        transport_cond = str(user_input.get("transport_condition", "Ambient")).lower()
        map_required = str(user_input.get("map_required", "No")).lower()
        sustainability_priority = str(user_input.get("sustainability_priority", "Standard")).lower()

        # 1. Oxygen Barrier Requirement
        # Driven by fat oxidation sensitivity, requested shelf life, and ambient/warm storage
        o2_score = 0.2
        if "high" in fat_sensitivity:
            o2_score += 0.4
        elif "medium" in fat_sensitivity:
            o2_score += 0.25
        
        if shelf_life_days > 180:
            o2_score += 0.25
        elif shelf_life_days > 60:
            o2_score += 0.15

        if storage_temp > 25:
            o2_score += 0.1
        
        o2_score = min(1.0, o2_score)
        if o2_score >= 0.7:
            oxygen_req = "High"
            oxygen_desc = "Critical oxygen protection required to prevent lipid peroxidation, rancidity, and nutritional degradation."
        elif o2_score >= 0.4:
            oxygen_req = "Medium"
            oxygen_desc = "Moderate oxygen barrier suitable for intermediate shelf-life with moderate lipid presence."
        else:
            oxygen_req = "Low"
            oxygen_desc = "Standard barrier acceptable; product has low lipid vulnerability."

        # 2. Moisture Barrier Requirement
        # Driven by moisture delta between product and ambient RH, moisture sensitivity, shelf life
        moisture_score = 0.2
        if moisture < 12.0:
            # Dry, crisp food (e.g. biscuits, snacks) - must keep moisture OUT
            moisture_score += 0.45 if relative_humidity > 60 else 0.35
        elif moisture > 60.0:
            # High-moisture food - must keep moisture IN or manage condensation
            moisture_score += 0.35
        else:
            # Intermediate moisture
            moisture_score += 0.25

        if shelf_life_days > 90:
            moisture_score += 0.25
        elif shelf_life_days > 30:
            moisture_score += 0.15

        moisture_score = min(1.0, moisture_score)
        if moisture_score >= 0.7:
            moisture_req = "High"
            moisture_desc = "Tight moisture barrier required to prevent crispness loss, caking, or rapid dehydration."
        elif moisture_score >= 0.4:
            moisture_req = "Medium"
            moisture_desc = "Moderate moisture barrier sufficient to maintain equilibrium moisture content."
        else:
            moisture_req = "Low"
            moisture_desc = "Permeable or standard barrier acceptable under controlled storage."

        # 3. Mechanical Protection Requirement
        # Driven by transport rigor, product fragility, package geometry
        mech_score = 0.3
        if "rough" in transport_cond or "long-distance" in transport_cond or "export" in transport_cond:
            mech_score += 0.4
        elif "ambient" in transport_cond or "refrigerated" in transport_cond:
            mech_score += 0.2

        if "biscuit" in food_category or "fruit" in food_category or "snack" in food_category or "egg" in food_category:
            mech_score += 0.3 # Fragile / crush-susceptible

        mech_score = min(1.0, mech_score)
        if mech_score >= 0.7:
            mech_req = "High"
            mech_desc = "Rigid container, reinforced corrugated board, or cushioned thermoformed tray required to prevent physical damage."
        elif mech_score >= 0.4:
            mech_req = "Medium"
            mech_desc = "Standard structural strength; flexible pouch or folding boxboard acceptable."
        else:
            mech_req = "Low"
            mech_desc = "Lightweight flexible wrap or standard carton sufficient."

        # 4. Sealability Requirement
        seal_score = 0.3
        if "yes" in map_required:
            seal_score = 0.95
        elif shelf_life_days > 90 or "liquid" in food_category or "oil" in food_category:
            seal_score = 0.8
        elif shelf_life_days > 30:
            seal_score = 0.5
        
        seal_req = "High (Hermetic)" if seal_score >= 0.7 else ("Medium" if seal_score >= 0.4 else "Standard")
        seal_desc = "Hermetic heat-seal or gas-tight closure required" if seal_score >= 0.7 else "Standard commercial seal acceptable."

        # 5. MAP / Gas Exchange Requirement
        if "yes" in map_required:
            if "high" in respiration:
                map_req = "Equilibrium MAP / Perforated Barrier"
                map_desc = "High-respiration produce under MAP requires micro-perforations or selective permeability to prevent anaerobic fermentation."
            else:
                map_req = "Mandatory Gas Barrier"
                map_desc = "Must maintain modified atmosphere (CO2/N2) without premature gas escape."
        elif "high" in respiration:
            map_req = "Permeable / Breathable"
            map_desc = "Active produce respiration requires controlled gas permeability, ventilation, or macro-perforations to prevent anaerobic spoilage."
        elif "medium" in respiration:
            map_req = "Semi-permeable / Breathable"
            map_desc = "Moderate produce respiration requires balanced gas exchange or ventilated containment to avoid condensation and senescence."
        elif "optional" in map_required:
            map_req = "Recommended"
            map_desc = "MAP beneficial for shelf-life extension but standard containment acceptable."
        else:
            map_req = "Standard Gas Barrier" if shelf_life_days > 90 else "Not Required"
            map_desc = "Standard ambient atmosphere packaging suitable."

        # 6. Shelf-life Protection Requirement
        if shelf_life_days > 180:
            shelf_req = "Long-Term Preservation (>6 months)"
            shelf_desc = "Demands robust chemical and physical barrier, protection against oxidation, microbial ingress, and flavor scalping."
        elif shelf_life_days > 30:
            shelf_req = "Medium-Term Preservation (1-6 months)"
            shelf_desc = "Requires balanced protection for retail distribution and standard shelf stability."
        else:
            shelf_req = "Short-Term / Fresh (<1 month)"
            shelf_desc = "Fresh distribution; priority on cold-chain integrity and hygienic containment."

        # 7. Compatibility Requirement
        compatibility_notes = []
        if ph < 4.5:
            compatibility_notes.append("High-acid product: Metal surfaces must have epoxy/phenolic lacquering per IS 5837; avoid reactive bare metals.")
        if "high" in fat_sensitivity or "oil" in food_category:
            compatibility_notes.append("High fat content: Plastic polymers must be resistant to environmental stress cracking and oil migration.")
        if not compatibility_notes:
            compatibility_notes.append("Standard direct food-contact compliance under FSS (Packaging) Regulations 2018.")

        # 8. Sustainability Requirement
        if "high" in sustainability_priority or "strict" in sustainability_priority:
            sust_req = "High (Circular / Recyclable / Bio-based)"
            sust_desc = "Mandatory single-polymer recyclability (Mono-PE/PP), paperboard, glass, or certified compostable materials."
        else:
            sust_req = "Standard EPR Compliance"
            sust_desc = "Compliance with Plastic Waste Management Rules 2016 and CPCB EPR guidelines."

        # 9. Light Sensitivity / Darkness Requirement
        # Tubers (potatoes) synthesize chlorophyll and toxic glycoalkaloids (solanine) upon light exposure.
        # Edible oils undergo photo-oxidation.
        if any(k in food_name for k in ["potato", "tuber", "onion"]) or any(k in food_category for k in ["root", "tuber"]):
            light_req = "Mandatory Opaque / Light Barrier"
            light_desc = "Tuber requires dark storage to prevent light-induced chlorophyll formation and toxic solanine accumulation."
        elif "high" in fat_sensitivity or "oil" in food_category:
            light_req = "Light-Protective Barrier"
            light_desc = "Fat/oil content sensitive to photo-oxidation; opaque, amber, or metallized barrier recommended."
        else:
            light_req = "Standard (Light protection not critical)"
            light_desc = "Transparent or translucent packaging acceptable."

        return {
            "disclaimer": "Calculated requirement estimate based on product inputs; not a laboratory measurement.",
            "respiration_profile": resp_ref,
            "oxygen_requirement": {
                "level": oxygen_req,
                "score": round(o2_score, 2),
                "description": oxygen_desc,
                "label": "CALCULATED REQUIREMENT"
            },
            "moisture_requirement": {
                "level": moisture_req,
                "score": round(moisture_score, 2),
                "description": moisture_desc,
                "label": "CALCULATED REQUIREMENT"
            },
            "mechanical_requirement": {
                "level": mech_req,
                "score": round(mech_score, 2),
                "description": mech_desc,
                "label": "CALCULATED REQUIREMENT"
            },
            "sealability_requirement": {
                "level": seal_req,
                "score": round(seal_score, 2),
                "description": seal_desc,
                "label": "CALCULATED REQUIREMENT"
            },
            "map_gas_requirement": {
                "level": map_req,
                "description": map_desc,
                "label": "CALCULATED REQUIREMENT"
            },
            "shelf_life_protection": {
                "level": shelf_req,
                "days_requested": shelf_life_days,
                "description": shelf_desc,
                "label": "CALCULATED REQUIREMENT"
            },
            "compatibility_requirement": {
                "notes": compatibility_notes,
                "label": "CALCULATED REQUIREMENT"
            },
            "sustainability_requirement": {
                "level": sust_req,
                "description": sust_desc,
                "label": "CALCULATED REQUIREMENT"
            },
            "light_requirement": {
                "level": light_req,
                "description": light_desc,
                "label": "CALCULATED REQUIREMENT"
            }
        }

requirement_engine = RequirementEngine()
