# SCIENTIFIC LIMITATIONS & TRANSPARENCY NOTICE

## SIH Problem Statement 26236: Smart Food-Packaging Recommendation System

This document outlines the scientific boundaries, data availability limitations, and algorithmic assumptions of the SmartPack prototype system.

---

### 1. Decision-Support Prototype, Not Laboratory Validation
SmartPack is an algorithmic **scientific decision-support tool** intended to assist packaging engineers and food processors in screening technically suitable materials.
- It does **not** replace analytical laboratory migration testing (e.g. IS 9845 overall migration tests).
- It does **not** substitute for commercial microbiological challenge tests, shelf-life verification studies, or structural drop/compression testing under ASTM/IS methods.

---

### 2. Physical & Barrier Property Gaps in Supplied Data
- **Oxygen Transmission Rate (OTR):** The supplied project datasets (`Claude-DataSet/`) do not contain broad experimental OTR measurements across flexible plastic barrier films. In strict compliance with Prompt Rule #1 and #36, **no OTR numbers have been fabricated or hallucinated**. When unmeasured in the primary dataset, the system displays `"Data unavailable in source database"`.
- **Water Vapor Transmission Rate (WVTR):** Only coated regenerated cellulose film (`08_barrier_properties_dataset.csv`, IS 5012:1987) has real laboratory WVTR figures (15 and 30 g/m²/24h). Polymeric WVTR for commodity plastics is not measured in the supplied extract and is reported transparently as unavailable.

---

### 3. Shelf-Life Estimation vs. Empirical Reality
- **User Requested Shelf-Life:** Represents the commercial target entered by the user (e.g., 180 days).
- **Packaging Shelf-Life Protection:** Represents the candidate's barrier capability relative to product vulnerability.
- **Limitation:** Exact empirical shelf life depends on initial microbial load, food water activity (aw), head-space volume, seal integrity, barrier pinholing during transit, and storage temperature abuse. The system clearly notes:
  > *"Exact product shelf life requires empirical real-time or accelerated shelf-life testing with the actual food formulation."*

---

### 4. ML Model Target Limitation (Prompt Section 12)
- The ML model is trained on a **transparent prototype target (`suitability_label`)** constructed from multi-factor requirement satisfaction rules and FSSAI Schedule IV recommendations.
- It is **not** an experimentally measured ground-truth target.
- Output scores (e.g., 82/100) are **derived suitability scores**, NOT empirical statistical probabilities.

---

### 5. Regulatory & Environmental Dynamics
- Prohibitions (e.g. banning recycled plastics in direct food contact under IS 14534, prohibition of newspaper wrapping under FSSAI Reg 4(4)) reflect statutory Indian standards.
- Future statutory amendments by FSSAI, MoEFCC, or CPCB may update EPR categories or allowable recycled contents.
