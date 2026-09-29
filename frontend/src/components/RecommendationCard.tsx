import React from 'react';
import { Recommendation } from '../types';
import { OriginBadge } from './OriginBadge';
import { ArrowRight, Wind, Droplets, Sun } from 'lucide-react';

interface Props {
  recommendation: Recommendation;
  onOpenExplain: (rec: Recommendation) => void;
}

export const RecommendationCard: React.FC<Props> = ({ recommendation, onOpenExplain }) => {
  const {
    rank,
    material,
    packaging_type,
    packaging_structure,
    suitability_score,
    ml_prediction,
    barrier_properties,
    sustainability,
    technical_data_coverage,
    technical_coverage_pct
  } = recommendation;

  // Derive qualitative barrier ratings (with asterisk notation matching wireframe)
  const matLower = material.toLowerCase();
  const isHighBarrier = matLower.includes('foil') || matLower.includes('aluminium') || matLower.includes('glass') || matLower.includes('tin') || matLower.includes('retort') || matLower.includes('aseptic') || matLower.includes('laminate') || matLower.includes('multilayer');
  const isPorousLow = matLower.includes('jute') || matLower.includes('sacking') || matLower.includes('porous') || (matLower.includes('paper') && !matLower.includes('laminate') && !matLower.includes('foil') && !matLower.includes('coated'));
  const isPlasticPoly = (matLower.includes('pp') || matLower.includes('hdpe') || matLower.includes('pet') || matLower.includes('ldpe')) && !isPorousLow;

  const oxygenBarrierQualitative = isPorousLow ? 'Low*' : (isHighBarrier ? 'High*' : (isPlasticPoly ? 'Medium*' : 'Low*'));
  const moistureBarrierQualitative = isPorousLow ? 'Low*' : ((isHighBarrier || isPlasticPoly) ? 'High*' : 'Low*');
  const lightBarrierQualitative = (matLower.includes('foil') || matLower.includes('tin') || matLower.includes('aluminium') || matLower.includes('metal')) 
    ? 'High*' 
    : (matLower.includes('paper') || matLower.includes('board') ? 'Moderate*' : 'Low (Transparent)*');

  const getBarrierLevelConfig = (val: string) => {
    const v = val.toLowerCase();
    if (v.includes('high')) {
      return { pct: 90, color: 'bg-emerald-500' };
    }
    if (v.includes('medium') || v.includes('moderate')) {
      return { pct: 60, color: 'bg-blue-500' };
    }
    return { pct: 25, color: 'bg-amber-400' };
  };

  const oxygenBar = getBarrierLevelConfig(oxygenBarrierQualitative);
  const moistureBar = getBarrierLevelConfig(moistureBarrierQualitative);
  const lightBar = getBarrierLevelConfig(lightBarrierQualitative);

  // Derive structure representation if standard or missing
  let displayStructure = packaging_structure;
  if (!displayStructure || displayStructure.toLowerCase() === 'standard form') {
    if (matLower.includes('aluminium') || matLower.includes('foil')) {
      displayStructure = 'PET / ALUMINIUM FOIL / PE';
    } else if (matLower.includes('aseptic') || matLower.includes('tetra') || matLower.includes('paperboard')) {
      displayStructure = 'PAPERBOARD / AL FOIL / LDPE';
    } else if (matLower.includes('retort')) {
      displayStructure = 'PET / NYLON / CPP';
    } else if (matLower.includes('pp')) {
      displayStructure = 'PP / EVOH / PP MULTILAYER';
    } else if (matLower.includes('pet')) {
      displayStructure = 'POLYETHYLENE TEREPHTHALATE (PET)';
    } else if (matLower.includes('glass')) {
      displayStructure = 'TYPE-III SODA LIME SILICATE CONTAINER';
    } else if (matLower.includes('tin')) {
      displayStructure = 'ELECTROLYTIC TINPLATE (ETP) / LACQUERED';
    } else {
      displayStructure = 'MULTILAYER COMPOSITE STRUCTURE';
    }
  }


  // Header rank title matching wireframe
  const rankLabel = rank === 1 ? '#1 RECOMMENDED PACKAGING' : `#${rank} ALTERNATIVE PACKAGING`;


  return (
    <div className="bg-white rounded-xl border border-slate-300 shadow-sm hover:shadow transition-all flex flex-col justify-between overflow-hidden font-sans">
      
      {/* ─── 1. TOP HEADER SECTION ─── */}
      <div className="p-5 pb-4">
        <div className="font-mono font-bold text-xs tracking-wider text-slate-800 uppercase mb-1">
          {rankLabel}
        </div>

        <div className="text-xs text-slate-500 font-medium mb-3">
          {technical_data_coverage} — {technical_coverage_pct}%
        </div>

        {/* Primary Material Title */}
        <h3 className="text-sm font-extrabold text-slate-900 uppercase tracking-tight leading-snug">
          {material}
        </h3>

        {/* Secondary Structure Formulation */}
        <div className="text-xs font-mono text-slate-600 mt-1 uppercase tracking-wide">
          {displayStructure.toUpperCase()}
        </div>

        {/* Multi-component Packaging Breakdown (Primary vs Secondary) */}
        {recommendation.secondary_packaging && 
         !recommendation.secondary_packaging.toLowerCase().includes('not specified') && 
         !recommendation.secondary_packaging.toLowerCase().includes('none') && (
          <div className="mt-2.5 p-2 bg-slate-50 rounded border border-slate-200 text-[11px] space-y-1">
            <div className="text-slate-700">
              <span className="font-semibold text-slate-900">Primary Contact:</span> {recommendation.primary_packaging}
            </div>
            <div className="text-slate-700">
              <span className="font-semibold text-slate-900">Secondary Packaging:</span> {recommendation.secondary_packaging}
            </div>
          </div>
        )}

        {/* Type & Model Suitability Bar */}
        <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-700">
          <span>Type: <strong className="text-slate-900 font-semibold">{packaging_type}</strong></span>
          <span>Model Suitability: <strong className="text-slate-900 font-mono font-bold">{suitability_score || ml_prediction.score}/100</strong></span>
        </div>
      </div>

      {/* ─── 2. BARRIER PERFORMANCE SECTION ─── */}
      <div className="border-t border-slate-200 p-5 py-3.5 bg-slate-50/50">
        <div className="flex items-center justify-between mb-2.5">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-900">
            BARRIER PERFORMANCE
          </span>
          <OriginBadge origin="DATABASE VALUE" size="xs" />
        </div>

        <div className="space-y-1.5 text-xs">
          <div className="flex justify-between items-center">
            <span className="text-slate-600">OTR (Oxygen Transmission)</span>
            <span className="font-mono text-slate-800">
              {barrier_properties.otr !== null && barrier_properties.otr !== undefined
                ? `${barrier_properties.otr} ${barrier_properties.otr_unit}`
                : 'Not available'}
            </span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-slate-600">WVTR (Water Vapor Transmission)</span>
            <span className="font-mono text-slate-800">
              {barrier_properties.wvtr !== null && barrier_properties.wvtr !== undefined
                ? `${barrier_properties.wvtr} ${barrier_properties.wvtr_unit}`
                : 'Not available'}
            </span>
          </div>

          {/* ─── Barrier Protection Horizontal Bar Chart ─── */}
          <div className="pt-2.5 mt-2 border-t border-slate-200/60 space-y-2.5">
            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-800">
              Barrier Protection
            </div>

            {/* Oxygen Barrier */}
            <div>
              <div className="flex justify-between items-center text-xs mb-1">
                <span className="text-slate-600 flex items-center gap-1.5 font-medium">
                  <Wind className="w-3.5 h-3.5 text-indigo-500 flex-shrink-0" />
                  <span>Oxygen Barrier</span>
                </span>
                <span className="font-semibold text-slate-900 text-[11px]">{oxygenBarrierQualitative}</span>
              </div>
              <div className="w-full bg-slate-200/80 h-2 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${oxygenBar.color}`}
                  style={{ width: `${oxygenBar.pct}%` }}
                />
              </div>
            </div>

            {/* Moisture Barrier */}
            <div>
              <div className="flex justify-between items-center text-xs mb-1">
                <span className="text-slate-600 flex items-center gap-1.5 font-medium">
                  <Droplets className="w-3.5 h-3.5 text-blue-500 flex-shrink-0" />
                  <span>Moisture Barrier</span>
                </span>
                <span className="font-semibold text-slate-900 text-[11px]">{moistureBarrierQualitative}</span>
              </div>
              <div className="w-full bg-slate-200/80 h-2 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${moistureBar.color}`}
                  style={{ width: `${moistureBar.pct}%` }}
                />
              </div>
            </div>

            {/* Light Barrier */}
            <div>
              <div className="flex justify-between items-center text-xs mb-1">
                <span className="text-slate-600 flex items-center gap-1.5 font-medium">
                  <Sun className="w-3.5 h-3.5 text-amber-500 flex-shrink-0" />
                  <span>Light Barrier</span>
                </span>
                <span className="font-semibold text-slate-900 text-[11px]">{lightBarrierQualitative}</span>
              </div>
              <div className="w-full bg-slate-200/80 h-2 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${lightBar.color}`}
                  style={{ width: `${lightBar.pct}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>


      {/* ─── 4. MATERIAL & SUSTAINABILITY SECTION ─── */}
      <div className="border-t border-slate-200 p-5 py-3.5 bg-slate-50/50">
        <div className="text-xs font-bold uppercase tracking-wider text-slate-900 mb-2.5">
          MATERIAL & SUSTAINABILITY
        </div>

        <div className="space-y-1.5 text-xs">
          <div className="flex justify-between items-center">
            <span className="text-slate-600">Food Compatibility</span>
            <span className="font-semibold text-emerald-800">Compatible*</span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-slate-600">Recyclability</span>
            <span className="font-medium text-slate-800">
              {sustainability.recyclable || 'Structure-dependent'}
            </span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-slate-600">Food-contact compliance</span>
            <span className="font-medium text-slate-700">Verify applicable</span>
          </div>
        </div>
      </div>


      {/* ─── 6. FOOTER CTA ─── */}
      <div className="border-t border-slate-200 p-4 bg-slate-50/80">
        <button
          onClick={() => onOpenExplain(recommendation)}
          className="w-full py-2.5 px-4 bg-violet-600 hover:bg-violet-700 active:bg-violet-800 text-white rounded-lg text-xs font-bold shadow-sm transition-all flex items-center justify-center gap-2 cursor-pointer"
        >
          <span>Why this packaging?</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

    </div>
  );
};
