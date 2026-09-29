import React, { useState, useEffect } from 'react';
import { AnalyzeRequest } from '../types';
import { fetchCategories, fetchFoods } from '../services/api';
import { Sparkles, Search, Sliders, RotateCcw } from 'lucide-react';

interface Props {
  formData: AnalyzeRequest;
  setFormData: React.Dispatch<React.SetStateAction<AnalyzeRequest>>;
  onAnalyze: () => void;
  loading: boolean;
}

export const FoodInputForm: React.FC<Props> = ({ formData, setFormData, onAnalyze, loading }) => {
  const [categories, setCategories] = useState<string[]>([]);
  const [foodSearchQuery, setFoodSearchQuery] = useState('');
  const [foodSuggestions, setFoodSuggestions] = useState<any[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    fetchCategories().then(setCategories).catch(console.error);
  }, []);

  useEffect(() => {
    if (foodSearchQuery.length >= 2) {
      fetchFoods(foodSearchQuery).then((res) => {
        setFoodSuggestions(res);
        setShowSuggestions(true);
      });
    } else {
      setFoodSuggestions([]);
      setShowSuggestions(false);
    }
  }, [foodSearchQuery]);

  const selectFood = (food: any) => {
    setFormData((prev) => ({
      ...prev,
      food_name: food.food_name,
      food_category: food.food_category || prev.food_category,
      moisture_level: food.moisture_content !== null ? food.moisture_content : prev.moisture_level,
      fat_oil_sensitivity: food.fat_content && food.fat_content > 15 ? 'High' : (food.fat_content > 3 ? 'Medium' : 'Low')
    }));
    setFoodSearchQuery(food.food_name);
    setShowSuggestions(false);
  };

  const resetForm = () => {
    setFormData({
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
    });
    setFoodSearchQuery('');
    setShowSuggestions(false);
  };

  const loadScenario = (type: string) => {
    switch (type) {
      case 'biscuits':
        setFormData({
          food_name: 'Biscuits / Cookies',
          food_category: 'Cereals and cereal products',
          moisture_level: 4.5,
          fat_oil_sensitivity: 'Medium',
          ph: 6.5,
          respiration_activity: 'Low',
          desired_shelf_life_days: 180,
          storage_temperature_c: 25,
          relative_humidity_pct: 65,
          storage_condition: 'Ambient',
          transport_condition: 'Ambient / Road',
          map_required: 'No',
          sustainability_priority: 'Standard',
          preferred_package_type: 'Any'
        });
        setFoodSearchQuery('Biscuits / Cookies');
        break;
      case 'fruits':
        setFormData({
          food_name: 'Fresh Apples / Mangoes',
          food_category: 'Fruit & Vegetable products',
          moisture_level: 84.0,
          fat_oil_sensitivity: 'Low',
          ph: 4.0,
          respiration_activity: 'High',
          desired_shelf_life_days: 21,
          storage_temperature_c: 12,
          relative_humidity_pct: 85,
          storage_condition: 'Chilled',
          transport_condition: 'Rough / Long-Distance',
          map_required: 'Optional',
          sustainability_priority: 'High (Recyclable)',
          preferred_package_type: 'Rigid'
        });
        setFoodSearchQuery('Fresh Apples / Mangoes');
        break;
      case 'spices':
        setFormData({
          food_name: 'Ground Turmeric & Chili Spices',
          food_category: 'Salt, spices, Condiments and related products',
          moisture_level: 8.0,
          fat_oil_sensitivity: 'High',
          ph: 5.8,
          respiration_activity: 'Low',
          desired_shelf_life_days: 365,
          storage_temperature_c: 25,
          relative_humidity_pct: 60,
          storage_condition: 'Ambient',
          transport_condition: 'Ambient',
          map_required: 'No',
          sustainability_priority: 'Standard',
          preferred_package_type: 'Flexible'
        });
        setFoodSearchQuery('Ground Turmeric & Chili Spices');
        break;
      case 'milk':
        setFormData({
          food_name: 'Pasteurized Milk / Dairy Drink',
          food_category: 'Milk and milk products',
          moisture_level: 88.0,
          fat_oil_sensitivity: 'High',
          ph: 6.7,
          respiration_activity: 'Low',
          desired_shelf_life_days: 14,
          storage_temperature_c: 4,
          relative_humidity_pct: 75,
          storage_condition: 'Refrigerated',
          transport_condition: 'Cold-Chain',
          map_required: 'No',
          sustainability_priority: 'High (Recyclable)',
          preferred_package_type: 'Any'
        });
        setFoodSearchQuery('Pasteurized Milk / Dairy Drink');
        break;
      case 'snacks':
        setFormData({
          food_name: 'Fried Potato Chips / Extruded Snacks',
          food_category: 'Fats, oils and fat emulsions',
          moisture_level: 2.5,
          fat_oil_sensitivity: 'High',
          ph: 6.0,
          respiration_activity: 'Low',
          desired_shelf_life_days: 120,
          storage_temperature_c: 25,
          relative_humidity_pct: 60,
          storage_condition: 'Ambient',
          transport_condition: 'Ambient',
          map_required: 'Yes',
          sustainability_priority: 'Standard',
          preferred_package_type: 'Flexible'
        });
        setFoodSearchQuery('Fried Potato Chips / Extruded Snacks');
        break;
      case 'strict_safety':
        setFormData({
          food_name: 'Acidic Organic Berry Pulp',
          food_category: 'Fruit & Vegetable products',
          moisture_level: 89.0,
          fat_oil_sensitivity: 'Low',
          ph: 3.2,
          respiration_activity: 'Low',
          desired_shelf_life_days: 365,
          storage_temperature_c: 25,
          relative_humidity_pct: 65,
          storage_condition: 'Ambient',
          transport_condition: 'Ambient',
          map_required: 'Yes',
          sustainability_priority: 'Strict (Zero-Plastic)',
          preferred_package_type: 'Flexible'
        });
        setFoodSearchQuery('Acidic Organic Berry Pulp');
        break;
      default:
        break;
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-sm mb-8">
      {/* Scenario Presets Bar */}
      <div className="mb-8 pb-6 border-b border-slate-100">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-brand-600" />
            Quick Demo Scenarios (Prompt Spec #33)
          </span>
          <span className="text-[11px] text-slate-400">Pre-populates verified parameters</span>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={() => loadScenario('biscuits')}
            className="px-3 py-1.5 rounded-lg border border-slate-200 hover:border-brand-300 hover:bg-brand-50/50 text-xs font-medium text-slate-700 transition-colors"
          >
            🍪 Biscuits (Dry, Crisp)
          </button>
          <button
            type="button"
            onClick={() => loadScenario('fruits')}
            className="px-3 py-1.5 rounded-lg border border-slate-200 hover:border-brand-300 hover:bg-brand-50/50 text-xs font-medium text-slate-700 transition-colors"
          >
            🍎 Fresh Fruits (High Respiration)
          </button>
          <button
            type="button"
            onClick={() => loadScenario('spices')}
            className="px-3 py-1.5 rounded-lg border border-slate-200 hover:border-brand-300 hover:bg-brand-50/50 text-xs font-medium text-slate-700 transition-colors"
          >
            🌶️ Spices (Aroma Protection)
          </button>
          <button
            type="button"
            onClick={() => loadScenario('milk')}
            className="px-3 py-1.5 rounded-lg border border-slate-200 hover:border-brand-300 hover:bg-brand-50/50 text-xs font-medium text-slate-700 transition-colors"
          >
            🥛 Milk Product (Cold-Chain)
          </button>
          <button
            type="button"
            onClick={() => loadScenario('snacks')}
            className="px-3 py-1.5 rounded-lg border border-slate-200 hover:border-brand-300 hover:bg-brand-50/50 text-xs font-medium text-slate-700 transition-colors"
          >
            🥔 Fried Snack (MAP / Nitrogen)
          </button>
          <button
            type="button"
            onClick={() => loadScenario('strict_safety')}
            className="px-3 py-1.5 rounded-lg border border-rose-200 bg-rose-50/30 hover:bg-rose-50 text-xs font-medium text-rose-800 transition-colors"
          >
            ⚠️ Strict Zero-Plastic (Safety Filter Test)
          </button>
          <button
            type="button"
            onClick={resetForm}
            className="px-3 py-1.5 rounded-lg border border-dashed border-slate-300 hover:border-slate-400 hover:bg-slate-100 text-xs font-medium text-slate-600 transition-colors flex items-center gap-1.5"
            title="Reset all fields to empty placeholders"
          >
            <RotateCcw className="w-3.5 h-3.5 text-slate-500" />
            Clear to Placeholders
          </button>
        </div>
      </div>

      <form onSubmit={(e) => { e.preventDefault(); onAnalyze(); }}>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Section 1: Product Information */}
          <div className="bg-slate-50/60 p-5 sm:p-6 rounded-2xl border border-slate-200/80 space-y-4 md:col-span-2 lg:col-span-4">
            <div className="flex items-center justify-between border-b border-slate-200 pb-3">
              <div className="flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-violet-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
                  1
                </span>
                <h3 className="text-sm font-bold text-slate-900 tracking-tight">Product Information</h3>
              </div>
              <span className="text-[11px] font-normal text-slate-400">Database Auto-Search from ICMR IFCT 2017</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Field 1: Food Product Name */}
              <div className="relative">
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Food Product Name
                </label>
                <div className="relative">
                  <input
                    type="text"
                    value={formData.food_name}
                    onChange={(e) => {
                      setFormData({ ...formData, food_name: e.target.value });
                      setFoodSearchQuery(e.target.value);
                    }}
                    placeholder="e.g. Potato, brown skin, big (Solanum tuberosum)"
                    className="w-full pl-9 pr-3 py-2.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs"
                  />
                  <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                </div>
                {showSuggestions && foodSuggestions.length > 0 && (
                  <div className="absolute z-20 left-0 right-0 mt-1 bg-white border border-slate-200 rounded-xl shadow-lg max-h-48 overflow-y-auto">
                    {foodSuggestions.map((item, idx) => (
                      <div
                        key={idx}
                        onClick={() => selectFood(item)}
                        className="p-2.5 hover:bg-slate-50 cursor-pointer border-b border-slate-100 last:border-b-0 text-xs"
                      >
                        <div className="font-medium text-slate-800">{item.food_name}</div>
                        <div className="text-[10px] text-slate-400">
                          {item.food_category} • Moisture: {item.moisture_content}% • Fat: {item.fat_content}g
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Field 2: FSSAI Food Category */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  FSSAI Food Category (Schedule IV Mapping)
                </label>
                <select
                  value={formData.food_category}
                  onChange={(e) => setFormData({ ...formData, food_category: e.target.value })}
                  className={`w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs ${
                    !formData.food_category ? 'text-slate-400' : 'text-slate-900'
                  }`}
                >
                  <option value="" disabled className="text-slate-400">
                    Select FSSAI Food Category (e.g. Roots and Tubers)...
                  </option>
                  {categories.map((cat, i) => (
                    <option key={i} value={cat} className="text-slate-900">
                      {cat}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Section 2: Food Characteristics */}
          <div className="bg-slate-50/60 p-5 sm:p-6 rounded-2xl border border-slate-200/80 space-y-4 md:col-span-2 lg:col-span-2 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 border-b border-slate-200 pb-3 mb-4">
                <span className="w-6 h-6 rounded-full bg-violet-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
                  2
                </span>
                <h3 className="text-sm font-bold text-slate-900 tracking-tight">Food Characteristics</h3>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Field 3: Moisture Level */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                    Moisture Level (%)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    value={formData.moisture_level === '' ? '' : formData.moisture_level}
                    onChange={(e) => setFormData({ ...formData, moisture_level: e.target.value === '' ? '' : parseFloat(e.target.value) })}
                    placeholder="e.g. 80.7"
                    className="w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs"
                  />
                </div>

                {/* Field 4: Fat / Oil Sensitivity */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                    Fat / Oil Sensitivity
                  </label>
                  <select
                    value={formData.fat_oil_sensitivity}
                    onChange={(e) => setFormData({ ...formData, fat_oil_sensitivity: e.target.value })}
                    className={`w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs ${
                      !formData.fat_oil_sensitivity ? 'text-slate-400' : 'text-slate-900'
                    }`}
                  >
                    <option value="" disabled className="text-slate-400">
                      Select Fat / Oil Sensitivity...
                    </option>
                    <option value="Low" className="text-slate-900">Low (Negligible Fat)</option>
                    <option value="Medium" className="text-slate-900">Medium (Standard Lipid Content)</option>
                    <option value="High" className="text-slate-900">High (High Fat, Prone to Rancidity)</option>
                  </select>
                </div>

                {/* Field 5: Product pH */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="block text-xs font-semibold text-slate-700">
                      Product pH
                    </label>
                    <span className="text-[10px] text-slate-400">&lt;4.5 triggers acid-lacquering</span>
                  </div>
                  <input
                    type="number"
                    step="0.1"
                    min="1"
                    max="14"
                    value={formData.ph === '' ? '' : formData.ph}
                    onChange={(e) => setFormData({ ...formData, ph: e.target.value === '' ? '' : parseFloat(e.target.value) })}
                    placeholder="e.g. 6.2"
                    className="w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs"
                  />
                </div>

                {/* Field 6: Respiration / Activity */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                    Respiration / Activity
                  </label>
                  <select
                    value={formData.respiration_activity}
                    onChange={(e) => setFormData({ ...formData, respiration_activity: e.target.value })}
                    className={`w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs ${
                      !formData.respiration_activity ? 'text-slate-400' : 'text-slate-900'
                    }`}
                  >
                    <option value="" disabled className="text-slate-400">
                      Select Respiration / Activity...
                    </option>
                    <option value="Low" className="text-slate-900">Low (Processed / Dry / Inactive)</option>
                    <option value="Medium" className="text-slate-900">Medium (Moderate Produce)</option>
                    <option value="High" className="text-slate-900">High (Live Produce / Horticulture)</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Section 3: Shelf Life & Storage */}
          <div className="bg-slate-50/60 p-5 sm:p-6 rounded-2xl border border-slate-200/80 space-y-4 md:col-span-2 lg:col-span-2 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 border-b border-slate-200 pb-3 mb-4">
                <span className="w-6 h-6 rounded-full bg-violet-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
                  3
                </span>
                <h3 className="text-sm font-bold text-slate-900 tracking-tight">Shelf Life & Storage</h3>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Field 7: Desired Shelf Life */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                    Desired Shelf Life (Days)
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="1000"
                    value={formData.desired_shelf_life_days === '' ? '' : formData.desired_shelf_life_days}
                    onChange={(e) => setFormData({ ...formData, desired_shelf_life_days: e.target.value === '' ? '' : parseInt(e.target.value, 10) })}
                    placeholder="e.g. 120"
                    className="w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs"
                  />
                </div>

                {/* Field 8: Storage Temperature */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                    Storage Temperature (°C)
                  </label>
                  <input
                    type="number"
                    step="1"
                    value={formData.storage_temperature_c === '' ? '' : formData.storage_temperature_c}
                    onChange={(e) => setFormData({ ...formData, storage_temperature_c: e.target.value === '' ? '' : parseFloat(e.target.value) })}
                    placeholder="e.g. 15"
                    className="w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs"
                  />
                </div>

                {/* Field 9: Relative Humidity */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                    Relative Humidity (%)
                  </label>
                  <input
                    type="number"
                    step="1"
                    min="10"
                    max="100"
                    value={formData.relative_humidity_pct === '' ? '' : formData.relative_humidity_pct}
                    onChange={(e) => setFormData({ ...formData, relative_humidity_pct: e.target.value === '' ? '' : parseFloat(e.target.value) })}
                    placeholder="e.g. 75"
                    className="w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs"
                  />
                </div>

                {/* Field 10: Transport Rigor */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                    Transport Rigor
                  </label>
                  <select
                    value={formData.transport_condition}
                    onChange={(e) => setFormData({ ...formData, transport_condition: e.target.value })}
                    className={`w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs ${
                      !formData.transport_condition ? 'text-slate-400' : 'text-slate-900'
                    }`}
                  >
                    <option value="" disabled className="text-slate-400">
                      Select Transport Rigor...
                    </option>
                    <option value="Ambient / Road" className="text-slate-900">Ambient / Road Standard</option>
                    <option value="Rough / Long-Distance" className="text-slate-900">Rough / Long-Distance Logistics</option>
                    <option value="Cold-Chain" className="text-slate-900">Dedicated Cold-Chain</option>
                    <option value="Export" className="text-slate-900">Export Intermodal Freight</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Section 4: Packaging Requirements & Preferences */}
          <div className="bg-slate-50/60 p-5 sm:p-6 rounded-2xl border border-slate-200/80 space-y-4 md:col-span-2 lg:col-span-4">
            <div className="flex items-center gap-2 border-b border-slate-200 pb-3">
              <span className="w-6 h-6 rounded-full bg-violet-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
                4
              </span>
              <h3 className="text-sm font-bold text-slate-900 tracking-tight">Packaging Requirements & Preferences</h3>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {/* Field 11: Modified Atmosphere */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Modified Atmosphere (MAP) Required?
                </label>
                <select
                  value={formData.map_required}
                  onChange={(e) => setFormData({ ...formData, map_required: e.target.value })}
                  className={`w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs ${
                    !formData.map_required ? 'text-slate-400' : 'text-slate-900'
                  }`}
                >
                  <option value="" disabled className="text-slate-400">
                    Select MAP requirement...
                  </option>
                  <option value="No" className="text-slate-900">No (Ambient Air)</option>
                  <option value="Yes" className="text-slate-900">Yes (Gas Barrier Mandatory)</option>
                  <option value="Optional" className="text-slate-900">Optional (Beneficial if Available)</option>
                </select>
              </div>

              {/* Field 12: Sustainability Priority */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Sustainability Priority
                </label>
                <select
                  value={formData.sustainability_priority}
                  onChange={(e) => setFormData({ ...formData, sustainability_priority: e.target.value })}
                  className={`w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs ${
                    !formData.sustainability_priority ? 'text-slate-400' : 'text-slate-900'
                  }`}
                >
                  <option value="" disabled className="text-slate-400">
                    Select Sustainability Priority...
                  </option>
                  <option value="Standard" className="text-slate-900">Standard (CPCB EPR Compliant)</option>
                  <option value="High (Recyclable)" className="text-slate-900">High (Single-Polymer / Recyclable)</option>
                  <option value="Strict (Zero-Plastic)" className="text-slate-900">Strict (Zero-Plastic / Compostable)</option>
                </select>
              </div>

              {/* Field 13: Preferred Packaging Format */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Preferred Packaging Format
                </label>
                <select
                  value={formData.preferred_package_type}
                  onChange={(e) => setFormData({ ...formData, preferred_package_type: e.target.value })}
                  className={`w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 shadow-xs ${
                    !formData.preferred_package_type ? 'text-slate-400' : 'text-slate-900'
                  }`}
                >
                  <option value="" disabled className="text-slate-400">
                    Select Preferred Packaging Format...
                  </option>
                  <option value="Any" className="text-slate-900">Any Format (Rigid or Flexible)</option>
                  <option value="Flexible" className="text-slate-900">Flexible (Pouch, Film, Bag)</option>
                  <option value="Rigid" className="text-slate-900">Rigid (Bottle, Can, Jar, Tub, Box)</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="mt-8 pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-[11px] text-slate-500">
            *Technical properties (OTR, WVTR, mechanical limits) are retrieved exclusively from source BIS/FSSAI datasets.
          </p>
          <button
            type="submit"
            disabled={loading}
            className="w-full sm:w-auto px-8 py-3.5 bg-violet-600 hover:bg-violet-700 active:bg-violet-800 text-white font-bold text-sm rounded-xl shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Running Scientific Requirement Analysis...</span>
              </>
            ) : (
              <>
                <span>Analyze & Recommend Packaging</span>
                <Sliders className="w-4 h-4 ml-1" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
