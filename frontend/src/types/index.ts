export interface AnalyzeRequest {
  food_name: string;
  food_category: string;
  moisture_level: number | '';
  fat_oil_sensitivity: string;
  ph: number | '';
  respiration_activity: string;
  desired_shelf_life_days: number | '';
  storage_temperature_c: number | '';
  relative_humidity_pct: number | '';
  storage_condition: string;
  transport_condition: string;
  map_required: string;
  sustainability_priority: string;
  preferred_package_type: string;
}

export interface RequirementItem {
  level: string;
  score?: number;
  description: string;
  label: string;
  days_requested?: number;
  notes?: string[];
}

export interface CalculatedRequirements {
  disclaimer: string;
  oxygen_requirement: RequirementItem;
  moisture_requirement: RequirementItem;
  mechanical_requirement: RequirementItem;
  sealability_requirement: RequirementItem;
  map_gas_requirement: RequirementItem;
  shelf_life_protection: RequirementItem;
  compatibility_requirement: RequirementItem;
  sustainability_requirement: RequirementItem;
}

export interface ContributingFactor {
  factor: string;
  score: number;
  weight: number;
}

export interface Recommendation {
  rank: number;
  rank_title: string;
  material: string;
  primary_packaging?: string;
  secondary_packaging?: string;
  packaging_type: string;
  packaging_structure: string;
  suitability_score: number;
  suitability_score_label: string;
  ml_prediction: {
    score: number;
    label: string;
    note: string;
  };
  compatibility: {
    status: string;
    label: string;
  };
  barrier_properties: {
    otr: number | null;
    otr_unit: string;
    wvtr: number | null;
    wvtr_unit: string;
    test_condition?: string | null;
    data_status: string;
    label: string;
  };
  mechanical_properties: {
    tensile_strength?: string;
    burst_strength?: string;
    compression_strength?: string;
    burst_index?: string;
    thickness_spec?: string;
    mechanical_note?: string;
    data_status: string;
    label: string;
  };
  sustainability: {
    recyclable: string;
    compostable: string;
    biodegradable: string;
    epr_category: string;
    advantages?: string | null;
    concerns?: string | null;
    label: string;
  };
  barrier_classification?: string;
  shelf_life_suitability: {
    requested_days: number;
    expected_shelf_life_db: string;
    estimated_protection_level: string;
    validation_status?: string;
    validation_note?: string;
    additional_validation_required?: boolean;
    label: string;
  };
  map_suitability: string;
  technical_data_coverage: string;
  technical_coverage_pct: number;
  evidence_points: string[];
  contributing_factors: ContributingFactor[];
  warnings: string[];
  source_citation: {
    document: string;
    page: string;
    label: string;
  };
  scientific_limitations: string[];
}

export interface DebugInfo {
  workflow_steps: string[];
  candidate_funnel: {
    initial_generated: number;
    after_hard_constraint_filtering: number;
    rejected_count: number;
    final_top_recommendations: number;
  };
  rejected_sample: Array<{
    material: string;
    rejection_reasons: string[];
  }>;
  applied_weights: Record<string, number>;
}

export interface AnalyzeResponse {
  status?: string;
  requirements: CalculatedRequirements;
  recommendations: Recommendation[];
  all_ranked_candidates_count?: number;
  rejected_candidates?: any[];
  message?: string;
  debug?: DebugInfo;
}

export interface MLStatusResponse {
  model_type?: string;
  model_status: string;
  dataset_rows?: number;
  train_rows?: number;
  test_rows?: number;
  target_notice?: string;
  metrics?: {
    regression: {
      mae: number;
      rmse: number;
      r2: number;
    };
    classification: {
      accuracy: number;
      precision: number;
      recall: number;
      f1: number;
      confusion_matrix: number[][];
    };
  };
  feature_importance?: Record<string, number>;
}
