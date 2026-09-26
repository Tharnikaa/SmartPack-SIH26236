import React from 'react';
import { Package, Terminal, FileText, Database } from 'lucide-react';

interface Props {
  activeTab: 'analysis' | 'catalog' | 'modelcard';
  setActiveTab: (tab: 'analysis' | 'catalog' | 'modelcard') => void;
  devMode: boolean;
  setDevMode: (val: boolean) => void;
}

export const Navbar: React.FC<Props> = ({ activeTab, setActiveTab, devMode, setDevMode }) => {
  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('analysis')}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white shadow-sm shadow-brand-500/20">
            <Package className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg tracking-tight text-slate-900">SmartPack</span>
              <span className="text-[10px] uppercase font-mono font-semibold px-2 py-0.5 rounded bg-brand-100 text-brand-700 border border-brand-200">
                SIH 26236
              </span>
            </div>
            <p className="text-xs text-slate-500 hidden sm:block">AI-assisted food packaging recommendation</p>
          </div>
        </div>

        {/* Navigation tabs */}
        <nav className="flex items-center gap-1 sm:gap-2">
          <button
            onClick={() => setActiveTab('analysis')}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              activeTab === 'analysis'
                ? 'bg-slate-100 text-slate-900'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            Analysis & Recommendations
          </button>
          <button
            onClick={() => setActiveTab('catalog')}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
              activeTab === 'catalog'
                ? 'bg-slate-100 text-slate-900'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <Database className="w-4 h-4 text-slate-400" />
            <span className="hidden sm:inline">Packaging Database</span>
          </button>
          <button
            onClick={() => setActiveTab('modelcard')}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
              activeTab === 'modelcard'
                ? 'bg-slate-100 text-slate-900'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <FileText className="w-4 h-4 text-slate-400" />
            <span className="hidden sm:inline">Model Card & Audit</span>
          </button>
        </nav>

        {/* Developer Mode Toggle */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setDevMode(!devMode)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-medium border transition-all ${
              devMode
                ? 'bg-brand-50 border-brand-300 text-brand-700 shadow-sm'
                : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
            }`}
            title="Toggle Developer & Scientific Pipeline Audit Inspector"
          >
            <Terminal className="w-3.5 h-3.5" />
            <span>Dev Mode</span>
            <span
              className={`w-2 h-2 rounded-full ${
                devMode ? 'bg-brand-500 animate-pulse' : 'bg-slate-300'
              }`}
            />
          </button>
        </div>
      </div>
    </header>
  );
};
