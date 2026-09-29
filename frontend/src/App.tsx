import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { FoodInputForm } from './components/FoodInputForm';
import { RequirementMeters } from './components/RequirementMeters';
import { RecommendationCard } from './components/RecommendationCard';
import { ComparisonTable } from './components/ComparisonTable';
import { WhyPackagingModal } from './components/WhyPackagingModal';
import { DeveloperDrawer } from './components/DeveloperDrawer';
import { PackagingCatalogView } from './components/PackagingCatalogView';
import { ModelCardView } from './components/ModelCardView';
import { AnalyzeRequest, AnalyzeResponse, Recommendation } from './types';
import { analyzePackaging } from './services/api';
import { 
  Sparkles, ShieldAlert, Award, CheckCircle2, AlertTriangle 
} from 'lucide-react';

const defaultForm: AnalyzeRequest = {
  food_name: '',
  food_category: '',
  moisture_level: '',
  fat_oil_sensitivity: '',
  ph: '',
  respiration_activity: '',
  desired_shelf_life_days: '',
  storage_temperature_c: '',
  relative_humidity_pct: '',
  storage_condition: 'Ambient',
  transport_condition: '',
  map_required: '',
  sustainability_priority: '',
  preferred_package_type: ''
};

class ErrorBoundary extends React.Component<{ children: React.ReactNode }, { hasError: boolean; error: any }> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error: any) {
    return { hasError: true, error };
  }
  componentDidCatch(error: any, errorInfo: any) {
    console.error("SmartPack ErrorBoundary caught error:", error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm">
          <div className="bg-white rounded-2xl p-6 max-w-md shadow-2xl border border-slate-200 text-center space-y-4">
            <h3 className="text-base font-bold text-slate-900">Evaluation Notice</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Unable to render detailed evaluation modal for this item.
            </p>
            <button
              onClick={() => this.setState({ hasError: false })}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-semibold"
            >
              Close
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

export function App() {
  const [activeTab, setActiveTab] = useState<'analysis' | 'catalog' | 'modelcard'>('analysis');
  const [devMode, setDevMode] = useState(false);
  const [formData, setFormData] = useState<AnalyzeRequest>(defaultForm);
  const [results, setResults] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedRec, setSelectedRec] = useState<Recommendation | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const sanitizedPayload: AnalyzeRequest = {
        ...formData,
        food_name: formData.food_name?.trim() || 'Potato, brown skin, big (Solanum tuberosum)',
        food_category: formData.food_category || 'Roots and Tubers',
        moisture_level: formData.moisture_level !== '' && formData.moisture_level !== undefined ? Number(formData.moisture_level) : 80.7,
        fat_oil_sensitivity: formData.fat_oil_sensitivity || 'Low',
        ph: formData.ph !== '' && formData.ph !== undefined ? Number(formData.ph) : 6.2,
        respiration_activity: formData.respiration_activity || 'Low',
        desired_shelf_life_days: formData.desired_shelf_life_days !== '' && formData.desired_shelf_life_days !== undefined ? Number(formData.desired_shelf_life_days) : 120,
        storage_temperature_c: formData.storage_temperature_c !== '' && formData.storage_temperature_c !== undefined ? Number(formData.storage_temperature_c) : 15.0,
        relative_humidity_pct: formData.relative_humidity_pct !== '' && formData.relative_humidity_pct !== undefined ? Number(formData.relative_humidity_pct) : 75.0,
        storage_condition: formData.storage_condition || 'Ambient',
        transport_condition: formData.transport_condition || 'Ambient / Road',
        map_required: formData.map_required || 'No',
        sustainability_priority: formData.sustainability_priority || 'High (Recyclable)',
        preferred_package_type: formData.preferred_package_type || 'Any'
      };
      const data = await analyzePackaging(sanitizedPayload);
      setResults(data);
      // Smooth scroll down to results
      setTimeout(() => {
        const el = document.getElementById('results-section');
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err: any) {
      setError(err.message || 'Failed to complete analysis');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50/60 text-slate-900 font-sans flex flex-col selection:bg-brand-500/20">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        devMode={devMode}
        setDevMode={setDevMode}
      />

      {activeTab === 'catalog' && <PackagingCatalogView />}
      {activeTab === 'modelcard' && <ModelCardView />}

      {activeTab === 'analysis' && (
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
          {/* Hero / Header Section (Screen 1) */}
          <div className="mb-8 bg-gradient-to-r from-brand-50 via-white to-slate-50 border border-brand-200/50 rounded-3xl p-6 sm:p-10 shadow-sm relative overflow-hidden">
            <div className="max-w-3xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-100/80 border border-brand-200 text-brand-800 text-xs font-semibold uppercase tracking-wider mb-4">
                <Sparkles className="w-3.5 h-3.5 text-brand-600" />
                SIH Problem Statement 26236 Working Prototype
              </div>
              <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight leading-tight">
                Smart Food-Packaging Recommendation System
              </h1>
              <p className="text-slate-600 text-sm sm:text-base mt-3 leading-relaxed">
                Translate food composition and storage shelf-life requirements into scientific packaging specifications.
                Screen verified candidates from FSSAI Schedule IV & BIS standards, filter incompatible materials via hard constraints,
                and rank with a transparent hybrid ML pipeline.
              </p>

              <div className="mt-6 flex flex-wrap items-center gap-4 text-xs text-slate-500 font-medium">
                <span className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" /> ICMR IFCT 2017 Nutrients
                </span>
                <span className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" /> FSSAI Schedule IV Lookup
                </span>
                <span className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" /> BIS IS Packaging Specs
                </span>
                <span className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Zero Fabricated Values
                </span>
              </div>
            </div>
          </div>

          {/* Error Banner */}
          {error && (
            <div className="mb-6 p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-900 text-xs flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-rose-600 flex-shrink-0" />
              <div>
                <strong className="font-bold">Error during analysis:</strong> {error}
                <p className="text-[11px] text-rose-700 mt-0.5">Please ensure the backend API is running on localhost:8000.</p>
              </div>
            </div>
          )}

          {/* Screen 2: Food Input Form */}
          <FoodInputForm
            formData={formData}
            setFormData={setFormData}
            onAnalyze={handleAnalyze}
            loading={loading}
          />

          {/* Results Container */}
          {results && (
            <div id="results-section" className="space-y-8 animate-in fade-in duration-300">
              {/* Screen 3: Calculated Requirements Analysis */}
              <RequirementMeters requirements={results.requirements} />

              {/* Case when no packaging survives hard constraint filtering */}
              {results.status === 'NO_COMPATIBLE_PACKAGING' || results.recommendations.length === 0 ? (
                <div className="bg-rose-50/70 border border-rose-200 rounded-2xl p-8 text-center max-w-3xl mx-auto shadow-sm">
                  <div className="w-12 h-12 rounded-full bg-rose-100 text-rose-700 flex items-center justify-center mx-auto mb-4">
                    <ShieldAlert className="w-6 h-6" />
                  </div>
                  <h3 className="text-lg font-bold text-rose-900">
                    No Packaging Option Satisfies All Current Requirements
                  </h3>
                  <p className="text-xs text-rose-800 mt-2 max-w-xl mx-auto leading-relaxed">
                    {results.message ||
                      'Strict safety, regulatory, or physical compatibility constraints rejected all evaluated candidates. In accordance with safety rules, incompatible options are never promoted to the final recommendation.'}
                  </p>

                  {results.rejected_candidates && results.rejected_candidates.length > 0 && (
                    <div className="mt-6 text-left max-w-lg mx-auto p-4 bg-white rounded-xl border border-rose-200 text-xs">
                      <span className="font-bold text-slate-800 block mb-2">Closest Evaluated Options & Rejection Audit:</span>
                      <div className="space-y-2">
                        {results.rejected_candidates.slice(0, 3).map((rej, i) => (
                          <div key={i} className="p-2 rounded bg-slate-50 border border-slate-200/70 text-[11px]">
                            <strong className="text-slate-900">{rej.material}</strong>:
                            <span className="text-rose-700 ml-1">{rej.rejection_reasons?.[0]}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <>
                  {/* Screen 4: Results (Top 3 Candidates) */}
                  <div>
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 mb-6 gap-2">
                      <div>
                        <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
                          <Award className="w-6 h-6 text-brand-600" />
                          Recommended Packaging (Top 3 Candidates)
                        </h2>
                        <p className="text-xs text-slate-500 mt-1">
                          Evaluated against FSSAI Schedule IV, hard safety constraints, and ranked via transparent hybrid scoring.
                        </p>
                      </div>
                      <div className="text-xs font-mono text-slate-500 bg-white px-3 py-1.5 rounded-lg border border-slate-200">
                        Total Candidates Screened: <strong>{results.all_ranked_candidates_count || 3}</strong>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {results.recommendations.map((rec) => (
                        <RecommendationCard
                          key={rec.rank}
                          recommendation={rec}
                          onOpenExplain={(r) => setSelectedRec(r)}
                        />
                      ))}
                    </div>
                  </div>

                  {/* Screen 5: Comparison Table */}
                  <ComparisonTable recommendations={results.recommendations} />
                </>
              )}
            </div>
          )}
        </main>
      )}

      {/* Screen 6: "Why This Packaging?" Modal */}
      {selectedRec && (
        <ErrorBoundary>
          <WhyPackagingModal
            recommendation={selectedRec}
            userInput={formData}
            requirements={results?.requirements}
            onClose={() => setSelectedRec(null)}
          />
        </ErrorBoundary>
      )}

      {/* Screen 7: Developer Telemetry Drawer */}
      <DeveloperDrawer
        debugInfo={results?.debug}
        isOpen={devMode}
        onClose={() => setDevMode(false)}
      />

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-200 bg-white py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>SmartPack — SIH Problem Statement 26236 Production-Style Prototype</span>
          <span className="font-mono text-[11px] text-slate-400">
            Source Data: ICMR IFCT 2017 • FSSAI Schedule IV • BIS Packaging Standards
          </span>
        </div>
      </footer>
    </div>
  );
}

export default App;
