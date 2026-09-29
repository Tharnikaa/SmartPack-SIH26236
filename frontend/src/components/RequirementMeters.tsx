import React from 'react';
import { CalculatedRequirements } from '../types';
import { OriginBadge } from './OriginBadge';
import { 
  Wind, Droplets, ShieldCheck, Lock, Activity, 
  Clock, CheckCircle2, Leaf, BarChart3 
} from 'lucide-react';

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

  const barrierMetrics = [
    {
      name: 'Oxygen Barrier',
      icon: Wind,
      iconColor: 'text-purple-600',
      barColor: 'from-purple-500 to-indigo-600',
      bgColor: 'bg-purple-50',
      score: oxygen_requirement.score ?? 0.85,
      level: oxygen_requirement.level || 'High',
      description: oxygen_requirement.description
    },
    {
      name: 'Moisture Barrier',
      icon: Droplets,
      iconColor: 'text-blue-600',
      barColor: 'from-blue-500 to-cyan-600',
      bgColor: 'bg-blue-50',
      score: moisture_requirement.score ?? 0.8,
      level: moisture_requirement.level || 'High',
      description: moisture_requirement.description
    },
    {
      name: 'Mechanical Robustness',
      icon: ShieldCheck,
      iconColor: 'text-emerald-600',
      barColor: 'from-emerald-500 to-teal-600',
      bgColor: 'bg-emerald-50',
      score: mechanical_requirement.score ?? 0.5,
      level: mechanical_requirement.level || 'Medium',
      description: mechanical_requirement.description
    },
    {
      name: 'Seal Integrity',
      icon: Lock,
      iconColor: 'text-rose-600',
      barColor: 'from-rose-500 to-pink-600',
      bgColor: 'bg-rose-50',
      score: sealability_requirement.score ?? 0.8,
      level: sealability_requirement.level || 'High (Hermetic)',
      description: sealability_requirement.description
    }
  ];

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-3.5 sm:p-4 shadow-sm mb-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-2.5 border-b border-slate-100 mb-3 gap-1.5">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-sm sm:text-base font-bold text-slate-900 tracking-tight">Food Requirement Performance Profile</h2>
            <OriginBadge origin="CALCULATED REQUIREMENT" />
          </div>
          <p className="text-[11px] text-slate-500 mt-0.5">
            Estimated barrier and physical protection targets calculated from food properties and storage inputs.
          </p>
        </div>
        <div className="bg-amber-50/80 border border-amber-200/60 rounded-lg px-2 py-0.5 text-[11px] text-amber-900 flex items-center gap-1 self-start sm:self-auto shrink-0">
          <Activity className="w-3 h-3 text-amber-600 flex-shrink-0" />
          <span>{disclaimer}</span>
        </div>
      </div>

      {/* Main Grid: Compact Horizontal Bar Chart on Left, Compact 2-Up 2-Down on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-3 items-start">
        {/* Left Side: Slim Horizontal Bar Chart for the 4 Barrier Parameters */}
        <div className="lg:col-span-6 bg-slate-50/60 rounded-xl border border-slate-200/70 p-3">
          <div className="flex items-center justify-between pb-1.5 border-b border-slate-200/60 mb-2">
            <div className="flex items-center gap-1.5">
              <BarChart3 className="w-3.5 h-3.5 text-violet-600" />
              <h3 className="text-[11px] font-bold uppercase tracking-wider text-slate-700">
                Barrier & Structural Targets
              </h3>
            </div>
            <span className="text-[9.5px] font-semibold text-slate-500 bg-white px-1.5 py-0.2 rounded border border-slate-200">
              Normalized (0.0 - 1.0)
            </span>
          </div>

          <div className="space-y-1.5">
            {barrierMetrics.map((metric) => (
              <div
                key={metric.name}
                className="py-1.5 px-2.5 bg-white rounded-lg border border-slate-200/70 shadow-2xs hover:shadow-xs transition-shadow"
              >
                <div className="flex items-center justify-between gap-1 mb-0.5">
                  <div className="flex items-center gap-1.5 min-w-0">
                    <span className={`p-0.5 rounded ${metric.bgColor}`}>
                      <metric.icon className={`w-3 h-3 ${metric.iconColor}`} />
                    </span>
                    <span className="text-[11px] font-bold text-slate-900 truncate">{metric.name}</span>
                  </div>
                  <div className="flex items-center gap-1.5 shrink-0">
                    <span className="text-[9.5px] font-semibold text-slate-700 bg-slate-100 px-1 py-0.2 rounded">
                      {metric.level}
                    </span>
                    <span className="text-[11px] font-mono font-bold text-slate-900 min-w-[42px] text-right">
                      {metric.score} <span className="text-[9.5px] text-slate-400 font-normal">/ 1.0</span>
                    </span>
                  </div>
                </div>

                {/* Horizontal Bar Track & Fill */}
                <div className="relative w-full bg-slate-100 h-1.5 rounded-full overflow-hidden my-0.5">
                  <div
                    className={`h-full rounded-full bg-gradient-to-r ${metric.barColor} transition-all duration-500 ease-out`}
                    style={{ width: `${Math.min(Math.max((metric.score || 0.5) * 100, 5), 100)}%` }}
                  />
                </div>

                {/* 1-Line Truncated Description with Title Tooltip */}
                <p className="text-[10px] text-slate-400 truncate leading-tight" title={metric.description}>
                  {metric.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Right Side: Compact 2 Up and 2 Down */}
        <div className="lg:col-span-6 grid grid-cols-1 sm:grid-cols-2 gap-2">
          {/* Top 1 (Up): MAP / Gas Environment */}
          <div className="p-2.5 bg-slate-50/70 rounded-xl border border-slate-200/70 flex flex-col justify-between hover:bg-slate-50 transition-colors">
            <div>
              <div className="flex items-center gap-1 text-[9.5px] font-bold text-slate-500 uppercase tracking-wider mb-0.5">
                <Activity className="w-3 h-3 text-violet-600" />
                <span>MAP / Gas Environment</span>
              </div>
              <h4 className="text-[11px] font-bold text-slate-900 mb-0.5">
                {map_gas_requirement.level}
              </h4>
              <p className="text-[10px] text-slate-600 line-clamp-2 leading-snug" title={map_gas_requirement.description}>
                {map_gas_requirement.description}
              </p>
            </div>
          </div>

          {/* Top 2 (Up): Shelf Life Horizon */}
          <div className="p-2.5 bg-slate-50/70 rounded-xl border border-slate-200/70 flex flex-col justify-between hover:bg-slate-50 transition-colors">
            <div>
              <div className="flex items-center gap-1 text-[9.5px] font-bold text-slate-500 uppercase tracking-wider mb-0.5">
                <Clock className="w-3 h-3 text-amber-600" />
                <span>Shelf Life Horizon</span>
              </div>
              <h4 className="text-[11px] font-bold text-slate-900 mb-0.5">
                {shelf_life_protection.level}
              </h4>
              <p className="text-[10px] text-slate-600 line-clamp-2 leading-snug" title={shelf_life_protection.description}>
                {shelf_life_protection.description}
              </p>
            </div>
          </div>

          {/* Bottom 1 (Down): Compatibility Mandate */}
          <div className="p-2.5 bg-slate-50/70 rounded-xl border border-slate-200/70 flex flex-col justify-between hover:bg-slate-50 transition-colors">
            <div>
              <div className="flex items-center gap-1 text-[9.5px] font-bold text-slate-500 uppercase tracking-wider mb-0.5">
                <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                <span>Compatibility Mandate</span>
              </div>
              <h4 className="text-[11px] font-bold text-slate-900 mb-0.5">
                FSSAI Safety Rules
              </h4>
              <p className="text-[10px] text-slate-600 line-clamp-2 leading-snug" title={compatibility_requirement.notes?.[0] || 'Standard direct food-contact migration compliance.'}>
                {compatibility_requirement.notes?.[0] || 'Standard direct food-contact migration compliance.'}
              </p>
            </div>
          </div>

          {/* Bottom 2 (Down): Sustainability Guideline */}
          <div className="p-2.5 bg-slate-50/70 rounded-xl border border-slate-200/70 flex flex-col justify-between hover:bg-slate-50 transition-colors">
            <div>
              <div className="flex items-center gap-1 text-[9.5px] font-bold text-slate-500 uppercase tracking-wider mb-0.5">
                <Leaf className="w-3 h-3 text-teal-600" />
                <span>Sustainability Guideline</span>
              </div>
              <h4 className="text-[11px] font-bold text-slate-900 mb-0.5">
                {sustainability_requirement.level}
              </h4>
              <p className="text-[10px] text-slate-600 line-clamp-2 leading-snug" title={sustainability_requirement.description}>
                {sustainability_requirement.description}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
