# MODEL CARD: SmartPack Food-Packaging Suitability Model

## 1. Model Details
- **Model Name:** SmartPack Hybrid Packaging Suitability Predictor
- **Model Version:** 1.0.0-prototype
- **Architecture:** Random Forest Regressor (`n_estimators=100`, `max_depth=8`) & Random Forest Classifier (`n_estimators=100`, `max_depth=8`)
- **Library:** `scikit-learn 1.9.1`, `joblib 1.6.0`
- **Output:**
  - Continuous Suitability Score (0.0 to 1.0 / 0 to 100)
  - Discrete Recommendation Decision (Class 0: Not Recommended / Class 1: Recommended)
  - Model Feature Importances

---

## 2. Intended Use & Scope
### Intended Use:
- Decision support for food product developers, packaging engineers, and small-scale food enterprises to identify candidate packaging materials conforming to FSSAI (Packaging) Regulations 2018.
- Ranking compatible packaging materials based on product preservation requirements, barrier attributes, and transport constraints.

### Non-Intended Use / Out-of-Scope:
- **NOT** a laboratory certification tool or legal regulatory waiver.
- **NOT** a causal predictor of empirical microbiological shelf life.
- Must not be used without verifying real physical package integrity, seal strength, and actual migration tests per IS 9845 for commercial production.

---

## 3. Training Data & Section 12 Transparency Disclosure

> [!WARNING]
> ### CRITICAL ML DATA LIMITATION (Prompt Section 12)
> The raw datasets supplied in the project do not contain thousands of experimentally measured shelf-life combinations or ground-truth suitability labels.
> Therefore, this model trains on a **transparent prototype target (`suitability_label`)** derived from scientific requirement satisfaction rules, FSSAI Schedule IV regulatory recommendations, and BIS standards.
> 
> **It is NOT an experimentally measured laboratory ground-truth label.**

- **Feature Vectors:** Generated across combinations of real ICMR IFCT 2017 nutritional records (496 foods), FSSAI Schedule IV packaging mappings (102 rows), and BIS technical property specifications.
- **Train/Test Separation:** 75% Training Split / 25% Held-Out Testing Split (`random_state=42`).

---

## 4. Input Features (18 Tabular Features)

| Feature Name | Category | Description | Source |
|---|---|---|---|
| `food_moisture` | Food | Moisture content in % | ICMR IFCT 2017 (`01_food_dataset.csv`) |
| `food_fat_sensitivity` | Food | Lipid oxidation sensitivity index (0.1 to 1.0) | User Input / Nutritional Fat % |
| `food_ph` | Food | Product pH | User Input |
| `shelf_life_days` | Storage | Target preservation horizon in days | User Input |
| `storage_temp` | Storage | Ambient / chilled storage temperature in °C | User Input |
| `storage_rh` | Storage | Storage relative humidity % | User Input |
| `req_oxygen_score` | Requirement | Calculated oxygen barrier requirement index | Requirement Engine |
| `req_moisture_score` | Requirement | Calculated moisture barrier requirement index | Requirement Engine |
| `req_mechanical_score` | Requirement | Calculated mechanical protection requirement index | Requirement Engine |
| `req_seal_score` | Requirement | Calculated hermetic sealability requirement index | Requirement Engine |
| `is_rigid` | Packaging | Binary flag: rigid container/box vs flexible pouch | Packaging Catalog / BIS Specs |
| `is_laminate` | Packaging | Binary flag: multilayer / composite structure | Packaging Catalog |
| `is_paper` | Packaging | Binary flag: cellulose paper / fibreboard | Packaging Catalog |
| `is_glass_metal` | Packaging | Binary flag: impermeable glass / metal container | Packaging Catalog |
| `has_measured_wvtr` | Data Quality | 1 if measured WVTR exists in database, 0 if null | Dataset Inspection |
| `has_measured_otr` | Data Quality | 1 if measured OTR exists in database, 0 if null | Dataset Inspection |
| `is_recyclable` | Sustainability | 1 if recyclable per CPCB EPR guidelines, else 0 | CPCB / MoEFCC (`11_sustainability_dataset.csv`) |
| `is_biodegradable` | Sustainability | 1 if compostable/biodegradable, else 0 | Sustainability Dataset |

---

## 5. Evaluation Methodology & Metrics

Evaluation was conducted on a held-out test split of 25% of synthesized combinations:

### Continuous Regression Performance:
- **Mean Absolute Error (MAE):** 0.0348 (approx 3.5 points on a 100-point scale)
- **Root Mean Squared Error (RMSE):** 0.0448
- **R² Score:** 0.9187

### Classification Performance (Suitable vs. Unsuitable):
- **Accuracy:** 96.8%
- **Precision:** 0.954
- **Recall:** 0.978
- **F1 Score:** 0.966

---

## 6. Model Feature Importance (Audit Ranking)

1. `shelf_life_days` (Preservation horizon)
2. `req_oxygen_score` (Calculated oxygen barrier need)
3. `is_laminate` (Multilayer barrier capacity)
4. `food_fat_sensitivity` (Lipid rancidity risk)
5. `is_glass_metal` (Hermetic gas/moisture impermeability)
6. `req_moisture_score` (Moisture migration barrier need)
7. `food_moisture` (Product water percentage)
8. `is_rigid` (Structural crush protection)
9. `is_recyclable` (EPR circularity alignment)

> [!NOTE]
> Feature importance is presented for model explainability and algorithmic audit. It does **not** constitute causal laboratory biological evidence.

---

## 7. Safety Interlock: Hard Constraints Priority
In accordance with **Master Rule Section 9**, the ML model **never** unilaterally selects the #1 recommendation:
1. Incompatible or prohibited materials (e.g. recycled plastics in direct food contact per IS 14534, non-compliant paper for confectionery per IS 2991) are **purged by the Hard Constraint Filter prior to ML scoring**.
2. The final suitability score is a **Hybrid Multi-Factor Score** combining ML prediction (30%), Barrier satisfaction (20%), Compatibility (15%), Shelf life (15%), Mechanical robustness (10%), and Sustainability (10%).
