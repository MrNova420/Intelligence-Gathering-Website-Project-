import Head from 'next/head'
import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
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
  Zap as ZapIcon, Bot, Cpu as ProcessorIcon, Orbit, Waves, Atom
} from 'lucide-react'

// Particle interface for quantum effects
interface Particle {
  id: number
  x: number
  y: number
  vx: number
  vy: number
  size: number
  color: string
  opacity: number
  life: number
}

// Ultimate Merged Intelligence Platform - AAA Industry Standards
export default function UltimateIntelligencePlatform() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchType, setSearchType] = useState('phone')
  const [isSearching, setIsSearching] = useState(false)
  const [searchResults, setSearchResults] = useState(null)
  const [showResults, setShowResults] = useState(false)
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const [particles, setParticles] = useState<Particle[]>([])
  const canvasRef = useRef<HTMLCanvasElement>(null)

  // Merged live platform metrics from all platforms
  const [metrics, setMetrics] = useState({
    activeUsers: 12847,
    searchesToday: 279016,
    aiAccuracy: 98.7,
    dataPoints: 15600000000, // 15.6B
    threatsBlocked: 1271,
    quantumProcessors: 18947,
    parallelRealities: 12834,
    neuralSynapses: 2847639,
    dimensionalGateways: 247,
    consciousnessStreams: 8934,
    quantumEntanglements: 18475,
    timelineAnalyses: 5692,
    multiverseConnections: 834
  })

  // Ultimate merged search capabilities (12 total from all platforms)
  const searchCapabilities = [
    { 
      id: 'phone', 
      name: 'Phone Intelligence',
      description: 'Advanced carrier detection, location mapping, social profiles',
      icon: <Smartphone className="w-5 h-5" />,
      confidence: 99.2,
      sources: 23,
      category: 'standard'
    },
    { 
      id: 'email', 
      name: 'Email Investigation',
      description: 'Breach detection, verification, account correlation',
      icon: <Mail className="w-5 h-5" />,
      confidence: 98.7,
      sources: 18,
      category: 'standard'
    },
    { 
      id: 'username', 
      name: 'Username Tracking',
      description: 'Cross-platform correlation, social media analysis',
      icon: <User className="w-5 h-5" />,
      confidence: 97.9,
      sources: 31,
      category: 'standard'
    },
    { 
      id: 'people', 
      name: 'People Search',
      description: 'Background checks, contact info, address history',
      icon: <Users className="w-5 h-5" />,
      confidence: 96.8,
      sources: 27,
      category: 'standard'
    },
    { 
      id: 'image', 
      name: 'Image Analysis',
      description: 'Facial recognition, reverse search, source tracking',
      icon: <Image className="w-5 h-5" />,
      confidence: 98.1,
      sources: 15,
      category: 'standard'
    },
    { 
      id: 'network', 
      name: 'Network Intelligence',
      description: 'IP geolocation, network topology, threat analysis',
      icon: <Network className="w-5 h-5" />,
      confidence: 95.4,
      sources: 42,
      category: 'standard'
    },
    // Quantum capabilities from NEXUS platform
    { 
      id: 'quantum-phone', 
      name: 'Quantum Phone Intel',
      description: 'Multi-dimensional carrier detection with parallel reality mapping',
      icon: <Atom className="w-5 h-5" />,
      confidence: 99.8,
      sources: 47,
      category: 'quantum'
    },
    { 
      id: 'neural-email', 
      name: 'Neural Email Matrix',
      description: 'AI-powered breach prediction with quantum encryption breaking',
      icon: <Brain className="w-5 h-5" />,
      confidence: 98.5,
      sources: 38,
      category: 'quantum'
    },
    { 
      id: 'bio-quantum', 
      name: 'Bio-Quantum Identity',
      description: 'Complete dimensional identity synthesis with consciousness analysis',
      icon: <Fingerprint className="w-5 h-5" />,
      confidence: 97.2,
      sources: 29,
      category: 'quantum'
    },
    { 
      id: 'social-constellation', 
      name: 'Social Constellation',
      description: 'Cross-dimensional social correlation with relationship quantum analysis',
      icon: <Network className="w-5 h-5" />,
      confidence: 96.1,
      sources: 52,
      category: 'quantum'
    },
    { 
      id: 'dark-web', 
      name: 'Dark Web Scanner',
      description: 'Multi-layer dark web analysis with quantum anonymity breaking',
      icon: <Shield className="w-5 h-5" />,
      confidence: 94.7,
      sources: 67,
      category: 'quantum'
    },
    { 
      id: 'universal-matrix', 
      name: 'Universal Data Matrix',
      description: 'Complete universal data synthesis across all dimensional databases',
      icon: <Database className="w-5 h-5" />,
      confidence: 96.9,
      sources: 89,
      category: 'quantum'
    }
  ]

  // Live metrics update with quantum fluctuations
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        activeUsers: prev.activeUsers + Math.floor(Math.random() * 5) - 2,
        searchesToday: prev.searchesToday + Math.floor(Math.random() * 8),
        aiAccuracy: Math.max(95, Math.min(99.9, prev.aiAccuracy + (Math.random() - 0.5) * 0.2)),
        dataPoints: prev.dataPoints + Math.floor(Math.random() * 1000),
        threatsBlocked: prev.threatsBlocked + Math.floor(Math.random() * 3),
        quantumProcessors: prev.quantumProcessors + Math.floor(Math.random() * 10) - 5,
        parallelRealities: prev.parallelRealities + Math.floor(Math.random() * 8) - 4,
        neuralSynapses: prev.neuralSynapses + Math.floor(Math.random() * 50),
        dimensionalGateways: prev.dimensionalGateways + Math.floor(Math.random() * 2),
        consciousnessStreams: prev.consciousnessStreams + Math.floor(Math.random() * 15) - 7,
        quantumEntanglements: prev.quantumEntanglements + Math.floor(Math.random() * 25) - 12,
        timelineAnalyses: prev.timelineAnalyses + Math.floor(Math.random() * 8) - 4,
        multiverseConnections: prev.multiverseConnections + Math.floor(Math.random() * 3) - 1
      }))
    }, 1500) // Faster updates for more dynamic feel
    return () => clearInterval(interval)
  }, [])

  // Initialize particles for quantum background
  useEffect(() => {
    const newParticles: Particle[] = []
    for (let i = 0; i < 180; i++) { // More particles for richer effect
      newParticles.push({
        id: i,
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: Math.random() * 3 + 1,
        color: ['#60A5FA', '#A78BFA', '#34D399', '#F472B6'][Math.floor(Math.random() * 4)],
        opacity: Math.random() * 0.6 + 0.2,
        life: Math.random() * 1000 + 500
      })
    }
    setParticles(newParticles)
  }, [])

  // Quantum particle animation system
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      setParticles(prevParticles => 
        prevParticles.map(particle => {
          // Update position
          let newX = particle.x + particle.vx
          let newY = particle.y + particle.vy
          
          // Bounce off edges
          if (newX <= 0 || newX >= canvas.width) particle.vx *= -1
          if (newY <= 0 || newY >= canvas.height) particle.vy *= -1
          
          // Mouse interaction
          const dx = mousePosition.x - newX
          const dy = mousePosition.y - newY
          const distance = Math.sqrt(dx * dx + dy * dy)
          
          if (distance < 100) {
            const force = (100 - distance) / 100
            newX -= dx * force * 0.01
            newY -= dy * force * 0.01
          }
          
          // Draw particle
          ctx.save()
          ctx.globalAlpha = particle.opacity
          ctx.fillStyle = particle.color
          ctx.beginPath()
          ctx.arc(newX, newY, particle.size, 0, Math.PI * 2)
          ctx.fill()
          ctx.restore()
          
          return {
            ...particle,
            x: newX,
            y: newY,
            life: particle.life - 1,
            opacity: particle.life > 100 ? particle.opacity : particle.opacity * 0.98
          }
        }).filter(particle => particle.life > 0)
      )
      
      requestAnimationFrame(animate)
    }
    
    animate()
    
    const handleResize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [mousePosition])

  // Mouse tracking for interactive effects
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY })
    }
    
    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [])
  // Search functionality with enhanced results
  const handleSearch = async () => {
    if (!searchQuery.trim()) return
    
    setIsSearching(true)
    setShowResults(false)
    
    // Simulate AI processing
    await new Promise(resolve => setTimeout(resolve, 2500))
    
    const selectedCapability = searchCapabilities.find(cap => cap.id === searchType) || searchCapabilities[0]
    
    // Generate realistic preview results
    const mockResults = {
      query: searchQuery,
      type: selectedCapability.name,
      confidence: selectedCapability.confidence,
      sources: selectedCapability.sources,
      preview: {
        location: "San Francisco, CA, USA",
        carrier: searchType === 'phone' ? "Advanced Networks Inc." : undefined,
        lineType: searchType === 'phone' ? "Quantum Interface Mobile" : undefined,
        socialProfiles: Math.floor(Math.random() * 20) + 5,
        associatedEmails: Math.floor(Math.random() * 10) + 3,
        riskLevel: "Low",
        lastSeen: "2 hours ago",
        verification: "Verified Account"
      },
      pricing: selectedCapability.category === 'quantum' ? "$19.99" : "$9.99"
    }
    
    setSearchResults(mockResults)
    setIsSearching(false)
    setShowResults(true)
  }

  const getCurrentCapability = () => {
    return searchCapabilities.find(cap => cap.id === searchType) || searchCapabilities[0]
  }
  return (
    <>
      <Head>
        <title>IntelliSearch Pro - Ultimate Intelligence Platform</title>
        <meta name="description" content="Professional-grade intelligence gathering platform with quantum processing capabilities" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white overflow-hidden relative">
        {/* Quantum Particle Background Canvas */}
        <canvas
          ref={canvasRef}
          className="absolute inset-0 z-0"
          style={{ background: 'transparent' }}
        />

        {/* Main Content */}
        <div className="relative z-10">
          {/* Enhanced Header with Live Metrics */}
          <header className="border-b border-white/10 backdrop-blur-sm bg-black/20">
            <div className="max-w-7xl mx-auto px-6 py-4">
              <div className="flex items-center justify-between">
                {/* Logo with Quantum Effects */}
                <motion.div 
                  className="flex items-center space-x-3"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.8 }}
                >
                  <div className="relative">
                    <motion.div
                      className="w-10 h-10 bg-gradient-to-br from-blue-400 via-purple-500 to-cyan-400 rounded-xl flex items-center justify-center"
                      animate={{ rotate: 360 }}
                      transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                    >
                      <Atom className="w-6 h-6 text-white" />
                      <motion.div
                        className="absolute inset-0 bg-gradient-to-br from-blue-400 via-purple-500 to-cyan-400 rounded-xl opacity-30"
                        animate={{ scale: [1, 1.2, 1] }}
                        transition={{ duration: 2, repeat: Infinity }}
                      />
                    </motion.div>
                  </div>
                  <div>
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                      IntelliSearch Pro
                    </h1>
                    <p className="text-xs text-slate-400">Ultimate Intelligence Platform</p>
                  </div>
                </motion.div>

                {/* Live Quantum Metrics */}
                <div className="flex items-center space-x-6">
                  <div className="flex items-center space-x-4 text-sm">
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                      <span className="text-slate-300">{metrics.activeUsers.toLocaleString()}+ users online</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Activity className="w-4 h-4 text-blue-400" />
                      <span className="text-slate-300">{metrics.searchesToday.toLocaleString()}+ searches today</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Brain className="w-4 h-4 text-purple-400" />
                      <span className="text-slate-300">{metrics.aiAccuracy.toFixed(1)}% AI accuracy</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Database className="w-4 h-4 text-cyan-400" />
                      <span className="text-slate-300">{(metrics.dataPoints / 1000000000).toFixed(1)}B+ records</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </header>

          {/* Hero Section with Quantum Search */}
          <section className="pt-20 pb-16 px-6">
            <div className="max-w-4xl mx-auto text-center">
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 1 }}
              >
                <h2 className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                  Find Anyone, Anywhere
                </h2>
                <p className="text-xl text-slate-300 mb-12 leading-relaxed">
                  Advanced quantum intelligence search engine with access to {(metrics.dataPoints / 1000000000).toFixed(1)}B+ records. 
                  Get instant results for phone numbers, emails, usernames, and more.
                </p>
              </motion.div>

              {/* Ultimate Search Interface */}
              <motion.div
                className="bg-black/30 backdrop-blur-xl rounded-2xl p-8 border border-white/10"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.3, duration: 0.8 }}
              >
                {/* Search Type Selector */}
                <div className="grid grid-cols-6 gap-2 mb-6">
                  {searchCapabilities.slice(0, 6).map((capability) => (
                    <motion.button
                      key={capability.id}
                      onClick={() => setSearchType(capability.id)}
                      className={`p-3 rounded-xl border transition-all ${
                        searchType === capability.id
                          ? 'bg-blue-500/20 border-blue-400 text-blue-300'
                          : 'bg-white/5 border-white/10 text-slate-400 hover:bg-white/10'
                      }`}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <div className="flex flex-col items-center space-y-2">
                        {capability.icon}
                        <span className="text-xs">{capability.name.split(' ')[0]}</span>
                      </div>
                    </motion.button>
                  ))}
                </div>

                {/* Quantum Search Type Selector */}
                <div className="mb-4">
                  <p className="text-sm text-slate-400 mb-2">Quantum Intelligence Capabilities:</p>
                  <div className="grid grid-cols-6 gap-2">
                    {searchCapabilities.slice(6, 12).map((capability) => (
                      <motion.button
                        key={capability.id}
                        onClick={() => setSearchType(capability.id)}
                        className={`p-2 rounded-lg border transition-all ${
                          searchType === capability.id
                            ? 'bg-purple-500/20 border-purple-400 text-purple-300'
                            : 'bg-white/5 border-white/10 text-slate-400 hover:bg-white/10'
                        }`}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        <div className="flex flex-col items-center space-y-1">
                          {capability.icon}
                          <span className="text-xs">{capability.name.split(' ')[0]}</span>
                        </div>
                      </motion.button>
                    ))}
                  </div>
                </div>

                {/* Search Input */}
                <div className="flex space-x-4">
                  <div className="flex-1 relative">
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      placeholder={getCurrentCapability().description}
                      className="w-full px-6 py-4 bg-white/10 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20 transition-all"
                      onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                    />
                    <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
                      <Search className="w-5 h-5 text-slate-400" />
                    </div>
                  </div>
                  <motion.button
                    onClick={handleSearch}
                    disabled={!searchQuery.trim() || isSearching}
                    className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:from-blue-600 hover:to-purple-700 transition-all"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    {isSearching ? (
                      <div className="flex items-center space-x-2">
                        <motion.div
                          className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                          animate={{ rotate: 360 }}
                          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        />
                        <span>Analyzing...</span>
                      </div>
                    ) : (
                      <span>Launch Intelligence</span>
                    )}
                  </motion.button>
                </div>

                {/* Current Capability Info */}
                <div className="mt-4 flex items-center justify-between text-sm text-slate-400">
                  <div className="flex items-center space-x-4">
                    <span>Confidence: {getCurrentCapability().confidence}%</span>
                    <span>Sources: {getCurrentCapability().sources}</span>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      getCurrentCapability().category === 'quantum' 
                        ? 'bg-purple-500/20 text-purple-300' 
                        : 'bg-blue-500/20 text-blue-300'
                    }`}>
                      {getCurrentCapability().category === 'quantum' ? 'Quantum' : 'Standard'}
                    </span>
                  </div>
                </div>
              </motion.div>

              {/* Professional Trust Indicators */}
              <motion.div
                className="flex items-center justify-center space-x-8 mt-8 text-sm text-slate-400"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.8, duration: 0.8 }}
              >
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  <span>Instant Access</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Shield className="w-4 h-4 text-blue-400" />
                  <span>Quantum Security</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Award className="w-4 h-4 text-purple-400" />
                  <span>Professional Intelligence</span>
                </div>
              </motion.div>
            </div>
          </section>

          {/* Search Results */}
          <AnimatePresence>
            {showResults && searchResults && (
              <motion.section
                className="px-6 pb-16"
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -50 }}
                transition={{ duration: 0.8 }}
              >
                <div className="max-w-2xl mx-auto">
                  <motion.div
                    className="bg-black/40 backdrop-blur-xl rounded-2xl p-8 border border-white/10"
                    initial={{ scale: 0.95 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.2, duration: 0.5 }}
                  >
                    <div className="flex items-center justify-between mb-6">
                      <h3 className="text-2xl font-bold text-white">Intelligence Results</h3>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                        <span className="text-sm text-green-400">Live Data</span>
                      </div>
                    </div>

                    {/* Results Preview */}
                    <div className="space-y-4 mb-6">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="bg-white/5 rounded-lg p-4">
                          <div className="text-sm text-slate-400 mb-1">Confidence</div>
                          <div className="text-xl font-bold text-green-400">{searchResults.confidence}%</div>
                        </div>
                        <div className="bg-white/5 rounded-lg p-4">
                          <div className="text-sm text-slate-400 mb-1">Sources</div>
                          <div className="text-xl font-bold text-blue-400">{searchResults.sources}</div>
                        </div>
                      </div>

                      {/* Blurred Preview Data */}
                      <div className="bg-white/5 rounded-lg p-6 relative">
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent backdrop-blur-sm rounded-lg flex items-center justify-center">
                          <div className="bg-black/50 rounded-lg px-6 py-3">
                            <p className="text-sm text-slate-300 mb-2">Preview Results ★ Premium Required</p>
                            <div className="space-y-2 text-sm">
                              <div>Location: {searchResults.preview.location}</div>
                              {searchResults.preview.carrier && <div>Carrier: {searchResults.preview.carrier}</div>}
                              <div>Social Profiles: {searchResults.preview.socialProfiles}</div>
                              <div>Associated Emails: {searchResults.preview.associatedEmails}</div>
                              <div>Risk Level: {searchResults.preview.riskLevel}</div>
                            </div>
                          </div>
                        </div>
                        <div className="opacity-20 space-y-3">
                          <div className="h-4 bg-slate-400 rounded w-3/4"></div>
                          <div className="h-4 bg-slate-400 rounded w-1/2"></div>
                          <div className="h-4 bg-slate-400 rounded w-2/3"></div>
                          <div className="h-4 bg-slate-400 rounded w-3/5"></div>
                          <div className="h-4 bg-slate-400 rounded w-4/5"></div>
                        </div>
                      </div>
                    </div>

                    {/* Commercial CTA */}
                    <motion.button
                      className="w-full py-4 bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl font-bold text-lg hover:from-green-600 hover:to-emerald-700 transition-all"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      Get Full Report - {searchResults.pricing}
                    </motion.button>
                  </motion.div>
                </div>
              </motion.section>
            )}
          </AnimatePresence>

          {/* Enhanced Quantum Metrics Dashboard */}
          <section className="px-6 pb-16">
            <div className="max-w-6xl mx-auto">
              <motion.div
                className="bg-black/20 backdrop-blur-xl rounded-2xl p-8 border border-white/10"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1, duration: 0.8 }}
              >
                <h3 className="text-2xl font-bold mb-6 text-center bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  Live Quantum Intelligence Metrics
                </h3>
                
                <div className="grid grid-cols-4 md:grid-cols-8 gap-4">
                  <div className="text-center p-4 bg-blue-500/10 rounded-xl border border-blue-500/30">
                    <div className="text-lg font-bold text-blue-400">{metrics.quantumProcessors.toLocaleString()}</div>
                    <div className="text-xs text-slate-400">Quantum CPUs</div>
                  </div>
                  <div className="text-center p-4 bg-purple-500/10 rounded-xl border border-purple-500/30">
                    <div className="text-lg font-bold text-purple-400">{metrics.parallelRealities.toLocaleString()}</div>
                    <div className="text-xs text-slate-400">Parallel Realities</div>
                  </div>
                  <div className="text-center p-4 bg-green-500/10 rounded-xl border border-green-500/30">
                    <div className="text-lg font-bold text-green-400">{(metrics.neuralSynapses / 1000000).toFixed(1)}M</div>
                    <div className="text-xs text-slate-400">Neural Synapses</div>
                  </div>
                  <div className="text-center p-4 bg-cyan-500/10 rounded-xl border border-cyan-500/30">
                    <div className="text-lg font-bold text-cyan-400">{metrics.dimensionalGateways}</div>
                    <div className="text-xs text-slate-400">Gateways</div>
                  </div>
                  <div className="text-center p-4 bg-pink-500/10 rounded-xl border border-pink-500/30">
                    <div className="text-lg font-bold text-pink-400">{metrics.consciousnessStreams.toLocaleString()}</div>
                    <div className="text-xs text-slate-400">Consciousness</div>
                  </div>
                  <div className="text-center p-4 bg-orange-500/10 rounded-xl border border-orange-500/30">
                    <div className="text-lg font-bold text-orange-400">{metrics.quantumEntanglements.toLocaleString()}</div>
                    <div className="text-xs text-slate-400">Entanglements</div>
                  </div>
                  <div className="text-center p-4 bg-indigo-500/10 rounded-xl border border-indigo-500/30">
                    <div className="text-lg font-bold text-indigo-400">{metrics.timelineAnalyses.toLocaleString()}</div>
                    <div className="text-xs text-slate-400">Timelines</div>
                  </div>
                  <div className="text-center p-4 bg-teal-500/10 rounded-xl border border-teal-500/30">
                    <div className="text-lg font-bold text-teal-400">{metrics.multiverseConnections}</div>
                    <div className="text-xs text-slate-400">Multiverse</div>
                  </div>
                </div>
              </motion.div>
            </div>
          </section>

          {/* Footer */}
          <footer className="border-t border-white/10 py-8 px-6">
            <div className="max-w-7xl mx-auto text-center">
              <p className="text-slate-400">
                © 2024 IntelliSearch Pro. Professional intelligence platform with quantum processing capabilities.
              </p>
            </div>
          </footer>
        </div>
      </div>
    </>
  )
}
        <canvas
          ref={canvasRef}
          className="absolute inset-0 pointer-events-none"
          style={{ mixBlendMode: 'screen' }}
        />

        {/* Professional Header */}
        <header className="relative z-10 border-b border-slate-800/50 backdrop-blur-sm bg-slate-900/20">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <motion.div 
                className="flex items-center space-x-3"
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
              >
                <div className="relative">
                  <motion.div
                    className="w-10 h-10 bg-gradient-to-br from-blue-500 via-purple-500 to-cyan-500 rounded-xl flex items-center justify-center"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                  >
                    <Radar className="w-6 h-6 text-white" />
                  </motion.div>
                  <motion.div
                    className="absolute -inset-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl opacity-20 blur"
                    animate={{ scale: [1, 1.1, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                </div>
                <div>
                  <h1 className="text-xl font-bold">IntelliSearch Pro</h1>
                  <p className="text-xs text-slate-400">Advanced Intelligence Platform</p>
                </div>
              </motion.div>

              {/* Live Metrics Bar */}
              <motion.div 
                className="hidden lg:flex items-center space-x-8"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
              >
                <div className="flex items-center space-x-2 text-sm">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                  <span className="text-slate-300">{metrics.activeUsers.toLocaleString()} users online</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <Activity className="w-4 h-4 text-blue-400" />
                  <span className="text-slate-300">{metrics.searchesToday.toLocaleString()} searches today</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <Brain className="w-4 h-4 text-purple-400" />
                  <span className="text-slate-300">{metrics.aiAccuracy.toFixed(1)}% AI accuracy</span>
                </div>
              </motion.div>

              {/* Professional Navigation */}
              <div className="flex items-center space-x-4">
                <button className="p-2 hover:bg-slate-800/50 rounded-lg transition-colors">
                  <Bell className="w-5 h-5" />
                </button>
                <button className="p-2 hover:bg-slate-800/50 rounded-lg transition-colors">
                  <Settings className="w-5 h-5" />
                </button>
                <button className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded-lg transition-colors">
                  <User className="w-4 h-4" />
                  <span className="text-sm font-medium">Sign In</span>
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <main className="relative z-10">
          <div className="max-w-7xl mx-auto px-6 pt-20 pb-32">
            <div className="text-center max-w-4xl mx-auto">
              <motion.div
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 1 }}
              >
                <h1 className="text-5xl lg:text-7xl font-bold mb-6">
                  <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                    Find Anyone,
                  </span>
                  <br />
                  <span className="text-white">Anywhere</span>
                </h1>
                <p className="text-xl text-slate-300 mb-12 leading-relaxed">
                  Advanced intelligence search engine with access to billions of records.
                  Get instant results for phone numbers, emails, usernames, and more.
                </p>
              </motion.div>

              {/* Advanced Search Interface */}
              <motion.div
                className="bg-slate-800/30 backdrop-blur-lg border border-slate-700/50 rounded-2xl p-8 mb-16"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.3 }}
              >
                {/* Search Type Selector */}
                <div className="flex flex-wrap justify-center gap-2 mb-6">
                  {searchCapabilities.map((capability) => (
                    <button
                      key={capability.id}
                      onClick={() => setSearchType(capability.id)}
                      className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        searchType === capability.id
                          ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/25'
                          : 'bg-slate-700/50 text-slate-300 hover:bg-slate-700'
                      }`}
                    >
                      {capability.icon}
                      <span>{capability.name}</span>
                    </button>
                  ))}
                </div>

                {/* Search Input */}
                <div className="relative mb-6">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <Search className="h-5 w-5 text-slate-400" />
                  </div>
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                    placeholder="Enter phone number, email, username, or any identifier..."
                    className="w-full pl-12 pr-4 py-4 bg-slate-900/50 border border-slate-600 rounded-xl text-white text-lg placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
                  />
                </div>

                <button
                  onClick={handleSearch}
                  disabled={isSearching || !searchQuery.trim()}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:from-slate-600 disabled:to-slate-700 text-white font-semibold py-4 px-8 rounded-xl transition-all duration-300 flex items-center justify-center space-x-3"
                >
                  {isSearching ? (
                    <>
                      <motion.div
                        className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      />
                      <span>Analyzing Intelligence...</span>
                    </>
                  ) : (
                    <>
                      <Zap className="w-5 h-5" />
                      <span>Launch Intelligence Search</span>
                    </>
                  )}
                </button>
              </motion.div>

              {/* Search Results */}
              <AnimatePresence>
                {showResults && searchResults && (
                  <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -50 }}
                    className="bg-slate-800/30 backdrop-blur-lg border border-slate-700/50 rounded-2xl p-8 mb-16"
                  >
                    <div className="flex items-center justify-between mb-6">
                      <h3 className="text-2xl font-bold text-white">Results Found!</h3>
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="w-5 h-5 text-green-400" />
                        <span className="text-green-400 font-medium">{searchResults.confidence}% Confidence</span>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                      <div className="space-y-3">
                        <div className="flex justify-between">
                          <span className="text-slate-400">Location:</span>
                          <span className="text-white font-medium blur-sm">{searchResults.location}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Carrier:</span>
                          <span className="text-white font-medium blur-sm">{searchResults.carrier}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Line Type:</span>
                          <span className="text-white font-medium blur-sm">{searchResults.lineType}</span>
                        </div>
                      </div>
                      <div className="space-y-3">
                        <div className="flex justify-between">
                          <span className="text-slate-400">Social Profiles:</span>
                          <span className="text-white font-medium blur-sm">{searchResults.profiles}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Associated Emails:</span>
                          <span className="text-white font-medium blur-sm">{searchResults.emails}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Risk Level:</span>
                          <span className="text-green-400 font-medium">{searchResults.riskLevel}</span>
                        </div>
                      </div>
                    </div>

                    <div className="border-t border-slate-700 pt-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          <Shield className="w-5 h-5 text-blue-400" />
                          <span className="text-slate-300">Instant Access</span>
                          <Lock className="w-5 h-5 text-green-400" />
                          <span className="text-slate-300">Secure & Verified</span>
                          <Eye className="w-5 h-5 text-purple-400" />
                          <span className="text-slate-300">Professional Intelligence</span>
                        </div>
                        <button className="bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-500 hover:to-blue-500 text-white font-semibold py-3 px-6 rounded-lg transition-all flex items-center space-x-2">
                          <Download className="w-4 h-4" />
                          <span>Get Full Report - $9.99</span>
                        </button>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>

          {/* Enterprise Features Section */}
          <div className="bg-slate-800/20 backdrop-blur-sm border-t border-slate-700/50">
            <div className="max-w-7xl mx-auto px-6 py-20">
              <div className="text-center mb-16">
                <h2 className="text-4xl font-bold text-white mb-4">
                  Advanced Intelligence Capabilities
                </h2>
                <p className="text-xl text-slate-300 max-w-3xl mx-auto">
                  Comprehensive search tools powered by AI and billions of data points
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {searchCapabilities.map((capability, index) => (
                  <motion.div
                    key={capability.id}
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.1 }}
                    className="bg-slate-800/30 backdrop-blur-lg border border-slate-700/50 rounded-xl p-6 hover:bg-slate-800/50 transition-all group"
                  >
                    <div className="flex items-center space-x-3 mb-4">
                      <div className="p-2 bg-blue-600/20 rounded-lg group-hover:bg-blue-600/30 transition-colors">
                        {capability.icon}
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-white">{capability.name}</h3>
                        <p className="text-sm text-blue-400">{capability.confidence}% accuracy</p>
                      </div>
                    </div>
                    <p className="text-slate-300 mb-4">{capability.description}</p>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-400">{capability.sources} sources</span>
                      <ArrowRight className="w-4 h-4 text-blue-400 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* Platform Statistics */}
          <div className="max-w-7xl mx-auto px-6 py-20">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">
                Trusted by Millions Worldwide
              </h2>
              <p className="text-xl text-slate-300">
                Professional-grade intelligence platform used by investigators, businesses, and individuals
              </p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
              <motion.div
                className="text-center"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6 }}
              >
                <div className="text-3xl font-bold text-blue-400 mb-2">
                  {metrics.activeUsers.toLocaleString()}+
                </div>
                <div className="text-slate-400">Active Users</div>
              </motion.div>
              <motion.div
                className="text-center"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.1 }}
              >
                <div className="text-3xl font-bold text-green-400 mb-2">
                  {(metrics.dataPoints / 1000000).toFixed(1)}B+
                </div>
                <div className="text-slate-400">Records Indexed</div>
              </motion.div>
              <motion.div
                className="text-center"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <div className="text-3xl font-bold text-purple-400 mb-2">
                  {metrics.aiAccuracy.toFixed(1)}%
                </div>
                <div className="text-slate-400">AI Accuracy</div>
              </motion.div>
              <motion.div
                className="text-center"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.3 }}
              >
                <div className="text-3xl font-bold text-cyan-400 mb-2">24/7</div>
                <div className="text-slate-400">Expert Support</div>
              </motion.div>
              <motion.div
                className="text-center"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.4 }}
              >
                <div className="text-3xl font-bold text-yellow-400 mb-2">
                  {metrics.searchesToday.toLocaleString()}+
                </div>
                <div className="text-slate-400">Searches Today</div>
              </motion.div>
              <motion.div
                className="text-center"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.5 }}
              >
                <div className="text-3xl font-bold text-red-400 mb-2">
                  {metrics.threatsBlocked.toLocaleString()}+
                </div>
                <div className="text-slate-400">Threats Blocked</div>
              </motion.div>
            </div>
          </div>
        </main>

        {/* Professional Footer */}
        <footer className="relative z-10 border-t border-slate-800/50 bg-slate-900/50 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-6 py-12">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
              <div>
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                    <Radar className="w-5 h-5 text-white" />
                  </div>
                  <span className="text-xl font-bold text-white">IntelliSearch Pro</span>
                </div>
                <p className="text-slate-400 text-sm">
                  The world's most advanced intelligence search platform. Find anyone, anywhere, instantly.
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold text-white mb-4">Services</h4>
                <ul className="space-y-2 text-sm text-slate-400">
                  <li><a href="#" className="hover:text-white transition-colors">Phone Lookup</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Email Search</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">People Finder</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Username Tracking</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Image Search</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">IP Analysis</a></li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-semibold text-white mb-4">Company</h4>
                <ul className="space-y-2 text-sm text-slate-400">
                  <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Support</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">API Docs</a></li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-semibold text-white mb-4">Connect</h4>
                <div className="flex space-x-3">
                  <a href="#" className="w-8 h-8 bg-slate-800 hover:bg-slate-700 rounded-lg flex items-center justify-center transition-colors">
                    <LinkIcon className="w-4 h-4 text-slate-400" />
                  </a>
                  <a href="#" className="w-8 h-8 bg-slate-800 hover:bg-slate-700 rounded-lg flex items-center justify-center transition-colors">
                    <Mail className="w-4 h-4 text-slate-400" />
                  </a>
                  <a href="#" className="w-8 h-8 bg-slate-800 hover:bg-slate-700 rounded-lg flex items-center justify-center transition-colors">
                    <MessageSquare className="w-4 h-4 text-slate-400" />
                  </a>
                </div>
              </div>
            </div>
            
            <div className="border-t border-slate-800 pt-8 flex flex-col md:flex-row justify-between items-center">
              <p className="text-slate-400 text-sm">
                © 2024 IntelliSearch Pro. All rights reserved. Professional intelligence platform.
              </p>
              <div className="flex items-center space-x-4 mt-4 md:mt-0">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                  <span className="text-slate-400 text-sm">All systems operational</span>
                </div>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}