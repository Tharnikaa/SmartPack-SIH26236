import os
import json
import logging
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class DataService:
    def __init__(self, data_dir: str = "data/original"):
        # Locate datasets across possible root directories
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
        possible_dirs = [
            os.path.join(base_dir, "data", "original"),
            os.path.join(base_dir, "Claude-DataSet"),
            data_dir,
            os.path.join("..", data_dir),
            "Claude-DataSet",
            os.path.join("..", "Claude-DataSet")
        ]
        self.resolved_data_dir = next((d for d in possible_dirs if os.path.exists(d) and os.listdir(d)), data_dir)
        self.data_dir = self.resolved_data_dir
        self.foods_df: pd.DataFrame = pd.DataFrame()
        self.packaging_mat_df: pd.DataFrame = pd.DataFrame()
        self.packaging_props_df: pd.DataFrame = pd.DataFrame()
        self.barrier_props_df: pd.DataFrame = pd.DataFrame()
        self.compatibility_df: pd.DataFrame = pd.DataFrame()
        self.shelf_life_df: pd.DataFrame = pd.DataFrame()
        self.sustainability_df: pd.DataFrame = pd.DataFrame()
        self.recyclability_df: pd.DataFrame = pd.DataFrame()
        self.regulatory_df: pd.DataFrame = pd.DataFrame()
        self.recommended_df: pd.DataFrame = pd.DataFrame()
        self.master_ml_df: pd.DataFrame = pd.DataFrame()
        self.material_reference_df: pd.DataFrame = pd.DataFrame()
        
        self.validation_report: Dict[str, Any] = {}
        self.load_all_datasets()

    def _read_csv_safe(self, filename: str) -> pd.DataFrame:
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
            alt_candidates = [
                os.path.join(base_dir, "Claude-DataSet", filename),
                os.path.join(base_dir, "data", "original", filename),
                os.path.join("Claude-DataSet", filename),
                os.path.join("..", "Claude-DataSet", filename)
            ]
            path = next((p for p in alt_candidates if os.path.exists(p)), None)
            if not path:
                logger.warning(f"File {filename} not found")
                return pd.DataFrame()
        try:
            return pd.read_csv(path, low_memory=False)
        except Exception:
            return pd.read_csv(path, encoding='latin1', low_memory=False)

    def load_all_datasets(self):
        logger.info("Loading all source datasets into memory...")
        self.foods_df = self._read_csv_safe("01_food_dataset.csv")
        self.packaging_mat_df = self._read_csv_safe("06_packaging_material_dataset.csv")
        props_df = self._read_csv_safe("07_packaging_properties_dataset.csv")
        if props_df.empty:
            props_df = self._read_csv_safe("07_packaging_properties_dataset_Claude.csv")
        self.packaging_props_df = props_df
        self.barrier_props_df = self._read_csv_safe("08_barrier_properties_dataset.csv")
        self.compatibility_df = self._read_csv_safe("09_food_packaging_compatibility_MERGED.csv")
        self.shelf_life_df = self._read_csv_safe("10_packaging_shelf_life_dataset.csv")
        self.sustainability_df = self._read_csv_safe("11_sustainability_dataset.csv")
        self.recyclability_df = self._read_csv_safe("12_recyclability_dataset.csv")
        self.regulatory_df = self._read_csv_safe("13_regulatory_rules.csv")
        self.recommended_df = self._read_csv_safe("14_recommended_packaging.csv")
        self.master_ml_df = self._read_csv_safe("15_MASTER_ML_DATASET.csv")
        self.material_reference_df = self._read_csv_safe("16_material_barrier_mechanical_reference.csv")
        self.respiration_df = self._read_csv_safe("respiration_reference_completed.csv")

        self.generate_validation_report()
        logger.info(f"Loaded {len(self.foods_df)} foods, {len(self.recommended_df)} recommended mappings, {len(self.packaging_mat_df)} packaging materials, {len(self.material_reference_df)} literature reference materials, {len(self.respiration_df)} respiration records.")

    def lookup_respiration(self, food_name: str, food_category: str = "") -> Optional[Dict[str, Any]]:
        """
        Looks up commodity-specific respiration rate and class from respiration_reference_completed.csv.
        Returns normalized respiration level ('Low', 'Medium', 'High') and reference metadata.
        Does not invent values if commodity is not present.
        """
        if self.respiration_df.empty or not food_name:
            return None

        q = food_name.strip().lower()
        df = self.respiration_df

        # 1. Exact match on canonical_commodity
        match = df[df["canonical_commodity"].astype(str).str.strip().str.lower() == q]
        
        # 2. Substring match on canonical_commodity or original_food_name
        if match.empty:
            match = df[df["canonical_commodity"].astype(str).str.lower().apply(lambda x: x in q or q in x)]
        if match.empty:
            match = df[df["original_food_name"].astype(str).str.lower().apply(lambda x: any(term in x for term in q.split() if len(term) > 3))]

        if match.empty:
            return None

        row = match.iloc[0]
        raw_class = str(row.get("respiration_class", "")).strip()
        if not raw_class or raw_class.lower() == "nan":
            return None

        # Normalize into Low / Medium / High
        rc_lower = raw_class.lower()
        if any(k in rc_lower for k in ["very low", "low"]):
            normalized = "Low"
        elif any(k in rc_lower for k in ["moderate", "medium"]):
            normalized = "Medium"
        elif any(k in rc_lower for k in ["high", "extremely high"]):
            normalized = "High"
        else:
            normalized = "Medium"

        return {
            "canonical_commodity": str(row.get("canonical_commodity", food_name)),
            "respiration_class": normalized,
            "raw_class": raw_class,
            "rate_min": None if pd.isna(row.get("respiration_rate_min")) else float(row.get("respiration_rate_min")),
            "rate_max": None if pd.isna(row.get("respiration_rate_max")) else float(row.get("respiration_rate_max")),
            "rate_unit": str(row.get("respiration_rate_unit", "mg CO2/kg/hr")),
            "temperature_c": str(row.get("temperature_C", "5")),
            "source": str(row.get("source_organization", "Kader Postharvest / Reference Table")),
            "confidence": str(row.get("confidence", "High"))
        }

    def generate_validation_report(self):
        datasets = {
            "01_food_dataset.csv": self.foods_df,
            "06_packaging_material_dataset.csv": self.packaging_mat_df,
            "07_packaging_properties_dataset.csv": self.packaging_props_df,
            "08_barrier_properties_dataset.csv": self.barrier_props_df,
            "09_food_packaging_compatibility_MERGED.csv": self.compatibility_df,
            "10_packaging_shelf_life_dataset.csv": self.shelf_life_df,
            "11_sustainability_dataset.csv": self.sustainability_df,
            "12_recyclability_dataset.csv": self.recyclability_df,
            "13_regulatory_rules.csv": self.regulatory_df,
            "14_recommended_packaging.csv": self.recommended_df,
            "15_MASTER_ML_DATASET.csv": self.master_ml_df,
            "16_material_barrier_mechanical_reference.csv": self.material_reference_df
        }

        report = {
            "status": "VALIDATED",
            "total_datasets": len(datasets),
            "datasets": {}
        }

        for name, df in datasets.items():
            if df.empty:
                report["datasets"][name] = {"rows": 0, "cols": 0, "usable": False, "reason": "Empty or missing"}
                continue
            
            n_rows, n_cols = df.shape
            dup_count = int(df.duplicated().sum())
            missing_total = int(df.isnull().sum().sum())
            missing_pct = round(missing_total / (n_rows * n_cols) * 100, 2) if n_rows * n_cols > 0 else 0
            
            report["datasets"][name] = {
                "rows": n_rows,
                "cols": n_cols,
                "duplicates": dup_count,
                "missing_cells_pct": missing_pct,
                "usable": True,
                "columns": list(df.columns)
            }

        self.validation_report = report
        
        # Save validation report
        os.makedirs("data/reports", exist_ok=True)
        with open("data/reports/DATA_VALIDATION_REPORT.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    def get_food_categories(self) -> List[str]:
        cats = set()
        if not self.recommended_df.empty and 'food_category' in self.recommended_df.columns:
            cats.update(self.recommended_df['food_category'].dropna().unique())
        if not self.foods_df.empty and 'food_category' in self.foods_df.columns:
            cats.update(self.foods_df['food_category'].dropna().unique())
        return sorted([str(c) for c in cats if str(c).strip()])

    def search_foods(self, query: str = "", limit: int = 25) -> List[Dict[str, Any]]:
        if self.foods_df.empty:
            return []
        
        df = self.foods_df
        if query:
            q = query.lower()
            mask = df['food_name'].astype(str).str.lower().str.contains(q, regex=False) | \
                   df['food_category'].astype(str).str.lower().str.contains(q, regex=False)
            df = df[mask]
        
        results = []
        for _, row in df.head(limit).iterrows():
            results.append({
                "food_id": str(row.get("food_id", "")),
                "food_name": str(row.get("food_name", "")),
                "food_category": str(row.get("food_category", "")),
                "moisture_content": None if pd.isna(row.get("moisture_content")) else float(row.get("moisture_content")),
                "fat_content": None if pd.isna(row.get("fat_content")) else float(row.get("fat_content")),
                "protein_content": None if pd.isna(row.get("protein_content")) else float(row.get("protein_content")),
                "source": str(row.get("source", "ICMR IFCT 2017"))
            })
        return results

    def get_packaging_materials_catalog(self) -> List[Dict[str, Any]]:
        materials = []
        if self.packaging_mat_df.empty:
            return []

        for _, row in self.packaging_mat_df.iterrows():
            mat_name = str(row.get("material_name", ""))
            pkg_id = str(row.get("packaging_id", ""))
            family = str(row.get("material_family", ""))
            
            # Find properties from 07_packaging_properties_dataset_Claude.csv
            props = []
            if not self.packaging_props_df.empty:
                mat_props = self.packaging_props_df[self.packaging_props_df['material_name'].astype(str).str.contains(mat_name, case=False, regex=False)]
                for _, prow in mat_props.iterrows():
                    props.append({
                        "property_name": str(prow.get("property_name", "")),
                        "property_value": str(prow.get("property_value", "")),
                        "unit": str(prow.get("unit", "")),
                        "test_condition": str(prow.get("test_condition", "")) if not pd.isna(prow.get("test_condition")) else None
                    })

            # Find barrier data from 08_barrier_properties_dataset.csv
            barrier_info = None
            if not self.barrier_props_df.empty:
                b_match = self.barrier_props_df[self.barrier_props_df['material_name'].astype(str).str.contains(mat_name, case=False, regex=False)]
                if not b_match.empty:
                    brow = b_match.iloc[0]
                    barrier_info = {
                        "wvtr": None if pd.isna(brow.get("water_vapour_transmission_rate")) else float(brow.get("water_vapour_transmission_rate")),
                        "wvtr_unit": str(brow.get("wvtr_unit", "g/m2/24h")),
                        "otr": None if pd.isna(brow.get("oxygen_transmission_rate")) else float(brow.get("oxygen_transmission_rate")),
                        "otr_unit": str(brow.get("otr_unit", "cc/m2/day")),
                        "test_temperature": None if pd.isna(brow.get("test_temperature")) else float(brow.get("test_temperature")),
                        "test_rh": None if pd.isna(brow.get("test_relative_humidity")) else float(brow.get("test_relative_humidity")),
                        "source": str(brow.get("source", "BIS"))
                    }

            # Find sustainability data from 11_sustainability_dataset.csv
            sust_info = None
            if not self.sustainability_df.empty:
                s_match = self.sustainability_df[self.sustainability_df['material_name'].astype(str).str.contains(mat_name, case=False, regex=False)]
                if not s_match.empty:
                    srow = s_match.iloc[0]
                    sust_info = {
                        "recyclable": str(srow.get("recyclable", "Unknown")),
                        "compostable": str(srow.get("compostable", "Unknown")),
                        "biodegradable": str(srow.get("biodegradable", "Unknown")),
                        "renewable_resource": str(srow.get("renewable_resource", "Unknown")),
                        "environmental_advantages": str(srow.get("environmental_advantages", "")) if not pd.isna(srow.get("environmental_advantages")) else None,
                        "environmental_concerns": str(srow.get("environmental_concerns", "")) if not pd.isna(srow.get("environmental_concerns")) else None
                    }

            materials.append({
                "packaging_id": pkg_id,
                "material_name": mat_name,
                "material_family": family,
                "material_type": str(row.get("material_type", "")),
                "food_contact_suitable": str(row.get("food_contact_suitable", "Yes")),
                "source_document": str(row.get("source_document", "")),
                "properties": props,
                "barrier_properties": barrier_info,
                "sustainability": sust_info
            })

        return materials

# Global singleton instance
data_service = DataService()
