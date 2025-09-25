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
  Award, Layers, Cpu, Cloud, GitBranch, Workflow, Zap as ZapIcon,
  MousePointer, Sparkles, Infinity, CircuitBoard, Satellite,
  Server, Terminal, GitMerge, Hexagon, PenTool, Command,
  Lightbulb, MessageSquare, TrendingDown, Monitor, Code,
  Gauge, Mic, Video, Headphones, BookOpen, Hash, AtSign,
  Bot, Package, Briefcase, Building, Orbit, Waves, Flame,
  Crown, Gem, Diamond, Palette, Layers3, Box, Component
} from 'lucide-react'

// Enhanced Intelligence Platform with Advanced Features
export default function EnhancedIntelligencePlatform() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchType, setSearchType] = useState('advanced-phone')
  const [isProcessing, setIsProcessing] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const [currentTime, setCurrentTime] = useState(new Date())
  const [activeTab, setActiveTab] = useState('intelligence')
  const canvasRef = useRef<HTMLCanvasElement>(null)

  // Enhanced live metrics with real-time updates
  const [advancedMetrics, setAdvancedMetrics] = useState({
    totalUsers: 15847,
    aiAccuracy: 99.8,
    dailyScans: 156789,
    successRate: 98.9,
    quantumCores: 847,
    neuralNetworks: 2847,
    activeInvestigators: 1247,
    threatLevel: 1.8,
    databaseSize: 47.2, // TB
    processingSpeed: 0.23, // seconds
    globalCoverage: 194, // countries
    realTimeAlerts: 8934
  })

  // Advanced intelligence capabilities
  const advancedCapabilities = [
    {
      icon: <Brain className="w-10 h-10" />,
      title: "Advanced AI Phone Intelligence",
      description: "Multi-dimensional phone analysis with carrier detection, location triangulation, social media correlation, and behavioral pattern recognition",
      confidence: 99.8,
      sources: 347,
      features: ["Carrier Intelligence", "Location Mapping", "Social Correlation", "Pattern Analysis"],
      color: "from-cyan-500 to-blue-600"
    },
    {
      icon: <Mail className="w-10 h-10" />,
      title: "Professional Email Investigation",
      description: "Deep email analysis with breach detection, domain investigation, SMTP tracking, and comprehensive social media linking",
      confidence: 99.2,
      sources: 289,
      features: ["Breach Detection", "Domain Analysis", "SMTP Tracking", "Social Linking"],
      color: "from-purple-500 to-pink-600"
    },
    {
      icon: <Users className="w-10 h-10" />,
      title: "Comprehensive People Search",
      description: "Advanced people intelligence with background checks, address history, relatives mapping, and social network analysis",
      confidence: 98.7,
      sources: 456,
      features: ["Background Checks", "Address History", "Relatives Map", "Social Analysis"],
      color: "from-green-500 to-emerald-600"
    },
    {
      icon: <User className="w-10 h-10" />,
      title: "Advanced Username Tracking",
      description: "Cross-platform username correlation with dating sites, forums, social media, and deep web presence detection",
      confidence: 97.9,
      sources: 234,
      features: ["Dating Sites", "Forum Analysis", "Deep Web Scan", "Platform Correlation"],
      color: "from-red-500 to-orange-600"
    },
    {
      icon: <Image className="w-10 h-10" />,
      title: "AI-Powered Image Analysis",
      description: "Advanced reverse image search with facial recognition, metadata extraction, location detection, and similarity matching",
      confidence: 96.8,
      sources: 189,
      features: ["Facial Recognition", "Metadata Analysis", "Location Detection", "Similarity Match"],
      color: "from-yellow-500 to-amber-600"
    },
    {
      icon: <Network className="w-10 h-10" />,
      title: "Professional IP Intelligence",
      description: "Comprehensive IP analysis with geolocation, ISP detection, threat assessment, and network topology mapping",
      confidence: 98.1,
      sources: 167,
      features: ["Geolocation", "ISP Detection", "Threat Assessment", "Network Mapping"],
      color: "from-indigo-500 to-violet-600"
    },
    {
      icon: <Globe className="w-10 h-10" />,
      title: "Advanced Domain Investigation",
      description: "Complete domain analysis with WHOIS data, DNS records, SSL certificates, and historical information tracking",
      confidence: 97.6,
      sources: 245,
      features: ["WHOIS Analysis", "DNS Records", "SSL Tracking", "Historical Data"],
      color: "from-teal-500 to-cyan-600"
    },
    {
      icon: <Shield className="w-10 h-10" />,
      title: "Comprehensive Security Audit",
      description: "Advanced security assessment with vulnerability scanning, breach detection, threat analysis, and risk evaluation",
      confidence: 98.4,
      sources: 178,
      features: ["Vulnerability Scan", "Breach Detection", "Threat Analysis", "Risk Assessment"],
      color: "from-rose-500 to-red-600"
    },
    {
      icon: <Database className="w-10 h-10" />,
      title: "Professional Data Mining",
      description: "Deep data correlation with public records, business databases, court records, and financial information analysis",
      confidence: 97.3,
      sources: 356,
      features: ["Public Records", "Business Data", "Court Records", "Financial Analysis"],
      color: "from-blue-500 to-indigo-600"
    },
    {
      icon: <Activity className="w-10 h-10" />,
      title: "Real-Time Monitoring",
      description: "Continuous monitoring with alert systems, change detection, social media tracking, and automated reporting",
      confidence: 98.9,
      sources: 289,
      features: ["Alert Systems", "Change Detection", "Social Tracking", "Auto Reports"],
      color: "from-orange-500 to-yellow-600"
    },
    {
      icon: <Lock className="w-10 h-10" />,
      title: "Advanced Threat Detection",
      description: "Sophisticated threat analysis with dark web monitoring, fraud detection, identity theft alerts, and risk scoring",
      confidence: 99.1,
      sources: 234,
      features: ["Dark Web Monitor", "Fraud Detection", "Identity Alerts", "Risk Scoring"],
      color: "from-emerald-500 to-green-600"
    },
    {
      icon: <Cpu className="w-10 h-10" />,
      title: "AI-Powered Analytics",
      description: "Machine learning analytics with pattern recognition, predictive modeling, behavioral analysis, and intelligence synthesis",
      confidence: 98.6,
      sources: 412,
      features: ["Pattern Recognition", "Predictive Models", "Behavioral Analysis", "AI Synthesis"],
      color: "from-purple-500 to-blue-600"
    }
  ]

  // Enhanced particle system for background
  useEffect(() => {
    if (!canvasRef.current) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }

    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    const particles: any[] = []
    const particleCount = 100

    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: Math.random() * 2 + 1,
        color: ['#00f5ff', '#ff0080', '#8000ff', '#00ff80'][Math.floor(Math.random() * 4)],
        opacity: Math.random() * 0.6 + 0.2
      })
    }

    let animationId: number
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      particles.forEach(particle => {
        particle.x += particle.vx
        particle.y += particle.vy

        if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1
        if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1

        ctx.save()
        ctx.globalAlpha = particle.opacity
        ctx.fillStyle = particle.color
        ctx.shadowColor = particle.color
        ctx.shadowBlur = 5
        ctx.beginPath()
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2)
        ctx.fill()
        ctx.restore()
      })

      animationId = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      window.removeEventListener('resize', resizeCanvas)
      cancelAnimationFrame(animationId)
    }
  }, [])

  // Real-time metrics updates
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date())
      setAdvancedMetrics(prev => ({
        ...prev,
        totalUsers: prev.totalUsers + Math.floor(Math.random() * 5),
        dailyScans: prev.dailyScans + Math.floor(Math.random() * 20),
        activeInvestigators: prev.activeInvestigators + Math.floor(Math.random() * 3) - 1,
        realTimeAlerts: prev.realTimeAlerts + Math.floor(Math.random() * 10)
      }))
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  const handleAdvancedSearch = async () => {
    if (!searchQuery.trim()) return

    setIsProcessing(true)
    setShowResults(false)

    // Simulate advanced processing
    await new Promise(resolve => setTimeout(resolve, 3000))

    setIsProcessing(false)
    setShowResults(true)
  }

  const mockAdvancedResults = [
    { category: "Advanced Location", data: "San Francisco, CA, USA (Precision: ±50m)", confidence: 99.8, threat: 'low', sources: 47 },
    { category: "Carrier Intelligence", data: "Verizon Wireless (Advanced Network Analysis)", confidence: 99.2, threat: 'low', sources: 23 },
    { category: "Social Correlation", data: "15 social profiles linked with 94% confidence", confidence: 94.7, threat: 'medium', sources: 67 },
    { category: "Digital Footprint", data: "847 data points across 23 platforms", confidence: 96.8, threat: 'low', sources: 89 },
    { category: "Risk Assessment", data: "Low risk profile with 2.1/10 threat score", confidence: 98.1, threat: 'low', sources: 34 },
    { category: "Behavioral Analysis", data: "Standard user patterns detected", confidence: 87.4, threat: 'low', sources: 56 },
    { category: "Network Analysis", data: "Clean IP reputation, no malicious activity", confidence: 99.5, threat: 'low', sources: 12 },
    { category: "Timeline Analysis", data: "Account creation: 2019, last activity: 24h ago", confidence: 95.6, threat: 'low', sources: 28 }
  ]

  return (
    <>
      <Head>
        <title>Enhanced Intelligence Platform - Professional Grade</title>
        <meta name="description" content="Advanced intelligence gathering platform with 12 professional capabilities" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-black text-white overflow-hidden relative">
        {/* Enhanced Background */}
        <canvas
          ref={canvasRef}
          className="fixed inset-0 pointer-events-none opacity-30"
          style={{ zIndex: 0 }}
        />

        {/* Professional Navigation */}
        <nav className="relative z-50 flex items-center justify-between p-6 bg-black/40 backdrop-blur-xl border-b border-cyan-500/20">
          <div className="flex items-center space-x-4">
            <motion.div
              className="relative w-12 h-12"
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            >
              <div className="w-full h-full rounded-full bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 flex items-center justify-center">
                <Brain className="w-6 h-6 text-white" />
              </div>
            </motion.div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                IntelliSearch Pro
              </h1>
              <p className="text-xs text-gray-400">Enhanced Intelligence Platform</p>
            </div>
          </div>

          {/* Advanced Status Bar */}
          <div className="flex items-center space-x-6 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
              <span className="text-green-400">Online</span>
            </div>
            <div className="text-cyan-400">Users: {advancedMetrics.totalUsers.toLocaleString()}</div>
            <div className="text-purple-400">AI: {advancedMetrics.aiAccuracy}%</div>
            <div className="text-pink-400">Cores: {advancedMetrics.quantumCores}</div>
            <div className="text-yellow-400">{currentTime.toLocaleTimeString()}</div>
          </div>
        </nav>

        {/* Enhanced Metrics Dashboard */}
        <div className="relative z-40 px-6 py-4">
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {[
              { label: "Daily Scans", value: advancedMetrics.dailyScans, color: "cyan", icon: <Search className="w-4 h-4" /> },
              { label: "Success Rate", value: `${advancedMetrics.successRate}%`, color: "green", icon: <CheckCircle className="w-4 h-4" /> },
              { label: "Active Users", value: advancedMetrics.activeInvestigators, color: "purple", icon: <Users className="w-4 h-4" /> },
              { label: "Neural Networks", value: advancedMetrics.neuralNetworks, color: "pink", icon: <Brain className="w-4 h-4" /> },
              { label: "Database Size", value: `${advancedMetrics.databaseSize}TB`, color: "yellow", icon: <Database className="w-4 h-4" /> },
              { label: "Response Time", value: `${advancedMetrics.processingSpeed}s`, color: "blue", icon: <Zap className="w-4 h-4" /> }
            ].map((metric, index) => (
              <motion.div
                key={metric.label}
                className={`bg-black/60 backdrop-blur-xl rounded-xl p-4 border border-${metric.color}-500/30 hover:border-${metric.color}-400/60 transition-all duration-300`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.05, y: -2 }}
              >
                <div className="flex items-center space-x-2 mb-2">
                  <div className={`text-${metric.color}-400`}>{metric.icon}</div>
                  <div className={`text-xs text-${metric.color}-400`}>{metric.label}</div>
                </div>
                <div className={`text-xl font-bold text-${metric.color}-300`}>
                  {typeof metric.value === 'number' ? metric.value.toLocaleString() : metric.value}
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="relative z-30 px-6 pb-20">
          {/* Enhanced Hero Section */}
          <div className="max-w-6xl mx-auto text-center py-16">
            <motion.h1
              className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1 }}
            >
              Enhanced Intelligence
            </motion.h1>
            <motion.p
              className="text-xl md:text-2xl text-gray-300 mb-12 max-w-4xl mx-auto"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.2 }}
            >
              Professional-grade intelligence platform with 12 advanced capabilities. 
              Comprehensive analysis with unmatched accuracy and depth.
            </motion.p>

            {/* Enhanced Search Interface */}
            <motion.div
              className="max-w-3xl mx-auto mb-16"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.4 }}
            >
              <div className="relative">
                <div className="flex mb-4 space-x-2 justify-center">
                  {['Phone', 'Email', 'Username', 'IP'].map((type) => (
                    <button
                      key={type}
                      className={`px-4 py-2 rounded-lg text-sm transition-all duration-300 ${
                        searchType === `advanced-${type.toLowerCase()}` 
                          ? 'bg-cyan-500 text-white' 
                          : 'bg-black/40 text-gray-400 hover:text-white hover:bg-black/60'
                      }`}
                      onClick={() => setSearchType(`advanced-${type.toLowerCase()}`)}
                    >
                      {type}
                    </button>
                  ))}
                </div>
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Enter phone, email, username, or IP address for advanced analysis..."
                  className="w-full px-6 py-4 bg-black/40 backdrop-blur-xl border-2 border-cyan-500/30 rounded-2xl text-lg text-white placeholder-gray-400 focus:border-cyan-400 focus:outline-none transition-all duration-300"
                  onKeyPress={(e) => e.key === 'Enter' && handleAdvancedSearch()}
                />
                <motion.button
                  onClick={handleAdvancedSearch}
                  className="absolute right-2 top-16 px-8 py-2 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-xl font-semibold hover:from-cyan-400 hover:to-purple-500 transition-all duration-300 flex items-center space-x-2"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  disabled={isProcessing}
                >
                  {isProcessing ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                      <span>Processing...</span>
                    </>
                  ) : (
                    <>
                      <Search className="w-4 h-4" />
                      <span>Advanced Analysis</span>
                    </>
                  )}
                </motion.button>
              </div>
            </motion.div>
          </div>

          {/* 12 Advanced Intelligence Capabilities */}
          <div className="max-w-7xl mx-auto mb-20">
            <h2 className="text-4xl font-bold text-center mb-16 bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              12 Professional Intelligence Capabilities
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {advancedCapabilities.map((capability, index) => (
                <motion.div
                  key={capability.title}
                  className={`group bg-gradient-to-br ${capability.color} p-0.5 rounded-2xl`}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.05, rotate: 1 }}
                >
                  <div className="bg-black/90 backdrop-blur-xl rounded-2xl p-6 h-full">
                    <div className="text-center mb-4">
                      <div className="mx-auto mb-3 text-cyan-400 group-hover:text-purple-400 transition-colors duration-300">
                        {capability.icon}
                      </div>
                      <div className="text-right text-xs mb-2">
                        <span className="text-green-400 font-semibold">{capability.confidence}%</span>
                        <span className="text-gray-400 ml-2">{capability.sources} sources</span>
                      </div>
                    </div>
                    <h3 className="text-lg font-bold mb-3 text-white group-hover:text-cyan-400 transition-colors duration-300">
                      {capability.title}
                    </h3>
                    <p className="text-sm text-gray-300 mb-4 line-clamp-3">
                      {capability.description}
                    </p>
                    <div className="space-y-1">
                      {capability.features.map((feature, idx) => (
                        <div key={idx} className="flex items-center text-xs text-gray-400">
                          <CheckCircle className="w-3 h-3 text-green-400 mr-2 flex-shrink-0" />
                          <span>{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Enhanced Results Display */}
          <AnimatePresence>
            {showResults && (
              <motion.div
                className="max-w-6xl mx-auto"
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -50 }}
                transition={{ duration: 0.8 }}
              >
                <div className="bg-black/60 backdrop-blur-xl rounded-3xl border border-cyan-500/30 p-8">
                  <div className="flex items-center justify-between mb-8">
                    <h3 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                      Enhanced Intelligence Report
                    </h3>
                    <motion.button
                      className="px-8 py-3 bg-gradient-to-r from-pink-500 to-red-600 rounded-xl font-semibold hover:from-pink-400 hover:to-red-500 transition-all duration-300 flex items-center space-x-2"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <Download className="w-5 h-5" />
                      <span>Get Full Professional Report - $19.99</span>
                    </motion.button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {mockAdvancedResults.map((result, index) => (
                      <motion.div
                        key={result.category}
                        className="relative bg-black/40 backdrop-blur-xl rounded-xl p-6 border border-gray-700/50 overflow-hidden"
                        initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <div className="flex items-center justify-between mb-4">
                          <h4 className="text-lg font-semibold text-cyan-400">{result.category}</h4>
                          <div className="flex items-center space-x-3">
                            <div className={`w-2 h-2 rounded-full ${
                              result.threat === 'low' ? 'bg-green-400' :
                              result.threat === 'medium' ? 'bg-yellow-400' : 'bg-red-400'
                            }`}></div>
                            <span className="text-sm text-gray-400">{result.confidence}%</span>
                            <span className="text-xs text-purple-400">{result.sources} sources</span>
                          </div>
                        </div>
                        <div className="text-white filter blur-sm select-none mb-4">
                          {result.data}
                        </div>
                        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent rounded-xl flex items-center justify-center">
                          <div className="text-center">
                            <Lock className="w-8 h-8 text-cyan-400 mx-auto mb-2" />
                            <div className="text-sm text-cyan-400 font-semibold">Professional Access Required</div>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>

                  <div className="mt-8 flex items-center justify-center space-x-8 text-sm text-gray-400">
                    <div className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-400" />
                      <span>Instant Access</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Shield className="w-4 h-4 text-blue-400" />
                      <span>Professional Grade</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Award className="w-4 h-4 text-purple-400" />
                      <span>Industry Leading</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Zap className="w-4 h-4 text-yellow-400" />
                      <span>Real-Time Results</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </>
  )
}