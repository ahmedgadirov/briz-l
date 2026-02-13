'use client';

import { useState, useEffect } from 'react';
import { Search, MessageSquare, User, Calendar } from 'lucide-react';
import Link from 'next/link';

interface Conversation {
  user_id: string;
  first_contact: string;
  last_interaction: string;
  total_messages: number;
  lead_score: number;
  lead_status: string;
  surgeries_interested: string[];
}

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const response = await fetch('/admin/api/leads?limit=50');
      const data = await response.json();
      if (response.ok) {
        setConversations(data.leads || []);
      }
    } catch (error) {
      console.error('Error fetching conversations:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('az-AZ', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    });
  };

  const filteredConversations = conversations.filter(conv =>
    searchQuery === '' ||
    conv.user_id.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Conversations</h1>
          <p className="text-gray-500">View all chat histories</p>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white rounded-xl border border-gray-200 p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search by user ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
          />
        </div>
      </div>

      {/* Conversations List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {loading ? (
          <div className="col-span-full flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : filteredConversations.length > 0 ? (
          filteredConversations.map((conv) => (
            <Link
              key={conv.user_id}
              href={`/admin/conversations/${conv.user_id}`}
              className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900 text-sm">
                      {conv.user_id.length > 20 ? conv.user_id.substring(0, 20) + '...' : conv.user_id}
                    </p>
                    <p className="text-xs text-gray-500">{conv.total_messages} messages</p>
                  </div>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  conv.lead_status === 'hot' ? 'bg-red-100 text-red-700' :
                  conv.lead_status === 'warm' ? 'bg-yellow-100 text-yellow-700' :
                  conv.lead_status === 'converted' ? 'bg-green-100 text-green-700' :
                  'bg-gray-100 text-gray-700'
                }`}>
                  {conv.lead_status}
                </span>
              </div>

              <div className="flex items-center gap-4 text-xs text-gray-500">
                <div className="flex items-center gap-1">
                  <Calendar className="w-3 h-3" />
                  {formatDate(conv.last_interaction)}
                </div>
                <div className="flex items-center gap-1">
                  <MessageSquare className="w-3 h-3" />
                  Score: {conv.lead_score}
                </div>
              </div>

              {conv.surgeries_interested?.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-1">
                  {conv.surgeries_interested.slice(0, 2).map((s, i) => (
                    <span key={i} className="px-2 py-0.5 bg-blue-50 text-blue-700 rounded text-xs">
                      {s}
                    </span>
                  ))}
                  {conv.surgeries_interested.length > 2 && (
                    <span className="text-gray-400 text-xs">+{conv.surgeries_interested.length - 2}</span>
                  )}
                </div>
              )}
            </Link>
          ))
        ) : (
          <div className="col-span-full text-center py-12 text-gray-500">
            No conversations found
          </div>
        )}
      </div>
    </div>
  );
}