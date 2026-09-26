import React from 'react';
import { CalculatedRequirements } from '../types';
import { OriginBadge } from './OriginBadge';
import { Wind, Droplets, ShieldCheck, Lock, Activity, Clock, CheckCircle2, Leaf } from 'lucide-react';

interface Props {
  requirements: CalculatedRequirements;
}

export const RequirementMeters: React.FC<Props> = ({ requirements }) => {
  const {
    disclaimer,
    oxygen_requirement,
    moisture_requirement,
    mechanical_requirement,
    sealability_requirement,
    map_gas_requirement,
    shelf_life_protection,
    compatibility_requirement,
    sustainability_requirement
  } = requirements;

  const getMeterColor = (score: number = 0.5) => {
    if (score >= 0.7) return 'bg-rose-500';
    if (score >= 0.4) return 'bg-amber-500';
    return 'bg-emerald-500';
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm mb-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 mb-6 gap-2">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-semibold text-slate-900">Food Requirement Performance Profile</h2>
            <OriginBadge origin="CALCULATED REQUIREMENT" />
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Estimated barrier and physical protection targets calculated from food properties and storage inputs.
          </p>
        </div>
        <div className="bg-amber-50/80 border border-amber-200/60 rounded-lg px-3 py-1.5 text-xs text-amber-900 flex items-center gap-1.5">
          <Activity className="w-3.5 h-3.5 text-amber-600 flex-shrink-0" />
          <span>{disclaimer}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Oxygen Barrier */}
        <div className="bg-slate-50/70 rounded-xl p-4 border border-slate-200/60 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                <Wind className="w-4 h-4 text-purple-600" />
                Oxygen Barrier
              </span>
              <span className="text-xs font-bold text-slate-800">{oxygen_requirement.level}</span>
            </div>
            <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden mb-2">
              <div
                className={`h-full rounded-full transition-all duration-500 ${getMeterColor(oxygen_requirement.score)}`}
                style={{ width: `${(oxygen_requirement.score || 0.5) * 100}%` }}
              />
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">{oxygen_requirement.description}</p>
          </div>
          <div className="mt-3 pt-2 border-t border-slate-200/40 flex justify-between items-center text-[11px] text-slate-400">
            <span>Calculated Score</span>
            <span className="font-mono font-medium text-slate-600">{oxygen_requirement.score} / 1.0</span>
          </div>
        </div>

        {/* Moisture Barrier */}
        <div className="bg-slate-50/70 rounded-xl p-4 border border-slate-200/60 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                <Droplets className="w-4 h-4 text-blue-600" />
                Moisture Barrier
              </span>
              <span className="text-xs font-bold text-slate-800">{moisture_requirement.level}</span>
            </div>
            <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden mb-2">
              <div
                className={`h-full rounded-full transition-all duration-500 ${getMeterColor(moisture_requirement.score)}`}
                style={{ width: `${(moisture_requirement.score || 0.5) * 100}%` }}
              />
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">{moisture_requirement.description}</p>
          </div>
          <div className="mt-3 pt-2 border-t border-slate-200/40 flex justify-between items-center text-[11px] text-slate-400">
            <span>Calculated Score</span>
            <span className="font-mono font-medium text-slate-600">{moisture_requirement.score} / 1.0</span>
          </div>
        </div>

        {/* Mechanical Protection */}
        <div className="bg-slate-50/70 rounded-xl p-4 border border-slate-200/60 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                Mechanical Robustness
              </span>
              <span className="text-xs font-bold text-slate-800">{mechanical_requirement.level}</span>
            </div>
            <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden mb-2">
              <div
                className={`h-full rounded-full transition-all duration-500 ${getMeterColor(mechanical_requirement.score)}`}
                style={{ width: `${(mechanical_requirement.score || 0.5) * 100}%` }}
              />
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">{mechanical_requirement.description}</p>
          </div>
          <div className="mt-3 pt-2 border-t border-slate-200/40 flex justify-between items-center text-[11px] text-slate-400">
            <span>Calculated Score</span>
            <span className="font-mono font-medium text-slate-600">{mechanical_requirement.score} / 1.0</span>
          </div>
        </div>

        {/* Sealability */}
        <div className="bg-slate-50/70 rounded-xl p-4 border border-slate-200/60 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                <Lock className="w-4 h-4 text-amber-600" />
                Seal Integrity
              </span>
              <span className="text-xs font-bold text-slate-800">{sealability_requirement.level}</span>
            </div>
            <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden mb-2">
              <div
                className={`h-full rounded-full transition-all duration-500 ${getMeterColor(sealability_requirement.score)}`}
                style={{ width: `${(sealability_requirement.score || 0.5) * 100}%` }}
              />
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">{sealability_requirement.description}</p>
          </div>
          <div className="mt-3 pt-2 border-t border-slate-200/40 flex justify-between items-center text-[11px] text-slate-400">
            <span>Calculated Score</span>
            <span className="font-mono font-medium text-slate-600">{sealability_requirement.score} / 1.0</span>
          </div>
        </div>
      </div>

      {/* Secondary Requirements Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-4 pt-4 border-t border-slate-100">
        <div className="p-3 bg-white rounded-lg border border-slate-200/80">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1 flex items-center gap-1">
            <Activity className="w-3.5 h-3.5 text-slate-400" /> MAP / Gas Environment
          </span>
          <span className="text-xs font-semibold text-slate-900 block mb-1">{map_gas_requirement.level}</span>
          <p className="text-[11px] text-slate-500">{map_gas_requirement.description}</p>
        </div>

        <div className="p-3 bg-white rounded-lg border border-slate-200/80">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1 flex items-center gap-1">
            <Clock className="w-3.5 h-3.5 text-slate-400" /> Shelf Life Horizon
          </span>
          <span className="text-xs font-semibold text-slate-900 block mb-1">{shelf_life_protection.level}</span>
          <p className="text-[11px] text-slate-500">{shelf_life_protection.description}</p>
        </div>

        <div className="p-3 bg-white rounded-lg border border-slate-200/80">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1 flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5 text-slate-400" /> Compatibility Mandate
          </span>
          <span className="text-xs font-semibold text-slate-900 block mb-1">FSSAI Safety Rules</span>
          <p className="text-[11px] text-slate-500">
            {compatibility_requirement.notes?.[0] || 'Standard direct food-contact migration compliance.'}
          </p>
        </div>

        <div className="p-3 bg-white rounded-lg border border-slate-200/80">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1 flex items-center gap-1">
            <Leaf className="w-3.5 h-3.5 text-slate-400" /> Sustainability Guideline
          </span>
          <span className="text-xs font-semibold text-slate-900 block mb-1">{sustainability_requirement.level}</span>
          <p className="text-[11px] text-slate-500">{sustainability_requirement.description}</p>
        </div>
      </div>
    </div>
  );
};
