# 16_material_barrier_mechanical_reference.csv — What This Adds

## Why this file exists
Your original audit (`DATA_QUALITY_AND_ML_DESIGN_REPORT.md`) found that Datasets 07/08 had
**zero OTR values, only 2 WVTR values, and no mechanical-strength data** for the common
packaging materials your recommendations will actually surface (LDPE, PET, EVOH, foil
laminates, etc.). This file closes that specific gap.

## What's in it — 20 materials, 23 columns
Covers the materials that will realistically appear as candidates from your rule engine:
LDPE, LLDPE, HDPE, CPP, BOPP, BOPET/PET, plasticized PVC, PVDC-coated film, EVOH,
BOPA/Nylon, metalized BOPP, metalized PET, aluminum foil laminate, PLA, PBAT/PLA blend,
uncoated cellulose film, uncoated kraft paper, tinplate/TFS can, glass, and a high-barrier
retort pouch laminate.

For each material: OTR, WVTR (both as **ranges**, not false-precision single points),
a CO2TR note, tensile-strength range, heat-seal temperature, a sealability rating,
a recyclability note, and — importantly — a `key_limitation` column flagging the real
caveats (e.g. EVOH's barrier collapsing at high humidity, metalized films cracking on
flexing, PVC's food-contact restrictions).

## Data origin — read this before using it in your pipeline
Every row is tagged `data_origin = REFERENCE VALUE (published literature)`, **not**
`DATABASE VALUE` like your existing FSSAI/BIS/ICAR/AGMARK rows. That distinction matters:
- `DATABASE VALUE` (Datasets 01–14) = a number traced to a specific regulatory document or
  field trial with a page number.
- `REFERENCE VALUE` (this file) = a typical range from standard packaging-science
  literature (Robertson's *Food Packaging: Principles and Practice*, Selke's *Plastics
  Packaging*, and equivalent peer-reviewed/technical sources cited per row), at standard
  test conditions (ASTM D3985 for OTR, ASTM F1249 for WVTR). These are the same class of
  values used industry-wide for first-pass material selection — but they are **typical
  ranges for the polymer class**, not a specific supplier's certified datasheet, and should
  be labeled that way in your UI, exactly as your explainability engine already
  distinguishes "DATABASE VALUE" vs "DERIVED SCORE."

Keep this as a **third badge** in your app: `DATABASE VALUE` / `REFERENCE VALUE
(literature)` / `DERIVED (calculated)` — don't collapse it into either existing category.

## Where it overlaps with your existing data
Four rows explicitly cross-reference material instances you already have real trial data
for — use both together, don't let this file overwrite them:
- **Kraft paper**: mechanical/moisture specs already in Datasets 06/07 (IS 1397) — this file
  only adds the barrier-gap context (paper has no meaningful O2/moisture barrier at all).
- **Cellulose film**: your Dataset 08 has 2 real WVTR values, but only for the *coated*
  grade — this file's uncoated-cellophane row explains why that distinction matters.
- **Tinplate can & glass bottle**: your Dataset 09/10 already has real shelf-life outcomes
  (canned catfish, buttermilk in glass) — this file adds the barrier numbers behind why
  those worked (zero permeability), it doesn't replace the real outcome data.
- **Retort pouch laminate**: your Dataset 10 has three real retort shelf-life outcomes
  (soy paneer, tapioca/fish curry) — use those as your shelf-life anchor, this file supplies
  the barrier range for that material class.

## Using it for the thickness calculation
`otr_low`/`otr_high` and `wvtr_low`/`wvtr_high` are given at `reference_thickness_micron`.
To solve for the thickness needed to hit a food's *required* OTR/WVTR (from your Stage 2
requirement engine):

```
permeability = otr_value_at_reference × reference_thickness_micron
required_thickness = permeability / required_OTR
```
Do this for both OTR and WVTR, take the larger (more conservative) result, then round up to
the nearest commercial gauge (25/37/50/75/100 micron are standard). **Do not run this
calculation on REF-18 (tinplate can) or REF-19 (glass)** — they're rigid/impermeable, not
thickness-scalable films; flag those two as "N/A — rigid, impermeable" in your UI instead.

For multilayer laminates (REF-13, REF-20, and any metalized film), treat the calculated
thickness as a rougher estimate — layers in series don't average linearly, so label it
"estimated (multilayer)" rather than "calculated" the way you would for a single-layer film.

## What this file does NOT fix
Shelf-life-outcome precision (still anchored on your real 26-row Dataset 05/10) and
MAP gas-composition precision for less-studied food categories are unaffected by this file
— those gaps are on the food/outcome side, not the material-property side, and no material
reference table closes them. Keep presenting those as ranges/estimates, as already agreed.
