# SIH 26236 — Food Packaging Recommendation Engine
## Data Quality Report & ML Design Notes

---

## A. Files Processed

| # | Filename | Type | Useful? | Datasets contributed |
|---|---|---|---|---|
| 1 | Food Composition Data ICMR.pdf (IFCT 2017, 585p) | Nutrient composition tables | **Yes — core** | 01 |
| 2 | Volume-5 (Fruits and Vegetables Compendium)-AGMARK.pdf | Grading standard | Yes | 02 |
| 3 | Volume-7 (Food grains and allied products Compendium)-AGMARK.pdf | Grading standard | Yes | 02, 04 |
| 4 | Volume-9 (Spices and condiments Compendium)-AGMARK.pdf | Grading standard | Yes (partial — see caveat) | 02 |
| 5 | listofagmarkcommodities.pdf | Reference list | Reference only | — |
| 6 | Compendium_Contaminants_Regulations_28_01_2022-FSSAI.pdf (81p) | Regulatory limits | **Yes — core** | 03 |
| 7 | Contaminants_Regulations-FSSAI.pdf (19p) | Regulatory limits | No (superseded by #6) | — |
| 8 | FSSAI_Packaging_Regulations.pdf | Regulatory + recommendations | **Yes — core** | 13, 14 |
| 9 | Download the official FSSAI Labelling & Display Compendium PDF.pdf | Regulatory | Partial | 13 |
| 10 | BIS_Food_Packaging_Handbook.pdf (418p) | Material standards (IS specs) | Yes | 06, 07, 08, 11, 13 |
| 11 | CPCB Plastic Waste Management SOP.pdf | EPR/recycling rules | Yes | 11, 12, 13 |
| 12 | Download CPCB SOP PDF.pdf | *duplicate of #11* | No (identical, MD5-confirmed) | — |
| 13 | Plastic Waste Management SOP.pdf | *duplicate of #11* | No (identical, MD5-confirmed) | — |
| 14 | MoEFCC_Plastic_Waste_Management_Rules.pdf | Plastic waste rules | Yes | 11, 12, 13 |
| 15 | ManualOfQualityCOntrol.pdf (FCI, 259p) | Grain QC manual | **No — scanned, no text layer** | — |
| 16 | PHM-Value-addtion-AR-2011-12_0-ICAR.pdf (6p) | R&D annual report | **Yes — only real shelf-life source** | 04, 05, 09, 10, 14 |
| 17 | SOP-Standard_Operating_Procedure_1691398899.pdf (2p, FCI) | Circular | No (no extractable data beyond other sources) | — |

**3 files were byte-identical duplicates** (confirmed via MD5 checksum) of the CPCB SOP and were only counted once.

---

## B. Dataset Sizes

| Dataset | Rows | Real/sourced? |
|---|---:|---|
| 01_food_dataset.csv | 496 | Yes — ICMR IFCT 2017 |
| 02_food_quality_dataset.csv | 1,506 | Yes — AGMARK (see column-mapping caveat for spices) |
| 03_contamination_dataset.csv | 1,359 | Yes — FSSAI Compendium |
| 04_storage_dataset.csv | 8 | Yes, but **very thin** |
| 05_shelf_life_dataset.csv | 26 | Yes — all from the single ICAR report |
| 06_packaging_material_dataset.csv | 10 | Yes — BIS Handbook |
| 07_packaging_properties_dataset.csv | 85 | Yes — BIS Handbook (7 IS standards) |
| 08_barrier_properties_dataset.csv | 2 | Yes, but **critically insufficient** |
| 09_food_packaging_compatibility.csv | 5 | Yes, but **critically insufficient** |
| 10_packaging_shelf_life_dataset.csv | 17 | Yes — the core ML-relevant table, but **far too small** |
| 11_sustainability_dataset.csv | 11 | Yes |
| 12_recyclability_dataset.csv | 6 | Yes |
| 13_regulatory_rules.csv | 20 | Yes (representative subset, not exhaustive) |
| 14_recommended_packaging.csv | 102 | Yes — 93 rows from the authoritative FSSAI Schedule IV table |
| 15_MASTER_ML_DATASET.csv | 17 | Derived from Dataset 10 only (see Section E) |

---

## C. Missing / Insufficient Data (be honest)

| Field | Status |
|---|---|
| OTR (oxygen transmission rate) | **Missing entirely.** No source in the ZIP reports OTR for any material. |
| WVTR (water vapour transmission rate) | **Insufficient.** Only 2 values found (Cellulose Film, IS 5012:1987). No plastics data. |
| Food pH / water activity | **Missing entirely** for all 496 foods — IFCT 2017 does not report these in the extracted table. |
| Food-packaging compatibility | **Critically insufficient** — 5 source-backed rows only. |
| Packaging→shelf-life relationships | **Insufficient for ML** — 17 rows, all from one 6-page ICAR annual-report summary, not a dedicated shelf-life study. |
| Storage temperature/RH by food | **Insufficient** — only 8 rows, mostly inferred from the same ICAR report. |
| Packaging material cost | Not collected (explicitly out of scope per your brief). |
| AGMARK spice-table column identity | Ambiguous — see caveat below. |
| FCI grain manual (259p) | **Not extracted** — scanned, no OCR text layer; spot-OCR did not yield usable tables within reasonable effort. |

### Known extraction-quality caveats (please QA before production use)
1. **AGMARK Volume-9 (spices) grade columns** in `02_food_quality_dataset.csv` were labeled using the same generic column template as Volume-7 (pulses) — i.e., `Moisture`, `Foreign_matter_organic`, etc. — but spice grade tables often use different columns (volatile oil %, extraneous matter, ash, etc.). **The parameter names for Volume-9 rows should be treated as positional placeholders, not verified column identities**, until manually checked against the source pages.
2. **FSSAI Contaminants Compendium** (metals + pesticide tables) was parsed with a line-based regex across a two-column PDF layout. A small number of rows have merged or truncated food-item descriptions where a food name wrapped across the original two-column layout. The contaminant name, food association, and numeric limit are generally reliable; a few food-name strings may be imprecise.
3. **IS 8970:1991 Aluminium Foil Laminate** table in the BIS Handbook was OCR-corrupted in the source scan (character-substitution artifacts). We **excluded its numeric values entirely** rather than report unreliable numbers — this is a real gap, not an oversight.
4. **ManualOfQualityCOntrol.pdf (FCI, 259 pages)** is a scanned document with no embedded text layer. We rendered and OCR'd the cover page, table of contents, and a sample of pages in the "Specifications" and "Storage and Preservation" chapters; the OCR output was administrative/legal boilerplate, not the grade/storage tables we expected. Fully OCR-ing all 259 pages was outside the scope of this pass — flagging it as a **candidate for a dedicated future extraction effort**, not silently dropping it.

---

## D. Data Conflicts

No direct numeric conflicts were found between authoritative sources on the same fact (e.g., two different FSSAI documents disagreeing on the same pesticide limit) — the two contaminants PDFs were the same regulation family at different vintages, so we used only the more complete/recent one (81-page Compendium) rather than reconciling values.

One **implicit tension** worth flagging: `Contaminants_Regulations-FSSAI.pdf` (19p, older/shorter) and `Compendium_Contaminants_Regulations_28_01_2022-FSSAI.pdf` (81p) are versions of the same FSSAI (Contaminants, Toxins and Residues) Regulations, 2011. We used the newer, more complete version and did not cross-check every value between them — if the shorter file is actually a different amendment with independently valid values, a line-by-line diff would be needed.

| Field | Source A | Source B | Difference | Preferred | Reason |
|---|---|---|---|---|---|
| Contaminant limits | Contaminants_Regulations-FSSAI.pdf (19p) | Compendium...28_01_2022-FSSAI.pdf (81p) | B is more complete/current (dated 27/28 Jan 2022) | B | Later consolidated version explicitly versioned "Version VI" |

---

## E. Target Variable & Model Design — Honest Assessment

### E.1 What the ML model should predict
**Input:** food characteristics + storage/shelf-life requirement + candidate packaging material's properties.
**Output:** a ranked list (top 3) of packaging materials suited to that food.

### E.2 Target variable construction
We did **not** set `recommended = 1` for every packaging material mentioned in a source document — that would conflate "this material exists / was tested" with "this material is the right choice." Instead:

- **Dataset 14** (`14_recommended_packaging.csv`) rows are **positive examples only** — each row is a food-category-to-material pairing an authoritative source (FSSAI Schedule IV regulation, or an ICAR field trial with a measured outcome) explicitly endorses. This is a reasonable *candidate generation* signal but is **not a trained classifier's output** — it has no negative examples (materials NOT recommended for a food) except the 1 explicit "not recommended" case in Dataset 9.
- **Dataset 10** (`10_packaging_shelf_life_dataset.csv`) is the closest thing to a real supervised-learning table (food + packaging + storage condition → measured shelf-life), but it has only **17 rows**, all from a single 6-page ICAR annual-report summary rather than a dedicated shelf-life study.

**Honest conclusion: there is not enough labeled data in the provided ZIP to train a real supervised ML ranking/classification model today.** A conventional model (even a simple gradient-boosted classifier) needs at minimum dozens to hundreds of examples per class with both positive and negative labels; we have single-digit-to-low-double-digit counts for the exact food+packaging+outcome combination that matters, and zero explicit negative examples beyond one row.

### E.3 What IS large enough to build on now
- **Regulatory compliance rule engine** (Datasets 03, 13): 1,359 contamination limits + 20 regulatory rules — large enough to build a hard-constraint filter (reject packaging/food combos that would violate FSSAI/BIS/CPCB/MoEFCC rules).
- **Candidate generation via Schedule IV lookup** (Dataset 14): 93 authoritative food-category → packaging-material mappings from FSSAI's own regulation — usable *directly as a rule-based recommender* (not an ML model) for the 10 broad food categories it covers.
- **Food composition lookup** (Dataset 01): 496 foods, real nutrient data — usable as an input-feature table once a food is matched to one of these records.
- **Packaging property lookup** (Dataset 07): 85 real technical properties across 7 materials — usable as packaging-side features once a candidate shortlist exists.

### E.4 Recommended near-term architecture for the hackathon (given actual data volume)
Given the honest data-sufficiency picture above, we recommend **not** starting with a trained ML ranker. Instead:

1. **Rule-based candidate generation** using Dataset 14 (FSSAI Schedule IV) keyed on food category → gives 1-10 candidate materials per category, already regulator-endorsed.
2. **Hard-constraint filtering** using Dataset 13 (regulatory) + Dataset 03 (contamination) — eliminate any candidate that would violate a labelling/migration/compliance rule.
3. **Scoring/ranking** the surviving candidates using a transparent weighted-score formula (not a trained model) over: sustainability flags (Dataset 11), recyclability/EPR category (Dataset 12), and packaging property fit where available (Dataset 07) — e.g., moisture-sensitive food → prefer material with good moisture-barrier property.
4. **Present this as "ML-assisted rule engine v1"** to the jury, honestly, while continuing to collect the shelf-life/compatibility/barrier data (via targeted lab tests or additional literature) needed for a genuine trained model in a v2.
5. The **LLM (Gemini/OpenAI) only explains** the already-ranked top-3 output from steps 1-3 — consistent with your intended architecture; it never influences the ranking itself.

This is not a downgrade of ambition — it is the technically honest path: presenting 17 rows as if they trained a robust ML ranker would be a fragile (and easily challenged) claim in a jury Q&A.

### E.5 Column roles
| Role | Columns |
|---|---|
| **ML input features** | moisture/protein/fat/fibre content (01), storage temp/RH/atmosphere (04/10), packaging property values (07), material family/sustainability flags (06/11/12) |
| **Candidate target (not yet a trained label)** | `recommended` in Dataset 14/15, `shelf_life` in Dataset 05/10 |
| **Rule-engine fields (never ML features)** | everything in Datasets 03 and 13 — contaminant limits, regulatory permitted/prohibited flags |
| **LLM explanation fields** | `reason`, `compatibility_reason`, `environmental_advantages/concerns`, `notes` columns across all datasets — pass these to the LLM as grounding context, never as model input features |
| **Reference-only** | `source`, `source_document`, `page_number` in every dataset — for traceability/audit, not modeling |

---

## F. Source Traceability
Every row across all 15 CSVs carries `source`, `source_document`, and `page_number` (or equivalent) columns. See `DATA_SOURCE_MAPPING.xlsx` for the file-level summary and `DATA_DICTIONARY.xlsx` for column-level definitions, units, and ML-role tagging.

## G. Bottom line
You have a strong, defensible foundation for **food composition** (496 real records), **regulatory compliance** (1,379 rules/limits), **grading standards** (1,506 rows), and a **credible rule-based recommendation engine** using the FSSAI Schedule IV table. You do **not yet** have enough shelf-life, barrier-property, or compatibility data to train a genuine supervised ML model — that is the honest gap to close next, most efficiently by digitizing a handful of dedicated ICAR/NIFTEM/CFTRI packaging-shelf-life studies (full papers, not annual-report summaries) or running your own small experiments.
