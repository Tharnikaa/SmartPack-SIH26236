import React from 'react';
import { Recommendation } from '../types';
import { OriginBadge } from './OriginBadge';
import { CoverageBadge } from './CoverageBadge';
import { 
  Award, CheckCircle, AlertTriangle, ShieldCheck, 
  Wind, Droplets, Leaf, ChevronRight, HelpCircle 
} from 'lucide-react';

interface Props {
  recommendation: Recommendation;
  onOpenExplain: (rec: Recommendation) => void;
}

export const RecommendationCard: React.FC<Props> = ({ recommendation, onOpenExplain }) => {
  const {
    rank,
    rank_title,
    material,
    packaging_type,
    packaging_structure,
    suitability_score,
    ml_prediction,
    barrier_properties,
    mechanical_properties,
    sustainability,
    shelf_life_suitability,
    map_suitability,
    technical_data_coverage,
    technical_coverage_pct,
    evidence_points,
    warnings,
    source_citation
  } = recommendation;

  const isFirst = rank === 1;

  return (
    <div
      className={`rounded-2xl border transition-all duration-200 bg-white flex flex-col justify-between ${
        isFirst
          ? 'border-brand-300 ring-2 ring-brand-500/10 shadow-md'
          : 'border-slate-200 shadow-sm hover:shadow-md'
      }`}
    >
      {/* Top Header */}
      <div className="p-6 border-b border-slate-100">
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex items-center gap-2">
            <span
              className={`inline-flex items-center justify-center font-bold rounded-lg text-xs px-2.5 py-1 ${
                isFirst
                  ? 'bg-brand-600 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-700'
              }`}
            >
              {isFirst && <Award className="w-3.5 h-3.5 mr-1" />}
              #{rank} {rank_title}
            </span>
            <CoverageBadge rating={technical_data_coverage} pct={technical_coverage_pct} />
          </div>

          <div className="text-right">
            <div className="flex items-baseline gap-1 justify-end">
              <span className="text-2xl font-extrabold tracking-tight text-slate-900">
                {suitability_score}
              </span>
              <span className="text-xs text-slate-400 font-medium">/ 100</span>
            </div>
            <div className="flex justify-end mt-0.5">
              <OriginBadge origin="DERIVED SCORE" size="xs" />
            </div>
          </div>
        </div>

        {/* Material & Type */}
        <h3 className="text-lg font-bold text-slate-900 leading-snug">{material}</h3>
        <p className="text-xs text-slate-500 mt-1 flex items-center gap-2">
          <span>Type: <strong className="text-slate-700 font-medium">{packaging_type}</strong></span>
          <span>•</span>
          <span>Structure: <strong className="text-slate-700 font-medium">{packaging_structure}</strong></span>
        </p>

        {/* ML Sub-Score note */}
        <div className="mt-3 py-1.5 px-2.5 rounded-lg bg-slate-50 border border-slate-200/60 flex items-center justify-between text-xs">
          <span className="text-slate-500 flex items-center gap-1 font-mono text-[11px]">
            Model Suitability Index: <strong className="text-purple-700">{ml_prediction.score}</strong>
          </span>
          <OriginBadge origin="ML PREDICTION" size="xs" />
        </div>
      </div>

      {/* Technical Properties Grid */}
      <div className="p-6 space-y-4 text-xs">
        {/* Barrier Matrix */}
        <div className="p-3.5 rounded-xl bg-slate-50/80 border border-slate-200/70">
          <div className="flex items-center justify-between mb-2">
            <span className="font-semibold text-slate-700 flex items-center gap-1">
              <Wind className="w-3.5 h-3.5 text-purple-600" /> Barrier Performance
            </span>
            <OriginBadge origin="DATABASE VALUE" size="xs" />
          </div>

          <div className="grid grid-cols-2 gap-2 text-[11px]">
            <div>
              <span className="text-slate-400 block">OTR (Oxygen Transmission):</span>
              <span className="font-medium text-slate-800">
                {barrier_properties.otr !== null && barrier_properties.otr !== undefined
                  ? `${barrier_properties.otr} ${barrier_properties.otr_unit}`
                  : 'Data unavailable'}
              </span>
            </div>
            <div>
              <span className="text-slate-400 block">WVTR (Water Vapor Transmission):</span>
              <span className="font-medium text-slate-800">
                {barrier_properties.wvtr !== null && barrier_properties.wvtr !== undefined
                  ? `${barrier_properties.wvtr} ${barrier_properties.wvtr_unit}`
                  : 'Data unavailable'}
              </span>
            </div>
          </div>
          {barrier_properties.test_condition && (
            <p className="text-[10px] text-slate-400 mt-1 italic">
              Test regime: {barrier_properties.test_condition}
            </p>
          )}
        </div>

        {/* Shelf Life & Storage */}
        <div className="p-3.5 rounded-xl bg-slate-50/80 border border-slate-200/70">
          <div className="flex items-center justify-between mb-1.5">
            <span className="font-semibold text-slate-700">Preservation Suitability</span>
            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200">
              {shelf_life_suitability.estimated_protection_level} Protection
            </span>
          </div>
          <p className="text-[11px] text-slate-600">
            Target requested: <strong className="text-slate-800">{shelf_life_suitability.requested_days} days</strong>
          </p>
          <p className="text-[11px] text-slate-500 mt-0.5">
            Prescribed benchmark: {shelf_life_suitability.expected_shelf_life_db}
          </p>
        </div>

        {/* Mechanical & Sustainability Pills */}
        <div className="grid grid-cols-2 gap-2">
          <div className="p-2.5 rounded-lg border border-slate-200 bg-white">
            <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block">Mechanical Spec</span>
            <span className="text-xs font-medium text-slate-800 line-clamp-1">
              {mechanical_properties.tensile_strength || mechanical_properties.burst_index || 'BIS Spec standard'}
            </span>
          </div>

          <div className="p-2.5 rounded-lg border border-slate-200 bg-white">
            <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block">Recyclability</span>
            <span className="text-xs font-medium text-slate-800 flex items-center gap-1">
              <Leaf className="w-3 h-3 text-emerald-600" />
              {sustainability.recyclable || 'Standard EPR'}
            </span>
          </div>
        </div>

        {/* Positive Evidence Points */}
        <div className="space-y-1.5">
          <span className="text-[11px] font-semibold text-slate-700 uppercase tracking-wider block">
            Evidence Highlights
          </span>
          {evidence_points.slice(0, 2).map((ev, i) => (
            <div key={i} className="flex items-start gap-1.5 text-xs text-slate-600">
              <CheckCircle className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0 mt-0.5" />
              <span>{ev}</span>
            </div>
          ))}
        </div>

        {/* Warnings if any */}
        {warnings && warnings.length > 0 && (
          <div className="p-2.5 rounded-lg bg-amber-50/70 border border-amber-200/80 text-[11px] text-amber-900 flex items-start gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600 flex-shrink-0 mt-0.5" />
            <span className="leading-tight">{warnings[0]}</span>
          </div>
        )}
      </div>

      {/* Bottom CTA */}
      <div className="p-4 bg-slate-50 border-t border-slate-100 rounded-b-2xl">
        <button
          onClick={() => onOpenExplain(recommendation)}
          className={`w-full py-2 px-3 rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition-all ${
            isFirst
              ? 'bg-brand-600 hover:bg-brand-700 text-white shadow-sm'
              : 'bg-white hover:bg-slate-100 text-slate-800 border border-slate-200'
          }`}
        >
          <span>Why this packaging? View Analysis</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </button>
        <p className="text-[10px] text-slate-400 text-center mt-2 truncate">
          Ref: {source_citation.document} (p.{source_citation.page})
        </p>
      </div>
    </div>
  );
};
