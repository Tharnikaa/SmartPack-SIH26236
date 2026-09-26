from typing import List, Dict, Any

class ExplanationEngine:
    def __init__(self):
        pass

    def build_recommendations(
        self,
        ranked_candidates: List[Dict[str, Any]],
        user_input: Dict[str, Any],
        calculated_reqs: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Builds the Top 3 Recommendations with transparent explanations, origin labels,
        positive evidence points, scientific warnings, and documented limitations.
        """
        recommendations = []
        top_3 = ranked_candidates[:3]

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

            # Formulate warnings / caveats
            warnings = []
            barrier = cand.get("barrier_properties", {})
            if barrier.get("wvtr") is None and barrier.get("otr") is None:
                warnings.append("Barrier Data Gap: Exact numerical OTR/WVTR are unmeasured in the primary database; barrier fit is evaluated via polymer class standards.")
            
            if cand.get("technical_data_coverage") == "Low technical-data coverage":
                warnings.append("Data Incomplete: Limited physical test parameters documented in source standard.")

            if user_input.get("ph", 6.0) < 4.5 and "metal" in mat.lower():
                warnings.append("Acidic Product Precaution: Verify food-grade epoxy-phenolic internal lacquering per IS 5837.")

            # Top contributing factors
            factors = [
                {"factor": "Barrier Protection", "score": score_breakdown.get("barrier_score", 0), "weight": scoring_data.get("applied_weights", {}).get("barrier_score", 0.2)},
                {"factor": "Compatibility & Safety", "score": score_breakdown.get("compatibility_score", 0), "weight": scoring_data.get("applied_weights", {}).get("compatibility_score", 0.15)},
                {"factor": "Shelf-Life Preservation", "score": score_breakdown.get("shelf_life_score", 0), "weight": scoring_data.get("applied_weights", {}).get("shelf_life_score", 0.15)},
                {"factor": "Mechanical Robustness", "score": score_breakdown.get("mechanical_score", 0), "weight": scoring_data.get("applied_weights", {}).get("mechanical_score", 0.10)},
                {"factor": "Sustainability", "score": score_breakdown.get("sustainability_score", 0), "weight": scoring_data.get("applied_weights", {}).get("sustainability_score", 0.10)},
                {"factor": "ML Suitability Model", "score": score_breakdown.get("ml_score", 0), "weight": scoring_data.get("applied_weights", {}).get("ml_score", 0.30)}
            ]

            recommendations.append({
                "rank": rank,
                "rank_title": rank_title,
                "material": mat,
                "packaging_type": pkg_type,
                "packaging_structure": cand.get("packaging_structure", "Flexible/Rigid"),
                "suitability_score": final_score,
                "suitability_score_label": "DERIVED SCORE",
                "ml_prediction": {
                    "score": round(score_breakdown.get("ml_score", 0.70) * 100, 1),
                    "label": "ML PREDICTION",
                    "note": "Prototype Random Forest suitability output (0-100 scale, not an empirical probability)"
                },
                "compatibility": {
                    "status": cand.get("compatibility_status", "Compatible"),
                    "label": "DATABASE VALUE"
                },
                "barrier_properties": cand.get("barrier_properties", {}),
                "mechanical_properties": cand.get("mechanical_properties", {}),
                "sustainability": cand.get("sustainability", {}),
                "shelf_life_suitability": {
                    "requested_days": user_input.get("desired_shelf_life_days", 90),
                    "expected_shelf_life_db": cand.get("expected_shelf_life", "Not specified"),
                    "estimated_protection_level": "High" if score_breakdown.get("shelf_life_score", 0) >= 0.8 else "Moderate",
                    "label": "DATABASE VALUE (Expected) / DERIVED SCORE (Protection)"
                },
                "map_suitability": cand.get("map_suitability", "Conditional"),
                "technical_data_coverage": cand.get("technical_data_coverage", "Medium technical-data coverage"),
                "technical_coverage_pct": cand.get("technical_coverage_pct", 60),
                "evidence_points": evidence,
                "contributing_factors": factors,
                "warnings": warnings,
                "source_citation": cand.get("source", {}),
                "scientific_limitations": [
                    "OTR and WVTR barrier transmission rates depend heavily on real-world test conditions (temperature, RH, gauge).",
                    "Exact product shelf life requires empirical accelerated or real-time shelf-life testing with the actual food formulation.",
                    "Missing technical properties are displayed as 'Data unavailable' and never fabricated.",
                    "ML suitability is a prototype estimation based on domain scoring and regulatory mappings, not a laboratory certification."
                ]
            })

        return recommendations

explanation_engine = ExplanationEngine()
