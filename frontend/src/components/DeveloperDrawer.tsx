import React, { useState, useEffect } from 'react';
import { DebugInfo, MLStatusResponse } from '../types';
import { fetchMLStatus, triggerMLTrain, fetchWeights, updateWeights } from '../services/api';
import { Terminal, RefreshCw, Sliders, CheckCircle, X } from 'lucide-react';

interface Props {
  debugInfo?: DebugInfo;
  isOpen: boolean;
  onClose: () => void;
}

export const DeveloperDrawer: React.FC<Props> = ({ debugInfo, isOpen, onClose }) => {
  const [mlStatus, setMlStatus] = useState<MLStatusResponse | null>(null);
  const [weights, setWeights] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const [mStatus, wData] = await Promise.all([fetchMLStatus(), fetchWeights()]);
      setMlStatus(mStatus);
      setWeights(wData);
    } catch (err) {
      console.error('Failed to load dev data:', err);
    }
  };

  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen]);

  const handleRetrain = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const res = await triggerMLTrain();
      setMessage(`Model successfully trained! Accuracy: ${(res.metrics?.classification?.accuracy * 100).toFixed(1)}%`);
      await loadData();
    } catch (err: any) {
      setMessage(`Training failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleWeightChange = (key: string, val: number) => {
    setWeights((prev) => ({ ...prev, [key]: val }));
  };

  const handleSaveWeights = async () => {
    setLoading(true);
    try {
      await updateWeights(weights);
      setMessage('Scoring weights updated successfully!');
    } catch (err: any) {
      setMessage(`Failed to update weights: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full max-w-md bg-white border-l border-slate-200 shadow-2xl flex flex-col animate-in slide-in-from-right duration-200">
      {/* Drawer Header */}
      <div className="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
        <div className="flex items-center gap-2">
          <Terminal className="w-5 h-5 text-brand-600" />
          <div>
            <h2 className="text-sm font-bold text-slate-900">Developer & Audit Inspector</h2>
            <p className="text-[11px] text-slate-500">SIH 26236 Internal Pipeline Telemetry</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Drawer Body */}
      <div className="flex-1 overflow-y-auto p-4 space-y-5 text-xs text-slate-700">
        {message && (
          <div className="p-3 rounded-lg bg-brand-50 border border-brand-200 text-brand-800 text-[11px] flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-brand-600 flex-shrink-0" />
            <span>{message}</span>
          </div>
        )}

        {/* Section 1: Candidate Generation & Hard Filter Funnel */}
        <div>
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
            1. Candidate Processing Funnel
          </h3>
          {debugInfo?.candidate_funnel ? (
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 space-y-2 font-mono text-[11px]">
              <div className="flex justify-between">
                <span className="text-slate-500">Candidates Generated:</span>
                <span className="font-bold text-slate-800">{debugInfo.candidate_funnel.initial_generated}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Surviving Hard Filter:</span>
                <span className="font-bold text-emerald-700">{debugInfo.candidate_funnel.after_hard_constraint_filtering}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Hard Rejected Candidates:</span>
                <span className="font-bold text-rose-600">{debugInfo.candidate_funnel.rejected_count}</span>
              </div>
              <div className="flex justify-between pt-1 border-t border-slate-200">
                <span className="text-slate-500">Top-3 Ranked for UI:</span>
                <span className="font-bold text-brand-700">{debugInfo.candidate_funnel.final_top_recommendations}</span>
              </div>
            </div>
          ) : (
            <p className="text-slate-400 italic">Run an analysis to inspect funnel drops.</p>
          )}

          {debugInfo?.rejected_sample && debugInfo.rejected_sample.length > 0 && (
            <div className="mt-3 p-3 rounded-xl bg-rose-50/70 border border-rose-200/90 text-xs space-y-2">
              <div className="flex items-center justify-between pb-1 border-b border-rose-200/60">
                <span className="font-bold text-rose-950 text-xs">Sample Rejection Reasons</span>
                <span className="text-[10px] font-semibold text-rose-700 bg-rose-100 px-1.5 py-0.5 rounded">
                  Safety & Compatibility Audit
                </span>
              </div>
              <div className="space-y-1.5">
                {debugInfo.rejected_sample.map((rej, i) => {
                  const rawReason = rej.rejection_reasons?.[0] || 'Constraint violation';
                  // Clean up any unformatted raw strings
                  const cleanedReason = rawReason.replace(
                    /Format Mismatch: User specified '([^']+)' but candidate format is ([a-z]+)\.?/i,
                    (_m, p1, p2) => `Format Incompatibility: Candidate format is ${p2.charAt(0).toUpperCase() + p2.slice(1)}, conflicting with specified ${p1.charAt(0).toUpperCase() + p1.slice(1)} format.`
                  );
                  return (
                    <div key={i} className="text-rose-900 text-[11px] leading-relaxed flex items-start gap-1.5">
                      <span className="text-rose-400 font-bold shrink-0 mt-0.5">•</span>
                      <div>
                        <strong className="text-rose-950 font-semibold">{rej.material}</strong>:
                        <span className="text-rose-800 ml-1">{cleanedReason}</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Section 2: ML Model State & Metrics */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              2. Random Forest Model
            </h3>
            <button
              onClick={handleRetrain}
              disabled={loading}
              className="px-2 py-1 rounded bg-brand-50 hover:bg-brand-100 text-brand-700 text-[10px] font-semibold border border-brand-200 flex items-center gap-1 transition-colors"
            >
              <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
              <span>Retrain Model</span>
            </button>
          </div>

          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 space-y-2 text-[11px]">
            <div className="flex justify-between">
              <span className="text-slate-500">Model Status:</span>
              <span className="font-semibold text-emerald-700">{mlStatus?.model_status || 'READY'}</span>
            </div>
            {mlStatus?.metrics && (
              <>
                <div className="flex justify-between">
                  <span className="text-slate-500">Regression MAE:</span>
                  <span className="font-mono text-slate-800">{mlStatus.metrics.regression.mae}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Regression R²:</span>
                  <span className="font-mono text-slate-800">{mlStatus.metrics.regression.r2}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Classification Accuracy:</span>
                  <span className="font-mono text-emerald-700">{(mlStatus.metrics.classification.accuracy * 100).toFixed(1)}%</span>
                </div>
              </>
            )}
            <p className="text-[10px] text-slate-400 pt-1 border-t border-slate-200/80 italic">
              {mlStatus?.target_notice || 'Prototype target generated from domain rules; not laboratory measurements.'}
            </p>
          </div>
        </div>

        {/* Section 3: Feature Importances */}
        {mlStatus?.feature_importance && (
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
              3. Model Feature Importances
            </h3>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 space-y-1.5 max-h-40 overflow-y-auto">
              {Object.entries(mlStatus.feature_importance)
                .sort(([, a], [, b]) => b - a)
                .map(([feat, imp]) => (
                  <div key={feat} className="flex justify-between text-[11px] font-mono">
                    <span className="text-slate-600 truncate">{feat}:</span>
                    <span className="text-slate-900 font-semibold">{imp}</span>
                  </div>
                ))}
            </div>
            <p className="text-[10px] text-slate-400 mt-1 italic">
              *Feature importance reflects model tabular correlation, not biological causation.
            </p>
          </div>
        )}

        {/* Section 4: Configurable Scoring Weights */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1">
              <Sliders className="w-3.5 h-3.5" /> 4. Configurable Scoring Weights
            </h3>
            <button
              onClick={handleSaveWeights}
              disabled={loading}
              className="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-900 text-white text-[10px] font-semibold transition-colors"
            >
              Save Weights
            </button>
          </div>

          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
            {Object.entries(weights).map(([k, v]) => (
              <div key={k}>
                <div className="flex justify-between text-[11px] mb-1">
                  <span className="font-medium text-slate-700 capitalize">{k.replace('_', ' ')}:</span>
                  <span className="font-mono text-slate-500 font-semibold">{(v * 100).toFixed(0)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="0.5"
                  step="0.05"
                  value={v}
                  onChange={(e) => handleWeightChange(k, parseFloat(e.target.value))}
                  className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-brand-600"
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
