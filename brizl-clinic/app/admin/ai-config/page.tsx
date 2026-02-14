'use client';

import { useState, useEffect } from 'react';
import { Save, RefreshCw, Plus, Trash2, ChevronDown, ChevronUp } from 'lucide-react';

interface Doctor {
  name: string;
  title: string;
  phone: string;
  whatsapp: string;
}

interface Surgery {
  name: string;
  description: string;
}

interface ScoringWeights {
  price_inquiry: number;
  doctor_inquiry: number;
  surgery_inquiry: number;
  symptom_mentioned: number;
  booking_intent: number;
  multiple_messages: number;
  return_visit: number;
  urgent_symptoms: number;
}

const DEFAULT_DOCTORS: Doctor[] = [
  { name: 'Dr. İltifat Şərif', title: 'Baş həkim, Oftalmoloq', phone: '010 710 74 65', whatsapp: '994107107465' },
  { name: 'Dr. Emil Qafarlı', title: 'Oftalmoloq', phone: '051 844 76 21', whatsapp: '994518447621' },
  { name: 'Dr. Səbinə Əbiyeva', title: 'Oftalmoloq', phone: '055 319 75 76', whatsapp: '994553197576' },
  { name: 'Dr. Seymur Bayramov', title: 'Oftalmoloq', phone: '070 505 00 01', whatsapp: '994705050001' },
];

const DEFAULT_SURGERIES: Surgery[] = [
  { name: 'Excimer laser', description: 'Gözlük/lenslərdən azadlıq, yaxın/uzaq görmə düzəlişi' },
  { name: 'Katarakta (mirvari suyu)', description: 'Göz lensinin dəyişdirilməsi, dumanlı görmə' },
  { name: 'Pteregium', description: 'Göz ağında toxuma təmizlənməsi' },
  { name: 'Phacic', description: 'Gözə süni lens yerləşdirilməsi' },
  { name: 'Çəplik', description: 'Göz əzələsi düzəlişi' },
  { name: 'Cross linking', description: 'Buynuz qişası möhkəmləndirilməsi (keratokonus)' },
  { name: 'Arqon laser', description: 'Göz dibi müalicəsi (retina, diabet)' },
  { name: 'YAG laser', description: 'Katarakta sonrası kapsul təmizlənməsi' },
  { name: 'Avastin', description: 'Göz dibinə iynə (makula, diabetik retinopatiya)' },
  { name: 'Qlaukoma (qara su)', description: 'Qara su əməliyyatı' },
];

const DEFAULT_SCORING: ScoringWeights = {
  price_inquiry: 30,
  doctor_inquiry: 20,
  surgery_inquiry: 15,
  symptom_mentioned: 25,
  booking_intent: 40,
  multiple_messages: 10,
  return_visit: 15,
  urgent_symptoms: 35,
};

const DEFAULT_PROMPT = `Sən "Briz-L Göz Klinikası"nın AĞILLI süni intellekt köməkçisisən - tibbi köməkçi və MÜŞTƏRİ CƏLBEDİCİSİ.
Adın: VERA (Virtual Eye-care Representative Assistant)
Məqsəd: Briz-L Göz Klinikasının müştərilərinə professional və empatik xidmət

**ƏSAS MİSSİYAN:**
- Hər istifadəçinin bilgi səviyyəsini başa düş (başlayan/orta/ekspert)
- Simptomları dinlə, DİAQNOSTİK suallar ver
- TƏCİLİ vəziyyətləri tanı
- Uyğun bələdçilik və tövsiyələr ver
- Peşəkar TİBBİ KÖMƏKÇI kimi davran
- **MÜAYİNƏYƏ YÖNLƏNDİR və MÜŞTƏRİ QAZANMAĞA ÇALIŞ**`;

export default function AIConfigPage() {
  const [systemPrompt, setSystemPrompt] = useState(DEFAULT_PROMPT);
  const [doctors, setDoctors] = useState<Doctor[]>(DEFAULT_DOCTORS);
  const [surgeries, setSurgeries] = useState<Surgery[]>(DEFAULT_SURGERIES);
  const [scoring, setScoring] = useState<ScoringWeights>(DEFAULT_SCORING);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [expandedSections, setExpandedSections] = useState({
    prompt: true,
    doctors: false,
    surgeries: false,
    scoring: false,
  });

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    setLoading(true);
    try {
      const response = await fetch('/admin/api/ai-config');
      if (response.ok) {
        const data = await response.json();
        if (data) {
          if (data.system_prompt) setSystemPrompt(data.system_prompt);
          if (data.doctors) setDoctors(data.doctors);
          if (data.surgeries) setSurgeries(data.surgeries);
          if (data.scoring_weights) setScoring(data.scoring_weights);
        }
      }
    } catch (error) {
      console.error('Error fetching config:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage(null);
    try {
      const response = await fetch('/admin/api/ai-config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          system_prompt: systemPrompt,
          doctors,
          surgeries,
          scoring_weights: scoring,
        }),
      });

      if (response.ok) {
        setMessage({ type: 'success', text: 'Configuration saved successfully!' });
      } else {
        setMessage({ type: 'error', text: 'Failed to save configuration' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to save configuration' });
    } finally {
      setSaving(false);
    }
  };

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  const updateDoctor = (index: number, field: keyof Doctor, value: string) => {
    const newDoctors = [...doctors];
    newDoctors[index] = { ...newDoctors[index], [field]: value };
    setDoctors(newDoctors);
  };

  const addDoctor = () => {
    setDoctors([...doctors, { name: '', title: '', phone: '', whatsapp: '' }]);
  };

  const removeDoctor = (index: number) => {
    setDoctors(doctors.filter((_, i) => i !== index));
  };

  const updateSurgery = (index: number, field: keyof Surgery, value: string) => {
    const newSurgeries = [...surgeries];
    newSurgeries[index] = { ...newSurgeries[index], [field]: value };
    setSurgeries(newSurgeries);
  };

  const addSurgery = () => {
    setSurgeries([...surgeries, { name: '', description: '' }]);
  };

  const removeSurgery = (index: number) => {
    setSurgeries(surgeries.filter((_, i) => i !== index));
  };

  const updateScoring = (field: keyof ScoringWeights, value: number) => {
    setScoring({ ...scoring, [field]: value });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">AI Configuration</h1>
          <p className="text-gray-500">Customize Vera's behavior and knowledge</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchConfig}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Reset
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            className="flex items-center gap-2 px-4 py-2 bg-mint text-white rounded-lg hover:bg-mint-dark transition-colors"
          >
            <Save className="w-4 h-4" />
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </div>

      {message && (
        <div className={`px-4 py-3 rounded-lg ${message.type === 'success' ? 'bg-green-50 border border-green-200 text-green-700' : 'bg-red-50 border border-red-200 text-red-700'}`}>
          {message.text}
        </div>
      )}

      {/* System Prompt */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <button
          onClick={() => toggleSection('prompt')}
          className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50"
        >
          <div className="text-left">
            <h2 className="text-lg font-semibold text-gray-900">System Prompt</h2>
            <p className="text-sm text-gray-500">Main AI personality and instructions</p>
          </div>
          {expandedSections.prompt ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        {expandedSections.prompt && (
          <div className="px-6 pb-6">
            <textarea
              value={systemPrompt}
              onChange={(e) => setSystemPrompt(e.target.value)}
              rows={20}
              className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-mint focus:border-transparent outline-none font-mono text-sm"
              placeholder="Enter system prompt..."
            />
          </div>
        )}
      </div>

      {/* Doctors */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <button
          onClick={() => toggleSection('doctors')}
          className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50"
        >
          <div className="text-left">
            <h2 className="text-lg font-semibold text-gray-900">Doctors</h2>
            <p className="text-sm text-gray-500">{doctors.length} doctors configured</p>
          </div>
          {expandedSections.doctors ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        {expandedSections.doctors && (
          <div className="px-6 pb-6 space-y-4">
            {doctors.map((doctor, index) => (
              <div key={index} className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg">
                <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input
                    type="text"
                    value={doctor.name}
                    onChange={(e) => updateDoctor(index, 'name', e.target.value)}
                    placeholder="Name"
                    className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                  <input
                    type="text"
                    value={doctor.title}
                    onChange={(e) => updateDoctor(index, 'title', e.target.value)}
                    placeholder="Title"
                    className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                  <input
                    type="text"
                    value={doctor.phone}
                    onChange={(e) => updateDoctor(index, 'phone', e.target.value)}
                    placeholder="Phone"
                    className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                  <input
                    type="text"
                    value={doctor.whatsapp}
                    onChange={(e) => updateDoctor(index, 'whatsapp', e.target.value)}
                    placeholder="WhatsApp"
                    className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                </div>
                <button
                  onClick={() => removeDoctor(index)}
                  className="p-2 text-red-500 hover:bg-red-50 rounded-lg"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            ))}
            <button
              onClick={addDoctor}
              className="flex items-center gap-2 px-4 py-2 text-mint hover:bg-mint/10 rounded-lg"
            >
              <Plus className="w-4 h-4" />
              Add Doctor
            </button>
          </div>
        )}
      </div>

      {/* Surgeries */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <button
          onClick={() => toggleSection('surgeries')}
          className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50"
        >
          <div className="text-left">
            <h2 className="text-lg font-semibold text-gray-900">Surgeries</h2>
            <p className="text-sm text-gray-500">{surgeries.length} procedures configured</p>
          </div>
          {expandedSections.surgeries ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        {expandedSections.surgeries && (
          <div className="px-6 pb-6 space-y-4">
            {surgeries.map((surgery, index) => (
              <div key={index} className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg">
                <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-4">
                  <input
                    type="text"
                    value={surgery.name}
                    onChange={(e) => updateSurgery(index, 'name', e.target.value)}
                    placeholder="Surgery name"
                    className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                  <input
                    type="text"
                    value={surgery.description}
                    onChange={(e) => updateSurgery(index, 'description', e.target.value)}
                    placeholder="Description"
                    className="md:col-span-2 px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                </div>
                <button
                  onClick={() => removeSurgery(index)}
                  className="p-2 text-red-500 hover:bg-red-50 rounded-lg"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            ))}
            <button
              onClick={addSurgery}
              className="flex items-center gap-2 px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg"
            >
              <Plus className="w-4 h-4" />
              Add Surgery
            </button>
          </div>
        )}
      </div>

      {/* Scoring Weights */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <button
          onClick={() => toggleSection('scoring')}
          className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50"
        >
          <div className="text-left">
            <h2 className="text-lg font-semibold text-gray-900">Lead Scoring Weights</h2>
            <p className="text-sm text-gray-500">Points assigned for different user actions</p>
          </div>
          {expandedSections.scoring ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        {expandedSections.scoring && (
          <div className="px-6 pb-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {Object.entries(scoring).map(([key, value]) => (
                <div key={key}>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-sm font-medium text-gray-700">
                      {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </label>
                    <span className="text-sm font-bold text-blue-600">{value} pts</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="50"
                    value={value}
                    onChange={(e) => updateScoring(key as keyof ScoringWeights, parseInt(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}