import React from 'react';
import { ShieldCheck, ShieldAlert, Shield } from 'lucide-react';

interface Props {
  rating: string;
  pct?: number;
}

export const CoverageBadge: React.FC<Props> = ({ rating, pct }) => {
  let bg = 'bg-slate-50 border-slate-200 text-slate-700';
  let Icon = Shield;

  if (rating.toLowerCase().includes('high')) {
    bg = 'bg-emerald-50 border-emerald-200 text-emerald-800';
    Icon = ShieldCheck;
  } else if (rating.toLowerCase().includes('medium')) {
    bg = 'bg-amber-50 border-amber-200 text-amber-800';
    Icon = Shield;
  } else if (rating.toLowerCase().includes('low') || rating.toLowerCase().includes('incomplete')) {
    bg = 'bg-rose-50 border-rose-200 text-rose-800';
    Icon = ShieldAlert;
  }

  return (
    <div
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full border text-xs font-medium ${bg}`}
      title="Availability of verified technical packaging properties in source datasets"
    >
      <Icon className="w-3.5 h-3.5" />
      <span>{rating}</span>
      {pct !== undefined && <span className="opacity-75">({pct}%)</span>}
    </div>
  );
};
