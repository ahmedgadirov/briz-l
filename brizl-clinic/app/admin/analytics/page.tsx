'use client';

import { useState, useEffect } from 'react';
import { TrendingUp, Users, Calendar, BarChart3 } from 'lucide-react';

interface DailyStat {
  date: string;
  total_leads: number;
  hot_leads: number;
  booking_intents: number;
  follow_ups_sent: number;
  follow_up_responses: number;
}

interface FunnelData {
  funnel: {
    total_leads: number;
    engaged_leads: number;
    hot_leads: number;
    booking_intents: number;
    converted: number;
  };
  rates: {
    engagement_rate: number;
    hot_lead_rate: number;
    intent_rate: number;
    conversion_rate: number;
  };
}

interface TopSurgery {
  surgery: string;
  inquiry_count: number;
}

export default function AnalyticsPage() {
  const [dailyStats, setDailyStats] = useState<DailyStat[]>([]);
  const [funnel, setFunnel] = useState<FunnelData | null>(null);
  const [topSurgeries, setTopSurgeries] = useState<TopSurgery[]>([]);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('7');

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const [dailyRes, funnelRes, surgeriesRes] = await Promise.all([
        fetch(`/admin/api/daily-stats?days=${timeRange}`),
        fetch('/admin/api/funnel'),
        fetch('/admin/api/top-surgeries'),
      ]);

      if (dailyRes.ok) setDailyStats(await dailyRes.json());
      if (funnelRes.ok) setFunnel(await funnelRes.json());
      if (surgeriesRes.ok) setTopSurgeries(await surgeriesRes.json());
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('az-AZ', { day: '2-digit', month: 'short' });
  };

  const maxLeads = Math.max(...dailyStats.map(d => d.total_leads), 1);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-500">Detailed marketing performance metrics</p>
        </div>
        <select
          value={timeRange}
          onChange={(e) => setTimeRange(e.target.value)}
          className="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
        >
          <option value="7">Last 7 days</option>
          <option value="14">Last 14 days</option>
          <option value="30">Last 30 days</option>
        </select>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <>
          {/* Conversion Funnel */}
          {funnel && (
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Conversion Funnel
              </h2>
              
              <div className="grid grid-cols-5 gap-4 mb-6">
                {[
                  { label: 'Total', value: funnel.funnel.total_leads, rate: '100%', color: 'bg-blue-500' },
                  { label: 'Engaged', value: funnel.funnel.engaged_leads, rate: `${funnel.rates.engagement_rate}%`, color: 'bg-blue-400' },
                  { label: 'Hot', value: funnel.funnel.hot_leads, rate: `${funnel.rates.hot_lead_rate}%`, color: 'bg-orange-500' },
                  { label: 'Intent', value: funnel.funnel.booking_intents, rate: `${funnel.rates.intent_rate}%`, color: 'bg-purple-500' },
                  { label: 'Converted', value: funnel.funnel.converted, rate: `${funnel.rates.conversion_rate}%`, color: 'bg-green-500' },
                ].map((stage, idx) => (
                  <div key={idx} className="text-center">
                    <div className={`mx-auto w-16 h-16 ${stage.color} rounded-full flex items-center justify-center text-white font-bold text-lg mb-2`}>
                      {stage.value}
                    </div>
                    <p className="font-medium text-gray-900">{stage.label}</p>
                    <p className="text-sm text-gray-500">{stage.rate}</p>
                    {idx < 4 && (
                      <div className="hidden md:block absolute right-0 top-1/2 -translate-y-1/2 text-gray-300">
                        →
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Visual Funnel */}
              <div className="space-y-2">
                {[
                  { label: 'Total Leads', value: funnel.funnel.total_leads, total: funnel.funnel.total_leads, color: 'bg-blue-500' },
                  { label: 'Engaged (3+ msgs)', value: funnel.funnel.engaged_leads, total: funnel.funnel.total_leads, color: 'bg-blue-400' },
                  { label: 'Hot Leads', value: funnel.funnel.hot_leads, total: funnel.funnel.total_leads, color: 'bg-orange-500' },
                  { label: 'Booking Intent', value: funnel.funnel.booking_intents, total: funnel.funnel.total_leads, color: 'bg-purple-500' },
                  { label: 'Converted', value: funnel.funnel.converted, total: funnel.funnel.total_leads, color: 'bg-green-500' },
                ].map((stage, idx) => (
                  <div key={idx} className="flex items-center gap-4">
                    <div className="w-32 text-sm text-gray-600">{stage.label}</div>
                    <div className="flex-1 h-8 bg-gray-100 rounded-lg overflow-hidden">
                      <div
                        className={`h-full ${stage.color} rounded-lg transition-all duration-500 flex items-center justify-end pr-3`}
                        style={{ width: `${Math.max(5, (stage.value / stage.total) * 100)}%` }}
                      >
                        <span className="text-white text-sm font-medium">{stage.value}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Daily Leads Chart */}
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <BarChart3 className="w-5 h-5" />
                Daily Leads
              </h2>
              
              <div className="space-y-3">
                {dailyStats.length > 0 ? (
                  dailyStats.map((day, idx) => (
                    <div key={idx} className="flex items-center gap-4">
                      <div className="w-16 text-sm text-gray-500">{formatDate(day.date)}</div>
                      <div className="flex-1 h-6 bg-gray-100 rounded overflow-hidden">
                        <div
                          className="h-full bg-blue-500 rounded transition-all duration-300"
                          style={{ width: `${(day.total_leads / maxLeads) * 100}%` }}
                        />
                      </div>
                      <div className="w-12 text-sm font-medium text-right">{day.total_leads}</div>
                    </div>
                  ))
                ) : (
                  <p className="text-gray-500 text-center py-4">No data available</p>
                )}
              </div>
            </div>

            {/* Top Surgeries */}
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Top Surgery Inquiries</h2>
              
              <div className="space-y-3">
                {topSurgeries.length > 0 ? (
                  topSurgeries.map((surgery, idx) => {
                    const maxCount = topSurgeries[0]?.inquiry_count || 1;
                    return (
                      <div key={idx}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-700">{surgery.surgery}</span>
                          <span className="font-medium">{surgery.inquiry_count}</span>
                        </div>
                        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-purple-500 rounded-full transition-all duration-300"
                            style={{ width: `${(surgery.inquiry_count / maxCount) * 100}%` }}
                          />
                        </div>
                      </div>
                    );
                  })
                ) : (
                  <p className="text-gray-500 text-center py-4">No surgery data yet</p>
                )}
              </div>
            </div>
          </div>

          {/* Daily Stats Table */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                <Calendar className="w-5 h-5" />
                Daily Breakdown
              </h2>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">New Leads</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Hot Leads</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Booking Intents</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Follow-ups</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Responses</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {dailyStats.length > 0 ? (
                    dailyStats.map((day, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        <td className="px-6 py-4 text-sm font-medium text-gray-900">{formatDate(day.date)}</td>
                        <td className="px-6 py-4 text-sm text-gray-700">{day.total_leads}</td>
                        <td className="px-6 py-4 text-sm">
                          <span className="text-orange-600 font-medium">{day.hot_leads}</span>
                        </td>
                        <td className="px-6 py-4 text-sm">
                          <span className="text-purple-600 font-medium">{day.booking_intents}</span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-700">{day.follow_ups_sent}</td>
                        <td className="px-6 py-4 text-sm text-gray-700">{day.follow_up_responses}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                        No data available
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}