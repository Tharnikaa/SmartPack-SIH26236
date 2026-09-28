from typing import Dict, Any, List
import re
import numpy as np
import pandas as pd

class FeaturePipeline:
    def __init__(self):
        self.feature_names = [
            "food_moisture",
            "food_fat_sensitivity",
            "food_ph",
            "respiration_level",
            "shelf_life_days",
            "storage_temp",
            "storage_rh",
            "req_oxygen_score",
            "req_moisture_score",
            "req_mechanical_score",
            "req_seal_score",
            "pkg_log_otr",
            "pkg_log_wvtr",
            "pkg_is_rigid",
            "pkg_is_flexible",
            "pkg_is_breathable",
            "pkg_is_laminate",
            "pkg_tensile_mpa",
            "pkg_recyclable",
            "pkg_biodegradable",
            "barrier_match_oxygen",
            "barrier_match_moisture",
            "respiration_compatibility"
        ]

    def extract_features(self, user_input: Dict[str, Any], reqs: Dict[str, Any], candidate: Dict[str, Any]) -> List[float]:
        """
        Builds standardized candidate-specific numerical feature vector for the ML model.
        Every candidate packaging produces a candidate-specific feature vector reflecting its
        actual barrier properties (OTR, WVTR), format, tensile strength, circularity, and
        domain compatibility with the commodity.
        """
        # 1. Commodity Features
        moisture = float(user_input.get("moisture_level", 15.0) or 15.0)
        
        fat_sens_str = str(user_input.get("fat_oil_sensitivity", "Medium")).lower()
        fat_sens = 1.0 if "high" in fat_sens_str else (0.5 if "medium" in fat_sens_str else 0.1)
        
        ph = float(user_input.get("ph", 6.0) or 6.0)
        
        # Respiration activity
        resp_prof = reqs.get("respiration_profile") or {}
        resp_str = str(resp_prof.get("respiration_class") or user_input.get("respiration_activity", "Low")).lower()
        if "very high" in resp_str or "extremely" in resp_str:
            resp_val = 1.0
        elif "high" in resp_str:
            resp_val = 0.8
        elif "medium" in resp_str or "moderate" in resp_str:
            resp_val = 0.5
        elif "low" in resp_str:
            resp_val = 0.25
        else:
            resp_val = 0.0

        shelf_life_days = float(user_input.get("desired_shelf_life_days", 90) or 90)
        storage_temp = float(user_input.get("storage_temperature_c", 25.0) or 25.0)
        storage_rh = float(user_input.get("relative_humidity_pct", 65.0) or 65.0)

        # Requirements
        req_o2 = float(reqs.get("oxygen_requirement", {}).get("score", 0.5))
        req_h2o = float(reqs.get("moisture_requirement", {}).get("score", 0.5))
        req_mech = float(reqs.get("mechanical_requirement", {}).get("score", 0.5))
        req_seal = float(reqs.get("sealability_requirement", {}).get("score", 0.5))

        # 2. Candidate Packaging Features
        mat = str(candidate.get("material", "")).lower()
        pkg_type = str(candidate.get("packaging_type", "")).lower()
        barrier = candidate.get("barrier_properties", {})
        mech_props = candidate.get("mechanical_properties", {})
        sust = candidate.get("sustainability", {})

        # OTR (log10 scale)
        raw_otr = barrier.get("otr")
        if raw_otr is not None:
            try:
                pkg_log_otr = float(np.log10(max(0.0, float(raw_otr)) + 1.0))
            except (ValueError, TypeError):
                pkg_log_otr = 3.0
        else:
            if any(k in mat or k in pkg_type for k in ["glass", "tin", "metal", "foil", "can"]):
                pkg_log_otr = 0.0
            elif any(k in mat or k in pkg_type for k in ["jute", "sack", "mesh", "net"]):
                pkg_log_otr = 5.0
            elif any(k in mat for k in ["paper", "kraft", "fibreboard", "board"]):
                pkg_log_otr = 4.5
            elif any(k in mat for k in ["punnet", "overwrap"]):
                pkg_log_otr = 2.6
            elif any(k in mat for k in ["laminate", "evoh", "retort"]):
                pkg_log_otr = 1.0
            else:
                pkg_log_otr = 3.5

        # WVTR (log10 scale)
        raw_wvtr = barrier.get("wvtr")
        if raw_wvtr is not None:
            try:
                pkg_log_wvtr = float(np.log10(max(0.0, float(raw_wvtr)) + 1.0))
            except (ValueError, TypeError):
                pkg_log_wvtr = 1.5
        else:
            if any(k in mat or k in pkg_type for k in ["glass", "tin", "metal", "foil", "can"]):
                pkg_log_wvtr = 0.0
            elif any(k in mat or k in pkg_type for k in ["jute", "sack", "mesh"]):
                pkg_log_wvtr = 3.5
            elif any(k in mat for k in ["paper", "kraft", "fibreboard"]):
                pkg_log_wvtr = 3.0
            elif any(k in mat for k in ["punnet", "tray"]):
                pkg_log_wvtr = 1.6
            else:
                pkg_log_wvtr = 1.3

        # Formats
        pkg_is_rigid = 1.0 if any(k in pkg_type or k in mat for k in [
            "rigid", "bottle", "can", "jar", "box", "tub", "tray", "punnet", "tin", "crate"
        ]) else 0.0

        pkg_is_flexible = 1.0 if any(k in pkg_type or k in mat for k in [
            "pouch", "bag", "wrap", "film", "sachet", "liner", "flexible"
        ]) and not any(k in pkg_type for k in ["rigid container", "box with film liner", "rigid tub"]) else 0.0

        pkg_is_breathable = 1.0 if any(k in mat or k in pkg_type for k in [
            "jute", "sack", "punnet", "overwrap", "perforated", "ventilated", "cfb box", "corrugated", "mesh", "net"
        ]) or "selectively permeable" in mat else 0.0

        pkg_is_laminate = 1.0 if any(k in mat or k in pkg_type for k in [
            "laminate", "multilayer", "aseptic", "retort", "co-extruded", "composite"
        ]) else 0.0

        # Tensile strength (MPa)
        tensile_str = str(mech_props.get("tensile_strength", "")).lower()
        if "mpa" in tensile_str:
            nums = [float(s) for s in re.findall(r'\d+\.?\d*', tensile_str) if float(s) < 2000]
            pkg_tensile_mpa = float(np.mean(nums)) if nums else 25.0
        elif pkg_is_rigid:
            pkg_tensile_mpa = 80.0
        elif "pp" in mat or "bopp" in mat:
            pkg_tensile_mpa = 140.0
        elif "pet" in mat:
            pkg_tensile_mpa = 160.0
        elif "ldpe" in mat:
            pkg_tensile_mpa = 18.0
        elif "hdpe" in mat:
            pkg_tensile_mpa = 28.0
        elif "jute" in mat or "paper" in mat:
            pkg_tensile_mpa = 35.0
        else:
            pkg_tensile_mpa = 25.0

        # Sustainability
        rec_str = str(sust.get("recyclable", "")).lower()
        pkg_recyclable = 1.0 if "yes" in rec_str or any(k in mat for k in ["glass", "tin", "pet", "pp", "hdpe", "paper", "jute"]) else 0.0

        bio_str = str(sust.get("biodegradable", "")).lower()
        pkg_biodegradable = 1.0 if "yes" in bio_str or any(k in mat for k in ["jute", "paper", "fibreboard", "cellulose", "pla", "pbat"]) else 0.0

        # 3. Domain Interaction Terms
        # Oxygen match:
        if resp_val > 0.2:
            # Respiring produce needs breathability / moderate OTR; tight zero-barrier causes anaerobic decay
            barrier_match_oxygen = 1.0 if pkg_is_breathable or pkg_log_otr >= 2.0 else 0.2
        else:
            # Non-respiring goods: higher barrier needed when req_o2 is high
            if req_o2 >= 0.7:
                barrier_match_oxygen = 1.0 if pkg_log_otr <= 1.5 else (0.5 if pkg_log_otr <= 3.0 else 0.2)
            else:
                barrier_match_oxygen = 0.85

        # Moisture match:
        if moisture > 70.0 and resp_val > 0.2:
            # High moisture fresh produce needs condensation control (moderate permeability)
            barrier_match_moisture = 0.95 if pkg_log_wvtr >= 1.0 else 0.4
        elif req_h2o >= 0.7:
            # Dry crispy product needs low WVTR
            barrier_match_moisture = 1.0 if pkg_log_wvtr <= 1.0 else 0.3
        else:
            barrier_match_moisture = 0.80

        # Respiration compatibility:
        if resp_val >= 0.4:
            # Medium/high respiration
            if pkg_is_breathable or "punnet" in mat or "box" in mat or "jute" in mat:
                respiration_compatibility = 1.0
            elif "tray" in mat:
                respiration_compatibility = 0.8
            elif pkg_log_otr >= 3.5:
                respiration_compatibility = 0.65
            else:
                respiration_compatibility = 0.2
        elif resp_val > 0:
            # Low respiration (e.g. apple, potato)
            if pkg_is_breathable or pkg_is_rigid:
                respiration_compatibility = 0.95
            elif pkg_log_otr >= 2.0:
                respiration_compatibility = 0.85
            else:
                respiration_compatibility = 0.4
        else:
            # Non-respiring: hermetic packaging is great
            respiration_compatibility = 1.0 if not pkg_is_breathable else 0.7

        return [
            moisture,
            fat_sens,
            ph,
            resp_val,
            shelf_life_days,
            storage_temp,
            storage_rh,
            req_o2,
            req_h2o,
            req_mech,
            req_seal,
            pkg_log_otr,
            pkg_log_wvtr,
            pkg_is_rigid,
            pkg_is_flexible,
            pkg_is_breathable,
            pkg_is_laminate,
            pkg_tensile_mpa,
            pkg_recyclable,
            pkg_biodegradable,
            barrier_match_oxygen,
            barrier_match_moisture,
            respiration_compatibility
        ]

feature_pipeline = FeaturePipeline()
