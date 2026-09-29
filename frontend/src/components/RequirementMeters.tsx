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
    <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-7 shadow-sm mb-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 mb-6 gap-2">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold text-slate-900 tracking-tight">Food Requirement Performance Profile</h2>
            <OriginBadge origin="CALCULATED REQUIREMENT" />
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Estimated barrier and physical protection targets calculated from food properties and storage inputs.
          </p>
        </div>
        <div className="bg-amber-50/80 border border-amber-200/60 rounded-xl px-3 py-1.5 text-xs text-amber-900 flex items-center gap-1.5 self-start sm:self-auto">
          <Activity className="w-3.5 h-3.5 text-amber-600 flex-shrink-0" />
          <span>{disclaimer}</span>
        </div>
      </div>

      {/* Main Grid: Horizontal Bar Chart on Left, 2-Up 2-Down on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        {/* Left Side: Horizontal Bar Chart for the 4 Barrier Parameters */}
        <div className="lg:col-span-6 bg-slate-50/50 rounded-2xl border border-slate-200/80 p-5 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-slate-200/70 mb-4">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-violet-600" />
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                Barrier & Structural Targets
              </h3>
            </div>
            <span className="text-[10px] font-semibold text-slate-500 bg-white px-2 py-0.5 rounded-full border border-slate-200">
              Normalized (0.0 - 1.0)
            </span>
          </div>

          <div className="space-y-4 flex-1 flex flex-col justify-around">
            {barrierMetrics.map((metric) => (
              <div
                key={metric.name}
                className="p-3 bg-white rounded-xl border border-slate-200/70 shadow-2xs hover:shadow-xs transition-shadow"
              >
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-2">
                    <span className={`p-1 rounded-lg ${metric.bgColor}`}>
                      <metric.icon className={`w-3.5 h-3.5 ${metric.iconColor}`} />
                    </span>
                    <span className="text-xs font-bold text-slate-900">{metric.name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-semibold text-slate-700 bg-slate-100 px-2 py-0.5 rounded-md">
                      {metric.level}
                    </span>
                    <span className="text-xs font-mono font-bold text-slate-900 min-w-[50px] text-right">
                      {metric.score} <span className="text-[10px] text-slate-400 font-normal">/ 1.0</span>
                    </span>
                  </div>
                </div>

                {/* Horizontal Bar Chart Track & Fill */}
                <div className="relative w-full bg-slate-100 h-2.5 rounded-full overflow-hidden mb-1.5">
                  <div
                    className={`h-full rounded-full bg-gradient-to-r ${metric.barColor} transition-all duration-700 ease-out`}
                    style={{ width: `${Math.min(Math.max((metric.score || 0.5) * 100, 5), 100)}%` }}
                  />
                </div>

                {/* Description */}
                <p className="text-[11px] text-slate-500 leading-relaxed">
                  {metric.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Right Side: The rest 4 as 2 Up and 2 Down */}
        <div className="lg:col-span-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* Top 1 (Up): MAP / Gas Environment */}
          <div className="p-4 bg-slate-50/60 rounded-xl border border-slate-200/80 flex flex-col justify-between hover:bg-slate-50 transition-colors">
            <div>
              <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">
                <Activity className="w-3.5 h-3.5 text-violet-600" />
                <span>MAP / Gas Environment</span>
              </div>
              <h4 className="text-xs font-bold text-slate-900 mb-1">
                {map_gas_requirement.level}
              </h4>
              <p className="text-[11px] text-slate-600 leading-relaxed">
                {map_gas_requirement.description}
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-slate-200/60 flex items-center justify-between text-[10px] text-slate-400">
              <span>Environment Spec</span>
              <span className="font-semibold text-slate-600">Controlled Atmosphere</span>
            </div>
          </div>

          {/* Top 2 (Up): Shelf Life Horizon */}
          <div className="p-4 bg-slate-50/60 rounded-xl border border-slate-200/80 flex flex-col justify-between hover:bg-slate-50 transition-colors">
            <div>
              <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">
                <Clock className="w-3.5 h-3.5 text-amber-600" />
                <span>Shelf Life Horizon</span>
              </div>
              <h4 className="text-xs font-bold text-slate-900 mb-1">
                {shelf_life_protection.level}
              </h4>
              <p className="text-[11px] text-slate-600 leading-relaxed">
                {shelf_life_protection.description}
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-slate-200/60 flex items-center justify-between text-[10px] text-slate-400">
              <span>Target Longevity</span>
              <span className="font-semibold text-slate-600">Preservation Target</span>
            </div>
          </div>

          {/* Bottom 1 (Down): Compatibility Mandate */}
          <div className="p-4 bg-slate-50/60 rounded-xl border border-slate-200/80 flex flex-col justify-between hover:bg-slate-50 transition-colors">
            <div>
              <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>Compatibility Mandate</span>
              </div>
              <h4 className="text-xs font-bold text-slate-900 mb-1">
                FSSAI Safety Rules
              </h4>
              <p className="text-[11px] text-slate-600 leading-relaxed">
                {compatibility_requirement.notes?.[0] || 'Standard direct food-contact migration compliance.'}
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-slate-200/60 flex items-center justify-between text-[10px] text-slate-400">
              <span>Regulatory Standard</span>
              <span className="font-semibold text-emerald-700">FSSAI 2018</span>
            </div>
          </div>

          {/* Bottom 2 (Down): Sustainability Guideline */}
          <div className="p-4 bg-slate-50/60 rounded-xl border border-slate-200/80 flex flex-col justify-between hover:bg-slate-50 transition-colors">
            <div>
              <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">
                <Leaf className="w-3.5 h-3.5 text-teal-600" />
                <span>Sustainability Guideline</span>
              </div>
              <h4 className="text-xs font-bold text-slate-900 mb-1">
                {sustainability_requirement.level}
              </h4>
              <p className="text-[11px] text-slate-600 leading-relaxed">
                {sustainability_requirement.description}
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-slate-200/60 flex items-center justify-between text-[10px] text-slate-400">
              <span>EPR Mandate</span>
              <span className="font-semibold text-teal-700">CPCB Guidelines</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
