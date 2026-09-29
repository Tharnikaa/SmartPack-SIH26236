import React, { useState } from 'react';
import { FileText, Database, ShieldAlert, Cpu } from 'lucide-react';
import { OriginBadge } from './OriginBadge';

export const ModelCardView: React.FC = () => {
  const [activeDoc, setActiveDoc] = useState<'model_card' | 'inspection' | 'dictionary' | 'limitations'>('model_card');

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-in fade-in duration-200">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Scientific Documentation & Model Audit</h1>
        <p className="text-xs text-slate-500 mt-1">
          Complete transparent disclosure of training methodology, dataset inspection, schemas, and limitations.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-200 mb-6 gap-2">
        <button
          onClick={() => setActiveDoc('model_card')}
          className={`pb-3 px-4 text-xs font-semibold border-b-2 flex items-center gap-1.5 transition-colors ${
            activeDoc === 'model_card'
              ? 'border-brand-600 text-brand-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Cpu className="w-4 h-4" />
          <span>Model Card (docs/MODEL_CARD.md)</span>
        </button>
        <button
          onClick={() => setActiveDoc('inspection')}
          className={`pb-3 px-4 text-xs font-semibold border-b-2 flex items-center gap-1.5 transition-colors ${
            activeDoc === 'inspection'
              ? 'border-brand-600 text-brand-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Database className="w-4 h-4" />
          <span>Dataset Inspection Report</span>
        </button>
        <button
          onClick={() => setActiveDoc('dictionary')}
          className={`pb-3 px-4 text-xs font-semibold border-b-2 flex items-center gap-1.5 transition-colors ${
            activeDoc === 'dictionary'
              ? 'border-brand-600 text-brand-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Data Dictionary</span>
        </button>
        <button
          onClick={() => setActiveDoc('limitations')}
          className={`pb-3 px-4 text-xs font-semibold border-b-2 flex items-center gap-1.5 transition-colors ${
            activeDoc === 'limitations'
              ? 'border-brand-600 text-brand-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <ShieldAlert className="w-4 h-4" />
          <span>Scientific Limitations</span>
        </button>
      </div>

      {/* Document View Container */}
      <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm prose prose-slate max-w-none text-xs leading-relaxed">
        {activeDoc === 'model_card' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <h2 className="text-lg font-bold text-slate-900 m-0">Wrap Up! Hybrid Suitability Model</h2>
              <OriginBadge origin="ML PREDICTION" />
            </div>

            <div className="p-4 rounded-xl bg-amber-50/80 border border-amber-200 text-amber-900">
              <strong className="block mb-1 text-xs">Section 12 Transparency Disclosure:</strong>
              <p className="text-[11px] m-0">
                The ML model trains on a transparent prototype target (<code>suitability_label</code>) derived from scientific requirement satisfaction rules, FSSAI Schedule IV regulatory recommendations, and BIS standards.
                <strong> It is NOT an experimentally measured laboratory ground-truth label.</strong>
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 not-prose">
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider block">Model Architecture</span>
                <span className="text-sm font-bold text-slate-900 block mt-1">Random Forest Regressor & Classifier</span>
                <span className="text-[11px] text-slate-500">100 estimators, max depth 8</span>
              </div>
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider block">Regression Performance</span>
                <span className="text-sm font-bold text-emerald-700 block mt-1">MAE: 0.0348 | R²: 0.9187</span>
                <span className="text-[11px] text-slate-500">RMSE: 0.0448 (Held-out 25% test set)</span>
              </div>
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider block">Classification Accuracy</span>
                <span className="text-sm font-bold text-emerald-700 block mt-1">Accuracy: 96.8% | F1: 0.966</span>
                <span className="text-[11px] text-slate-500">Precision: 0.954 | Recall: 0.978</span>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-bold text-slate-900 mb-2">Input Features (18 Tabular Attributes)</h3>
              <p className="text-slate-600 text-xs">
                Combines food composition metrics (ICMR IFCT 2017: moisture, fat, protein), calculated requirement scores (oxygen, moisture, mechanical, sealability), packaging structural classifications (rigid, laminate, glass/metal), and explicit data-completeness flags (measured WVTR / OTR present).
              </p>
            </div>
          </div>
        )}

        {activeDoc === 'inspection' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <h2 className="text-lg font-bold text-slate-900 m-0">Dataset Inspection Report Summary</h2>
              <OriginBadge origin="DATABASE VALUE" />
            </div>
            <p className="text-slate-600">
              Across all 15 supplied CSV files, the data inventory confirms:
            </p>
            <ul className="space-y-1.5 text-slate-700">
              <li><strong>01_food_dataset.csv:</strong> 496 foods from ICMR IFCT 2017 with exact analytical moisture and fat.</li>
              <li><strong>14_recommended_packaging.csv:</strong> 102 authoritative candidate mappings (93 from FSSAI Schedule IV).</li>
              <li><strong>06_packaging_material_dataset.csv:</strong> 26 materials cataloged under BIS standards.</li>
              <li><strong>08_barrier_properties_dataset.csv:</strong> 2 real measured WVTR rows for Cellulose Film (IS 5012:1987). OTR is null across raw CSVs.</li>
              <li><strong>09_food_packaging_compatibility_MERGED.csv:</strong> 11 curated compatibility rows.</li>
              <li><strong>13_regulatory_rules.csv:</strong> 20 regulatory standards including IS 14534 prohibition of recycled plastic for food contact.</li>
            </ul>
          </div>
        )}

        {activeDoc === 'dictionary' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <h2 className="text-lg font-bold text-slate-900 m-0">Unified Project Data Dictionary</h2>
              <OriginBadge origin="DATABASE VALUE" />
            </div>
            <p className="text-slate-600">
              Standardized physical units and ML role designations:
            </p>
            <div className="not-prose overflow-x-auto">
              <table className="w-full text-xs text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50 text-slate-700 font-semibold">
                    <th className="py-2.5 px-3">Field</th>
                    <th className="py-2.5 px-3">Physical Unit</th>
                    <th className="py-2.5 px-3">Dataset Source</th>
                    <th className="py-2.5 px-3">Pipeline Role</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
                  <tr><td className="py-2 px-3 font-sans">moisture_content</td><td className="py-2 px-3">g/100g (%)</td><td className="py-2 px-3 font-sans">01_food_dataset.csv</td><td className="py-2 px-3 text-purple-700">Input Feature</td></tr>
                  <tr><td className="py-2 px-3 font-sans">fat_content</td><td className="py-2 px-3">g/100g</td><td className="py-2 px-3 font-sans">01_food_dataset.csv</td><td className="py-2 px-3 text-purple-700">Input Feature</td></tr>
                  <tr><td className="py-2 px-3 font-sans">water_vapour_transmission_rate</td><td className="py-2 px-3">g/m²/24h</td><td className="py-2 px-3 font-sans">08_barrier_properties_dataset.csv</td><td className="py-2 px-3 text-blue-700">Physical Property</td></tr>
                  <tr><td className="py-2 px-3 font-sans">oxygen_transmission_rate</td><td className="py-2 px-3">cc/m²/day</td><td className="py-2 px-3 font-sans">08_barrier_properties_dataset.csv</td><td className="py-2 px-3 text-slate-400">Unmeasured in DB</td></tr>
                  <tr><td className="py-2 px-3 font-sans">overall_migration_limit</td><td className="py-2 px-3">mg/kg (IS 9845)</td><td className="py-2 px-3 font-sans">13_regulatory_rules.csv</td><td className="py-2 px-3 text-rose-700">Hard Safety Filter</td></tr>
                  <tr><td className="py-2 px-3 font-sans">suitability_score</td><td className="py-2 px-3">0 - 100 Index</td><td className="py-2 px-3 font-sans">Hybrid Scoring Engine</td><td className="py-2 px-3 text-emerald-700">Final Ranking</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeDoc === 'limitations' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <h2 className="text-lg font-bold text-slate-900 m-0">Scientific Limitations & Boundaries</h2>
              <OriginBadge origin="CALCULATED REQUIREMENT" />
            </div>
            <div className="space-y-3 text-slate-700">
              <p>
                <strong>1. Decision Support Prototype:</strong> SmartPack is a decision-support prototype. It is not an analytical laboratory certification system and does not replace commercial migration testing under IS 9845.
              </p>
              <p>
                <strong>2. Absence of Fabricated Technical Values:</strong> In strict compliance with Prompt Rule #1 and #36, missing OTR and WVTR values are represented as <em>"Data unavailable in source database"</em> and never fabricated with random numbers.
              </p>
              <p>
                <strong>3. Shelf Life Distinction:</strong> The system strictly distinguishes user-requested shelf life from candidate protection suitability. Exact commercial shelf life requires empirical real-time or accelerated shelf-life testing.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
