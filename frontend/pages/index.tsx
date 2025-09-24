import Head from 'next/head'
import { useState, useEffect } from 'react'
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

interface Testimonial {
  name: string
  role: string
  company: string
  avatar: string
  content: string
  rating: number
}

interface Feature {
  icon: React.ReactNode
  title: string
  description: string
  gradient: string
}

interface LiveMetric {
  label: string
  value: string
  change: string
  trend: 'up' | 'down' | 'stable'
  icon: React.ReactNode
}

interface ThreatIndicator {
  level: 'low' | 'medium' | 'high' | 'critical'
  count: number
  change: number
}

export default function IntelligencePlatform() {
  const [currentTestimonial, setCurrentTestimonial] = useState(0)
  const [isVideoPlaying, setIsVideoPlaying] = useState(false)
  const [hoveredFeature, setHoveredFeature] = useState<number | null>(null)
  const [liveMetrics, setLiveMetrics] = useState<LiveMetric[]>([
    { label: 'Active Scans', value: '1,247', change: '+12%', trend: 'up', icon: <Activity className="w-4 h-4" /> },
    { label: 'Threats Detected', value: '89', change: '-5%', trend: 'down', icon: <Shield className="w-4 h-4" /> },
    { label: 'Intel Sources', value: '129', change: '+3', trend: 'up', icon: <Database className="w-4 h-4" /> },
    { label: 'Success Rate', value: '97.8%', change: '+0.2%', trend: 'up', icon: <Target className="w-4 h-4" /> }
  ])
  const [threatLevel, setThreatLevel] = useState<ThreatIndicator>({
    level: 'medium',
    count: 23,
    change: -8
  })

  // Live data simulation
  useEffect(() => {
    const interval = setInterval(() => {
      setLiveMetrics(prev => prev.map(metric => ({
        ...metric,
        value: (parseInt(metric.value.replace(/[,%]/g, '')) + Math.floor(Math.random() * 10 - 5)).toLocaleString(),
        change: `${Math.random() > 0.5 ? '+' : '-'}${(Math.random() * 10).toFixed(1)}%`
      })))
    }, 5000)
    return () => clearInterval(interval)
  }, [])

  const testimonials: Testimonial[] = [
    {
      name: "Dr. Sarah Chen",
      role: "Chief Security Officer",
      company: "CyberGuard International",
      avatar: "/api/placeholder/64/64",
      content: "This platform has transformed our threat intelligence operations. The AI-powered correlation and real-time analysis capabilities are unmatched in the industry.",
      rating: 5
    },
    {
      name: "Marcus Rodriguez",
      role: "Senior Intelligence Analyst",
      company: "Federal Investigation Bureau",
      avatar: "/api/placeholder/64/64",
      content: "The comprehensive OSINT capabilities and professional reporting have streamlined our investigations. This is the most advanced platform I've worked with.",
      rating: 5
    },
    {
      name: "Dr. Elena Volkov",
      role: "Director of Cyber Research",
      company: "Advanced Threat Research Lab",
      avatar: "/api/placeholder/64/64",
      content: "The machine learning algorithms and pattern recognition capabilities provide insights that traditional tools simply cannot match. Exceptional platform.",
      rating: 5
    }
  ]

  const enterpriseFeatures: Feature[] = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "AI-Powered Intelligence",
      description: "Advanced machine learning algorithms automatically correlate data patterns, identify relationships, and predict threats with 97.8% accuracy.",
      gradient: "from-purple-500 to-pink-500"
    },
    {
      icon: <Layers className="w-8 h-8" />,
      title: "Multi-Source Aggregation",
      description: "Seamlessly integrate intelligence from 129+ sources including social media, dark web, public records, and proprietary threat feeds.",
      gradient: "from-blue-500 to-cyan-500"
    },
    {
      icon: <Radar className="w-8 h-8" />,
      title: "Real-Time Threat Detection",
      description: "Continuous monitoring with instant alerting on emerging threats, suspicious activities, and security indicators.",
      gradient: "from-red-500 to-orange-500"
    },
    {
      icon: <Network className="w-8 h-8" />,
      title: "Advanced Analytics",
      description: "Interactive visualizations, network graphs, and geospatial mapping provide comprehensive situational awareness.",
      gradient: "from-green-500 to-emerald-500"
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Enterprise Security",
      description: "Bank-grade encryption, role-based access control, and comprehensive audit logging ensure maximum security.",
      gradient: "from-indigo-500 to-purple-500"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Lightning Performance",
      description: "Sub-second response times with parallel processing architecture that scales to handle enterprise workloads.",
      gradient: "from-yellow-500 to-orange-500"
    }
  ]

  const industryLeaders = [
    { name: "Fortune 500", count: "87%" },
    { name: "Government Agencies", count: "120+" },
    { name: "Security Firms", count: "500+" },
    { name: "Law Enforcement", count: "200+" }
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length)
    }, 5000)
    return () => clearInterval(interval)
  }, [testimonials.length])

  return (
    <>
      <Head>
        <title>IntelliGather Pro - Enterprise Intelligence Platform | Advanced OSINT & Threat Analysis</title>
        <meta name="description" content="The world's most advanced intelligence gathering platform. AI-powered OSINT, real-time threat detection, and comprehensive analytics trusted by Fortune 500 companies and government agencies." />
        <meta name="keywords" content="intelligence platform, OSINT, threat intelligence, cybersecurity, AI analytics, enterprise security, real-time monitoring" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-black text-white relative overflow-hidden">
        {/* Advanced Animated Background */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute inset-0 bg-gradient-to-br from-black via-slate-900/90 to-blue-900/20" />
          
          {/* Animated Grid */}
          <div className="absolute inset-0 bg-[linear-gradient(rgba(59,130,246,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.1)_1px,transparent_1px)] bg-[size:100px_100px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,black,transparent)]" />
          
          {/* Floating Elements */}
          <div className="absolute top-1/4 left-1/6 w-2 h-2 bg-blue-400 rounded-full animate-pulse opacity-60" />
          <div className="absolute top-1/3 right-1/4 w-1 h-1 bg-purple-400 rounded-full animate-ping opacity-40" />
          <div className="absolute bottom-1/3 left-1/3 w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse opacity-50" />
          
          {/* Scanning Lines Effect */}
          <div className="absolute inset-0">
            <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-blue-500/50 to-transparent animate-scan-horizontal" />
            <div className="absolute bottom-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-purple-500/50 to-transparent animate-scan-horizontal-reverse" />
          </div>
        </div>

        {/* Advanced Navigation */}
        <nav className="relative z-50 bg-black/60 backdrop-blur-xl border-b border-slate-800/50">
          <div className="max-w-8xl mx-auto px-6 lg:px-8">
            <div className="flex justify-between items-center h-20">
              <div className="flex items-center space-x-4">
                <div className="relative">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 via-purple-500 to-cyan-500 rounded-2xl flex items-center justify-center">
                    <Radar className="w-7 h-7 text-white animate-pulse" />
                  </div>
                  <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full animate-ping" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
                    IntelliGather Pro
                  </h1>
                  <p className="text-xs text-slate-400 font-medium">Enterprise Intelligence Platform</p>
                </div>
              </div>
              
              {/* Live Metrics Bar */}
              <div className="hidden lg:flex items-center space-x-8">
                {liveMetrics.map((metric, index) => (
                  <div key={index} className="flex items-center space-x-2 px-3 py-1.5 bg-slate-900/60 rounded-lg border border-slate-700/50">
                    {metric.icon}
                    <div className="text-xs">
                      <div className="text-white font-semibold">{metric.value}</div>
                      <div className={`text-xs ${metric.trend === 'up' ? 'text-green-400' : metric.trend === 'down' ? 'text-red-400' : 'text-yellow-400'}`}>
                        {metric.change}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex items-center space-x-4">
                <div className="hidden md:flex items-center space-x-6">
                  <a href="#intelligence" className="text-slate-300 hover:text-white transition-all duration-300 font-medium">Intelligence</a>
                  <a href="#platform" className="text-slate-300 hover:text-white transition-all duration-300 font-medium">Platform</a>
                  <a href="#enterprise" className="text-slate-300 hover:text-white transition-all duration-300 font-medium">Enterprise</a>
                  <a href="/dashboard" className="text-slate-300 hover:text-white transition-all duration-300 font-medium">Dashboard</a>
                </div>
                
                <div className="flex items-center space-x-3">
                  <button className="text-slate-300 hover:text-white transition-all duration-300 px-4 py-2 rounded-lg hover:bg-slate-800/50">
                    Sign In
                  </button>
                  <button className="bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 text-white px-6 py-2.5 rounded-xl font-semibold hover:from-blue-700 hover:via-purple-700 hover:to-cyan-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105">
                    Start Intelligence Ops
                  </button>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section - Enterprise Grade */}
        <section className="relative py-24 lg:py-32">
          <div className="max-w-8xl mx-auto px-6 lg:px-8">
            <div className="grid lg:grid-cols-12 gap-16 items-center">
              <div className="lg:col-span-7 space-y-10">
                {/* Status Indicator */}
                <div className="inline-flex items-center space-x-3 bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/30 rounded-full px-6 py-3">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                  <span className="text-sm text-green-300 font-semibold">SYSTEM OPERATIONAL - 99.97% UPTIME</span>
                  <CheckCircle className="w-4 h-4 text-green-400" />
                </div>
                
                {/* Main Headline */}
                <div className="space-y-6">
                  <h1 className="text-6xl lg:text-8xl font-black leading-none tracking-tight">
                    <span className="block text-white">NEXT-GEN</span>
                    <span className="block bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                      INTELLIGENCE
                    </span>
                    <span className="block text-white">PLATFORM</span>
                  </h1>
                  
                  <p className="text-xl lg:text-2xl text-slate-300 leading-relaxed max-w-3xl">
                    Harness the power of <span className="text-blue-400 font-semibold">AI-driven analysis</span>, 
                    <span className="text-purple-400 font-semibold"> real-time threat detection</span>, and 
                    <span className="text-cyan-400 font-semibold"> comprehensive OSINT capabilities</span> 
                    in the world's most advanced intelligence gathering ecosystem.
                  </p>
                </div>

                {/* Enterprise Stats */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="text-center p-4 bg-slate-900/30 rounded-xl border border-slate-700/50">
                    <div className="text-3xl font-bold text-blue-400">129+</div>
                    <div className="text-sm text-slate-400">Intel Sources</div>
                  </div>
                  <div className="text-center p-4 bg-slate-900/30 rounded-xl border border-slate-700/50">
                    <div className="text-3xl font-bold text-purple-400">97.8%</div>
                    <div className="text-sm text-slate-400">Accuracy Rate</div>
                  </div>
                  <div className="text-center p-4 bg-slate-900/30 rounded-xl border border-slate-700/50">
                    <div className="text-3xl font-bold text-cyan-400">&lt;0.5s</div>
                    <div className="text-sm text-slate-400">Response Time</div>
                  </div>
                  <div className="text-center p-4 bg-slate-900/30 rounded-xl border border-slate-700/50">
                    <div className="text-3xl font-bold text-green-400">500M+</div>
                    <div className="text-sm text-slate-400">Data Points</div>
                  </div>
                </div>

                {/* CTA Buttons */}
                <div className="flex flex-col sm:flex-row gap-4">
                  <button className="bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:from-blue-700 hover:via-purple-700 hover:to-cyan-700 transition-all duration-300 shadow-2xl hover:shadow-3xl transform hover:scale-105 flex items-center justify-center space-x-3">
                    <Zap className="w-6 h-6" />
                    <span>Launch Intelligence Ops</span>
                    <ArrowRight className="w-5 h-5" />
                  </button>
                  
                  <button className="border-2 border-slate-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:border-slate-500 hover:bg-slate-800/50 transition-all duration-300 flex items-center justify-center space-x-3">
                    <Play className="w-5 h-5" />
                    <span>Watch Platform Demo</span>
                  </button>
                </div>

                {/* Trust Indicators */}
                <div className="pt-8">
                  <p className="text-sm text-slate-500 mb-4">TRUSTED BY INDUSTRY LEADERS</p>
                  <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                    {industryLeaders.map((leader, index) => (
                      <div key={index} className="text-center">
                        <div className="text-lg font-bold text-white">{leader.count}</div>
                        <div className="text-xs text-slate-400">{leader.name}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Live Dashboard Preview */}
              <div className="lg:col-span-5">
                <div className="relative">
                  {/* Dashboard Frame */}
                  <div className="bg-gradient-to-br from-slate-900/90 to-slate-800/90 rounded-2xl border border-slate-700/50 p-6 backdrop-blur-xl shadow-2xl">
                    {/* Dashboard Header */}
                    <div className="flex items-center justify-between mb-6">
                      <div className="flex items-center space-x-3">
                        <div className="w-3 h-3 bg-red-400 rounded-full" />
                        <div className="w-3 h-3 bg-yellow-400 rounded-full" />
                        <div className="w-3 h-3 bg-green-400 rounded-full" />
                        <span className="text-sm text-slate-400 ml-4">Live Intelligence Dashboard</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                        <span className="text-xs text-green-400">LIVE</span>
                      </div>
                    </div>

                    {/* Live Threat Map */}
                    <div className="bg-black/40 rounded-xl p-4 mb-4">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-sm font-semibold text-white">Global Threat Activity</span>
                        <div className={`px-2 py-1 rounded text-xs font-bold ${
                          threatLevel.level === 'critical' ? 'bg-red-500/20 text-red-400' :
                          threatLevel.level === 'high' ? 'bg-orange-500/20 text-orange-400' :
                          threatLevel.level === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                          'bg-green-500/20 text-green-400'
                        }`}>
                          {threatLevel.level.toUpperCase()}
                        </div>
                      </div>
                      <div className="grid grid-cols-3 gap-2">
                        {[...Array(9)].map((_, i) => (
                          <div key={i} className={`h-8 rounded ${
                            Math.random() > 0.7 ? 'bg-red-500/30' :
                            Math.random() > 0.5 ? 'bg-yellow-500/30' :
                            'bg-green-500/30'
                          } animate-pulse`} style={{ animationDelay: `${i * 0.1}s` }} />
                        ))}
                      </div>
                    </div>

                    {/* Live Metrics */}
                    <div className="grid grid-cols-2 gap-3">
                      <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3">
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-blue-300">Active Scans</span>
                          <Activity className="w-4 h-4 text-blue-400" />
                        </div>
                        <div className="text-lg font-bold text-white">1,247</div>
                        <div className="text-xs text-green-400">+12% ↗</div>
                      </div>
                      <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-3">
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-purple-300">Intel Sources</span>
                          <Database className="w-4 h-4 text-purple-400" />
                        </div>
                        <div className="text-lg font-bold text-white">129</div>
                        <div className="text-xs text-green-400">+3 ↗</div>
                      </div>
                    </div>
                  </div>

                  {/* Floating Elements */}
                  <div className="absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-full blur-xl animate-pulse" />
                  <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-gradient-to-br from-cyan-500/20 to-green-500/20 rounded-full blur-xl animate-pulse delay-1000" />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Enterprise Features Section */}
        <section id="intelligence" className="relative py-24 lg:py-32">
          <div className="max-w-8xl mx-auto px-6 lg:px-8">
            <div className="text-center mb-20">
              <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/30 rounded-full px-6 py-3 mb-8">
                <Sparkles className="w-5 h-5 text-blue-400" />
                <span className="text-blue-300 font-semibold">ENTERPRISE INTELLIGENCE CAPABILITIES</span>
              </div>
              
              <h2 className="text-5xl lg:text-6xl font-black text-white mb-8">
                ADVANCED <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">AI-POWERED</span>
                <br />INTELLIGENCE OPERATIONS
              </h2>
              
              <p className="text-xl text-slate-300 max-w-4xl mx-auto leading-relaxed">
                Deploy cutting-edge machine learning algorithms and comprehensive OSINT capabilities 
                to gather, analyze, and correlate intelligence data from across the digital landscape 
                with unprecedented speed and accuracy.
              </p>
            </div>

            <div className="grid lg:grid-cols-3 gap-8">
              {enterpriseFeatures.map((feature, index) => (
                <div
                  key={index}
                  className="group relative p-8 bg-gradient-to-br from-slate-900/60 to-slate-800/60 rounded-2xl border border-slate-700/50 hover:border-slate-600/50 transition-all duration-500 hover:transform hover:scale-105"
                  onMouseEnter={() => setHoveredFeature(index)}
                  onMouseLeave={() => setHoveredFeature(null)}
                >
                  <div className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-10 rounded-2xl transition-opacity duration-500`} />
                  
                  <div className={`w-16 h-16 bg-gradient-to-br ${feature.gradient} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                    {feature.icon}
                  </div>
                  
                  <h3 className="text-2xl font-bold text-white mb-4 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-slate-300 group-hover:bg-clip-text transition-all duration-300">
                    {feature.title}
                  </h3>
                  
                  <p className="text-slate-300 leading-relaxed mb-6">
                    {feature.description}
                  </p>
                  
                  <div className="flex items-center text-slate-400 group-hover:text-white transition-colors duration-300">
                    <span className="text-sm font-medium">Learn More</span>
                    <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform duration-300" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Advanced Analytics Section */}
        <section id="platform" className="relative py-24 lg:py-32 bg-gradient-to-br from-slate-900/30 to-black/30">
          <div className="max-w-8xl mx-auto px-6 lg:px-8">
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              <div className="space-y-8">
                <div className="space-y-6">
                  <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-500/30 rounded-full px-6 py-3">
                    <BarChart3 className="w-5 h-5 text-purple-400" />
                    <span className="text-purple-300 font-semibold">ADVANCED ANALYTICS ENGINE</span>
                  </div>
                  
                  <h2 className="text-4xl lg:text-5xl font-black text-white">
                    REAL-TIME INTELLIGENCE
                    <br />
                    <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                      VISUALIZATION
                    </span>
                  </h2>
                  
                  <p className="text-xl text-slate-300 leading-relaxed">
                    Transform raw intelligence data into actionable insights with interactive visualizations, 
                    network graphs, geospatial mapping, and predictive analytics powered by advanced machine learning.
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-6">
                  <div className="bg-slate-900/40 rounded-xl p-6 border border-slate-700/50">
                    <div className="flex items-center space-x-3 mb-4">
                      <Network className="w-6 h-6 text-cyan-400" />
                      <span className="font-semibold text-white">Network Analysis</span>
                    </div>
                    <p className="text-sm text-slate-400">Interactive relationship mapping and entity correlation</p>
                  </div>
                  
                  <div className="bg-slate-900/40 rounded-xl p-6 border border-slate-700/50">
                    <div className="flex items-center space-x-3 mb-4">
                      <Map className="w-6 h-6 text-green-400" />
                      <span className="font-semibold text-white">Geospatial Intel</span>
                    </div>
                    <p className="text-sm text-slate-400">Global threat mapping and location-based analysis</p>
                  </div>
                  
                  <div className="bg-slate-900/40 rounded-xl p-6 border border-slate-700/50">
                    <div className="flex items-center space-x-3 mb-4">
                      <TrendingUp className="w-6 h-6 text-blue-400" />
                      <span className="font-semibold text-white">Predictive Analytics</span>
                    </div>
                    <p className="text-sm text-slate-400">AI-powered threat prediction and risk assessment</p>
                  </div>
                  
                  <div className="bg-slate-900/40 rounded-xl p-6 border border-slate-700/50">
                    <div className="flex items-center space-x-3 mb-4">
                      <Clock className="w-6 h-6 text-orange-400" />
                      <span className="font-semibold text-white">Timeline Analysis</span>
                    </div>
                    <p className="text-sm text-slate-400">Temporal correlation and event sequence analysis</p>
                  </div>
                </div>
              </div>

              <div className="relative">
                <div className="bg-gradient-to-br from-slate-900/90 to-slate-800/90 rounded-2xl border border-slate-700/50 p-8 backdrop-blur-xl">
                  <div className="mb-6">
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-lg font-bold text-white">Live Intelligence Feed</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                        <span className="text-xs text-green-400">STREAMING</span>
                      </div>
                    </div>
                    
                    <div className="space-y-3">
                      {[
                        { type: 'threat', severity: 'high', message: 'Suspicious domain registered: malware-c2.com', time: '2m ago' },
                        { type: 'intel', severity: 'medium', message: 'New social media profile linked to target entity', time: '5m ago' },
                        { type: 'alert', severity: 'low', message: 'Email validation completed: 94.7% confidence', time: '8m ago' }
                      ].map((item, index) => (
                        <div key={index} className="flex items-center space-x-3 p-3 bg-black/40 rounded-lg border border-slate-700/30">
                          <div className={`w-2 h-2 rounded-full ${
                            item.severity === 'high' ? 'bg-red-400' :
                            item.severity === 'medium' ? 'bg-yellow-400' :
                            'bg-green-400'
                          } animate-pulse`} />
                          <div className="flex-1">
                            <p className="text-sm text-white">{item.message}</p>
                            <p className="text-xs text-slate-400">{item.time}</p>
                          </div>
                          <ArrowRight className="w-4 h-4 text-slate-400" />
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-3 gap-4">
                    <div className="text-center p-3 bg-blue-500/10 rounded-lg border border-blue-500/30">
                      <div className="text-lg font-bold text-blue-400">47</div>
                      <div className="text-xs text-slate-400">Active Queries</div>
                    </div>
                    <div className="text-center p-3 bg-purple-500/10 rounded-lg border border-purple-500/30">
                      <div className="text-lg font-bold text-purple-400">1.2K</div>
                      <div className="text-xs text-slate-400">Data Points</div>
                    </div>
                    <div className="text-center p-3 bg-green-500/10 rounded-lg border border-green-500/30">
                      <div className="text-lg font-bold text-green-400">98.7%</div>
                      <div className="text-xs text-slate-400">Accuracy</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Testimonials Section */}
        <section id="testimonials" className="relative py-24 lg:py-32">
          <div className="max-w-8xl mx-auto px-6 lg:px-8">
            <div className="text-center mb-20">
              <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/30 rounded-full px-6 py-3 mb-8">
                <Award className="w-5 h-5 text-green-400" />
                <span className="text-green-300 font-semibold">TRUSTED BY PROFESSIONALS</span>
              </div>
              
              <h2 className="text-4xl lg:text-5xl font-black text-white mb-8">
                WHAT <span className="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">EXPERTS</span> SAY
              </h2>
            </div>

            <div className="relative">
              <div className="bg-gradient-to-br from-slate-900/60 to-slate-800/60 rounded-3xl border border-slate-700/50 p-12 backdrop-blur-xl">
                <div className="text-center max-w-4xl mx-auto">
                  <Quote className="w-12 h-12 text-slate-600 mx-auto mb-8" />
                  
                  <p className="text-2xl lg:text-3xl text-white leading-relaxed mb-8 font-medium">
                    "{testimonials[currentTestimonial]?.content}"
                  </p>
                  
                  <div className="flex items-center justify-center space-x-4 mb-8">
                    <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                      <User className="w-8 h-8 text-white" />
                    </div>
                    <div className="text-left">
                      <div className="text-xl font-bold text-white">{testimonials[currentTestimonial]?.name}</div>
                      <div className="text-slate-400">{testimonials[currentTestimonial]?.role}</div>
                      <div className="text-slate-500 text-sm">{testimonials[currentTestimonial]?.company}</div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-center space-x-2">
                    {testimonials.map((_, index) => (
                      <button
                        key={index}
                        className={`w-3 h-3 rounded-full transition-all duration-300 ${
                          index === currentTestimonial ? 'bg-blue-400 scale-125' : 'bg-slate-600 hover:bg-slate-500'
                        }`}
                        onClick={() => setCurrentTestimonial(index)}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Enterprise CTA Section */}
        <section id="enterprise" className="relative py-24 lg:py-32 bg-gradient-to-br from-blue-900/20 via-purple-900/20 to-cyan-900/20">
          <div className="max-w-8xl mx-auto px-6 lg:px-8">
            <div className="text-center space-y-12">
              <div className="space-y-8">
                <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 border border-blue-500/50 rounded-full px-8 py-4">
                  <Zap className="w-6 h-6 text-blue-400" />
                  <span className="text-blue-300 font-bold text-lg">READY FOR ENTERPRISE DEPLOYMENT</span>
                </div>
                
                <h2 className="text-5xl lg:text-7xl font-black text-white">
                  START YOUR
                  <br />
                  <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                    INTELLIGENCE
                  </span>
                  OPERATIONS
                </h2>
                
                <p className="text-2xl text-slate-300 max-w-4xl mx-auto leading-relaxed">
                  Join the elite network of intelligence professionals who rely on our platform 
                  for mission-critical operations and strategic intelligence gathering.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
                <button className="bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 text-white px-12 py-6 rounded-2xl font-bold text-xl hover:from-blue-700 hover:via-purple-700 hover:to-cyan-700 transition-all duration-300 shadow-2xl hover:shadow-3xl transform hover:scale-105 flex items-center space-x-4">
                  <Target className="w-7 h-7" />
                  <span>Deploy Intelligence Platform</span>
                  <ArrowRight className="w-6 h-6" />
                </button>
                
                <button className="border-2 border-slate-500 text-white px-12 py-6 rounded-2xl font-bold text-xl hover:border-slate-400 hover:bg-slate-800/50 transition-all duration-300 flex items-center space-x-4">
                  <MessageSquare className="w-6 h-6" />
                  <span>Schedule Enterprise Demo</span>
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 pt-16">
                <div className="text-center">
                  <div className="text-4xl font-bold text-blue-400 mb-2">24/7</div>
                  <div className="text-slate-300">Enterprise Support</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-purple-400 mb-2">99.97%</div>
                  <div className="text-slate-300">Uptime SLA</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-cyan-400 mb-2">SOC 2</div>
                  <div className="text-slate-300">Compliance Ready</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="relative bg-black/80 border-t border-slate-800/50">
          <div className="max-w-8xl mx-auto px-6 lg:px-8 py-16">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
              <div className="space-y-6">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 via-purple-500 to-cyan-500 rounded-xl flex items-center justify-center">
                    <Radar className="w-6 h-6 text-white" />
                  </div>
                  <span className="text-xl font-bold text-white">IntelliGather Pro</span>
                </div>
                <p className="text-slate-400 leading-relaxed">
                  The world's most advanced intelligence gathering platform for professionals 
                  and enterprises demanding the highest level of precision and security.
                </p>
              </div>
              
              <div>
                <h4 className="font-bold text-white mb-6">Platform</h4>
                <ul className="space-y-3">
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Intelligence Sources</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Real-time Analytics</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Threat Detection</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">API Documentation</a></li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-bold text-white mb-6">Enterprise</h4>
                <ul className="space-y-3">
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Security & Compliance</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Custom Deployment</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Professional Services</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">24/7 Support</a></li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-bold text-white mb-6">Resources</h4>
                <ul className="space-y-3">
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Documentation</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Training Center</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Community</a></li>
                  <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Contact</a></li>
                </ul>
              </div>
            </div>
            
            <div className="border-t border-slate-800 mt-16 pt-8 flex flex-col md:flex-row justify-between items-center">
              <p className="text-slate-500 text-sm">
                © 2024 IntelliGather Pro. All rights reserved. Enterprise Intelligence Platform.
              </p>
              <div className="flex items-center space-x-6 mt-4 md:mt-0">
                <a href="#" className="text-slate-500 hover:text-white transition-colors text-sm">Privacy Policy</a>
                <a href="#" className="text-slate-500 hover:text-white transition-colors text-sm">Terms of Service</a>
                <a href="#" className="text-slate-500 hover:text-white transition-colors text-sm">Security</a>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}