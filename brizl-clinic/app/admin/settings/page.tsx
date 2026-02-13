'use client';

import { useState, useEffect } from 'react';
import { Eye, EyeOff, Key, Globe, Database, RefreshCw, CheckCircle, XCircle, Table } from 'lucide-react';

interface TableStat {
  table: string;
  count: number;
}

export default function SettingsPage() {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  
  // Database migration state
  const [dbConnected, setDbConnected] = useState<boolean | null>(null);
  const [dbError, setDbError] = useState<string | null>(null);
  const [tableStats, setTableStats] = useState<TableStat[]>([]);
  const [migrating, setMigrating] = useState(false);
  const [migrationResult, setMigrationResult] = useState<{ success: boolean; message: string } | null>(null);

  useEffect(() => {
    checkDatabaseStatus();
  }, []);

  const checkDatabaseStatus = async () => {
    try {
      const response = await fetch('/admin/api/migrate');
      const data = await response.json();
      
      setDbConnected(data.success);
      if (data.success) {
        setTableStats(data.tables || []);
        setDbError(null);
      } else {
        setDbError(data.details || data.error);
      }
    } catch (error) {
      setDbConnected(false);
      setDbError('Failed to connect to database');
    }
  };

  const runMigrations = async () => {
    setMigrating(true);
    setMigrationResult(null);
    
    try {
      const response = await fetch('/admin/api/migrate', { method: 'POST' });
      const data = await response.json();
      
      setMigrationResult({
        success: data.success,
        message: data.success 
          ? `Migration complete! Tables created: ${data.tables_created?.join(', ')}`
          : data.error || 'Migration failed'
      });
      
      if (data.success) {
        setTableStats(data.table_stats || []);
        setDbConnected(true);
        setDbError(null);
      }
    } catch (error) {
      setMigrationResult({
        success: false,
        message: 'Failed to run migrations'
      });
    } finally {
      setMigrating(false);
    }
  };

  const handlePasswordChange = (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword.length >= 6) {
      setMessage({ type: 'success', text: 'Password updated successfully! (Note: This is a demo - changes are not persisted)' });
    } else {
      setMessage({ type: 'error', text: 'Password must be at least 6 characters' });
    }
  };

  const getTableDisplayName = (table: string) => {
    const names: Record<string, string> = {
      'marketing_leads': 'Marketing Leads',
      'follow_ups': 'Follow-ups',
      'conversion_events': 'Conversion Events',
      'marketing_analytics': 'Analytics',
      'ai_config': 'AI Configuration'
    };
    return names[table] || table;
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
        {/* Database Migration */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6 lg:col-span-2">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Database className="w-5 h-5" />
            Database Migration
          </h2>
          
          <div className="space-y-4">
            {/* Connection Status */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                {dbConnected === null ? (
                  <div className="w-3 h-3 bg-gray-400 rounded-full animate-pulse" />
                ) : dbConnected ? (
                  <CheckCircle className="w-5 h-5 text-green-500" />
                ) : (
                  <XCircle className="w-5 h-5 text-red-500" />
                )}
                <div>
                  <p className="font-medium text-gray-900">
                    {dbConnected === null ? 'Checking connection...' : dbConnected ? 'Database Connected' : 'Connection Failed'}
                  </p>
                  {dbError && (
                    <p className="text-sm text-red-600">{dbError}</p>
                  )}
                </div>
              </div>
              <button
                onClick={checkDatabaseStatus}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                title="Refresh status"
              >
                <RefreshCw className="w-4 h-4" />
              </button>
            </div>

            {/* Migration Result */}
            {migrationResult && (
              <div className={`p-4 rounded-lg ${migrationResult.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                <p className={migrationResult.success ? 'text-green-700' : 'text-red-700'}>
                  {migrationResult.message}
                </p>
              </div>
            )}

            {/* Table Stats */}
            {tableStats.length > 0 && (
              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
                  <h3 className="font-medium text-gray-900 flex items-center gap-2">
                    <Table className="w-4 h-4" />
                    Database Tables
                  </h3>
                </div>
                <div className="divide-y divide-gray-200">
                  {tableStats.map((stat) => (
                    <div key={stat.table} className="flex items-center justify-between px-4 py-3">
                      <span className="text-gray-700">{getTableDisplayName(stat.table)}</span>
                      <div className="flex items-center gap-2">
                        {stat.count === -1 ? (
                          <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">
                            Not Created
                          </span>
                        ) : (
                          <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
                            {stat.count} records
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Run Migration Button */}
            <button
              onClick={runMigrations}
              disabled={migrating || dbConnected === false}
              className={`w-full py-3 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2 ${
                migrating || dbConnected === false
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              {migrating ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  Running Migrations...
                </>
              ) : (
                <>
                  <Database className="w-5 h-5" />
                  Run Database Migrations
                </>
              )}
            </button>
            
            <p className="text-xs text-gray-500 text-center">
              This will create all required tables if they don't exist. Safe to run multiple times.
            </p>
          </div>
        </div>

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

        {/* System Info */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6 lg:col-span-2">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">System Information</h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">Version</p>
              <p className="font-mono text-sm font-medium">1.0.0</p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">Framework</p>
              <p className="font-mono text-sm font-medium">Next.js 15</p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">AI Model</p>
              <p className="font-mono text-sm font-medium">GPT-4o-mini</p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">Bot Name</p>
              <p className="font-mono text-sm font-medium">VERA</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}