import React from 'react';
import { Recommendation } from '../types';
import { OriginBadge } from './OriginBadge';
import { CoverageBadge } from './CoverageBadge';
import { 
  X, CheckCircle, AlertTriangle, Info, BookOpen, 
  BarChart2, ShieldAlert, FileText 
} from 'lucide-react';

interface Props {
  recommendation: Recommendation | null;
  onClose: () => void;
}

export const WhyPackagingModal: React.FC<Props> = ({ recommendation, onClose }) => {
  if (!recommendation) return null;

  const {
    rank,
    rank_title,
    material,
    packaging_type,
    suitability_score,
    ml_prediction,
    evidence_points,
    contributing_factors,
    warnings,
    source_citation,
    scientific_limitations,
    technical_data_coverage,
    technical_coverage_pct
  } = recommendation;

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

          {/* Section 1: Positive Evidence Checklist */}
          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-emerald-600" />
              Evidence-Based Recommendation Rationale
            </h3>
            <div className="space-y-2">
              {evidence_points.map((pt, i) => (
                <div key={i} className="p-3 rounded-lg bg-emerald-50/50 border border-emerald-100 flex items-start gap-2.5">
                  <CheckCircle className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                  <span className="text-xs text-emerald-950 font-medium leading-relaxed">{pt}</span>
                </div>
              ))}
            </div>
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
              {scientific_limitations.map((lim, i) => (
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
