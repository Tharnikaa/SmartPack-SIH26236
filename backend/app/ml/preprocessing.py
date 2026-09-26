from typing import Dict, Any, List
import numpy as np
import pandas as pd

class FeaturePipeline:
    def __init__(self):
        self.feature_names = [
            "food_moisture",
            "food_fat_sensitivity",
            "food_ph",
            "shelf_life_days",
            "storage_temp",
            "storage_rh",
            "req_oxygen_score",
            "req_moisture_score",
            "req_mechanical_score",
            "req_seal_score",
            "is_rigid",
            "is_laminate",
            "is_paper",
            "is_glass_metal",
            "has_measured_wvtr",
            "has_measured_otr",
            "is_recyclable",
            "is_biodegradable"
        ]

    def extract_features(self, user_input: Dict[str, Any], reqs: Dict[str, Any], candidate: Dict[str, Any]) -> List[float]:
        """
        Builds standardized numerical feature vector for the ML model.
        Features combine food properties, calculated requirements, and packaging attributes.
        """
        moisture = float(user_input.get("moisture_level", 15.0) or 15.0)
        
        fat_sens_str = str(user_input.get("fat_oil_sensitivity", "Medium")).lower()
        fat_sens = 1.0 if "high" in fat_sens_str else (0.5 if "medium" in fat_sens_str else 0.1)
        
        ph = float(user_input.get("ph", 6.0) or 6.0)
        shelf_life_days = float(user_input.get("desired_shelf_life_days", 90) or 90)
        storage_temp = float(user_input.get("storage_temperature_c", 25.0) or 25.0)
        storage_rh = float(user_input.get("relative_humidity_pct", 65.0) or 65.0)

        req_o2 = float(reqs.get("oxygen_requirement", {}).get("score", 0.5))
        req_h2o = float(reqs.get("moisture_requirement", {}).get("score", 0.5))
        req_mech = float(reqs.get("mechanical_requirement", {}).get("score", 0.5))
        req_seal = float(reqs.get("sealability_requirement", {}).get("score", 0.5))

        mat = candidate.get("material", "").lower()
        pkg_type = candidate.get("packaging_type", "").lower()

        is_rigid = 1.0 if any(k in pkg_type or k in mat for k in ["rigid", "bottle", "can", "jar", "box", "tub", "tin"]) else 0.0
        is_laminate = 1.0 if any(k in mat or k in pkg_type for k in ["laminate", "multilayer", "aseptic", "retort"]) else 0.0
        is_paper = 1.0 if any(k in mat for k in ["paper", "kraft", "fibreboard", "board", "jute"]) else 0.0
        is_glass_metal = 1.0 if any(k in mat for k in ["glass", "tin", "aluminium", "can", "metal"]) else 0.0

        # Technical Data completeness flags (Never fabricate missing values)
        barrier = candidate.get("barrier_properties", {})
        has_measured_wvtr = 1.0 if barrier.get("wvtr") is not None else 0.0
        has_measured_otr = 1.0 if barrier.get("otr") is not None else 0.0

        sust = candidate.get("sustainability", {})
        is_recyclable = 1.0 if sust.get("recyclable") == "Yes" or "yes" in str(sust.get("recyclable", "")).lower() else 0.0
        is_biodegradable = 1.0 if sust.get("biodegradable") == "Yes" or "yes" in str(sust.get("biodegradable", "")).lower() else 0.0

        return [
            moisture,
            fat_sens,
            ph,
            shelf_life_days,
            storage_temp,
            storage_rh,
            req_o2,
            req_h2o,
            req_mech,
            req_seal,
            is_rigid,
            is_laminate,
            is_paper,
            is_glass_metal,
            has_measured_wvtr,
            has_measured_otr,
            is_recyclable,
            is_biodegradable
        ]

feature_pipeline = FeaturePipeline()
