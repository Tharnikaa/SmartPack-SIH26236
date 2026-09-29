import React, { useEffect } from 'react';
import { Recommendation } from '../types';
import { OriginBadge } from './OriginBadge';
import { X, ArrowLeftRight, CheckCircle2, Award } from 'lucide-react';

interface Props {
  recommendations: Recommendation[];
  onClose: () => void;
}

export const ComparisonModal: React.FC<Props> = ({ recommendations, onClose }) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!recommendations || recommendations.length === 0) return null;

  const topCandidates = recommendations.slice(0, 3);

  const getVal = (val: any) => {
    if (React.isValidElement(val)) {
      return val;
    }
    if (
      val === null ||
      val === undefined ||
      val === '' ||
      String(val).toLowerCase() === 'nan' ||
      String(val).toLowerCase().includes('(nan)') ||
      String(val).toLowerCase().includes('data unavailable') ||
      String(val).toLowerCase() === 'none' ||
      String(val).toLowerCase() === 'undefined'
    ) {
      return <span className="text-slate-400 italic">Not available</span>;
    }
    return String(val);
  };

  const rows = [
    {
      label: 'Rank & Designation',
      values: topCandidates.map((r) => `#${r.rank} ${r.rank === 1 ? 'Primary Recommendation' : 'Alternative Option'}`)
    },
    {
      label: 'Material Specification',
      values: topCandidates.map((r) => r.material)
    },
    {
      label: 'Primary Packaging Contact',
      values: topCandidates.map((r) => r.primary_packaging || r.material)
    },
    {
      label: 'Secondary / Outer System',
      values: topCandidates.map((r) => r.secondary_packaging || 'Not applicable (Single unit)')
    },
    {
      label: 'Packaging Type',
      values: topCandidates.map((r) => r.packaging_type)
    },
    {
      label: 'Barrier Classification',
      values: topCandidates.map((r) => (
        <span key={r.rank} className={`font-semibold ${
          r.barrier_classification?.includes('Conditional')
            ? 'text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200'
            : r.barrier_classification?.includes('High')
            ? 'text-emerald-700'
            : 'text-slate-700'
        }`}>
          {r.barrier_classification || 'Standard Barrier'}
        </span>
      ))
    },
    {
      label: 'OTR (Oxygen Transmission)',
      values: topCandidates.map((r) =>
        r.barrier_properties.otr !== null && r.barrier_properties.otr !== undefined
          ? `${r.barrier_properties.otr} ${r.barrier_properties.otr_unit}`
          : 'Not available'
      )
    },
    {
      label: 'WVTR (Moisture Vapor Transmission)',
      values: topCandidates.map((r) =>
        r.barrier_properties.wvtr !== null && r.barrier_properties.wvtr !== undefined
          ? `${r.barrier_properties.wvtr} ${r.barrier_properties.wvtr_unit}`
          : 'Not available'
      )
    },
    {
      label: 'Thickness Spec',
      values: topCandidates.map((r) => r.mechanical_properties?.thickness_spec || 'Not available')
    },
    {
      label: 'Tensile Strength (MPa)',
      values: topCandidates.map((r) => r.mechanical_properties?.tensile_strength || 'Not available / unit not standardized')
    },
    {
      label: 'Bursting Strength',
      values: topCandidates.map((r) => r.mechanical_properties?.burst_strength || r.mechanical_properties?.burst_index || 'Not available')
    },
    {
      label: 'Sealability / Closure',
      values: topCandidates.map((r) => r.packaging_type.toLowerCase().includes('bottle') || r.packaging_type.toLowerCase().includes('jar') ? 'Hermetic Cap / Foil Seal' : 'Heat-Seal / Pouch Crimp')
    },
    {
      label: 'Compatibility Status',
      values: topCandidates.map((r) => r.compatibility?.status || 'Compatible')
    },
    {
      label: 'MAP Suitability',
      values: topCandidates.map((r) => r.map_suitability || 'Not available')
    },
    {
      label: 'Validated Benchmark (Source DB)',
      values: topCandidates.map((r) => {
        const exp = r.shelf_life_suitability?.expected_shelf_life_db;
        const hasValidExp = exp && !['nan', 'none', 'not specified', 'data unavailable', 'not available', ''].includes(String(exp).trim().toLowerCase());
        return hasValidExp ? exp : 'Not available in source database';
      })
    },
    {
      label: 'Shelf-Life Validation Status',
      values: topCandidates.map((r) => {
        const sl = r.shelf_life_suitability;
        if (sl?.additional_validation_required) {
          return (
            <div key={r.rank} className="flex flex-col gap-0.5 text-[11px] text-amber-800 bg-amber-50 p-1.5 rounded border border-amber-200">
              <span className="font-bold text-[10px] uppercase tracking-wider text-amber-700">Additional validation required</span>
              <span>Target: {sl.requested_days || 180} days</span>
              <span>Validated benchmark: {sl.expected_shelf_life_db}</span>
            </div>
          );
        }
        if (sl?.validation_status === 'FULLY_VALIDATED') {
          return (
            <span key={r.rank} className="text-emerald-700 font-semibold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
              Fully Validated ({sl.expected_shelf_life_db})
            </span>
          );
        }
        return (
          <span key={r.rank} className="text-slate-600 font-medium">
            {sl?.estimated_protection_level || 'Theoretical Barrier Fit'}
          </span>
        );
      })
    },
    {
      label: 'Sustainability / Recyclability',
      values: topCandidates.map((r) => r.sustainability?.recyclable || 'Not available')
    },
    {
      label: 'Technical Data Coverage',
      values: topCandidates.map((r) => `${r.technical_data_coverage} (${r.technical_coverage_pct}%)`)
    },
    {
      label: 'ML Suitability Score',
      values: topCandidates.map((r) => `${r.ml_prediction.score} / 100`)
    },
    {
      label: 'Final Suitability Score',
      isFinal: true,
      values: topCandidates.map((r) => `${r.suitability_score} / 100`)
    }
  ];

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-900/50 backdrop-blur-sm animate-in fade-in duration-200"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl max-w-6xl w-full max-h-[92vh] flex flex-col overflow-hidden">
        {/* Modal Header */}
        <div className="p-5 sm:p-6 border-b border-slate-100 flex items-start justify-between bg-slate-50/80">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-violet-100 text-violet-700 border border-violet-200/60">
                <ArrowLeftRight className="w-3.5 h-3.5" />
                Complete Candidate Comparison
              </span>
              <OriginBadge origin="DATABASE VALUE" />
            </div>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Side-by-Side Candidate Evaluation
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Complete technical, barrier, preservation, mechanical, and regulatory parameter comparison across all screened options.
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 transition-colors cursor-pointer"
            aria-label="Close Comparison"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body - Table with Sticky Header */}
        <div className="overflow-y-auto overflow-x-auto flex-1 bg-white">
          <table className="w-full text-left text-xs border-separate border-spacing-0 min-w-[720px]">
            <thead className="sticky top-0 z-20 shadow-xs">
              <tr>
                <th className="sticky top-0 z-20 py-3.5 px-5 sm:px-6 font-semibold text-slate-800 bg-slate-100 border-b-2 border-slate-200 w-1/4">
                  Property Specification
                </th>
                {topCandidates.map((r, i) => (
                  <th
                    key={i}
                    className={`sticky top-0 z-20 py-3.5 px-5 sm:px-6 font-bold w-1/4 border-b-2 border-slate-200 ${
                      i === 0 ? 'bg-violet-100 text-violet-950' : 'bg-slate-100 text-slate-900'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-1">
                      <span className="truncate">Option #{r.rank}</span>
                      {i === 0 ? (
                        <span className="inline-flex items-center gap-1 text-[10px] font-semibold bg-violet-600 text-white px-2 py-0.5 rounded-full shrink-0 shadow-xs">
                          <Award className="w-3 h-3" />
                          #1 Primary
                        </span>
                      ) : (
                        <span className="text-[10px] font-semibold bg-slate-200 text-slate-700 px-1.5 py-0.5 rounded shrink-0">
                          Alternative
                        </span>
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, idx) => (
                <tr
                  key={idx}
                  className={`hover:bg-slate-50/80 transition-colors ${
                    row.isFinal ? 'bg-emerald-50/50 font-bold' : ''
                  }`}
                >
                  <td className="py-3 px-5 sm:px-6 font-semibold text-slate-600 bg-slate-50/70 border-b border-slate-100">
                    {row.label}
                  </td>
                  {row.values.map((v, cIdx) => (
                    <td
                      key={cIdx}
                      className={`py-3 px-5 sm:px-6 border-b border-slate-100 ${
                        cIdx === 0 ? 'bg-violet-50/20' : ''
                      } ${row.isFinal ? 'text-emerald-900 font-extrabold text-sm' : 'text-slate-800'}`}
                    >
                      {getVal(v)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Modal Footer */}
        <div className="p-4 px-6 border-t border-slate-200/80 bg-slate-50/70 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-[11px] text-slate-500">
            *Unmeasured properties display <span className="italic font-medium">"Not available"</span> in strict compliance with data integrity protocols.
          </p>
          <button
            onClick={onClose}
            className="w-full sm:w-auto px-5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-semibold shadow-xs transition-colors cursor-pointer"
          >
            Close Comparison
          </button>
        </div>
      </div>
    </div>
  );
};
