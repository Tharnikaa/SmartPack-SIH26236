import re
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

        food_name = str(user_input.get("food_name", "")).strip().lower()
        food_cat = str(user_input.get("food_category", "")).lower()
        map_required = str(user_input.get("map_required", "No")).lower() == "yes"
        sustainability_priority = str(user_input.get("sustainability_priority", "Standard")).lower()
        preferred_package_type = str(user_input.get("preferred_package_type", "Any")).strip().lower()
        ph = float(user_input.get("ph", 6.0) or 6.0)

        resp_prof = calculated_reqs.get("respiration_profile") or {}
        respiration_level = str(resp_prof.get("respiration_class") or user_input.get("respiration_activity", "Low")).title()
        gas_req = str((calculated_reqs.get("map_gas_requirement") or {}).get("level", "")).lower()

        # Identify if this is raw fresh produce (not processed/canned/retorted/cooked)
        is_fresh_produce = (
            any(k in food_cat for k in ["fruit", "vegetable", "root", "tuber", "produce"]) and
            not any(k in food_name for k in ["pickle", "jam", "jelly", "canned", "retort", "puree", "sauce", "paste", "fried", "chip", "flour", "dried", "cooked", "juice", "beverage", "syrup", "chutney"])
        )

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
            # If user demands MAP, porous, open-weave, or unsealed packaging must be rejected
            if map_required:
                is_porous_or_unsealed = (
                    any(k in mat for k in ["jute", "sacking", "hessian", "burlap", "mesh", "net"]) or
                    ("box" in mat and "except top" in mat) or
                    ("paper" in mat and not any(k in mat for k in ["laminate", "coated", "foil", "aluminium", "aluminum"]))
                )
                if is_porous_or_unsealed or str(map_suitability).lower().startswith("no"):
                    reasons_rejected.append("MAP Incompatibility: Product requires gas barrier for modified atmosphere (MAP); porous or unsealed container cannot retain protective N2/CO2 gas blend.")

            # 5. Preferred Package Form filter (if user selected specific non-Any preference)
            if preferred_package_type not in ["any", "", "all", "none"]:
                req_title = preferred_package_type.capitalize()
                # Check if package type matches user selection
                if preferred_package_type in ["rigid", "bottle", "can", "jar", "box", "tub", "tray", "punnet"]:
                    if not any(k in pkg_type or k in mat for k in ["rigid", "bottle", "can", "jar", "box", "tub", "tin", "tray", "punnet", "crate"]):
                        reasons_rejected.append(f"Format Incompatibility: Candidate format is Flexible, which does not satisfy the specified {req_title} packaging requirement.")
                elif preferred_package_type in ["flexible", "pouch", "bag", "wrap"]:
                    if not any(k in pkg_type or k in mat for k in ["flexible", "pouch", "bag", "wrap", "film", "sachet", "liner", "sacking", "net", "mesh"]):
                        reasons_rejected.append(f"Format Incompatibility: Candidate format is Rigid, which does not satisfy the specified {req_title} packaging requirement.")

            # 6. Strict Sustainability Constraint
            if "strict" in sustainability_priority or "zero-plastic" in sustainability_priority:
                # If zero plastic requested, reject non-recyclable multi-material plastics
                if "plastic" in mat and sust.get("recyclable") == "No":
                    reasons_rejected.append("Sustainability Incompatibility: Material is non-recyclable composite, failing user strict sustainability mandate.")

            # 7. Respiration & Gas Exchange Hard Compatibility Interlock
            # Fresh respiring produce requires controlled gas exchange / breathability.
            # Airtight, hermetic containers (cans, glass bottles without breathability, non-perforated foil/retort pouches)
            # cause anaerobic fermentation, off-odors, and tissue breakdown in fresh commodities.
            if is_fresh_produce:
                # Airtight metal cans (tinplate, aluminium can, TFS can, tin container)
                if any(k in mat for k in ["tinplate", "aluminium can", "tfs", "tin container"]) or (re.search(r'\bcan\b', mat) and "box" not in mat and "cfb" not in mat and "jute" not in mat):
                    reasons_rejected.append(f"Respiration Incompatibility: Fresh respiring produce ({user_input.get('food_name', 'produce')}, {respiration_level} respiration) sealed in airtight metal cans experiences rapid oxygen starvation and anaerobic rot (metal canning requires thermal sterilization for processed foods).")
                # Airtight glass containers without ventilation
                elif "glass bottle" in mat or "glass jar" in mat:
                    reasons_rejected.append(f"Respiration Incompatibility: Airtight hermetic glass containers without gas exchange induce rapid anaerobic decay in fresh produce (Schedule IV lists glass for processed preserves/juices).")
                # Impermeable aseptic/retort barrier
                elif "retort" in mat or ("aluminium foil" in mat and "aseptic" in mat):
                    reasons_rejected.append(f"Respiration Incompatibility: Impermeable aseptic/retort barrier suffocates respiring fresh produce unless specially micro-perforated.")
                # Blister pack with foil/PE lid is for unit-portion jams/jellies/purees
                elif "blister" in mat or ("thermoformed" in mat and "foil" in mat):
                    reasons_rejected.append("Format Incompatibility: Thermoformed blister container with foil lid is intended for portion-packaged jams, jellies, or processed fruit spreads, not whole fresh respiring produce.")
                # Stand-up pouch with spout is meant for liquids/purees
                elif "spout" in mat or "spout" in pkg_type:
                    reasons_rejected.append("Format Incompatibility: Stand-up pouch with spout is designed for liquid/pureed products, not whole fresh produce.")
                # Rigid plastic jars with screw caps lack ventilation for fresh produce
                elif any(k in mat for k in ["plastic rigid jar", "plastic jar"]):
                    reasons_rejected.append("Format Incompatibility: Rigid plastic jars with screw caps are designed for dry foods, confectionery, or processed pastes/spreads, lacking the ventilation needed for fresh produce.")

            # 8. Snack / Dry Crisp Physical Dispensing Interlock
            # Planar crispy snacks (chips, crisps, wafers, crackers) cannot physically fit or dispense through narrow-neck bottle openings
            is_dry_crisp = any(k in food_name for k in ["chip", "crisp", "wafer", "cracker"])
            if is_dry_crisp:
                if "bottle" in mat or "bottle" in pkg_type or "wooden cask" in mat:
                    reasons_rejected.append("Physical Format Incompatibility: Narrow-neck bottle packaging cannot accommodate or dispense brittle, planar crispy snack solids (bottles are designed for flowable liquids, syrups, and beverages).")

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
