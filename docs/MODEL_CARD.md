# MODEL CARD: SmartPack Decision & Scoring System

## 1. System Details
- **Architecture:** Transparent Multi-Criteria Engineering Engine (Stage 1 FSSAI Schedule IV Retrieval $\rightarrow$ Stage 2 Fick's-Law Barrier & Thickness Engine $\rightarrow$ Stage 3 Hard Regulatory Constraint Interlock $\rightarrow$ Stage 4 Deterministic Multi-Criteria Scoring $\rightarrow$ Stage 5 Provenance & Evidence Engine)
- **Status:** **ML Suitability Scoring Removed Pending Real Labeled Outcome Data**
- **Legacy Prototype Code:** Retained in `app/ml/` (`train.py`, `predict.py`, `model_loader.py`) for reference and future model development when sufficient real experimental data is available.

---

## 2. Intended Use & Scope
### Intended Use:
- Decision support for food product developers, packaging engineers, and small-scale food enterprises to identify candidate packaging materials conforming to FSSAI (Packaging) Regulations 2018.
- Ranking compatible packaging materials based on product preservation requirements, barrier attributes (Fick's-law thickness solver), and transport constraints.
- Displaying transparent data provenance badges (`DATABASE VALUE`, `REFERENCE VALUE (published literature)`, `CALCULATED REQUIREMENT`, `DERIVED SCORE`).

### Non-Intended Use / Out-of-Scope:
- **NOT** a laboratory certification tool or legal regulatory waiver.
- **NOT** a causal predictor of empirical microbiological shelf life.
- Must not be used without verifying real physical package integrity, seal strength, and actual migration tests per IS 9845 for commercial production.

---

## 3. Scientific Integrity & Data Limitation Disclosure

> [!IMPORTANT]
> ### NOTICE: REMOVAL OF SYNTHETIC ML SUITABILITY MODEL
> An engineering audit revealed that the prototype ML training pipeline (`generate_prototype_training_data()` in `backend/app/ml/train.py`) synthesized 7,200 rows using hardcoded rule-based scoring with artificial Gaussian noise, and reported high regression/classification metrics ($R^2 = 0.9187$, Accuracy = $91.83\%$).
>
> Because these targets were circularly generated from rules rather than experimentally measured laboratory outcomes, reporting high machine-learning performance metrics was scientifically misleading.
>
> **ML suitability scoring has been completely removed from the active scoring pipeline.**
> Scoring is now deterministically computed across five scientific and regulatory criteria based on verified database records (Datasets 01–14) and cited packaging science literature values (`16_material_barrier_mechanical_reference.csv`).

---

## 4. Multi-Criteria Scoring Architecture (Sum = 1.00)

The legacy 0.30 weight allocated to the synthetic ML model was redistributed proportionally across the remaining five criteria (new weight = old weight / 0.70):

| Scoring Criterion | Weight | Data Provenance & Methodology | Source |
|---|---|---|---|
| **Barrier Fit** | **28.57%** | Compares candidate OTR and WVTR against product preservation targets derived via Fick's first law of diffusion. Rigid impermeable containers (glass, tinplate) score 0.98. | Dataset 08 (IS 5012) & Dataset 16 literature references (Robertson / Selke) |
| **Compatibility & Safety** | **21.43%** | Evaluates chemical compatibility, non-reactivity, and adherence to FSSAI (Packaging) Regulations 2018 Schedule IV. | Datasets 09, 13, 14 |
| **Shelf-Life Protection** | **21.43%** | Compares benchmark database shelf life against requested user horizon. | Datasets 05, 10 |
| **Mechanical Protection** | **14.29%** | Evaluates tensile strength (MPa), burst index, reference gauge, and structural rigidity against transport rigor. | Dataset 07 (BIS specs) & Dataset 16 (typical ranges) |
| **Sustainability & Circularity** | **14.28%** | Scored via CPCB Extended Producer Responsibility (EPR) categorisation and biodegradability/compostability status. | Datasets 11, 12 |

---

## 5. Fick's-Law Packaging Thickness Solver
To close the physical property gap without fabricating false data, the system implements a deterministic thickness solver (`backend/app/logic/thickness_engine.py`):
$$\text{Permeability } (P) = \text{TR}_{\text{reference}} \times \text{Thickness}_{\text{reference}}$$
$$\text{Required Thickness} = \frac{P}{\text{Target TR}}$$
- Solved for both OTR and WVTR; the larger thickness governs.
- Rounded up to standard commercial film gauges: **25, 37, 50, 75, 100 $\mu$m**.
- Rigid impermeable materials (glass bottles, tinplate cans) are flagged as **`N/A — rigid, impermeable`**.
- Multilayer/metalized composites are clearly labeled **`estimated (multilayer)`**.

---

## 6. Safety Interlock: Hard Constraints Priority
In accordance with mandatory safety guidelines, candidate scoring is strictly subordinate to hard regulatory constraints:
1. Incompatible or prohibited materials (e.g. recycled plastics in direct food contact per IS 14534, non-compliant paper for confectionery per IS 2991) are **purged by the Hard Constraint Filter prior to scoring**.
2. If all candidates are eliminated, the system displays prominent safety warnings with closest non-compliant alternatives and explicitly cites the violated BIS/FSSAI clause.
