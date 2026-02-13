'use client';

import { useState } from 'react';
import { Save, Eye, EyeOff, Key, Globe, Database } from 'lucide-react';

export default function SettingsPage() {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handlePasswordChange = (e: React.FormEvent) => {
    e.preventDefault();
    // In production, this would update the password in the database
    if (newPassword.length >= 6) {
      setMessage({ type: 'success', text: 'Password updated successfully! (Note: This is a demo - changes are not persisted)' });
    } else {
      setMessage({ type: 'error', text: 'Password must be at least 6 characters' });
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-500">Manage your admin panel settings</p>
      </div>

      {message && (
        <div className={`px-4 py-3 rounded-lg ${message.type === 'success' ? 'bg-green-50 border border-green-200 text-green-700' : 'bg-red-50 border border-red-200 text-red-700'}`}>
          {message.text}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Password Settings */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Key className="w-5 h-5" />
            Admin Password
          </h2>
          
          <form onSubmit={handlePasswordChange} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Current Password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none pr-10"
                  placeholder="Enter current password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">New Password</label>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                placeholder="Enter new password"
              />
            </div>
            
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Update Password
            </button>
          </form>
          
          <p className="mt-4 text-xs text-gray-500">
            Current password: <code className="bg-gray-100 px-1 rounded">brizl2024admin</code>
          </p>
        </div>

        {/* Domain Info */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Globe className="w-5 h-5" />
            Domain Configuration
          </h2>
          
          <div className="space-y-4">
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500 mb-1">Admin Panel URL</p>
              <p className="font-mono text-blue-600">https://admin-brizl.baysart.com</p>
            </div>
            
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500 mb-1">Main Website</p>
              <p className="font-mono text-blue-600">https://baysart.com</p>
            </div>
            
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800">
                To configure the domain, add the following DNS record:
              </p>
              <code className="block mt-2 text-xs bg-yellow-100 p-2 rounded">
                CNAME admin-brizl → [your-server-ip]
              </code>
            </div>
          </div>
        </div>

        {/* Database Info */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Database className="w-5 h-5" />
            Database Connection
          </h2>
          
          <div className="space-y-3">
            <div className="flex justify-between py-2 border-b border-gray-100">
              <span className="text-gray-500">Host</span>
              <span className="font-mono text-sm">{process.env.DB_HOST || 'localhost'}</span>
            </div>
            <div className="flex justify-between py-2 border-b border-gray-100">
              <span className="text-gray-500">Port</span>
              <span className="font-mono text-sm">{process.env.DB_PORT || '5432'}</span>
            </div>
            <div className="flex justify-between py-2 border-b border-gray-100">
              <span className="text-gray-500">Database</span>
              <span className="font-mono text-sm">{process.env.DB_NAME || 'briz-l'}</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-gray-500">Status</span>
              <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                Connected
              </span>
            </div>
          </div>
        </div>

        {/* System Info */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">System Information</h2>
          
          <div className="space-y-3">
            <div className="flex justify-between py-2 border-b border-gray-100">
              <span className="text-gray-500">Version</span>
              <span className="font-mono text-sm">1.0.0</span>
            </div>
            <div className="flex justify-between py-2 border-b border-gray-100">
              <span className="text-gray-500">Framework</span>
              <span className="font-mono text-sm">Next.js 15</span>
            </div>
            <div className="flex justify-between py-2 border-b border-gray-100">
              <span className="text-gray-500">AI Model</span>
              <span className="font-mono text-sm">GPT-4o-mini</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-gray-500">Bot Name</span>
              <span className="font-mono text-sm">VERA</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}