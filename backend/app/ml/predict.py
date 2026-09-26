from typing import Dict, Any, List
import pandas as pd
from app.ml.preprocessing import feature_pipeline
from app.ml.model_loader import model_loader

class Predictor:
    def __init__(self):
        pass

    def predict_candidate(self, user_input: Dict[str, Any], reqs: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs ML model inference on the candidate packaging option.
        Labels the score clearly as 'ML PREDICTION' and clarifies it is a prototype suitability score,
        not a laboratory-measured probability.
        """
        bundle = model_loader.get_bundle()
        raw_feats = feature_pipeline.extract_features(user_input, reqs, candidate)
        
        if bundle is None:
            # Fallback baseline score if model has not been trained yet
            return {
                "predicted_score": 0.70,
                "label": "ML PREDICTION (Fallback Untrained)",
                "confidence_notice": "Model bundle not yet loaded; using rule-based baseline."
            }

        regressor = bundle.get("regressor")
        feat_names = bundle.get("feature_names", feature_pipeline.feature_names)
        
        X = pd.DataFrame([raw_feats], columns=feat_names)
        pred_val = float(regressor.predict(X)[0])
        # Bound between 0.05 and 0.98
        score = min(0.98, max(0.05, pred_val))

        return {
            "predicted_score": round(score, 4),
            "label": "ML PREDICTION",
            "confidence_notice": "Predicted suitability score from trained Random Forest prototype; not an experimental probability."
        }

predictor = Predictor()
