import os
import logging
from typing import Dict, Any, Optional
import httpx
from dotenv import load_dotenv

# Load .env file from project root or current working dir
load_dotenv()
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env")))

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()

    def is_configured(self) -> bool:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        return bool(self.api_key and self.api_key != "your_gemini_api_key_here")

    def generate_ai_explanation(
        self, 
        recommendation: Dict[str, Any], 
        user_input: Dict[str, Any], 
        requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Uses Google Gemini to produce an authoritative, natural-language packaging audit narrative.
        STRICT COMPLIANCE RULE: Grounded 100% in supplied pipeline evidence. Never alters rankings or fabricates data.
        """
        if not self.is_configured():
            return {
                "status": "UNCONFIGURED",
                "narrative": None,
                "message": "Gemini API key is not configured. Add GEMINI_API_KEY to .env in the project root to activate dynamic AI explanations."
            }

        prompt = f"""
You are the Chief Food Packaging Scientist for SmartPack (SIH Problem Statement 26236).
Write an authoritative, concise, 2-paragraph scientific justification explaining why this packaging option was selected for this food product.

PRODUCT DETAILS:
- Food Name: {user_input.get('food_name')}
- Food Category: {user_input.get('food_category')}
- Moisture Level: {user_input.get('moisture_level')}%
- Fat/Oil Sensitivity: {user_input.get('fat_oil_sensitivity')}
- Product pH: {user_input.get('ph')}
- Desired Shelf Life: {user_input.get('desired_shelf_life_days')} days
- Storage Temp: {user_input.get('storage_temperature_c')}°C

CALCULATED REQUIREMENTS:
- Oxygen Barrier: {requirements.get('oxygen_requirement', {}).get('level')}
- Moisture Barrier: {requirements.get('moisture_requirement', {}).get('level')}
- Mechanical Protection: {requirements.get('mechanical_requirement', {}).get('level')}

RECOMMENDED OPTION (Rank #{recommendation.get('rank')}):
- Material: {recommendation.get('material')}
- Format: {recommendation.get('packaging_type')} ({recommendation.get('packaging_structure')})
- Derived Suitability Score: {recommendation.get('suitability_score')}/100
- Measured OTR: {recommendation.get('barrier_properties', {}).get('otr') or 'Data unavailable in database'}
- Measured WVTR: {recommendation.get('barrier_properties', {}).get('wvtr') or 'Data unavailable in database'}
- Statutory Endorsement: {recommendation.get('source_citation', {}).get('document')} (Page {recommendation.get('source_citation', {}).get('page')})
- Evidence Points: {', '.join(recommendation.get('evidence_points', []))}

RULES:
1. Explain technical preservation mechanics clearly (lipid oxidation prevention, moisture migration control).
2. Reference the statutory compliance under FSSAI Packaging Regulations 2018 or BIS Standards.
3. Be truthful about data limitations: do NOT invent fake OTR or WVTR numbers if unmeasured.
4. Keep the tone professional, scientific, and concise (under 160 words).
"""

        model_candidates = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.5-flash-lite", "gemini-1.5-flash"]
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 450
            }
        }

        with httpx.Client(timeout=20.0) as client:
            for model_name in model_candidates:
                endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
                try:
                    resp = client.post(endpoint, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                            return {
                                "status": "SUCCESS",
                                "narrative": text.strip(),
                                "model": model_name,
                                "label": "AI EXPLANATION (Ground-Truth Evidence Synthesis)"
                            }
                    elif resp.status_code != 404:
                        logger.warning(f"Gemini API returned {resp.status_code} for {model_name}: {resp.text[:200]}")
                except Exception as e:
                    logger.warning(f"Error calling {model_name}: {e}")

        return {
            "status": "API_ERROR",
            "narrative": None,
            "message": "Gemini API request failed. Please verify your API key permissions."
        }

llm_service = LLMService()
