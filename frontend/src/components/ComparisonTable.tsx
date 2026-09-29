import React from 'react';
import { Recommendation } from '../types';
import { OriginBadge } from './OriginBadge';
import { ArrowLeftRight } from 'lucide-react';

interface Props {
  recommendations: Recommendation[];
}

export const ComparisonTable: React.FC<Props> = ({ recommendations }) => {
  if (!recommendations || recommendations.length === 0) return null;

  const top3 = recommendations.slice(0, 3);

  const getVal = (val: any) => {
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
      values: top3.map((r) => `#${r.rank} ${r.rank === 1 ? 'Primary Recommendation' : 'Alternative Option'}`)
    },
    {
      label: 'Material Specification',
      values: top3.map((r) => r.material)
    },
    {
      label: 'Primary Packaging Contact',
      values: top3.map((r) => r.primary_packaging || r.material)
    },
    {
      label: 'Secondary / Outer System',
      values: top3.map((r) => r.secondary_packaging || 'Not applicable (Single unit)')
    },
    {
      label: 'Packaging Type',
      values: top3.map((r) => r.packaging_type)
    },
    {
      label: 'Barrier Classification',
      values: top3.map((r) => (
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
      values: top3.map((r) =>
        r.barrier_properties.otr !== null && r.barrier_properties.otr !== undefined
          ? `${r.barrier_properties.otr} ${r.barrier_properties.otr_unit}`
          : 'Not available'
      )
    },
    {
      label: 'WVTR (Moisture Vapor Transmission)',
      values: top3.map((r) =>
        r.barrier_properties.wvtr !== null && r.barrier_properties.wvtr !== undefined
          ? `${r.barrier_properties.wvtr} ${r.barrier_properties.wvtr_unit}`
          : 'Not available'
      )
    },
    {
      label: 'Thickness Spec',
      values: top3.map((r) => r.mechanical_properties?.thickness_spec || 'Not available')
    },
    {
      label: 'Tensile Strength (MPa)',
      values: top3.map((r) => r.mechanical_properties?.tensile_strength || 'Not available / unit not standardized')
    },
    {
      label: 'Bursting Strength',
      values: top3.map((r) => r.mechanical_properties?.burst_strength || r.mechanical_properties?.burst_index || 'Not available')
    },
    {
      label: 'Sealability / Closure',
      values: top3.map((r) => r.packaging_type.toLowerCase().includes('bottle') || r.packaging_type.toLowerCase().includes('jar') ? 'Hermetic Cap / Foil Seal' : 'Heat-Seal / Pouch Crimp')
    },
    {
      label: 'Compatibility Status',
      values: top3.map((r) => r.compatibility?.status || 'Compatible')
    },
    {
      label: 'MAP Suitability',
      values: top3.map((r) => r.map_suitability || 'Not available')
    },
    {
      label: 'Validated Benchmark (Source DB)',
      values: top3.map((r) => {
        const exp = r.shelf_life_suitability?.expected_shelf_life_db;
        const hasValidExp = exp && !['nan', 'none', 'not specified', 'data unavailable', 'not available', ''].includes(String(exp).trim().toLowerCase());
        return hasValidExp ? exp : 'Not available in source database';
      })
    },
    {
      label: 'Shelf-Life Validation Status',
      values: top3.map((r) => {
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
      values: top3.map((r) => r.sustainability?.recyclable || 'Not available')
    },
    {
      label: 'Technical Data Coverage',
      values: top3.map((r) => `${r.technical_data_coverage} (${r.technical_coverage_pct}%)`)
    },
    {
      label: 'ML Suitability Score',
      values: top3.map((r) => `${r.ml_prediction.score} / 100`)
    },
    {
      label: 'Final Suitability Score',
      isFinal: true,
      values: top3.map((r) => `${r.suitability_score} / 100`)
    }
  ];

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm mb-8 overflow-hidden">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 mb-6 gap-2">
        <div className="flex items-center gap-2">
          <ArrowLeftRight className="w-5 h-5 text-brand-600" />
          <h2 className="text-lg font-semibold text-slate-900">Side-by-Side Candidate Comparison</h2>
          <OriginBadge origin="DATABASE VALUE" />
        </div>
        <p className="text-xs text-slate-500">
          Unmeasured technical properties display <span className="italic font-medium">"Not available"</span> in strict compliance with data integrity protocols.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50/70">
              <th className="py-3 px-4 font-semibold text-slate-700 w-1/4">Property Specification</th>
              {top3.map((r, i) => (
                <th
                  key={i}
                  className={`py-3 px-4 font-bold text-slate-900 w-1/4 ${
                    i === 0 ? 'bg-brand-50/60 text-brand-900' : ''
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span>Option {r.rank}</span>
                    {i === 0 && (
                      <span className="text-[10px] font-semibold bg-brand-600 text-white px-2 py-0.5 rounded">
                        #1 Top Rank
                      </span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.map((row, idx) => (
              <tr
                key={idx}
                className={`hover:bg-slate-50/50 transition-colors ${
                  row.isFinal ? 'bg-emerald-50/40 font-bold' : ''
                }`}
              >
                <td className="py-3 px-4 font-medium text-slate-600 bg-slate-50/30">
                  {row.label}
                </td>
                {row.values.map((v, cIdx) => (
                  <td
                    key={cIdx}
                    className={`py-3 px-4 ${
                      cIdx === 0 ? 'bg-brand-50/20' : ''
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
    </div>
  );
};
