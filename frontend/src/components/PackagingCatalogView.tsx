import React, { useState, useEffect } from 'react';
import { fetchPackagingMaterials } from '../services/api';
import { Database, Search, Shield, Wind, Droplets, Leaf, BookOpen } from 'lucide-react';
import { OriginBadge } from './OriginBadge';

export const PackagingCatalogView: React.FC = () => {
  const [materials, setMaterials] = useState<any[]>([]);
  const [search, setSearch] = useState('');
  const [selectedMat, setSelectedMat] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPackagingMaterials()
      .then((data) => {
        setMaterials(data);
        if (data.length > 0) setSelectedMat(data[0]);
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered = materials.filter((m) =>
    m.material_name.toLowerCase().includes(search.toLowerCase()) ||
    m.material_family.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-in fade-in duration-200">
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-slate-900">Packaging Materials Database Catalog</h1>
            <OriginBadge origin="DATABASE VALUE" />
          </div>
          <p className="text-xs text-slate-500 mt-1">
            26 officially cataloged packaging materials and BIS/IS standard technical properties.
          </p>
        </div>

        <div className="relative w-full sm:w-72">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search material or polymer..."
            className="w-full pl-9 pr-3 py-2 bg-white border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
          />
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left List */}
        <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm max-h-[700px] overflow-y-auto space-y-2">
          {loading ? (
            <div className="p-8 text-center text-xs text-slate-400">Loading database records...</div>
          ) : filtered.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-400">No matching materials found.</div>
          ) : (
            filtered.map((mat, i) => (
              <div
                key={i}
                onClick={() => setSelectedMat(mat)}
                className={`p-3 rounded-xl border cursor-pointer transition-all ${
                  selectedMat?.material_name === mat.material_name
                    ? 'bg-brand-50/60 border-brand-300 shadow-sm'
                    : 'bg-white border-slate-100 hover:border-slate-200 hover:bg-slate-50/50'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-xs text-slate-900">{mat.material_name}</span>
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-100 text-slate-600">
                    {mat.packaging_id}
                  </span>
                </div>
                <div className="text-[11px] text-slate-500 flex items-center gap-2">
                  <span>{mat.material_family}</span>
                  <span>•</span>
                  <span>{mat.food_contact_suitable === 'Yes' ? 'Food Grade' : 'Conditional'}</span>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Right Details */}
        <div className="lg:col-span-2">
          {selectedMat ? (
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
              <div className="border-b border-slate-100 pb-4">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-mono font-bold text-brand-700 bg-brand-100 px-2 py-0.5 rounded">
                    {selectedMat.packaging_id}
                  </span>
                  <span className="text-xs text-slate-500">{selectedMat.material_family}</span>
                </div>
                <h2 className="text-xl font-bold text-slate-900">{selectedMat.material_name}</h2>
                <p className="text-xs text-slate-500 mt-1">
                  Standard designation: <strong className="text-slate-700">{selectedMat.material_type}</strong>
                </p>
              </div>

              {/* Barrier Matrix */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                  <Wind className="w-3.5 h-3.5 text-purple-600" /> Barrier Transmission Data (08_barrier_properties_dataset.csv)
                </h3>
                {selectedMat.barrier_properties ? (
                  <div className="grid grid-cols-2 gap-3 p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs">
                    <div>
                      <span className="text-slate-400 block text-[11px]">Oxygen Transmission (OTR):</span>
                      <span className="font-bold text-slate-800">
                        {selectedMat.barrier_properties.otr !== null
                          ? `${selectedMat.barrier_properties.otr} ${selectedMat.barrier_properties.otr_unit}`
                          : 'Data unavailable in source database'}
                      </span>
                    </div>
                    <div>
                      <span className="text-slate-400 block text-[11px]">Water Vapor Transmission (WVTR):</span>
                      <span className="font-bold text-slate-800">
                        {selectedMat.barrier_properties.wvtr !== null
                          ? `${selectedMat.barrier_properties.wvtr} ${selectedMat.barrier_properties.wvtr_unit}`
                          : 'Data unavailable in source database'}
                      </span>
                    </div>
                  </div>
                ) : (
                  <p className="text-xs text-slate-400 italic p-3 bg-slate-50 rounded-xl">
                    No barrier transmission data measured in source CSV.
                  </p>
                )}
              </div>

              {/* Mechanical & Standard Specifications */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                  <Shield className="w-3.5 h-3.5 text-emerald-600" /> Technical Properties from BIS Standard
                </h3>
                {selectedMat.properties && selectedMat.properties.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs text-left">
                      <thead>
                        <tr className="border-b border-slate-200 bg-slate-50 text-slate-600">
                          <th className="py-2 px-3">Property Name</th>
                          <th className="py-2 px-3">Value</th>
                          <th className="py-2 px-3">Unit</th>
                          <th className="py-2 px-3">Test Condition</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
                        {selectedMat.properties.map((p: any, idx: number) => (
                          <tr key={idx} className="hover:bg-slate-50/50">
                            <td className="py-2 px-3 font-sans text-slate-800 font-medium">{p.property_name}</td>
                            <td className="py-2 px-3 font-bold text-slate-900">{p.property_value}</td>
                            <td className="py-2 px-3 text-slate-500">{p.unit || '-'}</td>
                            <td className="py-2 px-3 text-slate-400 font-sans text-[10px]">{p.test_condition || '-'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className="text-xs text-slate-400 italic p-3 bg-slate-50 rounded-xl">
                    Specific mechanical limits not cataloged in dataset 07.
                  </p>
                )}
              </div>

              {/* Sustainability & Environmental Attributes */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                  <Leaf className="w-3.5 h-3.5 text-emerald-600" /> Sustainability Profile (11_sustainability_dataset.csv)
                </h3>
                {selectedMat.sustainability ? (
                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2 text-xs">
                    <div className="grid grid-cols-3 gap-2">
                      <div>
                        <span className="text-slate-400 text-[11px] block">Recyclable:</span>
                        <strong className="text-slate-800">{selectedMat.sustainability.recyclable}</strong>
                      </div>
                      <div>
                        <span className="text-slate-400 text-[11px] block">Compostable:</span>
                        <strong className="text-slate-800">{selectedMat.sustainability.compostable}</strong>
                      </div>
                      <div>
                        <span className="text-slate-400 text-[11px] block">Biodegradable:</span>
                        <strong className="text-slate-800">{selectedMat.sustainability.biodegradable}</strong>
                      </div>
                    </div>
                    {selectedMat.sustainability.advantages && (
                      <p className="text-[11px] text-emerald-800 pt-2 border-t border-slate-200">
                        <strong>Advantages:</strong> {selectedMat.sustainability.advantages}
                      </p>
                    )}
                    {selectedMat.sustainability.concerns && (
                      <p className="text-[11px] text-amber-800">
                        <strong>Concerns:</strong> {selectedMat.sustainability.concerns}
                      </p>
                    )}
                  </div>
                ) : (
                  <p className="text-xs text-slate-400 italic p-3 bg-slate-50 rounded-xl">
                    Sustainability metadata unavailable in primary dataset.
                  </p>
                )}
              </div>

              {/* Source Document Citation */}
              <div className="p-3 rounded-lg bg-blue-50/60 border border-blue-100 flex items-center gap-2 text-xs text-blue-900">
                <BookOpen className="w-4 h-4 text-blue-700 flex-shrink-0" />
                <span>
                  Source: <strong>{selectedMat.source_document || 'FSSAI / BIS Standards'}</strong>
                </span>
              </div>
            </div>
          ) : (
            <div className="p-12 text-center text-xs text-slate-400 bg-white rounded-2xl border border-slate-200">
              Select a packaging material on the left to inspect properties.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
