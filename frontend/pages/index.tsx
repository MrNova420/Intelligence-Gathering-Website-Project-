import Head from 'next/head'
import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence, useAnimation } from 'framer-motion'
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
  Zap as ZapIcon, Bot, Cpu as ProcessorIcon, Orbit
} from 'lucide-react'

// Next-Gen Quantum Intelligence Platform - Revolutionary Design Vision
export default function QuantumIntelliSearch() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchType, setSearchType] = useState('quantum-phone')
  const [isSearching, setIsSearching] = useState(false)
  const [searchResults, setSearchResults] = useState(null)
  const [showResults, setShowResults] = useState(false)
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const [quantumField, setQuantumField] = useState(false)
  const [aiThinking, setAiThinking] = useState(false)
  const canvasRef = useRef(null)
  const controls = useAnimation()

  // Revolutionary live metrics with quantum fluctuations
  const [quantumMetrics, setQuantumMetrics] = useState({
    quantumUsers: 7429,
    multiDimensionalScans: 124876,
    aiConfidence: 99.4,
    threatMatrix: 892,
    quantumEntanglement: 97.8,
    neuralNetworks: 34567,
    darkWebNodes: 8934,
    blockchainValidations: 45678
  })

  // Next-generation quantum search capabilities
  const quantumSearchTypes = [
    { 
      id: 'quantum-phone', 
      name: 'Quantum Phone Intelligence', 
      icon: <Smartphone className="w-10 h-10" />, 
      placeholder: 'Quantum phone analysis - enter target number...',
      description: 'Multi-dimensional carrier mapping, quantum location tracking, parallel reality social correlation',
      gradient: 'from-cyan-300 via-blue-400 to-indigo-600',
      particles: 'cyan',
      confidence: 99.2
    },
    { 
      id: 'neuro-email', 
      name: 'Neuro Email Synthesis', 
      icon: <Mail className="w-10 h-10" />, 
      placeholder: 'Neural email trace - quantum verification...',
      description: 'AI-powered breach prediction, quantum encryption analysis, temporal email tracking',
      gradient: 'from-purple-300 via-pink-400 to-red-500',
      particles: 'purple',
      confidence: 98.7
    },
    { 
      id: 'bio-identity', 
      name: 'Bio-Quantum Identity Matrix', 
      icon: <User className="w-10 h-10" />, 
      placeholder: 'Biometric quantum search - full spectrum analysis...',
      description: 'Dimensional identity mapping, quantum behavioral analysis, parallel universe tracking',
      gradient: 'from-green-300 via-emerald-400 to-teal-600',
      particles: 'green',
      confidence: 97.9
    },
    { 
      id: 'neural-social', 
      name: 'Neural Social Web', 
      icon: <Users className="w-10 h-10" />, 
      placeholder: 'Social quantum entanglement analysis...',
      description: 'Cross-dimensional social mapping, quantum relationship analysis, temporal connection tracking',
      gradient: 'from-orange-300 via-amber-400 to-yellow-500',
      particles: 'orange',
      confidence: 96.8
    },
    { 
      id: 'quantum-image', 
      name: 'Quantum Visual Recognition', 
      icon: <Image className="w-10 h-10" />, 
      placeholder: 'Multi-dimensional image analysis...',
      description: 'Quantum facial reconstruction, parallel reality image matching, temporal visual tracking',
      gradient: 'from-rose-300 via-pink-400 to-fuchsia-600',
      particles: 'pink',
      confidence: 98.1
    },
    { 
      id: 'darkweb-intel', 
      name: 'Dark Web Quantum Scan', 
      icon: <Globe className="w-10 h-10" />, 
      placeholder: 'Deep quantum web intelligence...',
      description: 'Multi-layer dark web analysis, quantum anonymity breaking, temporal footprint tracking',
      gradient: 'from-slate-400 via-gray-500 to-zinc-600',
      particles: 'gray',
      confidence: 95.4
    }
  ]

  // Mouse tracking for holographic effects
  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY })
    }
    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [])

  // Continuous metrics updates with realistic fluctuations
  useEffect(() => {
    const interval = setInterval(() => {
      setLiveMetrics(prev => ({
        usersOnline: Math.max(4500, prev.usersOnline + Math.floor(Math.random() * 20 - 10)),
        searchesToday: prev.searchesToday + Math.floor(Math.random() * 100),
        accuracy: Math.min(99.9, Math.max(97.0, prev.accuracy + (Math.random() - 0.5) * 0.5)),
        threats: Math.max(1000, prev.threats + Math.floor(Math.random() * 10 - 5)),
        aiProcessing: Math.min(99.9, Math.max(85.0, prev.aiProcessing + (Math.random() - 0.5) * 2)),
        networksScanned: prev.networksScanned + Math.floor(Math.random() * 500)
      }))
    }, 2000)
    return () => clearInterval(interval)
  }, [])

  // Advanced search function
  const handleSearch = async () => {
    if (!searchQuery.trim()) return
    
    setIsSearching(true)
    setHologramEffect(true)
    
    // Simulate advanced processing
    await new Promise(resolve => setTimeout(resolve, 2500))
    
    const mockResults = {
      phone: {
        location: 'San Francisco, CA, USA',
        carrier: 'Quantum Wireless Networks',
        lineType: 'Neural Interface Mobile',
        confidence: 97.8,
        socialProfiles: 15,
        breachData: 2,
        associatedEmails: 8,
        threatLevel: 'Low',
        lastActivity: '2 hours ago'
      },
      email: {
        status: 'Quantum Verified & Active',
        breaches: 3,
        socialAccounts: 22,
        lastSeen: '47 minutes ago',
        confidence: 94.3,
        riskScore: 'Medium-Low',
        domainAge: '12 years',
        aiTrustScore: 8.7
      }
    }
    
    setSearchResults(mockResults[searchType] || mockResults.phone)
    setShowPreview(true)
    setIsSearching(false)
    setHologramEffect(false)
  }

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden relative">
      <Head>
        <title>IntelliSearch Pro - Ultra-Futuristic Neural Intelligence Platform</title>
        <meta name="description" content="Next-generation intelligence platform with quantum-level analysis, neural networks, and holographic visualization." />
      </Head>

      {/* Ultra-Advanced Background System */}
      <div className="fixed inset-0 z-0 overflow-hidden">
        {/* Dynamic Gradient Mesh */}
        <div className="absolute inset-0 bg-gradient-to-br from-black via-slate-900 to-purple-950/30" />
        
        {/* Animated Circuit Pattern */}
        <div className="absolute inset-0 opacity-20">
          <div className="w-full h-full" 
               style={{
                 backgroundImage: `radial-gradient(circle at 25% 25%, cyan 0%, transparent 2%),
                                   radial-gradient(circle at 75% 75%, purple 0%, transparent 2%),
                                   linear-gradient(45deg, transparent 48%, cyan 50%, transparent 52%)`,
                 backgroundSize: '100px 100px, 150px 150px, 200px 200px',
                 animation: 'drift 20s linear infinite'
               }} />
        </div>

        {/* Floating Particles */}
        {[...Array(30)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-cyan-400 rounded-full opacity-60"
            initial={{ 
              x: Math.random() * (typeof window !== 'undefined' ? window.innerWidth : 1920), 
              y: Math.random() * (typeof window !== 'undefined' ? window.innerHeight : 1080)
            }}
            animate={{
              x: Math.random() * (typeof window !== 'undefined' ? window.innerWidth : 1920),
              y: Math.random() * (typeof window !== 'undefined' ? window.innerHeight : 1080),
              scale: [0.5, 1.5, 0.5],
              opacity: [0.3, 0.8, 0.3]
            }}
            transition={{
              duration: Math.random() * 20 + 10,
              repeat: Infinity,
              ease: "linear"
            }}
          />
        ))}

        {/* Mouse-following Holographic Orb */}
        <motion.div
          className="absolute w-96 h-96 rounded-full opacity-10 pointer-events-none"
          style={{
            background: 'radial-gradient(circle, cyan 0%, purple 50%, transparent 70%)',
            left: mousePosition.x - 192,
            top: mousePosition.y - 192,
            filter: 'blur(40px)'
          }}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.1, 0.3, 0.1]
          }}
          transition={{ duration: 3, repeat: Infinity }}
        />
      </div>

      {/* Futuristic Header */}
      <motion.header 
        className="relative z-50 backdrop-blur-xl bg-black/50 border-b border-cyan-500/20"
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 1, ease: "easeOut" }}
      >
        <div className="max-w-8xl mx-auto px-8 py-6">
          <div className="flex items-center justify-between">
            {/* Holographic Logo */}
            <motion.div 
              className="flex items-center space-x-6"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="relative">
                <motion.div
                  className="w-16 h-16 bg-gradient-to-br from-cyan-400 via-purple-500 to-pink-600 rounded-2xl flex items-center justify-center shadow-2xl shadow-cyan-500/50"
                  animate={{
                    boxShadow: [
                      '0 0 20px rgba(6, 182, 212, 0.5)',
                      '0 0 40px rgba(168, 85, 247, 0.5)',
                      '0 0 20px rgba(6, 182, 212, 0.5)'
                    ]
                  }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  <Brain className="w-9 h-9 text-white" />
                </motion.div>
                {/* Holographic Glow Ring */}
                <motion.div
                  className="absolute -inset-2 rounded-2xl border-2 border-cyan-400/30"
                  animate={{
                    rotate: 360,
                    borderColor: ['rgba(6, 182, 212, 0.3)', 'rgba(168, 85, 247, 0.3)', 'rgba(6, 182, 212, 0.3)']
                  }}
                  transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                />
              </div>
              <div>
                <h1 className="text-3xl font-black bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                  IntelliSearch Pro
                </h1>
                <p className="text-sm text-cyan-300 font-semibold tracking-wide">Neural Intelligence Network</p>
              </div>
            </motion.div>

            {/* Real-time Metrics HUD */}
            <div className="hidden lg:flex items-center space-x-6">
              {[
                { label: 'Neural Users', value: liveMetrics.usersOnline.toLocaleString(), icon: <Users className="w-5 h-5" />, color: 'text-green-400', bg: 'bg-green-500/10' },
                { label: 'AI Accuracy', value: `${liveMetrics.accuracy.toFixed(1)}%`, icon: <Brain className="w-5 h-5" />, color: 'text-cyan-400', bg: 'bg-cyan-500/10' },
                { label: 'Quantum Scans', value: liveMetrics.searchesToday.toLocaleString(), icon: <Search className="w-5 h-5" />, color: 'text-purple-400', bg: 'bg-purple-500/10' },
                { label: 'Threat Matrix', value: liveMetrics.threats.toLocaleString(), icon: <Shield className="w-5 h-5" />, color: 'text-red-400', bg: 'bg-red-500/10' }
              ].map((metric, i) => (
                <motion.div
                  key={metric.label}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-xl ${metric.bg} backdrop-blur border border-white/10 shadow-lg`}
                  initial={{ opacity: 0, y: -20, scale: 0.8 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ delay: i * 0.2, duration: 0.8 }}
                  whileHover={{ scale: 1.05, y: -2 }}
                >
                  <div className={metric.color}>{metric.icon}</div>
                  <div>
                    <div className={`font-bold ${metric.color} text-lg`}>{metric.value}</div>
                    <div className="text-xs text-slate-400">{metric.label}</div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Control Panel */}
            <div className="flex items-center space-x-4">
              <motion.button
                className="p-3 rounded-xl bg-cyan-500/10 border border-cyan-400/20 hover:bg-cyan-500/20 transition-all relative"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
              >
                <Bell className="w-6 h-6 text-cyan-400" />
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full animate-pulse flex items-center justify-center">
                  <span className="text-xs font-bold text-white">3</span>
                </div>
              </motion.button>
              
              <motion.button
                className="p-3 rounded-xl bg-purple-500/10 border border-purple-400/20 hover:bg-purple-500/20 transition-all"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
              >
                <User className="w-6 h-6 text-purple-400" />
              </motion.button>
            </div>
          </div>
        </div>
      </motion.header>

      <div className="relative z-10">
        {/* Ultra-Futuristic Hero Section */}
        <section className="relative pt-32 pb-40 overflow-hidden">
          <div className="max-w-8xl mx-auto px-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
              
              {/* Left: Holographic Search Interface */}
              <motion.div
                initial={{ opacity: 0, x: -100 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 1.2, ease: "easeOut" }}
                className="space-y-12"
              >
                <div className="space-y-8">
                  <motion.h1 
                    className="text-7xl lg:text-8xl font-black leading-tight"
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3, duration: 1 }}
                  >
                    <motion.span 
                      className="bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent"
                      animate={{
                        backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
                      }}
                      transition={{ duration: 5, repeat: Infinity }}
                    >
                      Neural
                    </motion.span>
                    <br />
                    <motion.span 
                      className="bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent"
                      animate={{
                        backgroundPosition: ['100% 50%', '0% 50%', '100% 50%'],
                      }}
                      transition={{ duration: 5, repeat: Infinity }}
                    >
                      Intelligence
                    </motion.span>
                  </motion.h1>
                  
                  <motion.p 
                    className="text-2xl text-slate-300 leading-relaxed max-w-3xl"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6, duration: 1 }}
                  >
                    Next-generation quantum intelligence platform with 
                    <span className="text-cyan-400 font-bold"> neural network processing</span>, 
                    holographic visualization, and 
                    <span className="text-purple-400 font-bold"> dimensional threat analysis</span>.
                  </motion.p>
                </div>

                {/* Holographic Search Interface */}
                <motion.div
                  className="space-y-10 p-10 rounded-3xl bg-gradient-to-br from-slate-900/50 to-black/50 backdrop-blur-xl border border-cyan-500/20 shadow-2xl shadow-cyan-500/10"
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.9, duration: 1 }}
                  style={{
                    boxShadow: '0 0 60px rgba(6, 182, 212, 0.1), inset 0 1px 0 rgba(255,255,255,0.1)'
                  }}
                >
                  {/* Search Type Selector */}
                  <div className="space-y-6">
                    <div className="flex items-center justify-between">
                      <h3 className="text-xl font-bold text-white">Neural Analysis Type</h3>
                      <div className="flex items-center space-x-3 text-sm text-cyan-400">
                        <motion.div 
                          className="w-3 h-3 bg-green-500 rounded-full"
                          animate={{ opacity: [1, 0.3, 1] }}
                          transition={{ duration: 2, repeat: Infinity }}
                        />
                        <span className="font-semibold">Quantum Network Online</span>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      {searchTypes.map((type, index) => (
                        <motion.button
                          key={type.id}
                          onClick={() => setSearchType(type.id)}
                          className={`p-6 rounded-2xl border-2 transition-all duration-500 relative overflow-hidden ${
                            searchType === type.id
                              ? 'border-cyan-400 bg-gradient-to-br from-cyan-500/20 to-purple-600/20 shadow-lg shadow-cyan-500/20'
                              : 'border-white/10 bg-white/5 hover:border-cyan-400/50 hover:bg-cyan-500/10'
                          }`}
                          whileHover={{ 
                            scale: 1.03, 
                            y: -2,
                            boxShadow: '0 10px 30px rgba(6, 182, 212, 0.2)'
                          }}
                          whileTap={{ scale: 0.98 }}
                          initial={{ opacity: 0, y: 30 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 1.2 + index * 0.1 }}
                        >
                          {/* Holographic Background Effect */}
                          {searchType === type.id && (
                            <motion.div
                              className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 to-purple-600/10"
                              animate={{
                                opacity: [0.1, 0.3, 0.1],
                                scale: [1, 1.05, 1]
                              }}
                              transition={{ duration: 2, repeat: Infinity }}
                            />
                          )}
                          
                          <div className="flex items-center space-x-4 mb-3 relative z-10">
                            <motion.div 
                              className={`p-3 rounded-xl bg-gradient-to-br ${type.color} ${type.glow} shadow-lg`}
                              whileHover={{ rotate: 5, scale: 1.1 }}
                            >
                              {type.icon}
                            </motion.div>
                            <span className="font-bold text-white text-lg">{type.name}</span>
                          </div>
                          <p className="text-sm text-slate-400 text-left leading-relaxed relative z-10">
                            {type.description}
                          </p>
                        </motion.button>
                      ))}
                    </div>
                  </div>

                  {/* Advanced Search Input */}
                  <div className="space-y-6">
                    <div className="relative">
                      <motion.input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder={searchTypes.find(t => t.id === searchType)?.placeholder}
                        className="w-full p-8 rounded-2xl bg-black/50 border-2 border-cyan-400/20 text-white placeholder-slate-400 focus:border-cyan-400 focus:outline-none transition-all duration-500 text-xl font-medium"
                        style={{
                          boxShadow: 'inset 0 2px 20px rgba(0,0,0,0.5), 0 0 20px rgba(6, 182, 212, 0.1)'
                        }}
                        whileFocus={{ 
                          scale: 1.02,
                          boxShadow: 'inset 0 2px 20px rgba(0,0,0,0.5), 0 0 30px rgba(6, 182, 212, 0.3)'
                        }}
                        onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                      />
                      
                      {/* Holographic Search Indicator */}
                      <AnimatePresence>
                        {isSearching && (
                          <motion.div
                            className="absolute right-6 top-1/2 transform -translate-y-1/2"
                            initial={{ opacity: 0, scale: 0 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0 }}
                          >
                            <motion.div
                              className="w-10 h-10 rounded-full border-3 border-cyan-400 border-t-transparent"
                              animate={{ rotate: 360 }}
                              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                            />
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>

                    {/* Neural Search Button */}
                    <motion.button
                      onClick={handleSearch}
                      disabled={!searchQuery.trim() || isSearching}
                      className="w-full p-8 rounded-2xl bg-gradient-to-r from-cyan-500 via-purple-600 to-pink-600 text-white font-bold text-xl disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden shadow-2xl shadow-cyan-500/30"
                      whileHover={{ 
                        scale: 1.02, 
                        boxShadow: '0 20px 40px rgba(6, 182, 212, 0.4)',
                        y: -2
                      }}
                      whileTap={{ scale: 0.98 }}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 1.8 }}
                    >
                      {/* Animated Background Gradient */}
                      <motion.div
                        className="absolute inset-0 bg-gradient-to-r from-white/20 via-cyan-300/20 to-white/20"
                        animate={{ x: ['-100%', '200%'] }}
                        transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                      />
                      
                      <div className="flex items-center justify-center space-x-4 relative z-10">
                        {isSearching ? (
                          <>
                            <motion.div
                              animate={{ 
                                rotate: 360,
                                scale: [1, 1.2, 1]
                              }}
                              transition={{ 
                                rotate: { duration: 2, repeat: Infinity, ease: "linear" },
                                scale: { duration: 1, repeat: Infinity }
                              }}
                            >
                              <Radar className="w-8 h-8" />
                            </motion.div>
                            <span className="text-xl">Neural Processing...</span>
                          </>
                        ) : (
                          <>
                            <Search className="w-8 h-8" />
                            <span className="text-xl">Launch Neural Analysis</span>
                          </>
                        )}
                      </div>

                      {/* Holographic Border Effect */}
                      {hologramEffect && (
                        <motion.div
                          className="absolute inset-0 rounded-2xl border-2 border-cyan-400"
                          animate={{
                            opacity: [0, 1, 0],
                            scale: [1, 1.1, 1]
                          }}
                          transition={{ duration: 0.5, repeat: 3 }}
                        />
                      )}
                    </motion.button>
                  </div>
                </motion.div>
              </motion.div>

              {/* Right: Holographic Visualization Dashboard */}
              <motion.div
                initial={{ opacity: 0, x: 100 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 1.2, delay: 0.5, ease: "easeOut" }}
                className="space-y-10"
              >
                {/* Live Neural Network Visualization */}
                <div className="space-y-6">
                  <h2 className="text-3xl font-bold text-white mb-8">Neural Network Activity</h2>
                  
                  {/* Holographic Display */}
                  <motion.div
                    className="h-96 rounded-3xl bg-gradient-to-br from-slate-900/50 to-black/80 backdrop-blur-xl border border-cyan-500/20 p-8 relative overflow-hidden shadow-2xl shadow-cyan-500/10"
                    whileHover={{ scale: 1.02 }}
                  >
                    {/* Neural Network Visualization */}
                    <div className="absolute inset-0 flex items-center justify-center">
                      <motion.div
                        className="w-64 h-64 relative"
                        animate={{ rotate: 360 }}
                        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                      >
                        {/* Central Node */}
                        <motion.div
                          className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-16 h-16 bg-gradient-to-br from-cyan-400 to-purple-600 rounded-full shadow-lg shadow-cyan-500/50"
                          animate={{
                            scale: [1, 1.2, 1],
                            boxShadow: [
                              '0 0 20px rgba(6, 182, 212, 0.5)',
                              '0 0 40px rgba(168, 85, 247, 0.8)',
                              '0 0 20px rgba(6, 182, 212, 0.5)'
                            ]
                          }}
                          transition={{ duration: 2, repeat: Infinity }}
                        />
                        
                        {/* Orbital Nodes */}
                        {[...Array(8)].map((_, i) => (
                          <motion.div
                            key={i}
                            className="absolute w-8 h-8 bg-gradient-to-br from-pink-400 to-cyan-400 rounded-full shadow-lg"
                            style={{
                              top: '50%',
                              left: '50%',
                              transformOrigin: '0 0'
                            }}
                            animate={{
                              rotate: i * 45,
                              x: 100 * Math.cos((i * 45) * Math.PI / 180),
                              y: 100 * Math.sin((i * 45) * Math.PI / 180),
                              scale: [0.8, 1.2, 0.8]
                            }}
                            transition={{
                              rotate: { duration: 10, repeat: Infinity, ease: "linear" },
                              scale: { duration: 2, repeat: Infinity, delay: i * 0.2 }
                            }}
                          />
                        ))}
                      </motion.div>
                    </div>

                    {/* Data Overlay */}
                    <div className="absolute top-6 left-6 space-y-2">
                      <div className="text-cyan-400 font-bold text-lg">Neural Processing: {liveMetrics.aiProcessing.toFixed(1)}%</div>
                      <div className="text-purple-400 font-semibold">Networks Scanned: {liveMetrics.networksScanned.toLocaleString()}</div>
                      <div className="text-pink-400 font-semibold">Threat Analysis: Active</div>
                    </div>

                    {/* Scanning Effect */}
                    <motion.div
                      className="absolute inset-0 border-2 border-cyan-400/30 rounded-3xl"
                      animate={{
                        borderColor: ['rgba(6, 182, 212, 0.3)', 'rgba(168, 85, 247, 0.6)', 'rgba(6, 182, 212, 0.3)']
                      }}
                      transition={{ duration: 3, repeat: Infinity }}
                    />
                  </motion.div>
                </div>

                {/* Advanced Metrics Grid */}
                <div className="grid grid-cols-2 gap-6">
                  {[
                    { 
                      title: 'Quantum Accuracy',
                      value: `${liveMetrics.accuracy.toFixed(1)}%`,
                      change: '+0.3%',
                      color: 'from-green-400 to-emerald-600',
                      icon: <Target className="w-6 h-6" />
                    },
                    { 
                      title: 'Neural Speed',
                      value: '0.24s',
                      change: '-0.02s',
                      color: 'from-cyan-400 to-blue-600',
                      icon: <Zap className="w-6 h-6" />
                    },
                    { 
                      title: 'Threat Matrix',
                      value: liveMetrics.threats.toLocaleString(),
                      change: '+12',
                      color: 'from-red-400 to-pink-600',
                      icon: <Shield className="w-6 h-6" />
                    },
                    { 
                      title: 'Data Sources',
                      value: '342+',
                      change: '+3',
                      color: 'from-purple-400 to-indigo-600',
                      icon: <Database className="w-6 h-6" />
                    }
                  ].map((metric, index) => (
                    <motion.div
                      key={metric.title}
                      className="p-6 rounded-2xl bg-gradient-to-br from-slate-900/50 to-black/50 backdrop-blur-xl border border-white/10 relative overflow-hidden"
                      initial={{ opacity: 0, y: 30 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 2 + index * 0.1 }}
                      whileHover={{ 
                        scale: 1.05, 
                        y: -5,
                        boxShadow: '0 10px 30px rgba(0,0,0,0.3)'
                      }}
                    >
                      <div className="flex items-center justify-between mb-4">
                        <div className={`p-2 rounded-lg bg-gradient-to-br ${metric.color}`}>
                          {metric.icon}
                        </div>
                        <span className="text-green-400 text-sm font-semibold">{metric.change}</span>
                      </div>
                      
                      <div className="space-y-1">
                        <div className="text-2xl font-black text-white">{metric.value}</div>
                        <div className="text-sm text-slate-400">{metric.title}</div>
                      </div>

                      {/* Glow Effect */}
                      <motion.div
                        className={`absolute inset-0 bg-gradient-to-br ${metric.color} opacity-0 rounded-2xl`}
                        whileHover={{ opacity: 0.1 }}
                        transition={{ duration: 0.3 }}
                      />
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Search Results with Holographic Display */}
        <AnimatePresence>
          {showPreview && searchResults && (
            <motion.section
              className="py-20 relative"
              initial={{ opacity: 0, y: 100 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -100 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            >
              <div className="max-w-6xl mx-auto px-8">
                <motion.div
                  className="p-10 rounded-3xl bg-gradient-to-br from-slate-900/80 to-black/60 backdrop-blur-xl border border-cyan-500/20 shadow-2xl shadow-cyan-500/20"
                  initial={{ scale: 0.9 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  <div className="flex items-center justify-between mb-10">
                    <div className="flex items-center space-x-6">
                      <motion.div 
                        className="p-4 rounded-2xl bg-gradient-to-br from-green-500 to-emerald-600 shadow-lg shadow-green-500/50"
                        animate={{
                          boxShadow: [
                            '0 0 20px rgba(16, 185, 129, 0.5)',
                            '0 0 40px rgba(16, 185, 129, 0.8)',
                            '0 0 20px rgba(16, 185, 129, 0.5)'
                          ]
                        }}
                        transition={{ duration: 2, repeat: Infinity }}
                      >
                        <CheckCircle className="w-8 h-8 text-white" />
                      </motion.div>
                      <div>
                        <h3 className="text-3xl font-bold text-white">Neural Analysis Complete</h3>
                        <p className="text-slate-400 text-lg">Quantum verification successful • 97.8% confidence</p>
                      </div>
                    </div>
                    
                    <motion.button
                      onClick={() => setShowPreview(false)}
                      className="p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-colors"
                      whileHover={{ scale: 1.1, rotate: 90 }}
                      whileTap={{ scale: 0.9 }}
                    >
                      <XCircle className="w-8 h-8 text-slate-400" />
                    </motion.button>
                  </div>

                  {/* Holographic Results Display */}
                  <div className="space-y-8 mb-10">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {Object.entries(searchResults).map(([key, value], index) => (
                        <motion.div
                          key={key}
                          className="p-6 rounded-2xl bg-black/40 border border-cyan-400/20 relative overflow-hidden"
                          initial={{ opacity: 0, scale: 0.8, y: 30 }}
                          animate={{ opacity: 1, scale: 1, y: 0 }}
                          transition={{ delay: index * 0.1 }}
                          whileHover={{ scale: 1.02, y: -5 }}
                        >
                          <div className="flex items-center justify-between mb-3">
                            <span className="text-sm text-cyan-400 font-semibold uppercase tracking-wide">
                              {key.replace(/([A-Z])/g, ' $1').trim()}
                            </span>
                            <motion.div 
                              className="w-3 h-3 bg-green-500 rounded-full"
                              animate={{ opacity: [1, 0.3, 1] }}
                              transition={{ duration: 2, repeat: Infinity }}
                            />
                          </div>
                          
                          <div className="relative">
                            {/* Blurred Preview Effect */}
                            <div className="filter blur-sm select-none pointer-events-none">
                              <span className="text-white font-bold text-lg">{String(value)}</span>
                            </div>
                            
                            {/* Unlock Overlay */}
                            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-purple-600/20 rounded-lg flex items-center justify-center">
                              <Lock className="w-6 h-6 text-cyan-400" />
                            </div>
                          </div>

                          {/* Scanning Lines */}
                          <motion.div
                            className="absolute inset-0 bg-gradient-to-r from-transparent via-cyan-400/20 to-transparent h-full"
                            animate={{ x: ['-100%', '200%'] }}
                            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                          />
                        </motion.div>
                      ))}
                    </div>
                  </div>

                  {/* Premium Neural Unlock */}
                  <motion.div
                    className="text-center space-y-8"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.8 }}
                  >
                    <div className="space-y-4">
                      <h4 className="text-3xl font-bold text-white">Unlock Full Neural Analysis</h4>
                      <p className="text-slate-400 text-lg max-w-2xl mx-auto">
                        Access complete quantum intelligence report with dimensional analysis, 
                        threat assessment, and neural network verification
                      </p>
                    </div>
                    
                    <motion.button
                      className="px-12 py-6 rounded-2xl bg-gradient-to-r from-green-500 via-emerald-600 to-teal-600 text-white font-bold text-xl shadow-2xl shadow-green-500/30 relative overflow-hidden"
                      whileHover={{ 
                        scale: 1.05, 
                        boxShadow: '0 20px 40px rgba(16, 185, 129, 0.4)',
                        y: -3
                      }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <motion.div
                        className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent"
                        animate={{ x: ['-100%', '200%'] }}
                        transition={{ duration: 2, repeat: Infinity }}
                      />
                      <span className="relative z-10">Get Full Neural Report - $7.99</span>
                    </motion.button>
                    
                    <div className="flex items-center justify-center space-x-8 text-slate-400">
                      {[
                        { icon: <CheckCircle className="w-5 h-5 text-green-400" />, text: 'Instant Neural Access' },
                        { icon: <Shield className="w-5 h-5 text-blue-400" />, text: 'Quantum Security' },
                        { icon: <Award className="w-5 h-5 text-purple-400" />, text: 'Verified Intelligence' }
                      ].map((item, i) => (
                        <motion.span 
                          key={i}
                          className="flex items-center space-x-2"
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 1 + i * 0.1 }}
                        >
                          {item.icon}
                          <span className="font-semibold">{item.text}</span>
                        </motion.span>
                      ))}
                    </div>
                  </motion.div>
                </motion.div>
              </div>
            </motion.section>
          )}
        </AnimatePresence>

        {/* Call to Action */}
        <section className="py-32 relative">
          <div className="max-w-6xl mx-auto px-8 text-center">
            <motion.div
              className="space-y-12"
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 1 }}
              viewport={{ once: true }}
            >
              <motion.h2 
                className="text-6xl font-black"
                animate={{
                  backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
                }}
                transition={{ duration: 5, repeat: Infinity }}
              >
                <span className="bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                  Ready for Neural Intelligence?
                </span>
              </motion.h2>
              
              <p className="text-2xl text-slate-400 leading-relaxed max-w-4xl mx-auto">
                Join the future of intelligence gathering with our quantum-powered platform. 
                Experience the next evolution of digital investigation.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-6 justify-center">
                <motion.button
                  className="px-12 py-6 rounded-2xl bg-gradient-to-r from-cyan-500 to-purple-600 text-white font-bold text-xl shadow-2xl shadow-cyan-500/30"
                  whileHover={{ 
                    scale: 1.05, 
                    boxShadow: '0 20px 40px rgba(6, 182, 212, 0.4)',
                    y: -3
                  }}
                  whileTap={{ scale: 0.95 }}
                >
                  Begin Neural Analysis
                </motion.button>
                
                <motion.button
                  className="px-12 py-6 rounded-2xl border-2 border-cyan-400/50 text-cyan-400 font-bold text-xl hover:bg-cyan-500/10 transition-all"
                  whileHover={{ 
                    scale: 1.05,
                    borderColor: 'rgba(6, 182, 212, 1)',
                    boxShadow: '0 10px 30px rgba(6, 182, 212, 0.3)',
                    y: -3
                  }}
                  whileTap={{ scale: 0.95 }}
                >
                  Explore Quantum Features
                </motion.button>
              </div>
            </motion.div>
          </div>
        </section>
      </div>

      {/* Futuristic Footer */}
      <footer className="relative border-t border-cyan-500/20 bg-black/80 backdrop-blur-xl">
        <div className="max-w-8xl mx-auto px-8 py-20">
          <div className="text-center space-y-8">
            <div className="flex items-center justify-center space-x-4">
              <motion.div
                className="w-12 h-12 bg-gradient-to-br from-cyan-400 to-purple-600 rounded-xl flex items-center justify-center"
                animate={{
                  boxShadow: [
                    '0 0 20px rgba(6, 182, 212, 0.5)',
                    '0 0 40px rgba(168, 85, 247, 0.5)',
                    '0 0 20px rgba(6, 182, 212, 0.5)'
                  ]
                }}
                transition={{ duration: 3, repeat: Infinity }}
              >
                <Brain className="w-7 h-7 text-white" />
              </motion.div>
              <span className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                IntelliSearch Pro
              </span>
            </div>
            
            <p className="text-slate-400 text-lg max-w-3xl mx-auto leading-relaxed">
              Next-generation neural intelligence platform. Powered by quantum computing, 
              enhanced by AI, secured by advanced encryption.
            </p>
            
            <div className="text-slate-500 text-sm">
              © 2024 IntelliSearch Pro. Neural Intelligence Network. All rights reserved.
            </div>
          </div>
        </div>
      </footer>

      <style jsx>{`
        @keyframes drift {
          0% { transform: translateX(0px) translateY(0px); }
          25% { transform: translateX(10px) translateY(-10px); }
          50% { transform: translateX(-5px) translateY(-20px); }
          75% { transform: translateX(-15px) translateY(-10px); }
          100% { transform: translateX(0px) translateY(0px); }
        }
      `}</style>
    </div>
  )
}