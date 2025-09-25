import Head from 'next/head'
import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Search, Shield, Target, Zap, Users, BarChart3, Lock, Globe, 
  TrendingUp, Calendar, FileText, Download, Eye, Clock, 
  AlertTriangle, CheckCircle, XCircle, Activity, Database,
  Filter, Settings, Bell, User, LogOut, ChevronDown, Plus,
  Map, Smartphone, Mail, Link as LinkIcon, Image, Network,
  Brain, Radar, Fingerprint, Crosshair, Star, ArrowRight,
  Play, Pause, Volume2, ChevronLeft, ChevronRight, Quote,
  Award, Layers, Cpu, Cloud, GitBranch, Workflow, Zap as ZapIcon,
  MousePointer, Sparkles, Infinity, CircuitBoard, Satellite,
  Server, Terminal, GitMerge, Hexagon, PenTool,
  Lightbulb, MessageSquare, TrendingDown, Monitor, Code,
  Gauge, Mic, Video, Headphones, BookOpen, Hash, AtSign,
  Command, GitPullRequest, Package, Briefcase, Building,
  Crown, Gem, Diamond, Palette, Layers3, Box, Component,
  Gamepad2, Joystick, Trophy, Medal, FlaskConical, Beaker,
  Microscope, TestTube, Dna, Atom, Orbit, Rocket, Plane,
  Car, Train, Ship, Anchor, Compass, Wind, Sun, Moon,
  Sunrise, Sunset, CloudRain, CloudSnow, Thermometer
} from 'lucide-react'

// Enhanced Intelligence Platform inspired by industry leaders:
// GitHub (clean interface, search), Linear (modern gradients, animations)
// Discord (live activity, dark theme), Notion (organized content)
// Vercel (performance focus), Stripe (payment UX), Figma (design system)
export default function IntelliSearchPro() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchType, setSearchType] = useState('phone')
  const [isSearching, setIsSearching] = useState(false)
  const [searchResults, setSearchResults] = useState(null)
  const [showPreview, setShowPreview] = useState(false)

  // Search types available
  const searchTypes = [
    { id: 'phone', name: 'Phone Number', icon: <Smartphone className="w-5 h-5" />, placeholder: 'Enter phone number...' },
    { id: 'email', name: 'Email Address', icon: <Mail className="w-5 h-5" />, placeholder: 'Enter email address...' },
    { id: 'username', name: 'Username/Social', icon: <AtSign className="w-5 h-5" />, placeholder: 'Enter username...' },
    { id: 'name', name: 'Full Name', icon: <User className="w-5 h-5" />, placeholder: 'Enter full name...' },
    { id: 'image', name: 'Reverse Image', icon: <Image className="w-5 h-5" />, placeholder: 'Upload or paste image URL...' },
    { id: 'ip', name: 'IP Address', icon: <Globe className="w-5 h-5" />, placeholder: 'Enter IP address...' }
  ]

  // Advanced features inspired by industry leaders
  const [showAdvancedSearch, setShowAdvancedSearch] = useState(false)
  const [selectedFilters, setSelectedFilters] = useState([])
  const [recentSearches, setRecentSearches] = useState([
    { query: 'john.doe@gmail.com', type: 'email', time: '2 min ago', results: 23 },
    { query: '+1-555-0123', type: 'phone', time: '5 min ago', results: 15 },
    { query: 'jane_smith', type: 'username', time: '8 min ago', results: 31 }
  ])
  
  // Collaboration features inspired by GitHub/Linear
  const [teamActivity, setTeamActivity] = useState([
    { user: 'Detective_Mike', action: 'completed phone lookup', target: '+1-555-0199', confidence: 94, time: '3 min ago' },
    { user: 'Analyst_Sarah', action: 'found email breaches', target: 'target@domain.com', severity: 'high', time: '7 min ago' },
    { user: 'OSINT_Expert', action: 'traced social profiles', target: '@username123', profiles: 8, time: '12 min ago' }
  ])

  // Real-time notifications like Discord
  const [notifications, setNotifications] = useState([
    { id: 1, type: 'success', message: 'New intelligence match found', time: '30s ago', unread: true },
    { id: 2, type: 'warning', message: 'Potential data breach detected', time: '2 min ago', unread: true },
    { id: 3, type: 'info', message: 'Weekly intelligence report ready', time: '1 hour ago', unread: false }
  ])

  // Live stats for social proof with enhanced metrics
  const [liveStats, setLiveStats] = useState({
    searchesToday: 24567,
    recordsSearched: 8900000000,
    successRate: 94.8,
    usersOnline: 1247,
    activeInvestigations: 189,
    dataSources: 247,
    countriesCovered: 89,
    mlAccuracy: 97.3
  })

  // Simulate live counter updates
  useEffect(() => {
    const interval = setInterval(() => {
      setLiveStats(prev => ({
        ...prev,
        searchesToday: prev.searchesToday + Math.floor(Math.random() * 3),
        usersOnline: prev.usersOnline + (Math.random() > 0.5 ? 1 : -1)
      }))
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  // Handle search
  const handleSearch = async () => {
    if (!searchQuery.trim()) return
    
    setIsSearching(true)
    setShowPreview(false)
    
    // Simulate search
    setTimeout(() => {
      setSearchResults({
        query: searchQuery,
        type: searchType,
        preview: {
          found: true,
          confidence: 94.7,
          sources: 23,
          dataPoints: 156
        }
      })
      setShowPreview(true)
      setIsSearching(false)
    }, 2000)
  }

  return (
    <>
      <Head>
        <title>IntelliSearch Pro - Advanced People & Digital Intelligence Platform</title>
        <meta name="description" content="Find anyone, anywhere. Advanced intelligence search for phone numbers, emails, usernames, and more. Get instant results from billions of records." />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-black text-white overflow-hidden">
        {/* Futuristic Background */}
        <div className="fixed inset-0 z-0">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-purple-900/20 to-cyan-900/20" />
          <div className="absolute inset-0" style={{
            backgroundImage: `
              radial-gradient(circle at 25% 25%, rgba(0, 100, 255, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 75% 75%, rgba(150, 0, 255, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 50% 0%, rgba(0, 255, 200, 0.1) 0%, transparent 50%)
            `
          }} />
          {/* Animated grid */}
          <div className="absolute inset-0 opacity-10">
            <div className="h-full w-full" style={{
              backgroundImage: `
                linear-gradient(rgba(0, 150, 255, 0.3) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 150, 255, 0.3) 1px, transparent 1px)
              `,
              backgroundSize: '40px 40px'
            }} />
          </div>
        </div>

        {/* Enhanced Header - Inspired by GitHub/Linear/Vercel */}
        <header className="relative z-10 border-b border-gray-800/50 bg-black/80 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              {/* Logo and Brand */}
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 via-purple-500 to-cyan-500 rounded-xl flex items-center justify-center shadow-xl shadow-blue-500/25">
                  <Search className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                    IntelliSearch Pro
                  </h1>
                  <p className="text-sm text-gray-400">Advanced Intelligence Platform</p>
                </div>
              </div>

              {/* Advanced Navigation - GitHub style */}
              <div className="hidden lg:flex items-center space-x-6">
                {/* Navigation Links */}
                <nav className="flex items-center space-x-1">
                  <a href="#search" className="px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800/50 transition-all duration-200 text-sm font-medium">
                    Search
                  </a>
                  <a href="#analytics" className="px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800/50 transition-all duration-200 text-sm font-medium">
                    Analytics
                  </a>
                  <a href="#reports" className="px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800/50 transition-all duration-200 text-sm font-medium">
                    Reports
                  </a>
                  <a href="/pricing" className="px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800/50 transition-all duration-200 text-sm font-medium">
                    Pricing
                  </a>
                </nav>

                {/* Quick Search - Inspired by GitHub command palette */}
                <div className="relative">
                  <button 
                    onClick={() => setShowAdvancedSearch(true)}
                    className="flex items-center space-x-2 px-4 py-2 bg-gray-800/50 border border-gray-700/50 rounded-lg text-gray-400 hover:bg-gray-700/50 hover:text-white transition-all duration-200"
                  >
                    <Search className="w-4 h-4" />
                    <span className="text-sm">Quick search...</span>
                    <div className="px-2 py-1 bg-gray-700 rounded text-xs">⌘K</div>
                  </button>
                </div>

                {/* Notifications */}
                <div className="relative">
                  <button className="relative p-2 rounded-lg hover:bg-gray-800/50 transition-colors group">
                    <Bell className="w-5 h-5 text-gray-400 group-hover:text-white" />
                    {notifications.filter(n => n.unread).length > 0 && (
                      <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full flex items-center justify-center">
                        <span className="text-xs text-white font-bold">{notifications.filter(n => n.unread).length}</span>
                      </span>
                    )}
                  </button>
                </div>

                {/* User Menu */}
                <button className="w-8 h-8 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center shadow-lg shadow-green-500/25">
                  <User className="w-4 h-4 text-white" />
                </button>
              </div>

              {/* Mobile Navigation */}
              <div className="flex lg:hidden items-center space-x-4">
                <button className="relative p-2 rounded-lg hover:bg-gray-800/50 transition-colors">
                  <Bell className="w-5 h-5 text-gray-400" />
                  {notifications.filter(n => n.unread).length > 0 && (
                    <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
                  )}
                </button>
                <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">
                  Sign In
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Enhanced Live Stats Bar - Inspired by Vercel/Linear dashboards */}
        <div className="relative z-10 bg-gradient-to-r from-blue-900/50 via-purple-900/50 to-cyan-900/50 border-b border-gray-800/50">
          <div className="max-w-7xl mx-auto px-6 py-3">
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center space-x-8">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                  <span className="text-gray-300">{liveStats.usersOnline.toLocaleString()} users online</span>
                </div>
                <div className="text-gray-300 flex items-center space-x-1">
                  <TrendingUp className="w-4 h-4 text-green-400" />
                  <span>{liveStats.searchesToday.toLocaleString()} searches today</span>
                </div>
                <div className="text-gray-300">
                  {(liveStats.recordsSearched / 1000000000).toFixed(1)}B+ records
                </div>
                <div className="hidden md:flex items-center space-x-1 text-gray-300">
                  <Database className="w-4 h-4 text-blue-400" />
                  <span>{liveStats.dataSources} sources</span>
                </div>
                <div className="hidden lg:flex items-center space-x-1 text-gray-300">
                  <Brain className="w-4 h-4 text-purple-400" />
                  <span>{liveStats.mlAccuracy}% ML accuracy</span>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  <span className="text-green-400">{liveStats.successRate}% success</span>
                </div>
                <div className="hidden md:flex items-center space-x-1 text-gray-300">
                  <Activity className="w-4 h-4 text-orange-400" />
                  <span>{liveStats.activeInvestigations} active</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Hero Section */}
        <main className="relative z-10">
          <div className="max-w-7xl mx-auto px-6 py-16">
            <div className="text-center max-w-4xl mx-auto mb-16">
              <motion.h1 
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-5xl md:text-7xl font-bold mb-6"
              >
                Find Anyone,{' '}
                <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                  Anywhere
                </span>
              </motion.h1>
              
              <motion.p 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="text-xl md:text-2xl text-gray-300 mb-12"
              >
                Advanced intelligence search engine with access to billions of records.
                <br />
                <span className="text-blue-400">Get instant results</span> for phone numbers, emails, usernames, and more.
              </motion.p>

              {/* Search Interface */}
              <motion.div 
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="bg-gray-900/50 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-8 mb-8"
              >
                {/* Search Type Selector */}
                <div className="flex flex-wrap justify-center gap-2 mb-6">
                  {searchTypes.map((type) => (
                    <button
                      key={type.id}
                      onClick={() => setSearchType(type.id)}
                      className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-all ${
                        searchType === type.id 
                          ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/25' 
                          : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                      }`}
                    >
                      {type.icon}
                      <span className="text-sm font-medium">{type.name}</span>
                    </button>
                  ))}
                </div>

                {/* Search Input */}
                <div className="relative max-w-2xl mx-auto mb-6">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder={searchTypes.find(t => t.id === searchType)?.placeholder}
                    className="w-full px-6 py-4 bg-gray-800/50 border border-gray-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 text-lg"
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  />
                  <button
                    onClick={handleSearch}
                    disabled={isSearching || !searchQuery.trim()}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg text-white font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                  >
                    {isSearching ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        <span>Searching...</span>
                      </>
                    ) : (
                      <>
                        <Search className="w-4 h-4" />
                        <span>Search</span>
                      </>
                    )}
                  </button>
                </div>

                {/* Search Results Preview */}
                <AnimatePresence>
                  {showPreview && searchResults && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="bg-gray-800/50 border border-gray-600/50 rounded-xl p-6 max-w-2xl mx-auto"
                    >
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <CheckCircle className="w-6 h-6 text-green-400" />
                          <h3 className="text-lg font-semibold text-white">Results Found!</h3>
                        </div>
                        <div className="flex items-center space-x-2 text-sm text-gray-400">
                          <Clock className="w-4 h-4" />
                          <span>0.8s</span>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                        <div className="text-center">
                          <div className="text-2xl font-bold text-green-400">94.7%</div>
                          <div className="text-sm text-gray-400">Confidence</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-blue-400">23</div>
                          <div className="text-sm text-gray-400">Sources</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-purple-400">156</div>
                          <div className="text-sm text-gray-400">Data Points</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-cyan-400">12</div>
                          <div className="text-sm text-gray-400">Profiles</div>
                        </div>
                      </div>

                      <div className="bg-gray-900/50 rounded-lg p-4 mb-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-gray-300">Preview Results</span>
                          <span className="text-sm text-yellow-400">⭐ Premium Required</span>
                        </div>
                        <div className="space-y-2 text-sm text-gray-400">
                          <div className="flex justify-between">
                            <span>Location:</span>
                            <span className="blur-sm">San Francisco, CA</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Associated Emails:</span>
                            <span className="blur-sm">3 found</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Social Profiles:</span>
                            <span className="blur-sm">7 found</span>
                          </div>
                        </div>
                      </div>

                      <div className="flex space-x-3">
                        <button className="flex-1 px-4 py-3 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 rounded-lg text-white font-medium transition-all">
                          Get Full Report - $4.99
                        </button>
                        <button className="px-4 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-white transition-all">
                          Save Search
                        </button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            </div>
          </div>
        </main>

        {/* Trust Indicators */}
        <section className="relative z-10 py-16 border-t border-gray-800/50">
          <div className="max-w-7xl mx-auto px-6">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-white mb-4">Trusted by Millions Worldwide</h2>
              <p className="text-gray-400">Professional-grade intelligence platform used by investigators, businesses, and individuals</p>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-400 mb-2">50M+</div>
                <div className="text-gray-400">Searches Performed</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-400 mb-2">8.9B</div>
                <div className="text-gray-400">Records Indexed</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-400 mb-2">99.2%</div>
                <div className="text-gray-400">Customer Satisfaction</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-cyan-400 mb-2">24/7</div>
                <div className="text-gray-400">Expert Support</div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section className="relative z-10 py-16">
          <div className="max-w-7xl mx-auto px-6">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Advanced Intelligence{' '}
                <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  Capabilities
                </span>
              </h2>
              <p className="text-xl text-gray-400">
                Comprehensive search tools powered by AI and billions of data points
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[
                {
                  icon: <Smartphone className="w-8 h-8" />,
                  title: 'Phone Intelligence',
                  description: 'Comprehensive phone number lookup with carrier info, location data, and associated profiles.',
                  features: ['Carrier identification', 'Location tracking', 'Social media links', 'Background checks']
                },
                {
                  icon: <Mail className="w-8 h-8" />,
                  title: 'Email Investigation',
                  description: 'Deep email analysis including verification, breach detection, and associated accounts.',
                  features: ['Email verification', 'Breach monitoring', 'Account discovery', 'Social connections']
                },
                {
                  icon: <User className="w-8 h-8" />,
                  title: 'People Search',
                  description: 'Advanced people finder with comprehensive background information and contact details.',
                  features: ['Background checks', 'Contact information', 'Address history', 'Criminal records']
                },
                {
                  icon: <AtSign className="w-8 h-8" />,
                  title: 'Username Tracking',
                  description: 'Cross-platform username investigation across social media and online platforms.',
                  features: ['Social media profiles', 'Dating site accounts', 'Forum participation', 'Online activity']
                },
                {
                  icon: <Image className="w-8 h-8" />,
                  title: 'Reverse Image Search',
                  description: 'Advanced image recognition and reverse lookup across the web and social platforms.',
                  features: ['Facial recognition', 'Source identification', 'Profile matching', 'Duplicate detection']
                },
                {
                  icon: <Globe className="w-8 h-8" />,
                  title: 'IP & Network Analysis',
                  description: 'Comprehensive IP address investigation including geolocation and network analysis.',
                  features: ['Geolocation data', 'ISP information', 'Network topology', 'Security analysis']
                }
              ].map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-gray-900/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 hover:border-blue-500/50 transition-all group"
                >
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="p-3 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg text-white group-hover:shadow-lg group-hover:shadow-blue-600/25 transition-all">
                      {feature.icon}
                    </div>
                    <h3 className="text-xl font-semibold text-white">{feature.title}</h3>
                  </div>
                  <p className="text-gray-400 mb-4">{feature.description}</p>
                  <ul className="space-y-2">
                    {feature.features.map((item, i) => (
                      <li key={i} className="flex items-center space-x-2 text-sm text-gray-300">
                        <CheckCircle className="w-4 h-4 text-green-400" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="relative z-10 border-t border-gray-800/50 bg-gray-900/50 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-6 py-12">
            <div className="grid md:grid-cols-4 gap-8">
              <div>
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 via-purple-500 to-cyan-500 rounded-lg flex items-center justify-center">
                    <Search className="w-5 h-5 text-white" />
                  </div>
                  <span className="text-xl font-bold text-white">IntelliSearch Pro</span>
                </div>
                <p className="text-gray-400 text-sm">
                  The world's most advanced intelligence search platform. Find anyone, anywhere, instantly.
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold text-white mb-4">Services</h4>
                <ul className="space-y-2 text-sm text-gray-400">
                  <li><a href="#" className="hover:text-white transition-colors">Phone Lookup</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Email Search</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">People Finder</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Image Search</a></li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-semibold text-white mb-4">Company</h4>
                <ul className="space-y-2 text-sm text-gray-400">
                  <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-semibold text-white mb-4">Support</h4>
                <ul className="space-y-2 text-sm text-gray-400">
                  <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">API Docs</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Status</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Contact Support</a></li>
                </ul>
              </div>
            </div>
            
            <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
              <p>&copy; 2024 IntelliSearch Pro. All rights reserved. Professional intelligence platform.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}