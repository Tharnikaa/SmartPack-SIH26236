import json
import os
from typing import Dict, Any, List
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
        if target_path:
            self.weights_path = target_path
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "ml_score": 0.30,
            "barrier_score": 0.20,
            "compatibility_score": 0.15,
            "shelf_life_score": 0.15,
            "mechanical_score": 0.10,
            "sustainability_score": 0.10
        }

    def save_weights(self, new_weights: Dict[str, float]) -> bool:
        try:
            with open(self.weights_path, "w", encoding="utf-8") as f:
                json.dump(new_weights, f, indent=2)
            self.weights = new_weights
            return True
        except Exception:
            return False

    def score_candidate(self, candidate: Dict[str, Any], user_input: Dict[str, Any], reqs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combines ML prediction, requirement satisfaction, barrier fit, compatibility,
        shelf-life protection, mechanical robustness, and sustainability into a transparent hybrid score.
        All sub-scores are explicitly broken down.
        """
        w = self.weights

        # 1. ML Suitability Score
        ml_res = predictor.predict_candidate(user_input, reqs, candidate)
        ml_score = ml_res["predicted_score"]

        # 2. Barrier Requirement Satisfaction Score
        mat = candidate.get("material", "").lower()
        pkg_type = candidate.get("packaging_type", "").lower()
        req_o2_level = reqs.get("oxygen_requirement", {}).get("level", "Medium")
        req_h2o_level = reqs.get("moisture_requirement", {}).get("level", "Medium")

        barrier_score = 0.6 # Baseline
        if "laminate" in mat or "multilayer" in mat or "foil" in mat or "aseptic" in mat or "glass" in mat or "tin" in mat:
            barrier_score = 0.95
        elif "pp" in mat or "hdpe" in mat or "pet" in mat:
            barrier_score = 0.75 if req_o2_level != "High" else 0.55
        elif "paper" in mat or "jute" in mat:
            barrier_score = 0.35 if (req_h2o_level == "High" or req_o2_level == "High") else 0.70

        # 3. Compatibility Score
        # Candidates passed hard constraint filter, so compatibility is at least compliant
        compat_score = 0.90
        if "glass" in mat:
            compat_score = 1.0 # Chemically inert
        elif "aseptic" in mat or "retort" in mat or "lacquered" in mat:
            compat_score = 0.95
        elif "plastic" in mat and "oil" in str(user_input.get("food_category", "")).lower():
            compat_score = 0.80

        # 4. Shelf-Life Protection Score
        requested_days = int(user_input.get("desired_shelf_life_days", 90) or 90)
        expected_sl = candidate.get("expected_shelf_life", "").lower()
        
        shelf_life_score = 0.70
        if "year" in expected_sl or "12 months" in expected_sl or "retort" in mat or "glass" in mat or "tin" in mat or "aseptic" in mat:
            shelf_life_score = 0.95
        elif "month" in expected_sl:
            shelf_life_score = 0.85 if requested_days <= 180 else 0.60
        elif "day" in expected_sl or "week" in expected_sl:
            shelf_life_score = 0.85 if requested_days <= 21 else 0.40

        # 5. Mechanical Protection Score
        req_mech_level = reqs.get("mechanical_requirement", {}).get("level", "Medium")
        is_rigid = any(k in pkg_type or k in mat for k in ["rigid", "bottle", "can", "jar", "box", "tub", "tin", "corrugated"])
        
        mechanical_score = 0.65
        if is_rigid:
            mechanical_score = 0.95
        elif req_mech_level == "High":
            mechanical_score = 0.45 # Flexible pouch subjected to high crush risk
        else:
            mechanical_score = 0.80

        # 6. Sustainability Score
        sust = candidate.get("sustainability", {})
        is_rec = sust.get("recyclable") == "Yes" or "yes" in str(sust.get("recyclable", "")).lower()
        is_bio = sust.get("biodegradable") == "Yes" or "yes" in str(sust.get("biodegradable", "")).lower()
        
        sustainability_score = 0.50
        if is_bio or "kraft paper" in mat:
            sustainability_score = 0.95
        elif "glass" in mat or "aluminium" in mat:
            sustainability_score = 0.90 # Infinitely recyclable
        elif is_rec:
            sustainability_score = 0.80
        elif "multilayer" in mat or "laminate" in mat:
            sustainability_score = 0.40 # Hard to recycle mixed polymers

        # Weighted Composite Score (0.0 to 1.0)
        final_composite = (
            w.get("ml_score", 0.30) * ml_score +
            w.get("barrier_score", 0.20) * barrier_score +
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
