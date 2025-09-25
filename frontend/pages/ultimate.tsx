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
  Gauge, Mic, Video, Headphones, BookOpen, Hash, AtSign
} from 'lucide-react'

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

interface QuantumNode {
  id: number
  x: number
  y: number
  angle: number
  radius: number
  speed: number
  connections: number[]
}

interface IntelligenceResult {
  category: string
  data: string
  confidence: number
  threat: 'low' | 'medium' | 'high'
  sources: number
}

export default function UltimateIntelligencePlatform() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [particles, setParticles] = useState<Particle[]>([])
  const [quantumNodes, setQuantumNodes] = useState<QuantumNode[]>([])
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const [searchQuery, setSearchQuery] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const [currentTime, setCurrentTime] = useState(new Date())
  const [activeUsers] = useState(8247)
  const [totalScans] = useState(156789)
  const [aiAccuracy] = useState(99.4)
  const [threatLevel] = useState(2.1)
  const [quantumCores] = useState(24)
  const [parallelDimensions] = useState(15)
  const [neuralNetworks] = useState(847)

  // Advanced metrics that update in real-time
  const [liveMetrics, setLiveMetrics] = useState({
    quantumProcessors: 18947,
    parallelRealities: 12834,
    neuralSynapses: 2847639,
    dimensionalGateways: 247,
    consciousnessStreams: 8934,
    quantumEntanglements: 18475,
    timelineAnalyses: 5692,
    multiverseConnections: 834
  })

  // Initialize particles and quantum nodes
  useEffect(() => {
    const initParticles = Array.from({ length: 250 }, (_, i) => ({
      id: i,
      x: Math.random() * (typeof window !== 'undefined' ? window.innerWidth : 1200),
      y: Math.random() * (typeof window !== 'undefined' ? window.innerHeight : 800),
      vx: (Math.random() - 0.5) * 2,
      vy: (Math.random() - 0.5) * 2,
      size: Math.random() * 3 + 1,
      color: ['#00f5ff', '#ff0080', '#8000ff', '#00ff80', '#ff8000'][Math.floor(Math.random() * 5)],
      opacity: Math.random() * 0.8 + 0.2,
      life: Math.random() * 100 + 50
    }))

    const initNodes = Array.from({ length: 12 }, (_, i) => ({
      id: i,
      x: 0,
      y: 0,
      angle: (i / 12) * Math.PI * 2,
      radius: 150 + Math.random() * 100,
      speed: 0.01 + Math.random() * 0.02,
      connections: []
    }))

    setParticles(initParticles)
    setQuantumNodes(initNodes)
  }, [])

  // Advanced canvas animation system
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

    let animationId: number
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Draw quantum field background
      const gradient = ctx.createRadialGradient(
        canvas.width / 2, canvas.height / 2, 0,
        canvas.width / 2, canvas.height / 2, Math.max(canvas.width, canvas.height) / 2
      )
      gradient.addColorStop(0, 'rgba(0, 245, 255, 0.05)')
      gradient.addColorStop(0.5, 'rgba(128, 0, 255, 0.03)')
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0.1)')
      ctx.fillStyle = gradient
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Update and draw particles
      setParticles(prevParticles => 
        prevParticles.map(particle => {
          const dx = mousePosition.x - particle.x
          const dy = mousePosition.y - particle.y
          const distance = Math.sqrt(dx * dx + dy * dy)
          
          if (distance < 150) {
            particle.vx += dx * 0.00001
            particle.vy += dy * 0.00001
          }

          particle.x += particle.vx
          particle.y += particle.vy
          particle.life -= 0.1

          if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1
          if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1

          if (particle.life <= 0) {
            particle.x = Math.random() * canvas.width
            particle.y = Math.random() * canvas.height
            particle.life = Math.random() * 100 + 50
          }

          // Draw particle
          ctx.save()
          ctx.globalAlpha = particle.opacity
          ctx.fillStyle = particle.color
          ctx.shadowColor = particle.color
          ctx.shadowBlur = 10
          ctx.beginPath()
          ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2)
          ctx.fill()
          ctx.restore()

          return particle
        })
      )

      // Update and draw quantum nodes
      const centerX = canvas.width / 2
      const centerY = canvas.height / 2

      setQuantumNodes(prevNodes => 
        prevNodes.map(node => {
          node.angle += node.speed
          node.x = centerX + Math.cos(node.angle) * node.radius
          node.y = centerY + Math.sin(node.angle) * node.radius

          // Draw node
          ctx.save()
          ctx.fillStyle = '#00f5ff'
          ctx.shadowColor = '#00f5ff'
          ctx.shadowBlur = 20
          ctx.beginPath()
          ctx.arc(node.x, node.y, 8, 0, Math.PI * 2)
          ctx.fill()
          ctx.restore()

          return node
        })
      )

      // Draw connections between nodes
      ctx.strokeStyle = 'rgba(0, 245, 255, 0.3)'
      ctx.lineWidth = 1
      quantumNodes.forEach((node, i) => {
        quantumNodes.forEach((otherNode, j) => {
          if (i < j && Math.random() > 0.95) {
            ctx.beginPath()
            ctx.moveTo(node.x, node.y)
            ctx.lineTo(otherNode.x, otherNode.y)
            ctx.stroke()
          }
        })
      })

      // Draw mouse attraction field
      if (mousePosition.x > 0 && mousePosition.y > 0) {
        const fieldGradient = ctx.createRadialGradient(
          mousePosition.x, mousePosition.y, 0,
          mousePosition.x, mousePosition.y, 100
        )
        fieldGradient.addColorStop(0, 'rgba(255, 0, 128, 0.1)')
        fieldGradient.addColorStop(1, 'rgba(255, 0, 128, 0)')
        ctx.fillStyle = fieldGradient
        ctx.beginPath()
        ctx.arc(mousePosition.x, mousePosition.y, 100, 0, Math.PI * 2)
        ctx.fill()
      }

      animationId = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      window.removeEventListener('resize', resizeCanvas)
      cancelAnimationFrame(animationId)
    }
  }, [mousePosition, quantumNodes])

  // Mouse tracking
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY })
    }

    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [])

  // Real-time metrics updates
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date())
      setLiveMetrics(prev => ({
        quantumProcessors: prev.quantumProcessors + Math.floor(Math.random() * 10) - 5,
        parallelRealities: prev.parallelRealities + Math.floor(Math.random() * 8) - 4,
        neuralSynapses: prev.neuralSynapses + Math.floor(Math.random() * 100) - 50,
        dimensionalGateways: prev.dimensionalGateways + Math.floor(Math.random() * 3) - 1,
        consciousnessStreams: prev.consciousnessStreams + Math.floor(Math.random() * 20) - 10,
        quantumEntanglements: prev.quantumEntanglements + Math.floor(Math.random() * 15) - 7,
        timelineAnalyses: prev.timelineAnalyses + Math.floor(Math.random() * 12) - 6,
        multiverseConnections: prev.multiverseConnections + Math.floor(Math.random() * 5) - 2
      }))
    }, 1500)

    return () => clearInterval(interval)
  }, [])

  const handleSearch = async () => {
    if (!searchQuery.trim()) return

    setIsProcessing(true)
    setShowResults(false)

    // Simulate advanced quantum processing
    await new Promise(resolve => setTimeout(resolve, 3500))

    setIsProcessing(false)
    setShowResults(true)
  }

  const intelligenceCapabilities = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "Quantum Consciousness Mapping",
      description: "Multi-dimensional consciousness analysis across parallel realities with 99.8% quantum coherence",
      confidence: 99.8,
      dimensions: 17,
      color: "from-cyan-500 to-blue-600"
    },
    {
      icon: <Satellite className="w-8 h-8" />,
      title: "Hyperspace Phone Intelligence",
      description: "Advanced carrier detection with dimensional signal tracing and quantum network topology mapping",
      confidence: 99.2,
      dimensions: 15,
      color: "from-purple-500 to-pink-600"
    },
    {
      icon: <Network className="w-8 h-8" />,
      title: "Neural Email Matrix Analysis",
      description: "Quantum encryption breaking with temporal email tracking across multiple timeline branches",
      confidence: 98.7,
      dimensions: 14,
      color: "from-green-500 to-emerald-600"
    },
    {
      icon: <Fingerprint className="w-8 h-8" />,
      title: "Bio-Quantum Identity Synthesis",
      description: "Complete dimensional identity mapping with consciousness fingerprinting and reality anchoring",
      confidence: 97.9,
      dimensions: 16,
      color: "from-red-500 to-orange-600"
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Quantum Social Constellation",
      description: "Cross-dimensional social correlation with relationship quantum entanglement analysis",
      confidence: 96.8,
      dimensions: 13,
      color: "from-yellow-500 to-amber-600"
    },
    {
      icon: <Eye className="w-8 h-8" />,
      title: "Quantum Visual Recognition Matrix",
      description: "Advanced facial reconstruction with parallel reality matching and temporal analysis",
      confidence: 98.1,
      dimensions: 12,
      color: "from-indigo-500 to-violet-600"
    },
    {
      icon: <Lock className="w-8 h-8" />,
      title: "Dark Web Quantum Scanner",
      description: "Multi-layer dark web analysis with quantum anonymity breaking and shadow network mapping",
      confidence: 95.4,
      dimensions: 11,
      color: "from-slate-500 to-gray-600"
    },
    {
      icon: <Database className="w-8 h-8" />,
      title: "Universal Data Matrix",
      description: "Complete universal data synthesis across all dimensional databases and quantum storage systems",
      confidence: 97.6,
      dimensions: 18,
      color: "from-teal-500 to-cyan-600"
    },
    {
      icon: <Cpu className="w-8 h-8" />,
      title: "Quantum Threat Prediction",
      description: "Advanced threat matrix calculation with predictive quantum modeling and risk assessment",
      confidence: 98.9,
      dimensions: 19,
      color: "from-rose-500 to-red-600"
    },
    {
      icon: <Command className="w-8 h-8" />,
      title: "Temporal Analysis Engine",
      description: "Time-series intelligence analysis with quantum temporal mechanics and timeline correlation",
      confidence: 97.3,
      dimensions: 14,
      color: "from-blue-500 to-indigo-600"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Quantum Behavioral Synthesis",
      description: "Advanced behavioral pattern analysis with consciousness prediction and quantum psychology",
      confidence: 96.5,
      dimensions: 13,
      color: "from-orange-500 to-yellow-600"
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Multiversal Security Analysis",
      description: "Cross-dimensional security assessment with quantum encryption analysis and threat vectoring",
      confidence: 98.4,
      dimensions: 16,
      color: "from-emerald-500 to-green-600"
    }
  ]

  const mockResults: IntelligenceResult[] = [
    { category: "Quantum Location", data: "San Francisco, CA, USA (Dimensional Anchor: Earth-616)", confidence: 99.8, threat: 'low', sources: 247 },
    { category: "Carrier Matrix", data: "Quantum Wireless Networks (Multi-dimensional)", confidence: 99.2, threat: 'low', sources: 189 },
    { category: "Consciousness Type", data: "Baseline Human with Quantum Awareness", confidence: 97.9, threat: 'medium', sources: 156 },
    { category: "Parallel Identities", data: "47 dimensional variants detected", confidence: 96.8, threat: 'low', sources: 234 },
    { category: "Social Quantum State", data: "15 social profiles, 8 dimensional layers", confidence: 98.1, threat: 'low', sources: 178 },
    { category: "Temporal Footprint", data: "Digital presence across 12 timelines", confidence: 95.4, threat: 'medium', sources: 145 },
    { category: "Threat Assessment", data: "Quantum threat level: 2.1/10 (Negligible)", confidence: 98.9, threat: 'low', sources: 289 },
    { category: "Consciousness Rating", data: "Standard awareness, no quantum abilities", confidence: 97.3, threat: 'low', sources: 167 }
  ]

  return (
    <>
      <Head>
        <title>ULTIMATE Intelligence Platform - Quantum Consciousness Analysis</title>
        <meta name="description" content="Ultimate quantum intelligence platform with consciousness mapping and multiversal analysis" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-black text-white overflow-hidden relative">
        {/* Advanced Quantum Canvas Background */}
        <canvas
          ref={canvasRef}
          className="fixed inset-0 pointer-events-none"
          style={{ zIndex: 0 }}
        />

        {/* Navigation Header */}
        <nav className="relative z-50 flex items-center justify-between p-6 bg-black/20 backdrop-blur-xl border-b border-cyan-500/20">
          <div className="flex items-center space-x-4">
            <motion.div
              className="relative"
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            >
              <div className="w-12 h-12 rounded-full bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 flex items-center justify-center">
                <motion.div
                  className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center"
                  animate={{ rotate: -360 }}
                  transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                >
                  <Brain className="w-4 h-4 text-cyan-400" />
                </motion.div>
              </div>
            </motion.div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                ULTIMATE Platform
              </h1>
              <p className="text-xs text-gray-400">Quantum Consciousness Intelligence</p>
            </div>
          </div>

          {/* Real-time Status Bar */}
          <div className="flex items-center space-x-6 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
              <span className="text-green-400">Quantum Online</span>
            </div>
            <div className="text-cyan-400">
              Users: {activeUsers.toLocaleString()}
            </div>
            <div className="text-purple-400">
              Quantum Cores: {quantumCores}
            </div>
            <div className="text-pink-400">
              Dimensions: {parallelDimensions}
            </div>
            <div className="text-yellow-400">
              {currentTime.toLocaleTimeString()}
            </div>
          </div>
        </nav>

        {/* Advanced Live Metrics Dashboard */}
        <div className="relative z-40 px-6 py-4">
          <div className="grid grid-cols-4 md:grid-cols-8 gap-4">
            {[
              { label: "Quantum CPUs", value: liveMetrics.quantumProcessors, color: "cyan" },
              { label: "Parallel Realities", value: liveMetrics.parallelRealities, color: "purple" },
              { label: "Neural Synapses", value: liveMetrics.neuralSynapses, color: "pink" },
              { label: "Dimensional Gates", value: liveMetrics.dimensionalGateways, color: "green" },
              { label: "Consciousness Streams", value: liveMetrics.consciousnessStreams, color: "yellow" },
              { label: "Quantum Entanglements", value: liveMetrics.quantumEntanglements, color: "blue" },
              { label: "Timeline Analyses", value: liveMetrics.timelineAnalyses, color: "red" },
              { label: "Multiverse Links", value: liveMetrics.multiverseConnections, color: "indigo" }
            ].map((metric, index) => (
              <motion.div
                key={metric.label}
                className={`bg-black/40 backdrop-blur-xl rounded-lg p-3 border border-${metric.color}-500/30 hover:border-${metric.color}-400/60 transition-all duration-300`}
                whileHover={{ scale: 1.05, y: -2 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className={`text-xs text-${metric.color}-400 mb-1`}>{metric.label}</div>
                <div className={`text-lg font-bold text-${metric.color}-300`}>
                  {metric.value.toLocaleString()}
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="relative z-30 px-6 pb-20">
          {/* Hero Section */}
          <div className="max-w-6xl mx-auto text-center py-20">
            <motion.h1
              className="text-6xl md:text-8xl font-bold mb-8 bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1 }}
            >
              ULTIMATE
            </motion.h1>
            <motion.p
              className="text-xl md:text-2xl text-gray-300 mb-12 max-w-4xl mx-auto"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.2 }}
            >
              The most advanced quantum consciousness intelligence platform ever created. 
              Analyze across infinite dimensions with unprecedented accuracy and insight.
            </motion.p>

            {/* Advanced Search Interface */}
            <motion.div
              className="max-w-2xl mx-auto mb-16"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.4 }}
            >
              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Enter phone, email, username, or consciousness signature..."
                  className="w-full px-6 py-4 bg-black/40 backdrop-blur-xl border-2 border-cyan-500/30 rounded-2xl text-lg text-white placeholder-gray-400 focus:border-cyan-400 focus:outline-none transition-all duration-300"
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
                <motion.button
                  onClick={handleSearch}
                  className="absolute right-2 top-2 px-8 py-2 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-xl font-semibold hover:from-cyan-400 hover:to-purple-500 transition-all duration-300 flex items-center space-x-2"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  disabled={isProcessing}
                >
                  {isProcessing ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                      <span>Quantum Processing...</span>
                    </>
                  ) : (
                    <>
                      <Search className="w-4 h-4" />
                      <span>Launch Ultimate Analysis</span>
                    </>
                  )}
                </motion.button>
              </div>
            </motion.div>
          </div>

          {/* 12 Advanced Intelligence Capabilities */}
          <div className="max-w-7xl mx-auto mb-20">
            <h2 className="text-4xl font-bold text-center mb-16 bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              12 Quantum Intelligence Capabilities
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {intelligenceCapabilities.map((capability, index) => (
                <motion.div
                  key={capability.title}
                  className={`bg-gradient-to-br ${capability.color} p-0.5 rounded-2xl`}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.05, rotate: 1 }}
                >
                  <div className="bg-black/80 backdrop-blur-xl rounded-2xl p-6 h-full">
                    <div className="flex items-center justify-between mb-4">
                      <div className={`text-${capability.color.split('-')[1]}-400`}>
                        {capability.icon}
                      </div>
                      <div className="text-right">
                        <div className="text-sm text-gray-400">Confidence</div>
                        <div className="text-lg font-bold text-green-400">{capability.confidence}%</div>
                      </div>
                    </div>
                    <h3 className="text-lg font-bold mb-2 text-white">{capability.title}</h3>
                    <p className="text-sm text-gray-300 mb-4">{capability.description}</p>
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-cyan-400">Dimensions: {capability.dimensions}</span>
                      <span className="text-purple-400">Quantum Ready</span>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Advanced Results Display */}
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
                      Ultimate Quantum Analysis Results
                    </h3>
                    <motion.button
                      className="px-8 py-3 bg-gradient-to-r from-pink-500 to-red-600 rounded-xl font-semibold hover:from-pink-400 hover:to-red-500 transition-all duration-300 flex items-center space-x-2"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <Download className="w-5 h-5" />
                      <span>Get Full Quantum Report - $29.99</span>
                    </motion.button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {mockResults.map((result, index) => (
                      <motion.div
                        key={result.category}
                        className="bg-black/40 backdrop-blur-xl rounded-xl p-6 border border-gray-700/50"
                        initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <div className="flex items-center justify-between mb-4">
                          <h4 className="text-lg font-semibold text-cyan-400">{result.category}</h4>
                          <div className="flex items-center space-x-2">
                            <div className={`w-2 h-2 rounded-full ${
                              result.threat === 'low' ? 'bg-green-400' :
                              result.threat === 'medium' ? 'bg-yellow-400' : 'bg-red-400'
                            }`}></div>
                            <span className="text-sm text-gray-400">{result.confidence}%</span>
                          </div>
                        </div>
                        <div className="text-white filter blur-sm select-none">
                          {result.data}
                        </div>
                        <div className="mt-4 text-xs text-gray-400">
                          Sources: {result.sources} • Quantum Verified
                        </div>
                        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent rounded-xl flex items-center justify-center">
                          <div className="text-center">
                            <Lock className="w-8 h-8 text-cyan-400 mx-auto mb-2" />
                            <div className="text-sm text-cyan-400 font-semibold">Unlock Full Data</div>
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
                      <span>Quantum Secure</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Infinity className="w-4 h-4 text-purple-400" />
                      <span>Universal Intelligence</span>
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