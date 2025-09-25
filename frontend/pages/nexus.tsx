import Head from 'next/head'
import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Brain, Atom, Lock, CheckCircle, Shield, Award, Zap as ZapIcon, Orbit,
  Smartphone, Mail, Users, Image, Globe, User, Database, Network
} from 'lucide-react'

// NEXUS - Revolutionary Quantum Intelligence Command Center
export default function QuantumNexus() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchType, setSearchType] = useState('nexus-core')
  const [isSearching, setIsSearching] = useState(false)
  const [searchResults, setSearchResults] = useState(null)
  const [showResults, setShowResults] = useState(false)
  const [aiProcessing, setAiProcessing] = useState(false)
  const [quantumField, setQuantumField] = useState(false)
  const canvasRef = useRef(null)

  // Ultra-Advanced Nexus Metrics
  const [nexusMetrics, setNexusMetrics] = useState({
    quantumProcessors: 12847,
    parallelRealities: 7834,
    quantumEntanglement: 99.7,
    aiEvolution: 97.4,
    cosmicIntelligence: 99.1,
    multiverseMapping: 94.8,
    neuralClusters: 45629,
    darkMatterNodes: 2847
  })

  // Next-Gen NEXUS Capabilities
  const nexusCapabilities = [
    { 
      id: 'nexus-core', 
      name: 'NEXUS Core Matrix', 
      icon: <Atom className="w-12 h-12" />, 
      placeholder: 'Universal quantum nexus analysis...',
      description: 'Multi-dimensional intelligence synthesis across infinite parallel realities',
      gradient: 'from-cyan-200 via-blue-300 to-indigo-500',
      confidence: 99.8
    },
    { 
      id: 'quantum-phone', 
      name: 'Quantum Phone Intelligence', 
      icon: <Smartphone className="w-12 h-12" />, 
      placeholder: 'Quantum phone analysis - parallel reality mapping...',
      description: 'Advanced carrier detection with quantum location tracking across dimensions',
      gradient: 'from-purple-200 via-pink-300 to-red-400',
      confidence: 99.2
    },
    { 
      id: 'neural-email', 
      name: 'Neural Email Matrix', 
      icon: <Mail className="w-12 h-12" />, 
      placeholder: 'Multi-dimensional email trace analysis...',
      description: 'AI-powered breach prediction with quantum encryption breaking capabilities',
      gradient: 'from-green-200 via-emerald-300 to-teal-500',
      confidence: 98.7
    },
    { 
      id: 'bio-identity', 
      name: 'Bio-Quantum Identity Mapping', 
      icon: <User className="w-12 h-12" />, 
      placeholder: 'Universal identity quantum mapping...',
      description: 'Complete dimensional identity synthesis with consciousness pattern analysis',
      gradient: 'from-orange-200 via-amber-300 to-yellow-400',
      confidence: 97.9
    },
    { 
      id: 'social-web', 
      name: 'Quantum Social Network', 
      icon: <Users className="w-12 h-12" />, 
      placeholder: 'Social quantum entanglement mapping...',
      description: 'Cross-dimensional social correlation with relationship quantum analysis',
      gradient: 'from-rose-200 via-pink-300 to-fuchsia-500',
      confidence: 96.8
    },
    { 
      id: 'visual-quantum', 
      name: 'Quantum Visual Recognition', 
      icon: <Image className="w-12 h-12" />, 
      placeholder: 'Multi-dimensional image quantum analysis...',
      description: 'Advanced facial reconstruction with parallel reality image matching',
      gradient: 'from-violet-200 via-purple-300 to-indigo-500',
      confidence: 98.1
    },
    { 
      id: 'darkweb-nexus', 
      name: 'Dark Web NEXUS Scanner', 
      icon: <Globe className="w-12 h-12" />, 
      placeholder: 'Deep dark web quantum intelligence...',
      description: 'Multi-layer dark web analysis with quantum anonymity breaking',
      gradient: 'from-slate-300 via-gray-400 to-zinc-500',
      confidence: 95.4
    },
    { 
      id: 'data-nexus', 
      name: 'NEXUS Data Matrix', 
      icon: <Database className="w-12 h-12" />, 
      placeholder: 'Universal data nexus correlation...',
      description: 'Quantum data synthesis across all dimensional databases',
      gradient: 'from-blue-200 via-cyan-300 to-sky-500',
      confidence: 97.6
    }
  ]

  // Advanced Quantum Canvas Animation
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const particles = []
    const quantumNodes = []

    // Generate advanced particles
    for (let i = 0; i < 180; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.6,
        vy: (Math.random() - 0.5) * 0.6,
        size: Math.random() * 3 + 1,
        opacity: Math.random() * 0.8 + 0.2,
        color: `hsl(${Math.random() * 60 + 180}, 80%, 70%)`,
        quantumPhase: Math.random() * Math.PI * 2
      })
    }

    // Generate quantum nodes
    for (let i = 0; i < 10; i++) {
      quantumNodes.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 50 + 30,
        pulsePhase: Math.random() * Math.PI * 2,
        energy: Math.random() * 100 + 50
      })
    }

    let animationId
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Quantum background
      const gradient = ctx.createRadialGradient(
        canvas.width / 2, canvas.height / 2, 0,
        canvas.width / 2, canvas.height / 2, canvas.width / 2
      )
      gradient.addColorStop(0, 'rgba(8, 15, 35, 0.95)')
      gradient.addColorStop(0.5, 'rgba(15, 23, 50, 0.8)')
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0.9)')
      ctx.fillStyle = gradient
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Update particles
      particles.forEach((particle, index) => {
        particle.x += particle.vx
        particle.y += particle.vy
        particle.quantumPhase += 0.03

        if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1
        if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1

        const quantumSize = particle.size + Math.sin(particle.quantumPhase) * 1.5
        ctx.save()
        ctx.globalAlpha = particle.opacity
        ctx.fillStyle = particle.color
        ctx.shadowBlur = 12
        ctx.shadowColor = particle.color
        ctx.beginPath()
        ctx.arc(particle.x, particle.y, quantumSize, 0, Math.PI * 2)
        ctx.fill()
        ctx.restore()

        // Quantum connections
        particles.slice(index + 1).forEach(otherParticle => {
          const dist = Math.sqrt(
            (particle.x - otherParticle.x) ** 2 + (particle.y - otherParticle.y) ** 2
          )
          if (dist < 80) {
            ctx.save()
            ctx.globalAlpha = (80 - dist) / 80 * 0.3
            ctx.strokeStyle = `hsl(${200 + Math.sin(Date.now() * 0.001) * 40}, 70%, 60%)`
            ctx.lineWidth = 1.5
            ctx.beginPath()
            ctx.moveTo(particle.x, particle.y)
            ctx.lineTo(otherParticle.x, otherParticle.y)
            ctx.stroke()
            ctx.restore()
          }
        })
      })

      // Quantum nodes
      quantumNodes.forEach(node => {
        node.pulsePhase += 0.02
        const pulseSize = Math.sin(node.pulsePhase) * 12 + node.radius

        ctx.save()
        ctx.globalAlpha = 0.5
        ctx.strokeStyle = `hsl(${120 + Math.sin(node.pulsePhase) * 40}, 80%, 60%)`
        ctx.lineWidth = 2
        ctx.shadowBlur = 25
        ctx.shadowColor = ctx.strokeStyle
        ctx.beginPath()
        ctx.arc(node.x, node.y, pulseSize, 0, Math.PI * 2)
        ctx.stroke()
        
        ctx.fillStyle = `hsla(${180 + Math.sin(node.pulsePhase * 2) * 30}, 80%, 70%, 0.4)`
        ctx.beginPath()
        ctx.arc(node.x, node.y, pulseSize * 0.3, 0, Math.PI * 2)
        ctx.fill()
        ctx.restore()
      })

      animationId = requestAnimationFrame(animate)
    }

    animate()
    return () => cancelAnimationFrame(animationId)
  }, [])

  // Live metrics updates
  useEffect(() => {
    const interval = setInterval(() => {
      setNexusMetrics(prev => ({
        quantumProcessors: prev.quantumProcessors + Math.floor(Math.random() * 20 - 10),
        parallelRealities: prev.parallelRealities + Math.floor(Math.random() * 15 - 7),
        quantumEntanglement: Math.min(99.9, Math.max(95.0, prev.quantumEntanglement + (Math.random() - 0.5) * 0.3)),
        aiEvolution: Math.min(99.9, Math.max(90.0, prev.aiEvolution + (Math.random() - 0.5) * 0.4)),
        cosmicIntelligence: Math.min(99.9, Math.max(95.0, prev.cosmicIntelligence + (Math.random() - 0.5) * 0.2)),
        multiverseMapping: Math.min(99.9, Math.max(85.0, prev.multiverseMapping + (Math.random() - 0.5) * 0.6)),
        neuralClusters: prev.neuralClusters + Math.floor(Math.random() * 50 + 10),
        darkMatterNodes: prev.darkMatterNodes + Math.floor(Math.random() * 8 - 4)
      }))
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  // Revolutionary processing function
  const executeNexusSearch = async () => {
    if (!searchQuery.trim()) return

    setIsSearching(true)
    setAiProcessing(true)
    setQuantumField(true)
    
    await new Promise(resolve => setTimeout(resolve, 4500))
    
    const selectedCapability = nexusCapabilities.find(cap => cap.id === searchType)
    
    const nexusResults = {
      query: searchQuery,
      capability: selectedCapability.name,
      confidence: selectedCapability.confidence,
      processing_time: '3.847s',
      quantum_dimensions: 15,
      parallel_analyses: 12,
      neural_pathways: Math.floor(Math.random() * 800 + 400),
      data_synthesis: Math.floor(Math.random() * 2000 + 1000),
      results: {
        primary_location: 'San Francisco Bay Area, CA, USA',
        quantum_carrier: 'Advanced Quantum Communications Inc.',
        dimensional_classification: 'Multi-Reality Quantum Device',
        bio_neural_profiles: Math.floor(Math.random() * 40 + 20),
        quantum_correlations: Math.floor(Math.random() * 30 + 15),
        molecular_signatures: Math.floor(Math.random() * 25 + 10),
        cosmic_resonance: 'Quantum-Synchronized',
        nexus_threat_level: 'Quantum-Secure',
        consciousness_pattern: 'Advanced Human Cognitive Matrix',
        universal_entanglement: `${Math.floor(Math.random() * 30 + 70)}%`,
        ai_evolution_stage: `Stage ${Math.floor(Math.random() * 3 + 4)}`
      }
    }

    setSearchResults(nexusResults)
    setIsSearching(false)
    setAiProcessing(false)
    setQuantumField(false)
    setShowResults(true)
  }

  const unlockNexusReport = () => {
    alert('🚀 NEXUS Quantum Intelligence Report - $19.99\n\n🌌 Complete Multi-Dimensional Analysis:\n• Full quantum consciousness mapping\n• All parallel reality correlations\n• Universal intelligence synthesis\n• Bio-neural pattern analysis\n• Cosmic resonance data\n• Dark matter intelligence\n• AI evolution staging\n\n💎 Premium NEXUS Access - Redirecting to secure quantum payment...')
  }

  const currentCapability = nexusCapabilities.find(cap => cap.id === searchType)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-indigo-950 relative overflow-hidden">
      <Head>
        <title>NEXUS - Quantum Intelligence Command Center | Revolutionary Multi-Dimensional Analysis</title>
        <meta name="description" content="NEXUS - Revolutionary quantum intelligence platform with multi-dimensional consciousness mapping" />
      </Head>

      {/* Quantum Field Canvas */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full"
        style={{ zIndex: 1 }}
      />

      {/* Dynamic Grid Overlay */}
      <div className="absolute inset-0 opacity-25" style={{ zIndex: 2 }}>
        <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="nexus-grid" width="100" height="100" patternUnits="userSpaceOnUse">
              <path d="M 100 0 L 0 0 0 100" fill="none" stroke="rgba(59, 130, 246, 0.4)" strokeWidth="1"/>
              <circle cx="50" cy="50" r="3" fill="rgba(34, 197, 94, 0.6)"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#nexus-grid)" />
        </svg>
      </div>

      {/* Revolutionary NEXUS Header */}
      <motion.header 
        className="relative z-50 bg-gradient-to-r from-slate-950/90 via-blue-950/90 to-indigo-950/90 backdrop-blur-2xl border-b border-cyan-400/40 shadow-2xl"
        initial={{ y: -120, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 1, ease: "easeOut" }}
      >
        <div className="max-w-8xl mx-auto px-8 py-6">
          <div className="flex items-center justify-between">
            <motion.div 
              className="flex items-center space-x-6"
              whileHover={{ scale: 1.02 }}
            >
              <div className="relative">
                <motion.div
                  className="w-20 h-20 rounded-full bg-gradient-to-r from-cyan-300 via-blue-400 to-purple-500 p-1"
                  animate={{
                    rotate: 360,
                    boxShadow: [
                      "0 0 30px rgba(59, 130, 246, 0.6)",
                      "0 0 50px rgba(34, 197, 94, 0.6)",
                      "0 0 40px rgba(168, 85, 247, 0.6)",
                      "0 0 60px rgba(234, 179, 8, 0.6)",
                      "0 0 30px rgba(59, 130, 246, 0.6)"
                    ]
                  }}
                  transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                >
                  <div className="w-full h-full rounded-full bg-slate-950 flex items-center justify-center">
                    <Atom className="w-10 h-10 text-cyan-300" />
                  </div>
                </motion.div>
                <motion.div
                  className="absolute inset-0 w-24 h-24 -m-2 border-2 border-cyan-300/30 rounded-full"
                  animate={{ rotate: -360 }}
                  transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
                />
                <motion.div
                  className="absolute inset-0 w-28 h-28 -m-4 border border-purple-300/20 rounded-full"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                />
              </div>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-300 via-blue-300 to-purple-400 bg-clip-text text-transparent">
                  NEXUS
                </h1>
                <p className="text-slate-300 text-lg">Quantum Intelligence Command Center</p>
                <p className="text-slate-400 text-sm">Multi-Dimensional Analysis Platform</p>
              </div>
            </motion.div>

            {/* Advanced Metrics Grid */}
            <div className="grid grid-cols-4 gap-4">
              <motion.div 
                className="text-center p-3 bg-gradient-to-r from-cyan-400/10 to-blue-500/10 rounded-xl border border-cyan-400/40 backdrop-blur-xl"
                whileHover={{ scale: 1.05, boxShadow: "0 0 25px rgba(59, 130, 246, 0.4)" }}
              >
                <div className="text-xl font-bold text-cyan-300">{nexusMetrics.quantumProcessors.toLocaleString()}</div>
                <div className="text-xs text-slate-400">Quantum CPUs</div>
              </motion.div>
              <motion.div 
                className="text-center p-3 bg-gradient-to-r from-purple-400/10 to-pink-500/10 rounded-xl border border-purple-400/40 backdrop-blur-xl"
                whileHover={{ scale: 1.05, boxShadow: "0 0 25px rgba(168, 85, 247, 0.4)" }}
              >
                <div className="text-xl font-bold text-purple-300">{nexusMetrics.parallelRealities.toLocaleString()}</div>
                <div className="text-xs text-slate-400">Parallel Realities</div>
              </motion.div>
              <motion.div 
                className="text-center p-3 bg-gradient-to-r from-green-400/10 to-emerald-500/10 rounded-xl border border-green-400/40 backdrop-blur-xl"
                whileHover={{ scale: 1.05, boxShadow: "0 0 25px rgba(34, 197, 94, 0.4)" }}
              >
                <div className="text-xl font-bold text-green-300">{nexusMetrics.quantumEntanglement.toFixed(1)}%</div>
                <div className="text-xs text-slate-400">Entanglement</div>
              </motion.div>
              <motion.div 
                className="text-center p-3 bg-gradient-to-r from-yellow-400/10 to-orange-500/10 rounded-xl border border-yellow-400/40 backdrop-blur-xl"
                whileHover={{ scale: 1.05, boxShadow: "0 0 25px rgba(234, 179, 8, 0.4)" }}
              >
                <div className="text-xl font-bold text-yellow-300">{nexusMetrics.aiEvolution.toFixed(1)}%</div>
                <div className="text-xs text-slate-400">AI Evolution</div>
              </motion.div>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main NEXUS Interface */}
      <main className="relative z-40 pt-16 pb-20">
        <div className="max-w-7xl mx-auto px-8">
          
          {/* NEXUS Command Center */}
          <motion.div 
            className="text-center mb-20"
            initial={{ opacity: 0, y: 60 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1.2, delay: 0.3 }}
          >
            <motion.h2 
              className="text-7xl font-bold mb-8 bg-gradient-to-r from-cyan-200 via-blue-300 to-purple-400 bg-clip-text text-transparent"
              animate={{
                backgroundPosition: ["0%", "100%", "0%"]
              }}
              transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
            >
              Quantum NEXUS
            </motion.h2>
            <motion.p 
              className="text-2xl text-slate-200 mb-12 max-w-4xl mx-auto leading-relaxed"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
            >
              Revolutionary multi-dimensional intelligence command center with quantum consciousness mapping, 
              temporal analysis, cosmic intelligence synthesis, and universal threat assessment.
            </motion.p>

            {/* NEXUS Capabilities Matrix */}
            <motion.div 
              className="max-w-6xl mx-auto"
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 1, duration: 0.6 }}
            >
              {/* Capability Selector */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
                {nexusCapabilities.map((capability) => (
                  <motion.button
                    key={capability.id}
                    onClick={() => setSearchType(capability.id)}
                    className={`p-5 rounded-2xl border-2 transition-all duration-300 ${
                      searchType === capability.id
                        ? `border-cyan-300 bg-gradient-to-r ${capability.gradient} bg-opacity-20 shadow-2xl`
                        : 'border-slate-600 bg-slate-900/60 hover:border-slate-500'
                    }`}
                    whileHover={{ scale: 1.03, y: -3 }}
                    whileTap={{ scale: 0.98 }}
                    style={{
                      boxShadow: searchType === capability.id ? '0 0 30px rgba(59, 130, 246, 0.3)' : 'none'
                    }}
                  >
                    <div className="flex flex-col items-center space-y-3">
                      <div className={`p-3 rounded-xl bg-gradient-to-r ${capability.gradient} bg-opacity-30`}>
                        {capability.icon}
                      </div>
                      <div className="text-lg font-bold text-white">{capability.name}</div>
                      <div className="text-xs text-slate-400 text-center leading-relaxed">{capability.description}</div>
                      <div className="text-xs text-green-300 font-bold">{capability.confidence}% Confidence</div>
                    </div>
                  </motion.button>
                ))}
              </div>

              {/* NEXUS Command Input */}
              <motion.div 
                className="relative mb-12"
                animate={quantumField ? { scale: [1, 1.02, 1] } : {}}
                transition={{ duration: 2.5, repeat: quantumField ? Infinity : 0 }}
              >
                <div className="relative">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder={currentCapability.placeholder}
                    className="w-full px-8 py-8 text-xl bg-slate-950/80 border-3 border-cyan-400/60 rounded-3xl 
                             text-white placeholder-slate-300 focus:outline-none focus:border-cyan-300 
                             backdrop-blur-2xl shadow-2xl transition-all duration-300"
                    style={{
                      boxShadow: quantumField ? '0 0 50px rgba(59, 130, 246, 0.4)' : '0 0 30px rgba(0, 0, 0, 0.3)'
                    }}
                  />
                  <motion.div
                    className="absolute right-6 top-1/2 transform -translate-y-1/2"
                    animate={aiProcessing ? { 
                      rotate: 360,
                      scale: [1, 1.2, 1]
                    } : {}}
                    transition={{ 
                      rotate: { duration: 1.5, repeat: aiProcessing ? Infinity : 0, ease: "linear" },
                      scale: { duration: 1, repeat: aiProcessing ? Infinity : 0 }
                    }}
                  >
                    <Brain className={`w-10 h-10 ${aiProcessing ? 'text-cyan-300' : 'text-slate-500'}`} />
                  </motion.div>
                </div>

                {/* NEXUS Processing Indicator */}
                <AnimatePresence>
                  {aiProcessing && (
                    <motion.div
                      className="absolute -bottom-16 left-0 right-0 text-center"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                    >
                      <div className="text-cyan-300 text-lg font-bold mb-2">
                        🧠 NEXUS Quantum AI Processing... Analyzing multi-dimensional consciousness patterns...
                      </div>
                      <motion.div
                        className="w-full h-2 bg-slate-800 rounded-full overflow-hidden"
                      >
                        <motion.div
                          className="h-full bg-gradient-to-r from-cyan-300 via-blue-400 to-purple-500"
                          initial={{ width: "0%" }}
                          animate={{ width: "100%" }}
                          transition={{ duration: 4.5, ease: "easeInOut" }}
                        />
                      </motion.div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>

              {/* NEXUS Launch Button */}
              <motion.button
                onClick={executeNexusSearch}
                disabled={isSearching || !searchQuery.trim()}
                className={`px-16 py-6 rounded-3xl font-bold text-xl transition-all duration-300 ${
                  isSearching || !searchQuery.trim()
                    ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                    : `bg-gradient-to-r ${currentCapability.gradient} text-white shadow-2xl hover:shadow-cyan-400/30`
                }`}
                whileHover={!isSearching && searchQuery.trim() ? { scale: 1.05, y: -3 } : {}}
                whileTap={!isSearching && searchQuery.trim() ? { scale: 0.95 } : {}}
                style={{
                  boxShadow: !isSearching && searchQuery.trim() ? '0 0 40px rgba(59, 130, 246, 0.5)' : 'none'
                }}
              >
                {isSearching ? (
                  <div className="flex items-center space-x-3">
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                    >
                      <Orbit className="w-8 h-8" />
                    </motion.div>
                    <span>NEXUS Quantum Processing...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-3">
                    <ZapIcon className="w-8 h-8" />
                    <span>Initialize NEXUS Analysis</span>
                  </div>
                )}
              </motion.button>
            </motion.div>
          </motion.div>

          {/* NEXUS Analysis Results */}
          <AnimatePresence>
            {showResults && searchResults && (
              <motion.div
                className="max-w-6xl mx-auto"
                initial={{ opacity: 0, y: 60, scale: 0.9 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -60, scale: 0.9 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
              >
                <div className="bg-gradient-to-r from-slate-950/95 via-blue-950/95 to-indigo-950/95 backdrop-blur-2xl rounded-3xl border-2 border-cyan-400/40 p-10 shadow-2xl">
                  
                  {/* Results Header */}
                  <div className="flex items-center justify-between mb-8">
                    <div>
                      <h3 className="text-3xl font-bold text-white mb-3">NEXUS Quantum Analysis Complete</h3>
                      <div className="flex items-center space-x-6 text-lg text-slate-300">
                        <span>Query: {searchResults.query}</span>
                        <span>•</span>
                        <span>Capability: {searchResults.capability}</span>
                        <span>•</span>
                        <span>Confidence: {searchResults.confidence}%</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-green-300 font-bold text-lg">Processing: {searchResults.processing_time}</div>
                      <div className="text-cyan-300">Dimensions: {searchResults.quantum_dimensions}</div>
                      <div className="text-purple-300">Pathways: {searchResults.neural_pathways}</div>
                    </div>
                  </div>

                  {/* Premium Results Preview */}
                  <div className="relative">
                    <div className="absolute inset-0 bg-gradient-to-r from-cyan-400/20 via-blue-500/20 to-purple-500/20 rounded-3xl z-10 backdrop-blur-md flex items-center justify-center">
                      <motion.div
                        className="text-center max-w-md"
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ delay: 0.4 }}
                      >
                        <div className="mb-6">
                          <Lock className="w-20 h-20 text-cyan-300 mx-auto mb-4" />
                          <h4 className="text-2xl font-bold text-white mb-3">NEXUS Premium Intelligence</h4>
                          <p className="text-slate-200 mb-6 leading-relaxed">Complete multi-dimensional quantum analysis with universal consciousness mapping</p>
                        </div>
                        <motion.button
                          onClick={unlockNexusReport}
                          className="px-10 py-4 bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 text-white font-bold rounded-2xl 
                                   shadow-2xl hover:shadow-cyan-400/30 transition-all duration-300 text-lg"
                          whileHover={{ scale: 1.05, boxShadow: "0 0 30px rgba(59, 130, 246, 0.5)" }}
                          whileTap={{ scale: 0.95 }}
                        >
                          🚀 Unlock NEXUS Report - $19.99
                        </motion.button>
                        <div className="flex items-center justify-center space-x-6 mt-6 text-sm text-slate-300">
                          <div className="flex items-center space-x-2">
                            <CheckCircle className="w-5 h-5 text-green-300" />
                            <span>Instant Access</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Shield className="w-5 h-5 text-blue-300" />
                            <span>Quantum Secure</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Award className="w-5 h-5 text-purple-300" />
                            <span>Universal Intelligence</span>
                          </div>
                        </div>
                      </motion.div>
                    </div>

                    {/* Blurred Comprehensive Results */}
                    <div className="filter blur-sm opacity-50 grid grid-cols-1 md:grid-cols-2 gap-8 p-8 bg-slate-900/40 rounded-3xl">
                      <div className="space-y-5">
                        <div className="flex items-center justify-between p-4 bg-slate-800/60 rounded-xl">
                          <span className="text-slate-200 font-medium">Primary Location:</span>
                          <span className="text-green-300 font-bold">{searchResults.results.primary_location}</span>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-slate-800/60 rounded-xl">
                          <span className="text-slate-200 font-medium">Quantum Carrier:</span>
                          <span className="text-blue-300 font-bold">{searchResults.results.quantum_carrier}</span>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-slate-800/60 rounded-xl">
                          <span className="text-slate-200 font-medium">Classification:</span>
                          <span className="text-purple-300 font-bold">{searchResults.results.dimensional_classification}</span>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-slate-800/60 rounded-xl">
                          <span className="text-slate-200 font-medium">Bio-Neural Profiles:</span>
                          <span className="text-orange-300 font-bold">{searchResults.results.bio_neural_profiles}</span>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-slate-800/60 rounded-xl">
                          <span className="text-slate-200 font-medium">Quantum Correlations:</span>
                          <span className="text-cyan-300 font-bold">{searchResults.results.quantum_correlations}</span>
                        </div>
                      </div>
                      <div className="space-y-5">
                        <div className="flex items-center justify-between p-4 bg-slate-800/60 rounded-xl">
                          <span className="text-slate-200 font-medium">Molecular Signatures:</span>
                          <span className="text-pink-300 font-bold">{searchResults.results.molecular_signatures}</span>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-slate-800/60 rounded-xl">
                          <span className="text-slate-200 font-medium">Cosmic Resonance:</span>
                          <span className="text-yellow-300 font-bold">{searchResults.results.cosmic_resonance}</span>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-slate-800/60 rounded-xl">
                          <span className="text-slate-200 font-medium">Threat Level:</span>
                          <span className="text-green-300 font-bold">{searchResults.results.nexus_threat_level}</span>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-slate-800/60 rounded-xl">
                          <span className="text-slate-200 font-medium">Consciousness Pattern:</span>
                          <span className="text-rose-300 font-bold">{searchResults.results.consciousness_pattern}</span>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-slate-800/60 rounded-xl">
                          <span className="text-slate-200 font-medium">Universal Entanglement:</span>
                          <span className="text-emerald-300 font-bold">{searchResults.results.universal_entanglement}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Processing Statistics */}
                  <div className="mt-10 grid grid-cols-2 md:grid-cols-4 gap-6">
                    <div className="text-center p-5 bg-cyan-400/10 rounded-2xl border border-cyan-400/40">
                      <div className="text-2xl font-bold text-cyan-300">{searchResults.neural_pathways}</div>
                      <div className="text-sm text-slate-400">Neural Pathways</div>
                    </div>
                    <div className="text-center p-5 bg-purple-400/10 rounded-2xl border border-purple-400/40">
                      <div className="text-2xl font-bold text-purple-300">{searchResults.parallel_analyses}</div>
                      <div className="text-sm text-slate-400">Parallel Analyses</div>
                    </div>
                    <div className="text-center p-5 bg-green-400/10 rounded-2xl border border-green-400/40">
                      <div className="text-2xl font-bold text-green-300">{searchResults.quantum_dimensions}</div>
                      <div className="text-sm text-slate-400">Quantum Dimensions</div>
                    </div>
                    <div className="text-center p-5 bg-orange-400/10 rounded-2xl border border-orange-400/40">
                      <div className="text-2xl font-bold text-orange-300">{searchResults.confidence}%</div>
                      <div className="text-sm text-slate-400">Confidence Level</div>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Extended NEXUS Metrics Dashboard */}
          <motion.div 
            className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.5, duration: 1 }}
          >
            <motion.div 
              className="text-center p-8 bg-gradient-to-r from-cyan-400/10 to-blue-500/10 rounded-3xl border border-cyan-400/40 backdrop-blur-2xl"
              whileHover={{ scale: 1.05, boxShadow: "0 0 40px rgba(59, 130, 246, 0.4)" }}
            >
              <div className="text-4xl font-bold text-cyan-300 mb-3">{nexusMetrics.neuralClusters.toLocaleString()}</div>
              <div className="text-sm text-slate-300 mb-3">Neural Clusters</div>
              <div className="w-full bg-slate-800 rounded-full h-3">
                <motion.div 
                  className="bg-gradient-to-r from-cyan-300 to-blue-400 h-3 rounded-full"
                  initial={{ width: "0%" }}
                  animate={{ width: "92%" }}
                  transition={{ delay: 2, duration: 1.5 }}
                />
              </div>
            </motion.div>

            <motion.div 
              className="text-center p-8 bg-gradient-to-r from-purple-400/10 to-pink-500/10 rounded-3xl border border-purple-400/40 backdrop-blur-2xl"
              whileHover={{ scale: 1.05, boxShadow: "0 0 40px rgba(168, 85, 247, 0.4)" }}
            >
              <div className="text-4xl font-bold text-purple-300 mb-3">{nexusMetrics.darkMatterNodes.toLocaleString()}</div>
              <div className="text-sm text-slate-300">Dark Matter Nodes</div>
            </motion.div>

            <motion.div 
              className="text-center p-8 bg-gradient-to-r from-green-400/10 to-emerald-500/10 rounded-3xl border border-green-400/40 backdrop-blur-2xl"
              whileHover={{ scale: 1.05, boxShadow: "0 0 40px rgba(34, 197, 94, 0.4)" }}
            >
              <div className="text-4xl font-bold text-green-300 mb-3">{nexusMetrics.multiverseMapping.toFixed(1)}%</div>
              <div className="text-sm text-slate-300">Multiverse Mapping</div>
            </motion.div>

            <motion.div 
              className="text-center p-8 bg-gradient-to-r from-yellow-400/10 to-orange-500/10 rounded-3xl border border-yellow-400/40 backdrop-blur-2xl"
              whileHover={{ scale: 1.05, boxShadow: "0 0 40px rgba(234, 179, 8, 0.4)" }}
            >
              <div className="text-4xl font-bold text-yellow-300 mb-3">{nexusMetrics.cosmicIntelligence.toFixed(1)}%</div>
              <div className="text-sm text-slate-300">Cosmic Intelligence</div>
            </motion.div>
          </motion.div>

        </div>
      </main>

      {/* NEXUS Command Footer */}
      <motion.footer 
        className="relative z-40 bg-gradient-to-r from-slate-950/90 via-blue-950/90 to-indigo-950/90 backdrop-blur-2xl border-t border-cyan-400/40 py-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2 }}
      >
        <div className="max-w-8xl mx-auto px-8 text-center">
          <p className="text-slate-300 mb-6 text-lg">
            NEXUS Quantum Intelligence Command Center™ - Revolutionary Multi-Dimensional Analysis Platform | Enhanced by Universal Consciousness Mapping
          </p>
          <div className="flex justify-center space-x-12 text-slate-400">
            <span>Quantum Processing</span>
            <span>•</span>
            <span>Multi-Dimensional Analysis</span>
            <span>•</span>
            <span>Temporal Intelligence</span>
            <span>•</span>
            <span>Cosmic Consciousness Mapping</span>
            <span>•</span>
            <span>Universal Threat Assessment</span>
          </div>
        </div>
      </motion.footer>
    </div>
  )
}