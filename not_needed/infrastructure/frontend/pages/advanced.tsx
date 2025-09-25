import Head from 'next/head'
import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence, useScroll, useTransform } from 'framer-motion'
import { 
  Search, Shield, Target, Zap, Users, BarChart3, Lock, Globe, 
  TrendingUp, Calendar, FileText, Download, Eye, Clock, 
  AlertTriangle, CheckCircle, XCircle, Activity, Database,
  Filter, Settings, Bell, User, LogOut, ChevronDown, Plus,
  Map, Smartphone, Mail, Link as LinkIcon, Image, Network,
  Brain, Radar, Fingerprint, Crosshair, Star, ArrowRight,
  Play, Pause, Volume2, ChevronLeft, ChevronRight, Quote,
  Award, Layers, Cpu, Cloud, GitBranch, Workflow, 
  MousePointer, Sparkles, Infinity, CircuitBoard, Satellite,
  Server, Terminal, GitMerge, Hexagon, PenTool,
  Lightbulb, MessageSquare, TrendingDown, Monitor, Code,
  Gauge, Mic, Video, Headphones, BookOpen, Hash, AtSign,
  Command, GitPullRequest, Package, Briefcase, Building,
  Crown, Gem, Diamond, Palette, Layers3, Box, Component,
  Gamepad2, Joystick, Trophy, Medal, FlaskConical, Beaker,
  Microscope, TestTube, Dna, Atom, Orbit, Rocket, Plane,
  Car, Train, Ship, Anchor, Compass, Wind, Sun, Moon,
  Menu, X, ExternalLink, Share2, Copy, ThumbsUp, MessageCircle,
  Bookmark, Send, RefreshCw, MoreHorizontal, TrendingDown as Trending
} from 'lucide-react'

// Advanced Intelligence Platform inspired by industry leaders
// GitHub, Linear, Discord, Notion, Vercel, Stripe, Figma, etc.
export default function AdvancedIntelligencePlatform() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchType, setSearchType] = useState('phone')
  const [isSearching, setIsSearching] = useState(false)
  const [searchResults, setSearchResults] = useState(null)
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false)
  const [selectedTab, setSelectedTab] = useState('search')
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const containerRef = useRef(null)
  
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end start"]
  })
  
  const headerOpacity = useTransform(scrollYProgress, [0, 0.1], [1, 0.95])
  const heroScale = useTransform(scrollYProgress, [0, 0.5], [1, 0.98])

  // Advanced search types inspired by leading OSINT platforms
  const searchCategories = [
    {
      category: 'People Intelligence',
      color: 'from-blue-500 to-cyan-500',
      searches: [
        { id: 'phone', name: 'Phone Lookup', icon: <Smartphone className="w-5 h-5" />, desc: 'Carrier, location, social profiles' },
        { id: 'email', name: 'Email Investigation', icon: <Mail className="w-5 h-5" />, desc: 'Breaches, accounts, verification' },
        { id: 'name', name: 'People Search', icon: <User className="w-5 h-5" />, desc: 'Background, contacts, records' },
        { id: 'username', name: 'Username Tracking', icon: <AtSign className="w-5 h-5" />, desc: 'Social media, dating sites' }
      ]
    },
    {
      category: 'Digital Forensics',
      color: 'from-purple-500 to-pink-500',
      searches: [
        { id: 'image', name: 'Reverse Image', icon: <Image className="w-5 h-5" />, desc: 'Facial recognition, sources' },
        { id: 'ip', name: 'IP Analysis', icon: <Globe className="w-5 h-5" />, desc: 'Geolocation, ISP, network' },
        { id: 'domain', name: 'Domain Intel', icon: <Network className="w-5 h-5" />, desc: 'WHOIS, DNS, certificates' },
        { id: 'hash', name: 'File Analysis', icon: <FileText className="w-5 h-5" />, desc: 'Hash lookup, malware' }
      ]
    },
    {
      category: 'Social Intelligence',
      color: 'from-green-500 to-emerald-500',
      searches: [
        { id: 'social', name: 'Social Profiling', icon: <Users className="w-5 h-5" />, desc: 'Cross-platform analysis' },
        { id: 'leaked', name: 'Data Breaches', icon: <Shield className="w-5 h-5" />, desc: 'Leaked credentials, exposure' },
        { id: 'crypto', name: 'Crypto Tracking', icon: <Database className="w-5 h-5" />, desc: 'Wallet analysis, transactions' },
        { id: 'darkweb', name: 'Dark Web Scan', icon: <Eye className="w-5 h-5" />, desc: 'Underground mentions' }
      ]
    }
  ]

  // Real-time metrics inspired by GitHub/Linear dashboards
  const [liveMetrics, setLiveMetrics] = useState({
    searches: { today: 47234, total: 125634892 },
    users: { online: 3847, total: 892456 },
    accuracy: 97.3,
    uptime: 99.97,
    avgResponse: 0.42,
    dataPoints: 12.4
  })

  // Live feed inspired by Discord/Linear activity feeds
  const [liveFeed, setLiveFeed] = useState([
    { id: 1, type: 'search', user: 'Detective_Mike', action: 'found 23 profiles for email', time: '2s ago', confidence: 94 },
    { id: 2, type: 'breach', user: 'Investigator_Sarah', action: 'detected in 3 data breaches', time: '7s ago', severity: 'high' },
    { id: 3, type: 'success', user: 'OSINT_Expert', action: 'located missing person via phone', time: '12s ago', confidence: 98 },
    { id: 4, type: 'crypto', user: 'BlockchainAnalyst', action: 'traced $2.3M transaction', time: '18s ago', confidence: 91 },
    { id: 5, type: 'image', user: 'DigitalForensics', action: 'matched face across 15 platforms', time: '23s ago', confidence: 96 }
  ])

  // Advanced filtering inspired by GitHub/GitLab search
  const advancedFilters = [
    { id: 'timeRange', name: 'Time Range', options: ['Last 24h', 'Last week', 'Last month', 'All time'] },
    { id: 'confidence', name: 'Confidence Level', options: ['90%+', '80%+', '70%+', 'Any'] },
    { id: 'sources', name: 'Data Sources', options: ['Public Records', 'Social Media', 'Dark Web', 'Breaches'] },
    { id: 'geography', name: 'Geographic Region', options: ['North America', 'Europe', 'Asia Pacific', 'Global'] }
  ]

  // Simulate live updates
  useEffect(() => {
    const updateMetrics = () => {
      setLiveMetrics(prev => ({
        ...prev,
        searches: {
          ...prev.searches,
          today: prev.searches.today + Math.floor(Math.random() * 3)
        },
        users: {
          ...prev.users,
          online: prev.users.online + Math.floor(Math.random() * 5) - 2
        }
      }))
    }

    const updateFeed = () => {
      const activities = [
        'found 15 social profiles',
        'detected security breach',
        'traced cryptocurrency wallet',
        'identified fake profile',
        'located digital footprint',
        'discovered hidden connections',
        'mapped network topology',
        'analyzed behavioral patterns'
      ]
      
      const newActivity = {
        id: Date.now(),
        type: ['search', 'breach', 'success', 'crypto', 'image'][Math.floor(Math.random() * 5)],
        user: `User_${Math.floor(Math.random() * 1000)}`,
        action: activities[Math.floor(Math.random() * activities.length)],
        time: 'just now',
        confidence: 85 + Math.floor(Math.random() * 15)
      }

      setLiveFeed(prev => [newActivity, ...prev.slice(0, 9)])
    }

    const metricsInterval = setInterval(updateMetrics, 3000)
    const feedInterval = setInterval(updateFeed, 8000)

    return () => {
      clearInterval(metricsInterval)
      clearInterval(feedInterval)
    }
  }, [])

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    setIsSearching(true)
    
    // Simulate realistic search process
    await new Promise(resolve => setTimeout(resolve, 1200))
    
    // Generate realistic results based on search type
    const mockResults = {
      confidence: 87 + Math.floor(Math.random() * 12),
      sources: 15 + Math.floor(Math.random() * 20),
      dataPoints: 89 + Math.floor(Math.random() * 200),
      timeMs: 420 + Math.floor(Math.random() * 400),
      preview: {
        location: ['San Francisco, CA', 'New York, NY', 'Austin, TX', 'Seattle, WA'][Math.floor(Math.random() * 4)],
        associatedAccounts: 3 + Math.floor(Math.random() * 8),
        socialProfiles: 5 + Math.floor(Math.random() * 12),
        dataBreaches: Math.floor(Math.random() * 4),
        riskScore: Math.floor(Math.random() * 100)
      }
    }

    setSearchResults(mockResults)
    setIsSearching(false)
  }

  const currentSearchType = searchCategories
    .flatMap(cat => cat.searches)
    .find(search => search.id === searchType) || searchCategories[0].searches[0]

  return (
    <>
      <Head>
        <title>Advanced Intelligence Platform - Next-Gen OSINT & Investigation</title>
        <meta name="description" content="Professional intelligence gathering platform with advanced search capabilities, real-time analytics, and industry-leading accuracy." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div ref={containerRef} className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white overflow-x-hidden">
        {/* Animated Background Grid - Inspired by Linear */}
        <div className="fixed inset-0 opacity-20 pointer-events-none">
          <div className="absolute inset-0 bg-[linear-gradient(rgba(59,130,246,0.3)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.3)_1px,transparent_1px)] bg-[size:72px_72px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)]" />
        </div>

        {/* Enhanced Header - Inspired by GitHub/Vercel */}
        <motion.header 
          style={{ opacity: headerOpacity }}
          className="fixed top-0 left-0 right-0 z-50 border-b border-slate-800/50 backdrop-blur-xl bg-slate-950/80"
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 via-purple-500 to-cyan-500 rounded-xl flex items-center justify-center shadow-xl shadow-blue-500/25">
                    <Brain className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h1 className="text-xl font-bold bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
                      IntelliSearch Pro
                    </h1>
                    <p className="text-xs text-slate-400">Advanced OSINT Platform</p>
                  </div>
                </div>
              </div>

              {/* Navigation Tabs - Inspired by Linear */}
              <nav className="hidden md:flex items-center space-x-1">
                {['search', 'analytics', 'reports', 'tools'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setSelectedTab(tab)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      selectedTab === tab
                        ? 'bg-blue-500/20 text-blue-400 shadow-lg shadow-blue-500/25'
                        : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                    }`}
                  >
                    {tab.charAt(0).toUpperCase() + tab.slice(1)}
                  </button>
                ))}
              </nav>

              {/* User Menu - Inspired by GitHub */}
              <div className="flex items-center space-x-4">
                <button className="relative p-2 rounded-lg hover:bg-slate-800/50 transition-colors">
                  <Bell className="w-5 h-5 text-slate-400" />
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
                </button>
                <button 
                  onClick={() => setIsMenuOpen(!isMenuOpen)}
                  className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center"
                >
                  <User className="w-4 h-4 text-white" />
                </button>
              </div>
            </div>
          </div>
        </motion.header>

        {/* Live Status Bar - Inspired by Discord */}
        <div className="fixed top-16 left-0 right-0 z-40 bg-gradient-to-r from-green-500/10 via-blue-500/10 to-purple-500/10 border-b border-slate-800/30 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between py-2 text-sm">
              <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span className="text-green-400 font-medium">{liveMetrics.users.online.toLocaleString()} users online</span>
                </div>
                <div className="text-slate-400">
                  {liveMetrics.searches.today.toLocaleString()} searches today
                </div>
                <div className="text-slate-400">
                  {liveMetrics.dataPoints}B+ records
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  <span className="text-green-400">{liveMetrics.accuracy}% accuracy</span>
                </div>
                <div className="text-slate-400">
                  ⚡ {liveMetrics.avgResponse}s avg response
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <main className="pt-32 pb-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Hero Section - Enhanced with Parallax */}
            <motion.div 
              style={{ scale: heroScale }}
              className="text-center mb-16"
            >
              <motion.h1 
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="text-5xl md:text-7xl font-bold mb-6"
              >
                <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                  Advanced Intelligence
                </span>
                <br />
                <span className="text-white">at Your Fingertips</span>
              </motion.h1>
              
              <motion.p 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="text-xl text-slate-300 mb-12 max-w-3xl mx-auto leading-relaxed"
              >
                Next-generation OSINT platform powered by AI and machine learning. 
                Search across {liveMetrics.dataPoints}B+ records with {liveMetrics.accuracy}% accuracy.
              </motion.p>

              {/* Enhanced Search Interface */}
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.4 }}
                className="max-w-4xl mx-auto"
              >
                {/* Search Categories */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  {searchCategories.map((category, idx) => (
                    <motion.div
                      key={category.category}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.6, delay: 0.6 + idx * 0.1 }}
                      className="group"
                    >
                      <div className={`bg-gradient-to-r ${category.color} p-0.5 rounded-2xl`}>
                        <div className="bg-slate-900/90 backdrop-blur-sm rounded-2xl p-6 h-full group-hover:bg-slate-800/90 transition-all duration-300">
                          <h3 className="text-lg font-semibold text-white mb-4">{category.category}</h3>
                          <div className="space-y-3">
                            {category.searches.map((search) => (
                              <button
                                key={search.id}
                                onClick={() => setSearchType(search.id)}
                                className={`w-full flex items-center space-x-3 p-3 rounded-lg text-left transition-all duration-200 ${
                                  searchType === search.id 
                                    ? 'bg-blue-500/20 text-blue-400 shadow-lg shadow-blue-500/25' 
                                    : 'hover:bg-slate-700/50 text-slate-300'
                                }`}
                              >
                                {search.icon}
                                <div>
                                  <div className="font-medium">{search.name}</div>
                                  <div className="text-xs text-slate-400">{search.desc}</div>
                                </div>
                              </button>
                            ))}
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>

                {/* Advanced Search Bar */}
                <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 shadow-2xl shadow-blue-500/5">
                  <form onSubmit={handleSearch} className="space-y-4">
                    <div className="relative">
                      <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder={`${currentSearchType.name} - ${currentSearchType.desc}`}
                        className="w-full bg-slate-800/50 border border-slate-600/50 rounded-xl px-6 py-4 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
                      />
                      <div className="absolute right-4 top-4 flex items-center space-x-2">
                        <button
                          type="button"
                          onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
                          className="p-2 rounded-lg hover:bg-slate-700 transition-colors"
                        >
                          <Settings className="w-5 h-5 text-slate-400" />
                        </button>
                      </div>
                    </div>

                    {/* Advanced Filters Panel */}
                    <AnimatePresence>
                      {showAdvancedFilters && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          exit={{ opacity: 0, height: 0 }}
                          className="border-t border-slate-700/50 pt-4"
                        >
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {advancedFilters.map((filter) => (
                              <div key={filter.id}>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                  {filter.name}
                                </label>
                                <select className="w-full bg-slate-800/50 border border-slate-600/50 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50">
                                  {filter.options.map((option) => (
                                    <option key={option} value={option}>{option}</option>
                                  ))}
                                </select>
                              </div>
                            ))}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>

                    <button
                      type="submit"
                      disabled={isSearching || !searchQuery.trim()}
                      className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-slate-700 disabled:to-slate-700 text-white font-semibold py-4 px-8 rounded-xl transition-all duration-200 shadow-lg shadow-blue-500/25 disabled:shadow-none flex items-center justify-center space-x-2"
                    >
                      {isSearching ? (
                        <>
                          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                          <span>Searching...</span>
                        </>
                      ) : (
                        <>
                          <Search className="w-5 h-5" />
                          <span>Search Intelligence</span>
                        </>
                      )}
                    </button>
                  </form>
                </div>

                {/* Search Results Preview */}
                <AnimatePresence>
                  {searchResults && (
                    <motion.div
                      initial={{ opacity: 0, y: 30 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -30 }}
                      className="mt-8 bg-slate-900/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 shadow-2xl"
                    >
                      <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center space-x-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center">
                            <CheckCircle className="w-6 h-6 text-white" />
                          </div>
                          <div>
                            <h3 className="text-xl font-semibold text-white">Intelligence Found</h3>
                            <p className="text-slate-400">Search completed in {searchResults.timeMs}ms</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-green-400">{searchResults.confidence}%</div>
                          <div className="text-sm text-slate-400">Confidence</div>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                        <div className="bg-slate-800/50 rounded-lg p-4 text-center">
                          <div className="text-xl font-bold text-blue-400">{searchResults.sources}</div>
                          <div className="text-sm text-slate-400">Sources</div>
                        </div>
                        <div className="bg-slate-800/50 rounded-lg p-4 text-center">
                          <div className="text-xl font-bold text-purple-400">{searchResults.dataPoints}</div>
                          <div className="text-sm text-slate-400">Data Points</div>
                        </div>
                        <div className="bg-slate-800/50 rounded-lg p-4 text-center">
                          <div className="text-xl font-bold text-green-400">{searchResults.preview.socialProfiles}</div>
                          <div className="text-sm text-slate-400">Profiles</div>
                        </div>
                        <div className="bg-slate-800/50 rounded-lg p-4 text-center">
                          <div className="text-xl font-bold text-orange-400">{searchResults.preview.associatedAccounts}</div>
                          <div className="text-sm text-slate-400">Accounts</div>
                        </div>
                      </div>

                      <div className="bg-slate-800/30 rounded-xl p-6 mb-6">
                        <h4 className="text-lg font-semibold text-white mb-4 flex items-center">
                          <Eye className="w-5 h-5 mr-2" />
                          Preview Results
                          <span className="ml-auto text-sm bg-gradient-to-r from-yellow-400 to-orange-400 bg-clip-text text-transparent font-bold">
                            ⭐ Premium Required
                          </span>
                        </h4>
                        <div className="space-y-3">
                          <div className="flex justify-between items-center p-3 bg-slate-700/30 rounded-lg">
                            <span className="text-slate-300">Location:</span>
                            <span className="text-white font-medium filter blur-sm">{searchResults.preview.location}</span>
                          </div>
                          <div className="flex justify-between items-center p-3 bg-slate-700/30 rounded-lg">
                            <span className="text-slate-300">Associated Accounts:</span>
                            <span className="text-white font-medium filter blur-sm">{searchResults.preview.associatedAccounts} found</span>
                          </div>
                          <div className="flex justify-between items-center p-3 bg-slate-700/30 rounded-lg">
                            <span className="text-slate-300">Social Profiles:</span>
                            <span className="text-white font-medium filter blur-sm">{searchResults.preview.socialProfiles} found</span>
                          </div>
                          <div className="flex justify-between items-center p-3 bg-slate-700/30 rounded-lg">
                            <span className="text-slate-300">Risk Score:</span>
                            <span className="text-white font-medium filter blur-sm">{searchResults.preview.riskScore}/100</span>
                          </div>
                        </div>
                      </div>

                      <div className="flex flex-col sm:flex-row gap-4">
                        <button className="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 shadow-lg shadow-green-500/25 flex items-center justify-center space-x-2">
                          <Download className="w-5 h-5" />
                          <span>Get Full Report - $6.99</span>
                        </button>
                        <button className="px-6 py-3 border border-slate-600 rounded-xl text-slate-300 hover:bg-slate-800/50 transition-all duration-200 flex items-center justify-center space-x-2">
                          <Bookmark className="w-5 h-5" />
                          <span>Save Search</span>
                        </button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            </motion.div>

            {/* Live Activity Feed - Inspired by Linear/Discord */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
              <div className="lg:col-span-2">
                <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                  <Activity className="w-6 h-6 mr-3 text-blue-400" />
                  Live Intelligence Feed
                </h2>
                <div className="space-y-4">
                  {liveFeed.map((item, idx) => (
                    <motion.div
                      key={item.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: idx * 0.1 }}
                      className="bg-slate-900/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-4 hover:bg-slate-800/50 transition-all duration-200"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                            item.type === 'search' ? 'bg-blue-500/20 text-blue-400' :
                            item.type === 'breach' ? 'bg-red-500/20 text-red-400' :
                            item.type === 'success' ? 'bg-green-500/20 text-green-400' :
                            item.type === 'crypto' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-purple-500/20 text-purple-400'
                          }`}>
                            {item.type === 'search' && <Search className="w-4 h-4" />}
                            {item.type === 'breach' && <Shield className="w-4 h-4" />}
                            {item.type === 'success' && <CheckCircle className="w-4 h-4" />}
                            {item.type === 'crypto' && <Database className="w-4 h-4" />}
                            {item.type === 'image' && <Image className="w-4 h-4" />}
                          </div>
                          <div>
                            <p className="text-white">
                              <span className="font-medium text-blue-400">{item.user}</span> {item.action}
                            </p>
                            <p className="text-sm text-slate-400">{item.time}</p>
                          </div>
                        </div>
                        {item.confidence && (
                          <div className="text-right">
                            <div className="text-sm font-medium text-green-400">{item.confidence}%</div>
                            <div className="text-xs text-slate-500">confidence</div>
                          </div>
                        )}
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Metrics Dashboard */}
              <div>
                <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                  <BarChart3 className="w-6 h-6 mr-3 text-purple-400" />
                  Platform Metrics
                </h2>
                <div className="space-y-4">
                  <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-300">Search Volume</span>
                      <TrendingUp className="w-5 h-5 text-green-400" />
                    </div>
                    <div className="text-2xl font-bold text-white">{liveMetrics.searches.today.toLocaleString()}</div>
                    <div className="text-sm text-slate-400">+12.3% from yesterday</div>
                  </div>

                  <div className="bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/20 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-300">Active Users</span>
                      <Users className="w-5 h-5 text-green-400" />
                    </div>
                    <div className="text-2xl font-bold text-white">{liveMetrics.users.online.toLocaleString()}</div>
                    <div className="text-sm text-slate-400">Across 47 countries</div>
                  </div>

                  <div className="bg-gradient-to-r from-yellow-500/10 to-orange-500/10 border border-yellow-500/20 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-300">System Status</span>
                      <CheckCircle className="w-5 h-5 text-green-400" />
                    </div>
                    <div className="text-2xl font-bold text-white">{liveMetrics.uptime}%</div>
                    <div className="text-sm text-slate-400">Uptime (30 days)</div>
                  </div>

                  <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-500/20 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-300">Response Time</span>
                      <Zap className="w-5 h-5 text-yellow-400" />
                    </div>
                    <div className="text-2xl font-bold text-white">{liveMetrics.avgResponse}s</div>
                    <div className="text-sm text-slate-400">Average response</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>

        {/* Enhanced Footer */}
        <footer className="border-t border-slate-800/50 bg-slate-950/50 backdrop-blur-xl">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 via-purple-500 to-cyan-500 rounded-xl flex items-center justify-center">
                    <Brain className="w-6 h-6 text-white" />
                  </div>
                  <span className="text-xl font-bold text-white">IntelliSearch Pro</span>
                </div>
                <p className="text-slate-400 leading-relaxed">
                  Next-generation intelligence gathering platform for professionals and enterprises.
                </p>
                <div className="flex space-x-4">
                  <button className="w-10 h-10 bg-slate-800 rounded-lg flex items-center justify-center hover:bg-slate-700 transition-colors">
                    <GitBranch className="w-5 h-5 text-slate-400" />
                  </button>
                  <button className="w-10 h-10 bg-slate-800 rounded-lg flex items-center justify-center hover:bg-slate-700 transition-colors">
                    <MessageCircle className="w-5 h-5 text-slate-400" />
                  </button>
                  <button className="w-10 h-10 bg-slate-800 rounded-lg flex items-center justify-center hover:bg-slate-700 transition-colors">
                    <Share2 className="w-5 h-5 text-slate-400" />
                  </button>
                </div>
              </div>

              <div>
                <h4 className="font-bold text-white mb-6">Intelligence</h4>
                <ul className="space-y-3">
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">People Search</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Email Investigation</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Phone Lookup</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Image Analysis</a></li>
                </ul>
              </div>

              <div>
                <h4 className="font-bold text-white mb-6">Platform</h4>
                <ul className="space-y-3">
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">API Access</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Documentation</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Status Page</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Pricing</a></li>
                </ul>
              </div>

              <div>
                <h4 className="font-bold text-white mb-6">Support</h4>
                <ul className="space-y-3">
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Help Center</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Contact</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Community</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Security</a></li>
                </ul>
              </div>
            </div>

            <div className="border-t border-slate-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
              <p className="text-slate-500 text-sm">
                © 2024 IntelliSearch Pro. All rights reserved. Advanced Intelligence Platform.
              </p>
              <div className="flex items-center space-x-6 mt-4 md:mt-0">
                <a href="#" className="text-slate-500 hover:text-white transition-colors text-sm">Privacy</a>
                <a href="#" className="text-slate-500 hover:text-white transition-colors text-sm">Terms</a>
                <a href="#" className="text-slate-500 hover:text-white transition-colors text-sm">Security</a>
                <div className="flex items-center space-x-2 text-slate-500 text-sm">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>All systems operational</span>
                </div>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}