from typing import List, Dict, Any, Tuple
from app.services.data_service import data_service

class ConstraintFilter:
    def __init__(self):
        pass

    def apply_filters(
        self, 
        candidates: List[Dict[str, Any]], 
        user_input: Dict[str, Any], 
        calculated_reqs: Dict[str, Any]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Enforces strict regulatory, compatibility, and physical safety constraints before ML ranking.
        Returns (surviving_candidates, rejected_candidates).
        """
        surviving = []
        rejected = []

        food_cat = str(user_input.get("food_category", "")).lower()
        map_required = str(user_input.get("map_required", "No")).lower() == "yes"
        sustainability_priority = str(user_input.get("sustainability_priority", "Standard")).lower()
        preferred_package_type = str(user_input.get("preferred_package_type", "Any")).strip().lower()
        ph = float(user_input.get("ph", 6.0) or 6.0)

        for cand in candidates:
            reasons_rejected = []
            mat = cand.get("material", "").lower()
            pkg_type = cand.get("packaging_type", "").lower()
            map_suitability = cand.get("map_suitability", "")
            sust = cand.get("sustainability", {})

            # 1. Hard Prohibition Rule: IS 14534 / FSSAI Rule RG004
            # Recycled plastic is strictly prohibited for direct food contact
            if "recycled plastic" in mat or "recycled post-consumer" in mat:
                reasons_rejected.append("Prohibited by FSSAI Regulation 4(4) and IS 14534: Recycled plastics prohibited for direct food contact.")

            # 2. Hard Prohibition Rule: IS 2991 Clause 1.1 / 09 Compatibility
            # Base paper for waxed paper explicitly excluded for confectionery and food wrapping
            if "base paper for waxed paper" in mat and ("confectionery" in food_cat or "sweets" in food_cat):
                reasons_rejected.append("Prohibited by IS 2991:1988 Clause 1.1: Explicitly excludes use for confectionery and direct food wrapping.")

            # 3. High Acid Chemical Interaction: Uncoated bare tinplate/reactive metals for pH < 4.5
            if ph < 4.5 and "tinplate" in mat and "plain" in mat and "lacquered" not in mat:
                reasons_rejected.append("Chemical Incompatibility: Unlacquered plain tinplate susceptible to heavy acid etching and tin dissolution (IS 5837 requires internal lacquering).")

            # 4. MAP Hard Requirement
            # If user demands MAP, porous or unsealable packaging must be rejected
            if map_required:
                if map_suitability == "No" or ("paper" in mat and "laminate" not in mat and "coated" not in mat):
                    reasons_rejected.append("MAP Incompatibility: Product requires gas barrier for modified atmosphere; non-laminated paper/porous material cannot retain CO2/N2 gas blend.")

            # 5. Preferred Package Form filter (if user selected specific non-Any preference)
            if preferred_package_type not in ["any", "", "all", "none"]:
                # Check if package type matches user selection
                if preferred_package_type in ["rigid", "bottle", "can", "jar", "box", "tub"]:
                    if not any(k in pkg_type or k in mat for k in ["rigid", "bottle", "can", "jar", "box", "tub", "tin"]):
                        reasons_rejected.append(f"Format Mismatch: User specified '{preferred_package_type}' but candidate format is flexible.")
                elif preferred_package_type in ["flexible", "pouch", "bag", "wrap"]:
                    if not any(k in pkg_type or k in mat for k in ["flexible", "pouch", "bag", "wrap", "film", "sachet"]):
                        reasons_rejected.append(f"Format Mismatch: User specified '{preferred_package_type}' but candidate format is rigid.")

            # 6. Strict Sustainability Constraint
            if "strict" in sustainability_priority or "zero-plastic" in sustainability_priority:
                # If zero plastic requested, reject non-recyclable multi-material plastics
                if "plastic" in mat and sust.get("recyclable") == "No":
                    reasons_rejected.append("Sustainability Incompatibility: Material is non-recyclable composite, failing user strict sustainability mandate.")

            if reasons_rejected:
                rejected.append({
                    **cand,
                    "rejection_reasons": reasons_rejected,
                    "rejected_by": "HARD_CONSTRAINT_FILTER"
                })
            else:
                surviving.append(cand)

        return surviving, rejected

constraint_filter = ConstraintFilter()
