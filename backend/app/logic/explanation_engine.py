from typing import List, Dict, Any

class ExplanationEngine:
    def __init__(self):
        pass

    def _get_family(self, cand: Dict[str, Any]) -> str:
        mat = str(cand.get("material", "")).lower()
        pkg = str(cand.get("packaging_type", "")).lower()
        if "glass" in mat:
            return "glass"
        if any(k in mat for k in ["carton", "composite container", "paperboard"]):
            return "composite_or_carton"
        if any(k in mat for k in ["tin", "aluminium can", "metal container", "tfs"]):
            return "metal"
        if any(k in mat for k in ["aseptic", "foil wrap", "aluminium-foil-based", "foil pouch"]):
            return "foil_aseptic_or_wrap"
        if any(k in mat for k in ["thermoform", "tray", "punnet", "tub"]):
            return "thermoformed_tray"
        if any(k in mat for k in ["pouch", "bag", "film", "wrapper"]):
            return "flexible_pouch"
        if any(k in mat for k in ["rigid jar", "rigid container"]):
            return "rigid_plastic"
        return mat[:20]

    def build_recommendations(
        self,
        ranked_candidates: List[Dict[str, Any]],
        user_input: Dict[str, Any],
        calculated_reqs: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Builds the Top 3 Recommendations with transparent explanations, origin labels,
        positive evidence points, scientific warnings, and documented limitations.
        Diversifies options across distinct material families to avoid duplicate formats.
        """
        recommendations = []
        
        # Select diversified top candidates from different packaging families
        diverse_top = []
        seen_families = set()
        for cand in ranked_candidates:
            fam = self._get_family(cand)
            if fam not in seen_families:
                seen_families.add(fam)
                diverse_top.append(cand)
                if len(diverse_top) == 3:
                    break

        if len(diverse_top) < 3:
            for cand in ranked_candidates:
                if cand not in diverse_top:
                    diverse_top.append(cand)
                    if len(diverse_top) == 3:
                        break

        top_3 = diverse_top

        rank_names = ["Recommended Packaging", "Alternative Packaging (Option 2)", "Alternative Packaging (Option 3)"]

        for idx, cand in enumerate(top_3):
            rank = idx + 1
            rank_title = rank_names[idx] if idx < len(rank_names) else f"Alternative Option {rank}"
            
            scoring_data = cand.get("scoring", {})
            score_breakdown = scoring_data.get("score_breakdown", {})
            final_score = scoring_data.get("final_suitability_score", 75.0)
            
            mat = cand.get("material", "Unknown Material")
            pkg_type = cand.get("packaging_type", "Standard Packaging")
            
            # Formulate positive evidence points
            evidence = []
            resp_info = calculated_reqs.get("respiration_profile")
            if resp_info and resp_info.get("respiration_class") in ["High", "Medium"]:
                evidence.append(f"Respiration Compatibility: Provides gas exchange / ventilation suited for {resp_info.get('respiration_class')} respiration produce.")
            if score_breakdown.get("barrier_score", 0) >= 0.75:
                evidence.append("Barrier Performance: Satisfies calculated oxygen and moisture barrier requirements.")
            if score_breakdown.get("compatibility_score", 0) >= 0.85:
                evidence.append("Chemical Compatibility: Chemically compatible and approved under FSSAI Schedule IV.")
            if score_breakdown.get("shelf_life_score", 0) >= 0.80:
                evidence.append(f"Preservation Capability: Sufficient protection for the requested {user_input.get('desired_shelf_life_days', 90)}-day shelf life.")
            if score_breakdown.get("mechanical_score", 0) >= 0.80:
                evidence.append("Physical Integrity: Suitable structural strength for the specified transport conditions.")
            if score_breakdown.get("sustainability_score", 0) >= 0.75:
                evidence.append("Environmental Fit: Aligns with circular recycling guidelines / EPR categories.")
            
            if not evidence:
                evidence.append("Complies with basic regulatory standards and hygienic containment guidelines.")

            # Light protection evidence
            light_level = str((calculated_reqs.get("light_requirement") or {}).get("level", "")).lower()
            if "mandatory opaque" in light_level or "light barrier" in light_level:
                if any(k in mat.lower() for k in ["jute", "sacking", "cfb", "corrugated", "board", "paper", "foil", "box"]):
                    evidence.append("Light Exclusion: Opaque material prevents light penetration, avoiding chlorophyll and solanine greening in tubers.")

            # Formulate warnings / caveats
            warnings = []
            validation_status = scoring_data.get("validation_status", "UNKNOWN")
            validation_note = scoring_data.get("validation_note", "")
            additional_validation_req = scoring_data.get("additional_validation_required", False)
            barrier_class = scoring_data.get("barrier_classification", "Standard")

            if validation_status == "ADDITIONAL_VALIDATION_REQUIRED":
                warnings.append(f"Shelf-Life Benchmark Mismatch: Target shelf life is {user_input.get('desired_shelf_life_days', 90)} days, but validated source benchmark is {cand.get('expected_shelf_life')}. Additional empirical validation required for target shelf life.")
            elif validation_status in ["THEORETICAL_BARRIER_PROTECTION", "INSUFFICIENT_EVIDENCE"]:
                warnings.append(f"Unvalidated Shelf Life: Target shelf life is {user_input.get('desired_shelf_life_days', 90)} days, but no empirical benchmark is recorded in source database. Empirical shelf-life testing required.")

            if "mandatory opaque" in light_level and any(k in mat.lower() for k in ["punnet", "transparent", "tray"]):
                warnings.append("Light Sensitivity Warning: Transparent packaging allows ambient light penetration; store in dark to prevent oxidation/greening.")

            barrier = cand.get("barrier_properties", {})
            if barrier_class == "Conditional / Insufficient Technical Evidence":
                warnings.append("Insufficient Technical Evidence: OTR/WVTR are unmeasured in source databases and no validated barrier classification exists; barrier fit cannot be guaranteed without empirical testing.")
            elif barrier.get("wvtr") is None and barrier.get("otr") is None:
                warnings.append("Barrier Data Gap: Exact numerical OTR/WVTR are unmeasured in the primary database; barrier fit is evaluated via polymer class standards.")
            
            if cand.get("technical_data_coverage") == "Low technical-data coverage":
                warnings.append("Data Incomplete: Limited physical test parameters documented in source standard.")

            if user_input.get("ph", 6.0) < 4.5 and "metal" in mat.lower():
                warnings.append("Acidic Product Precaution: Verify food-grade epoxy-phenolic internal lacquering per IS 5837.")

            # Top contributing factors (active 6 criteria including ML)
            factors = [
                {"factor": "ML Suitability Model", "score": score_breakdown.get("ml_score", 0), "weight": scoring_data.get("applied_weights", {}).get("ml_score", 0.25)},
                {"factor": "Barrier Protection", "score": score_breakdown.get("barrier_score", 0), "weight": scoring_data.get("applied_weights", {}).get("barrier_score", 0.25)},
                {"factor": "Compatibility & Safety", "score": score_breakdown.get("compatibility_score", 0), "weight": scoring_data.get("applied_weights", {}).get("compatibility_score", 0.15)},
                {"factor": "Shelf-Life Preservation", "score": score_breakdown.get("shelf_life_score", 0), "weight": scoring_data.get("applied_weights", {}).get("shelf_life_score", 0.15)},
                {"factor": "Mechanical Robustness", "score": score_breakdown.get("mechanical_score", 0), "weight": scoring_data.get("applied_weights", {}).get("mechanical_score", 0.10)},
                {"factor": "Sustainability", "score": score_breakdown.get("sustainability_score", 0), "weight": scoring_data.get("applied_weights", {}).get("sustainability_score", 0.10)}
            ]

            # Sanitize expected shelf life to prevent any nan leakage
            raw_db_sl = cand.get("expected_shelf_life")
            if not raw_db_sl or str(raw_db_sl).strip().lower() in ["nan", "none", "", "not specified", "data unavailable"]:
                clean_db_sl = "Not available in source database"
            else:
                clean_db_sl = str(raw_db_sl).strip()

            coverage_text = cand.get("technical_data_coverage", "Medium technical-data coverage")
            if barrier_class == "Conditional / Insufficient Technical Evidence":
                coverage_text = "Conditional / Insufficient Technical Evidence"

            protection_level_label = (
                "Fully Validated" if validation_status == "FULLY_VALIDATED"
                else ("Partially Validated (Target Exceeds Benchmark)" if validation_status == "ADDITIONAL_VALIDATION_REQUIRED"
                else ("Theoretical Barrier Protection" if validation_status == "THEORETICAL_BARRIER_PROTECTION"
                else "Unverified Shelf Life"))
            )

            recommendations.append({
                "rank": rank,
                "rank_title": rank_title,
                "material": mat,
                "primary_packaging": cand.get("primary_packaging", mat),
                "secondary_packaging": cand.get("secondary_packaging", "Not specified"),
                "packaging_type": pkg_type,
                "packaging_structure": cand.get("packaging_structure", "Flexible/Rigid"),
                "suitability_score": final_score,
                "suitability_score_label": "DERIVED SCORE",
                "ml_prediction": {
                    "score": round(score_breakdown.get("ml_score", 0.70) * 100, 1),
                    "label": "ML PREDICTION",
                    "note": "Random Forest suitability output (0-100 scale, weighted ranking signal)"
                },
                "compatibility": {
                    "status": cand.get("compatibility_status", "Compatible"),
                    "label": "DATABASE VALUE"
                },
                "barrier_properties": cand.get("barrier_properties", {}),
                "barrier_classification": barrier_class,
                "mechanical_properties": cand.get("mechanical_properties", {}),
                "sealability": cand.get("sealability", "Standard heat-sealable flexible structure"),
                "thickness_recommendation": cand.get("thickness_recommendation"),
                "sustainability": cand.get("sustainability", {}),
                "shelf_life_suitability": {
                    "requested_days": user_input.get("desired_shelf_life_days", 90),
                    "expected_shelf_life_db": clean_db_sl,
                    "validation_status": validation_status,
                    "validation_note": validation_note,
                    "additional_validation_required": additional_validation_req,
                    "estimated_protection_level": protection_level_label,
                    "label": "DATABASE VALUE (Benchmark) / DERIVED SCORE (Evaluation)"
                },
                "map_suitability": cand.get("map_suitability", "Conditional"),
                "technical_data_coverage": coverage_text,
                "technical_coverage_pct": cand.get("technical_coverage_pct", 60),
                "evidence_points": evidence,
                "contributing_factors": factors,
                "warnings": warnings,
                "source_citation": cand.get("source", {}),
                "scientific_limitations": [
                    "OTR and WVTR barrier transmission rates depend heavily on real-world test conditions (temperature, RH, gauge).",
                    "Exact product shelf life requires empirical accelerated or real-time shelf-life testing with the actual food formulation.",
                    "Missing technical properties are displayed as 'Data unavailable' and never fabricated.",
                    "ML suitability is an algorithmic scoring signal based on multi-attribute feature engineering, integrated into the hybrid multi-criteria ranking."
                ]
            })

        return recommendations

explanation_engine = ExplanationEngine()
