'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, User, MessageSquare, Calendar, Phone, Mail } from 'lucide-react';
import Link from 'next/link';

interface Message {
  timestamp: string;
  message: string;
  items?: any;
}

interface LeadDetail {
  user_id: string;
  first_contact: string;
  last_interaction: string;
  total_messages: number;
  symptoms: string[];
  surgeries_interested: string[];
  doctors_inquired: string[];
  lead_score: number;
  lead_status: string;
  booking_intent_detected: boolean;
  conversation_history: Message[];
}

export default function ConversationDetailPage() {
  const params = useParams();
  const router = useRouter();
  const userId = params.id as string;
  
  const [lead, setLead] = useState<LeadDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeadDetails();
  }, [userId]);

  const fetchLeadDetails = async () => {
    try {
      const response = await fetch(`/admin/api/leads/${encodeURIComponent(userId)}`);
      if (response.ok) {
        const data = await response.json();
        setLead(data);
      }
    } catch (error) {
      console.error('Error fetching lead details:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('az-AZ', {
      day: '2-digit',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('az-AZ', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!lead) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Conversation not found</p>
        <Link href="/admin/conversations" className="text-blue-600 mt-2 inline-block">
          ← Back to conversations
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => router.back()}
          className="p-2 hover:bg-gray-100 rounded-lg"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div className="flex-1">
          <h1 className="text-2xl font-bold text-gray-900">Conversation Details</h1>
          <p className="text-gray-500 text-sm">{lead.user_id}</p>
        </div>
        <a
          href={`https://wa.me/${lead.user_id.replace(/\D/g, '')}`}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
        >
          <MessageSquare className="w-4 h-4" />
          WhatsApp
        </a>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Lead Info */}
        <div className="space-y-4">
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <User className="w-5 h-5" />
              Lead Information
            </h2>
            
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-500">Status</span>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  lead.lead_status === 'hot' ? 'bg-red-100 text-red-700' :
                  lead.lead_status === 'warm' ? 'bg-yellow-100 text-yellow-700' :
                  lead.lead_status === 'converted' ? 'bg-green-100 text-green-700' :
                  'bg-gray-100 text-gray-700'
                }`}>
                  {lead.lead_status}
                </span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-gray-500">Score</span>
                <span className="font-medium">{lead.lead_score}/100</span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-gray-500">Messages</span>
                <span className="font-medium">{lead.total_messages}</span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-gray-500">Booking Intent</span>
                <span className={`font-medium ${lead.booking_intent_detected ? 'text-green-600' : 'text-gray-400'}`}>
                  {lead.booking_intent_detected ? 'Yes' : 'No'}
                </span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-gray-500">First Contact</span>
                <span className="text-sm">{formatDate(lead.first_contact)}</span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-gray-500">Last Active</span>
                <span className="text-sm">{formatDate(lead.last_interaction)}</span>
              </div>
            </div>
          </div>

          {/* Interested In */}
          {lead.surgeries_interested?.length > 0 && (
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <h2 className="font-semibold text-gray-900 mb-3">Interested Surgeries</h2>
              <div className="flex flex-wrap gap-2">
                {lead.surgeries_interested.map((surgery, i) => (
                  <span key={i} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">
                    {surgery}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Symptoms */}
          {lead.symptoms?.length > 0 && (
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <h2 className="font-semibold text-gray-900 mb-3">Mentioned Symptoms</h2>
              <div className="flex flex-wrap gap-2">
                {lead.symptoms.map((symptom, i) => (
                  <span key={i} className="px-3 py-1 bg-red-50 text-red-700 rounded-full text-sm">
                    {symptom}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Doctors Inquired */}
          {lead.doctors_inquired?.length > 0 && (
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <h2 className="font-semibold text-gray-900 mb-3">Doctors Inquired</h2>
              <div className="flex flex-wrap gap-2">
                {lead.doctors_inquired.map((doctor, i) => (
                  <span key={i} className="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-sm">
                    {doctor}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Conversation History */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <div className="px-5 py-4 border-b border-gray-200">
              <h2 className="font-semibold text-gray-900 flex items-center gap-2">
                <MessageSquare className="w-5 h-5" />
                Conversation History
              </h2>
            </div>
            
            <div className="p-5 space-y-4 max-h-[600px] overflow-y-auto">
              {lead.conversation_history?.length > 0 ? (
                lead.conversation_history.map((msg, index) => (
                  <div key={index} className="space-y-3">
                    {/* User Message */}
                    <div className="flex justify-end">
                      <div className="max-w-[80%] bg-blue-600 text-white rounded-2xl rounded-br-md px-4 py-2">
                        <p className="text-sm">{msg.message}</p>
                        <p className="text-xs text-blue-200 mt-1">{formatTime(msg.timestamp)}</p>
                      </div>
                    </div>
                    
                    {/* Detected Items */}
                    {msg.items && Object.keys(msg.items).length > 0 && (
                      <div className="flex justify-end">
                        <div className="max-w-[80%] bg-gray-100 rounded-lg px-3 py-2 text-xs text-gray-600">
                          {msg.items.surgeries?.length > 0 && (
                            <span>Surgeries: {msg.items.surgeries.join(', ')} | </span>
                          )}
                          {msg.items.symptoms?.length > 0 && (
                            <span>Symptoms: {msg.items.symptoms.join(', ')} | </span>
                          )}
                          {msg.items.booking_intent && (
                            <span className="text-green-600 font-medium">Booking Intent!</span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-gray-500">
                  No conversation history available
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}