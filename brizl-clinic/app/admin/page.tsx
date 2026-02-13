'use client';

import { useState, useEffect } from 'react';
import {
  Users,
  Flame,
  TrendingUp,
  Calendar,
  Eye,
  Phone,
  MessageSquare,
  ChevronRight,
  RefreshCw
} from 'lucide-react';
import Link from 'next/link';

interface LeadStats {
  total_leads: number;
  hot_leads: number;
  today_leads: number;
  warm_leads: number;
  cold_leads: number;
  new_leads: number;
  converted: number;
}

interface HotLead {
  user_id: string;
  lead_score: number;
  last_interaction: string;
  surgeries_interested: string[];
  booking_intent_detected: boolean;
}

interface TopSurgery {
  surgery: string;
  inquiry_count: number;
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

export default function AdminDashboard() {
  const [stats, setStats] = useState<LeadStats | null>(null);
  const [hotLeads, setHotLeads] = useState<HotLead[]>([]);
  const [topSurgeries, setTopSurgeries] = useState<TopSurgery[]>([]);
  const [funnel, setFunnel] = useState<FunnelData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const [statsRes, hotRes, surgeriesRes, funnelRes] = await Promise.all([
        fetch('/admin/api/stats'),
        fetch('/admin/api/hot-leads'),
        fetch('/admin/api/top-surgeries'),
        fetch('/admin/api/funnel'),
      ]);

      if (statsRes.ok) setStats(await statsRes.json());
      if (hotRes.ok) setHotLeads(await hotRes.json());
      if (surgeriesRes.ok) setTopSurgeries(await surgeriesRes.json());
      if (funnelRes.ok) setFunnel(await funnelRes.json());
    } catch (err) {
      setError('Failed to load data. Please check database connection.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('az-AZ', {
      day: '2-digit',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const truncateId = (id: string) => {
    return id.length > 15 ? id.substring(0, 15) + '...' : id;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500">Welcome back, Seljan! Here's your clinic overview.</p>
        </div>
        <button
          onClick={fetchData}
          className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total Leads</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.total_leads || 0}</p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
              <Users className="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-green-600 font-medium">+{stats?.today_leads || 0}</span>
            <span className="text-gray-500 ml-1">today</span>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Hot Leads</p>
              <p className="text-3xl font-bold text-orange-600">{stats?.hot_leads || 0}</p>
            </div>
            <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
              <Flame className="w-6 h-6 text-orange-600" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-gray-500">Ready to convert</span>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Conversion Rate</p>
              <p className="text-3xl font-bold text-green-600">{funnel?.rates.conversion_rate || 0}%</p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-green-600" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-gray-500">{stats?.converted || 0} converted</span>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Booking Intents</p>
              <p className="text-3xl font-bold text-purple-600">{funnel?.funnel.booking_intents || 0}</p>
            </div>
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
              <Calendar className="w-6 h-6 text-purple-600" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-gray-500">{funnel?.rates.intent_rate || 0}% of leads</span>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Conversion Funnel */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Conversion Funnel</h2>
          {funnel && (
            <div className="space-y-4">
              {[
                { label: 'Total Leads', value: funnel.funnel.total_leads, color: 'bg-blue-500', width: 100 },
                { label: 'Engaged (3+ msgs)', value: funnel.funnel.engaged_leads, color: 'bg-blue-400', width: Math.max(10, (funnel.funnel.engaged_leads / funnel.funnel.total_leads) * 100) || 10 },
                { label: 'Hot Leads', value: funnel.funnel.hot_leads, color: 'bg-orange-500', width: Math.max(10, (funnel.funnel.hot_leads / funnel.funnel.total_leads) * 100) || 10 },
                { label: 'Booking Intent', value: funnel.funnel.booking_intents, color: 'bg-purple-500', width: Math.max(10, (funnel.funnel.booking_intents / funnel.funnel.total_leads) * 100) || 10 },
                { label: 'Converted', value: funnel.funnel.converted, color: 'bg-green-500', width: Math.max(10, (funnel.funnel.converted / funnel.funnel.total_leads) * 100) || 10 },
              ].map((item, idx) => (
                <div key={idx}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">{item.label}</span>
                    <span className="font-medium">{item.value}</span>
                  </div>
                  <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${item.color} rounded-full transition-all duration-500`}
                      style={{ width: `${item.width}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Top Surgeries */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Top Inquiries</h2>
          <div className="space-y-3">
            {topSurgeries.length > 0 ? (
              topSurgeries.slice(0, 5).map((surgery, idx) => (
                <div key={idx} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium">
                      {idx + 1}
                    </span>
                    <span className="text-gray-700 text-sm">{surgery.surgery}</span>
                  </div>
                  <span className="text-gray-500 text-sm">{surgery.inquiry_count}</span>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-sm">No surgery data yet</p>
            )}
          </div>
        </div>
      </div>

      {/* Hot Leads Table */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        <div className="p-6 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">🔥 Hot Leads</h2>
          <Link
            href="/admin/leads?status=hot"
            className="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center gap-1"
          >
            View all <ChevronRight className="w-4 h-4" />
          </Link>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Interested In</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Active</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {hotLeads.length > 0 ? (
                hotLeads.map((lead) => (
                  <tr key={lead.user_id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-medium text-gray-900">{truncateId(lead.user_id)}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        lead.lead_score >= 80 ? 'bg-red-100 text-red-800' :
                        lead.lead_score >= 60 ? 'bg-orange-100 text-orange-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {lead.lead_score}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-wrap gap-1">
                        {lead.surgeries_interested?.slice(0, 2).map((s, i) => (
                          <span key={i} className="inline-block px-2 py-0.5 bg-gray-100 text-gray-700 rounded text-xs">
                            {s}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDate(lead.last_interaction)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <Link
                          href={`/admin/conversations/${lead.user_id}`}
                          className="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded"
                        >
                          <Eye className="w-4 h-4" />
                        </Link>
                        <a
                          href={`https://wa.me/${lead.user_id.replace(/\D/g, '')}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="p-1.5 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded"
                        >
                          <MessageSquare className="w-4 h-4" />
                        </a>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-gray-500">
                    No hot leads yet. Keep engaging with your visitors!
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Lead Status Distribution */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'New', count: stats?.new_leads || 0, color: 'bg-blue-500' },
          { label: 'Cold', count: stats?.cold_leads || 0, color: 'bg-gray-400' },
          { label: 'Warm', count: stats?.warm_leads || 0, color: 'bg-yellow-500' },
          { label: 'Hot', count: stats?.hot_leads || 0, color: 'bg-orange-500' },
        ].map((status) => (
          <div key={status.label} className="bg-white rounded-xl border border-gray-200 p-4 flex items-center gap-4">
            <div className={`w-3 h-3 ${status.color} rounded-full`} />
            <div>
              <p className="text-2xl font-bold text-gray-900">{status.count}</p>
              <p className="text-sm text-gray-500">{status.label}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}