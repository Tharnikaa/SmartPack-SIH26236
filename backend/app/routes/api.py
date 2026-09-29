import os
import json
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import AnalyzeRequest, ScoringWeightsUpdate
from app.services.data_service import data_service
from app.logic.requirement_engine import requirement_engine
from app.logic.candidate_generator import candidate_generator
from app.logic.constraint_filter import constraint_filter
from app.logic.scoring_engine import scoring_engine
from app.logic.explanation_engine import explanation_engine
from app.ml.train import model_trainer
from app.ml.model_loader import model_loader
from app.services.llm_service import llm_service

router = APIRouter(prefix="/api")

@router.post("/explain/gemini")
def explain_with_gemini(payload: Dict[str, Any]):
    recommendation = payload.get("recommendation", {})
    user_input = payload.get("user_input", {})
    requirements = payload.get("requirements", {})
    return llm_service.generate_ai_explanation(recommendation, user_input, requirements)

@router.get("/health")
def get_health():
    return {
        "status": "healthy",
        "service": "SmartPack Recommendation Engine",
        "datasets_loaded": {
            "foods": len(data_service.foods_df),
            "packaging_materials": len(data_service.packaging_mat_df),
            "recommended_mappings": len(data_service.recommended_df),
            "regulatory_rules": len(data_service.regulatory_df)
        }
    }

@router.get("/foods")
def search_foods(q: str = Query(default="", description="Search query")):
    return data_service.search_foods(query=q, limit=25)

@router.get("/categories")
def get_categories():
    return data_service.get_food_categories()

@router.get("/packaging/materials")
def get_packaging_materials():
    return data_service.get_packaging_materials_catalog()

@router.get("/packaging/{material}")
def get_packaging_detail(material: str):
    catalog = data_service.get_packaging_materials_catalog()
    for item in catalog:
        if material.lower() in item["material_name"].lower():
            return item
    raise HTTPException(status_code=404, detail=f"Material '{material}' not found in database catalog")

@router.get("/config/weights")
def get_weights():
    return scoring_engine.weights

@router.put("/config/weights")
def update_weights(weights: ScoringWeightsUpdate):
    w_dict = weights.model_dump()
    success = scoring_engine.save_weights(w_dict)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save weights configuration")
    return {"status": "SUCCESS", "updated_weights": w_dict}

@router.get("/ml/status")
def get_ml_status():
    metrics_path = "models/model_metrics.json"
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "model_status": "NOT_TRAINED",
        "message": "Model has not been trained yet. Trigger /api/ml/train to train prototype."
    }

@router.post("/ml/train")
def train_model():
    metrics = model_trainer.train_model()
    # Invalidate model loader cache to reload fresh bundle
    model_loader._bundle = None
    return metrics

@router.post("/analyze")
def analyze_packaging(request: AnalyzeRequest):
    user_input = request.model_dump()

    # 1. Scientific Requirement Engine
    calculated_reqs = requirement_engine.compute_requirements(user_input)

    # 2. Candidate Generation from FSSAI Schedule IV & BIS properties
    raw_candidates = candidate_generator.generate_candidates(user_input, calculated_reqs)
    total_candidates_generated = len(raw_candidates)

    # 3. Hard Constraint Filtering
    surviving_candidates, rejected_candidates = constraint_filter.apply_filters(
        raw_candidates, user_input, calculated_reqs
    )
    total_candidates_surviving = len(surviving_candidates)

    if not surviving_candidates:
        # If no candidates satisfy hard constraints, provide closest rejected candidates with warnings
        return {
            "requirements": calculated_reqs,
            "candidates_count": {
                "generated": total_candidates_generated,
                "surviving_hard_filter": 0,
                "rejected": len(rejected_candidates)
            },
            "recommendations": [],
            "status": "NO_COMPATIBLE_PACKAGING",
            "message": "No packaging option satisfies all current strict requirements and hard safety constraints.",
            "rejected_candidates": rejected_candidates[:5],
            "debug": {
                "user_input": user_input,
                "rejection_summary": [
                    {"material": r.get("material"), "reasons": r.get("rejection_reasons")}
                    for r in rejected_candidates
                ]
            }
        }

    # 4. Hybrid Scoring & ML Suitability
    scored_candidates = []
    for cand in surviving_candidates:
        scoring_res = scoring_engine.score_candidate(cand, user_input, calculated_reqs)
        scored_candidates.append({
            **cand,
            "scoring": scoring_res
        })

    # Sort descending by final suitability score
    scored_candidates.sort(key=lambda x: x["scoring"]["final_suitability_score"], reverse=True)

    # 5. Explainable Top-3 Recommendation Engine
    recommendations = explanation_engine.build_recommendations(
        scored_candidates, user_input, calculated_reqs
    )

    # Compile Developer & Audit Debug Info
    debug_info = {
        "workflow_steps": [
            "1. User Input Received",
            "2. Food Requirement Engine Estimated Performance",
            "3. Packaging Database Candidate Lookup (FSSAI Schedule IV)",
            "4. Hard Constraint Filter Run (Regulatory + Physical Compatibility)",
            "5. Feature Pipeline & ML Random Forest Suitability Estimation",
            "6. Configurable Hybrid Multi-Factor Scoring Applied",
            "7. Explainability & Scientific Limitation Disclosures Formulated"
        ],
        "candidate_funnel": {
            "initial_generated": total_candidates_generated,
            "after_hard_constraint_filtering": total_candidates_surviving,
            "rejected_count": len(rejected_candidates),
            "final_top_recommendations": len(recommendations)
        },
        "rejected_sample": (
            # Pick candidates with distinct rejection categories to avoid repetitive reasons
            lambda cands: [
                {"material": r.get("material"), "rejection_reasons": r.get("rejection_reasons")}
                for r in (
                    {
                        (r.get("rejection_reasons") or ["Constraint"])[0].split(":")[0]: r
                        for r in cands
                    }.values()
                )
            ][:3] if cands else []
        )(rejected_candidates),
        "applied_weights": scoring_engine.weights
    }

    return {
        "status": "SUCCESS",
        "requirements": calculated_reqs,
        "recommendations": recommendations,
        "all_ranked_candidates_count": len(scored_candidates),
        "rejected_candidates": rejected_candidates,
        "debug": debug_info
    }
