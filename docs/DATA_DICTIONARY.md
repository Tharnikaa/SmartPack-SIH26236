# DATA DICTIONARY: SmartPack Unified Datasets

This data dictionary outlines the schemas, data types, physical units, and ML roles across all supplied datasets in `Claude-DataSet/` and `data/original/`.

---

## 1. Food Dataset (`01_food_dataset.csv`)
**Source:** ICMR Indian Food Composition Tables (IFCT 2017), 496 rows.

| Field Name | Type | Unit | Description | ML Role |
|---|---|---|---|---|
| `food_id` | String | - | Unique food identifier | Metadata |
| `food_name` | String | - | Common food name | Identification / Search |
| `food_category` | String | - | Broad food category classification | Primary Key / Lookup |
| `food_subcategory` | String | - | Specific commodity category | Lookup |
| `moisture_content` | Float | g/100g (%) | Analytical moisture content | Input Feature |
| `protein_content` | Float | g/100g | Crude protein content | Input Feature |
| `fat_content` | Float | g/100g | Total fat content | Input Feature (Oxidation driver) |
| `carbohydrate_content` | Float | g/100g | Total available carbohydrate | Input Feature |
| `fiber_content` | Float | g/100g | Dietary fiber | Reference |
| `ash_content` | Float | g/100g | Total mineral ash content | Reference |
| `pH` | Float | - | Food acidity (null in raw IFCT extract) | User Input Parameter |
| `water_activity` | Float | - | Water activity aw (null in raw IFCT extract) | Derived / User Input |
| `source` | String | - | ICMR / National Institute of Nutrition | Audit Citation |

---

## 2. Packaging Materials Dataset (`06_packaging_material_dataset.csv`)
**Source:** BIS Food Packaging Handbook & FSSAI Packaging Regulations, 26 rows.

| Field Name | Type | Unit | Description | Role |
|---|---|---|---|---|
| `packaging_id` | String | - | Unique identifier (e.g. PKG-001) | Primary Key |
| `material_name` | String | - | Standard polymer / substrate name | Core Entity |
| `material_family` | String | - | Polymer family (Plastic, Glass, Metal, Paper) | Categorical Grouping |
| `material_type` | String | - | Chemical designation (e.g. PET, HDPE, Tinplate) | Subtype |
| `food_contact_suitable` | String | - | Compliance with FSS Regulations 2018 | Safety Filter |
| `source_document` | String | - | BIS Handbook / FSSAI Regulations | Audit Citation |

---

## 3. Packaging Properties Dataset (`07_packaging_properties_dataset_Claude.csv`)
**Source:** BIS Standards (IS 1397, IS 2991, IS 5012, IS 6615, IS 10176, IS 16186), 85 rows.

| Field Name | Type | Unit | Description | Role |
|---|---|---|---|---|
| `material_name` | String | - | Substrate name with IS standard designation | Foreign Key |
| `property_name` | String | - | Physical / mechanical parameter name | Technical Metric |
| `property_value` | String / Float | Various | Numerical specification threshold | Technical Property |
| `unit` | String | Various | %, N, kN/m, g/m², kPa, etc. | Physical Unit |
| `test_condition` | String | - | Standardized test regime (e.g., Cobb 60s, 27°C) | Test Standard |

---

## 4. Barrier Properties Dataset (`08_barrier_properties_dataset.csv`)
**Source:** BIS Standards (IS 5012:1987), 2 rows.

| Field Name | Type | Unit | Description | Role |
|---|---|---|---|---|
| `material_name` | String | - | Coated Regenerated Cellulose Film | Foreign Key |
| `water_vapour_transmission_rate` | Float | g/m²/24h | Water vapor transmission rate (15 uncreased, 30 creased) | Measured Barrier Metric |
| `oxygen_transmission_rate` | Float | cc/m²/day | Oxygen transmission rate (**Null in raw dataset**) | Not Fabricated |
| `test_temperature` | Float | °C | Test temperature (38°C) | Test Regime |
| `test_relative_humidity` | Float | % | Test relative humidity (90% RH) | Test Regime |

---

## 5. Regulatory Mappings & Recommendations (`14_recommended_packaging.csv`)
**Source:** FSSAI Packaging Regulations 2018 Schedule IV & ICAR PHM Reports, 102 rows.

| Field Name | Type | Unit | Description | Role |
|---|---|---|---|---|
| `food_name` | String | - | Specific tested food product | Lookup |
| `food_category` | String | - | FSSAI Schedule IV food category | Candidate Lookup Key |
| `recommended_packaging_material` | String | - | Prescribed packaging substrate | Candidate Material |
| `recommended_packaging_type` | String | - | Bottle, Pouch, Can, Jar, Tub, Carton | Candidate Format |
| `recommended_packaging_structure` | String | - | Multilayer, Mono-layer, Rigid, Flexible | Structural Specification |
| `storage_condition` | String | - | Ambient, Chilled, Frozen | Storage Regime |
| `expected_shelf_life` | String | - | Prescribed preservation expectation | Shelf-Life Benchmark |
| `reason` | String | - | FSSAI technical rationale | Explainability Evidence |

---

## 6. Food Packaging Compatibility Dataset (`09_food_packaging_compatibility_MERGED.csv`)
**Source:** FSSAI Regulations & ICAR Trials, 11 rows.

| Field Name | Type | Unit | Description | Role |
|---|---|---|---|---|
| `food_category` | String | - | Target food group | Foreign Key |
| `packaging_material` | String | - | Packaging material evaluated | Foreign Key |
| `compatibility` | String | - | Compatible, Less Compatible, or Prohibited | Compatibility Metric |
| `compatibility_reason` | String | - | Scientific rationale (e.g. lipid oxidation in pouch vs tub) | Explainability Evidence |

---

## 7. Regulatory Rules & Prohibitions (`13_regulatory_rules.csv`)
**Source:** FSSAI / BIS / CPCB / MoEFCC, 20 rows.

| Field Name | Type | Unit | Description | Role |
|---|---|---|---|---|
| `rule_id` | String | - | Rule identifier (RG001 to RG020) | Key |
| `requirement` | String | - | Regulatory compliance requirement | Mandate |
| `prohibited` | String | - | Strictly banned practices (e.g., recycled plastic direct contact) | Hard Safety Filter |
| `migration_requirement` | String | mg/kg, mg/dm² | Overall migration limits per IS 9845 | Chemical Safety Filter |
