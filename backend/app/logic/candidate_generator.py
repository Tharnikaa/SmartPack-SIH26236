from typing import List, Dict, Any, Optional
import re
import pandas as pd
from app.services.data_service import data_service
from app.logic.thickness_engine import thickness_engine

class CandidateGenerator:
    def __init__(self):
        pass

    def _match_reference_row(self, material_name: str) -> Optional[pd.Series]:
        """
        Matches a packaging material candidate against 16_material_barrier_mechanical_reference.csv
        by material family keyword (ldpe, hdpe, pet, pp, bopp, evoh, foil, glass, tinplate, pla,
        pbat, cellulose, kraft, nylon/pa, pvc, pvdc, metalized, retort).
        """
        df = data_service.material_reference_df
        if df.empty:
            return None

        m = material_name.lower()

        # 1. Retort pouch laminate
        if "retort" in m:
            match = df[df["material_id"] == "REF-20"]
            if not match.empty:
                return match.iloc[0]

        # 2. Foil / Aluminium laminate
        if any(k in m for k in ["foil", "aluminium", "aluminum"]):
            match = df[df["material_id"] == "REF-13"]
            if not match.empty:
                return match.iloc[0]

        # 3. Metalized films
        if any(k in m for k in ["metalized", "metallized"]):
            if any(k in m for k in ["pet", "polyester"]):
                match = df[df["material_id"] == "REF-12"]
                if not match.empty:
                    return match.iloc[0]
            match = df[df["material_id"] == "REF-11"]
            if not match.empty:
                return match.iloc[0]

        # 4. EVOH
        if "evoh" in m:
            match = df[df["material_id"] == "REF-09"]
            if not match.empty:
                return match.iloc[0]

        # 5. PVDC / Saran
        if any(k in m for k in ["pvdc", "saran"]):
            match = df[df["material_id"] == "REF-08"]
            if not match.empty:
                return match.iloc[0]

        # 6. Glass
        if "glass" in m:
            match = df[df["material_id"] == "REF-19"]
            if not match.empty:
                return match.iloc[0]

        # 7. Tinplate / Can / Steel
        if any(k in m for k in ["tin", "tinplate", "can", "steel", "tfs"]):
            match = df[df["material_id"] == "REF-18"]
            if not match.empty:
                return match.iloc[0]

        # 8. Biodegradable (PLA, PBAT)
        if "pbat" in m:
            match = df[df["material_id"] == "REF-15"]
            if not match.empty:
                return match.iloc[0]
        if "pla" in m:
            match = df[df["material_id"] == "REF-14"]
            if not match.empty:
                return match.iloc[0]

        # 9. Nylon / Polyamide / BOPA
        if any(k in m for k in ["nylon", "bopa", "polyamide"]) or re.search(r'\bpa\b', m) or "pa/" in m:
            match = df[df["material_id"] == "REF-10"]
            if not match.empty:
                return match.iloc[0]

        # 10. PVC / Vinyl
        if any(k in m for k in ["pvc", "vinyl"]):
            match = df[df["material_id"] == "REF-07"]
            if not match.empty:
                return match.iloc[0]

        # 11. Kraft / Paper
        if any(k in m for k in ["kraft", "paper", "board", "carton"]):
            match = df[df["material_id"] == "REF-17"]
            if not match.empty:
                return match.iloc[0]

        # 12. Cellulose / Cellophane
        if any(k in m for k in ["cellulose", "cellophane"]):
            match = df[df["material_id"] == "REF-16"]
            if not match.empty:
                return match.iloc[0]

        # 13. Polypropylene (BOPP, CPP, PP)
        if "bopp" in m:
            match = df[df["material_id"] == "REF-05"]
            if not match.empty:
                return match.iloc[0]
        if "cpp" in m or "cast polypropylene" in m:
            match = df[df["material_id"] == "REF-04"]
            if not match.empty:
                return match.iloc[0]
        if "pp" in m or "polypropylene" in m or re.search(r'\bpp\b', m) or "/pp" in m:
            match = df[df["material_id"] == "REF-05"]
            if not match.empty:
                return match.iloc[0]

        # 14. Polyethylene (LLDPE, HDPE, LDPE, PE)
        if "lldpe" in m:
            match = df[df["material_id"] == "REF-02"]
            if not match.empty:
                return match.iloc[0]
        if "hdpe" in m:
            match = df[df["material_id"] == "REF-03"]
            if not match.empty:
                return match.iloc[0]
        if "ldpe" in m:
            match = df[df["material_id"] == "REF-01"]
            if not match.empty:
                return match.iloc[0]
        if "pe" in m or "polyethylene" in m or re.search(r'\bpe\b', m) or "/pe" in m:
            match = df[df["material_id"] == "REF-01"]
            if not match.empty:
                return match.iloc[0]

        # 15. PET / Polyester / BOPET
        if any(k in m for k in ["pet", "bopet", "polyester"]) or re.search(r'\bpet\b', m) or "pet/" in m:
            match = df[df["material_id"] == "REF-06"]
            if not match.empty:
                return match.iloc[0]

        # 16. Multilayer laminate fallback
        if any(k in m for k in ["laminate", "multilayer", "composite"]):
            match = df[df["material_id"] == "REF-20"]
            if not match.empty:
                return match.iloc[0]

        return None

    def generate_candidates(self, user_input: Dict[str, Any], calculated_reqs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generates packaging candidates from the authoritative FSSAI Schedule IV recommendations
        (14_recommended_packaging.csv) and material specifications (06_packaging_material_dataset.csv),
        annotating each candidate with exact database values, published literature reference values,
        Fick's-law thickness solver recommendations, origin citations, and sealability.
        """
        food_name = str(user_input.get("food_name", "")).strip().lower()
        food_cat = str(user_input.get("food_category", "")).strip()
        preferred_type = str(user_input.get("preferred_package_type", "Any")).strip().lower()

        candidates: List[Dict[str, Any]] = []
        rec_df = data_service.recommended_df

        if rec_df.empty:
            return []

        # Find category matches in 14_recommended_packaging.csv
        matched_rows = pd.DataFrame()
        cat_lower = food_cat.lower()
        name_lower = food_name.lower()

        # 1. Direct commodity name matches in FSSAI/ICAR (e.g. Mango, Sapota, Foodgrains)
        if name_lower:
            name_matches = rec_df[rec_df['food_name'].astype(str).str.lower().apply(lambda x: any(w in x for w in name_lower.split() if len(w) > 3))]
            if not name_matches.empty:
                matched_rows = pd.concat([matched_rows, name_matches])

        # 2. Category normalization for FSSAI Schedule IV lookup
        search_terms = []
        if any(k in cat_lower for k in ['root', 'tuber']):
            search_terms = ['fruit & vegetable', 'vegetable']
        elif 'fruit' in cat_lower:
            search_terms = ['fruit']
        elif 'vegetable' in cat_lower:
            search_terms = ['vegetable', 'fruit & vegetable']
        elif food_cat:
            search_terms = [food_cat]

        for term in search_terms:
            mask = rec_df['food_category'].astype(str).str.contains(re.escape(term), case=False, na=False)
            # Never pull beverage categories when searching for solid fruit/vegetables
            if any(k in cat_lower for k in ['fruit', 'vegetable', 'root', 'tuber', 'produce']):
                mask = mask & (~rec_df['food_category'].astype(str).str.contains('Beverage', case=False, na=False))
            sub = rec_df[mask]
            if not sub.empty:
                matched_rows = pd.concat([matched_rows, sub])

        # 3. For bulk tubers / root crops (like Potato) or foodgrains, also include breathable bulk storage from rec_df
        if any(k in cat_lower or k in name_lower for k in ['potato', 'tuber', 'root', 'onion']):
            bulk_mask = rec_df['recommended_packaging_material'].astype(str).str.contains('Jute|Corrugated', case=False, na=False)
            matched_rows = pd.concat([matched_rows, rec_df[bulk_mask]])

        matched_rows = matched_rows.drop_duplicates()
        if matched_rows.empty:
            matched_rows = rec_df.head(15)

        for idx, row in matched_rows.iterrows():
            mat_raw = str(row.get("recommended_packaging_material", "Unknown"))
            raw_type = row.get("recommended_packaging_type")
            if pd.isna(raw_type) or str(raw_type).strip().lower() in ["nan", "none", ""]:
                if any(k in mat_raw.lower() for k in ["bottle", "jar", "can", "tin", "box", "tub", "tray", "punnet", "crate"]):
                    pkg_type = "Rigid Container"
                elif any(k in mat_raw.lower() for k in ["pouch", "bag", "wrap", "film", "sachet", "liner", "sacking", "net", "mesh"]):
                    pkg_type = "Flexible Pouch / Wrap"
                else:
                    pkg_type = "Standard Food Packaging"
            else:
                pkg_type = str(raw_type).strip()

            raw_struct = row.get("recommended_packaging_structure")
            pkg_struct = "Standard Form" if pd.isna(raw_struct) or str(raw_struct).strip().lower() in ["nan", "none"] else str(raw_struct).strip()
            expected_sl = str(row.get("expected_shelf_life", "Not specified"))
            storage_cond = str(row.get("storage_condition", "Ambient"))
            source_doc = str(row.get("source_document", "FSSAI Packaging Regulations / ICAR"))
            page_num = str(row.get("page_number", ""))
            original_reason = str(row.get("reason", "Regulator-endorsed packaging for this food category"))

            # Packaging Material Metadata & Properties Lookup
            barrier_data = self._lookup_barrier(mat_raw)
            mechanical_props = self._lookup_properties(mat_raw)
            sust_data = self._lookup_sustainability(mat_raw)
            cpcb_recyclability = self._lookup_recyclability(mat_raw)
            sealability_val = self._lookup_sealability(mat_raw, pkg_type)

            # Fick's-law thickness solver (step c)
            ref_row_dict = barrier_data.get("_ref_row")
            thickness_rec = thickness_engine.calculate_thickness(
                material_name=mat_raw,
                barrier_props=barrier_data,
                reqs=calculated_reqs,
                ref_row=ref_row_dict
            )

            # Determine Technical Data Coverage
            coverage_score = self._compute_coverage(barrier_data, mechanical_props, sust_data)

            # MAP suitability estimation based on numerical OTR check (step j)
            otr_val = barrier_data.get("otr")
            map_suitable = None
            if otr_val is not None:
                try:
                    otr_num = float(otr_val)
                    if otr_num <= 20.0:
                        map_suitable = "Yes"
                    elif otr_num <= 500.0:
                        map_suitable = "Conditional/Low"
                    else:
                        map_suitable = "No (Not suitable without added barrier layer)"
                except (ValueError, TypeError):
                    map_suitable = None

            if map_suitable is None:
                # Fallback to structure keyword heuristic when no numerical OTR is available
                if any(k in mat_raw.lower() or k in pkg_type.lower() for k in ["laminate", "barrier", "evoh", "map", "retort", "vacuum", "rigid", "glass", "tin"]):
                    map_suitable = "Conditional/Low (Rough estimate - unverified barrier)"
                else:
                    map_suitable = "No (Rough estimate - unverified barrier)"

            candidate = {
                "candidate_id": f"CAND-{idx:03d}",
                "material": mat_raw,
                "packaging_type": pkg_type,
                "packaging_structure": pkg_struct,
                "storage_condition": storage_cond,
                "expected_shelf_life": expected_sl,
                "source": {
                    "document": source_doc,
                    "page": page_num,
                    "label": "DATABASE VALUE"
                },
                "barrier_properties": {
                    "otr": barrier_data.get("otr"),
                    "otr_unit": barrier_data.get("otr_unit", "cc/m2/day"),
                    "wvtr": barrier_data.get("wvtr"),
                    "wvtr_unit": barrier_data.get("wvtr_unit", "g/m2/24h"),
                    "gas_permeability": barrier_data.get("gas_permeability"),
                    "test_condition": barrier_data.get("test_condition"),
                    "data_status": barrier_data.get("data_status", "Data unavailable in source database"),
                    "label": barrier_data.get("label", "DATABASE VALUE")
                },
                "mechanical_properties": {
                    "tensile_strength": mechanical_props.get("tensile_strength"),
                    "burst_index": mechanical_props.get("burst_index"),
                    "thickness_spec": mechanical_props.get("thickness_spec"),
                    "data_status": mechanical_props.get("data_status", "Data unavailable in source database"),
                    "label": mechanical_props.get("label", "DATABASE VALUE")
                },
                "sealability": sealability_val,
                "thickness_recommendation": thickness_rec,
                "sustainability": {
                    "recyclable": sust_data.get("recyclable", cpcb_recyclability.get("recyclable", "Data unavailable")),
                    "compostable": sust_data.get("compostable", "Data unavailable"),
                    "biodegradable": sust_data.get("biodegradable", "Data unavailable"),
                    "epr_category": cpcb_recyclability.get("epr_category", "Standard"),
                    "advantages": sust_data.get("advantages"),
                    "concerns": sust_data.get("concerns"),
                    "label": "DATABASE VALUE"
                },
                "compatibility_status": "Compatible (FSSAI Schedule IV suggestive candidate)",
                "map_suitability": map_suitable,
                "technical_data_coverage": coverage_score["rating"],
                "technical_coverage_pct": coverage_score["pct"],
                "reason_considered": f"Officially prescribed by {source_doc} (p.{page_num}) for {food_cat}: {original_reason}"
            }
            candidates.append(candidate)

        # Deduplicate candidates by material + type
        unique_candidates = []
        seen = set()
        for c in candidates:
            key = (c["material"].strip().lower(), c["packaging_type"].strip().lower())
            if key not in seen:
                seen.add(key)
                unique_candidates.append(c)

        return unique_candidates

    def _lookup_barrier(self, material_name: str) -> Dict[str, Any]:
        """
        Looks up barrier properties in 08_barrier_properties_dataset.csv first (DATABASE VALUE).
        If unavailable, falls back to 16_material_barrier_mechanical_reference.csv
        labeled as 'REFERENCE VALUE (published literature)'.
        """
        # 1. Authoritative Dataset 08 Lookup
        df = data_service.barrier_props_df
        if not df.empty:
            for _, r in df.iterrows():
                m = str(r.get("material_name", ""))
                if any(term in material_name.lower() for term in ["cellulose", "cellophane"]) and "cellulose" in m.lower():
                    raw_otr = r.get("oxygen_transmission_rate")
                    raw_wvtr = r.get("water_vapour_transmission_rate")
                    return {
                        "wvtr": None if pd.isna(raw_wvtr) else float(raw_wvtr),
                        "wvtr_unit": str(r.get("wvtr_unit", "g/m2/24h")),
                        "otr": None if pd.isna(raw_otr) else float(raw_otr),
                        "otr_unit": str(r.get("otr_unit", "cc/m2/day")),
                        "gas_permeability": "Not separately measured in standard (see literature reference for typical CO2TR)",
                        "test_condition": f"Temperature: {r.get('test_temperature', 38)}°C, RH: {r.get('test_relative_humidity', 90)}%",
                        "data_status": "Measured in DB (IS 5012:1987)",
                        "label": "DATABASE VALUE"
                    }

        # 2. Literature Reference Fallback (16_material_barrier_mechanical_reference.csv)
        ref = self._match_reference_row(material_name)
        if ref is not None:
            otr_val = None
            try:
                o_hi = ref.get("otr_high")
                o_lo = ref.get("otr_low")
                if pd.notna(o_hi) and str(o_hi).strip() != "":
                    otr_val = float(o_hi)
                elif pd.notna(o_lo) and str(o_lo).strip() != "":
                    otr_val = float(o_lo)
            except (ValueError, TypeError):
                otr_val = None

            wvtr_val = None
            try:
                w_hi = ref.get("wvtr_high")
                w_lo = ref.get("wvtr_low")
                if pd.notna(w_hi) and str(w_hi).strip() != "":
                    wvtr_val = float(w_hi)
                elif pd.notna(w_lo) and str(w_lo).strip() != "":
                    wvtr_val = float(w_lo)
            except (ValueError, TypeError):
                wvtr_val = None

            co2_note = str(ref.get("co2tr_note", "Data unavailable")) if pd.notna(ref.get("co2tr_note")) else "Data unavailable"
            otr_cond = str(ref.get("otr_test_condition", "ASTM D3985 (23°C, 0% RH)")) if pd.notna(ref.get("otr_test_condition")) else "ASTM D3985"
            wvtr_cond = str(ref.get("wvtr_test_condition", "ASTM F1249 (38°C, 90% RH)")) if pd.notna(ref.get("wvtr_test_condition")) else "ASTM F1249"

            return {
                "otr": otr_val,
                "otr_unit": str(ref.get("otr_unit", "cc/m2/day")),
                "wvtr": wvtr_val,
                "wvtr_unit": str(ref.get("wvtr_unit", "g/m2/24h")),
                "gas_permeability": co2_note,
                "test_condition": f"OTR: {otr_cond} | WVTR: {wvtr_cond}",
                "data_status": f"Published literature reference ({ref.get('source_citation', 'Robertson / Selke')})",
                "label": "REFERENCE VALUE (published literature)",
                "_ref_row": ref.to_dict()
            }

        return {
            "otr": None,
            "otr_unit": "cc/m2/day",
            "wvtr": None,
            "wvtr_unit": "g/m2/24h",
            "gas_permeability": None,
            "test_condition": None,
            "data_status": "Data unavailable in source database",
            "label": "DATABASE VALUE"
        }

    def _lookup_properties(self, material_name: str) -> Dict[str, Any]:
        """
        Looks up mechanical properties in 07_packaging_properties_dataset.csv first (DATABASE VALUE).
        If unavailable, falls back to 16_material_barrier_mechanical_reference.csv (REFERENCE VALUE).
        """
        df = data_service.packaging_props_df
        results = {}
        if not df.empty:
            mat_lower = material_name.lower()
            matched = df[df['material_name'].astype(str).str.lower().apply(lambda x: any(k in mat_lower for k in x.split()[:2]))]
            for _, r in matched.iterrows():
                p_name = str(r.get("property_name", "")).lower()
                val = str(r.get("property_value", ""))
                unit = str(r.get("unit", ""))
                if "tensile" in p_name:
                    results["tensile_strength"] = f"{val} {unit}".strip()
                elif "burst" in p_name:
                    results["burst_index"] = f"{val} {unit}".strip()
                elif "thickness" in p_name or "substance" in p_name:
                    results["thickness_spec"] = f"{val} {unit}".strip()

        if results and (results.get("tensile_strength") or results.get("burst_index")):
            results["data_status"] = "BIS Standard specifications available"
            results["label"] = "DATABASE VALUE"
            return results

        # Fallback to literature reference
        ref = self._match_reference_row(material_name)
        if ref is not None:
            t_lo = ref.get("tensile_strength_low_MPa")
            t_hi = ref.get("tensile_strength_high_MPa")
            tensile_str = None
            if pd.notna(t_lo) and pd.notna(t_hi) and str(t_lo) != "nan":
                tensile_str = f"{t_lo} - {t_hi} MPa"
            elif pd.notna(t_lo) and str(t_lo) != "nan":
                tensile_str = f"{t_lo} MPa"

            ref_gauge = ref.get("reference_thickness_micron")
            if pd.notna(ref_gauge) and str(ref_gauge).strip() != "":
                if any(c.isdigit() for c in str(ref_gauge)) and not any(k in str(ref_gauge).lower() for k in ["standard", "gauge", "n/a"]):
                    thick_str = f"{ref_gauge} µm (reference baseline)"
                else:
                    thick_str = str(ref_gauge)
            else:
                thick_str = None
            mech_note = str(ref.get("mechanical_note", "")) if pd.notna(ref.get("mechanical_note")) else None

            return {
                "tensile_strength": tensile_str,
                "burst_index": None,
                "thickness_spec": thick_str,
                "mechanical_note": mech_note,
                "data_status": f"Published literature reference ({ref.get('source_citation', 'Robertson / Selke')})",
                "label": "REFERENCE VALUE (published literature)"
            }

        return {
            "tensile_strength": None,
            "burst_index": None,
            "thickness_spec": None,
            "data_status": "Data unavailable in source database",
            "label": "DATABASE VALUE"
        }

    def _lookup_sealability(self, material_name: str, pkg_type: str) -> str:
        """
        Sources sealability from material_reference_df (rating + temperature),
        or closure type (lug cap / double seam) for rigid containers (step i).
        """
        m = material_name.lower()
        p = pkg_type.lower()

        # Rigid container closure types
        if any(k in m or k in p for k in ["glass", "bottle", "jar"]):
            return "Lug cap / Crown closure with plastisol liner (rigid container closure)"
        if any(k in m or k in p for k in ["tin", "tinplate", "can", "steel", "tfs"]):
            return "Double seam with compound lining (rigid container closure)"

        # Check reference dataset
        ref = self._match_reference_row(material_name)
        if ref is not None:
            rating = str(ref.get("sealability_rating", "")).strip()
            temp = str(ref.get("heat_seal_temp_C", "")).strip()
            
            if rating and rating.lower() != "nan" and "n/a" not in rating.lower():
                if temp and temp.lower() != "nan" and "n/a" not in temp.lower() and not temp.startswith("Requires"):
                    # Check if temp has numeric temperature range
                    if any(c.isdigit() for c in temp) and not any(k in temp.lower() for k in ["not heat-seal", "needs", "closure"]):
                        return f"{rating} ({temp}°C)"
                    return f"{rating} ({temp})"
                return rating
            if "n/a" in rating.lower() and any(k in m for k in ["rigid", "tin", "glass"]):
                return "Mechanical seam / Lug cap closure"

        return "Standard heat-sealable flexible structure"

    def _lookup_sustainability(self, material_name: str) -> Dict[str, Any]:
        df = data_service.sustainability_df
        if df.empty:
            return {}

        mat_lower = material_name.lower()
        for _, r in df.iterrows():
            m_name = str(r.get("material_name", "")).lower()
            if any(k in mat_lower for k in m_name.split()[:2]):
                return {
                    "recyclable": str(r.get("recyclable", "Unknown")),
                    "compostable": str(r.get("compostable", "Unknown")),
                    "biodegradable": str(r.get("biodegradable", "Unknown")),
                    "advantages": str(r.get("environmental_advantages", "")) if not pd.isna(r.get("environmental_advantages")) else None,
                    "concerns": str(r.get("environmental_concerns", "")) if not pd.isna(r.get("environmental_concerns")) else None
                }
        return {}

    def _lookup_recyclability(self, material_name: str) -> Dict[str, Any]:
        df = data_service.recyclability_df
        if df.empty:
            return {}

        mat_lower = material_name.lower()
        for _, r in df.iterrows():
            cat = str(r.get("category_name", "")).lower()
            poly = str(r.get("plastic_types", "")).lower()
            if any(p in mat_lower for p in ["pet", "hdpe", "pp", "ldpe"]):
                if any(p in poly for p in ["pet", "hdpe", "pp", "ldpe"]):
                    return {
                        "recyclable": "Yes (EPR Regulated)",
                        "epr_category": str(r.get("category_name", "Rigid / Flexible"))
                    }
        return {"recyclable": "Data unavailable", "epr_category": "Standard"}

    def _compute_coverage(self, barrier: Dict, mech: Dict, sust: Dict) -> Dict[str, Any]:
        """Calculates transparent technical data coverage without presenting it as model confidence."""
        points = 0
        total = 5

        # Has barrier
        if barrier.get("wvtr") is not None or barrier.get("otr") is not None:
            points += 1
        # Has mechanical / physical specs
        if mech:
            points += 1
        # Has sustainability info
        if sust and sust.get("recyclable") != "Data unavailable":
            points += 1
        # Material identified in BIS standard
        points += 1
        # Regulatory endorsement
        points += 1

        pct = int((points / total) * 100)
        if pct >= 80:
            rating = "High technical-data coverage"
        elif pct >= 50:
            rating = "Medium technical-data coverage"
        else:
            rating = "Low technical-data coverage"

        return {"pct": pct, "rating": rating}

candidate_generator = CandidateGenerator()
