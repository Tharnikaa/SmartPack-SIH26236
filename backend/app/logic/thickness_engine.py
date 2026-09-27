"""
Fick's-Law Packaging Thickness Solver for SmartPack.

Calculates required polymer film thickness to satisfy product preservation
oxygen (OTR) and moisture (WVTR) limits based on Fick's first law of diffusion:
    permeability (P) = transmission_rate (TR) * reference_thickness
    required_thickness = P / required_TR

Standard commercial film gauges: 25, 37, 50, 75, 100 microns.
"""

from typing import Dict, Any, Optional, Tuple, Union
import logging
import math

logger = logging.getLogger(__name__)

STANDARD_GAUGES = [25, 37, 50, 75, 100]

class ThicknessRecommendation(dict):
    """
    Dictionary representation of thickness recommendation supporting both
    dictionary field lookups and transparent string comparisons (e.g. 'N/A — rigid, impermeable').
    """
    def __str__(self) -> str:
        return str(self.get("gauge_display") or self.get("method") or "N/A")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return other in (
                self.get("gauge_display"),
                self.get("method"),
                self.get("label"),
                self.get("recommended_gauge")
            )
        return super().__eq__(other)


class ThicknessEngine:
    def __init__(self):
        pass

    def get_target_limits(self, reqs: Dict[str, Any]) -> Dict[str, float]:
        """
        Derives target OTR and WVTR thresholds from requirement engine's 0-1 scores.
        
        NOTE: Clearly labeled as an illustrative threshold mapping to refine later with
        empirical food-package testing, not a hard scientific constant:
          score >= 0.7 (High)   -> target OTR <= 5 cc/m2/day,   target WVTR <= 2 g/m2/day
          score 0.4-0.7 (Medium)-> target OTR <= 500 cc/m2/day, target WVTR <= 10 g/m2/day
          score < 0.4 (Low)     -> target OTR <= 5000 cc/m2/day,target WVTR <= 20 g/m2/day
        """
        o2_score = 0.5
        h2o_score = 0.5

        if reqs:
            o2_obj = reqs.get("oxygen_requirement", {})
            if isinstance(o2_obj, dict):
                o2_score = float(o2_obj.get("score", 0.5))
            elif isinstance(o2_obj, (int, float)):
                o2_score = float(o2_obj)

            h2o_obj = reqs.get("moisture_requirement", {})
            if isinstance(h2o_obj, dict):
                h2o_score = float(h2o_obj.get("score", 0.5))
            elif isinstance(h2o_obj, (int, float)):
                h2o_score = float(h2o_obj)

        if o2_score >= 0.7:
            target_otr = 5.0
        elif o2_score >= 0.4:
            target_otr = 500.0
        else:
            target_otr = 5000.0

        if h2o_score >= 0.7:
            target_wvtr = 2.0
        elif h2o_score >= 0.4:
            target_wvtr = 10.0
        else:
            target_wvtr = 20.0

        return {
            "target_otr": target_otr,
            "target_wvtr": target_wvtr,
            "o2_score": o2_score,
            "h2o_score": h2o_score,
            "threshold_disclaimer": "Illustrative threshold mapping to refine later, not a hard scientific constant"
        }

    def _round_to_standard_gauge(self, thickness: float) -> Tuple[int, str]:
        """Rounds up to standard commercial gauge: 25, 37, 50, 75, 100 micron."""
        for g in STANDARD_GAUGES:
            if thickness <= g:
                return g, f"{g} µm"
        # If exceeds 100 microns
        rounded = int(math.ceil(thickness))
        return rounded, f">100 µm ({rounded} µm - requires barrier coating / laminate)"

    def calculate_thickness(
        self,
        material_name: str,
        barrier_props: Dict[str, Any],
        reqs: Dict[str, Any],
        ref_row: Optional[Dict[str, Any]] = None
    ) -> ThicknessRecommendation:
        """
        Solves Fick's-law thickness for candidate material:
          permeability = ref_transmission * ref_thickness_micron
          required_thickness = permeability / target_limit
          take max(required_otr_thickness, required_wvtr_thickness)
          round up to nearest standard gauge (25/37/50/75/100 µm).

        Skip calculation for glass/tinplate -> 'N/A — rigid, impermeable'.
        Label laminate/metalized -> 'estimated (multilayer)'.
        """
        mat_lower = material_name.lower()
        targets = self.get_target_limits(reqs)
        target_otr = targets["target_otr"]
        target_wvtr = targets["target_wvtr"]

        # 1. Skip calculation for rigid impermeable materials (glass, tinplate, cans, REF-18, REF-19)
        ref_id = str(ref_row.get("material_id", "")) if ref_row else ""
        is_flexible_composite = any(k in mat_lower for k in ["pouch", "laminate", "film", "flexible", "wrap", "foil"])
        is_rigid_container = (
            (ref_id in ["REF-18", "REF-19"] or any(k in mat_lower for k in [
                "glass", "tinplate", "tin-free", "tin can", "metal can", "steel can", "rigid can"
            ]))
            and not is_flexible_composite
        )
        if is_rigid_container:
            return ThicknessRecommendation({
                "recommended_gauge_micron": None,
                "gauge_display": "N/A — rigid, impermeable",
                "calculated_thickness_micron": None,
                "limiting_barrier": "N/A",
                "method": "N/A — rigid, impermeable",
                "label": "N/A — rigid, impermeable",
                "target_otr": target_otr,
                "target_wvtr": target_wvtr,
                "threshold_disclaimer": targets["threshold_disclaimer"],
                "notes": "Glass and rigid metal containers are impermeable barriers; thickness scaling is non-applicable."
            })

        # 2. Check porous/uncoated paper
        if "paper" in mat_lower and not any(k in mat_lower for k in ["laminate", "coated", "poly", "aseptic"]):
            return ThicknessRecommendation({
                "recommended_gauge_micron": None,
                "gauge_display": "N/A — porous material",
                "calculated_thickness_micron": None,
                "limiting_barrier": "N/A",
                "method": "N/A — porous material",
                "label": "N/A — porous material",
                "target_otr": target_otr,
                "target_wvtr": target_wvtr,
                "threshold_disclaimer": targets["threshold_disclaimer"],
                "notes": "Uncoated paper has no meaningful gas/moisture barrier without polymer or foil lamination."
            })

        # Determine reference values
        ref_thickness = 25.0
        otr_val = None
        wvtr_val = None

        if ref_row is not None and not (isinstance(ref_row, dict) and len(ref_row) == 0):
            try:
                ref_thickness = float(ref_row.get("reference_thickness_micron", 25.0) or 25.0)
            except (ValueError, TypeError):
                ref_thickness = 25.0

            # OTR
            try:
                o_hi = ref_row.get("otr_high")
                o_lo = ref_row.get("otr_low")
                if o_hi is not None and not str(o_hi).strip().lower().startswith("nan"):
                    otr_val = float(o_hi)
                elif o_lo is not None and not str(o_lo).strip().lower().startswith("nan"):
                    otr_val = float(o_lo)
            except (ValueError, TypeError):
                otr_val = None

            # WVTR
            try:
                w_hi = ref_row.get("wvtr_high")
                w_lo = ref_row.get("wvtr_low")
                if w_hi is not None and not str(w_hi).strip().lower().startswith("nan"):
                    wvtr_val = float(w_hi)
                elif w_lo is not None and not str(w_lo).strip().lower().startswith("nan"):
                    wvtr_val = float(w_lo)
            except (ValueError, TypeError):
                wvtr_val = None

        # Fallback to barrier_props dict if reference row didn't yield numbers
        if otr_val is None and barrier_props.get("otr") is not None:
            try:
                otr_val = float(barrier_props["otr"])
            except (ValueError, TypeError):
                pass

        if wvtr_val is None and barrier_props.get("wvtr") is not None:
            try:
                wvtr_val = float(barrier_props["wvtr"])
            except (ValueError, TypeError):
                pass

        # If barrier values are effectively 0 (foil laminate)
        if otr_val == 0.0 and (wvtr_val is not None and wvtr_val <= 0.3):
            is_multi = True
            return ThicknessRecommendation({
                "recommended_gauge_micron": 25,
                "gauge_display": "25 µm (minimum standard gauge)",
                "calculated_thickness_micron": 25.0,
                "limiting_barrier": "Structural/Handling",
                "method": "estimated (multilayer)",
                "label": "estimated (multilayer)",
                "target_otr": target_otr,
                "target_wvtr": target_wvtr,
                "threshold_disclaimer": targets["threshold_disclaimer"],
                "notes": "Aluminum foil / high-barrier laminate provides near-zero permeability; 25 µm standard composite gauge recommended for mechanical pinhole resistance."
            })

        # Calculate thickness for OTR and WVTR via Fick's law
        req_thick_otr = None
        if otr_val is not None and otr_val > 0 and target_otr > 0:
            perm_otr = otr_val * ref_thickness
            req_thick_otr = perm_otr / target_otr

        req_thick_wvtr = None
        if wvtr_val is not None and wvtr_val > 0 and target_wvtr > 0:
            perm_wvtr = wvtr_val * ref_thickness
            req_thick_wvtr = perm_wvtr / target_wvtr

        if req_thick_otr is None and req_thick_wvtr is None:
            return ThicknessRecommendation({
                "recommended_gauge_micron": 25,
                "gauge_display": "25 µm (default standard gauge)",
                "calculated_thickness_micron": None,
                "limiting_barrier": "Data unavailable",
                "method": "estimated (standard default)",
                "label": "estimated (standard default)",
                "target_otr": target_otr,
                "target_wvtr": target_wvtr,
                "threshold_disclaimer": targets["threshold_disclaimer"],
                "notes": "Empirical transmission rates unavailable; standard baseline gauge assigned."
            })

        # Take the larger of the two
        if req_thick_otr is not None and req_thick_wvtr is not None:
            if req_thick_otr >= req_thick_wvtr:
                raw_required = req_thick_otr
                limiting = "OTR"
            else:
                raw_required = req_thick_wvtr
                limiting = "WVTR"
        elif req_thick_otr is not None:
            raw_required = req_thick_otr
            limiting = "OTR"
        else:
            raw_required = req_thick_wvtr
            limiting = "WVTR"

        std_gauge, gauge_display = self._round_to_standard_gauge(raw_required)

        # Multi-layer / metalized identification
        is_multilayer = any(k in mat_lower for k in [
            "laminate", "multilayer", "metalized", "metallized", "retort",
            "foil", "composite", "aseptic", "tetra", "pvdc"
        ])

        method_str = "estimated (multilayer)" if is_multilayer else "calculated"

        return ThicknessRecommendation({
            "recommended_gauge_micron": std_gauge,
            "gauge_display": gauge_display,
            "calculated_thickness_micron": round(raw_required, 2),
            "limiting_barrier": limiting,
            "method": method_str,
            "label": method_str,
            "target_otr": target_otr,
            "target_wvtr": target_wvtr,
            "threshold_disclaimer": targets["threshold_disclaimer"],
            "notes": f"Required thickness driven by {limiting} protection to meet food shelf-life requirement."
        })

thickness_engine = ThicknessEngine()
