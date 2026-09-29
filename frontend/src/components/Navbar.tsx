import React from 'react';
import { Package, Terminal, FileText, Database } from 'lucide-react';

interface Props {
  activeTab: 'analysis' | 'catalog' | 'modelcard';
  setActiveTab: (tab: 'analysis' | 'catalog' | 'modelcard') => void;
  devMode: boolean;
  setDevMode: (val: boolean) => void;
}

export const Navbar: React.FC<Props> = ({ activeTab, setActiveTab, devMode, setDevMode }) => {
  const handleToggleDevMode = () => {
    const next = !devMode;
    setDevMode(next);
    if (!next) {
      setActiveTab('analysis');
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('analysis')}>
          <img 
            src="/wrap_up_logo.png" 
            alt="Wrap Up! Logo" 
            className="w-10 h-10 object-contain rounded-xl shadow-xs" 
          />
          <div>
            <div className="flex items-center gap-2">
              <span className="font-black text-xl tracking-tight bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">Wrap Up!</span>
              <span className="text-[10px] uppercase font-mono font-semibold px-2 py-0.5 rounded bg-brand-100 text-brand-700 border border-brand-200">
                SIH 26236
              </span>
            </div>
            <p className="text-xs text-slate-500 hidden sm:block">AI-assisted food packaging recommendation</p>
          </div>
        </div>

        {/* Navigation tabs - only visible in Dev Mode */}
        {devMode && (
          <nav className="flex items-center gap-1 sm:gap-2 animate-in fade-in duration-200">
            <button
              onClick={() => setActiveTab('analysis')}
              className={`px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                activeTab === 'analysis'
                  ? 'bg-violet-100 text-violet-900 font-semibold shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              Analysis & Recommendations
            </button>
            <button
              onClick={() => setActiveTab('catalog')}
              className={`px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium transition-colors flex items-center gap-1.5 ${
                activeTab === 'catalog'
                  ? 'bg-violet-100 text-violet-900 font-semibold shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Database className="w-4 h-4 text-violet-600" />
              <span className="hidden sm:inline">Packaging Database</span>
            </button>
            <button
              onClick={() => setActiveTab('modelcard')}
              className={`px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium transition-colors flex items-center gap-1.5 ${
                activeTab === 'modelcard'
                  ? 'bg-violet-100 text-violet-900 font-semibold shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <FileText className="w-4 h-4 text-violet-600" />
              <span className="hidden sm:inline">Model Card & Audit</span>
            </button>
          </nav>
        )}

        {/* Developer Mode Toggle */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleToggleDevMode}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-medium border transition-all ${
              devMode
                ? 'bg-violet-50 border-violet-300 text-violet-800 shadow-sm'
                : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
            }`}
            title="Toggle Developer & Scientific Pipeline Audit Inspector"
          >
            <Terminal className="w-3.5 h-3.5" />
            <span>Dev Mode</span>
            <span
              className={`w-2 h-2 rounded-full ${
                devMode ? 'bg-violet-600 animate-pulse' : 'bg-slate-300'
              }`}
            />
          </button>
        </div>
      </div>
    </header>
  );
};
