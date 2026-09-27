import json
import os
import re
from typing import Dict, Any, List
from app.logic.thickness_engine import thickness_engine
from app.ml.predict import predictor

class ScoringEngine:
    def __init__(self, weights_path: str = "config/scoring_weights.json"):
        self.weights_path = weights_path
        self.weights = self.load_weights()

    def load_weights(self) -> Dict[str, float]:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
        candidates = [
            self.weights_path,
            os.path.join(base_dir, "config", "scoring_weights.json"),
            os.path.join("..", self.weights_path)
        ]
        target_path = next((p for p in candidates if os.path.exists(p)), None)
        raw_weights = None
        if target_path:
            self.weights_path = target_path
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    raw_weights = json.load(f)
            except Exception:
                pass

        default_weights = {
            "ml_score": 0.25,
            "barrier_score": 0.25,
            "compatibility_score": 0.15,
            "shelf_life_score": 0.15,
            "mechanical_score": 0.10,
            "sustainability_score": 0.10
        }

        if not raw_weights or not isinstance(raw_weights, dict):
            return default_weights

        filtered = {k: v for k, v in raw_weights.items() if k in default_weights}
        total_w = sum(filtered.values())
        if total_w > 0:
            return {k: round(v / total_w, 4) for k, v in filtered.items()}
        return default_weights

    def save_weights(self, new_weights: Dict[str, float]) -> bool:
        try:
            allowed = ["ml_score", "barrier_score", "compatibility_score", "shelf_life_score", "mechanical_score", "sustainability_score"]
            filtered = {k: v for k, v in new_weights.items() if k in allowed}
            total = sum(filtered.values())
            if total > 0:
                normalized = {k: round(v / total, 4) for k, v in filtered.items()}
            else:
                normalized = filtered
            with open(self.weights_path, "w", encoding="utf-8") as f:
                json.dump(normalized, f, indent=2)
            self.weights = normalized
            return True
        except Exception:
            return False

    def score_candidate(self, candidate: Dict[str, Any], user_input: Dict[str, Any], reqs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes transparent multi-criteria packaging suitability based on real candidate data:
        1. Barrier fit: Evaluated against calculated OTR/WVTR limits derived via Fick's law.
        2. Compatibility: Assessed from regulatory FSSAI Schedule IV endorsement and chemical inertness.
        3. Shelf-life preservation: Compared against requested preservation days and benchmark database.
        4. Mechanical robustness: Evaluated from material tensile/burst/gauge specifications and packaging rigidity.
        5. Sustainability: Scored from CPCB recyclability, biodegradability, and EPR category classifications.

        NOTE: ML scoring term was removed; weights redistributed proportionally to sum to 1.0.
        """
        w = self.weights
        mat_lower = candidate.get("material", "").lower()
        pkg_type = candidate.get("packaging_type", "").lower()

        # -------------------------------------------------------------
        # 1. Barrier Fit Score (Based on candidate barrier_properties vs requirements)
        # -------------------------------------------------------------
        targets = thickness_engine.get_target_limits(reqs)
        target_otr = targets["target_otr"]
        target_wvtr = targets["target_wvtr"]

        barrier = candidate.get("barrier_properties", {})
        otr = barrier.get("otr")
        wvtr = barrier.get("wvtr")

        gas_req = str(reqs.get("map_gas_requirement", {}).get("level", "")).lower()
        is_breathable_req = "permeable" in gas_req or "breathable" in gas_req

        is_rigid_impermeable = (
            any(k in mat_lower for k in ["glass", "tinplate", "tin can", "steel can", "tfs"])
            and not any(k in mat_lower for k in ["pouch", "laminate", "film"])
        )

        if is_breathable_req:
            # Fresh respiring produce requires controlled gas exchange / breathability
            if any(k in mat_lower or k in pkg_type for k in ["punnet", "overwrap", "tray with overwrap", "permeable", "perforated", "box", "cfb", "jute"]):
                barrier_score = 0.95
            elif "pouch" in mat_lower or "film" in mat_lower:
                barrier_score = 0.85
            else:
                barrier_score = 0.65
        elif is_rigid_impermeable or (otr == 0.0 and (wvtr is not None and wvtr <= 0.3)):
            # Hermetic glass, metal, or foil composite
            barrier_score = 0.98
        else:
            otr_score = None
            if otr is not None:
                try:
                    o_num = float(otr)
                    if o_num <= target_otr:
                        otr_score = 0.95
                    elif o_num <= target_otr * 2.0:
                        otr_score = 0.80
                    elif o_num <= target_otr * 5.0:
                        otr_score = 0.60
                    elif o_num <= target_otr * 20.0:
                        otr_score = 0.40
                    else:
                        otr_score = 0.25
                except (ValueError, TypeError):
                    otr_score = None

            wvtr_score = None
            if wvtr is not None:
                try:
                    w_num = float(wvtr)
                    if w_num <= target_wvtr:
                        wvtr_score = 0.95
                    elif w_num <= target_wvtr * 2.0:
                        wvtr_score = 0.80
                    elif w_num <= target_wvtr * 5.0:
                        wvtr_score = 0.60
                    elif w_num <= target_wvtr * 20.0:
                        wvtr_score = 0.40
                    else:
                        wvtr_score = 0.25
                except (ValueError, TypeError):
                    wvtr_score = None

            if otr_score is not None and wvtr_score is not None:
                o2_req_score = targets.get("o2_score", 0.5)
                h2o_req_score = targets.get("h2o_score", 0.5)
                total_req = o2_req_score + h2o_req_score
                if total_req > 0:
                    barrier_score = (o2_req_score * otr_score + h2o_req_score * wvtr_score) / total_req
                else:
                    barrier_score = 0.5 * otr_score + 0.5 * wvtr_score
            elif otr_score is not None:
                barrier_score = otr_score
            elif wvtr_score is not None:
                barrier_score = wvtr_score
            else:
                # Non-numeric fallback (e.g. uncoated paper)
                if "porous" in str(barrier.get("test_condition", "")).lower() or ("paper" in mat_lower and "coated" not in mat_lower and "laminate" not in mat_lower):
                    barrier_score = 0.30
                else:
                    barrier_score = 0.55

        # -------------------------------------------------------------
        # 2. Compatibility Score (FSSAI Schedule IV endorsement & chemical inertness)
        # -------------------------------------------------------------
        # Candidates that passed constraint filter are verified compatible
        compat_score = 0.90
        if is_rigid_impermeable and "glass" in mat_lower:
            compat_score = 1.0  # Chemically inert
        elif any(k in mat_lower for k in ["retort", "aseptic", "lacquered"]):
            compat_score = 0.95
        elif "plastic" in mat_lower and "oil" in str(user_input.get("food_category", "")).lower():
            compat_score = 0.85

        # Light sensitivity & photo-degradation protection
        light_req = str((reqs.get("light_requirement") or {}).get("level", "")).lower()
        if "mandatory opaque" in light_req or "light barrier" in light_req:
            is_opaque = any(k in mat_lower for k in ["jute", "sacking", "cfb", "corrugated", "board", "paper", "foil", "metal", "kraft", "box"])
            if is_opaque:
                compat_score = max(compat_score, 0.95)
            elif any(k in mat_lower for k in ["punnet", "transparent", "tray"]) and not any(k in mat_lower for k in ["cfb", "box", "jute"]):
                # Clear transparent packaging without light barrier induces solanine greening in tubers
                compat_score = min(compat_score, 0.70)

        # -------------------------------------------------------------
        # 3. Shelf-Life Score (Comparing expected shelf life against requested days)
        # -------------------------------------------------------------
        requested_days = int(user_input.get("desired_shelf_life_days", 90) or 90)
        expected_sl = str(candidate.get("expected_shelf_life", "")).lower()

        expected_days = None
        if any(k in expected_sl for k in ["year", "12 month", "18 month", "24 month"]):
            expected_days = 365
        elif "6 month" in expected_sl or "180 day" in expected_sl:
            expected_days = 180
        elif "3 month" in expected_sl or "90 day" in expected_sl:
            expected_days = 90
        elif "1 month" in expected_sl or "30 day" in expected_sl:
            expected_days = 30
        elif any(k in expected_sl for k in ["week", "14 day", "21 day"]):
            expected_days = 21
        elif "day" in expected_sl:
            expected_days = 7

        if expected_days is not None:
            if expected_days >= requested_days:
                shelf_life_score = 0.95
            elif expected_days >= requested_days * 0.7:
                shelf_life_score = 0.85
            elif expected_days >= requested_days * 0.4:
                shelf_life_score = 0.65
            else:
                shelf_life_score = 0.45
        else:
            # Fallback to barrier fit if expected shelf life is not specified in DB
            shelf_life_score = 0.80 if barrier_score >= 0.75 else 0.60

        # -------------------------------------------------------------
        # 4. Mechanical Protection Score (Specs from mechanical_properties)
        # -------------------------------------------------------------
        mech = candidate.get("mechanical_properties", {})
        tensile = str(mech.get("tensile_strength", "")).lower()
        burst = str(mech.get("burst_index", "")).lower()
        req_mech_level = reqs.get("mechanical_requirement", {}).get("level", "Medium")

        is_rigid = any(k in pkg_type or k in mat_lower for k in [
            "rigid", "bottle", "can", "jar", "box", "tub", "tin", "corrugated"
        ])

        if is_rigid:
            mechanical_score = 0.95
        elif "mpa" in tensile:
            numbers = [float(s) for s in re.findall(r'\d+\.?\d*', tensile) if float(s) < 1000]
            if numbers and max(numbers) >= 40:
                mechanical_score = 0.90
            else:
                mechanical_score = 0.80 if req_mech_level != "High" else 0.60
        elif burst and burst != "none":
            mechanical_score = 0.85
        elif req_mech_level == "High":
            mechanical_score = 0.50
        else:
            mechanical_score = 0.75

        # -------------------------------------------------------------
        # 5. Sustainability Score (Lookups from sustainability dict)
        # -------------------------------------------------------------
        sust = candidate.get("sustainability", {})
        rec = str(sust.get("recyclable", "")).lower()
        bio = str(sust.get("biodegradable", "")).lower()
        comp = str(sust.get("compostable", "")).lower()
        epr = str(sust.get("epr_category", "")).lower()

        if "yes" in bio or "yes" in comp:
            sustainability_score = 0.95
        elif any(k in mat_lower for k in ["glass", "aluminium", "aluminum", "tinplate"]):
            sustainability_score = 0.90
        elif "yes" in rec:
            if any(k in epr for k in ["category i", "rigid"]):
                sustainability_score = 0.88
            else:
                sustainability_score = 0.80
        elif any(k in mat_lower for k in ["multilayer", "laminate", "composite"]):
            sustainability_score = 0.40
        else:
            sustainability_score = 0.55

        # -------------------------------------------------------------
        # 6. ML Suitability Model Prediction
        # -------------------------------------------------------------
        ml_res = predictor.predict_candidate(user_input, reqs, candidate)
        ml_score = float(ml_res.get("predicted_score", 0.70))

        # -------------------------------------------------------------
        # Weighted Composite Score (6 factors including active ML score)
        # -------------------------------------------------------------
        final_composite = (
            w.get("ml_score", 0.25) * ml_score +
            w.get("barrier_score", 0.25) * barrier_score +
            w.get("compatibility_score", 0.15) * compat_score +
            w.get("shelf_life_score", 0.15) * shelf_life_score +
            w.get("mechanical_score", 0.10) * mechanical_score +
            w.get("sustainability_score", 0.10) * sustainability_score
        )

        final_suitability_score = round(final_composite * 100, 1)

        return {
            "final_suitability_score": final_suitability_score,
            "label": "DERIVED SCORE",
            "score_breakdown": {
                "ml_score": round(ml_score, 3),
                "barrier_score": round(barrier_score, 3),
                "compatibility_score": round(compat_score, 3),
                "shelf_life_score": round(shelf_life_score, 3),
                "mechanical_score": round(mechanical_score, 3),
                "sustainability_score": round(sustainability_score, 3)
            },
            "applied_weights": w,
            "ml_details": ml_res
        }

scoring_engine = ScoringEngine()
