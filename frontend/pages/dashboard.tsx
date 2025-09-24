import Head from 'next/head'
import { useState, useEffect } from 'react'
import { 
  Search, Shield, Target, Zap, Users, BarChart3, Lock, Globe, 
  TrendingUp, Calendar, FileText, Download, Eye, Clock, 
  AlertTriangle, CheckCircle, XCircle, Activity, Database,
  Filter, Settings, Bell, User, LogOut, ChevronDown, Plus,
  Map, Smartphone, Mail, Link as LinkIcon, Image, Network,
  Brain, Radar, Fingerprint, Crosshair
} from 'lucide-react'

interface ScanResult {
  id: string
  target: string
  type: string
  status: 'completed' | 'running' | 'failed'
  confidence: number
  sourcesFound: number
  createdAt: string
  preview: {
    socialProfiles: number
    publicRecords: number
    phoneNumbers: number
    locations: number
  }
}

interface DashboardStats {
  totalScans: number
  successRate: number
  activeScans: number
  queriesUsed: number
  queriesLimit: number
  creditsRemaining: number
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalScans: 247,
    successRate: 94.2,
    activeScans: 3,
    queriesUsed: 18,
    queriesLimit: 100,
    creditsRemaining: 2450
  })

  const [recentScans, setRecentScans] = useState<ScanResult[]>([
    {
      id: 'scan_1',
      target: 'john.doe@example.com',
      type: 'email',
      status: 'completed',
      confidence: 87.5,
      sourcesFound: 23,
      createdAt: '2024-01-15T10:30:00Z',
      preview: { socialProfiles: 5, publicRecords: 8, phoneNumbers: 2, locations: 3 }
    },
    {
      id: 'scan_2',
      target: '+1 555-0123',
      type: 'phone',
      status: 'running',
      confidence: 0,
      sourcesFound: 0,
      createdAt: '2024-01-15T11:15:00Z',
      preview: { socialProfiles: 0, publicRecords: 0, phoneNumbers: 0, locations: 0 }
    },
    {
      id: 'scan_3',
      target: 'Sarah Johnson',
      type: 'name',
      status: 'completed',
      confidence: 76.3,
      sourcesFound: 18,
      createdAt: '2024-01-15T09:45:00Z',
      preview: { socialProfiles: 3, publicRecords: 12, phoneNumbers: 1, locations: 5 }
    }
  ])

  const [activeTab, setActiveTab] = useState('overview')
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false)

  const scannerCategories = [
    { name: 'Social Media', icon: <Users className="w-5 h-5" />, count: 24, color: 'bg-blue-500' },
    { name: 'Email Intel', icon: <Mail className="w-5 h-5" />, count: 18, color: 'bg-green-500' },
    { name: 'Phone Lookup', icon: <Smartphone className="w-5 h-5" />, count: 15, color: 'bg-purple-500' },
    { name: 'Public Records', icon: <FileText className="w-5 h-5" />, count: 32, color: 'bg-orange-500' },
    { name: 'Image Analysis', icon: <Image className="w-5 h-5" />, count: 12, color: 'bg-pink-500' },
    { name: 'Network Intel', icon: <Network className="w-5 h-5" />, count: 8, color: 'bg-cyan-500' },
    { name: 'AI Correlation', icon: <Brain className="w-5 h-5" />, count: 6, color: 'bg-indigo-500' },
    { name: 'Geospatial', icon: <Map className="w-5 h-5" />, count: 10, color: 'bg-emerald-500' }
  ]

  const quickActions = [
    { name: 'New Email Scan', icon: <Mail className="w-5 h-5" />, action: () => {} },
    { name: 'Phone Lookup', icon: <Smartphone className="w-5 h-5" />, action: () => {} },
    { name: 'Reverse Image', icon: <Image className="w-5 h-5" />, action: () => {} },
    { name: 'Name Search', icon: <User className="w-5 h-5" />, action: () => {} }
  ]

  return (
    <>
      <Head>
        <title>Dashboard - Intelligence Platform</title>
        <meta name="description" content="Intelligence gathering dashboard with real-time analytics" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        {/* Navigation Header */}
        <header className="bg-slate-900/90 backdrop-blur-sm border-b border-slate-700 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              {/* Logo */}
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <Radar className="w-5 h-5 text-white" />
                </div>
                <div className="hidden sm:block">
                  <h1 className="text-lg font-bold text-white">Intelligence Platform</h1>
                  <p className="text-xs text-slate-400">Professional Dashboard</p>
                </div>
              </div>

              {/* Navigation Tabs */}
              <nav className="hidden md:flex space-x-8">
                {[
                  { id: 'overview', label: 'Overview', icon: <BarChart3 className="w-4 h-4" /> },
                  { id: 'scans', label: 'Scans', icon: <Search className="w-4 h-4" /> },
                  { id: 'reports', label: 'Reports', icon: <FileText className="w-4 h-4" /> },
                  { id: 'analytics', label: 'Analytics', icon: <TrendingUp className="w-4 h-4" /> }
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                      activeTab === tab.id
                        ? 'bg-blue-600 text-white'
                        : 'text-slate-300 hover:text-white hover:bg-slate-700'
                    }`}
                  >
                    {tab.icon}
                    <span>{tab.label}</span>
                  </button>
                ))}
              </nav>

              {/* User Menu */}
              <div className="flex items-center space-x-4">
                <button className="p-2 text-slate-400 hover:text-white transition-colors">
                  <Bell className="w-5 h-5" />
                </button>
                <div className="relative">
                  <button
                    onClick={() => setIsProfileMenuOpen(!isProfileMenuOpen)}
                    className="flex items-center space-x-2 p-2 rounded-lg hover:bg-slate-700 transition-colors"
                  >
                    <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                      <User className="w-4 h-4 text-white" />
                    </div>
                    <ChevronDown className="w-4 h-4 text-slate-400" />
                  </button>
                  
                  {isProfileMenuOpen && (
                    <div className="absolute right-0 mt-2 w-48 bg-slate-800 rounded-lg shadow-lg border border-slate-700 py-2">
                      <a href="#" className="block px-4 py-2 text-slate-300 hover:bg-slate-700 hover:text-white">
                        Profile Settings
                      </a>
                      <a href="#" className="block px-4 py-2 text-slate-300 hover:bg-slate-700 hover:text-white">
                        Billing
                      </a>
                      <a href="#" className="block px-4 py-2 text-slate-300 hover:bg-slate-700 hover:text-white">
                        API Keys
                      </a>
                      <hr className="my-2 border-slate-700" />
                      <a href="#" className="block px-4 py-2 text-red-400 hover:bg-slate-700">
                        Sign Out
                      </a>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-8">
              {/* Stats Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm">Total Scans</p>
                      <p className="text-2xl font-bold text-white">{stats.totalScans}</p>
                    </div>
                    <div className="p-3 bg-blue-500/20 rounded-lg">
                      <Search className="w-6 h-6 text-blue-400" />
                    </div>
                  </div>
                  <div className="mt-4 flex items-center space-x-2 text-sm">
                    <TrendingUp className="w-4 h-4 text-green-400" />
                    <span className="text-green-400">+12%</span>
                    <span className="text-slate-400">vs last month</span>
                  </div>
                </div>

                <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm">Success Rate</p>
                      <p className="text-2xl font-bold text-white">{stats.successRate}%</p>
                    </div>
                    <div className="p-3 bg-green-500/20 rounded-lg">
                      <CheckCircle className="w-6 h-6 text-green-400" />
                    </div>
                  </div>
                  <div className="mt-4 flex items-center space-x-2 text-sm">
                    <TrendingUp className="w-4 h-4 text-green-400" />
                    <span className="text-green-400">+2.1%</span>
                    <span className="text-slate-400">vs last month</span>
                  </div>
                </div>

                <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm">Active Scans</p>
                      <p className="text-2xl font-bold text-white">{stats.activeScans}</p>
                    </div>
                    <div className="p-3 bg-orange-500/20 rounded-lg">
                      <Activity className="w-6 h-6 text-orange-400" />
                    </div>
                  </div>
                  <div className="mt-4 flex items-center space-x-2 text-sm">
                    <Clock className="w-4 h-4 text-orange-400" />
                    <span className="text-slate-400">Real-time</span>
                  </div>
                </div>

                <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm">Credits</p>
                      <p className="text-2xl font-bold text-white">{stats.creditsRemaining}</p>
                    </div>
                    <div className="p-3 bg-purple-500/20 rounded-lg">
                      <Database className="w-6 h-6 text-purple-400" />
                    </div>
                  </div>
                  <div className="mt-4 flex items-center space-x-2 text-sm">
                    <span className="text-slate-400">Professional Plan</span>
                  </div>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <h3 className="text-lg font-semibold text-white mb-4">Quick Actions</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {quickActions.map((action, index) => (
                    <button
                      key={index}
                      onClick={action.action}
                      className="p-4 bg-slate-700/50 rounded-lg border border-slate-600 hover:bg-slate-600/50 transition-colors group"
                    >
                      <div className="flex flex-col items-center space-y-2">
                        <div className="p-2 bg-blue-500/20 rounded-lg group-hover:bg-blue-500/30 transition-colors">
                          {action.icon}
                        </div>
                        <span className="text-sm text-slate-300 group-hover:text-white transition-colors">
                          {action.name}
                        </span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Scanner Categories */}
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-semibold text-white">Scanner Tools</h3>
                  <span className="text-sm text-slate-400">129 total tools</span>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {scannerCategories.map((category, index) => (
                    <div key={index} className="p-4 bg-slate-700/30 rounded-lg border border-slate-600">
                      <div className="flex items-center space-x-3 mb-2">
                        <div className={`p-2 ${category.color}/20 rounded-lg`}>
                          {category.icon}
                        </div>
                        <div>
                          <h4 className="font-medium text-white">{category.name}</h4>
                          <p className="text-sm text-slate-400">{category.count} tools</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recent Activity */}
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-semibold text-white">Recent Scans</h3>
                  <button className="text-blue-400 hover:text-blue-300 text-sm">View All</button>
                </div>
                <div className="space-y-4">
                  {recentScans.map((scan) => (
                    <div key={scan.id} className="flex items-center justify-between p-4 bg-slate-700/30 rounded-lg border border-slate-600">
                      <div className="flex items-center space-x-4">
                        <div className={`p-2 rounded-lg ${
                          scan.status === 'completed' ? 'bg-green-500/20' :
                          scan.status === 'running' ? 'bg-orange-500/20' : 'bg-red-500/20'
                        }`}>
                          {scan.status === 'completed' && <CheckCircle className="w-5 h-5 text-green-400" />}
                          {scan.status === 'running' && <Clock className="w-5 h-5 text-orange-400" />}
                          {scan.status === 'failed' && <XCircle className="w-5 h-5 text-red-400" />}
                        </div>
                        <div>
                          <p className="font-medium text-white">{scan.target}</p>
                          <p className="text-sm text-slate-400 capitalize">{scan.type} scan</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-4">
                        {scan.status === 'completed' && (
                          <>
                            <div className="text-right">
                              <p className="text-sm font-medium text-white">{scan.confidence}% confidence</p>
                              <p className="text-xs text-slate-400">{scan.sourcesFound} sources</p>
                            </div>
                            <button className="p-2 text-slate-400 hover:text-white transition-colors">
                              <Eye className="w-4 h-4" />
                            </button>
                          </>
                        )}
                        {scan.status === 'running' && (
                          <div className="w-5 h-5 border-2 border-orange-500/20 border-t-orange-400 rounded-full animate-spin" />
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Other tabs content can be added here */}
          {activeTab !== 'overview' && (
            <div className="text-center py-20">
              <h3 className="text-2xl font-semibold text-white mb-4">
                {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Section
              </h3>
              <p className="text-slate-400">
                This section is under development. Advanced {activeTab} features coming soon.
              </p>
            </div>
          )}
        </main>
      </div>
    </>
  )
}