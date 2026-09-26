from typing import Tuple, Dict, Any, List
import os
import json
import logging
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, mean_absolute_error, root_mean_squared_error, r2_score
)
from app.ml.preprocessing import feature_pipeline
from app.services.data_service import data_service

logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)
        self.model_path = os.path.join(self.model_dir, "packaging_suitability_model.pkl")
        self.metrics_path = os.path.join(self.model_dir, "model_metrics.json")

    def generate_prototype_training_data(self) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
        """
        Synthesizes a representative training set from real FSSAI Schedule IV mappings (14_recommended_packaging.csv)
        and real ICMR food nutritional data (01_food_dataset.csv).
        
        CRITICAL SECTION 12 NOTICE:
        Prototype target is generated from domain rule-based barrier/compatibility scoring.
        It is NOT an experimentally measured ground-truth label.
        """
        foods = data_service.foods_df
        recs = data_service.recommended_df

        rows = []
        labels_reg = []
        labels_clf = []

        if recs.empty:
            # Fallback if datasets aren't loaded
            return pd.DataFrame(), pd.Series(), pd.Series()

        # Build feature pairs
        for f_idx, frow in foods.head(60).iterrows():
            moisture = float(frow.get("moisture_content", 20.0) or 20.0)
            fat = float(frow.get("fat_content", 5.0) or 5.0)
            f_cat = str(frow.get("food_category", "Cereals and cereal products"))

            # Derive synthetic shelf life and storage conditions
            for days in [14, 60, 180, 365]:
                for temp in [4.0, 25.0, 35.0]:
                    req_o2 = 0.8 if (fat > 15.0 or days > 180) else 0.4
                    req_h2o = 0.85 if (moisture < 10.0 or days > 90) else 0.4
                    req_mech = 0.7 if days > 90 else 0.3
                    req_seal = 0.85 if days > 60 else 0.4

                    u_input = {
                        "moisture_level": moisture,
                        "fat_oil_sensitivity": "High" if fat > 15 else "Medium",
                        "ph": 6.0,
                        "desired_shelf_life_days": days,
                        "storage_temperature_c": temp,
                        "relative_humidity_pct": 65.0
                    }

                    c_reqs = {
                        "oxygen_requirement": {"score": req_o2},
                        "moisture_requirement": {"score": req_h2o},
                        "mechanical_requirement": {"score": req_mech},
                        "sealability_requirement": {"score": req_seal}
                    }

                    # Sample 5 candidate packaging materials
                    for r_idx, rrow in recs.head(10).iterrows():
                        mat = str(rrow.get("recommended_packaging_material", "PP"))
                        pkg_type = str(rrow.get("recommended_packaging_type", "Pouch"))
                        cand = {
                            "material": mat,
                            "packaging_type": pkg_type,
                            "barrier_properties": {"wvtr": None, "otr": None},
                            "sustainability": {"recyclable": "Yes" if "glass" in mat.lower() or "pet" in mat.lower() else "No"}
                        }

                        feats = feature_pipeline.extract_features(u_input, c_reqs, cand)
                        
                        # Rule-based synthetic target calculation
                        # Long shelf life + high fat needs laminate or glass/metal
                        score = 0.5
                        is_high_barrier = ("laminate" in mat.lower() or "glass" in mat.lower() or "tin" in mat.lower() or "retort" in mat.lower())
                        if days > 180:
                            score = 0.85 if is_high_barrier else 0.35
                        elif days < 30:
                            score = 0.80 if ("paper" in mat.lower() or "pp" in mat.lower() or "pe" in mat.lower()) else 0.65
                        
                        # Adjust for moisture requirement
                        if moisture < 10.0 and not is_high_barrier and "paper" in mat.lower():
                            score = max(0.2, score - 0.3)
                        
                        # Add slight noise to avoid artificial perfection
                        noisy_score = min(1.0, max(0.1, score + np.random.normal(0, 0.04)))
                        binary_label = 1 if noisy_score >= 0.65 else 0

                        rows.append(feats)
                        labels_reg.append(noisy_score)
                        labels_clf.append(binary_label)

        X = pd.DataFrame(rows, columns=feature_pipeline.feature_names)
        y_reg = pd.Series(labels_reg)
        y_clf = pd.Series(labels_clf)
        return X, y_reg, y_clf

    def train_model(self) -> Dict[str, Any]:
        """Trains both regressor and classifier metrics on proper train/test split."""
        logger.info("Generating prototype training dataset...")
        X, y_reg, y_clf = self.generate_prototype_training_data()

        if X.empty or len(X) < 20:
            return {"status": "ERROR", "message": "Insufficient data to train"}

        X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = train_test_split(
            X, y_reg, y_clf, test_size=0.25, random_state=42
        )

        # Train Random Forest Regressor for continuous suitability score
        rf_reg = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
        rf_reg.fit(X_train, y_reg_train)
        y_reg_pred = rf_reg.predict(X_test)

        mae = float(mean_absolute_error(y_reg_test, y_reg_pred))
        rmse = float(root_mean_squared_error(y_reg_test, y_reg_pred))
        r2 = float(r2_score(y_reg_test, y_reg_pred))

        # Train Random Forest Classifier for discrete suitability
        rf_clf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
        rf_clf.fit(X_train, y_clf_train)
        y_clf_pred = rf_clf.predict(X_test)

        acc = float(accuracy_score(y_clf_test, y_clf_pred))
        prec = float(precision_score(y_clf_test, y_clf_pred, zero_division=0))
        rec = float(recall_score(y_clf_test, y_clf_pred, zero_division=0))
        f1 = float(f1_score(y_clf_test, y_clf_pred, zero_division=0))
        cm = confusion_matrix(y_clf_test, y_clf_pred).tolist()

        # Feature importances
        importances = {}
        for fname, imp in zip(feature_pipeline.feature_names, rf_reg.feature_importances_):
            importances[fname] = round(float(imp), 4)

        metrics = {
            "model_type": "RandomForestRegressor & Classifier",
            "model_status": "TRAINED",
            "dataset_rows": len(X),
            "train_rows": len(X_train),
            "test_rows": len(X_test),
            "target_notice": "Prototype target generated from rule-based domain scoring; not an experimentally measured ground-truth label.",
            "metrics": {
                "regression": {
                    "mae": round(mae, 4),
                    "rmse": round(rmse, 4),
                    "r2": round(r2, 4)
                },
                "classification": {
                    "accuracy": round(acc, 4),
                    "precision": round(prec, 4),
                    "recall": round(rec, 4),
                    "f1": round(f1, 4),
                    "confusion_matrix": cm
                }
            },
            "feature_importance": importances
        }

        # Save model and metrics
        joblib.dump({"regressor": rf_reg, "classifier": rf_clf, "feature_names": feature_pipeline.feature_names}, self.model_path)
        with open(self.metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)

        logger.info(f"Model successfully trained. Accuracy: {acc:.4f}, MAE: {mae:.4f}")
        return metrics

model_trainer = ModelTrainer()
