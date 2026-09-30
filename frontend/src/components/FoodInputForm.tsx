import React, { useState, useEffect } from 'react';
import { AnalyzeRequest } from '../types';
import { fetchCategories, fetchFoods } from '../services/api';
import { Search, Sliders } from 'lucide-react';

interface Props {
  formData: AnalyzeRequest;
  setFormData: React.Dispatch<React.SetStateAction<AnalyzeRequest>>;
  onAnalyze: () => void;
  loading: boolean;
}

const FSSAI_DEFAULT_CATEGORIES = [
  'Animal Meat',
  'Beverages (other than Dairy and Fruits & Vegetables based)',
  'Cereals and Millets',
  'Cereals and cereal products',
  'Condiments and Spices',
  'Dairy',
  'Egg and Egg Products',
  'Fats, oils and fat emulsions',
  'Fish and fish products or Seafood',
  'Freshwater Fish and Shellfish',
  'Fruit & Vegetable products',
  'Grain Legumes',
  'Green Leafy Vegetables',
  'Marine Fish',
  'Meat and Meat Products or Poultry Products',
  'Milk and Milk Products',
  'Miscellaneous Foods (beverages)',
  'Mushrooms',
  'Nuts and Oil Seeds',
  'Other Vegetables',
  'Poultry',
  'Ready-to-eat meal',
  'Roots and Tubers',
  'Salt, spices, Condiments and related products',
  'Sweetening agents including Honey',
  'Sweets and Confectionery'
];

export const FoodInputForm: React.FC<Props> = ({ formData, setFormData, onAnalyze, loading }) => {
  const [categories, setCategories] = useState<string[]>(FSSAI_DEFAULT_CATEGORIES);
  const [foodSearchQuery, setFoodSearchQuery] = useState('');
  const [foodSuggestions, setFoodSuggestions] = useState<any[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    fetchCategories()
      .then((res) => {
        if (Array.isArray(res) && res.length > 0) {
          setCategories(res);
        }
      })
      .catch(console.error);
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



  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-sm mb-8">

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
