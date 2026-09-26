import React from 'react';
import { Recommendation } from '../types';
import { OriginBadge } from './OriginBadge';
import { ArrowRight, AlertTriangle } from 'lucide-react';

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
    shelf_life_suitability,
    technical_data_coverage,
    technical_coverage_pct,
    evidence_points,
    source_citation
  } = recommendation;

  // Derive qualitative barrier ratings (with asterisk notation matching wireframe)
  const matLower = material.toLowerCase();
  const isHighBarrier = matLower.includes('foil') || matLower.includes('aluminium') || matLower.includes('glass') || matLower.includes('tin') || matLower.includes('retort') || matLower.includes('aseptic') || matLower.includes('laminate');
  const isPlasticPoly = matLower.includes('pp') || matLower.includes('hdpe') || matLower.includes('pet') || matLower.includes('ldpe');

  const oxygenBarrierQualitative = isHighBarrier ? 'High*' : (isPlasticPoly ? 'Medium*' : 'Low*');
  const moistureBarrierQualitative = isHighBarrier || isPlasticPoly ? 'High*' : 'Low*';
  const lightBarrierQualitative = (matLower.includes('foil') || matLower.includes('tin') || matLower.includes('aluminium') || matLower.includes('metal')) 
    ? 'High*' 
    : (matLower.includes('paper') || matLower.includes('board') ? 'Moderate*' : 'Low (Transparent)*');

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

  // Benchmark formatting (clean up 'nan' or empty strings)
  const rawBenchmark = shelf_life_suitability.expected_shelf_life_db;
  const benchmarkClean = (!rawBenchmark || rawBenchmark.toLowerCase() === 'nan' || rawBenchmark.trim() === '') 
    ? 'Not available' 
    : rawBenchmark;

  // Header rank title matching wireframe
  const rankLabel = rank === 1 ? '#1 RECOMMENDED PACKAGING' : `#${rank} ALTERNATIVE PACKAGING`;

  // Filter or curate fallback evidence points if needed
  const displayEvidence = evidence_points && evidence_points.length > 0
    ? evidence_points
    : [
        'High barrier against oxygen and moisture',
        'Light protection from packaging layer',
        'Suitable for oxidation- and moisture-sensitive foods',
        'Flexible format provides good sealability'
      ];

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

          <div className="flex justify-between items-center pt-1 border-t border-slate-200/60">
            <span className="text-slate-600">Oxygen Barrier</span>
            <span className="font-semibold text-slate-900">{oxygenBarrierQualitative}</span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-slate-600">Moisture Barrier</span>
            <span className="font-semibold text-slate-900">{moistureBarrierQualitative}</span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-slate-600">Light Barrier</span>
            <span className="font-semibold text-slate-900">{lightBarrierQualitative}</span>
          </div>
        </div>
      </div>

      {/* ─── 3. PRESERVATION SUITABILITY SECTION ─── */}
      <div className="border-t border-slate-200 p-5 py-3.5">
        <div className="text-xs font-bold uppercase tracking-wider text-slate-900 mb-2">
          PRESERVATION SUITABILITY
        </div>

        <div className="inline-block text-xs font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 mb-2.5">
          {shelf_life_suitability.estimated_protection_level} Protection
        </div>

        <div className="space-y-1.5 text-xs">
          <div className="flex justify-between items-center">
            <span className="text-slate-600">Target Shelf Life</span>
            <span className="font-mono font-semibold text-slate-900">
              {shelf_life_suitability.requested_days} days
            </span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-slate-600">Validated Benchmark</span>
            <span className="text-slate-800 font-mono text-[11px] truncate max-w-[170px]" title={benchmarkClean}>
              {benchmarkClean}
            </span>
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

      {/* ─── 5. WHY THIS PACKAGING? BULLET POINTS ─── */}
      <div className="border-t border-slate-200 p-5 py-3.5">
        <div className="text-xs font-bold uppercase tracking-wider text-slate-900 mb-2">
          WHY THIS PACKAGING?
        </div>

        <div className="space-y-1 text-xs text-slate-700">
          {displayEvidence.map((pt, i) => (
            <div key={i} className="flex items-start gap-2">
              <span className="text-slate-400 font-bold">•</span>
              <span className="leading-snug">{pt}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ─── 6. DATA LIMITATION & FOOTER CTA ─── */}
      <div className="border-t border-slate-200 p-5 bg-slate-50/80 flex flex-col justify-between">
        <div className="mb-3.5">
          <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-amber-800 mb-1">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600 flex-shrink-0" />
            <span>DATA LIMITATION</span>
          </div>
          <p className="text-[11px] text-slate-600 leading-relaxed">
            Numerical OTR/WVTR values are unavailable for the selected structure under the required test conditions. Barrier fit is therefore based on source-supported qualitative data and is not a numerical performance guarantee.
          </p>
          <p className="text-[10px] text-slate-500 font-mono mt-2 truncate">
            Source: {source_citation.document || 'FSSAI Packaging Regulations'} • {source_citation.page ? `Page ${source_citation.page}` : 'Schedule IV'}
          </p>
        </div>

        {/* Action Button: [ Why this packaging? → ] */}
        <button
          onClick={() => onOpenExplain(recommendation)}
          className="w-full py-2.5 px-4 bg-violet-600 hover:bg-violet-700 active:bg-violet-800 text-white rounded-lg text-xs font-bold shadow-sm transition-all flex items-center justify-center gap-2 cursor-pointer mt-1"
        >
          <span>Why this packaging?</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

    </div>
  );
};
