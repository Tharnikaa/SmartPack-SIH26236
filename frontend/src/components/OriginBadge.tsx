import React from 'react';

interface Props {
  origin: 'DATABASE VALUE' | 'CALCULATED REQUIREMENT' | 'ML PREDICTION' | 'DERIVED SCORE' | 'REFERENCE VALUE (published literature)' | string;
  size?: 'sm' | 'xs';
}

export const OriginBadge: React.FC<Props> = ({ origin, size = 'xs' }) => {
  const normalized = origin.toUpperCase();

  let colorClasses = 'bg-slate-100 text-slate-700 border-slate-200';
  if (normalized.includes('DATABASE')) {
    colorClasses = 'bg-blue-50 text-blue-700 border-blue-200';
  } else if (normalized.includes('REFERENCE')) {
    colorClasses = 'bg-teal-50 text-teal-800 border-teal-200';
  } else if (normalized.includes('CALCULATED')) {
    colorClasses = 'bg-amber-50 text-amber-800 border-amber-200';
  } else if (normalized.includes('ML')) {
    colorClasses = 'bg-purple-50 text-purple-700 border-purple-200';
  } else if (normalized.includes('DERIVED')) {
    colorClasses = 'bg-emerald-50 text-emerald-800 border-emerald-200';
  }

  const sizeClasses = size === 'xs' ? 'text-[10px] px-1.5 py-0.5' : 'text-xs px-2 py-1';

  return (
    <span
      className={`inline-flex items-center font-mono font-medium rounded border uppercase tracking-wider ${sizeClasses} ${colorClasses}`}
      title={`Data Provenance: ${origin}`}
    >
      {origin}
    </span>
  );
};
