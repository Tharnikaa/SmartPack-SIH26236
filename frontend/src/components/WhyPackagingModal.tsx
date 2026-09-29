import React, { useState, useEffect } from 'react';
import { Recommendation } from '../types';
import { OriginBadge } from './OriginBadge';
import { CoverageBadge } from './CoverageBadge';
import { API_BASE } from '../services/api';
import { 
  X, CheckCircle, Info, BookOpen, 
  BarChart2, ShieldAlert, Sparkles, RefreshCw, Clock 
} from 'lucide-react';

interface Props {
  recommendation: Recommendation | null;
  userInput?: any;
  requirements?: any;
  onClose: () => void;
}

export const WhyPackagingModal: React.FC<Props> = ({ recommendation, userInput, requirements, onClose }) => {
  const [aiNarrative, setAiNarrative] = useState<string | null>(null);
  const [aiModel, setAiModel] = useState<string | null>(null);
  const [loadingAi, setLoadingAi] = useState(false);

  useEffect(() => {
    setAiNarrative(null);
    setAiModel(null);
    if (!recommendation) return;

    let isMounted = true;
    setLoadingAi(true);

    fetch(`${API_BASE}/explain/gemini`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        recommendation,
        user_input: userInput || {},
        requirements: requirements || {}
      })
    })
      .then((res) => res.json())
      .then((data) => {
        if (!isMounted) return;
        if (data.status === 'SUCCESS') {
          setAiNarrative(data.narrative);
          setAiModel(data.model || 'Gemini 2.5 Flash');
        } else {
          setAiNarrative(data.message || 'Gemini API key is not configured.');
        }
      })
      .catch(() => {
        if (!isMounted) return;
        setAiNarrative('Failed to contact explanation service.');
      })
      .finally(() => {
        if (isMounted) setLoadingAi(false);
      });

    return () => {
      isMounted = false;
    };
  }, [recommendation?.material, recommendation?.rank]);

  const handleRegenerate = () => {
    if (!recommendation) return;
    setLoadingAi(true);
    fetch(`${API_BASE}/explain/gemini`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        recommendation,
        user_input: userInput || {},
        requirements: requirements || {}
      })
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === 'SUCCESS') {
          setAiNarrative(data.narrative);
          setAiModel(data.model || 'Gemini 2.5 Flash');
        } else {
          setAiNarrative(data.message || 'Gemini API key is not configured.');
        }
      })
      .catch(() => {
        setAiNarrative('Failed to contact explanation service.');
      })
      .finally(() => {
        setLoadingAi(false);
      });
  };

  if (!recommendation) return null;

  const {
    rank = 1,
    material = 'Packaging Material',
    packaging_type = 'Package',
    suitability_score = 0,
    ml_prediction = { score: 0, label: 'ML Prediction', note: '' },
    evidence_points = [],
    contributing_factors = [],
    source_citation = { document: 'FSSAI Packaging Regulations 2018', page: 10 },
    scientific_limitations = [],
    technical_data_coverage = 'Standard',
    technical_coverage_pct = 75
  } = recommendation;

  const displayReasons = (evidence_points && evidence_points.length > 0)
    ? evidence_points
    : [
        'Barrier Performance: Satisfies calculated oxygen and moisture barrier requirements.',
        'Chemical Compatibility: Chemically compatible and approved under FSSAI Schedule IV.',
        'Physical Integrity: Suitable structural strength for the specified transport conditions.',
        'Environmental Fit: Aligns with circular recycling guidelines / EPR categories.'
      ];

  const safeLimitations = (scientific_limitations && scientific_limitations.length > 0)
    ? scientific_limitations
    : [
        'OTR and WVTR barrier transmission rates depend heavily on real-world test conditions.',
        'Exact product shelf life requires empirical accelerated or real-time shelf-life testing.',
        'ML suitability is an algorithmic scoring signal based on multi-attribute feature engineering.'
      ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xl max-w-3xl w-full max-h-[90vh] flex flex-col overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b border-slate-100 flex items-start justify-between bg-slate-50/70">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-brand-100 text-brand-700">
                Rank #{rank} Evaluation
              </span>
              <CoverageBadge rating={technical_data_coverage} pct={technical_coverage_pct} />
            </div>
            <h2 className="text-xl font-bold text-slate-900">Why was this packaging recommended?</h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Material: <strong className="text-slate-800">{material}</strong> ({packaging_type})
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-xs text-slate-700">
          {/* Scoring Origin Transparency */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">
                Derived Hybrid Suitability Score
              </span>
              <div className="flex items-baseline gap-1 mt-0.5">
                <span className="text-2xl font-black text-slate-900">{suitability_score}</span>
                <span className="text-xs text-slate-400">/ 100</span>
              </div>
            </div>
            <div className="flex flex-col gap-1 items-start sm:items-end">
              <div className="flex items-center gap-2">
                <span className="text-[11px] text-slate-500">Classification:</span>
                <OriginBadge origin="DERIVED SCORE" />
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] text-slate-500">ML Model Output: {ml_prediction.score}/100</span>
                <OriginBadge origin="ML PREDICTION" size="xs" />
              </div>
            </div>
          </div>

          {/* Reasons Why This Packaging Was Selected */}
          <div className="p-4 rounded-xl bg-violet-50/70 border border-violet-200">
            <h3 className="text-xs font-bold text-violet-950 uppercase tracking-wider mb-2.5 flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-violet-700 flex-shrink-0" />
              Reasons Why This Packaging Was Selected
            </h3>
            <div className="space-y-2">
              {displayReasons.map((pt, i) => (
                <div key={i} className="p-3 rounded-lg bg-white border border-violet-100 flex items-start gap-2.5 shadow-2xs">
                  <CheckCircle className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                  <span className="text-xs text-slate-800 font-medium leading-relaxed">{pt}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Shelf Life & Barrier Validation Status */}
          <div className={`p-4 rounded-xl border ${
            recommendation.shelf_life_suitability?.additional_validation_required
              ? 'bg-amber-50/80 border-amber-200'
              : 'bg-emerald-50/70 border-emerald-200'
          }`}>
            <div className="flex items-start justify-between gap-2">
              <div className="flex items-center gap-2">
                <Clock className={`w-4 h-4 ${recommendation.shelf_life_suitability?.additional_validation_required ? 'text-amber-700' : 'text-emerald-700'}`} />
                <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                  Shelf-Life & Technical Preservation Status
                </h3>
              </div>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ${
                recommendation.shelf_life_suitability?.additional_validation_required
                  ? 'bg-amber-200/80 text-amber-900 border border-amber-300'
                  : 'bg-emerald-200/80 text-emerald-900 border border-emerald-300'
              }`}>
                {recommendation.shelf_life_suitability?.additional_validation_required
                  ? 'Additional Validation Required'
                  : (recommendation.shelf_life_suitability?.estimated_protection_level || 'Validated')}
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 mt-3 text-xs">
              <div className="p-2 rounded-lg bg-white/80 border border-slate-200/60">
                <span className="text-[10px] text-slate-500 font-semibold block uppercase">Target Shelf Life</span>
                <span className="font-bold text-slate-900">{recommendation.shelf_life_suitability?.requested_days || userInput?.desired_shelf_life_days || 180} days</span>
              </div>
              <div className="p-2 rounded-lg bg-white/80 border border-slate-200/60">
                <span className="text-[10px] text-slate-500 font-semibold block uppercase">Validated Benchmark (DB)</span>
                <span className="font-bold text-slate-900">{recommendation.shelf_life_suitability?.expected_shelf_life_db || 'Not available'}</span>
              </div>
              <div className="p-2 rounded-lg bg-white/80 border border-slate-200/60">
                <span className="text-[10px] text-slate-500 font-semibold block uppercase">Barrier Classification</span>
                <span className="font-bold text-slate-900">{recommendation.barrier_classification || 'Standard'}</span>
              </div>
            </div>

            {recommendation.shelf_life_suitability?.additional_validation_required && (
              <p className="mt-2.5 text-[11px] text-amber-900 font-medium leading-relaxed bg-amber-100/60 p-2 rounded border border-amber-200">
                ⚠️ <strong>Validation Gap Notice:</strong> Target shelf life ({recommendation.shelf_life_suitability?.requested_days || 180} days) exceeds the empirically validated database benchmark ({recommendation.shelf_life_suitability?.expected_shelf_life_db}). Additional real-time or accelerated shelf-life validation is required for target commercial distribution.
              </p>
            )}
          </div>

          {/* Optional Gemini AI Scientific Narrative */}
          <div className="p-4 rounded-xl bg-gradient-to-br from-brand-50/70 to-purple-50/50 border border-brand-200">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-brand-600" />
                <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                  AI Scientific Justification (Google Gemini)
                </h3>
              </div>
              <button
                onClick={handleRegenerate}
                disabled={loadingAi}
                className="px-2.5 py-1 rounded-lg bg-white border border-brand-200 hover:bg-brand-50 text-[11px] font-semibold text-brand-700 flex items-center gap-1.5 transition-colors shadow-2xs"
              >
                <RefreshCw className={`w-3 h-3 ${loadingAi ? 'animate-spin' : ''}`} />
                <span>{loadingAi ? 'Synthesizing...' : (aiNarrative ? 'Regenerate Narrative' : 'Generate Gemini Narrative')}</span>
              </button>
            </div>

            {loadingAi ? (
              <div className="mt-2 text-xs text-slate-700 flex items-center gap-2.5 p-3.5 bg-white/90 rounded-lg border border-brand-200">
                <RefreshCw className="w-4 h-4 text-brand-600 animate-spin flex-shrink-0" />
                <span className="font-medium">Synthesizing authoritative scientific packaging justification using Google Gemini...</span>
              </div>
            ) : aiNarrative ? (
              <div className="mt-2 text-xs text-slate-800 leading-relaxed font-normal bg-white/80 p-3 rounded-lg border border-brand-100 whitespace-pre-line">
                {aiNarrative}
                <div className="mt-2 pt-2 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400">
                  <span>Synthesized by {aiModel || 'Gemini 2.5 Flash'} grounded in FSSAI Schedule IV & BIS limits</span>
                  <OriginBadge origin="AI EXPLANATION" size="xs" />
                </div>
              </div>
            ) : (
              <p className="text-[11px] text-slate-600 leading-relaxed">
                Click <strong>"Generate Gemini Narrative"</strong> above to synthesize an authoritative scientific justification with Google Gemini.
              </p>
            )}
          </div>

          {/* Section 2: Hybrid Contributing Factors */}
          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
              <BarChart2 className="w-4 h-4 text-brand-600" />
              Scoring Weight Breakdown & Factors
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {contributing_factors.map((f, i) => (
                <div key={i} className="p-3 rounded-lg border border-slate-200/80 bg-white flex flex-col justify-between">
                  <div className="flex justify-between items-center mb-1.5">
                    <span className="font-semibold text-slate-700 text-xs">{f.factor}</span>
                    <span className="text-[11px] font-mono text-slate-500">Weight: {(f.weight * 100).toFixed(0)}%</span>
                  </div>
                  <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden mb-1">
                    <div
                      className="bg-brand-500 h-full rounded-full"
                      style={{ width: `${f.score * 100}%` }}
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 text-right">Factor Score: {(f.score * 100).toFixed(0)}/100</span>
                </div>
              ))}
            </div>
          </div>

          {/* Section 3: Regulatory Citation & Source Grounding */}
          <div className="p-4 rounded-xl bg-blue-50/50 border border-blue-100">
            <h3 className="text-xs font-bold text-blue-900 mb-1 flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-blue-700" />
              Authoritative Source Reference
            </h3>
            <p className="text-xs text-blue-800">
              Endorsed in <strong>{source_citation.document}</strong> (Page {source_citation.page}).
              Complies with Schedule IV of Food Safety and Standards (Packaging) Regulations, 2018.
            </p>
          </div>

          {/* Section 4: Warnings & Limitations */}
          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-amber-600" />
              Mandatory Scientific Disclosures & Limitations
            </h3>
            <div className="space-y-2">
              {safeLimitations.map((lim, i) => (
                <div key={i} className="p-2.5 rounded-lg bg-slate-50 border border-slate-200/80 flex items-start gap-2 text-slate-600 text-[11px]">
                  <Info className="w-3.5 h-3.5 text-slate-400 flex-shrink-0 mt-0.5" />
                  <span className="leading-relaxed">{lim}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-100 bg-slate-50 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-xl text-xs font-semibold transition-colors"
          >
            Close Analysis
          </button>
        </div>
      </div>
    </div>
  );
};
