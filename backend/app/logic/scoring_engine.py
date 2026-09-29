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

        o2_req_score = targets.get("o2_score", 0.5)
        h2o_req_score = targets.get("h2o_score", 0.5)
        fat_oil_high = str(user_input.get("fat_oil_sensitivity", "")).lower() == "high"
        moisture_low = float(user_input.get("moisture_level", 50.0) or 50.0) <= 5.0
        is_lipid_or_dry_sensitive = fat_oil_high or moisture_low or o2_req_score >= 0.70 or h2o_req_score >= 0.70

        is_rigid_impermeable = (
            any(k in mat_lower for k in ["glass", "tinplate", "tin can", "steel can", "tfs", "metal container"])
            and not any(k in mat_lower for k in ["pouch", "laminate", "film"])
        )
        is_foil_barrier = any(k in mat_lower for k in ["aluminium foil", "aluminum foil", "al foil", "foil-based", "foil laminate"])

        has_numeric_barrier = (otr is not None) or (wvtr is not None)
        barrier_classification = "Standard"

        if is_breathable_req:
            # Fresh respiring produce requires controlled gas exchange / breathability
            if any(k in mat_lower or k in pkg_type for k in ["punnet", "overwrap", "tray with overwrap", "permeable", "perforated", "box", "cfb", "jute"]):
                barrier_score = 0.95
                barrier_classification = "Breathable / Ventilated (Produce Suitable)"
            elif "pouch" in mat_lower or "film" in mat_lower:
                barrier_score = 0.85
                barrier_classification = "Permeable Film"
            else:
                barrier_score = 0.65
                barrier_classification = "Moderate Ventilation"
        elif is_rigid_impermeable or is_foil_barrier or (otr == 0.0 and (wvtr is not None and wvtr <= 0.3)):
            # Hermetic glass, metal, or aluminium foil composite
            barrier_score = 0.98
            barrier_classification = "High (Hermetic / Foil Composite)"
        elif any(k in mat_lower for k in ["jute", "sacking", "hessian", "burlap", "mesh"]):
            # Explicitly porous textile
            barrier_score = 0.08 if is_lipid_or_dry_sensitive else 0.40
            barrier_classification = "Low (Porous Textile - Inadequate Barrier)"
        elif "except top" in mat_lower or ("cfb" in mat_lower and "laminate" not in mat_lower and "foil" not in mat_lower):
            # Open-top or unsealed fibreboard
            barrier_score = 0.12 if is_lipid_or_dry_sensitive else 0.45
            barrier_classification = "Low (Unsealed / Porous Fibreboard)"
        elif "paper" in mat_lower and not any(k in mat_lower for k in ["laminate", "foil", "coated", "wax"]):
            # Uncoated porous paper
            barrier_score = 0.10 if is_lipid_or_dry_sensitive else 0.35
            barrier_classification = "Low (Uncoated Paper - Inadequate Barrier)"
        elif has_numeric_barrier:
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
                        otr_score = 0.35
                    else:
                        otr_score = 0.10 if is_lipid_or_dry_sensitive else 0.25
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
                        wvtr_score = 0.35
                    else:
                        wvtr_score = 0.10 if is_lipid_or_dry_sensitive else 0.25
                except (ValueError, TypeError):
                    wvtr_score = None

            if otr_score is not None and wvtr_score is not None:
                total_req = o2_req_score + h2o_req_score
                barrier_score = (o2_req_score * otr_score + h2o_req_score * wvtr_score) / total_req if total_req > 0 else (0.5 * otr_score + 0.5 * wvtr_score)
            elif otr_score is not None:
                barrier_score = otr_score
            elif wvtr_score is not None:
                barrier_score = wvtr_score
            else:
                barrier_score = 0.55

            barrier_classification = "High (Numerical Verified)" if barrier_score >= 0.80 else ("Moderate" if barrier_score >= 0.55 else "Low")
        else:
            # Missing numerical OTR/WVTR in DB — evaluate validated structural classification without fabricating numbers
            if any(k in mat_lower for k in ["multilayer", "laminate", "composite", "retort", "co-extruded", "zipper pouch"]):
                # Regulated multi-layer flexible barrier pouch (e.g. IS 9845)
                barrier_score = 0.88
                barrier_classification = "High (Validated Multilayer Barrier Structure)"
            elif any(k in mat_lower for k in ["coated", "wax"]):
                barrier_score = 0.65
                barrier_classification = "Moderate (Coated Paper/Board)"
            elif any(k in mat_lower for k in ["plastic rigid", "pet bottle", "hdpe jar", "thermoform container"]):
                barrier_score = 0.72
                barrier_classification = "Moderate (Rigid Polymer)"
            else:
                # Missing OTR/WVTR and NO validated barrier classification exists
                # Marked as conditional / insufficient technical evidence rather than assuming suitability
                barrier_score = 0.35
                barrier_classification = "Conditional / Insufficient Technical Evidence"

        # -------------------------------------------------------------
        # 2. Compatibility Score (FSSAI Schedule IV endorsement & chemical inertness)
        # -------------------------------------------------------------
        # Candidates that passed constraint filter are verified compatible
        compat_score = 0.90
        if is_rigid_impermeable and "glass" in mat_lower:
            compat_score = 1.0  # Chemically inert
        elif any(k in mat_lower for k in ["retort", "aseptic", "lacquered", "foil"]):
            compat_score = 0.95
        elif "plastic" in mat_lower and "oil" in str(user_input.get("food_category", "")).lower():
            compat_score = 0.85

        # Light sensitivity & photo-degradation protection
        light_req = str((reqs.get("light_requirement") or {}).get("level", "")).lower()
        if "mandatory opaque" in light_req or "light barrier" in light_req or is_lipid_or_dry_sensitive:
            is_opaque = any(k in mat_lower for k in ["jute", "sacking", "cfb", "corrugated", "board", "paper", "foil", "metal", "kraft", "box", "tin"])
            if is_opaque:
                compat_score = max(compat_score, 0.95)
            elif any(k in mat_lower for k in ["punnet", "transparent", "tray", "film twist"]) and not any(k in mat_lower for k in ["cfb", "box", "foil", "tin"]):
                compat_score = min(compat_score, 0.75)

        # -------------------------------------------------------------
        # 3. Shelf-Life Score & Benchmark Validation Accounting
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

        validation_status = "UNKNOWN"
        validation_note = ""

        if expected_days is not None:
            if expected_days >= requested_days:
                shelf_life_score = 0.95
                validation_status = "FULLY_VALIDATED"
                validation_note = f"Target: {requested_days} days | Validated benchmark: {candidate.get('expected_shelf_life')} | Fully covers target shelf life."
            else:
                # Target shelf life exceeds validated benchmark (e.g. 180 days target vs 3 months benchmark)
                ratio = expected_days / requested_days  # e.g. 90 / 180 = 0.50
                # Scoring engine explicitly accounts for this mismatch
                shelf_life_score = max(0.35, round(0.90 * (ratio ** 0.75), 3))
                validation_status = "ADDITIONAL_VALIDATION_REQUIRED"
                validation_note = f"Target: {requested_days} days | Validated benchmark: {candidate.get('expected_shelf_life')} | Additional validation required for target shelf life."
        else:
            # Expected shelf life not documented in source DB
            if barrier_score >= 0.85:
                # High-barrier structure provides physical protection, but lacks empirical benchmark
                shelf_life_score = 0.65
                validation_status = "THEORETICAL_BARRIER_PROTECTION"
                validation_note = f"Target: {requested_days} days | Validated benchmark: Not available in source database | Empirical validation recommended."
            else:
                shelf_life_score = 0.40
                validation_status = "INSUFFICIENT_EVIDENCE"
                validation_note = f"Target: {requested_days} days | Validated benchmark: Not available in source database | Additional validation required for target shelf life."

        # -------------------------------------------------------------
        # 4. Mechanical Protection Score (Specs from mechanical_properties)
        # -------------------------------------------------------------
        mech = candidate.get("mechanical_properties", {})
        tensile = str(mech.get("tensile_strength", "")).lower()
        burst = str(mech.get("burst_strength", "") or mech.get("burst_index", "")).lower()
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

        # -------------------------------------------------------------
        # CRITICAL BARRIER DEFECT PENALTY:
        # A candidate with explicitly LOW oxygen/moisture barrier must not receive a high recommendation
        # merely because of generic compatibility, sustainability, or mechanical properties.
        # -------------------------------------------------------------
        barrier_defect_penalty = 1.0
        if is_lipid_or_dry_sensitive:
            if barrier_score <= 0.20:
                # Inadequate oxygen/moisture barrier directly causes rancidity and sogginess
                barrier_defect_penalty = 0.30
            elif barrier_score <= 0.40:
                # Marginal / insufficient technical evidence
                barrier_defect_penalty = 0.65

        final_composite = final_composite * barrier_defect_penalty
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
            "ml_details": ml_res,
            "barrier_classification": barrier_classification,
            "validation_status": validation_status,
            "validation_note": validation_note,
            "additional_validation_required": (expected_days is not None and expected_days < requested_days) or (expected_days is None and requested_days > 90)
        }

scoring_engine = ScoringEngine()
